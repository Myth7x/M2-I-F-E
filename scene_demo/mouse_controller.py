from _utils import LogTxt

class mouse_controller():
	############################################
	def __init__(self):
		self.__dict__ = {
			'current_mouse_position': [0, 0],
			'last_mouse_position': [0, 0],
			'mouse_over_window_target' : None,
			'drag_window_target': None,
			'mouse_left_down_target': None,
		}
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
	def on_mouse_over_window(self, scene_data_object):
		self.mouse_over_window_target = scene_data_object
	def on_mouse_over_out_window(self, scene_data_object):
		self.mouse_over_window_target = None
	def on_mouse_left_button_down(self, scene_data_object):
		self.mouse_left_down_target = scene_data_object
	def on_mouse_left_button_up(self):
		self.mouse_left_down_target = None
	
	############################################
	