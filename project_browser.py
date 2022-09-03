import ui

from listboxscroll import ListBoxScroll
from filter_editbox import FilterEditbox

class ProjectBrowser(ui.Bar):
		def __init__(self, width, height, color, objects):
			ui.Bar.__init__(self)
			self.objects = objects
			self.children = []
			self.last_filter = ""
			self.SetSize(width, height)
			self.SetColor(color)

			self.title = ui.TextLine()
			self.title.SetParent(self)
			self.title.SetPosition(10, 2)
			self.title.SetText("[ Project Browser ] - <Children:%s>" % (len(self.children)))
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

			for obj in self.children:
				self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (obj))
		
		def update(self):
			self.element_list.ClearItem()
			for obj in self.children:
				self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (obj))
			self.title.SetText("[ Project Browser ] - <Children:%s>" % (len(self.children)))

		def selected_object(self):
			return self.element_list.GetSelectedItemText()

		def add_child(self, class_name):
			for obj in self.objects:
				if obj == class_name:
					self.children.append(obj)
			self.update()

		# todo: dont delete by object name, could be multiple of TextLine, Window etc
		def remove_child(self, class_name):
			for child in self.children:
				if child == class_name:
					self.children.remove(child)
			self.update()

		def OnUpdate(self):
			filter = self.filter.filter_editline.GetText()
			if filter != self.filter.placeholder:
				if self.filter.filter_editline.IsFocus():
					if filter != self.last_filter:
						self.last_filter = filter
						self.element_list.ClearItem()
						for child in self.children:
							if filter.lower() in child.lower():
								self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (child))
				else:
					self.filter.filter_editline.SetText(self.filter.placeholder)
			else:
				if self.filter.filter_editline.IsFocus():
					self.filter.filter_editline.SetText("")

		def __del__(self):
			ui.Bar.__del__(self)
