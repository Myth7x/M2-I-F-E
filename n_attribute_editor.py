from pythonscriptloader import PythonScriptLoader
from proto_utils import LogTxt

import ui

import ifmgr_ui

import globals

class n_attribute_editor(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		#LogTxt(__name__, "Initializing...")

		self.object 			= None
		self.parent 			= None

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
		self.bg_attr_editor.SetColor(0x00000000)
		self.bg_attr_editor.Show()
		self.attr_editbox = ui.EditLine()
		self.attr_editbox.SetParent(self.bg_attr_editor)
		self.attr_editbox.SetPosition(0, 0)
		self.attr_editbox.SetMultiLine()
		self.attr_editbox.SetLimitWidth(self.bg_attr_editor.GetWidth())
		self.attr_editbox.SetSize(*(self.bg_attr_editor.GetWidth(), self.bg_attr_editor.GetHeight()))
		self.attr_editbox.SetText("Weeeeeeeeeeeeeew\n weeew")
		self.attr_editbox.SetMax(1000)
		self.attr_editbox.Show()

		# Create ComboBox for attribute.attribute selection
		self.cb_on_event_val = ui.ComboBox()
		self.cb_on_event_val.SetParent(self.ref_category_attribute_configuration)
		self.cb_on_event_val.SetPosition(20, 25)
		self.cb_on_event_val.SetSize(self.ref_category_attribute_configuration.GetWidth() - 40, 25)
		self.cb_on_event_val.Show()
	
		self.cb_on_event_val.SetCurrentItem('- Select Event -')
		self.cb_on_event_val.SetEvent(ui.__mem_func__(self.on_select_attr_val))
		self.cb_on_event_val.InsertItem(1, '__init__')
		self.cb_on_event_val.InsertItem(2, 'OnUpdate')
		self.cb_on_event_val.InsertItem(3, 'OnRender')

		#LogTxt(__name__, "Initialized!")

	def on_select_attr_val(self, selected_attr):
		if selected_attr > 0:
			#LogTxt(__name__, "Selected attribute: %s" % self.cb_on_event_val.listBox.textDict[selected_attr-1])

			self.attr_editbox.SetText(self.scene_object["child_object"].__dict__[self.cb_on_event_val.listBox.textDict[selected_attr-1]])
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
			selected_attr = self.cb_on_event_val.listBox.GetSelectedItem()
			if selected_attr > 0:
				selected_attr_str = self.cb_on_event_val.listBox.textDict[selected_attr-1]
				self.cb_on_event_val.SetCurrentItem(selected_attr_str)

	def render(self):
		pass
