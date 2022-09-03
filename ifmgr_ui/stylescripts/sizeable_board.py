import wndMgr, ui

from ...ifmgr_ui.board import IfMgr_Board

SCREEN_WIDTH = wndMgr.GetScreenWidth()
SCREEN_HEIGHT = wndMgr.GetScreenHeight()

_class = IfMgr_Board

object = {
    "name" : "SizeableBoard",

    "title" : "Sizeable Board Title",

    "style" : ("movable", "float",),

    "customFlag" : "sizeable",

	"x" : 1,
	"y" : 1,

	"width" : 136,
	"height" : 161,

	"children" :
	(
        {
            "name" : "test_child",
            "type" : "board",
            "style" : ("attach",),

            "x" : 1,
            "y" : 1,

            "width" : 136,
            "height" : 161,
        },
        {
            "name" : "test_titlebar",
            "type" : "titlebar",
            "style" : ("attach",),

            "x" : 1,
            "y" : 1,

            "width" : 136,
            "height" : 161,

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

            "x" : 136/2,
            "y" : 161/2,

            "position" : "relative",

            "text" : "Lorem Ipsum Dolor Sit Amet",

            "text_horizontal_align" : "center",
            "text_vertical_align" : "center",
        }
    ),
}
