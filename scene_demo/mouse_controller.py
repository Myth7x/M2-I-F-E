from _utils import LogTxt, rect_collision, rect_intersect_area_factor

import globals

class mouse_controller():
	"""mouse controller class
	- used for our scene demo objects control functions
	"""
	############################################
	def __init__(self, parent):
		self.__dict__ = {
			'current_mouse_position'	: [0, 0],
			'last_mouse_position'		: [0, 0],
			'mouse_over_window_target' 	: None,
			'drag_window_target'		: None,
			'mouse_left_down_target'	: None,
		}
		self.parent = parent
	def __del__(self):
		pass
	def __get__(self, key):
		return self.__dict__[key]
	def __set__(self, key, value):
		self.__dict__[key] = value
	def __del__(self, key):
		del self.__dict__[key]
	def __contains__(self, key):
		return key in self.__dict__

	############################################
	# mouse controller event callbacks
	def on_mouse_over_window(self, scene_data_object):
		if scene_data_object == None: return
		self.mouse_over_window_target = scene_data_object
		return True
	def on_mouse_over_out_window(self, scene_data_object):
		if scene_data_object != self.mouse_over_window_target: return
		self.mouse_over_window_target = None
		return True
	def on_mouse_left_button_down(self, scene_data_object):
		self.mouse_left_down_target = scene_data_object
		return True
	def on_mouse_left_button_up(self):
		"""Mouse left button up event"""
		# if we have a drag window target, call the on_drag_window_end event
		if self.mouse_over_window_target != None:
			self.parent.on_drag_window_end(
				self.mouse_over_window_target, 
				self.drag_window_target, 
				self.__dict__['current_mouse_position'][0],
				self.__dict__['current_mouse_position'][1]
			)
		self.mouse_left_down_target = None
		self.drag_window_target = None
		return True

	############################################
	def reset(self):
		"""Reset the mouse controller target objects"""
		self.__dict__['mouse_over_window_target'] = None
		self.__dict__['drag_window_target'] = None
		self.__dict__['mouse_left_down_target'] = None

	def find_drag_window_target(self, instance_scene_demo, exclude_list):
		"""Find the window that is being dragged
		- instance_scene_demo: scene_demo instance
		- exclude_list: list of window names to exclude from the search
		"""
		d = {
			'best' : None,
			'best_factor' : 0,
		}

		if self.mouse_over_window_target == None:
			return None

		t_mouse_over_window_target_position = self.mouse_over_window_target('wnd').GetGlobalPosition()
		r_mouse_over_window_target = [t_mouse_over_window_target_position[0], t_mouse_over_window_target_position[1], self.mouse_over_window_target('wnd').GetWidth(), self.mouse_over_window_target('wnd').GetHeight()]

		d_demo_objects = instance_scene_demo.d_demo['objects']

		# iterate our current demo objects
		for key in d_demo_objects:
			obj = d_demo_objects[key]

			# skip the current mouse over window target (window we are moving or clicking on)
			if obj == self.mouse_over_window_target: continue

			# unused atm, maybe for parenting later
			if obj in exclude_list:
				#LogTxt("find_drag_window_target: exclude_list: %s" % obj('name'))
				continue

			t_demo_position = obj('wnd').GetGlobalPosition()
			t_demo_size = (obj('wnd').GetWidth(), obj('wnd').GetHeight())
			r_demo_window = [t_demo_position[0], t_demo_position[1], t_demo_size[0], t_demo_size[1]]

			# check if the mouse over window target window is inside the demo object iterator window
			if rect_collision(r_mouse_over_window_target, r_demo_window):
				# calculate the intersect area factor
				f = rect_intersect_area_factor(r_mouse_over_window_target, r_demo_window)
				if f > d['best_factor'] and f > globals.MIN_WINDOW_INTERSECTION_FACTOR:
					d['best_factor'] = f
					d['best'] = obj
		# returning a dict bist the best object and the intersect area factor
		return d
