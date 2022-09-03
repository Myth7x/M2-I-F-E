import ui

from proto_utils import LogTxt
from listboxscroll import ListBoxScroll
from filter_editbox import FilterEditbox

class ObjectBrowser(ui.Bar):
		def __init__(self, width, height, color, objects):
			ui.Bar.__init__(self)
			self.objects = objects
			self.last_filter = ""
			self.SetSize(width, height)
			self.SetColor(color)

			self.title = ui.TextLine()
			self.title.SetParent(self)
			self.title.SetPosition(10, 2)
			self.title.SetText("[ Object Browser ]")
			self.title.Show()

			self.element_list = ListBoxScroll()
			self.element_list.SetParent(self)
			self.element_list.SetPosition(5, 15)
			self.element_list.SetSize(width - 10, height - 30)
			self.element_list.Show()

			self.filter = FilterEditbox(width, 20, color, "filter children..")
			self.filter.SetParent(self)
			self.filter.SetPosition(0, height - 20)
			self.filter.Show()

			for obj in self.objects:
				self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (obj))
		
		def selected_object(self):
			return self.element_list.GetSelectedItemText()

		def OnUpdate(self):
			filter = self.filter.filter_editline.GetText()
			if filter != self.filter.placeholder:
				if self.filter.filter_editline.IsFocus():
					if filter != self.last_filter:
						self.last_filter = filter
						self.element_list.ClearItem()
						for ui_class in self.objects:
							if filter in ui_class:
								self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (ui_class))
				else:
					self.filter.filter_editline.SetText(self.filter.placeholder)
			else:
				if self.filter.filter_editline.IsFocus():
					self.filter.filter_editline.SetText("")

		def __del__(self):
			ui.Bar.__del__(self)
