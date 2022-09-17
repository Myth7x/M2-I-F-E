import wndMgr, ui, grp

from ...ifmgr_ui.board import Board_Custom

SCREEN_WIDTH = wndMgr.GetScreenWidth()
SCREEN_HEIGHT = wndMgr.GetScreenHeight()

_class = Board_Custom

WIDTH = 240
HEIGHT = 430

object = {
    "name" : "scene_browser",

    "style" : ("movable", "float",),

    "sizeable" : {
        'enabled' : False,
        'min_width' : 200,
        'min_height' : 400,
        'max_width' : 500,
        'max_height' : 900,
    },

	"x" : SCREEN_WIDTH - WIDTH - 8,
	"y" : 70,

	"width" : WIDTH,
	"height" : HEIGHT,

	"children" :
	(
        {
            "name" : "board",
            "type" : "board",
            "style" : ("attach",), 

            "x" : 0,
            "y" : 0,

            "width" : WIDTH,
	        "height" : HEIGHT,

        },
        {
            "name" : "titlebar_title",
            "type" : "text",
            "x" : 15,
            "y" : 9,
            "text" : "Scene Browser",
            "text_horizontal_align" : "left",
        },
        {
            "name" : "bg_object_list",
            "type" : "thinboard",

            "x" : 8,
            "y" : 26,

            "width" : WIDTH - 15,
            "height" : 370,

            "size"      : "relative",
        },
        {
            "name" : "object_list",
            "type" : "listbox_scroll",

            "x" : 10 + 4,
            "y" : 26 + 6,

            "width" : WIDTH - 15 - 11,
            "height" : 370 - 12,

            "show_line_count" : False,

            "font_name" : "Fixedsys:14",

            "item_align" : wndMgr.HORIZONTAL_ALIGN_LEFT,

            "size"      : "relative",
        },

        # Copy Raw Data
        {
        	"name" : "btn_copy_raw_data",
        	"type" : "button",

        	"x" : 8,
        	"y" : HEIGHT - 30,

        	"text" : "Copy Raw Data",
        	"horizontal_align" : "left",
        	"vertical_align" : "top",

            "tooltip_text" : "Copy style dictionary to clipboard",

        	"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
            "over_image" : "d:/ymir work/ui/public/large_button_02.sub",
            "down_image" : "d:/ymir work/ui/public/large_button_03.sub",
        },

        # Save
        {
            "name" : "btn_save",
            "type" : "button",

            "x" : WIDTH - 8 - 60,
            "y" : HEIGHT - 30,

            "text" : "Save",

            "tooltip_text" : "Save scene to file",

            "default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
            "over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
            "down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
        },

    ),
}
