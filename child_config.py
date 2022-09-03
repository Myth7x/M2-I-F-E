from filter_editbox import FilterEditbox
import ui, wndMgr

from proto_utils import LogTxt
from listboxscroll import ListBoxScroll

import globals

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
		self.selected_attribute = None
		self.attributes = []
		self.last_filter = ""

		self._module = ui
		self._class = None

		self.title = ui.TextLine()
		self.title.SetParent(self)
		self.title.SetPosition(10, 2)
		self.title.SetText("[ Child Config ] - None")
		self.title.Show()

		self.element_list = ListBoxScroll()
		self.element_list.SetParent(self)
		self.element_list.SetPosition(5, 15)
		self.element_list.SetTextCenterAlign(wndMgr.HORIZONTAL_ALIGN_LEFT)
		self.element_list.SetEvent(ui.__mem_func__(self.OnAttributeSelect))
		self.element_list.SetSize(int(width/2) - 10, height - 30)
		self.element_list.Show()

		self.filter = FilterEditbox(self.element_list.GetWidth() - 20, 20, globals.BASE_THEME_EDITBOX_BACKGROUND_COLOR, "filter attributes..")
		self.filter.SetParent(self)
		self.filter.SetPosition(0, height - 20)
		self.filter.Show()

		self.title_selected_attribute = ui.TextLine()
		self.title_selected_attribute.SetParent(self)
		self.title_selected_attribute.SetPosition(int(width/2) + 5, 2)
		self.title_selected_attribute.SetText("[ Selected Attribute ] - None")
		self.title_selected_attribute.Show()

	def update(self, child_name, object_name):
		self.element_list.ClearItem()

		self.selected_child_in_project = child_name
		self.selected_object = object_name

		attributes = []
		for ui_class in self.ui_objects:
			if ui_class == object_name:
				self._class = getattr(self._module, ui_class)
				for ui_class_attr in self.ui_objects[ui_class][3]:
					_attribute = getattr(self._class, ui_class_attr)
					if callable(_attribute):
						_attribute = self.Attribute(ui_class_attr, None, type(self.ui_objects[ui_class][3][ui_class_attr]))
						attributes.append(ui_class_attr)
				break
		self.attributes = attributes

		self.title.SetText("[ Child Config ] - %s <Attributes:%s>" % (self.selected_child_in_project, len(attributes)))

		#if attributes != self.attributes:
		#	self.attributes = attributes
		#	for attribute in self.attributes:
		#		self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (attribute))

	def OnUpdate(self):
		filter = self.filter.filter_editline.GetText().lower()
		if filter != self.filter.placeholder.lower():
			if self.filter.filter_editline.IsFocus():
				if filter != self.last_filter:
					self.last_filter = filter
					self.element_list.ClearItem()
					for attribute in self.attributes:
						if filter.lower() in attribute.lower():
							self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (attribute))
			else:
				self.filter.filter_editline.SetText(self.filter.placeholder)
		else:
			if self.element_list.GetItemCount() != len(self.attributes):
				self.element_list.ClearItem()
				for attribute in self.attributes:
					self.element_list.InsertItem(self.element_list.GetItemCount(), "%s" % (attribute))
			if self.filter.filter_editline.IsFocus():
				self.filter.filter_editline.SetText("")
		
	def OnAttributeSelect(self, t=None, n=None):
		if n is None: return
		selected_attribute = self.element_list.GetSelectedItemText()
		self.title_selected_attribute.SetText("[ Selected Attribute ] - %s" % (selected_attribute))

		if selected_attribute and selected_attribute != self.selected_attribute:
			LogTxt("ChildConfig", "selected attribute: %s" % (selected_attribute))
			self.selected_attribute = selected_attribute

	def __del__(self):
		ui.Bar.__del__(self)
