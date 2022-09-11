from _utils import LogTxt
import ui, wndMgr, ime, grp

class InputDialog(ui.BoardWithTitleBar):
    def __init__(self):
        ui.BoardWithTitleBar.__init__(self)
        self.AddFlag("movable")
        self.SetSize(300, 100)
        self.SetCenterPosition()
        self.SetTitleName("Input Dialog")
        self.SetCloseEvent(self.Close)

        self.default_input = ""

        self.input_bg_big = ui.Bar()
        self.input_bg_big.SetParent(self)
        self.input_bg_big.SetSize(274, 18)
        self.input_bg_big.SetPosition(10, 33)
        self.input_bg_big.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
        self.input_bg_big.Show()

        self.input_bg_value = ui.Bar()
        self.input_bg_value.SetParent(self)
        self.input_bg_value.SetSize(146, 18)
        self.input_bg_value.SetPosition(10 + 120, 33)
        self.input_bg_value.SetColor(grp.GenerateColor(0.3, 0.3, 0.3, 0.5))
        self.input_bg_value.Show()

        self.input_desc = ui.TextLine()
        self.input_desc.SetParent(self.input_bg_big)
        self.input_desc.SetPosition(10, 2)
        self.input_desc.SetText("Input:")
        self.input_desc.Show()

        self.input = ui.EditLine()
        self.input.SetParent(self)
        self.input.SetPosition(10 + 120 + 4, 33 + 4)
        self.input.SetSize(146, 18)
        self.input.SetMax(16)
        self.input.Show()
        self.input.SetReturnEvent(self.on_press_return)
        self.input.OnMouseLeftButtonDown = self.OnMouseLeftButtonDown

        self.button = ui.Button()
        self.button.SetParent(self)
        self.button.SetEvent(ui.__mem_func__(self.on_button_press))
        self.button.SetUpVisual("d:/ymir work/ui/public/XLarge_Button_01.sub")
        self.button.SetOverVisual("d:/ymir work/ui/public/XLarge_Button_02.sub")
        self.button.SetDownVisual("d:/ymir work/ui/public/XLarge_Button_03.sub")
        self.button.SetPosition((self.GetWidth() / 2) - (self.button.GetWidth()/2), 60)
        self.button.SetText("OK")
        self.button.Show()
        self.fn_callback = None

        self.Show()

    def set_size(self, width, height):
        self.SetSize(width, height)

        self.button.SetPosition((self.GetWidth() / 2) - (self.button.GetWidth()/2), 60)
        self.input.SetSize((self.GetWidth() / 2) - (self.button.GetWidth()/2), 18)
        self.input_bg_big.SetSize(self.GetWidth() - 20, 18)
        self.input_bg_value.SetSize((self.GetWidth() / 2) - 20, 18)

    def set_callback(self, func):
        self.fn_callback = func

    def on_press_return(self):
        self.on_button_press()

    def on_button_press(self):
        LogTxt(__name__, self.input.GetText())
        if self.fn_callback:
            self.fn_callback(self.input.GetText())
        self.Close()

    def set_input_desc(self, text):
        self.input_desc.SetText(text)
    
    def set_input(self, text):
        self.default_input = text
        self.input.SetText(text)
    
    def get_input(self):
        return self.input.GetText()
    
    def set_title(self, title):
        self.SetTitleName(title)

    def Show(self):
        self.SetCenterPosition()
        self.SetTop()
        ui.BoardWithTitleBar.Show(self)

    def Close(self):
        self.Hide()
        ui.BoardWithTitleBar.__del__(self)

    def OnMouseLeftButtonDown(self):
        if self.input.GetText() == self.default_input:
            self.input.SetText("")
        else:
            if self.input.GetText() == "" and self.IsFocus() != True:
                self.input.SetText(self.default_input)

        ui.EditLine.OnMouseLeftButtonDown(self.input)
        