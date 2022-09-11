## WindowManager Funktion Shit

# Window Flags
#   -   FLAG_MOVABLE			= (1 <<  0),    <- enables moving of window? two times?
#   -	FLAG_LIMIT				= (1 <<  1),    <- limits the movable area to wndMgrSetLimitBias, initial value is 0, 0, 0, 0
#   -	FLAG_SNAP				= (1 <<  2),    <- nothing
#   -	FLAG_DRAGABLE			= (1 <<  3),    <- can move window with mouse
#   -	FLAG_ATTACH				= (1 <<  4),    <- is window attached to another window? needed for choosing the right position
#   -	FLAG_RESTRICT_X			= (1 <<  5),    <- restricts movement to x axis of parent window
#   -	FLAG_RESTRICT_Y			= (1 <<  6),    <- restricts movement to y axis of parent window
#   -	FLAG_NOT_CAPTURE		= (1 <<  7),    <- disable mouse input
#   -	FLAG_FLOAT				= (1 <<  8),    <- if not set, it disabled SetTop()
#   -	FLAG_NOT_PICK			= (1 <<  9),    <- disable don't pick window even if its the top window
#   -	FLAG_IGNORE_SIZE		= (1 << 10),    <- ignore size of window and always chooses the top window
#   -	FLAG_RTL				= (1 << 11),    <- some python shit not used anymore

# HorizontalAlign wndMgr.*
#   - TEXT_HORIZONTAL_ALIGN_LEFT    HORIZONTAL_ALIGN_LEFT = 0
#   - TEXT_HORIZONTAL_ALIGN_CENTER  HORIZONTAL_ALIGN_CENTER = 1
#   - TEXT_HORIZONTAL_ALIGN_RIGHT   HORIZONTAL_ALIGN_RIGHT = 2

# VerticalAlign wndMgr.*
#   - TEXT_VERTICAL_ALIGN_TOP       VERTICAL_ALIGN_TOP = 0
#   - TEXT_VERTICAL_ALIGN_CENTER	VERTICAL_ALIGN_CENTER = 1
#   - TEXT_VERTICAL_ALIGN_BOTTOM	VERTICAL_ALIGN_BOTTOM = 2

# Stuff thats i need to know
# app.OnMouseMove->wndMgr.RunMouseMove(x, y)    <- global mouse xy position
# wndMgr.IsIn()                                 <- first window choosen by ScreenToClient 
# wndMgr.UpdateRect()                           <- refresh size and position to parent
# wndMgr.wndMgrSetOutlineFlag()                 <- draw outline around window on mouse over
# wndMgr.wndMgrIsDragging()                     <- is window being dragged?
# wndMgr.wndMgrGetMousePosition()               <- get global mouse position
# wndMgr.wndMgrGetMouseLocalPosition()          <- get mouse position relative to window

import ui, wndMgr, grp

import globals
from _utils import LogTxt, rect_collision

## Side Infos

# 1. Parenting
#	- we dont set parent on wndMgr!, we only use parent for its position
#	- we set parent name on our scene data object

from mouse_controller import mouse_controller

