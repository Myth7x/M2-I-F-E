from _utils import LogTxt

import globals

import wndMgr, ui

class object_wrapper():
	"""object wrapper class
	Args:
		data (dict): data to be used for the object
		fn_mouse_left_button_down (function): function to be called when mouse left button is down
		fn_mouse_left_button_up (function): function to be called when mouse left button is up
		fn_mouse_over_window (function): function to be called when mouse is over window
		fn_mouse_over_out_window (function): function to be called when mouse is out of window
		fn_on_move (function): function to be called when window is moved
		fn_get_scene_object_data (function): function to be called to get scene object data"""
	
	# the instance of our object control window
	wnd = None

	# the instance of our demo object
	obj_instance = None
	
	originals = {
		'position' : None,
		'size' : None,
	}

	is_moving = False
	is_moving_target = False

	def __init__(self, data, fn_mouse_left_button_down, fn_mouse_left_button_up, fn_mouse_over_window, fn_mouse_over_out_window, fn_on_move, fn_get_scene_object_data, fn_get_parent_position):
		self.__dict__ = data
		self.originals['position'] = (self.__dict__['x'], self.__dict__['y'])
		self.originals['size'] = (self.__dict__['width'], self.__dict__['height'])
		
		# set ui class callbacks, set on and then called by our demo objects
		self.fn_get_parent_position = fn_get_parent_position
		self.fn_on_move 					= fn_on_move
		self.fn_mouse_over_window 			= fn_mouse_over_window
		self.fn_mouse_over_out_window 		= fn_mouse_over_out_window
		self.fn_mouse_left_button_down 		= fn_mouse_left_button_down
		self.fn_mouse_left_button_up 		= fn_mouse_left_button_up
		self.fn_get_scene_object_data		= fn_get_scene_object_data

		self.create_object_instance()

	def __del__(self):
		self.obj_instance.Hide()
		self.obj_instance.Destroy()
		self.wnd.Hide()
		ui.Window.__del__(self.wnd)

	def __call__(self, name):
		"""call function
		Args:
			name (str): name of the instance to return
		
		Returns:
			instance: the instance of the name
		"""
		return self.__dict__[name]

	def set_position(self, x, y):
		"""set wnd position"""
		self.x = x
		self.y = y
		self.uio_set_position(x, y)

	def update_data(self, key, value):
		"""update __dict__ entry by key"""
		self.__dict__[key] = value

	def get_global_position(self):
		"""get global position
		means... get the position of the object relative to the parent"""
		parent_pos = self.fn_get_parent_position(self)
		if parent_pos:
			return (parent_pos[0] + self.x, parent_pos[1] + self.y)
		return self.uio_get_position()

	def on_update(self):
		"""on update callback only here the object will be updated"""
		self.uio_update_relative_to_parent()

	def on_move(self, x, y):
		"""on move callback <on move callback to n_scene_demo instance, will call the func with our dict and wnd position>
		Args:
			x (int): x position
			y (int): y position
		"""
		self.x = x
		self.y = y
		if self.is_moving == True:
			self.fn_on_move(self, x, y)


	def create_object_instance(self):
		"""create object instance with controller"""
		self.wnd = ui.Window()			# create our control window
		self.wnd.AddFlag('movable') 	# we want to be able to move our controller
		self.wnd.AddFlag('float') 		# enabled settop

		self.wnd.SetPosition(self.x, self.y) # set position
		self.wnd.SetSize(self.width, self.height) # set size

		# override functions
		self.wnd.moveWindowEvent = self.on_move														# on move callback
		self.wnd.SetWindowName(self.child_name) 										# set window name			
		self.wnd.SetOverEvent(ui.__mem_func__(self.fn_mouse_over_window), self) 					# set mouse over event
		self.wnd.SetOverOutEvent(ui.__mem_func__(self.fn_mouse_over_out_window), self) 				# set mouse over out event
		self.wnd.SetMouseLeftButtonDownEvent(ui.__mem_func__(self.fn_mouse_left_button_down), self) # set mouse left button down event
		self.wnd.OnMouseLeftButtonUp = self.fn_mouse_left_button_up 								# set mouse left button up event			
		self.wnd.Show()

		try:
			# here we create our scene object instance
			# this is just the base, custom stuff will follow when other shit is done
			self.obj_instance = self.__dict__['class']()
			self.obj_instance.SetParent(self.wnd) 	# set parent to the window
			self.obj_instance.SetPosition(0, 0) 	# set position to 0,0, cuz window is our controller, this feller is just visual
			self.obj_instance.SetSize(self.width, self.height)
			self.obj_instance.AddFlag('not_pick')	# we dont want to be able to pick this object
			self.obj_instance.Show()
			
			# textline? set text to its name and set position to middle of the window
			if callable(getattr(self.obj_instance, "SetText", None)) and (ui.TextLine == type(self.obj_instance) or ui.EditLine == type(self.obj_instance)):
				self.obj_instance.SetText(self.child_name)
				if callable(getattr(self.obj_instance, "SetHorizontalAlignCenter", None)):
					self.obj_instance.SetHorizontalAlignCenter()
					self.obj_instance.SetVerticalAlignCenter()
				self.obj_instance.SetPosition(self.width/2, self.height/2)

		except Exception as e:
			LogTxt(__name__, 'scene_data_object.create_object_instance:: EXCEPTION <%s>' % e)

	############################################################################################################
	# UI object related functions
	############################################################################################################
	# We have to use our own functions for ui related stuff to split setting object infos and dictionary aka scene object infos
	# In the end this dictionary will be the raw data for the scene object, so we can save it to a file and load it again.
	# If we call any get function here, its because we want to get Window.GetPosition.
	############################################################################################################

	def uio_update_relative_to_parent(self):
		"""update relative to parent"""
		self.uio_set_position(self.get_global_position())
		if self.is_moving == True and self.is_moving_target == True:
			self.uio_add_flag('not_pick')
			self.uio_remove_flag('float')
		elif self.is_moving == True and self.is_moving_target == False:
			self.uio_remove_flag('uio_add_flag')
			self.uio_add_flag('float')
			self.wnd.SetTop()
			self.wnd.Show()

	def uio_get_position(self):
		"""ui.Window.GetPosition
		Returns:
			tuple: (x, y)"""
		return self.wnd.GetGlobalPosition()
	def uio_set_position(self, position):
		"""ui.Window.SetPosition
		Args:
			position (tuple): x, y position"""
		self.wnd.SetPosition(*position)

	def uio_get_size(self):
		"""(ui.Window.GetWidth, ui.Window.GetHeight)
		Returns:
			tuple: width, height"""
		return self.wnd.GetWidth(), self.wnd.GetHeight()
	def  uio_set_size(self, size):
		"""ui.Window.SetSize
		Args:
			size (tuple): width, height size"""
		self.wnd.SetSize(*size)
	
	def uio_set_parent(self, parent_name):
		"""ui.Window.SetParent
		Args:
			parent_name (str): parent name"""
		self.wnd.SetParent(parent_name)

	def uio_remove_flag(self, flag):
		"""ui.Window.RemoveFlag (*)
		Args:
			flag (str): flag to remove"""
		self.wnd.RemoveFlag(flag)
	def uio_add_flag(self, flag):
		"""ui.Window.AddFlag
		Args:
			flag (str): flag to add"""
		self.wnd.AddFlag(flag)