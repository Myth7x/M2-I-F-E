###############################################################################
import datetime, sys, os

# Interface Manager Modules
from _utils import LogTxt, ui_class_gathering
import ifmgr_ui, globals, object_browser, scene_browser, scene_demo

# Python Modules
import constinfo
# CPython Modules
import ui, wndMgr, app
###############################################################################

class InterfaceManager(ui.BoardWithTitleBar):
	"""interface manager class
	- main program module, handles create/load/save/delete of scenes
	"""
	current_scene 	= None
	yesno_dialog 	= None
	obj_browser 	= None
	scene_browser 	= None
	scene_demo 		= None

	def __init__(self, width, height):
		LogTxt(__name__, "Initializing..")

		ui.BoardWithTitleBar.__init__(self)

		self.WINDOW_SIZE = [width, height]

		LogTxt(__name__, "Looking for UI Modules..")
		self.ui = ui_class_gathering.UI_Classes()
		globals.UI_CLASS_DATA = self.ui.load_ui_data()
		LogTxt(__name__, "Found %d possible UI Modules!" % len(globals.UI_CLASS_DATA))

		if globals.UI_CLASS_EXPORT['enabled']:
			self.export_raw_ui_data()

		if self.build_window() != True:
			LogTxt(__name__, "Failed to build window!")
			return False

		constinfo.INTERFACE_MANAGER_INITIALIZED = True
		self.Show()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)



	def OnMouseLeftButtonDown(self):
		"""Overridden to reset focus on inputs"""
		self.SetFocus()

	def OnRender(self):
		"""Overridden to update the program"""
		if self.obj_browser != None:
			self.information.SetText("<Version:%s>" % globals.VERSION)
			if self.current_scene != None:
				self.new_scene_button.Hide()
		
		if app.IsPressed(app.DIK_LALT):
			wndMgr.SetOutlineFlag(True)
		else:
			wndMgr.SetOutlineFlag(False)
		
		if self.scene_demo:
			self.scene_demo.parent = self
			self.scene_demo.update()

	def build_window(self):
		"""Builds the interface manager window"""
		self.SetTitleName(globals.NAME)
		self.SetSize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
		self.SetPosition(wndMgr.GetScreenWidth() / 2 - self.WINDOW_SIZE[0] / 2, 20)
		self.AddFlag("movable")

		# Info Text
		self.information = ui.TextLine()
		self.information.SetParent(self)
		self.information.SetPosition(10, 30)
		self.information.Show()
		###############################################################################

		# New Scene Button
		self.new_scene_button = ui.Button()
		self.new_scene_button.SetParent(self)
		self.new_scene_button.SetPosition(10, 45)
		self.new_scene_button.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.new_scene_button.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.new_scene_button.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.new_scene_button.SetText("New Scene")
		self.new_scene_button.SetEvent(ui.__mem_func__(self.create_scene_ask_name))
		self.new_scene_button.Show()
		###############################################################################

		# Refresh Scene Button
		self.refresh_scene_button = ui.Button()
		self.refresh_scene_button.SetParent(self)
		self.refresh_scene_button.SetPosition(120, 45)
		self.refresh_scene_button.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.refresh_scene_button.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.refresh_scene_button.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.refresh_scene_button.SetText("Refresh Scene")
		self.refresh_scene_button.SetEvent(ui.__mem_func__(self.forward_scene_demo_refresh))
		self.refresh_scene_button.Show()

		# Exit Game
		self.cloase_game_button = ui.Button()
		self.cloase_game_button.SetParent(self)
		self.cloase_game_button.SetPosition(10, 70)
		self.cloase_game_button.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
		self.cloase_game_button.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
		self.cloase_game_button.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
		self.cloase_game_button.SetText("Close Game")
		self.cloase_game_button.SetEvent(ui.__mem_func__(self.close_game))
		self.cloase_game_button.Show()

		# Restart Game
		self.restart_game_button = ui.Button()
		self.restart_game_button.SetParent(self)
		self.restart_game_button.SetPosition(120, 70)
		self.restart_game_button.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
		self.restart_game_button.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
		self.restart_game_button.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
		self.restart_game_button.SetText("Restart Game")
		self.restart_game_button.SetEvent(ui.__mem_func__(self.restart_game))
		self.restart_game_button.Show()

		LogTxt(__name__, "Initialized!")
		return True

	def create_scene(self, name):
		"""Creates a new scene"""
		self.current_scene = name if not globals.INFO_INPUT_SCENE_NAME in name else 'New Scene'

		self.scene_demo = scene_demo.scene_demo()

		self.obj_browser = object_browser.object_browser()
		self.obj_browser.object.SetWindowName("object_browser")
		self.obj_browser.set_parent(self)
		
		self.scene_browser = scene_browser.scene_browser()
		self.scene_browser.object.SetWindowName("scene_browser")
		self.scene_browser.set_parent(self)
		self.scene_browser.set_scene_name(self.current_scene)

		self.input_dialog.Close()
		self.input_dialog = None

	def update_scene_object_data(self, data):
		self.scene_browser.update_scene_object_data(data)

	def on_demo_select_object(self, object_name):
		"""Called when an object is selected in the object browser
		- object_name: name of the selected object/name of the selected ui class"""
		object_list_index = 0
		for object in self.scene_browser.ref_object_list.textDict:
			if self.scene_browser.ref_object_list.textDict[object] == object_name:
				object_list_index = object
				break

		self.scene_browser.ref_object_list.SelectItem(object_list_index)

	def create_scene_ask_name(self):
		"""Asks for a name for the new scene on submit, creates the scene"""
		self.input_dialog = ifmgr_ui.InputDialog()
		self.input_dialog.set_size(500, 100)
		self.input_dialog.set_title("New Scene Name")
		self.input_dialog.set_input_desc("Scene Name:")
		self.input_dialog.set_input("New Scene  %s" % globals.INFO_INPUT_SCENE_NAME)
		self.input_dialog.set_callback(ui.__mem_func__(self.create_scene))
		self.input_dialog.Show()

	def restart_game(self):
		"""Restarts the game, useful if the m2 environment is broken"""
		self.close_game()
		os.system("start %s" % sys.executable)

	def close_game(self):
		"""Closes the game, also useful if the m2 environment is broken"""
		app.Exit()

	def forward_scene_demo_refresh(self):
		"""Forwards the refresh call to the scene demo"""
		self.scene_demo.set_scene_data(self.current_scene, self.scene_browser.scene)

	def add_scene_object_data(self, object_name, object_data):
		"""Copies the scene project object data from our scene browser to the scene demo"""
		self.scene_demo.add_scene_object_data(object_name, object_data)
		self.scene_browser.add_scene_object(object_name, object_data)

	def export_raw_ui_data(self):
		"""Exports the scraped raw ui data to a csv file"""
		ui_class_export = [["Class,Base,Function,Arguments"]]
		for ui_class in globals.UI_CLASS_DATA:
			ui_class_export.append(['%s,,' % (ui_class)])
			for ui_class_attr in self.ui[ui_class][3]:
				ui_class_export.append(['%s,%s,%s,%s' % (ui_class, self.ui[ui_class][2], ui_class_attr, self.ui[ui_class][3][ui_class_attr])])
		target_file = globals.UI_CLASS_EXPORT['path'] % (datetime.datetime.now().strftime('%Y-%m-%d'))
		with open(target_file, "w") as f:
			for row in ui_class_export:
				f.write(",".join(row) + "\n")
			f.close()
		LogTxt(__name__, "Exported UI Classes to %s" % target_file)


