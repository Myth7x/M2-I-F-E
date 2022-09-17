# coding: utf-8
# Second Window with our own scriptloader, but i realized, we gonna use the original ones for functionality
import copy
from distutils.log import Log
from _utils.pythonscriptloader import PythonScriptLoader
from _utils import LogTxt

import attribute_editor
from scene_demo import scene_demo

import ui, wndMgr

import globals

class scene_browser(ui.ScriptWindow):
	"""
	scene browser class
	- holds current scene data
	"""
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

		self.depth = 0

		self.scene_obj_editor = attribute_editor.attribute_editor()
		self.scene_obj_editor.set_parent(self)
		self.scene_obj_editor.ref_board.SetCloseEvent(self.on_close_object_editor)
		self.scene_obj_editor.ref_board.Hide()

		self.OnUpdate = self.update

		self.scene_obj_editor_open = False

		LogTxt(__name__, "Initialized!")

	def on_close_object_editor(self):
		LogTxt(__name__, "Closing object editor...")
		self.scene_obj_editor.ref_board.Hide()
		self.scene_obj_editor_open = False

	def toggle_scene_demo_refresh(self):
		self.parent.forward_scene_demo_refresh()

	def set_scene_name(self, name):
		self.scene['name'] = name
		self.toggle_scene_demo_refresh()

	def set_parent(self, parent):
		self.parent = parent
		self.toggle_scene_demo_refresh()

	# on scene object list double click open object attribute editor
	def on_double_click_object_list(self):
		selected_object = self.get_selected_children()
		if selected_object != None and self.scene_obj_editor_open == False:
			self.scene_obj_editor.set_scene_object(selected_object)
			self.scene_obj_editor.ref_board.Show()
			self.scene_obj_editor_open = True
		else:
			LogTxt(__name__, "Selected object is None!")

	def find_available_name_recursive(self, name, children):
		for child in children:
			if child['child_name'] == name:
				return self.find_available_name_recursive(name + "_", children)
		return name

	# add scene object by name with ui_gatherer data
	def add_scene_object(self, name, data):
		LogTxt(__name__, "================================================================================")
		LogTxt(__name__, "Adding scene object... %s" % name)
		
		child_name = self.find_available_name_recursive(name, self.scene['children'])		
		_child = {
			'child_name': child_name,
			'object_name': data[0],
			'parent':None,
			'class': data[1],
			'object': data[2],
			'x': wndMgr.GetScreenWidth() / 2 - 100 / 2,
			'y': wndMgr.GetScreenHeight() / 2 - 100 / 2,
			'width': 100,
			'height': 100,
		}

		self.scene['children'].append(_child)
		self.parent.scene_demo.add_scene_object_data(child_name, _child)
		LogTxt(__name__, "================================================================================")
		return

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

	# load ui from script
	def load(self):
		try:
			self.object = self.script_loader.load_script(self, "C:\\InterfaceManager\\ifmgr_ui\\stylescripts\\", "style_scene_browser.py")
		except:
			LogTxt(__name__, "Failed to load script!")
			return False
		return True

	# get scene object data dictionary by name
	def get_scene_object_data(self, object_name):
		for child in self.scene['children']:
			if child['child_name'] == object_name:
				return child
		return None

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
		return self.get_scene_object_data(selected_object)

	# Update UI Extra
	def update(self):
		if self.init == True:
			self.ref_titlebar_title.SetText("[ %s : %d children ]" % (self.scene['name'], self.ref_object_list.GetItemCount()))

			if self.ref_object_list.GetItemCount() != len(self.scene['children']):
				self.arrange_object_list()
				pass
			
			#self.ref_object_list.Update()

	# Render UI Extra
	def render(self):
		pass

	def update_scene_object_data(self, data):
		for obj_name in data:
			obj = data[obj_name]
			scene_data = self.get_scene_object_data(obj.child_name)
			if scene_data != None:
				scene_data['x'] = obj.x
				scene_data['y'] = obj.y
				scene_data['width'] = obj.width
				scene_data['height'] = obj.height
				scene_data['parent'] = obj.parent

		self.arrange_object_list()

	def iterate_object_list(self, data, parent_name):
		for child in data:
			if child['parent'] == parent_name:
	
				self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '|- %s' % child['child_name'])
				self.iterate_object_list(self.scene['children'], child['child_name'])

	def recursive_create_object_list(self, data, parent_name, prefix):
		original_depth = self.depth
		tabulator = ''
		for x in xrange(self.depth):
			tabulator += '\t' + '|' if x != self.depth - 1 else '\t'
		for child in data:
			if child['parent'] == parent_name:
				self.depth += 1


				
				tabulator_str = '|%s' % tabulator
				final_str = '|%s|%s %s' % (tabulator, prefix, child['child_name'])
				self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), final_str)
				
				self.recursive_create_object_list(self.scene['children'], child['child_name'], prefix)
		
		self.depth = original_depth
		# set self.depth back to our original depth

	# Refreshes the object list
	def arrange_object_list(self):
		self.ref_object_list.ClearItem()
		# wir bauen uns ein dict, dat konnen wir
		parent_names = []
		for child in self.scene['children']:
			if child['parent'] == None:
				parent_names.append(child['child_name'])

		self.depth = 1

		for parent_name in parent_names:
			self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '|-- %s ' % parent_name)
			original_depth = self.depth
			self.recursive_create_object_list(self.scene['children'], parent_name, "--")
			#if len(self.scene['children']) > 0 and self.ref_object_list.GetItemCount()-1 < len(self.scene['children']):
			#	self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '|----------------------------------------')
			self.depth = original_depth
			#self.iterate_object_list(self.scene['children'], parent_name)
