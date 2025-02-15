# coding: utf-8
# Second Window with our own scriptloader, but i realized, we gonna use the original ones for functionality
import copy
from distutils.log import Log
import inspect
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

		self.last_object_list_data = None

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
		self.OnMouseWheel = self.ref_object_list.OnMouseWheel


		self.depth = 0

		self.scene_obj_editor = attribute_editor.attribute_editor()
		self.scene_obj_editor.set_parent(self)
		self.scene_obj_editor.ref_board.SetCloseEvent(self.on_close_object_editor)
		self.scene_obj_editor.ref_board.Hide()

		self.OnUpdate = self.update

		self.scene_obj_editor_open = False

		LogTxt(__name__, "Initialized!")

	# load ui from script
	def load(self):
		try:
			self.object = self.script_loader.load_script(self, "C:\\InterfaceManager\\ifmgr_ui\\stylescripts\\", "style_scene_browser.py")
		except:
			LogTxt(__name__, "Failed to load script!")
			return False
		return True

	def update_object_attributes(self, child_name, attribute_list):
		"""update object attributes"""
		#for attr in attribute_list:
		#	LogTxt(__name__, "Updating attribute < %s:%s >" % (attr.name, attr.value))
		#	self.get_scene_object_data(child_name)[attr.name] = attr.value
		
		self.parent.update_object_attributes(child_name, attribute_list)

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
		self.SetParent(parent)

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
				t_name = child['child_name'].split("_")
				if len(t_name) >= 2:
					num = int(child['child_name'].split("_")[1])
					if num == 0 or num == None:
						num = 1
					num += 1
					return self.find_available_name_recursive("%s_%s" % (name.split("_")[0], num), children)
				else:
					return self.find_available_name_recursive("%s_1" % name, children)
		return name

	def add_scene_object(self, name, data):
		"""add scene object by name with ui_gatherer data"""
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
		#self.arrange_object_list(data)
		return

	def find_object(self, objects, object_name):
		"""find object by name in list of objects"""
		for object in objects:
			if object.GetWindowName() == object_name:
				return object
			if hasattr(object, "Children"):
				for child in object.Children:
					if child.GetWindowName() == object_name:
						return child
		return None

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

		# extract tree elements
		tree_elements = selected_object.replace(' ', '')
		tree_elements = tree_elements.replace('|', '')
		tree_elements = tree_elements.replace('-', '')
		tree_elements = tree_elements.replace('+', '')
		tree_elements = tree_elements.replace('`', '')
		LogTxt(__name__, "Tree elements: %s" % tree_elements)

		# Find dict in self.scene['children'] with the name of the selected object
		return self.get_scene_object_data(tree_elements)

	# Update UI Extra
	def update(self):
		if self.init == True:
			self.ref_titlebar_title.SetText("[ %s : %d children ]" % (self.scene['name'], self.ref_object_list.GetItemCount()))

			if self.ref_object_list.GetItemCount() != len(self.scene['children']):
				self.last_object_list_data = None
				#self.arrange_object_list(None)
				pass
			
			#self.ref_object_list.Update()

	# Render UI Extra
	def render(self):
		pass

	def compare_dict(self, d1, d2):
		if d1 != d2:
			return False
		
		for x in xrange(len(d1)):
			if d1[x] != d2[x]:
				return False
			else:
				if d1[x] == None:
					return False
				elif d1[x].child_name != d2[x].child_name:
					return False
				elif d1[x].parent != d2[x].parent:
					return False
				elif d1[x].x != d2[x].x:
					return False
				elif d1[x].y != d2[x].y:
					return False
				elif d1[x].width != d2[x].width:
					return False
				elif d1[x].height != d2[x].height:
					return False


		return True

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
		#self.arrange_object_list(data)
		#if self.last_object_list_data == None or self.compare_dict(data, self.last_object_list_data) == False:
		#	LogTxt(__name__, "Scene data and object data are not the same!")
		#	self.arrange_object_list(data)
		#	self.last_object_list_data = data


	def iterate_object_list(self, data, parent_name):
		parent_child_count = self.count_children(self.scene['children'], parent_name)
		for child in data:
			if child['parent'] == parent_name:
				if parent_child_count - self.ref_object_list.GetItemCount() > 1:
					self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '|- %s' % child['child_name'])
				else:
					self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '`- %s' % child['child_name'])
				self.iterate_object_list(self.scene['children'], child['child_name'])

	def count_children(self, data, parent_name):
		count = 0
		for child in data:
			if child['parent'] == parent_name:
				count += 1
				count += self.count_children(self.scene['children'], child['child_name'])
		return count

	def recursive_create_object_list(self, data, parent_name, prefix):
		original_depth = self.depth
		tabulator = ''
		for x in xrange(self.depth):
			tabulator += '  |'
		self.depth += 1
		for child in data:
			if child['parent'] == parent_name:
				orig_prefix = prefix
				if self.count_children(self.scene['children'], child['child_name']) > 0:
					prefix = prefix[:-1] + '+'
					final_str = '|%s|%s %s' % (tabulator, prefix, child['child_name'])
				else:
					final_str = '|%s|%s %s' % (tabulator, prefix, child['child_name'])

				self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), final_str)
				
				self.recursive_create_object_list(self.scene['children'], child['child_name'], orig_prefix)
		
		self.depth = original_depth
		# set self.depth back to our original depth

	# Refreshes the object list
	def arrange_object_list(self):
		
		self.ref_object_list.ClearItem()
		
		# log caller
		#LogTxt(__name__, "arrange_object_list called from %s" % inspect.stack()[1][3])

		# wir bauen uns ein dict, dat konnen wir
		parent_names = []
		for child in self.scene['children']:
			if child['parent'] == None:
				parent_names.append(child['child_name'])

		self.depth = 1
		#if len(parent_names) > 0:
		#	self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '|')
		for parent_name in parent_names:
			selected_scene_browser_obj_text = self.ref_object_list.GetSelectedItemText()
			if self.ref_object_list.GetItemCount() >= 1:
				self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '|')

			if self.count_children(self.scene['children'], parent_name) > 0:
				self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '|-+ %s ' % parent_name)
			else:
				self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '|-- %s ' % parent_name)
			original_depth = self.depth
			self.recursive_create_object_list(self.scene['children'], parent_name, "--")
			#if len(self.scene['children']) > 0 and self.ref_object_list.GetItemCount() < len(self.scene['children']):
			#	self.ref_object_list.InsertItem(self.ref_object_list.GetItemCount(), '|')
			self.depth = original_depth
			#self.iterate_object_list(self.scene['children'], parent_name)