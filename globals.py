from dbg import TraceError
from grp import GenerateColor

NAME = "Interface Manager"
VERSION = '0.1.2 - Object Attributes'
UI_CLASS_EXPORT = {
	'enabled' 	: False,
	'path' 		: 'C:\\InterfaceManager\\%s_ui_classes.csv',
}

BASE_THEME_COLOR_RGBA   = (0.3, 0.3, 0.3, 1)
BASE_THEME_COLOR        = GenerateColor(*BASE_THEME_COLOR_RGBA)

BASE_THEME_EDITBOX_BACKGROUND_COLOR_RGBA    = (0.2, 0.2, 0.2, 0.9)
BASE_THEME_EDITBOX_BACKGROUND_COLOR         = GenerateColor(*BASE_THEME_EDITBOX_BACKGROUND_COLOR_RGBA)

SCALE_BORDER_COLOR_RGBA  = (0.5, 0.6, 0.5, 0.13)
BASE_THEME_SCALE_BORDER_COLOR       = GenerateColor(*SCALE_BORDER_COLOR_RGBA)

TEXT_INFO_COLOR_RGBA    = (0.9, 0.9, 0.9, 1)
BASE_THEME_SCALE_INFO_COLOR         = GenerateColor(*TEXT_INFO_COLOR_RGBA)

UI_CLASS_DATA = {}

CLR_SCENE_OBJECT_MOUSE_OVER = GenerateColor(0.6, 0.6, 0.6, 0.08)
CLR_SCENE_OBJECT_MOUSE_DOWN = GenerateColor(0.6, 0.6, 0.6, 0.15)

CLR_SCENE_INFO = GenerateColor(0.9, 0.9, 0.9, 1)

CLR_SCENE_OBJECT_DRAG_CAN_DROP = GenerateColor(0.6, 0.6, 0.6, 0.08)
CLR_SCENE_OBJECT_DRAG_CANNOT_DROP = GenerateColor(0.9, 0.1, 0.1, 0.08)#(0.1, 0.9, 0.1, 0.08)

CLR_SCENE_TEXT_INDICATOR = GenerateColor(0.6, 0.6, 0.6, 0.5)

INFO_INPUT_SCENE_NAME = "(press <ENTER> for default name)"

MIN_WINDOW_INTERSECTION_FACTOR = 1200
