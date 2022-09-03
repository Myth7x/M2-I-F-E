import inspect
from proto_utils import LogTxt
import ui, wndMgr

from listboxscroll import ListBoxScroll
from filter_editbox import FilterEditbox

import globals

class ProjectBrowser(ui.Bar):
	class Child:
		def __init__(self, name, object, parent):
			self.name = name
			self.children = []
			self.parent = parent
			self.object = object
		def get_object(self):
			return self.object
		def __str__(self):
			return self.name
		def __repr__(self):
			return self.name
		def __eq__(self, other):
			return self.name == other.name
		def __ne__(self, other):
			return self.name != other.name
		def __call__(self):
			return self.name
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
		self.element_list.SetTextCenterAlign(wndMgr.HORIZONTAL_ALIGN_LEFT)
		self.element_list.SetSize(width - 10, height - 30)
		self.element_list.Show()

		self.filter = FilterEditbox(width, 20, globals.BASE_THEME_EDITBOX_BACKGROUND_COLOR, "filter children..")
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

	def selected_child_name(self):
		return self.element_list.GetSelectedItemText()

	def selected_child_object_name(self, child_name):
		for child in self.children:
			if child.name == child_name:
				return child.get_object()

	def add_child(self, class_name):
		for obj in self.objects:
			#LogTxt("Project Browser", "Checking object: %s" % (obj))
			if obj == class_name:
				_child = self.Child(class_name, obj, self)
				for child in self.children:
					if child.name == _child.name:
						_child.name = "%s_%s" % (child.name, len(self.children))
				self.children.append(_child)
		self.update()

	def remove_child(self, class_name):
		for child in self.children:
			if child.name == class_name:
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
						if filter.lower() in child().lower():
							self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (child))
			else:
				self.filter.filter_editline.SetText(self.filter.placeholder)
		else:
			if self.filter.filter_editline.IsFocus():
				self.filter.filter_editline.SetText("")

	def __del__(self):
		ui.Bar.__del__(self)
