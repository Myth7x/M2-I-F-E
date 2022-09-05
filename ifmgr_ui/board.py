from app import IsPressed, DIK_LSHIFT
from proto_utils import LogTxt
from wndMgr import GetMousePosition, GetScreenHeight, GetScreenWidth
import ui

#from ..proto_utils import LogTxt

import globals

# Our Main Board Class, will be used for all our Browser Boards (Objects, Project, Attributes, and what might be added later)
class Board_Custom(ui.ScriptWindow):
	script_data 		= {}
	sizeable 			= {}
	size 				= (0, 0)
	instruction_data 	= []

	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def set_sizeable_data(self, data):
		self.sizeable = data

	def set_instruction_data(self, data):
		self.instruction_data = data

	def add_custom_flag(self, flag):
		self.cf = flag

	def is_in_bounds(self, x, y):
		pos = self.GetGlobalPosition()
		size = (self.GetWidth(), self.GetHeight())
		
		if x >= pos[0] and x <= pos[0] + size[0] and \
			y >= pos[1] and y <= pos[1] + size[1]:

			return True
		return False

	def OnRender(self):
		for instruction in self.instruction_data:
			if instruction['type'] == "on_render":
				exec("exec('%s')" % instruction['exec_string'])

	def is_focused(self, children):
		focus = self.IsFocus()
		if focus == 0:
			for child in children:
				if hasattr(child, "Children"):
					focus = self.is_focused(child.Children)
				else:
					if child.IsFocus():
						focus = True
						break
		#LogTxt("TEST", "IsFocus: Window(%s) State(%s)" % (self.GetWindowName(), focus))
		return focus

	def hide_children(self, children):
		for child in children:
			if child.__class__ != ui.Board and child.__class__ != ui.TitleBar:
				child.Hide()
	
	def show_children(self, children):
		for child in children:
			if hasattr(child, "Children"):
				self.show_children(child.Children)
			else:
				child.Show()
	
	def OnMoveWindow(self, x, y):
		return True

	def OnRender(self):
		if 'parent' in self.__dict__:
			self.__dict__['parent'].render()
		return True

	def OnUpdate(self):
		self.script_data = self.__dict__['script_data']

		if 'parent' in self.__dict__:
			self.__dict__['parent'].update()

		# yea this is nasty, will be removed later
		for instruction in self.instruction_data:
			if instruction['type'] == "on_update":
				exec("exec('%s')" % instruction['exec_string'])

	def __del__(self):
		ui.ScriptWindow.__del__(self)