
class mouse_controller():
    def __init__(self):
        self.__dict__ = {
            'current_mouse_position': [0, 0],
            'last_mouse_position': [0, 0],
            'drag_window_target': None,
            'move_window_target': None,
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
