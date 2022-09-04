from app import IsPressed, DIK_LSHIFT
from proto_utils import LogTxt
from wndMgr import GetMousePosition, GetScreenHeight, GetScreenWidth
import ui

#from ..proto_utils import LogTxt

import globals

# Our Main Board Class, will be used for all our Browser Boards (Objects, Project, Attributes, and what might be added later)
class IfMgr_Board(ui.ScriptWindow):
	is_resizing 		= False
	pos_move_original 	= None
	scaling_border		= None
	scaling_info        = None
	script_data 	= {}
	sizeable 		= {}
	size 			= (0, 0)

	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		for child in self.Children: child.Destroy()
		ui.ScriptWindow.__del__(self)

	def set_sizeable_data(self, data):
		self.sizeable = data

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
		# Truncate the size to the minimum/maximum size
		self.size 		= (
			max(self.sizeable['min_width'], min(width, self.sizeable['max_width'])), 
			max(self.sizeable['min_height'], min(height, self.sizeable['max_height']))
		)
		
		current_position = self.GetGlobalPosition()
		out_of_bounds = False
		if current_position[0] + self.size[0] > GetScreenWidth():
			out_of_bounds = True
			current_position = (GetScreenWidth() - self.size[0], current_position[1])
		if current_position[1] + self.size[1] > GetScreenHeight():
			out_of_bounds = True
			current_position = (current_position[0], GetScreenHeight() - self.size[1])

		if out_of_bounds == False:
			self.SetSize(*self.size)
		self.update_children_size(self.Children)

	def update_children_pos_relative(self, children, new_parent_width, new_parent_height):
		for child in children:

			# Update the child's position
			_child = None
			for _data_child in self.script_data['children']:
				if _data_child['name'] == child.GetWindowName():
					_child = _data_child
					break
			
			if _child != None:
				#LogTxt("IfMgr_Board", "Updating Child: %s" % _child['name'])

				if not 'type' in _child or _child["type"] == "board" or _child["type"] == "window":
					continue
				elif _child["type"] == "titlebar":
					self.update_children_pos_relative(child.Children, new_parent_width, new_parent_height)
					continue

				start_position = (_child["x"], _child["y"])
				start_size = (_child["width"], _child["height"]) if 'width' in _child else (self.script_data['width'], self.script_data['height'])
				new_position = (start_position[0] * new_parent_width / start_size[0], start_position[1] * new_parent_height / start_size[1])
				#new_position = (max(self.sizeable['min_width'], new_position[0]), max(self.sizeable['min_height'], new_position[1]))
				child.SetPosition(new_position[0], new_position[1])
				child.SetFocus()

	def OnUpdate(self):
		self.script_data = self.__dict__['script_data']
		
		if self.sizeable['enabled']:

			xMouse, yMouse = GetMousePosition()
			x, y = self.GetGlobalPosition()

			if xMouse > x + self.size[0] - 55 \
					and yMouse > y + self.size[1] - 55:

				# set alpha of border texture to 0.5

				if IsPressed(DIK_LSHIFT):

					if self.pos_move_original == None:
						self.pos_move_original = (x, y)
					
					# Create the scaling border on beginning of resize
					if self.scaling_border == None:
						self.scaling_border = ui.Bar()
						self.scaling_border.SetColor(globals.BASE_THEME_SCALE_BORDER_COLOR)

					# Update the scaling border
					self.scaling_border.SetPosition(self.pos_move_original[0] + 5, self.pos_move_original[1] + 25)
					self.scaling_border.SetSize(self.size[0] - 10, self.size[1] - 35)
					self.scaling_border.SetFocus()
					if self.scaling_border.IsShow() == False:
						self.scaling_border.Show()

					# Create the scaling info on beginning of resize
					if self.scaling_info == None:
						self.scaling_info = ui.TextLine()
						self.scaling_info.SetFontColor(globals.BASE_THEME_SCALE_INFO_COLOR_RGBA[0], globals.BASE_THEME_SCALE_INFO_COLOR_RGBA[1], globals.BASE_THEME_SCALE_INFO_COLOR_RGBA[2])
						self.scaling_info.SetOutline()

					# Update the scaling info
					self.scaling_info.SetText("width:%d height:%d" % (self.size[0], self.size[1]))
					self.scaling_info.SetPosition(self.pos_move_original[0] + 5, self.pos_move_original[1] + self.size[1])
					if self.scaling_info.IsShow() == False:
						self.scaling_info.Show()

					self.is_resizing = True

					self.update_size(xMouse - x, yMouse - y)
					self.update_children_pos_relative(self.Children, self.size[0], self.size[1] - 55)
					self.SetPosition(self.pos_move_original[0], self.pos_move_original[1])
					return True

			# Destroy the scaling border
			if self.scaling_border != None:
				self.scaling_border.Hide()
				self.scaling_border.Destroy()
				self.scaling_border = None
				self.OnMouseLeftButtonDown = self._OnMouseLeftButtonDown

			# Destroy the scaling info
			if self.scaling_info != None:
				self.scaling_info.Hide()
				self.scaling_info.Destroy()
				self.scaling_info = None

			self.is_resizing 		= False
			self.pos_move_original 	= None
		# End of sizeable



	def __del__(self):
		ui.ScriptWindow.__del__(self)