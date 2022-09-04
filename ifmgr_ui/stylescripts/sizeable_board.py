import wndMgr, ui

from ...ifmgr_ui.board import IfMgr_Board

SCREEN_WIDTH = wndMgr.GetScreenWidth()
SCREEN_HEIGHT = wndMgr.GetScreenHeight()

_class = IfMgr_Board

object = {
    "name" : "SizeableBoard",

    "title" : "Object-Browser",

    "style" : ("movable", "float",),

    "sizeable" : {
        'enabled' : True,
        'min_width' : 200,
        'min_height' : 400,
        'max_width' : 500,
        'max_height' : 900,
    },

	"x" : 1,
	"y" : 1,

	"width" : 220,
	"height" : 450,

	"children" :
	(
        {
            "name" : "test_child",
            "type" : "board",
            "style" : ("attach",),

            "x" : 0,
            "y" : 0,

            "width" : 220,
            "height" : 450,
        },
        {
            "name" : "test_titlebar",
            "type" : "titlebar",
            "style" : ("attach",),

            "x" : 0,
            "y" : 0,

            "width" : 220,
            "height" : 30,

            "children" :
            (
                {
                    "name" : "test_titlebar_title",
                    "type" : "text",
                    "style" : ("attach",),

                    "x" : 136/2,
                    "y" : 5,

                    "text" : "Sizeable Board Title",

                    "text_horizontal_align" : "center",
                },
            ),
        },
        {
            "name" : "test_random_text",
            "type" : "text",
            "style" : ("attach",),

            "x" : 220/2,
            "y" : 450/2,

            "position" : "relative",

            "text" : "Lorem Ipsum Dolor Sit Amet",

            "text_horizontal_align" : "center",
            "text_vertical_align" : "center",
        }
    ),
}
