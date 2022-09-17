from _utils.pythonscriptloader import PythonScriptLoader
from _utils import LogTxt

import ui

import globals
from .standard_attributes import StandardAttributes, Attribute

class attribute_editor(ui.ScriptWindow):
	"""attribute editor class
	- used to edit attributes of a scene object duh
	"""
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		#LogTxt(__name__, "Initializing...")

		self.object 			= None
		self.parent 			= None

		self.attributes = []

		self.scene_object = {}

		self.script_loader = PythonScriptLoader()

		self.init = self.load()

		self.ref_category_attribute_configuration = self.object.Children[0].Children[1]
		self.ref_board = self.object.Children[0]
		#LogTxt(__name__, "Initialized! ref board %s" % self.ref_board)


		self.bg_attr_editor = ui.Bar()
		self.bg_attr_editor.SetParent(self.ref_category_attribute_configuration)
		self.bg_attr_editor.SetPosition(20, 60)
		self.bg_attr_editor.SetSize(self.ref_category_attribute_configuration.GetWidth() - 40, self.ref_category_attribute_configuration.GetHeight() - 80)
		self.bg_attr_editor.SetColor(0x304a4a4a)
		self.bg_attr_editor.Show()
		self.attr_editbox = ui.EditLine()
		self.attr_editbox.SetParent(self.bg_attr_editor)
		self.attr_editbox.SetPosition(3, 3)
		self.attr_editbox.SetMultiLine()
		self.attr_editbox.SetLimitWidth(self.bg_attr_editor.GetWidth())
		self.attr_editbox.SetSize(*(self.bg_attr_editor.GetWidth() -6, self.bg_attr_editor.GetHeight()-6))
		self.attr_editbox.SetText("Weeeeeeeeeeeeeew\n weeew")
		self.attr_editbox.SetMax(1000)
		self.attr_editbox.Show()

		# Create ComboBox for attribute.attribute selection
		self.cb_on_attr_val = ui.ComboBox()
		self.cb_on_attr_val.SetParent(self.ref_category_attribute_configuration)
		self.cb_on_attr_val.SetPosition(20, 25)
		self.cb_on_attr_val.SetSize(self.ref_category_attribute_configuration.GetWidth() - 40, 25)
		self.cb_on_attr_val.Show()
	
		self.fn_original_on_select_attr_val = self.cb_on_attr_val.OnSelectItem
		self.cb_on_attr_val.listBox.OnSelectItem = self.on_select_attr_val

		self.attributes = []
		for attr in StandardAttributes:
			LogTxt(__name__, "Adding attribute %s" % attr)
			self.attributes.append(Attribute(attr, StandardAttributes[attr]['type'], StandardAttributes[attr]['index'], 0, ""))
		LogTxt(__name__, "Attributes: %s" % self.attributes)
		for attr in self.attributes:
			self.cb_on_attr_val.InsertItem(self.cb_on_attr_val.listBox.GetItemCount(), attr.name)
		
		self.cb_on_attr_val.SelectItem(0)

		#LogTxt(__name__, "Initialized!")

	def on_select_attr_val(self, selected_attr, name):
		LogTxt(__name__, "Selected attribute: %s" % name)
		self.attr_editbox.SetText(selected_attr + " " + name)
		self.fn_original_on_select_attr_val(selected_attr, name)
	def set_parent(self, parent):
		self.parent = parent

	def set_scene_object(self, object):
		self.scene_object = object

	def find_object(self, objects, object_name):
		for object in objects:
			if hasattr(object, "Children") and len(object.Children) > 0:
				return self.find_object(object.Children, object_name)
			if object.GetWindowName() == object_name:
				return object
		return None

	def load(self):
		try:
			self.object = self.script_loader.load_script(self, "C:\\InterfaceManager\\ifmgr_ui\\stylescripts\\", "style_attribute_editor.py")
		except:
			#LogTxt(__name__, "Failed to load script!")
			return False
		return True

	def update(self):
		if self.ref_board.IsShow():
			self.ref_board.SetTitleName('Children Editor - %s' % self.scene_object["child_name"])
			selected_attr = self.cb_on_attr_val.listBox.GetSelectedItem()
			selected_attr_str = self.cb_on_attr_val.listBox.textDict[selected_attr]
			self.cb_on_attr_val.SetCurrentItem(selected_attr_str)

			self.attr_editbox.SetText(self.scene_object[selected_attr_str] if selected_attr_str in self.scene_object else '')
	
	def render(self):
		pass
