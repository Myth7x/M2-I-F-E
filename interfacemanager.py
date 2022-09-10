# UI Builder by myth, b1g speed in ya nose
# IfMgr : Interface Manager

NAME = "Interface Manager"
VERSION = '0.5-Rev.Pepp'
UI_CLASS_EXPORT = {
	'enabled' 	: False,
	'path' 		: 'C:\\Proto_InterfaceManager\\%s_ui_classes.csv',
}
###############################################################################
import datetime
import grp

# Interface Manager Modules
from ui_class_gathering import UI_Classes
from proto_utils import LogTxt
import ifmgr_ui, n_object_browser, n_scene_browser, n_scene_demo_re

# Python Modules
import constinfo
# CPython Modules
import ui, wndMgr, app

###############################################################################

import globals

import ifmgr_ui

# Main Interface Manager Class
class InterfaceManager(ui.BoardWithTitleBar):

	def __init__(self, width, height):
		self.current_scene 	= None
		self.yesno_dialog 	= None
		self.obj_browser 	= None
		self.scene_browser 	= None
		self.scene_demo 	= None
		LogTxt(__name__, "Initializing..")

		ui.BoardWithTitleBar.__init__(self)

		self.WINDOW_SIZE = [width, height]

		LogTxt(__name__, "Looking for UI Classes..")
		self.ui = UI_Classes()
		globals.UI_CLASS_DATA = self.ui.load_ui_data()
		LogTxt(__name__, "Found %d UI Classes!" % len(globals.UI_CLASS_DATA))

		if UI_CLASS_EXPORT['enabled']:
			ui_class_export = [["Class,Base,Function,Arguments"]]
			for ui_class in globals.UI_CLASS_DATA:
				ui_class_export.append(['%s,,' % (ui_class)])
				for ui_class_attr in self.ui[ui_class][3]:
					ui_class_export.append(['%s,%s,%s,%s' % (ui_class, self.ui[ui_class][2], ui_class_attr, self.ui[ui_class][3][ui_class_attr])])
			target_file = UI_CLASS_EXPORT['path'] % (datetime.datetime.now().strftime('%Y-%m-%d'))
			with open(target_file, "w") as f:
				for row in ui_class_export:
					f.write(",".join(row) + "\n")
				f.close()
			LogTxt(__name__, "Exported UI Classes to %s" % target_file)

		if self.build_window() != True:
			LogTxt(__name__, "Failed to build window!")
			return False
		
		constinfo.INTERFACE_MANAGER_INITIALIZED = True
		self.Show()

		## test
		#self.test_selectbox = ifmgr_ui.SelectBox()
		#self.test_selectbox.SetParent(self)
		#self.test_selectbox.SetPosition(140, 30)
		#self.test_selectbox.SetSize(200, 100)
		#self.test_selectbox.SetWidth(200)
		#self.test_selectbox.Show()

		return self



	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	# To Reset Focus on Inputs
	def OnMouseLeftButtonDown(self):
		self.SetFocus()

	def on_demo_select_object(self, object_name):
		object_list_index = 0
		for object in self.scene_browser.ref_object_list.textDict:
			if self.scene_browser.ref_object_list.textDict[object] == object_name:
				object_list_index = object
				break

		self.scene_browser.ref_object_list.SelectItem(object_list_index)

	def create_scene(self, name):
		self.current_scene = name

		try:
			self.scene_demo = n_scene_demo_re.n_scene_demo_re()
		except Exception as e:
			LogTxt(__name__, "Failed to load n_scene_demo_re %s" % e)
			self.scene_demo = None

		self.obj_browser = n_object_browser.n_object_browser()
		self.obj_browser.object.SetWindowName("n_object_browser")
		self.obj_browser.set_parent(self)
		
		self.scene_browser = n_scene_browser.n_scene_browser()
		self.scene_browser.object.SetWindowName("n_scene_browser")
		self.scene_browser.set_parent(self)
		self.scene_browser.set_scene_name(self.current_scene)

		self.refresh_scene_demo()

	def refresh_scene_demo(self):
		self.scene_demo.set_scene_data(self.current_scene, self.scene_browser.get_scene_data())

	def add_scene_object_data(self, object_name, object_data):
		self.scene_demo.add_scene_object_data(object_name, object_data)

	def request_create_scene(self):
		self.input_dialog = ifmgr_ui.InputDialog()
		self.input_dialog.set_title("New Scene Name")
		self.input_dialog.set_input_desc("Scene Name:")
		self.input_dialog.set_input("New Scene")
		self.input_dialog.set_callback(ui.__mem_func__(self.create_scene))
		self.input_dialog.Show()

	def create_yesno_dialog(self, title, desc, callback):
		self.yesno_dialog = ifmgr_ui.YesNoDialog()
		self.yesno_dialog.set_title(title)
		self.yesno_dialog.set_desc(desc)
		self.yesno_dialog.set_callback(callback)
		self.yesno_dialog.Show()

	def test_callback_yesno(self, result):
		LogTxt(__name__, "YesNoDialog Callback: %s" % result)

	def build_window(self):
		self.SetTitleName(NAME)
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
		self.new_scene_button.SetPosition(10, 50)
		self.new_scene_button.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.new_scene_button.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.new_scene_button.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.new_scene_button.SetText("New Scene")
		self.new_scene_button.SetEvent(ui.__mem_func__(self.request_create_scene))
		self.new_scene_button.Show()
		###############################################################################

		# Refresh Scene Button
		self.refresh_scene_button = ui.Button()
		self.refresh_scene_button.SetParent(self)
		self.refresh_scene_button.SetPosition(10, 80)
		self.refresh_scene_button.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.refresh_scene_button.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.refresh_scene_button.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.refresh_scene_button.SetText("Refresh Scene")
		self.refresh_scene_button.SetEvent(ui.__mem_func__(self.refresh_scene_demo))
		self.refresh_scene_button.Show()

		LogTxt(__name__, "Initialized!")
		return True


	# Abusing this loop to update
	def OnRender(self):
		if self.obj_browser != None:
			xMouse, yMouse = wndMgr.GetMousePosition()
			self.information.SetText("<Version:%s> <UI_Classes:%d> <Mouse:%d,%d>" % (VERSION, self.obj_browser.ref_object_list.GetItemCount(), xMouse, yMouse))
			if self.current_scene != None:
				self.new_scene_button.Hide()
		if app.IsPressed(app.DIK_LALT):
			wndMgr.SetOutlineFlag(True)
		else:
			wndMgr.SetOutlineFlag(False)

def setup_ifmgr(parent):
	if constinfo.INTERFACE_MANAGER_INITIALIZED == True:
		LogTxt(__name__, "Interface Manager is already initialized!")
		return None

	try:
		return InterfaceManager(350, 300)
	except:
		LogTxt(__name__, "Failed to initialize!")
		return None

############################################################################################################

