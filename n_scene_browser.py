# Second Window with our own scriptloader, but i realized, we gonna use the original ones for functionality
from distutils.log import Log
from pythonscriptloader import PythonScriptLoader
from proto_utils import LogTxt

import n_attribute_editor

import ui, wndMgr

import globals

class n_scene_browser(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		LogTxt(__name__, "Initializing...")

		self.style_script_data 	= None
		self.object 			= None
		self.parent 			= None

		self.scene_obj_editor 	= None

		self.scene = {
			"name": "*New Scene",
			"children": []
		}

		self.script_loader = PythonScriptLoader()

		self.init = self.load()

		self.ref_titlebar_title 		= self.find_object(self.object.Children, "titlebar_title")
		self.ref_object_list 	= self.find_object(self.object.Children, "object_list")
		self.ref_board 			= self.find_object(self.object.Children, "board")

		self.ref_object_list.OnMouseWheel = self.ref_object_list.scrollBar.OnMouseWheel
		self.ref_object_list.OnMouseLeftButtonDoubleClick = self.on_double_click_object_list

		self.scene_obj_editor = n_attribute_editor.n_attribute_editor()
		self.scene_obj_editor.set_parent(self)
		self.scene_obj_editor.ref_board.SetCloseEvent(self.on_close_object_editor)
		self.scene_obj_editor.ref_board.Hide()

		self.scene_obj_editor_open = False

		LogTxt(__name__, "Initialized!")

	def on_close_object_editor(self):
		LogTxt(__name__, "Closing object editor...")
		self.scene_obj_editor.ref_board.Hide()
		self.scene_obj_editor_open = False

	def get_scene_data(self):
		return self.scene

	def set_scene_name(self, name):
		self.scene['name'] = name

	def set_parent(self, parent):
		self.parent = parent

	def on_double_click_object_list(self):
		selected_object = self.get_selected_children()
		LogTxt(__name__, "Selected scene object: %s" % selected_object)
		if selected_object != None and self.scene_obj_editor_open == False:
			self.scene_obj_editor.set_scene_object(selected_object)
			self.scene_obj_editor.ref_board.Show()
			self.scene_obj_editor_open = True
		else:
			LogTxt(__name__, "Selected object is None!")


	def add_scene_object(self, data):
		LogTxt(__name__, "Adding object to scene...")
		new_name = data[0]
		for child in self.scene['children']:
			if child['child_name'] == new_name:
				LogTxt(__name__, "Object already exists!")
				object_count = 0
				for child2 in self.scene['children']:
					if child2['class'] == child['class']:
						object_count += 1
				new_name = "%s_%d" % (new_name, object_count)
				
		_child = {
			'child_name': new_name,
			'object_name': data[0],
			'class': data[1],
			'object': data[2],
			'x': 10,
			'y': 10,
			'width': 100,
			'height': 100,
			'event': {
				'__init__': [],
				'__del__': [],
				'OnUpdate': [],
				'OnRender': [],
			}
		}
		self.scene['children'].append(_child)
		LogTxt(__name__, "Adding object to scene: %s" % _child['child_name'])

	def update_scene_data(self, data):
		self.scene = data
		self.arrange_object_list()
		self.parent.refresh_scene_demo()
		LogTxt(__name__, "Refreshing scene demo...")


	# Finds specific object in a list of objects, used for iterating through the ui tree(children)
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
			self.object = self.script_loader.load_script(self, "C:\\Proto_InterfaceManager\\ifmgr_ui\\stylescripts\\", "style_scene_browser.py")
		except:
			LogTxt(__name__, "Failed to load script!")
			return False
		return True

	# return ui data dictionary
	def get_selected_object(self):
		if self.ref_object_list.GetItemCount() > 0:
			if self.ref_object_list.GetSelectedItem() != -1:
				selected_object = self.ref_object_list.GetSelectedItemText()
				try:
					return globals.UI_CLASS_DATA[selected_object]
				except:
					return None
		return None
	
	# returns the children dictionary with set values
	def get_selected_children(self):
		selected_object = self.ref_object_list.GetSelectedItemText()
		if selected_object == None:
			return None

		# Find dict in self.scene['children'] with the name of the selected object
		for child in self.scene['children']:
			if child['child_name'] == selected_object:
				return child

		return None

	def update_title_info(self):
		self.ref_titlebar_title.SetText("[ %s : %d children ]" % (self.scene['name'], self.ref_object_list.GetItemCount()))

	def update(self):
		if self.init == True:
			self.update_title_info()

			## do stuff here
			if self.ref_object_list.GetItemCount() != len(self.scene['children']):
				self.arrange_object_list()
				self.parent.refresh_scene_demo()
				LogTxt(__name__, "Refreshing scene demo...")
		
			self.ref_object_list.OnUpdate()

	def render(self):
		pass

	def arrange_object_list(self):
		self.ref_object_list.ClearItem()
		for child in self.scene['children']:
			self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), child['child_name'])


