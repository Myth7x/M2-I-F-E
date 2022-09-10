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

import ui, wndMgr

import globals
from proto_utils import LogTxt

## Side Infos

# 1. Parenting
#	- we dont set parent on wndMgr!, we only use parent for its position
#	- we set parent name on our scene data object

class n_scene_demo_re():
	# holds or scene data
	d_scene_data 	= {}

	# holds our demo data
	d_demo 			= {
		'objects' 					: {},
		'mouse_over_target' 		: None,
		'mouse_left_button_down' 	: False,
	}
	
	scene_name 		= ''

	###########################################################
	class scene_data_object():
		# the instance of our object control window
		wnd = None

		# the instance of our demo object
		obj_instance = None

		def __init__(self, data, fn_mouse_left_button_down, fn_mouse_left_button_up, fn_mouse_over_window, fn_mouse_over_out_window):
			self.__dict__ = data
			self.create_object_instance(fn_mouse_left_button_down, fn_mouse_left_button_up, fn_mouse_over_window, fn_mouse_over_out_window)

		def __del__(self):
			self.destroy_object_instance()

		def create_object_instance(self, fn_mouse_left_button_down, fn_mouse_left_button_up, fn_mouse_over_window, fn_mouse_over_out_window):
			#LogTxt(__name__, 'scene_data_object.create_object_instance:: %s' % self.__dict__)
			try:
				self.wnd = ui.Window()
				self.wnd.AddFlag('movable')
				self.wnd.AddFlag('float')

				self.wnd.SetSize(self.width, self.height)
				self.wnd.SetPosition(self.x, self.y)

				self.wnd.SetWindowName(self.child_name)

				self.wnd.SetOverEvent(ui.__mem_func__(fn_mouse_over_window), self)
				self.wnd.SetOverOutEvent(ui.__mem_func__(fn_mouse_over_out_window), self)
				self.wnd.SetMouseLeftButtonDownEvent(ui.__mem_func__(fn_mouse_left_button_down), self)
				self.wnd.OnMouseLeftButtonUp = fn_mouse_left_button_up

				self.wnd.Show()

				# init from strin
				self.obj_instance = self.__dict__['class']()
				self.obj_instance.SetParent(self.wnd)
				self.obj_instance.SetPosition(0, 0)
				self.obj_instance.SetSize(self.width, self.height)
				self.obj_instance.AddFlag('not_pick')
				self.obj_instance.Show()
			
				# TODO: logic like in our loader
				####


			except Exception as e:
				LogTxt(__name__, 'scene_data_object.create_object_instance:: %s' % e)

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

	def update(self):
		#LogTxt(__name__, 'Current Mouse Target: %s, is pressed: %s' % (self.d_demo['mouse_over_target'], self.d_demo['mouse_left_button_down']))
		pass

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
		self.d_demo['mouse_over_target'] = scene_data_object
		self.d_demo['mouse_left_button_down'] = True
	def on_mouse_left_button_up(self):
		#LogTxt(__name__, 'n_scene_demo_re.on_mouse_left_button_up')
		self.d_demo['mouse_over_target'] = None
		self.d_demo['mouse_left_button_down'] = False
	####

	def prepare_demo_object(self, data):
		obj = self.get_demo_object_data(data['child_name'])
		if obj == None:
			self.d_demo['objects'][data['child_name']] = self.scene_data_object(data, self.on_mouse_left_button_down, self.on_mouse_left_button_up, self.on_mouse_over_window, self.on_mouse_over_out_window)
			#LogTxt(__name__, 'n_scene_demo_re.prepare_demo_object:: data insert: %s' % self.d_demo['objects'][data['child_name']].__dict__)
		else:
			#LogTxt(__name__, 'n_scene_demo_re.prepare_demo_object:: data update: %s' % self.d_demo['objects'][data['child_name']].__dict__)
			for key, value in data.items():
				obj.__dict__[key] = value
		return False

	#
	def create_demo_objects(self):
		for data in self.d_scene_data['children']:
			#LogTxt(__name__, 'n_scene_demo_re.create_demo_objects:: data: %s' % data)
			self.prepare_demo_object(data)
	#	
	def get_demo_object_data(self, child_name):
		return self.d_demo['objects'].get(child_name)

	## Scene Data
	def create_scene(self):
		LogTxt(__name__, 'n_scene_demo_re.create_scene %s' % self.scene_name)
		self.create_demo_objects()
	# Get Scene Object Data
	def get_scene_object_data(self, child_name):
		for l in self.d_scene_data['children']:
			if l['child_name'] == child_name:
				return l
	# Set a full set of data
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