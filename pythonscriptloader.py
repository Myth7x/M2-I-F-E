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

		self.LoadChildren(_object, _data)
		
		_object.__dict__['script_data'] = _data
		_object.__dict__['parent'] 		= parent 

		_object.Show()

		return _object


