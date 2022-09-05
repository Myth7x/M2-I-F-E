import wndMgr, ui, grp

from ...ifmgr_ui.board import Board_Custom

SCREEN_WIDTH = wndMgr.GetScreenWidth()
SCREEN_HEIGHT = wndMgr.GetScreenHeight()

_class = Board_Custom

WIDTH = 240
HEIGHT = 430

object = {
    "name" : "n_object_browser",

    "style" : ("movable", "float",),

    "sizeable" : {
        'enabled' : False,
        'min_width' : 200,
        'min_height' : 400,
        'max_width' : 500,
        'max_height' : 900,
    },

	"x" : 8,
	"y" : 70,

	"width" : WIDTH,
	"height" : HEIGHT,

    #"instructions" : 
    #(
    #    {
    #        "type" : "on_update",
    #        "exec_string" : 'LogTxt("OnUpdate", "TEST")'
    #    },
    #    {
    #        "type" : "on_render",
    #        "exec_string" : 'LogTxt("OnRender", "TEST")'
    #    },
    #),

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
            "text" : "Object Browser",
            "text_horizontal_align" : "left",
        },
        {
            "name" : "titlebar_info",
            "type" : "text",
            "x" : WIDTH - 20 + 3,
            "y" : 9,
            "text" : "[ UI Classes: %d ]",
            "fontname" : "Tahoma:12",
            "text_horizontal_align" : "right",
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


            "item_align" : wndMgr.HORIZONTAL_ALIGN_LEFT,

            "size"      : "relative",
        },

        # Refresh Button
        {
            "name" : "btn_refresh",
            "type" : "button",

            "x" : WIDTH - 80,
            "y" : HEIGHT - 32,

            "text" : "Refresh",

            "tooltip_text" : "Refreshes the object browser",

            "default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
            "over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
            "down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
        },

    ),
}
