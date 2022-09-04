# This is my first test of utilizing our script loader.
from distutils.log import Log
from pythonscriptloader import PythonScriptLoader
from proto_utils import LogTxt

import ui, wndMgr

class n_object_browser(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		LogTxt(__name__, "Initializing...")

		self.style_script_data 	= None
		self.ui_data 			= None
		self.object 			= None

		self.script_loader = PythonScriptLoader()

		self.init = self.load()

		self.ref_titlebar_info 	= self.find_object(self.object.Children, "titlebar_info")
		self.ref_object_list 	= self.find_object(self.object.Children, "object_list")
		self.ref_board 			= self.find_object(self.object.Children, "board")

		self.ref_object_list.OnMouseWheel = self.ref_object_list.scrollBar.OnMouseWheel

		LogTxt(__name__, "Initialized!")

	def find_object(self, objects, object_name):
		for object in objects:
			if object.GetWindowName() == object_name:
				return object
			if hasattr(object, "Children"):
				for child in object.Children:
					if child.GetWindowName() == object_name:
						return child
		return None

	def set_ui_data(self, data):
		self.ui_data = data
		self.arrange_object_list()

	def load(self):
		try:
			self.object = self.script_loader.load_script(self, "C:\\Proto_InterfaceManager\\ifmgr_ui\\stylescripts\\", "style_object_browser.py")
		except:
			LogTxt(__name__, "Failed to load script!")
			return False
		return True

	def update_title_info(self):
		if self.ref_titlebar_info:
			self.ref_titlebar_info.SetText("[ %s objects ]" % len(self.ui_data))

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
				if self.ref_object_list.GetItemCount() != len(self.ui_data):
					self.arrange_object_list()

			self.ref_object_list.OnUpdate()

	def render(self):
		pass

	def arrange_object_list(self):
		# find object_list in object.Children
		if self.ref_object_list:
			self.ref_object_list.ClearItem()
			for object in self.ui_data:
				# print other infos about object
				
				ui_class_name = object
				ui_class_str = 'ui.%s' % ui_class_name
				ui_class = eval(ui_class_str)

				class_init_args = ui_class.__init__.func_code.co_varnames[1:ui_class.__init__.func_code.co_argcount]
				class_init_args_str = ""
				for arg in class_init_args:
					class_init_args_str += "%s, " % arg

				class_init_args_str = class_init_args_str[:-2]

				self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount()," - %s%s" % (ui_class_name, class_init_args))
