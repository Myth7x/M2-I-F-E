import ui


class FilterEditbox(ui.Bar):
	def __init__(self, width, height, color, placeholder, font = "Tahoma:12"):
		ui.Bar.__init__(self)
		self.SetSize(width, height)
		self.SetColor(color)

		self.placeholder = placeholder

		self.filter_editline = ui.EditLine()
		self.filter_editline.SetParent(self)
		self.filter_editline.SetSize(width - 20, 10)
		self.filter_editline.SetPosition(10, 5)
		self.filter_editline.SetMax(50)
		self.filter_editline.SetFontName(font)
		self.filter_editline.SetText(self.placeholder)
		self.filter_editline.Show()

	def __del__(self):
		ui.Bar.__del__(self)