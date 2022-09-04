# UI Builder by myth, b1g speed in ya nose
# IfMgr : Interface Manager

NAME = "Interface Manager"
VERSION = '0.1-Rev.Pepp'
UI_CLASS_EXPORT = {
	'enabled' 	: True,
	'path' 		: 'C:\\Proto_InterfaceManager\\%s_ui_classes.csv',
}
RGB_MODE = True

###############################################################################
import sys
import datetime
from listboxscroll import ListBoxScroll

# Interface Manager Modules
from ui_class_gathering import UI_Classes
from proto_utils import LogTxt
from object_browser import ObjectBrowser
from project_browser import ProjectBrowser
from child_config import ChildConfig

import globals

# Python Modules
import constinfo
# CPython Modules
import ui, wndMgr

###############################################################################


# Main Interface Manager Class
class InterfaceManager(ui.BoardWithTitleBar):

	def __init__(self, width, height):
		LogTxt(__name__, "Initializing..")

		ui.BoardWithTitleBar.__init__(self)

		self.WINDOW_SIZE = [width, height]

		LogTxt(__name__, "Looking for UI Classes..")

		self.ui = UI_Classes()._LoadUI()
		LogTxt(__name__, "Found %d UI Classes!" % len(self.ui))

		if UI_CLASS_EXPORT['enabled']:
			ui_class_export = [["Class,Base,Function,Arguments"]]
			for ui_class in self.ui:
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

	def build_window(self):
		self.SetTitleName(NAME)
		self.SetSize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
		self.SetCenterPosition()
		self.AddFlag("movable")

		# Info Text
		self.information = ui.TextLine()
		self.information.SetText("<Version:%s> <UI_Classes:%d>" % (VERSION, len(self.ui)))
		self.information.SetParent(self)
		self.information.SetPosition(10, 30)
		self.information.Show()
		###############################################################################

		# Add Object Button
		self.add_object_button = ui.Button()
		self.add_object_button.SetParent(self)
		self.add_object_button.SetPosition(160, 50)
		self.add_object_button.SetText("<ADD")
		self.add_object_button.ButtonText.SetPosition(66, 9)
		self.add_object_button.SetEvent(ui.__mem_func__(self.OnAddObject))
		self.add_object_button.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.add_object_button.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.add_object_button.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.add_object_button.Show()
		###############################################################################

		# Remove Object Button
		self.remove_object_button = ui.Button()
		self.remove_object_button.SetParent(self)
		self.remove_object_button.SetPosition(self.WINDOW_SIZE[0] - 210 - 55, 50)
		self.remove_object_button.SetText("DELETE>")
		self.remove_object_button.ButtonText.SetPosition(27, 9)
		self.remove_object_button.SetEvent(ui.__mem_func__(self.OnRemoveObject))
		self.remove_object_button.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.remove_object_button.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.remove_object_button.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.remove_object_button.Show()
		###############################################################################

		# New Object Browser
		import n_object_browser

		self.obj_browser = n_object_browser.n_object_browser()
		self.obj_browser.object.SetWindowName("n_object_browser")
		self.obj_browser.set_ui_data(self.ui)
		###############################################################################


		try:
			# Object Browser
			self.new_object_browser = ObjectBrowser(200, 200, globals.BASE_THEME_COLOR, self.ui)
			self.new_object_browser.SetParent(self)
			self.new_object_browser.SetPosition(10, 50)
			self.new_object_browser.Show()
			###############################################################################
		except:
			LogTxt(__name__, "Failed to build Object Browser!")
			return False

		try:
			# Project Browser
			self.project_browser = ProjectBrowser(200, 200, globals.BASE_THEME_COLOR, self.ui)
			self.project_browser.SetParent(self)
			self.project_browser.SetPosition(self.WINDOW_SIZE[0] - 210, 50)
			self.project_browser.Show()
			###############################################################################
		except:
			LogTxt(__name__, "Failed to build Project Browser!")
			return False

		try:
			# Child Config
			self.child_config = ChildConfig(self.WINDOW_SIZE[0] - 20, 205, globals.BASE_THEME_COLOR, self.ui)
			self.child_config.SetParent(self)
			self.child_config.SetPosition(10, 280)
			self.child_config.Show()
			###############################################################################
		except:
			LogTxt(__name__, "Failed to build Child Config!")
			return False

		LogTxt(__name__, "Initialized!")
		return True

	# Add Object to current project by name
	def OnAddObject(self):
		self.project_browser.add_child(self.new_object_browser.selected_object())
		self.new_object_browser.filter.filter_editline.SetText("")
		LogTxt(__name__, "Added %s to Project Browser" % self.new_object_browser.selected_object())

	# Remove Object from current project by name
	def OnRemoveObject(self):
		self.project_browser.remove_child(self.project_browser.selected_child_name())
		self.project_browser.filter.filter_editline.SetText("")
		LogTxt(__name__, "Removed %s from Project Browser" % self.project_browser.selected_child_name())

	# Abusing this loop to update
	def OnRender(self):
		#LogTxt("InterfaceManager::OnRender", "PB_SEL(%s) CC_SEL(%s)" % (self.project_browser.selected_child_name(), self.child_config.selected_child_in_project))

		xMouse, yMouse = wndMgr.GetMousePosition()
		self.information.SetText("<Version:%s> <UI_Classes:%d> <Mouse:%d,%d>" % (VERSION, len(self.ui), xMouse, yMouse))

		if self.child_config.selected_child_in_project != self.project_browser.selected_child_name():
			self.child_config.update(self.project_browser.selected_child_name(), self.project_browser.selected_child_object_name(self.project_browser.selected_child_name()))
		
		# Manage Object Browser Add Button
		if self.new_object_browser.object_list.GetSelectedItemText():
			if self.add_object_button.IsDown() and not self.add_object_button.IsIn():
				self.add_object_button.SetUp()
				self.add_object_button.Disable()
				self.add_object_button.Enable()
		else:
			self.add_object_button.Down()
		##################################################

		# Manage Project Browser Remove Button
		if self.project_browser.object_list.GetSelectedItemText():
			if self.remove_object_button.IsDown() and not self.remove_object_button.IsIn():
				self.remove_object_button.SetUp()
				self.remove_object_button.Disable()
				self.remove_object_button.Enable()
		else:
			self.remove_object_button.Down()
		##################################################

def setup_ifmgr(parent):
	if constinfo.INTERFACE_MANAGER_INITIALIZED == True:
		LogTxt(__name__, "Interface Manager is already initialized!")
		return None

	#try:
	ifmgr = InterfaceManager(550, 500)

	constinfo.INTERFACE_MANAGER_INITIALIZED = True

	return ifmgr
	#except:
	#	LogTxt(__name__, "Failed to initialize!")
	#	return None

############################################################################################################

