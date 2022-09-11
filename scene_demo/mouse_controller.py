from _utils import LogTxt, rect_collision

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
		if self.mouse_over_window_target == None or self.mouse_over_window_target != scene_data_object:
			self.mouse_over_window_target = scene_data_object
	def on_mouse_over_out_window(self, scene_data_object):
		self.mouse_over_window_target = None
	def on_mouse_left_button_down(self, scene_data_object):
		if self.mouse_left_down_target == None or self.mouse_left_down_target != scene_data_object:
			self.mouse_left_down_target = scene_data_object
	def on_mouse_left_button_up(self):
		self.mouse_over_window_target = None
		self.mouse_left_down_target = None
		self.drag_window_target = None
	
	############################################
	def find_drag_window_target(self, instance_scene_demo):
		d = {
			'best' : None,
			'best_factor' : 99999999999,
		}

		t_mouse_over_window_target_position = self.mouse_over_window_target('wnd').GetGlobalPosition()
		r_mouse_over_window_target = [t_mouse_over_window_target_position[0], t_mouse_over_window_target_position[1], self.mouse_over_window_target('wnd').GetWidth(), self.mouse_over_window_target('wnd').GetHeight()]

		d_demo_objects = instance_scene_demo.d_demo['objects']

		for key in d_demo_objects:
			obj = d_demo_objects[key]
			if obj == self.mouse_over_window_target: continue

			t_demo_position = obj('wnd').GetGlobalPosition()
			t_demo_size = (obj('wnd').GetWidth(), obj('wnd').GetHeight())
			r_demo_window = [t_demo_position[0], t_demo_position[1], t_demo_size[0], t_demo_size[1]]


			px = (self.current_mouse_position[0] - t_demo_position[0]) ** 2
			py = (self.current_mouse_position[1] - t_demo_position[1]) ** 2
			pw = (self.current_mouse_position[0] - (t_demo_position[0] + t_demo_size[0])) ** 2
			ph = (self.current_mouse_position[1] - (t_demo_position[1] + t_demo_size[1])) ** 2
			factor = (px + py + pw + ph) / 4

			if rect_collision(r_mouse_over_window_target, r_demo_window):

				if factor < d['best_factor']:
					d['best_factor'] = factor
					d['best'] = obj
					LogTxt('mouse_controller', 'find_drag_window_target() - < object:%s (collisions:%s) >' % (obj.__dict__['child_name'], factor))

		return d