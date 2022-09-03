import ui

from proto_utils import LogTxt
from listboxscroll import ListBoxScroll

class ChildConfig(ui.Bar):
	class Attribute:
		def __init__(self, name, value, type):
			self.name = name
			self.value = value
			self.type = type
			self.ui_representation = None

		def __str__(self):
			return "%s: %s" % (self.name, self.value)

		def __repr__(self):
			return "%s: %s" % (self.name, self.value)

	def __init__(self, width, height, color, ui_objects):
		ui.Bar.__init__(self)
		self.SetSize(width, height)
		self.SetColor(color)

		self.selected_child_in_project = None
		self.ui_objects = ui_objects
		self.selected_object = None
		self.attributes = []

		self.title = ui.TextLine()
		self.title.SetParent(self)
		self.title.SetPosition(10, 2)
		self.title.SetText("[ Child Config ] - None")
		self.title.Show()

		self.element_list = ListBoxScroll()
		self.element_list.SetParent(self)
		self.element_list.SetPosition(5, 15)
		self.element_list.SetSize(width - 10, height - 30)
		self.element_list.Show()

	def update(self, child_name, object_name):
		self.element_list.ClearItem()

		self.selected_child_in_project = child_name
		self.selected_object = object_name

		attributes = []
		for ui_class in self.ui_objects:
			if ui_class == object_name:
				_module = ui
				_class = getattr(_module, ui_class)
				for ui_class_attr in self.ui_objects[ui_class][3]:
					_attribute = getattr(_class, ui_class_attr)
					if callable(_attribute):
						_attribute = self.Attribute(ui_class_attr, None, type(self.ui_objects[ui_class][3][ui_class_attr]))
						attributes.append(_attribute)
				break
		self.attributes = attributes

		self.title.SetText("[ Child Config ] - %s <Attributes:%s>" % (self.selected_child_in_project, len(attributes)))

		self.update_attributes()

	# need to find a ui element that can scroll a list of ui elements
	def update_attributes(self):
		for attribute in self.attributes:
			self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (attribute))

	def selected_child(self):
		return self.element_list.GetSelectedItemText()

	def __del__(self):
		ui.Bar.__del__(self)
