import ui

import ifmgr_ui.listbox as listbox

# credits to ymir, event extention by myth
class ListBoxScroll(listbox.ListBox):
	def __init__(self):
		listbox.ListBox.__init__(self)

		self.scrollBar = ui.ScrollBar()
		self.scrollBar.SetParent(self)
		self.scrollBar.SetScrollEvent(self.__OnScroll)
		self.scrollBar.Hide()

	def SetSize(self, width, height):
		listbox.ListBox.SetSize(self, width - ui.ScrollBar.SCROLLBAR_WIDTH, height)
		ui.Window.SetSize(self, width, height)
		
		self.scrollBar.SetPosition(width - ui.ScrollBar.SCROLLBAR_WIDTH, 0)
		self.scrollBar.SetScrollBarSize(height)

	def ClearItem(self):
		listbox.ListBox.ClearItem(self)
		self.scrollBar.SetPos(0)

	def select_item_name(self, name):
		for i in range(len(self.itemList)):
			if self.itemList[i].GetWindowName() == name:
				self.SelectItem(i)
				break

	def _LocateItem(self):
		listbox.ListBox._LocateItem(self)
		
		if self.showLineCount < len(self.itemList):
			self.scrollBar.SetMiddleBarSize(float(self.GetViewItemCount())/self.GetItemCount())
			self.scrollBar.Show()
		else:
			self.scrollBar.Hide()

	def __OnScroll(self):
		scrollLen = self.GetItemCount()-self.GetViewItemCount()
		if scrollLen < 0:
			scrollLen = 0
		self.SetBasePos(int(self.scrollBar.GetPos()*scrollLen))
