from proto_utils import LogTxt

import ui

class Bar(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        
        self.parent = None
        self.bar_width = 0
        self.bar_height = 0
        self.bar_x = 0
        self.bar_y = 0
        self.bar_color = 0x00000000

        self.bar = ui.Bar()
        self.bar.SetParent(self)
        self.bar.SetSize(self.bar_width, self.bar_height)
        self.bar.SetPosition(0, 0)
        self.bar.SetColor(self.bar_color)
        self.bar.Show()

        self.Show()

    def __del__(self):
        ui.Window.__del__(self)

    def set_parent(self, parent):
        self.parent = parent
    
    def set_size(self, width, height):
        self.bar_width = width
        self.bar_height = height
        self.bar.SetSize(self.bar_width, self.bar_height)
    
    def set_position(self, x, y):
        self.bar_x = x
        self.bar_y = y
        self.SetPosition(self.bar_x, self.bar_y)
    
    def set_color(self, color):
        self.bar_color = color
        self.bar.SetColor(self.bar_color)
