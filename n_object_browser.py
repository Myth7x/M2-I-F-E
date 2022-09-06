# This is my first test of utilizing our script loader.
from distutils.log import Log
from pythonscriptloader import PythonScriptLoader
from proto_utils import LogTxt

import ui, wndMgr

import globals

# If we want to create a new window, we need to create a new class.
# It always needs to inherit from ui.ScriptWindow.
class n_object_browser(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		LogTxt(__name__, "Initializing...")

		self.style_script_data 	= None
		self.object 			= None
		self.parent 			= None

		self.script_loader = PythonScriptLoader()

		self.init = self.load()

		self.ref_titlebar 	= self.find_object(self.object.Children, "titlebar")
		self.ref_titlebar_info 	= self.find_object(self.object.Children, "titlebar_info")
		self.ref_object_list 	= self.find_object(self.object.Children, "object_list")
		self.ref_board 			= self.find_object(self.object.Children, "board")

		self.ref_object_list.OnMouseWheel = self.ref_object_list.scrollBar.OnMouseWheel
		self.ref_object_list.OnMouseLeftButtonDoubleClick = self.on_double_click_object_list

		LogTxt(__name__, "Initialized!")

	def set_parent(self, parent):
		self.parent = parent

	def on_double_click_object_list(self):
		self.parent.OnAddObject()

	def find_object(self, objects, object_name):
		for object in objects:
			if object.GetWindowName() == object_name:
				return object
			if hasattr(object, "Children"):
				for child in object.Children:
					if child.GetWindowName() == object_name:
						return child
		return None

	def load(self):
		try:
			self.object = self.script_loader.load_script(self, "C:\\Proto_InterfaceManager\\ifmgr_ui\\stylescripts\\", "style_object_browser.py")
		except:
			LogTxt(__name__, "Failed to load script!")
			return False
		return True

	def update_title_info(self):
		if self.ref_titlebar_info:
			self.ref_titlebar_info.SetText("[ UI Classes: %d ]" % len(globals.UI_CLASS_DATA))

	def update(self):
		if self.init == True:
			self.update_title_info()
			if self.ref_board == None or self.ref_object_list == None:
				for child in self.object.Children:
					if child.GetWindowName() == "object_list":
						self.ref_object_list = child
					elif child.GetWindowName() == "board":
						self.ref_board = child
				
			if self.ref_object_list and self.ref_board:
				if self.ref_object_list.GetItemCount() != len(globals.UI_CLASS_DATA):
					self.arrange_object_list()

			self.ref_object_list.OnUpdate()

	def render(self):
		pass

	def arrange_object_list(self):
		# find object_list in object.Children
		if self.ref_object_list:
			self.ref_object_list.ClearItem()
			for object in globals.UI_CLASS_DATA:
				self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(),"%s" % object)

	def get_selected_object(self):
		if self.ref_object_list.GetItemCount() > 0:
			if self.ref_object_list.GetSelectedItem() != -1:
				selected_object = self.ref_object_list.GetSelectedItemText()
				for object in globals.UI_CLASS_DATA:
					if selected_object == object:
						return globals.UI_CLASS_DATA[object]
		return None
