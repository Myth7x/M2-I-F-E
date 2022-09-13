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
		self.__dict__['x'] = x
		self.__dict__['y'] = y
		self.wnd.SetPosition(x, y)

	def update_data(self, key, value):
		"""update __dict__ entry by key"""
		self.__dict__[key] = value

	def get_parent_position(self):
		return self.fn_get_parent_position(self.__dict__)

	# get wnd position, relative to parent if parent is set
	def get_position(self): # return type=tuple
		# if we dont have a parent, we return our global position
		return self.wnd.GetGlobalPosition()

	def get_global_position(self):
		"""get global position"""
		#LogTxt(__name__, 'get_global_position:: parent: %s' % self.__dict__['parent'])
		parent_pos = self.get_parent_position()
		if parent_pos:
			return (parent_pos[0] + self.__dict__['x'], parent_pos[1] + self.__dict__['y'])
		if self.is_moving == False:
			return self.wnd.GetGlobalPosition()
		return (self.__dict__['x'], self.__dict__['y'])

	# updates the position of our window object, we do not update our dictionary values, they stay the same at this point!
	def update_position(self):
		self.wnd.SetPosition(*self.get_global_position())
		if self.is_moving == True and self.is_moving_target == True:
			wndMgr.AddFlag(self.wnd.hWnd, 'not_pick')
		else:
			wndMgr.RemoveFlag(self.wnd.hWnd, 'not_pick')
			self.wnd.SetTop()

	# update call for random stuff
	def on_update(self):
		#LogTxt(__name__, 'ON_UPDATE:: demo object: %s' % self.__dict__['child_name'])
		self.update_position()

	# on move callback to n_scene_demo instance, will call the func with our dict and wnd position
	def on_move(self, x, y):
		self.__dict__['x'] = x
		self.__dict__['y'] = y
		self.fn_on_move(self.__dict__, x, y)
		self.wnd.SetTop()

	# create our object instance
	def create_object_instance(self):
		#LogTxt(__name__, 'scene_data_object.create_object_instance:: %s' % self.__dict__['child_name'])

		self.wnd = ui.Window()			# create our control window
		self.wnd.AddFlag('movable') 	# we want to be able to move our controller
		self.wnd.AddFlag('float') 		# enabled settop

		self.wnd.SetPosition(*(self.__dict__['x'], self.__dict__['y'])) # set position
		self.wnd.SetSize(self.__dict__['width'], self.__dict__['height']) # set size

		# override functions
		self.wnd.moveWindowEvent = self.on_move														# on move callback
		self.wnd.SetWindowName(self.__dict__['child_name']) 										# set window name			
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
			self.obj_instance.SetSize(self.__dict__['width'], self.__dict__['height'])
			self.obj_instance.AddFlag('not_pick')	# we dont want to be able to pick this object
			self.obj_instance.AddFlag('attach')		# we want to be able to attach this object to other objects
			self.obj_instance.Show()
			
			# textline? set text to its name and set position to middle of the window
			if callable(getattr(self.obj_instance, "SetText", None)) and (ui.TextLine == type(self.obj_instance) or ui.EditLine == type(self.obj_instance)):
				self.obj_instance.SetText(self.__dict__['child_name'])
				if callable(getattr(self.obj_instance, "SetHorizontalAlignCenter", None)):
					self.obj_instance.SetHorizontalAlignCenter()
					self.obj_instance.SetVerticalAlignCenter()
				self.obj_instance.SetPosition(self.__dict__['width']/2, self.__dict__['height']/2)

		except Exception as e:
			LogTxt(__name__, 'scene_data_object.create_object_instance:: EXCEPTION <%s>' % e)
