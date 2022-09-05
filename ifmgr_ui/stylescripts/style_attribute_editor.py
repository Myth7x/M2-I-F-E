import wndMgr, ui, grp

from ...ifmgr_ui.board import Board_Custom

SCREEN_WIDTH = wndMgr.GetScreenWidth()
SCREEN_HEIGHT = wndMgr.GetScreenHeight()

_class = Board_Custom

WIDTH = 550
HEIGHT = 300

CATEGORY_ATTRIBUTES_WIDTH = WIDTH/3
CATEGORY_ATTRIBUTES_HEIGHT = HEIGHT - 34

CATEGORY_CONFIG_WIDTH = WIDTH/2 - 16
CATEGORY_CONFIG_HEIGHT = HEIGHT - 34

object = {
    "name" : "n_attribute_editor",

    "style" : ("movable", "float",),

    "sizeable" : {
        'enabled' : False,
        'min_width' : 200,
        'min_height' : 400,
        'max_width' : 500,
        'max_height' : 900,
    },

	"x" : SCREEN_WIDTH/2 - WIDTH/2,
	"y" : SCREEN_HEIGHT/2 - HEIGHT/2,

	"width" : WIDTH,
	"height" : HEIGHT,

	"children" :
	(
        {
            "name" : "board",
            "type" : "board_with_titlebar",
            "style" : ("attach",), 

            "x" : 0,
            "y" : 0,

            "width" : WIDTH,
	        "height" : HEIGHT,

            "title" : "Attribute Editor",

            "children" :
            (
                # Category Attribute List
                {
                    "name" : "category_attributes",
                    "type" : "thinboard",

                    "x" : 8,
                    "y" : 29,

                    "width" : CATEGORY_ATTRIBUTES_WIDTH,
                    "height" : CATEGORY_ATTRIBUTES_HEIGHT,

                    "children" :
                    (
                        {
                            "name" : "text_attributes_title",
                            "type" : "text",

                            "x" : CATEGORY_ATTRIBUTES_WIDTH/2,
                            "y" : 8,

                            "text" : "Attributes",
                            "text_horizontal_align" : "center",
                        },
                        {
                            "name" : "line_under_title",
                            "type" : "bar",

                            "x" : CATEGORY_ATTRIBUTES_WIDTH/2 - 50,
                            "y" : 22,

                            "width" : 100,
                            "height" : 1,

                            "color" : 0xffAAA6A1,
                        },
                    ),
                },

                # Category Attribute Configuration
                {
                    "name" : "category_attribute_configuration",
                    "type" : "thinboard",

                    "x" : 8 + CATEGORY_ATTRIBUTES_WIDTH + 8,
                    "y" : 29,

                    "width" : CATEGORY_CONFIG_WIDTH,
                    "height" : CATEGORY_CONFIG_HEIGHT,

                    "children" :
                    (
                        {
                            "name" : "text_attribute_configuration_title",
                            "type" : "text",

                            "x" : CATEGORY_CONFIG_WIDTH/2,
                            "y" : 8,

                            "text" : "Attribute Configuration",
                            "text_horizontal_align" : "center",
                        },
                        {
                            "name" : "line_under_title",
                            "type" : "bar",

                            "x" : CATEGORY_CONFIG_WIDTH/2 - 80,
                            "y" : 22,

                            "width" : 160,
                            "height" : 1,

                            "color" : 0xffAAA6A1,
                        },
                    ),
                },
            ),
        },
    ),
}
