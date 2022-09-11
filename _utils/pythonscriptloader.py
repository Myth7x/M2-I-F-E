import sys

# CPython Modules
import ui

# Our Modules
from _utils import LogTxt

from ..ifmgr_ui.board import Board_Custom
from ..ifmgr_ui.listboxscroll import ListBoxScroll

# Extend the ui.PythonScriptLoader class to add our own custom shit
class PythonScriptLoader(ui.PythonScriptLoader):
	def __init__(self):
		ui.PythonScriptLoader.__init__(self)

	def load_children(self, parent, dicChildren):

		if 'style' in dicChildren:
			for style in dicChildren["style"]:
				parent.AddFlag(style)

		if 'children' not in dicChildren:
			return False

		c = 0

		ChildrenList = dicChildren["children"]
		parent.Children = range(len(ChildrenList))
		for ElementValue in ChildrenList:
			try:
				Name = ElementValue["name"]				
			except KeyError:
				Name = ElementValue["name"] = "NONAME"
				
			try:
				Type = ElementValue["type"]
			except KeyError:								
				Type = ElementValue["type"] = "window"				

			if False == self.CheckKeyList(Name, ElementValue, self.DEFAULT_KEY_LIST):
				del parent.Children[c]
				continue

			if Type == "window":
				parent.Children[c] = ui.ScriptWindow()
				parent.Children[c].SetParent(parent)
				self.LoadElementWindow(parent.Children[c], ElementValue, parent)

			elif Type == "button":
				parent.Children[c] = ui.Button()
				parent.Children[c].SetParent(parent)
				self.LoadElementButton(parent.Children[c], ElementValue, parent)

			elif Type == "radio_button":
				parent.Children[c] = ui.RadioButton()
				parent.Children[c].SetParent(parent)
				self.LoadElementButton(parent.Children[c], ElementValue, parent)

			elif Type == "toggle_button":
				parent.Children[c] = ui.ToggleButton()
				parent.Children[c].SetParent(parent)
				self.LoadElementButton(parent.Children[c], ElementValue, parent)

			elif Type == "mark":
				parent.Children[c] = ui.MarkBox()
				parent.Children[c].SetParent(parent)
				self.LoadElementMark(parent.Children[c], ElementValue, parent)

			elif Type == "image":
				parent.Children[c] = ui.ImageBox()
				parent.Children[c].SetParent(parent)
				self.LoadElementImage(parent.Children[c], ElementValue, parent)

			elif Type == "expanded_image":
				parent.Children[c] = ui.ExpandedImageBox()
				parent.Children[c].SetParent(parent)
				self.LoadElementExpandedImage(parent.Children[c], ElementValue, parent)

			elif Type == "ani_image":
				parent.Children[c] = ui.AniImageBox()
				parent.Children[c].SetParent(parent)
				self.LoadElementAniImage(parent.Children[c], ElementValue, parent)

			elif Type == "slot":
				parent.Children[c] = ui.SlotWindow()
				parent.Children[c].SetParent(parent)
				self.LoadElementSlot(parent.Children[c], ElementValue, parent)

			elif Type == "candidate_list":
				parent.Children[c] = ui.CandidateListBox()
				parent.Children[c].SetParent(parent)
				self.LoadElementCandidateList(parent.Children[c], ElementValue, parent)

			elif Type == "grid_table":
				parent.Children[c] = ui.GridSlotWindow()
				parent.Children[c].SetParent(parent)
				self.LoadElementGridTable(parent.Children[c], ElementValue, parent)

			elif Type == "text":
				parent.Children[c] = ui.TextLine()
				parent.Children[c].SetParent(parent)
				self.LoadElementText(parent.Children[c], ElementValue, parent)

			elif Type == "editline":
				parent.Children[c] = ui.EditLine()
				parent.Children[c].SetParent(parent)
				self.LoadElementEditLine(parent.Children[c], ElementValue, parent)

			elif Type == "titlebar":
				parent.Children[c] = ui.TitleBar()
				parent.Children[c].SetParent(parent)
				self.LoadElementTitleBar(parent.Children[c], ElementValue, parent)

			elif Type == "horizontalbar":
				parent.Children[c] = ui.HorizontalBar()
				parent.Children[c].SetParent(parent)
				self.LoadElementHorizontalBar(parent.Children[c], ElementValue, parent)

			elif Type == "board":
				parent.Children[c] = ui.Board()
				parent.Children[c].SetParent(parent)
				self.LoadElementBoard(parent.Children[c], ElementValue, parent)

			elif Type == "board_with_titlebar":
				parent.Children[c] = ui.BoardWithTitleBar()
				parent.Children[c].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[c], ElementValue, parent)

			elif Type == "thinboard":
				parent.Children[c] = ui.ThinBoard()
				parent.Children[c].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[c], ElementValue, parent)
				
			elif Type == "thinboard_gold":
				parent.Children[c] = ui.ThinBoardGold()
				parent.Children[c].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[c], ElementValue, parent)

			elif Type == "thinboard_circle":
				parent.Children[c] = ui.ThinBoardCircle()
				parent.Children[c].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[c], ElementValue, parent)

			elif Type == "thinboard_gold":
				parent.Children[c] = ui.ThinBoardGold()
				parent.Children[c].SetParent(parent)
				self.LoadElementThinBoardGold(parent.Children[c], ElementValue, parent)

			elif Type == "thinboard_circle":
				parent.Children[c] = ui.ThinBoardCircle()
				parent.Children[c].SetParent(parent)
				self.LoadElementThinBoardCircle(parent.Children[c], ElementValue, parent)

			elif Type == "box":
				parent.Children[c] = ui.Box()
				parent.Children[c].SetParent(parent)
				self.LoadElementBox(parent.Children[c], ElementValue, parent)

			elif Type == "bar":
				parent.Children[c] = ui.Bar()
				parent.Children[c].SetParent(parent)
				self.LoadElementBar(parent.Children[c], ElementValue, parent)

			elif Type == "line":
				parent.Children[c] = ui.Line()
				parent.Children[c].SetParent(parent)
				self.LoadElementLine(parent.Children[c], ElementValue, parent)

			elif Type == "slotbar":
				parent.Children[c] = ui.SlotBar()
				parent.Children[c].SetParent(parent)
				self.LoadElementSlotBar(parent.Children[c], ElementValue, parent)

			elif Type == "gauge":
				parent.Children[c] = ui.Gauge()
				parent.Children[c].SetParent(parent)
				self.LoadElementGauge(parent.Children[c], ElementValue, parent)

			elif Type == "scrollbar":
				parent.Children[c] = ui.ScrollBar()
				parent.Children[c].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[c], ElementValue, parent)

			elif Type == "thin_scrollbar":
				parent.Children[c] = ui.ThinScrollBar()
				parent.Children[c].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[c], ElementValue, parent)

			elif Type == "small_thin_scrollbar":
				parent.Children[c] = ui.SmallThinScrollBar()
				parent.Children[c].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[c], ElementValue, parent)

			elif Type == "sliderbar":
				parent.Children[c] = ui.SliderBar()
				parent.Children[c].SetParent(parent)
				self.LoadElementSliderBar(parent.Children[c], ElementValue, parent)

			elif Type == "listbox":
				parent.Children[c] = ui.ListBox()
				parent.Children[c].SetParent(parent)
				self.LoadElementListBox(parent.Children[c], ElementValue, parent)

			elif Type == "listbox2":
				parent.Children[c] = ui.ListBox2()
				parent.Children[c].SetParent(parent)
				self.LoadElementListBox2(parent.Children[c], ElementValue, parent)
			elif Type == "listboxex":
				parent.Children[c] = ui.ListBoxEx()
				parent.Children[c].SetParent(parent)
				self.LoadElementListBoxEx(parent.Children[c], ElementValue, parent)
			elif Type == "listbox_scroll":
				parent.Children[c] = ListBoxScroll()
				parent.Children[c].SetParent(parent)
				self.LoadElementListBox(parent.Children[c], ElementValue, parent)
			elif Type == "combo_box":
				parent.Children[c] = ui.ComboBox()
				parent.Children[c].SetParent(parent)
				_ = self.load_element_combobox(parent.Children[c], ElementValue, parent)
			else:
				c += 1
				continue

			parent.Children[c].SetWindowName(Name)
			if self.InsertFunction:
				self.InsertFunction(Name, parent.Children[c])

			self.load_children(parent.Children[c], ElementValue)
			c += 1

	def load_element_combobox(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		if value.has_key("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	def load_script(self, parent, path, script):
		LogTxt(__name__, "Loading script: %s" % script)
		
		# Clears ScriptDictionary dict data and InsertFunction
		self.Clear()

		# Set the path to the script cuz we dont load from virtual file system
		sys.path.append(path)

		try:
			# Load the script
			_module = __import__(script.replace(".py", ""))
			# Get the object class from the script
			_class = getattr(_module, "_class")
			# Get the object data from the script
			_data = getattr(_module, "object")
			# Create the object
			_object = _class()
		except IOError, e:
			LogTxt(__name__, "Error: %s" % e)
			return None
		except RuntimeError, e:
			LogTxt(__name__, "Failed to load script: %s" % script)
			LogTxt(__name__, "Error: %s" % e)
			return None
		except:
			LogTxt(__name__, "Failed to load script: %s" % (script))
			return None

		if _class == ui.ScriptWindow:
			# Clears Children list data and ElementDictionary dict data
			_object.ClearDictionary()
		elif _class == Board_Custom:
			# Clears Children list data and ElementDictionary dict data
			_object.ClearDictionary()
			# Set attributes for our board
			_object.set_sizeable_data(_data['sizeable'])
			# Set instruction data
			if hasattr(_data, 'instructions'):
				_object.set_instruction_data(_data['instructions'])
		else:
			_object.SetParent(parent)
		
		_object.SetPosition(int(_data["x"]), int(_data["y"]))
		_object.SetSize(int(_data["width"]), int(_data["height"]))

		if hasattr(_data, 'style'):
			for style in _data["style"]:
				_object.AddFlag(style)

		self.load_children(_object, _data)
		
		_object.__dict__['script_data'] = _data
		_object.__dict__['parent'] 		= parent 

		_object.Show()

		return _object