class scene_demo():
	# holds or scene data
	d_scene_data 	= {}

	# holds our demo data
	d_demo 			= {
		'objects' 					: {},
		'mouse_over_target' 		: None,
		'mouse_left_down_target' 		: None,
		'window_drag_target' 		: None,
	}
	
	scene_name 		= ''

	# the instance of our mouse over bar
	obj_mouse_over = None

	# the instance of our window drag bar
	obj_window_drag = None

	# the instance of our scene info text
	obj_scene_info = None

	obj_mouse_controller = None

	###########################################################
	class scene_object_mouse_over(ui.Bar):
		def __init__(self, target):
			ui.Bar.__init__(self)
			self.AddFlag('not_pick')
			self.target = target
			self.target_wnd = target('wnd')
			self.SetParent(self.target_wnd)
			self.SetSize(*(self.target_wnd.GetWidth(), self.target_wnd.GetHeight()))
			self.SetPosition(0, 0)
			self.Show()

	###########################################################
	# Start of SceneDataObject
	class scene_data_object():
		# the instance of our object control window
		wnd = None

		# the instance of our demo object
		obj_instance = None
		
		originals = {
			'position' : None,
			'size' : None,
		}

		def __init__(self, data, fn_mouse_left_button_down, fn_mouse_left_button_up, fn_mouse_over_window, fn_mouse_over_out_window, fn_on_move, fn_get_scene_object_data):
			self.__dict__ = data
			self.originals['position'] = (self.__dict__['x'], self.__dict__['y'])
			self.originals['size'] = (self.__dict__['width'], self.__dict__['height'])
			
			self.fn_on_move 				= fn_on_move
			self.fn_mouse_over_window 		= fn_mouse_over_window
			self.fn_mouse_over_out_window 	= fn_mouse_over_out_window
			self.fn_mouse_left_button_down 	= fn_mouse_left_button_down
			self.fn_mouse_left_button_up 	= fn_mouse_left_button_up
			self.fn_get_scene_object_data		= fn_get_scene_object_data

			self.create_object_instance()

		# overloaded delete to remove our custom instances
		def __del__(self):
			self.obj_instance.Hide()
			self.obj_instance.Destroy()
			self.wnd.Hide()
			ui.Window.__del__(self.wnd)

		# on object call, return dict entry by key
		def __call__(self, name): # return type=dict
			return self.__dict__[name]

		# set wnd position
		def set_position(self, x, y):
			self.wnd.SetPosition(x, y)

		# update dict entry by key
		def update_data(self, key, value):
			self.__dict__[key] = value
			if value == None:
				del self.__dict__[key]

		# get wnd position, relative to parent if parent is set
		def get_position(self): # return type=tuple
			# if we have a parent
			if 'parent' in self.__dict__:
				parent = self.fn_get_scene_object_data(self.__dict__['parent'])('wnd')
				if parent:
					parent_position = parent.GetGlobalPosition()
					# we add our position to the parents position, since we have converted our position to local
					return (parent_position[0] + self.__dict__['x'], parent_position[1] + self.__dict__['y'])
			# if we dont have a parent, we return our global position
			return self.wnd.GetGlobalPosition()

		# updates the position of our window object, we do not update our dictionary values, they stay the same at this point!
		def update_position(self):
			self.set_position(*self.get_position())

		# update call for random stuff
		def on_update(self):
			LogTxt(__name__, 'ON_UPDATE:: demo object: %s' % self.__dict__['child_name'])
			self.update_position()

		# on move callback to n_scene_demo instance, will call the func with our dict and wnd position
		def on_move(self, x, y):
			wnd_position = self.get_position()
			self.fn_on_move(self.__dict__, wnd_position[0], wnd_position[1])

		# create our object instance
		def create_object_instance(self):
			LogTxt(__name__, 'scene_data_object.create_object_instance:: %s' % self.__dict__['child_name'])
			try:
				self.wnd = ui.Window()

				self.wnd.AddFlag('movable') 	# we want to be able to move our window
				self.wnd.AddFlag('float') 		# it should pop up above other windows
	
				self.wnd.moveWindowEvent = self.on_move	# we overwrite the moveWindowEvent to call our on_move function

				self.wnd.SetPosition(*self.get_position()) # set position
			
				self.wnd.SetSize(self.__dict__['width'], self.__dict__['height'])
				self.wnd.SetWindowName(self.__dict__['child_name'])

				self.wnd.SetOverEvent(ui.__mem_func__(self.fn_mouse_over_window), self)
				self.wnd.SetOverOutEvent(ui.__mem_func__(self.fn_mouse_over_out_window), self)
				self.wnd.SetMouseLeftButtonDownEvent(ui.__mem_func__(self.fn_mouse_left_button_down), self)
				self.wnd.OnMouseLeftButtonUp = self.fn_mouse_left_button_up

				self.wnd.Show()

				# this is just the base, custom stuff will follow when other shit is done
				self.obj_instance = self.__dict__['class']()
				self.obj_instance.SetParent(self.wnd) 	# set parent to the window
				self.obj_instance.SetPosition(0, 0) 	# set position to 0,0, cuz window is our controller, this feller is just visual
				self.obj_instance.SetSize(self.__dict__['width'], self.__dict__['height'])
				self.obj_instance.AddFlag('not_pick')	# we dont want to be able to pick this object
				self.obj_instance.AddFlag('attach')		# we want to be able to attach this object to other objects
				self.obj_instance.Show()
			
				####


			except Exception as e:
				LogTxt(__name__, 'scene_data_object.create_object_instance:: EXCEPTION <%s>' % e)

	# End of SceneDataObject
	###########################################################

	def __init__(self):
		LogTxt(__name__, "Initializing..")
		self.scene_name = 'scene_demo_re'

		width = wndMgr.GetScreenWidth()
		self.obj_scene_info = ui.TextLine()
		self.obj_scene_info.SetFontName("Tahoma:16")
		self.obj_scene_info.SetPosition(10, 10)
		self.obj_scene_info.SetSize(width, 20)
		self.obj_scene_info.Show()

		self.obj_hotkey_info = ui.TextLine()
		self.obj_hotkey_info.SetFontName("Tahoma:12")
		self.obj_hotkey_info.SetPosition(10, 25)
		self.obj_hotkey_info.SetSize(width, 20)
		self.obj_hotkey_info.SetText(" > TIPS : hold <ALT> to show window outlines | hold <MOUSE+SHIFT> to resize object")
		self.obj_hotkey_info.Show()

		self.obj_mouse_controller = mouse_controller()
		#LogTxt(__name__, "TestMouseController: %s" % self.obj_mouse_controller.current_mouse_position)

	###########################################################

	###########################################################
	# Indicator Methods
	###########################################################
	def create_mouse_over_indicator(self, obj):
		if self.obj_mouse_over == None:
			self.obj_mouse_over = self.scene_object_mouse_over(self.obj_mouse_controller.mouse_over_window_target)
	def destroy_mouse_over_indicator(self):
		if self.obj_mouse_over:
			self.obj_mouse_over.Destroy()
			self.obj_mouse_over = None
	def create_window_drag_indicator(self, obj):
		if self.obj_window_drag == None:
			self.obj_window_drag = self.scene_object_mouse_over(self.obj_mouse_controller.drag_window_target)
	def destroy_window_drag_indicator(self):
		if self.obj_window_drag:
			self.obj_window_drag.Destroy()
			self.obj_window_drag = None

	###########################################################
	# Control Methods
	def update_controls(self, scene_info_text):
		if self.obj_mouse_controller.mouse_over_window_target and self.obj_mouse_controller.mouse_left_down_target == None:
			#LogTxt(__name__, 'update_controls:: mouse_over_target: %s' % self.obj_mouse_controller.mouse_over_window_target)
			
			scene_info_text = self.control_move(scene_info_text)

		elif self.obj_mouse_controller.mouse_left_down_target and self.obj_mouse_controller.mouse_over_window_target != None:
			#LogTxt(__name__, 'update_controls:: mouse_left_down_target: %s' % self.obj_mouse_controller.mouse_left_down_target)

			scene_info_text = self.control_move(scene_info_text)
			scene_info_text = self.control_drag(scene_info_text)

		if self.obj_mouse_controller.mouse_left_down_target == None:
			self.destroy_window_drag_indicator()
		if self.obj_mouse_controller.mouse_over_window_target == None:
			self.destroy_mouse_over_indicator()
		
		return scene_info_text
	#
	def control_drag(self, scene_info_text):
		#LogTxt(__name__, 'control_drag:: %s' % self.__dict__)
		# lets look at wndMgr if we can get the next top window below our mouse and our dragged window
		self.destroy_window_drag_indicator()
		self.obj_mouse_controller.drag_window_target = self.obj_mouse_controller.find_drag_window_target(self)['best']
		if self.obj_mouse_controller.drag_window_target and self.obj_mouse_controller.mouse_left_down_target:
			self.create_window_drag_indicator(self.obj_mouse_controller.drag_window_target)
			scene_info_text += " | DRAGGING : %s" % self.obj_mouse_controller.drag_window_target('child_name')
			self.obj_window_drag.SetColor(globals.CLR_SCENE_OBJECT_DRAG)

			return scene_info_text
	
		self.destroy_window_drag_indicator()
			#for obj in self.d_demo['objects']:
			#	iterator_wnd = self.d_demo['objects'][obj]('wnd')
