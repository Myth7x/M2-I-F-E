import ui, app, wndMgr

from proto_utils import LogTxt

import globals

# this will be a ui.bar the size of the screen
# it will have some info text to the upper left
# it will have a dictionary that holds the scene data
# it will iterate through the scene data and create the ui elements
# we use a bar since we can easily set top_most and make it invisible aswell have all our normal events
class n_scene_demo(ui.Bar):
	def __init__(self):
		ui.Bar.__init__(self)
		LogTxt(__name__, "Initializing...")

		self.parent = None

		self.scene_data     = {}
		self.scene_name     = ""
		self.demo_objects   = {}

		self.clicked = False
		self.crtl_rezize = False
		self.crtl = False
		self.crtl_obj = None
		self.crtl_pos = None
		self.crtl_indicator_bar = None
		
		self.crtl_child_insert_indicator_bar = None
		self.mouse_over_target = None

		self.crtl_context_menu = None

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetPosition(0, 0)
		# set invisible hex color
		self.SetColor(0x00000000)

		self.SetMouseLeftButtonDownEvent(ui.__mem_func__(self.on_left_mouse_button_down), None)

		self.Show()

	def set_parent(self, parent):
		self.parent = parent

	def set_scene_data(self, scene_name, scene_data):
		self.scene_data = scene_data
		self.scene_name = scene_name
		self.create_scene()
	
	def destroy_scene(self):
		for obj in self.demo_objects:
			self.demo_objects[obj].Hide()
			self.demo_objects[obj].Destroy()
		self.demo_objects = {}

	def load_children(self, childs, parent=None):
		for obj in childs:
			try:
				
				# create the ui element
				self.demo_objects[obj['child_name']] = obj['class']()
				# set the position and size
				self.demo_objects[obj['child_name']].AddFlag('movable')
				self.demo_objects[obj['child_name']].AddFlag('float')

				# check this is a child of another object
				if 'parent' in obj:
					self.demo_objects[obj['child_name']].SetParent(self.demo_objects[obj['parent']])

				self.demo_objects[obj['child_name']].SetPosition(obj['x'], obj['y'])
				self.demo_objects[obj['child_name']].SetSize(obj['width'], obj['height'])
				# set control events
				self.demo_objects[obj['child_name']].SetMouseLeftButtonDownEvent(ui.__mem_func__(self.on_left_mouse_button_down), obj['child_name'])
				self.demo_objects[obj['child_name']].OnMouseLeftButtonUp = ui.__mem_func__(self.OnMouseLeftButtonUp)
				# show the demo element
				self.demo_objects[obj['child_name']].Show()

				if 'children' in obj and len(obj['children']) > 0:
					self.load_children(obj['children'], self.demo_objects[obj['child_name']])

			except Exception as e:
				LogTxt(__name__, "Error: %s" % e)
				continue
			LogTxt(__name__, "Created object: %s" % obj)

	def create_scene(self):
		self.destroy_scene()
		LogTxt(__name__, "Creating scene: %s" % self.scene_name)
		self.load_children(self.scene_data['children'])


	def get_object_scene_data(self, obj):
		for child in self.scene_data['children']:
			if child['child_name'] == obj:
				return child
		return None

	def destroy_scene_objects(self):
		for obj in self.demo_objects:
			self.demo_objects[obj].Hide()
			self.demo_objects[obj].Destroy()
		self.demo_objects = {}
		LogTxt(__name__, "Destroyed all scene objects")

	def update_scene_data(self, obj, demo_obj):

		for child in self.scene_data['children']:
			if child['child_name'] == obj:
				child['x'] = demo_obj.GetGlobalPosition()[0]
				child['y'] = demo_obj.GetGlobalPosition()[1]
				child['width'] = demo_obj.GetWidth()
				child['height'] = demo_obj.GetHeight()
				break
		self.parent.on_demo_select_object(obj)

	def on_left_mouse_button_down(self, child):
		self.clicked = True
		self.crtl_obj = child

	def destroy_child_insert_indicator(self):
		self.crtl_child_insert_indicator_bar.Hide()
		self.crtl_child_insert_indicator_bar.Destroy()
		self.crtl_child_insert_indicator_bar = None

	def destroy_indicator(self):
		self.crtl_indicator_bar.Hide()
		self.crtl_indicator_bar.Destroy()
		self.crtl_indicator_bar = None

	def make_child_insert_indicator(self, child, x, y, widht, height):
		self.crtl_child_insert_indicator_bar = ui.Bar("TOP_MOST")
		self.crtl_child_insert_indicator_bar.SetParent(child)
		self.crtl_child_insert_indicator_bar.SetPosition(0, 0)
		self.crtl_child_insert_indicator_bar.SetSize(widht, height)
		self.crtl_child_insert_indicator_bar.SetColor(0x10fcba03)
		self.crtl_child_insert_indicator_bar.Show()

	def update_child_insert_indicator(self, width, height):
		self.crtl_child_insert_indicator_bar.SetSize(width + 4, height + 4)
		self.crtl_child_insert_indicator_bar.Show()

	def make_indicator(self, child, x, y, widht, height):
		self.crtl_indicator_bar = ui.Bar("TOP_MOST")
		self.crtl_indicator_bar.SetParent(child)
		self.crtl_indicator_bar.SetPosition(0, 0)
		self.crtl_indicator_bar.SetSize(widht, height)
		self.crtl_indicator_bar.SetColor(0x10ff1100)
		self.crtl_indicator_bar.Show()

	def update_indicator(self, width, height):
		self.crtl_indicator_bar.SetSize(width + 4, height + 4)
		self.crtl_indicator_bar.Show()

	def update_object_scene_data(self, object, dict):
		for child in self.scene_data['children']:
			if child['child_name'] == object:
				child = dict
				break

	def insert_element_into_target(self, drag_object, target):
		#LogTxt(__name__, "Inserting element %s into target %s" % (drag_object, target))
		
		# get the drag object
		drag_obj = self.get_object_scene_data(drag_object)
		if drag_obj:
			#LogTxt(__name__, "Drag object: %s" % drag_obj)
			drag_obj_pos 	= self.demo_objects[drag_object].GetGlobalPosition()
			#LogTxt(__name__, "Drag object position: %s" % str(drag_obj_pos))

			if target == None:
				if 'parent' in drag_obj:
					
					parent_obj = self.get_object_scene_data(drag_obj['parent'])

					if 'children' in parent_obj:
						parent_obj['children'].remove(drag_obj)
						if len(parent_obj['children']) <= 0:
							del parent_obj['children']
					
					self.update_object_scene_data(drag_obj['parent'], parent_obj)

					del drag_obj['parent']
					self.update_object_scene_data(drag_object, drag_obj)

					self.create_scene()
					
					self.demo_objects[drag_object].OnMouseLeftButtonUp()
					self.demo_objects[drag_object].OnMouseLeftButtonDown()

					self.parent.update_scene_data(self.scene_data)
					return True

			target_obj 		= self.get_object_scene_data(target)
			if target_obj:
				#LogTxt(__name__, "Target object: %s" % target_obj)
				target_obj_pos 	= self.demo_objects[target].GetGlobalPosition()
				#LogTxt(__name__, "Target object position: %s" % str(target_obj_pos))

				# update scene data
				# dragged object
				drag_obj['parent'] = target
				drag_obj['x'] = drag_obj_pos[0] - target_obj_pos[0]
				drag_obj['y'] = drag_obj_pos[1] - target_obj_pos[1]
				# target object
				if not 'children' in target_obj:
					target_obj['children'] = []
				if not drag_obj in target_obj['children']:
					target_obj['children'].append(drag_obj)

				self.update_object_scene_data(drag_object, drag_obj)
				self.update_object_scene_data(target, target_obj)

				# update the scene
				self.create_scene()
				LogTxt(__name__, "Inserted element %s into target %s" % (drag_object, target))
				
				self.parent.update_scene_data(self.scene_data)
	
	def OnMouseLeftButtonUp(self):
		self.clicked = False

	def OnUpdate(self):
		if self.clicked == True and self.crtl_obj != None:


			crtl_scene_object = self.get_object_scene_data(self.crtl_obj)
			if crtl_scene_object:

				current_position 	= self.demo_objects[self.crtl_obj].GetGlobalPosition()
				current_size 		= (self.demo_objects[self.crtl_obj].GetWidth(), self.demo_objects[self.crtl_obj].GetHeight())
				mouse_position 		= wndMgr.GetMousePosition()

				parent_position = None

				if 'parent' in crtl_scene_object:
					parent = crtl_scene_object['parent']
					parent_position	= self.demo_objects[parent].GetGlobalPosition()
					current_position = (current_position[0] - parent_position[0], current_position[1] - parent_position[1])
							


				# if shift is pressed, we can resize the ui element
				if app.IsPressed(app.DIK_LSHIFT):

					if self.crtl_pos == None:
						self.crtl_pos = current_position

					if 'parent' in crtl_scene_object and parent_position != None:
						mouse_position = (mouse_position[0] - parent_position[0], mouse_position[1] - parent_position[1])

					# mouse distance to left border of ui
					mouse_distance_x = mouse_position[0] - (self.crtl_pos[0] if parent_position == None else self.crtl_pos[0] - parent_position[0])
					# mouse distance to top border of ui
					mouse_distance_y = mouse_position[1] - (self.crtl_pos[1] if parent_position == None else self.crtl_pos[1] - parent_position[1])

					# calculate the new size
					new_width 	= mouse_distance_x
					new_height 	= mouse_distance_y

					if parent_position:
						new_width -= parent_position[0]
						new_height -= parent_position[1]

					# set the new size
					self.demo_objects[self.crtl_obj].SetSize(new_width, new_height)
					self.demo_objects[self.crtl_obj].SetPosition(self.crtl_pos[0], self.crtl_pos[1])
					
					self.crtl_rezize = True
				else:
					self.crtl_pos = current_position

					if self.crtl_rezize == True:
						self.demo_objects[self.crtl_obj].OnMouseLeftButtonUp()
						self.crtl_rezize = False
						self.clicked = False
						self.crtl_obj = None
						return False

					is_over_child = False

					# check if is moving element over another element
					#LogTxt(__name__, "Checking if is moving element over another element")
					for obj in self.demo_objects:
						if obj != self.crtl_obj:


							# get the position of the other element
							other_position = self.demo_objects[obj].GetGlobalPosition() if not 'parent' in self.get_object_scene_data(obj) else (self.demo_objects[obj].GetGlobalPosition()[0] - self.demo_objects[self.get_object_scene_data(obj)['parent']].GetGlobalPosition()[0], self.demo_objects[obj].GetGlobalPosition()[1] - self.demo_objects[self.get_object_scene_data(obj)['parent']].GetGlobalPosition()[1])
							# get the size of the other element
							other_size = (self.demo_objects[obj].GetWidth(), self.demo_objects[obj].GetHeight())
							# check if the mouse is over the other element
							if mouse_position[0] > other_position[0] and mouse_position[0] < other_position[0] + other_size[0] and mouse_position[1] > other_position[1] and mouse_position[1] < other_position[1] + other_size[1]:
								#LogTxt(__name__, "Is in: %s" % obj)

								if self.crtl_child_insert_indicator_bar == None:
									self.make_child_insert_indicator(self.demo_objects[obj], other_position[0], other_position[1], self.demo_objects[obj].GetWidth(), self.demo_objects[obj].GetHeight())
								else:
									self.update_child_insert_indicator(other_size[0], other_size[1])
								
								is_over_child = True

								self.mouse_over_target = obj
								break
	
					
					if is_over_child == False:
						# insert the element into the target
						self.insert_element_into_target(self.crtl_obj, None)
						self.mouse_over_target = None
						if self.crtl_child_insert_indicator_bar != None:
							self.destroy_child_insert_indicator()
				# update the indicator bar
				if self.crtl_indicator_bar == None:

					# update the cursor icon
					if app.IsPressed(app.DIK_LSHIFT):
						app.SetCursor(app.HVSIZE)
					else:
						app.SetCursor(app.CAMERA_ROTATE)

					self.make_indicator(self.demo_objects[self.crtl_obj], self.crtl_pos[0], self.crtl_pos[1], self.demo_objects[self.crtl_obj].GetWidth(), self.demo_objects[self.crtl_obj].GetHeight())
				else:
					self.update_indicator(self.demo_objects[self.crtl_obj].GetWidth(), self.demo_objects[self.crtl_obj].GetHeight())

				# update the scene data
				self.update_scene_data(self.crtl_obj, self.demo_objects[self.crtl_obj])
		
		elif self.clicked == False and self.mouse_over_target:
			
			# insert the element into the target
			self.insert_element_into_target(self.crtl_obj, self.mouse_over_target)
			self.mouse_over_target = None
			#LogTxt(__name__, "Inserting element %s into target %s" % (self.crtl_obj, self.mouse_over_target))
				
		elif self.clicked == False :

			self.crtl_obj = None
			self.clicked 	= False
			self.crtl_pos 	= None

			if self.crtl_child_insert_indicator_bar != None:
				self.destroy_child_insert_indicator()

			if self.crtl_indicator_bar != None:
				# reset the cursor icon
				app.SetCursor(app.NORMAL)
				# destroy the indicator bar
				self.destroy_indicator()
			
	def OnRender(self):
		pass
