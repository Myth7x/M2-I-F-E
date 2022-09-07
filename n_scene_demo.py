from distutils.log import Log
import ui
import app
import wndMgr

import globals

from proto_utils import LogTxt

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
		self.crtl = False
		self.crtl_obj = None
		self.crtl_pos = None
		self.crtl_indicator_bar = None

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

	def create_scene(self):
		self.destroy_scene()
		LogTxt(__name__, "%s" % self.scene_data)
		# iterate through the scene data and create the ui elements
		for obj in self.scene_data['children']:
			try:
				# create the ui element
				self.demo_objects[obj['child_name']] = obj['class']()
				# set the position and size
				self.demo_objects[obj['child_name']].AddFlag('movable')
				self.demo_objects[obj['child_name']].AddFlag('pick')
				self.demo_objects[obj['child_name']].AddFlag('float')

				self.demo_objects[obj['child_name']].SetPosition(obj['x'], obj['y'])
				self.demo_objects[obj['child_name']].SetSize(obj['width'], obj['height'])
				# set control events
				self.demo_objects[obj['child_name']].SetMouseLeftButtonDownEvent(ui.__mem_func__(self.on_left_mouse_button_down), obj['child_name'])
				self.demo_objects[obj['child_name']].OnMouseLeftButtonUp = ui.__mem_func__(self.OnMouseLeftButtonUp)
				# show the demo element
				self.demo_objects[obj['child_name']].Show()
			except Exception as e:
				LogTxt(__name__, "Error: %s" % e)
				continue
			LogTxt(__name__, "Created object: %s" % obj)

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

	def destroy_indicator(self):
		self.crtl_indicator_bar.Hide()
		self.crtl_indicator_bar.Destroy()
		self.crtl_indicator_bar = None

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

	def OnMouseLeftButtonUp(self):
		self.clicked = False
		self.crtl_obj = None

	def OnUpdate(self):
		if self.clicked == True and self.crtl_obj != None:

			current_position 	= self.demo_objects[self.crtl_obj].GetGlobalPosition()
			current_size 		= (self.demo_objects[self.crtl_obj].GetWidth(), self.demo_objects[self.crtl_obj].GetHeight())
			mouse_position 		= wndMgr.GetMousePosition()

			# if shift is pressed, we can resize the ui element
			if app.IsPressed(app.DIK_LSHIFT):

				if self.crtl_pos == None:
					self.crtl_pos = current_position

				# mouse distance to left border of ui
				mouse_distance_x = mouse_position[0] - self.crtl_pos[0]
				# mouse distance to top border of ui
				mouse_distance_y = mouse_position[1] - self.crtl_pos[1]

				# calculate the new size
				new_width 	= mouse_distance_x
				new_height 	= mouse_distance_y

				# set the new size
				self.demo_objects[self.crtl_obj].SetSize(new_width, new_height)
				self.demo_objects[self.crtl_obj].SetPosition(self.crtl_pos[0], self.crtl_pos[1])
		
			else:
				self.crtl_pos = current_position

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

		# if ctrl is released, we stop moving and resizing
		if self.clicked == False or self.crtl_obj == None:
			self.crtl_obj 	= None
			self.clicked 	= False
			self.crtl_pos 	= None

			if self.crtl_indicator_bar != None:
				# reset the cursor icon
				app.SetCursor(app.NORMAL)
				# destroy the indicator bar
				self.destroy_indicator()

	def OnRender(self):
		pass