#
			#	iterator_scene_data = self.get_scene_object_data(obj)
			#	#if iterator_scene_data['child_name'] == self.obj_mouse_controller.mouse_left_down_target('child_name') or \
			#	#	'parent' in iterator_scene_data and iterator_scene_data['parent'] == self.obj_mouse_controller.mouse_left_down_target:
			#	#	continue
#
			#	mouse_over_target_position = wnd_mouse_over.GetGlobalPosition()
			#	mouse_over_target_rect = (mouse_over_target_position[0], mouse_over_target_position[1], wnd_mouse_over.GetWidth(), wnd_mouse_over.GetHeight())
#
			#	if iterator_wnd != wnd_mouse_over:
#
			#		obj_position = iterator_wnd.GetGlobalPosition()
			#		obj_rect = (obj_position[0], obj_position[1], iterator_wnd.GetWidth(), iterator_wnd.GetHeight())
#
			#		self.obj_mouse_controller.drag_window_target = self.obj_mouse_controller.find_drag_window_target(self)
			#		LogTxt(__name__, 'control_drag:: <TESTTESTTEST> %s' % _)
#
			#		# check if current_recht is colliding with obj_rect
			#		if rect_collision(mouse_over_target_rect, obj_rect):
			#			self.obj_mouse_controller.drag_window_target = self.d_demo['objects'][obj]
