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

from .object_wrapper import object_wrapper

class scene_demo():
	"""scene demo class
	- visualize our scene data
	- has a mouse controller for mouse input
	"""

	parent = None

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

	call_arrange_object_list = False

	###########################################################
	class window_indicator(ui.Bar):
		"""window indicator class
		- shows a colored bar around a window"""
		def __init__(self):
			ui.Bar.__init__(self)
			self.AddFlag('not_pick')
			self.target = None
			self.target_wnd = None
			self.color = grp.GenerateColor(0, 0, 0, 1)
			self.Hide()
		def update(self, window, color):
			self.target = window
			self.target_wnd = window('wnd')
			self.color = color
			self.SetParent(self.target_wnd)
			self.SetSize(*(self.target_wnd.GetWidth(), self.target_wnd.GetHeight()))
			self.SetColor(self.color)
			self.SetPosition(0, 0)
			self.Show()

	
	class text_indicator_inputs(ui.Bar):
		"""text indicator inputs class
		- shows state of any input captured
		"""

		def __init__(self):
			ui.Bar.__init__(self)
			self.SetSize(100, 20)
			self.text_lines = {}

			self.title = ui.TextLine()
			self.title.SetParent(self)
			self.title.SetPosition(int(self.GetWidth()/2), 0)
			self.title.SetHorizontalAlignCenter()
			self.title.SetText('Controls')
			self.title.SetFontColor(0.0, 0.0, 0.0)
			self.title.Show()

			self.Hide()
		def set_position(self, x, y):
			"""set position of the text indicator"""
			self.SetPosition(x, y)
			self.title.SetPosition(int(self.GetWidth()/2), 0)
		def set_size(self, width, height):
			"""set size of the text indicator"""
			self.SetSize(width, height)
			self.title.SetPosition(int(self.GetWidth()/2), 0)
		def add_text_line(self, name, text):
			"""add a text line to the text indicator"""
			if name in self.text_lines:
				return
			self.text_lines[name] = ui.TextLine()
			self.text_lines[name].SetParent(self)
			self.text_lines[name].SetPosition(10, 0)
			self.text_lines[name].SetHorizontalAlignLeft()
			self.text_lines[name].SetText(text)
			self.text_lines[name].SetFontColor(0.0, 0.0, 0.0)
			self.text_lines[name].Show()
		def update_text_line(self, name, text):
			"""update a text line"""
			if not name in self.text_lines:
				return
			self.text_lines[name].SetText(text)
		def remove_text_line(self, name):
			"""remove a text line"""
			if not name in self.text_lines:
				return
			self.text_lines[name].Hide()
			del self.text_lines[name]
		def set_text(self, name, text):
			"""set text for a line by name"""
			self.text_lines[name] = text
		def arrange_text_lines(self):
			"""arrange text lines"""
			y = 16
			for name in self.text_lines:
				self.text_lines[name].SetPosition(10, y)
				y += 16

	########################################################

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

		self.obj_mouse_over = self.window_indicator()
		self.obj_window_drag = self.window_indicator()

		self.obj_mouse_controller = mouse_controller(self)

		self.text_indicator = self.text_indicator_inputs()
		self.text_indicator.set_position(wndMgr.GetScreenWidth() - 310, wndMgr.GetScreenHeight() - 110)
		self.text_indicator.set_size(300, 100)
		self.text_indicator.SetColor(globals.CLR_SCENE_TEXT_INDICATOR)
		self.text_indicator.Show()

		self.text_indicator.add_text_line("MOUSE_LEFT_BUTTON_DOWN_TARGET", "Mouse Left Button Down Target: None")
		self.text_indicator.add_text_line("MOUSE_OVER_WINDOW_TARGET", "Mouse Over Window Target: None")
		self.text_indicator.add_text_line("DRAG_WINDOW_TARGET", "Drag&Drop Target Window: None")

	###########################################################

	###########################################################
	# Indicator Methods
	###########################################################
	# updates, parent, position, size, color
	def update_indicator(self, indicator, window, color):
		indicator.update(window, color)
	
	###########################################################
	# Control Methods
	def update_controls(self, scene_info_text):

		# find out if we have clicked a window

		# this exclude list will exclude the mouse_left_down_target children from every control check
		exclude_names = []
		if self.obj_mouse_controller.refs['mouse_left_down_target']:
			exclude_names.append(self.obj_mouse_controller.refs['mouse_left_down_target'].child_name)
			for child_object in self.d_demo['objects']:
				if self.d_demo['objects'][child_object].parent == self.obj_mouse_controller.refs['mouse_left_down_target'].child_name:
					exclude_names.append(child_object)

		best_drag_window_target = self.obj_mouse_controller.find_drag_window_target(self, exclude_names)
		if best_drag_window_target != None and best_drag_window_target['best'] != None:
			self.obj_mouse_controller.refs['drag_window_target'] = best_drag_window_target['best']
			#LogTxt(__name__, "update_controls:: drag_window_target: %s" % self.obj_mouse_controller.refs['drag_window_target']('wnd').GetWindowName())
		else:
			self.obj_mouse_controller.refs['drag_window_target'] = None
			#LogTxt(__name__, "update_controls:: drag_window_target: None")

			
		###########################################################
		scene_info_text += ' | MOUSE POS: (%s, %s)' % (self.obj_mouse_controller.mouse['position'][0], self.obj_mouse_controller.mouse['position'][1])
		###########################################################
		
		# has mouse over window target
		need_over_indicator = False
		if self.obj_mouse_controller.refs['mouse_over_window_target']:
			self.update_indicator(self.obj_mouse_over, self.obj_mouse_controller.refs['mouse_over_window_target'], globals.CLR_SCENE_OBJECT_MOUSE_OVER)
			wnd_mouse_over = self.obj_mouse_controller.refs['mouse_over_window_target']('wnd')
			# has left mouse button down
			if self.obj_mouse_controller.refs['mouse_left_down_target']:
				self.update_indicator(self.obj_mouse_over, self.obj_mouse_controller.refs['mouse_over_window_target'], globals.CLR_SCENE_OBJECT_MOUSE_DOWN)
			need_over_indicator = True
		
		scene_info_text = self.control_drag(scene_info_text)

		# hide mouse over indicator
		if need_over_indicator == False:
			self.obj_mouse_over.Hide()

		return scene_info_text

	def control_drag(self, scene_info_text):

		need_drag_indicator = False
		if self.obj_mouse_controller.refs['drag_window_target'] and self.obj_mouse_controller.refs['mouse_left_down_target'] != None:
			
			drag_window_pos = self.obj_mouse_controller.refs['drag_window_target']('wnd').GetGlobalPosition()
			rect_drag_window = (drag_window_pos[0], drag_window_pos[1], self.obj_mouse_controller.refs['drag_window_target']('wnd').GetWidth(), self.obj_mouse_controller.refs['drag_window_target']('wnd').GetHeight())

			mouse_move_window_pos = self.obj_mouse_controller.refs['mouse_left_down_target']('wnd').GetGlobalPosition()
			rect_mouse_move_window = (mouse_move_window_pos[0], mouse_move_window_pos[1], self.obj_mouse_controller.refs['mouse_left_down_target']('wnd').GetWidth(), self.obj_mouse_controller.refs['mouse_left_down_target']('wnd').GetHeight())
			if rect_collision(rect_drag_window, rect_mouse_move_window):
				self.update_indicator(self.obj_window_drag, self.obj_mouse_controller.refs['drag_window_target'], globals.CLR_SCENE_OBJECT_DRAG_CAN_DROP)
				need_drag_indicator = True
		
		# hide drag indicator
		if need_drag_indicator == False:
			self.obj_window_drag.Hide()

		return scene_info_text
	
	def get_sub_children(self, parent_name):
		children = []
		for child_object in self.d_demo['objects']:
			if self.d_demo['objects'][child_object].parent == parent_name:
				children.append(self.d_demo['objects'][child_object])
		return children

	def get_sub_children_name_list(self, parent_name):
		"""get a list of all child objects"""
		lst_names = []
		for object in self.d_demo['objects']:
			if self.d_demo['objects'][object].parent == parent_name:
				lst_names.append(object)
		for name in lst_names:
			lst_names += self.get_sub_children_name_list(name)
		return lst_names

	def on_drag_window_end(self, ctrl_wnd, dst_wnd, x, y):
		"""method used to update children if the moved window has any
		Args:
			ctrl_wnd (name:str): the window that was moved
			dst_wnd (name:str): the window that was moved to
			x (int): x position of the window
			y (int): y position of the window
		"""

		if dst_wnd == ctrl_wnd.parent:
			return
		
		if dst_wnd == None:
			ctrl_wnd_children = self.get_sub_children_name_list(ctrl_wnd.child_name)

			ctrl_wnd.is_moving = False
			ctrl_wnd.is_moving_target = False
			ctrl_wnd.parent = None

			ctrl_wnd.x = ctrl_wnd('wnd').GetGlobalPosition()[0]
			ctrl_wnd.y = ctrl_wnd('wnd').GetGlobalPosition()[1]

			ctrl_wnd.destroy_object_instance()
			ctrl_wnd.create_object_instance()

			for child in ctrl_wnd_children:
				obj = self.d_demo['objects'][child]
				#LogTxt(__name__, "we iterate children to update them after none dragdrop <%s>" % obj('wnd'))
				obj('wnd').SetParent(ctrl_wnd('wnd'))
				obj('wnd').SetPosition(obj.x, obj.y)

			self.call_arrange_object_list = True

			return

		if ctrl_wnd == dst_wnd or dst_wnd == None: 
			return

		# update object data
		#if self.d_demo['objects'][dst_wnd_name].parent != ctrl_wnd_name:
		ctrl_wnd.parent = dst_wnd.child_name
		ctrl_wnd('wnd').SetParent(dst_wnd('wnd'))
		ctrl_wnd.x = ctrl_wnd('wnd').GetGlobalPosition()[0] - dst_wnd('wnd').GetGlobalPosition()[0]
		ctrl_wnd.y = ctrl_wnd('wnd').GetGlobalPosition()[1] - dst_wnd('wnd').GetGlobalPosition()[1]
		ctrl_wnd('wnd').SetPosition(ctrl_wnd.x, ctrl_wnd.y)

		# reset drag window target and mouse left down target
		self.obj_mouse_controller.refs['drag_window_target'] 		= None
		self.obj_mouse_controller.refs['mouse_left_down_target'] 	= None
		self.call_arrange_object_list = True
		
	############################################################################################################
	# our update method, called from interfacemanager.onrender
	def update(self):
		scene_info_text = self.scene_name

		if self.obj_mouse_controller:
			self.obj_mouse_controller.mouse['position'] = wndMgr.GetMousePosition()

		scene_info_text = self.update_controls(scene_info_text)

		self.obj_scene_info.SetText(scene_info_text)
	
	    
		if self.obj_mouse_controller.refs['mouse_left_down_target'] != None:
			self.text_indicator.update_text_line("MOUSE_LEFT_BUTTON_DOWN_TARGET", "Mouse Left Button Down Target: %s" % self.obj_mouse_controller.refs['mouse_left_down_target'].child_name)
		else:
			self.text_indicator.update_text_line("MOUSE_LEFT_BUTTON_DOWN_TARGET", "Mouse Left Button Down Target: None")
		
		if self.obj_mouse_controller.refs['mouse_over_window_target'] != None:
			self.text_indicator.update_text_line("MOUSE_OVER_WINDOW_TARGET", "Mouse Over Window Target: %s" % self.obj_mouse_controller.refs['mouse_over_window_target'].child_name)
		else:
			self.text_indicator.update_text_line("MOUSE_OVER_WINDOW_TARGET", "Mouse Over Window Target: None")

		if self.obj_mouse_controller.refs['drag_window_target'] != None:
			self.text_indicator.update_text_line("DRAG_WINDOW_TARGET", "Drag&Drop Target Window: %s" % self.obj_mouse_controller.refs['drag_window_target'].child_name)
		else:
			self.text_indicator.update_text_line("DRAG_WINDOW_TARGET", "Drag&Drop Target Window: None")
		
		self.text_indicator.arrange_text_lines()

		for child in self.d_demo['objects']:
			self.d_demo['objects'][child].on_update()
		

		self.parent.update_scene_object_data(self.d_demo['objects'])
		if self.call_arrange_object_list == True:
			self.parent.arrange_object_list()
			self.call_arrange_object_list = False
	##########################################################################################
	## Demo Data

	def update_object_data(self, child_name, attribute_list):
		"""method used to update object data
		Args:
			child_name (str): the name of the object
			attribute_list (list): the list of attributes to update
		"""
		self.d_demo['objects'][child_name].update_object_data(attribute_list)

	def destroy_demo(self):
		for obj in self.d_demo['objects']:
			self.d_demo['objects'][obj]('wnd').Hide()

	def create_demo_objects(self):
		# create demo objects
		for obj in self.d_demo['objects']:
			self.d_demo['objects'][obj]('wnd').Show()
			self.d_demo['objects'][obj]('wnd').SetPosition(*(self.d_demo['objects'][obj].__dict__['x'], self.d_demo['objects'][obj].__dict__['y']))
			self.d_demo['objects'][obj]('wnd').SetSize(*(self.d_demo['objects'][obj].__dict__['width'], self.d_demo['objects'][obj].__dict__['height']))

	def prepare_demo_object(self, data):
		
		obj = self.get_demo_object_data(data['child_name'])
		if obj == None:
			self.d_demo['objects'][data['child_name']] = object_wrapper(data, self.obj_mouse_controller.on_mouse_left_button_down, self.obj_mouse_controller.on_mouse_left_button_up, self.obj_mouse_controller.on_mouse_over_window, self.obj_mouse_controller.on_mouse_over_out_window, None, self.get_demo_object_data, self.get_parent_position)
			self.d_demo['objects'][data['child_name']].parent = self
		else:
			self.d_demo['objects'][data['child_name']] = data

	def get_parent_position(self, child_data):
		if self.obj_mouse_controller.refs['mouse_left_down_target'] and self.obj_mouse_controller.refs['mouse_left_down_target'].child_name == child_data.parent:
			#LogTxt(__name__, 'n_scene_demo_re.get_parent_position:: mouse left down target: %s' % self.obj_mouse_controller.refs['mouse_left_down_target'].__dict__['child_name'])
			return self.d_demo['objects'][child_data.parent].uio_get_position()
		return None

	def get_demo_object_data(self, child_name):
		return self.d_demo['objects'].get(child_name)

	## Scene Data
	
	# Get Scene Object Data
	def get_scene_object_data(self, child_name):
		for l in self.d_scene_data['children']:
			if l['child_name'] == child_name:
				return l
	
	def set_scene_data(self, scene_name, data):
		# this can only be called once
		if self.scene_name != scene_name:
			self.scene_name = scene_name
			self.d_scene_data = data
		#self.create_demo_objects()
	# Set a single data
	def add_scene_object_data(self, child_name, data):
		#if not 'children' in self.d_scene_data:
		#	self.d_scene_data['children'] = []

		child = self.get_scene_object_data(child_name)
		if child == None:
			self.d_scene_data['children'].append(data)
			child = self.get_scene_object_data(child_name)
		else:
			for obj in data:
				#LogTxt(__name__, 'n_scene_demo_re.add_scene_object_data:: data update of object: %s, key: %s, value: %s' % (child_name, obj, data[obj]))
				child[obj] = data[obj]
		
		self.prepare_demo_object(child)
		self.parent.update_scene_object_data(self.d_demo['objects'])