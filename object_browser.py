import inspect
import ui, wndMgr

from proto_utils import LogTxt
from listboxscroll import ListBoxScroll
from filter_editbox import FilterEditbox

import globals

class ObjectBrowser(ui.Bar):
		def __init__(self, width, height, color, objects):
			ui.Bar.__init__(self)

			self.objects = objects
			self.check_objects()

			self.last_filter = ""
			self.SetSize(width, height)
			self.SetColor(color)

			self.title = ui.TextLine()
			self.title.SetParent(self)
			self.title.SetPosition(int(width / 2), 2)
			self.title.SetHorizontalAlignCenter()
			self.title.SetText("[ Object Browser ]")
			self.title.Show()

			self.object_list = ListBoxScroll()
			self.object_list.SetParent(self)
			self.object_list.SetPosition(5, 15)
			self.object_list.SetTextCenterAlign(wndMgr.HORIZONTAL_ALIGN_LEFT)
			self.object_list.SetSize(width - 10, height - 46)
			self.object_list.Show()

			self.filter = FilterEditbox(width, 20, globals.BASE_THEME_EDITBOX_BACKGROUND_COLOR, "filter objects..")
			self.filter.SetParent(self)
			self.filter.SetPosition(0, height - 20)
			self.filter.Show()

			self.update_object_list()
		
		def check_objects(self):
			not_good = []
			for ui_class in self.objects:
				_module = ui
				_class = getattr(_module, ui_class)
				if not inspect.isclass(_class) or len(str(self.objects[ui_class][2])) <= 0:
					#LogTxt("ObjectBrowser", "not good ui_class for object browser: %s - %s" % (ui_class, self.objects[ui_class][1]))
					#LogTxt("ObjectBrowser", "please report this to the author, or fix it yourself")
					not_good.append(ui_class)
			for ui_class in not_good:
				del self.objects[ui_class]

		def update_object_list(self):
			filter = self.filter.filter_editline.GetText()
			self.object_list.ClearItem()
			for ui_class in self.objects:
				if filter.lower() in ui_class.lower() or self.filter.filter_editline.GetText() == self.filter.placeholder:
					self.object_list.InsertItem(self.object_list.GetItemCount(), "%s" % (ui_class))

		def selected_object(self):
			return self.object_list.GetSelectedItemText()

		def OnUpdate(self):
			filter = self.filter.filter_editline.GetText()
			if filter != self.filter.placeholder:
				if self.filter.filter_editline.IsFocus():
					if filter != self.last_filter:
						self.last_filter = filter
						self.update_object_list()
				else:
					self.filter.filter_editline.SetText(self.filter.placeholder)
			else:
				if self.filter.filter_editline.IsFocus():
					self.filter.filter_editline.SetText("")

		def __del__(self):
			ui.Bar.__del__(self)
