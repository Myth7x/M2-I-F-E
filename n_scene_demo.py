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
from proto_utils import LogTxt

## Side Infos

# 1. Parenting
#	- we dont set parent on wndMgr!, we only use parent for its position
#	- we set parent name on our scene data object

class n_scene_demo():
	# holds or scene data
	d_scene_data 	= {}

	# holds our demo data
	d_demo 			= {
		'objects' 					: {},
		'mouse_over_target' 		: None,
		'mouse_left_down_target' 		: None,
		'window_drag_target' 		: None,
		'last_mouse_over_wnd' 	: None,
	}
	
	scene_name 		= ''

	# the instance of our mouse over bar
	obj_mouse_over = None

	# the instance of our window drag bar
	obj_window_drag = None

	# the instance of our scene info text
	obj_scene_info = None

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
	class scene_data_object():
		# the instance of our object control window
		wnd = None

		# the instance of our demo object
		obj_instance = None

		def __init__(self, data, fn_mouse_left_button_down, fn_mouse_left_button_up, fn_mouse_over_window, fn_mouse_over_out_window, fn_on_move):
			self.__dict__ = data
			
			self.fn_on_move 				= fn_on_move
			self.fn_mouse_over_window 		= fn_mouse_over_window
			self.fn_mouse_over_out_window 	= fn_mouse_over_out_window
			self.fn_mouse_left_button_down 	= fn_mouse_left_button_down
			self.fn_mouse_left_button_up 	= fn_mouse_left_button_up

			self.create_object_instance()

		def __del__(self):
			self.obj_instance.Hide()
			self.__dict__['class'].__del__(self.obj_instance)
			self.wnd.Hide()
			ui.Window.__del__(self.wnd)

		def destroy_objects(self):
			if self.obj_instance:
				self.obj_instance.Destroy()
			if self.wnd:
				self.wnd.Destroy()

		def __call__(self, name):
			return self.__dict__[name]

		def set_position(self, x, y):
			self.wnd.SetPosition(x, y)

		def update_data(self, key, value):
			#LogTxt('>>>>UPDATE DATA>>>>>>', '%s %s' % (key, value))
			self.__dict__[key] = value
			if value == None:
				del self.__dict__[key]

		def get_position(self):
			if 'parent' in self.__dict__:
				parent = self.__dict__['parent']('wnd')
				if parent:
					parent_position = parent.GetGlobalPosition()
					return (parent_position[0] + self.__dict__['x'], parent_position[1] + self.__dict__['y'])
			return (self.__dict__['x'], self.__dict__['y'])

		def update_position(self):
			self.set_position(*self.get_position())
			if 'parent' in self.__dict__:
				self.wnd.AddFlag('float')
				self.wnd.SetTop()


		def on_update(self):
			#LogTxt('>>>>UPDATE>>>>>>', '%s' % self.__dict__)
			self.update_position()


		def on_move(self, x, y):
			self.fn_on_move(self.__dict__, self.__dict__['x'], self.__dict__['y'])

		def create_object_instance(self):
			LogTxt(__name__, 'scene_data_object.create_object_instance:: %s' % self.__dict__)
			try:
				self.wnd = ui.Window()

				self.wnd.AddFlag('movable')
				self.wnd.AddFlag('float')
	
				self.wnd.moveWindowEvent = self.on_move

				self.wnd.SetPosition(*self.get_position())
			
				self.wnd.SetSize(self.width, self.height)
				self.wnd.SetWindowName(self.child_name)

				self.wnd.SetOverEvent(ui.__mem_func__(self.fn_mouse_over_window), self)
				self.wnd.SetOverOutEvent(ui.__mem_func__(self.fn_mouse_over_out_window), self)
				self.wnd.SetMouseLeftButtonDownEvent(ui.__mem_func__(self.fn_mouse_left_button_down), self)
				self.wnd.OnMouseLeftButtonUp = self.fn_mouse_left_button_up

				self.wnd.Show()

				# init from strin
				self.obj_instance = self.__dict__['class']()
				self.obj_instance.SetParent(self.wnd)
				self.obj_instance.SetPosition(0, 0)
				self.obj_instance.SetSize(self.width, self.height)
				self.obj_instance.AddFlag('not_pick')
				self.obj_instance.AddFlag('attach')
				self.obj_instance.Show()
			
				# TODO: logic like in our loader
				####


			except Exception as e:
				LogTxt(__name__, 'scene_data_object.create_object_instance:: <error> %s' % e)
			except AttributeError as e:
				LogTxt(__name__, 'scene_data_object.create_object_instance:: <error> %s' % e)

		def destroy_object_instance(self):
			try:
				self.obj_instance.Hide()
				self.obj_instance.Destroy()
				self.obj_instance = None
			except Exception as e:
				LogTxt(__name__, 'scene_data_object.destroy_object_instance:: %s' % e)

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

	def rect_collision(self, r1, r2):
		return (r1[0] < r2[0] + r2[2] and r1[0] + r1[2] > r2[0] and r1[1] < r2[1] + r2[3] and r1[1] + r1[3] > r2[1])

	def scene_object_on_move_callback(self, data, x, y):
		move_obj_scene_data = self.get_scene_object_data(data['child_name'])
		for obj in self.d_demo['objects']:
			obj_scene_data = self.get_scene_object_data(obj)
			if obj_scene_data['child_name'] == move_obj_scene_data['child_name']:
				continue
			if 'parent' in obj_scene_data:
				if obj_scene_data['parent']('wnd').GetWindowName() == move_obj_scene_data['child_name']:
					self.d_demo['objects'][obj].update_position()
		
	def update(self):
		mouse_position = wndMgr.GetMousePosition()
		scene_info_text = self.scene_name + (' | Mouse Position: %s' % str(mouse_position))

		if 'object' in self.__dict__ and len(self.d_demo['objects']) <= 0:
			return

		if self.d_demo['mouse_over_target']:
			mouse_over_wnd = self.d_demo['mouse_over_target']('wnd')

			if self.d_demo['last_mouse_over_wnd']:
				if mouse_over_wnd.GetWindowName() != self.d_demo['last_mouse_over_wnd'].GetWindowName() or self.d_demo['last_mouse_over_wnd'] == None: # same object
					self.d_demo['last_mouse_over_wnd'] = mouse_over_wnd
			else:
				self.d_demo['last_mouse_over_wnd'] = mouse_over_wnd
			
			mouse_over_target_position = mouse_over_wnd.GetGlobalPosition()
			mouse_over_target_rect = (mouse_over_target_position[0], mouse_over_target_position[1], mouse_over_wnd.GetWidth(), mouse_over_wnd.GetHeight())

			if self.rect_collision(mouse_over_target_rect, (mouse_position[0], mouse_position[1], 1, 1)) == False:
				self.on_mouse_over_out_window(self.d_demo['mouse_over_target'])
				return

			scene_info_text += ' | MOUSE_OVER: %s' % mouse_over_wnd.GetWindowName()
			
			if self.obj_mouse_over == None:
				self.obj_mouse_over = self.scene_object_mouse_over(self.d_demo['mouse_over_target'])

			self.obj_mouse_over.SetColor(globals.CLR_SCENE_OBJECT_MOUSE_OVER)
			self.obj_mouse_over.SetParent(mouse_over_wnd)
			self.obj_mouse_over.SetPosition(0, 0)
			

			if self.d_demo['mouse_left_down_target']:
				scene_info_text += ' | MOUSE_DOWN'
				self.obj_mouse_over.SetColor(globals.CLR_SCENE_OBJECT_MOUSE_DOWN)

				# lets look at wndMgr if we can get the next top window below our mouse and our dragged window
				any = False
				for obj in self.d_demo['objects']:
					iterator_wnd = self.d_demo['objects'][obj]('wnd')

					if 'parent' in self.d_demo['objects'][obj].__dict__:
						if self.d_demo['objects'][obj].__dict__['parent']('wnd').GetWindowName() == mouse_over_wnd.GetWindowName():
							continue

					if iterator_wnd.GetWindowName() != mouse_over_wnd.GetWindowName():

						obj_position = iterator_wnd.GetGlobalPosition()
						obj_rect = (obj_position[0], obj_position[1], iterator_wnd.GetWidth(), iterator_wnd.GetHeight())

						# check if current_recht is colliding with obj_rect
						if obj_rect[0] < mouse_over_target_rect[0] + mouse_over_target_rect[2] and obj_rect[0] + obj_rect[2] > mouse_over_target_rect[0] and obj_rect[1] < mouse_over_target_rect[1] + mouse_over_target_rect[3] and obj_rect[1] + obj_rect[3] > mouse_over_target_rect[1]:
							self.d_demo['window_drag_target'] = self.d_demo['objects'][obj]
							any = True
							continue


				if self.d_demo['window_drag_target'] and any == True:
					scene_info_text += ' | WINDOW DRAG TARGET: %s' % iterator_wnd.GetWindowName()

					if self.obj_window_drag == None:
						self.obj_window_drag = self.scene_object_mouse_over(self.d_demo['objects'][obj])
						self.obj_window_drag.SetParent(iterator_wnd)
						self.obj_window_drag.SetPosition(0, 0)
						self.obj_window_drag.SetSize(iterator_wnd.GetWidth(), iterator_wnd.GetHeight())
						self.obj_window_drag.Show()
					
					self.obj_window_drag.SetColor(globals.CLR_SCENE_OBJECT_DRAG)
				else:
					self.d_demo['window_drag_target'] = None
					if self.obj_window_drag:
						self.obj_window_drag.Hide()
						self.obj_window_drag.Destroy()
						self.obj_window_drag = None
			else:
				self.obj_mouse_over.SetColor(globals.CLR_SCENE_OBJECT_MOUSE_OVER)
				
				if self.d_demo['window_drag_target']:
					
					window_draw_wnd = self.d_demo['window_drag_target']('wnd')

					LogTxt(__name__, 'window_drag_target: %s' % window_draw_wnd.GetWindowName())

					mouse_over_target_scene_data = self.get_scene_object_data(mouse_over_wnd.GetWindowName())
					window_drag_target_scene_data = self.get_scene_object_data(window_draw_wnd.GetWindowName())

					if not 'parent' in mouse_over_target_scene_data or mouse_over_target_scene_data['parent'] != window_drag_target_scene_data['child_name']:

						LogTxt(__name__, 'mouse_over_target_scene_data: %s' % mouse_over_target_scene_data)
						LogTxt(__name__, 'window_drag_target_scene_data: %s' % window_drag_target_scene_data)

						self.update_scene_object_data(mouse_over_target_scene_data['child_name'], 'parent', window_drag_target_scene_data['child_name'])
						
						self.update_scene_object_data(mouse_over_target_scene_data['child_name'], 'x', mouse_over_wnd.GetGlobalPosition()[0] - window_draw_wnd.GetGlobalPosition()[0])
						self.update_scene_object_data(mouse_over_target_scene_data['child_name'], 'y', mouse_over_wnd.GetGlobalPosition()[1] - window_draw_wnd.GetGlobalPosition()[1])

						LogTxt(__name__, 'HAVE SET NEW PARENT; RE CREATE SCENE')

						if self.obj_mouse_over:
							self.obj_mouse_over.Hide()
							self.obj_mouse_over.Destroy()
							self.obj_mouse_over = None

						if self.obj_window_drag:
							self.obj_window_drag.Hide()
							self.obj_window_drag.Destroy()
							self.obj_window_drag = None

						self.create_scene()
						return
				else:
					if self.d_demo['last_mouse_over_wnd'] != None and self.d_demo['mouse_over_target'] == None:
						self.update_scene_object_data(self.d_demo['last_mouse_over_wnd'].GetWindowName(), 'parent', '__del_object__')
						self.d_demo['last_mouse_over_wnd'] = None

				if self.obj_window_drag:
					self.obj_window_drag.Hide()
					self.obj_window_drag.Destroy()
					self.obj_window_drag = None
		else:
			self.d_demo['window_drag_target'] = None

			if self.obj_mouse_over:
				self.obj_mouse_over.Hide()
				self.obj_mouse_over.Destroy()
				self.obj_mouse_over = None
			if self.obj_window_drag:
				self.obj_window_drag.Hide()
				self.obj_window_drag.Destroy()
				self.obj_window_drag = None

		self.obj_scene_info.SetText(scene_info_text)
	
	## Demo Data

	# we set our mouse over target here, we dont do other in position checks in our update logic down below
	def on_mouse_over_window(self, scene_data_object):
		#LogTxt(__name__, 'n_scene_demo_re.on_mouse_over_window:: <%s>' % scene_data_object)
		self.d_demo['mouse_over_target'] = scene_data_object
	def on_mouse_over_out_window(self, scene_data_object):
		#LogTxt(__name__, 'n_scene_demo_re.on_move_out:: <%s>' % scene_data_object)
		self.d_demo['mouse_over_target'] = None

	def on_mouse_left_button_down(self, scene_data_object):
		#LogTxt(__name__, 'n_scene_demo_re.on_mouse_left_button_down')
		self.d_demo['mouse_left_down_target'] = scene_data_object

	def on_mouse_left_button_up(self):
		#LogTxt(__name__, 'n_scene_demo_re.on_mouse_left_button_up')
		self.d_demo['mouse_left_down_target'] = None
	####

	def prepare_demo_object(self, data):
		LogTxt(__name__, "Start Dict: %s" % self.d_demo['objects'])
		LogTxt(__name__, "Self Dict: %s" % self.__dict__)

		obj = self.get_demo_object_data(data['child_name'])
		if obj == None:
			#LogTxt(__name__, 'n_scene_demo_re.prepare_demo_object:: data creation of object: %s' % data['child_name'])
			self.d_demo['objects'][data['child_name']] = self.scene_data_object(data, self.on_mouse_left_button_down, self.on_mouse_left_button_up, self.on_mouse_over_window, self.on_mouse_over_out_window, self.scene_object_on_move_callback)
		else:
			LogTxt(__name__, 'n_scene_demo_re.prepare_demo_object:: data update: %s' % self.d_demo['objects'][data['child_name']].__dict__)
			#update self.d_demo['objects'][data['child_name']].__dict__
			for key, value in data.items():
				self.d_demo['objects'][data['child_name']].update_data(key, value)
	def destroy_demo_objects(self):
		d = self.d_demo['objects']
		for obj in d:
			LogTxt(__name__, 'n_scene_demo_re.destroy_demo_objects:: %s' % obj)
			self.d_demo['objects'][obj].destroy_objects()
	#
	def create_demo_objects(self):
		queue = []
		for data in self.d_scene_data['children']:
			LogTxt(__name__, 'n_scene_demo_re.create_demo_objects:: data: %s' % data)
			
			# convert data['parent] to instance
			if 'parent' in data and data['parent'] != None:
				_ = self.get_demo_object_data(data['parent'])
				if not _:
					queue.append(data)
				else:
					data['parent'] = _
					self.prepare_demo_object(data)
		#for data in queue:
		#	if 'parent' in data and data['parent'] != None:
		#		_ = self.get_demo_object_data(data['parent'])
		#		data['parent'] = _('wnd')
		#		self.prepare_demo_object(data)

	def get_demo_object_data(self, child_name):
		return self.d_demo['objects'].get(child_name)

	## Scene Data
	def create_scene(self):
		LogTxt(__name__, 'n_scene_demo_re.create_scene %s' % self.scene_name)
		self.destroy_demo_objects()
		self.d_demo['mouse_over_target'] = None
		self.d_demo['mouse_left_down_target'] = None
		self.d_demo['window_drag_target'] = None
		self.create_demo_objects()
	# Get Scene Object Data
	def get_scene_object_data(self, child_name):
		for l in self.d_scene_data['children']:
			if l['child_name'] == child_name:
				return l
	# Update single scene object by name and key name
	def update_scene_object_data(self, child_name, key, value):
		LogTxt(__name__, 'n_scene_demo_re.update_scene_object_data:: child_name: %s, key: %s, value: %s' % (child_name, key, value))
		for scene_obj in self.d_scene_data['children']:
			if scene_obj['child_name'] == child_name:
				if value == '__del_object__':
					if key in scene_obj:
						del scene_obj[key]
				else:
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