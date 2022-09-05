from distutils.log import Log
from pythonscriptloader import PythonScriptLoader
from proto_utils import LogTxt

import ui, wndMgr

class n_attribute_editor(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		LogTxt(__name__, "Initializing...")

		self.ui_data 			= None
		self.object 			= None
		self.parent 			= None

		self.script_loader = PythonScriptLoader()

		self.init = self.load()

		self.ref_category_attribute_configuration = self.object.Children[0].Children[1]

		# Create ComboBox for attribute.attribute selection
		self.cb_attr_val = ui.ComboBox()
		self.cb_attr_val.SetParent(self.ref_category_attribute_configuration)
		self.cb_attr_val.SetPosition(20, 25)
		self.cb_attr_val.SetSize(self.ref_category_attribute_configuration.GetWidth() - 40, 25)
		self.cb_attr_val.Show()
	
		self.cb_attr_val.SetCurrentItem('- Select Attribute -')
		self.cb_attr_val.InsertItem(1, 'Attribute 1')
		self.cb_attr_val.InsertItem(2, 'Attribute 2')

		LogTxt(__name__, "Initialized!")

	def set_parent(self, parent):
		self.parent = parent

	def find_object(self, objects, object_name):
		for object in objects:
			if hasattr(object, "Children") and len(object.Children) > 0:
				return self.find_object(object.Children, object_name)
			if object.GetWindowName() == object_name:
				return object
		return None

	def set_ui_data(self, data):
		self.ui_data = data

	def load(self):
		try:
			self.object = self.script_loader.load_script(self, "C:\\Proto_InterfaceManager\\ifmgr_ui\\stylescripts\\", "style_attribute_editor.py")
		except:
			LogTxt(__name__, "Failed to load script!")
			return False
		return True

	def update(self):
		if self.init == True:
			selected_attr = self.cb_attr_val.listBox.GetSelectedItem()
			if selected_attr > 0:
				selected_attr_str = self.cb_attr_val.listBox.textDict[selected_attr-1]
				self.cb_attr_val.SetCurrentItem(selected_attr_str)

	def render(self):
		pass
