import ui, wndMgr, grp

BACKGROUND_COLOR 	= grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
DARK_COLOR 			= grp.GenerateColor(0.2, 0.2, 0.2, 1.0)
BRIGHT_COLOR 		= grp.GenerateColor(0.7, 0.7, 0.7, 1.0)
SELECT_COLOR 		= grp.GenerateColor(0.0, 0.0, 0.5, 0.3)

WHITE_COLOR 		= grp.GenerateColor(1.0, 1.0, 1.0, 0.5)
HALF_WHITE_COLOR 	= grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

# copy of ui.ListBox
class ListBox(ui.Window):

	TEMPORARY_PLACE = 3

	def __init__(self, layer = "UI"):
		ui.Window.__init__(self, layer)
		self.overLine = -1
		self.selectedLine = -1
		self.width = 0
		self.height = 0
		self.stepSize = 17
		self.basePos = 0
		self.showLineCount = 0
		self.itemCenterAlign = True
		self.itemList = []
		self.keyDict = {}
		self.textDict = {}
		self.event = lambda *arg: None
		self.fontName = 'Arial:12'

	def __del__(self):
		ui.Window.__del__(self)

	def SetShowRowNumber(self, state):
		self.showLineCount = state

	def SetWidth(self, width):
		self.SetSize(width, self.height)

	def SetSize(self, width, height):
		ui.Window.SetSize(self, width, height)
		self.width = width
		self.height = height

	def SetTextCenterAlign(self, flag):
		self.itemCenterAlign = flag

	def SetBasePos(self, pos):
		self.basePos = pos
		self._LocateItem()

	def ClearItem(self):
		self.keyDict 		= {}
		self.textDict 		= {}
		self.itemList 		= []
		self.overLine 		= -1
		self.selectedLine 	= -1

	def InsertItem(self, number, text):
		self.keyDict[len(self.itemList)] = number
		self.textDict[len(self.itemList)] = text

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.fontName)
		textLine.SetText(text)
		textLine.Show()

		if self.itemCenterAlign:
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()

		self.itemList.append(textLine)

		self._LocateItem()

	def SetFontName(self, fontName):
		self.fontName = fontName
		for textLine in self.itemList:
			text = textLine.GetText()
			pos = textLine.GetLocalPosition()
			textLine.SetFontName(self.fontName)
			textLine.SetPosition(pos[0], pos[1])
			textLine.SetText(text)

	def ChangeItem(self, number, text):
		for key, value in self.keyDict.items():
			if value == number:
				if not '>>' in text:
					self.textDict[key] = text
					if number < len(self.itemList):
						self.itemList[key].SetText('%d.%s' % (number+1, text))
				else:
					self.textDict[key] = text
					self.itemList[key].SetText('%s' % (text))
				

				return

	def LocateItem(self):
		self._LocateItem()

	def _LocateItem(self):
		skipCount = self.basePos
		yPos = 0
		self.showLineCount = 0

		for textLine in self.itemList:
			textLine.Hide()

			if skipCount > 0:
				skipCount -= 1
				continue

			textLine.SetPosition(0, yPos + 3)

			yPos += self.stepSize

			if yPos <= self.GetHeight():
				self.showLineCount += 1
				textLine.Show()

	def ArrangeItem(self):
		self.SetSize(self.width, len(self.itemList) * self.stepSize)
		self._LocateItem()

	def GetViewItemCount(self):
		return int(self.GetHeight() / self.stepSize)

	def GetItemCount(self):
		return len(self.itemList)

	def SetEvent(self, event):
		self.event = event

	def SelectItem(self, line):

		if not self.keyDict.has_key(line):
			return

		if line == self.selectedLine:
			return

		self.selectedLine = line
		self.event(self.keyDict.get(line, 0), self.textDict.get(line, "None"))

	def GetSelectedItemText(self):
		return self.textDict.get(self.selectedLine, None)

	def GetSelectedItem(self):
		return self.keyDict.get(self.selectedLine, 0)

	def OnMouseLeftButtonDown(self):
		if self.overLine < 0:
			return

	def OnMouseLeftButtonUp(self):
		if self.overLine >= 0:
			self.SelectItem(self.overLine+self.basePos)

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
		xRender, yRender = self.GetGlobalPosition()
		yRender -= self.TEMPORARY_PLACE
		widthRender = self.width
		heightRender = self.height + self.TEMPORARY_PLACE*2

		if -1 != self.overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + self.overLine*self.stepSize + 4, self.width - 3, self.stepSize)				

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					grp.RenderBar(xRender + 2, yRender + (self.selectedLine-self.basePos)*self.stepSize + 4, self.width - 3, self.stepSize)
