from app import IsPressed, DIK_LSHIFT
from proto_utils import LogTxt
from wndMgr import GetMousePosition
import ui

#from ..proto_utils import LogTxt

# Our Main Board Class, will be used for all our Browser Boards (Objects, Project, Attributes, and what might be added later)
class IfMgr_Board(ui.ScriptWindow):
	size = (0, 0)
	sizing = False
	pos_move_original = [-1, -1]
	script_data = {}

	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		for child in self.Children: child.Destroy()
		ui.ScriptWindow.__del__(self)

	def add_custom_flag(self, flag):
		self.cf = flag

	def update_children_size(self, children):
		for child in children:
			# Has children? Recursively call this function
			if hasattr(child, "Children"):
				self.update_children_size(child.Children)

			# Update the child's size
			_class = child.__class__
			if _class == ui.TitleBar:
				child.SetWidth(self.size[0])
			else:
				child.SetSize(self.size[0], self.size[1])

	def update_size(self, width, height):
		self.size 		= (width, height)

		self.SetSize(*self.size)
		self.update_children_size(self.Children)

	def update_children_pos_relative(self, children, new_parent_width, new_parent_height):
		for child in children:
			# Has children? Recursively call this function
			#if hasattr(child, "Children"):
			#	self.update_children_pos_relative(child.Children, new_parent_width, new_parent_height)

			# Update the child's position
			_child = None
			for _data_child in self.script_data['children']:
				if _data_child['name'] == child.GetWindowName():
					_child = _data_child
					break
			
			if _child != None:
				LogTxt("IfMgr_Board", "Updating Child: %s" % _child['name'])

				if not 'type' in _child or _child["type"] == "board" or _child["type"] == "window":
					continue
				elif _child["type"] == "titlebar":
					self.update_children_pos_relative(child.Children, new_parent_width, new_parent_height)
					continue

				start_position = (_child["x"], _child["y"])
				start_size = (_child["width"], _child["height"]) if 'width' in _child else (self.script_data['width'], self.script_data['height'])
				new_position = (start_position[0] * new_parent_width / start_size[0], start_position[1] * new_parent_height / start_size[1])
				child.SetPosition(new_position[0], new_position[1])	
				

	def OnUpdate(self):
		self.script_data = self.__dict__['script_data']
		
		LogTxt("IfMgr_Board", "Looking for Data Dict: %s" % self.__dict__)
		if self.cf == "sizeable":

			xMouse, yMouse = GetMousePosition()
			x, y = self.GetGlobalPosition()

			if xMouse > x + self.size[0] - 55 \
					and yMouse > y + self.size[1] - 55 \
					and IsPressed(DIK_LSHIFT) == True or self.sizing == True \
					and IsPressed(DIK_LSHIFT) == True:

				if self.pos_move_original[0] == -1:
					self.pos_move_original = (x, y)
				
				self.sizing = True

				self.update_size(xMouse - x, yMouse - y)
				self.update_children_pos_relative(self.Children, self.size[0], self.size[1])
				self.SetPosition(self.pos_move_original[0], self.pos_move_original[1])
			else:
				self.sizing = False
				self.pos_move_original = [-1, -1]

	def __del__(self):
		ui.ScriptWindow.__del__(self)