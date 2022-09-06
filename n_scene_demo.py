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

		self.crtl = False
		self.crtl_obj = None
		self.crtl_indicator_bar = None

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetPosition(0, 0)
		# set invisible hex color
		self.SetColor(0x00000000)
		# make clickthrough
		self.SetWindowHorizontalAlignCenter()
		self.SetWindowVerticalAlignCenter()

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
			# create the ui element
			self.demo_objects[obj['child_name']] = obj['class']()
			# set the position and size
			self.demo_objects[obj['child_name']].SetPosition(obj['x'], obj['y'])
			self.demo_objects[obj['child_name']].SetSize(obj['width'], obj['height'])
			
			self.demo_objects[obj['child_name']].SetParent(self)
			self.demo_objects[obj['child_name']].Show()
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

	def OnUpdate(self):
		if self.crtl == False:
			if self.crtl_indicator_bar != None:
				self.crtl_indicator_bar.Hide()
				self.crtl_indicator_bar.Destroy()
				self.crtl_indicator_bar = None
		# check if mouse is in one of the ui elements
		for obj in self.demo_objects:
			if self.demo_objects[obj].IsIn() or self.ctrl == True and self.crtl_obj == obj:
				LogTxt(__name__, "Mouse is in: %s" % obj)

				# if now ctrl is pressed, we can move the ui element
				if app.IsPressed(app.DIK_LCONTROL):
					# get the mouse position
					mouse_x, mouse_y = wndMgr.GetMousePosition()
					# get the ui element position
					x, y = self.demo_objects[obj].GetGlobalPosition()
					# get the ui element size
					width, height = (self.demo_objects[obj].GetWidth(), self.demo_objects[obj].GetHeight())
					# set the new position
					self.demo_objects[obj].SetPosition(mouse_x - width/2, mouse_y - height/2)
					# update the scene data
					self.update_scene_data(obj, self.demo_objects[obj])
					self.ctrl = True
					self.crtl_obj = obj

					if self.crtl_indicator_bar == None:
						self.crtl_indicator_bar = ui.Bar()
						self.crtl_indicator_bar.SetParent(self)
						self.crtl_indicator_bar.SetColor(0x55a1d162)
					self.crtl_indicator_bar.SetSize(width, height)
					self.crtl_indicator_bar.SetPosition(x, y)
					self.crtl_indicator_bar.Show()

					break
				# if shift is pressed, we can resize the ui element
				if app.IsPressed(app.DIK_LSHIFT):
					LogTxt(__name__, "Resizing: %s" % obj)
					# get the mouse position
					mouse_x, mouse_y = wndMgr.GetMousePosition()
					# get the ui element position
					x, y = self.demo_objects[obj].GetGlobalPosition()
					# we resize the ui element to the mouse position + 25
					self.demo_objects[obj].SetSize(mouse_x - x + 25, mouse_y - y + 25)
					# update the scene data
					self.update_scene_data(obj, self.demo_objects[obj])
					self.ctrl = True
					self.crtl_obj = obj

					if self.crtl_indicator_bar == None:
						self.crtl_indicator_bar = ui.Bar()
						self.crtl_indicator_bar.SetParent(self)
						self.crtl_indicator_bar.SetColor(0x55a1d162)
					self.crtl_indicator_bar.SetSize(self.demo_objects[obj].GetWidth(), self.demo_objects[obj].GetHeight())
					self.crtl_indicator_bar.SetPosition(x, y)
					self.crtl_indicator_bar.Show()

					break
		
		# if ctrl is released, we stop moving and resizing
		if app.IsPressed(app.DIK_LCONTROL) == False and app.IsPressed(app.DIK_LSHIFT) == False:
			self.ctrl = False
			self.crtl_obj = None

	def OnRender(self):
		pass
