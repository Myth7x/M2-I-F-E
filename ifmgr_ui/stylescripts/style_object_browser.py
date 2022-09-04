import wndMgr, ui

from ...ifmgr_ui.board import Board_Custom

SCREEN_WIDTH = wndMgr.GetScreenWidth()
SCREEN_HEIGHT = wndMgr.GetScreenHeight()

_class = Board_Custom

WIDTH = 240
HEIGHT = 480

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
            "name" : "titlebar",
            "type" : "titlebar",

            "x" : 3,
            "y" : 0,

            "width" : WIDTH - 6,
            "height" : 30,

            "children" :
            (
                {
                    "name" : "titlebar_title",
                    "type" : "text",

                    "x" : 18,
                    "y" : 3,

                    "text" : "Object-Browser",

                    "text_horizontal_align" : "left",
                },
                {
                    "name" : "titlebar_info",
                    "type" : "text",

                    "x" : WIDTH - 32,
                    "y" : 3,

                    "text" : "[ 0 objects ]",

                    "fontname" : "Tahoma:12",

                    "text_horizontal_align" : "right",
                },
                
            ),
        },
        {
            "name" : "bg_object_list",
            "type" : "thinboard",

            "x" : 8,
            "y" : 23,

            "width" : WIDTH - 15,
            "height" : HEIGHT - 60 - 50 - 10 + 25,

            "size"      : "relative",
        },
        {
            "name" : "object_list",
            "type" : "listbox_scroll",

            "x" : 10 + 4,
            "y" : 23 + 5 + 4,

            "width" : WIDTH - 15 - 11,
            "height" : HEIGHT - 60 - 50 - 30 + 25,


            "item_align" : wndMgr.HORIZONTAL_ALIGN_LEFT,

            "size"      : "relative",
        },

        # Show Attributes Button
        {
        	"name" : "btn_show_attributes",
        	"type" : "button",

        	"x" : 8,
        	"y" : 23 + 5 + 4 + (HEIGHT - 60 - 50 - 30) + 13 + 28,

        	"text" : "Attributes",
        	"horizontal_align" : "left",
        	"vertical_align" : "top",

            "tooltip_text" : "Show attributes",

        	"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
            "over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
            "down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
        },

        # Add Button
        {
            "name" : "btn_add",
            "type" : "button",

            "x" : 8 + 80,
            "y" : 23 + 5 + 4 + (HEIGHT - 60 - 50 - 30) + 13 + 28,

            "text" : "Add",

            "tooltip_text" : "Add selected object to scene",

            "default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
            "over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
            "down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
        },

        # Refresh Button
        {
            "name" : "btn_refresh",
            "type" : "button",

            "x" : 8 + WIDTH - 15 - 61,
            "y" : 23 + 5 + 4 + (HEIGHT - 60 - 50 - 30) + 13 + 28,

            "text" : "Refresh",

            "tooltip_text" : "Refreshes the object browser",

            "default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
            "over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
            "down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
        },

        {
            "name" : "bg_selected_object",
            "type" : "thinboard",

            "x" : 8,
            "y" : HEIGHT - 40,

            "width" : WIDTH - 15,
            "height" : 30,

            "size"      : "relative",
        },

        

        {
            "name" : "text_selected_object",
            "type" : "text",

            "x" : 18,
            "y" : HEIGHT - 40 + 8,

            "text" : "Selected: None",

            "text_horizontal_align" : "left",
        },
    ),
}
