# This is my first test of utilizing our script loader.
from pythonscriptloader import PythonScriptLoader
from proto_utils import LogTxt

import ui

class n_object_browser(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		LogTxt(__name__, "Initializing...")

		self.style_script_data 	= None
		self.ui_data 			= None
		self.object 			= None

		self.script_loader = PythonScriptLoader()

		self.init = self.load()

		self.ref_object_list 	= None
		self.ref_board 			= None

		LogTxt(__name__, "Initialized!")

	def set_ui_data(self, data):
		self.ui_data = data
		self.arrange_object_list()

	def load(self):
		try:
			self.object = self.script_loader.load_script(self, "C:\\Proto_InterfaceManager\\ifmgr_ui\\stylescripts\\", "style_object_browser.py")
		except IOError, e:
			LogTxt(__name__, "IOError: %s" % e)
			return False
		except RuntimeError, e:
			LogTxt(__name__, "Runtime Error: %s" % e)
			return False
		except:
			LogTxt(__name__, "Failed to load script!")
			return False
		return True

	def update_title_info(self):
		title_info_ref = None
		for child in self.object.Children:
			if hasattr(child, "Children"):
				for subchild in child.Children:
					if subchild.GetWindowName() == "titlebar_info":
						title_info_ref = subchild
						break
			elif child.GetWindowName() == "titlebar_info":
				title_info_ref = child
				break
		if title_info_ref:
			title_info_ref.SetText("[ %s objects ]" % len(self.ui_data))


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
