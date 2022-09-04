import sys

# CPython Modules
import ui

# Our Modules
from proto_utils import LogTxt

from .ifmgr_ui.board import Board_Custom

# Extend the ui.PythonScriptLoader class to add our own custom shit
class PythonScriptLoader(ui.PythonScriptLoader):
	def __init__(self):
		ui.PythonScriptLoader.__init__(self)

	def load_children(self, parent, dicChildren):

		if True == dicChildren.has_key("style"):
			for style in dicChildren["style"]:
				parent.AddFlag(style)

		if False == dicChildren.has_key("children"):
			return False

		Index = 0

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

			if FALSE == self.CheckKeyList(Name, ElementValue, self.DEFAULT_KEY_LIST):
				del parent.Children[Index]
				continue

			if Type == "window":
				parent.Children[Index] = ui.ScriptWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementWindow(parent.Children[Index], ElementValue, parent)

			elif Type == "button":
				parent.Children[Index] = ui.Button()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "radio_button":
				parent.Children[Index] = ui.RadioButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "toggle_button":
				parent.Children[Index] = ui.ToggleButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "mark":
				parent.Children[Index] = ui.MarkBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementMark(parent.Children[Index], ElementValue, parent)

			elif Type == "image":
				parent.Children[Index] = ui.ImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementImage(parent.Children[Index], ElementValue, parent)

			elif Type == "expanded_image":
				parent.Children[Index] = ui.ExpandedImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementExpandedImage(parent.Children[Index], ElementValue, parent)

			elif Type == "ani_image":
				parent.Children[Index] = ui.AniImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementAniImage(parent.Children[Index], ElementValue, parent)

			elif Type == "slot":
				parent.Children[Index] = ui.SlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlot(parent.Children[Index], ElementValue, parent)

			elif Type == "candidate_list":
				parent.Children[Index] = ui.CandidateListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCandidateList(parent.Children[Index], ElementValue, parent)

			elif Type == "grid_table":
				parent.Children[Index] = ui.GridSlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGridTable(parent.Children[Index], ElementValue, parent)

			elif Type == "text":
				parent.Children[Index] = ui.TextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementText(parent.Children[Index], ElementValue, parent)

			elif Type == "editline":
				parent.Children[Index] = ui.EditLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditLine(parent.Children[Index], ElementValue, parent)

			elif Type == "titlebar":
				parent.Children[Index] = ui.TitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "horizontalbar":
				parent.Children[Index] = ui.HorizontalBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementHorizontalBar(parent.Children[Index], ElementValue, parent)

			elif Type == "board":
				parent.Children[Index] = ui.Board()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "board_with_titlebar":
				parent.Children[Index] = ui.BoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard":
				parent.Children[Index] = ui.ThinBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)
				
			elif Type == "thinboard_gold":
				parent.Children[Index] = ui.ThinBoardGold()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_circle":
				parent.Children[Index] = ui.ThinBoardCircle()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_gold":
				parent.Children[Index] = ui.ThinBoardGold()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoardGold(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_circle":
				parent.Children[Index] = ui.ThinBoardCircle()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoardCircle(parent.Children[Index], ElementValue, parent)

			elif Type == "box":
				parent.Children[Index] = ui.Box()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBox(parent.Children[Index], ElementValue, parent)

			elif Type == "bar":
				parent.Children[Index] = ui.Bar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBar(parent.Children[Index], ElementValue, parent)

			elif Type == "line":
				parent.Children[Index] = ui.Line()
				parent.Children[Index].SetParent(parent)
				self.LoadElementLine(parent.Children[Index], ElementValue, parent)

			elif Type == "slotbar":
				parent.Children[Index] = ui.SlotBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlotBar(parent.Children[Index], ElementValue, parent)

			elif Type == "gauge":
				parent.Children[Index] = ui.Gauge()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGauge(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar":
				parent.Children[Index] = ui.ScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thin_scrollbar":
				parent.Children[Index] = ui.ThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "small_thin_scrollbar":
				parent.Children[Index] = ui.SmallThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "sliderbar":
				parent.Children[Index] = ui.SliderBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSliderBar(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox":
				parent.Children[Index] = ui.ListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox2":
				parent.Children[Index] = ui.ListBox2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox2(parent.Children[Index], ElementValue, parent)
			elif Type == "listboxex":
				parent.Children[Index] = ui.ListBoxEx()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBoxEx(parent.Children[Index], ElementValue, parent)
			elif Type == "listbox_scroll":
				parent.Children[Index] = ui.ListBoxScroll()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)

			else:
				Index += 1
				continue

			parent.Children[Index].SetWindowName(Name)
			if 0 != self.InsertFunction:
				self.InsertFunction(Name, parent.Children[Index])

			self.load_children(parent.Children[Index], ElementValue)
			Index += 1

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
			if 'instructions' in _data:
				_object.set_instruction_data(_data['instructions'])
		else:
			_object.SetParent(parent)
		
		if "style" in _data:
			for StyleList in _data["style"]:
				_object.AddFlag(StyleList)


		_object.SetPosition(int(_data["x"]), int(_data["y"]))
		_object.SetSize(int(_data["width"]), int(_data["height"]))

		if "style" in _data:
			for StyleList in _data["style"]:
				_object.AddFlag(StyleList)

		self.load_children(_object, _data)
		
		_object.__dict__['script_data'] = _data
		_object.__dict__['parent'] 		= parent 

		_object.Show()

		return _object