#
			#			self.create_window_drag_indicator(iterator_wnd)
			#			scene_info_text += ' | WINDOW DRAG TARGET: %s' % iterator_wnd.GetWindowName()
			#			self.obj_window_drag.SetColor(globals.CLR_SCENE_OBJECT_DRAG)
			#			break
	
		return scene_info_text
	#
	def control_move(self, scene_info_text):
		#LogTxt(__name__, 'control_move:: %s' % self.__dict__)

		mouse_position = self.obj_mouse_controller.current_mouse_position
		scene_info_text = self.scene_name + (' | Mouse Position: %s' % str(mouse_position))

		if self.obj_mouse_controller.mouse_over_window_target:

			wnd_mouse_over = self.obj_mouse_controller.mouse_over_window_target('wnd')
			t_mouse_over_target_position = wnd_mouse_over.GetGlobalPosition()
			r_mouse_over_target = (t_mouse_over_target_position[0], t_mouse_over_target_position[1], wnd_mouse_over.GetWidth(), wnd_mouse_over.GetHeight())


			# check if mouse is over our scene object
			if rect_collision((mouse_position[0], mouse_position[1], 1, 1), r_mouse_over_target):
			
				scene_info_text += ' | MOUSE_OVER: %s' % wnd_mouse_over.GetWindowName()
				
				self.create_mouse_over_indicator(self.obj_mouse_controller.mouse_over_window_target)

				self.obj_mouse_over.SetColor(globals.CLR_SCENE_OBJECT_MOUSE_OVER)
				self.obj_mouse_over.SetParent(wnd_mouse_over)
				self.obj_mouse_over.SetPosition(0, 0)
				
				if self.obj_mouse_controller.mouse_left_down_target:
					scene_info_text += ' | MOUSE_DOWN'
					self.obj_mouse_over.SetColor(globals.CLR_SCENE_OBJECT_MOUSE_DOWN)

				else:
					self.obj_mouse_over.SetColor(globals.CLR_SCENE_OBJECT_MOUSE_OVER)
			
				return scene_info_text

		self.destroy_mouse_over_indicator()

		
		return scene_info_text
	# scene Object Callback On Move, to update our children
	def control_scene_object_move(self, data, x, y):
		#LogTxt(__name__, 'control_scene_object_move:: CALLBACK FROM SCENE OBJECT %s' % data['child_name'])
		#move_obj_scene_data = self.get_scene_object_data(data['child_name'])
		#self.update_positions(self.d_scene_data, move_obj_scene_data)
		#move_obj_scene_data = self.get_scene_object_data(data['child_name'])
		#for obj in self.d_demo['objects']:
		#	obj_scene_data = self.get_scene_object_data(obj)
		#	if obj_scene_data['child_name'] == move_obj_scene_data['child_name']:
		#		continue
		#	if 'parent' in obj_scene_data:
		#		if obj_scene_data['parent']('wnd'):
		#			if obj_scene_data['parent']('wnd').GetWindowName() == move_obj_scene_data['child_name']:
		#				self.d_demo['objects'][obj].update_position()
		pass
		
	############################################################################################################

	# our update method, called from interfacemanager.onrender
	def update(self):
		scene_info_text = self.scene_name

		if self.obj_mouse_controller:
			self.obj_mouse_controller.current_mouse_position = wndMgr.GetMousePosition()

		if 'object' in self.__dict__ and len(self.d_demo['objects']) <= 0:
			return
		
		scene_info_text = self.update_controls(scene_info_text)

		self.obj_scene_info.SetText(scene_info_text)
	
	##########################################################################################
	## Demo Data


	def prepare_demo_object(self, data):
		#LogTxt(__name__, "Start Dict: %s" % self.d_demo['objects'])
		#LogTxt(__name__, "Self Dict: %s" % self.__dict__)

		obj = self.get_demo_object_data(data['child_name'])
		if obj == None:
			#LogTxt(__name__, 'n_scene_demo_re.prepare_demo_object:: data creation of object: %s' % data['child_name'])
			self.d_demo['objects'][data['child_name']] = self.scene_data_object(data, self.obj_mouse_controller.on_mouse_left_button_down, self.obj_mouse_controller.on_mouse_left_button_up, self.obj_mouse_controller.on_mouse_over_window, self.obj_mouse_controller.on_mouse_over_out_window, self.control_scene_object_move, self.get_demo_object_data)
		else:
			#LogTxt(__name__, 'n_scene_demo_re.prepare_demo_object:: data update of object: %s' % data['child_name'])
			#update self.d_demo['objects'][data['child_name']].__dict__
			for key, value in data.items():
				self.d_demo['objects'][data['child_name']].update_data(key, value)

	def destroy_demo_objects(self):
		d = self.d_demo['objects']
		for obj in d:
			#LogTxt(__name__, 'n_scene_demo_re.destroy_demo_objects:: %s' % obj)
			self.d_demo['objects'][obj].destroy_objects()
	#
	def create_demo_objects(self):
		for data in self.d_scene_data['children']:
			#LogTxt(__name__, 'n_scene_demo_re.create_demo_objects:: data: %s' % data)
			self.prepare_demo_object(data)

	def get_demo_object_data(self, child_name):
		return self.d_demo['objects'].get(child_name)

	## Scene Data
	def create_scene(self):
		#LogTxt(__name__, 'n_scene_demo_re.create_scene %s' % self.scene_name)
		#self.destroy_demo_objects()
		#self.obj_mouse_controller.mouse_over_window_target = None
		#self.obj_mouse_controller.mouse_left_down_target = None
		#self.obj_mouse_controller.drag_window_target = None
		self.create_demo_objects()
	# Get Scene Object Data
	def get_scene_object_data(self, child_name):
		for l in self.d_scene_data['children']:
			if l['child_name'] == child_name:
				return l
	# Update single scene object by name and key name
	def update_scene_object_data(self, child_name, key, value):
		#LogTxt(__name__, 'n_scene_demo_re.update_scene_object_data:: child_name: %s, key: %s, value: %s' % (child_name, key, value))
		for scene_obj in self.d_scene_data['children']:
			if scene_obj['child_name'] == child_name:
				if value == '__del_object__':
					if key in scene_obj:
						del scene_obj[key]
				else:
					if key == 'x' or key == 'y':
						if 'child_name' in scene_obj:
							if 'parent' in scene_obj:
								if scene_obj['parent'] != None:
									if 'x' in scene_obj['parent'] and 'y' in scene_obj['parent']:
										value = value - scene_obj['parent'][key]
					scene_obj[key] = value
				break
	def set_scene_data(self, scene_name, data):
		# this can only be called once
		if self.scene_name != scene_name:
			self.scene_name = scene_name
			self.d_scene_data = data
		#self.create_demo_objects()
	# Set a single data
	def add_scene_object_data(self, child_name, data):
		if 'children' in self.d_scene_data:
			child = self.get_scene_object_data(child_name)
			if child == None:
				self.d_scene_data['children'].append(data)
			else:
				for key, value in data.items():
					child[key] = value
			self.prepare_demo_object(data)
			return
