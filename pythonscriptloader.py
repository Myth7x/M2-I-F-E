# Python: 2.7.3 sadge sadge
############################

import sys, os

# CPython Modules
import ui, chr, player, app

# Our Modules
from proto_utils import LogTxt

from .ifmgr_ui.board import IfMgr_Board

# Extend the ui.PythonScriptLoader class to add our own custom shit
class PythonScriptLoader(ui.PythonScriptLoader):
	def __init__(self):
		ui.PythonScriptLoader.__init__(self)

	def prepare_script_data(self, script_data):
		# Prepare the script data
		for child in script_data['children']:
			child['script_data'] = script_data


	def load_script(self, parent, path, script):
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
		except:
			LogTxt("PythonScriptLoader", "Failed to load script: %s" % (script))
			return None

		if _class == ui.ScriptWindow:
			# Clears Children list data and ElementDictionary dict data
			_object.ClearDictionary()
		elif _class == IfMgr_Board:
			# Clears Children list data and ElementDictionary dict data
			_object.ClearDictionary()
			# Set attributes for our board
			_object.add_custom_flag(_data['customFlag'])
		
		if "style" in _data:
			for StyleList in _data["style"]:
				LogTxt("PythonScriptLoader", "Adding StyleList: %s %s" % (_data, StyleList))
				_object.AddFlag(StyleList)

		_object.SetPosition(int(_data["x"]), int(_data["y"]))
		_object.SetSize(int(_data["width"]), int(_data["height"]))

		if "style" in _data:
			for StyleList in _data["style"]:
				_object.AddFlag(StyleList)

		self.LoadChildren(_object, _data)
		
		_object.__dict__['script_data'] = _data
		self.prepare_script_data(_data)

		_object.Show()

		return _object


