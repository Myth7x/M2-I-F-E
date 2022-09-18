from _utils.pythonscriptloader import PythonScriptLoader
from _utils import LogTxt

import ui, grp, wndMgr

import globals
from .standard_attributes import StandardAttributes, Attribute

class attribute_editor(ui.ScriptWindow):
	"""attribute editor class
	- used to edit attributes of a scene object duh
	"""

	class attribute_input(ui.Bar):
		def __init__(self):
			ui.Bar.__init__(self)
			self.AddFlag('float')
			self.name = ""
			self.type = None
			self.value = None
			self.parent = None
		def set_name(self, name):
			self.name = name
		def set_parent(self, parent):
			self.parent = parent
		def set_type(self, type):
			self.type = type
		def set_value(self, value):
			self.value = value
		def get_value(self):
			return self.value
		def universal_callback(self, *args):
			if self.type == 'slider':
				self.value = self.input.GetSliderPos()

			elif self.type == 'text':
				self.value = self.input.GetText()
			elif self.type == 'float':
				self.value = self.input.GetText()
			elif self.type == 'bool':
				self.value = self.input.GetCheckStatus()
			self.parent.update_attribute(self.name, self.value)
			LogTxt("universal_callback", self.value)
		def build_input(self):
			if self.type == 'slider':
				# slider
				self.input = ui.SliderBar()
				self.input.AddFlag('float')
				self.input.SetSliderPos(self.value if self.value else 0.0)
				self.input.SetParent(self)
				self.input.SetPosition(10, 10)
				self.input.SetSize(100, 20)
				#self.input.SetLimit(0, 100)
				self.input.SetEvent(ui.__mem_func__(self.universal_callback))
				self.input.Show()
				self.input.SetTop()

			elif self.type == 'text':
				self.input = ui.EditLine()
				self.input.AddFlag('float')
				self.input.SetParent(self)
				self.input.SetWindowHorizontalAlignCenter()
				self.input.SetWindowVerticalAlignCenter()
				self.input.SetSize(100, 20)
				self.input.SetPosition(10, 10)
				self.input.SetReturnEvent(ui.__mem_func__(self.universal_callback))
				self.input.SetText(self.value if self.value else "")
				self.input.userMax = 999999
				self.input.SetFocus()
				self.input.SetTop()
			
			elif self.type == 'bool':
				self.input = ui.CheckBox()
				self.input.AddFlag('float')
				self.input.SetParent(self)
				self.input.SetWindowHorizontalAlignCenter()
				self.input.SetWindowVerticalAlignCenter()
				self.input.SetSize(100, 20)
				self.input.SetPosition(10, 10)
				self.input.SetEvent(ui.__mem_func__(self.universal_callback))
				self.input.SetCheck(self.value if self.value else False)
				self.input.SetTop()

			self.input.Show()

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		#LogTxt(__name__, "Initializing...")

		self.object 			= None
		self.parent 			= None
		self.has_updated = False

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

		# Create ComboBox for attribute.attribute selection
		self.cb_on_attr_val = ui.ComboBox()
		self.cb_on_attr_val.SetParent(self.ref_category_attribute_configuration)
		self.cb_on_attr_val.SetPosition(20, 25)
		self.cb_on_attr_val.SetSize(self.ref_category_attribute_configuration.GetWidth() - 40, 25)
		self.cb_on_attr_val.Show()

		self.attr_inputfield = None
	
		self.cb_on_attr_val.SetEvent(ui.__mem_func__(self.on_select_attr_val))

		self.attributes = []
		for attr in StandardAttributes:
			LogTxt(__name__, "Adding attribute %s" % attr)
			self.attributes.append(Attribute(attr, StandardAttributes[attr]['type'], StandardAttributes[attr]['index'], 0, ""))
		LogTxt(__name__, "Attributes: %s" % self.attributes)
		for attr in self.attributes:
			self.cb_on_attr_val.InsertItem(self.cb_on_attr_val.listBox.GetItemCount(), attr.name)
		
		self.cb_on_attr_val.SelectItem(0)

		#LogTxt(__name__, "Initialized!")

	def update_attribute(self, name, value):
		LogTxt(__name__, "Updating attribute %s to %s" % (name, value))
		for attr in self.attributes:
			if attr.name == name:
				attr.value = value
				break
		self.has_updated = True

	def on_select_attr_val(self, selected_attr):
		LogTxt(__name__, "Selected attribute: %s" % selected_attr)
		if self.attr_inputfield:
			self.attr_inputfield.Hide()
			self.attr_inputfield.Destroy()
			self.attr_inputfield = None
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
			
			attr = self.attributes[selected_attr]

			if self.attr_inputfield == None:
				self.attr_inputfield = self.attribute_input()
				self.attr_inputfield.set_name(attr.name)
				self.attr_inputfield.set_parent(self)
				self.attr_inputfield.SetParent(self.ref_category_attribute_configuration)
				self.attr_inputfield.SetPosition(3, 60)
				self.attr_inputfield.SetColor(grp.GenerateColor(0.2, 0.2, 0.2, 0.5))
				self.attr_inputfield.SetSize(*(self.bg_attr_editor.GetWidth() -6, self.bg_attr_editor.GetHeight()-6))
				self.attr_inputfield.Show()

				self.attr_inputfield.set_type(attr.type)
				self.attr_inputfield.build_input()
			self.attr_inputfield.set_value(attr.value)

			if self.has_updated:
				self.parent.update_object_attributes(self.scene_object["child_name"], self.attributes)
				self.has_updated = False

	def render(self):
		pass
