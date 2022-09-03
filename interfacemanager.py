# UI Builder by myth, b1g speed in ya nose
# IfMgr : Interface Manager

NAME = "Interface Manager"
VERSION = '0.1-Rev.Pepp'
UI_CLASS_EXPORT = {
	'enabled' 	: True,
	'path' 		: 'C:\\Proto_InterfaceManager\\%s_ui_classes.csv',
}

###############################################################################

import datetime

# Python Modules
import constinfo, ui
# CPython Modules
from grp import GenerateColor

# Interface Manager Modules
from ui_class_gathering import UI_Classes
from proto_utils import LogTxt
from object_browser import ObjectBrowser
from project_browser import ProjectBrowser
from child_config import ChildConfig

###############################################################################

BASE_THEME_COLOR = GenerateColor(0.3, 0.3, 0.3, 0.85)

class InterfaceManager(ui.ThinBoard):

	def __init__(self, width, height):
		LogTxt(NAME, "Initializing..")

		ui.ThinBoard.__init__(self)

		self.WINDOW_SIZE = [width, height]

		LogTxt(NAME, "Looking for UI Classes..")

		self.ui = UI_Classes()._LoadUI()
		LogTxt(NAME, "Found %d UI Classes!" % len(self.ui))

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
			LogTxt(NAME, "Exported UI Classes to %s" % target_file)

		LogTxt(NAME, "Building Window..")
		self.BuildWindow()
		LogTxt(NAME, "Window Built!")

		self.Show()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def BuildWindow(self):
		self.SetSize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
		self.SetCenterPosition()
		self.AddFlag("movable")

		# Title
		self.title_bar = ui.Bar()
		self.title_bar.SetParent(self)
		self.title_bar.SetSize(self.WINDOW_SIZE[0], 25)
		self.title_bar.SetPosition(0, 0)
		self.title_bar.SetColor(BASE_THEME_COLOR)
		#self.title_bar.AddFlag("movable") We need a hook onto onmousemove event on bar, if moving, update parent position relative to mouse position
		self.title_bar.Show()
		self.title = ui.TextLine()
		self.title.SetFontName("Tahoma:16")
		self.title.SetText("Interface Manager")
		self.title.SetParent(self.title_bar)
		self.title.SetPosition(int(self.WINDOW_SIZE[0]/2), 2)
		self.title.SetHorizontalAlignCenter()
		self.title.Show()
		###############################################################################

		# Info Text
		self.information = ui.TextLine()
		self.information.SetText("<Version:%s> <UI_Classes:%d>" % (VERSION, len(self.ui)))
		self.information.SetParent(self.title_bar)
		self.information.SetPosition(10, 30)
		self.information.Show()
		###############################################################################

		# Object Browser
		self.new_object_browser = ObjectBrowser(200, 200, BASE_THEME_COLOR, self.ui)
		self.new_object_browser.SetParent(self)
		self.new_object_browser.SetPosition(10, 50)
		self.new_object_browser.Show()
		###############################################################################

		# Project Browser
		self.project_browser = ProjectBrowser(200, 200, BASE_THEME_COLOR, self.ui)
		self.project_browser.SetParent(self)
		self.project_browser.SetPosition(self.WINDOW_SIZE[0] - 210, 50)
		self.project_browser.Show()
		###############################################################################

		# Child Config
		self.child_config = ChildConfig(self.WINDOW_SIZE[0] - 20, 205, BASE_THEME_COLOR, self.ui)
		self.child_config.SetParent(self)
		self.child_config.SetPosition(10, 280)
		self.child_config.Show()
		###############################################################################

		# Add Object Button
		self.add_object_button = ui.Button()
		self.add_object_button.SetParent(self)
		self.add_object_button.SetPosition(205, 70)
		self.add_object_button.SetText("Add Object>")
		self.add_object_button.ButtonText.SetPosition(45, 8)
		self.add_object_button.SetEvent(ui.__mem_func__(self.OnAddObject))
		self.add_object_button.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.add_object_button.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.add_object_button.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.add_object_button.Show()
		###############################################################################

		# Remove Object Button
		self.remove_object_button = ui.Button()
		self.remove_object_button.SetParent(self)
		self.remove_object_button.SetPosition(205, 100)
		self.remove_object_button.SetText("<Remove Object")
		self.remove_object_button.ButtonText.SetPosition(45, 8)
		self.remove_object_button.SetEvent(ui.__mem_func__(self.OnRemoveObject))
		self.remove_object_button.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.remove_object_button.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.remove_object_button.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.remove_object_button.Show()
		###############################################################################

		# Save Button
		self.save_button = ui.Button()
		self.save_button.SetParent(self)
		self.save_button.SetPosition(205, 190)
		self.save_button.SetText("Save Project")
		self.save_button.ButtonText.SetPosition(45, 8)
		#self.save_button.SetEvent(ui.__mem_func__(self.OnSave))
		self.save_button.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.save_button.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.save_button.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.save_button.Show()
		###############################################################################

		# Export Button
		self.export_button = ui.Button()
		self.export_button.SetParent(self)
		self.export_button.SetPosition(205, 220)
		self.export_button.SetText("Export UI")
		self.export_button.ButtonText.SetPosition(45, 8)
		#self.export_button.SetEvent(ui.__mem_func__(self.OnExport))
		self.export_button.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.export_button.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.export_button.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.export_button.Show()

	def OnAddObject(self):
		self.project_browser.add_child(self.new_object_browser.selected_object())
		self.new_object_browser.filter.filter_editline.SetText("")
		LogTxt(NAME, "Added %s to Project Browser" % self.new_object_browser.selected_object())

	def OnRemoveObject(self):
		self.project_browser.remove_child(self.project_browser.selected_child_name())
		self.project_browser.filter.filter_editline.SetText("")
		LogTxt(NAME, "Removed %s from Project Browser" % self.project_browser.selected_child_name())

	def OnRender(self):
		if self.child_config.selected_child_in_project != self.project_browser.selected_child_name():
			self.child_config.update(self.project_browser.selected_child_name(), self.project_browser.selected_child_object_name(self.project_browser.selected_child_name()))
			LogTxt(NAME, "Child Config updated: %s" % self.project_browser.selected_child_name())

def setup_ifmgr():
	if constinfo.INTERFACE_MANAGER_INITIALIZED == True:
		LogTxt(NAME, "Interface Manager is already initialized!")
		LogTxt(NAME, "Restart client if you want to reinitialize it.")
		return None
	
	#try:
	ifmgr = InterfaceManager(500, 500)

	constinfo.INTERFACE_MANAGER_INITIALIZED = True

	return ifmgr
	#except:
	#	LogTxt(NAME, "Failed to initialize!")
	#	return None
