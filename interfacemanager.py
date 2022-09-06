# UI Builder by myth, b1g speed in ya nose
# IfMgr : Interface Manager

NAME = "Interface Manager"
VERSION = '0.5-Rev.Pepp'
UI_CLASS_EXPORT = {
	'enabled' 	: True,
	'path' 		: 'C:\\Proto_InterfaceManager\\%s_ui_classes.csv',
}
###############################################################################
import datetime

# Interface Manager Modules
import ifmgr_ui
from ui_class_gathering import UI_Classes
from proto_utils import LogTxt
import n_object_browser
import n_scene_browser
import globals

# Python Modules
import constinfo
# CPython Modules
import ui, wndMgr

###############################################################################


# Main Interface Manager Class
class InterfaceManager(ui.BoardWithTitleBar):

	def __init__(self, width, height):
		self.current_scene = None
		LogTxt(__name__, "Initializing..")

		ui.BoardWithTitleBar.__init__(self)

		self.WINDOW_SIZE = [width, height]

		LogTxt(__name__, "Looking for UI Classes..")

		globals.UI_CLASS_DATA = UI_Classes()._LoadUI()
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

		if self.build_window() == False:
			LogTxt(__name__, "Failed to build window!")
			return False
		self.Show()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	# To Reset Focus on Inputs
	def OnMouseLeftButtonDown(self):
		self.SetFocus()

	def create_scene(self, name):
		self.current_scene = name
		self.obj_browser = n_object_browser.n_object_browser()
		self.obj_browser.object.SetWindowName("n_object_browser")
		self.obj_browser.set_parent(self)
		
		self.scene_browser = n_scene_browser.n_scene_browser()
		self.scene_browser.object.SetWindowName("n_scene_browser")
		self.scene_browser.set_parent(self)
		self.scene_browser.set_scene_name(self.current_scene)

	def request_create_scene(self):
		self.input_dialog = ifmgr_ui.InputDialog()
		self.input_dialog.set_title("New Scene")
		self.input_dialog.set_input_desc("Scene Name:")
		self.input_dialog.set_input("")
		self.input_dialog.set_callback(ui.__mem_func__(self.create_scene))
		self.input_dialog.Show()

	def build_window(self):
		self.SetTitleName(NAME)
		self.SetSize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
		self.SetPosition(wndMgr.GetScreenWidth() / 2 - self.WINDOW_SIZE[0] / 2, 20)
		self.AddFlag("movable")

		# Info Text
		self.information = ui.TextLine()
		self.information.SetText("<Version:%s> <UI_Classes:%d>" % (VERSION, len(self.ui)))
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

		## New Attribute Editor
		#import n_attribute_editor
#
		#self.attr_editor = n_attribute_editor.n_attribute_editor()
		#self.attr_editor.object.SetWindowName("n_attribute_editor")
		#self.attr_editor.set_parent(self)
		#self.attr_editor.set_ui_data(self.ui)
		################################################################################
#
		#try:
		#	# Child Config
		#	self.child_config = ChildConfig(self.WINDOW_SIZE[0] - 20, 205, globals.BASE_THEME_COLOR, self.ui)
		#	self.child_config.SetParent(self)
		#	self.child_config.SetPosition(10, 280)
		#	self.child_config.Show()
		#	###############################################################################
		#except:
		#	LogTxt(__name__, "Failed to build Child Config!")
		#	return False

		LogTxt(__name__, "Initialized!")
		return True

	# Add Object to current project by name
	def OnAddObject(self):
		self.scene_browser.add_scene_object(self.obj_browser.get_selected_object())

	# Remove Object from current project by name
	def OnRemoveObject(self):
		pass
		#self.scene_browser.remove_scene_object(self.obj_browser.get_selected_object())
		
		#self.project_browser.remove_child(self.project_browser.selected_child_name())
		#self.project_browser.filter.filter_editline.SetText("")
		#LogTxt(__name__, "Removed %s from Project Browser" % self.project_browser.selected_child_name())

	# Abusing this loop to update
	def OnRender(self):
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.information.SetText("<Version:%s> <UI_Classes:%d> <Mouse:%d,%d>" % (VERSION, len(self.ui), xMouse, yMouse))

		if self.current_scene != None:
			self.new_scene_button.Hide()
		#child = self.scene_browser.get_selected_children()
		#if child:
		#	if self.child_config.selected_child_in_project != child['object_name']:
		#		self.child_config.update(child['child_name'], child['object_name'])


def setup_ifmgr(parent):
	if constinfo.INTERFACE_MANAGER_INITIALIZED == True:
		LogTxt(__name__, "Interface Manager is already initialized!")
		return None

	try:
		ifmgr = InterfaceManager(350, 100)

		constinfo.INTERFACE_MANAGER_INITIALIZED = True

		return ifmgr
	except:
		LogTxt(__name__, "Failed to initialize!")
		return None

############################################################################################################

