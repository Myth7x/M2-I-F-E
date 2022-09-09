import ui, wndMgr, grp

import globals

from proto_utils import LogTxt

BACKGROUND_COLOR 	= grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
DARK_COLOR 			= grp.GenerateColor(0.2, 0.2, 0.2, 1.0)
BRIGHT_COLOR 		= grp.GenerateColor(0.7, 0.7, 0.7, 1.0)
SELECT_COLOR 		= grp.GenerateColor(0.0, 0.0, 0.5, 0.3)

WHITE_COLOR 		= grp.GenerateColor(1.0, 1.0, 1.0, 0.5)
HALF_WHITE_COLOR 	= grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

class SelectBox(ui.Window):
	def __init__(self, layer = "UI"):
		ui.Window.__init__(self, layer)

		self.overLine = -1
		self.stepSize = 20
		self.width = 100
		self.height = 100

		LogTxt(__name__, "Initialized!")

		self.Show()
	
	def SetWidth(self, width):
		self.SetSize(width, self.height)

	def SetSize(self, width, height):
		ui.Window.SetSize(self, width, height)
		self.width = width
		self.height = height

	def OnUpdate(self):
		self.overLine = -1
		if self.IsIn():
			x, y = self.GetGlobalPosition()
			height = self.GetHeight()
			xMouse, yMouse = wndMgr.GetMousePosition()

			if yMouse - y < height - 1:
				self.overLine = (yMouse - y) / self.stepSize

				if self.overLine < 0:
					self.overLine = -1
				if self.overLine >= len(self.itemList):
					self.overLine = -1


	def OnRender(self):
		current_pos = self.GetGlobalPosition()

		# we render our backgrounds
		grp.SetColor(BRIGHT_COLOR)
		grp.RenderBar(0 + current_pos[0], 0 + current_pos[1],  self.width, self.height)

