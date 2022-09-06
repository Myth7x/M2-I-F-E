from proto_utils import LogTxt
import ui, grp

class YesNoDialog(ui.BoardWithTitleBar):
    def __init__(self):
        ui.BoardWithTitleBar.__init__(self)
        self.AddFlag("movable")
        self.SetSize(300, 100)
        self.SetCenterPosition()
        self.SetTitleName("YesNo Dialog")
        self.SetCloseEvent(self.Close)

        self.text_lines = []
        self.text_lines.append(ui.TextLine())
        self.text_lines[0].SetParent(self)
        self.text_lines[0].SetText("YesNo Dialog")
        self.text_lines[0].SetPosition(self.GetWidth() / 2, 33)
        self.text_lines[0].SetHorizontalAlignCenter()
        self.text_lines[0].Show()

        self.button_yes = ui.Button()
        self.button_yes.SetParent(self)
        self.button_yes.SetEvent(ui.__mem_func__(self.on_button_yes))
        self.button_yes.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
        self.button_yes.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
        self.button_yes.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
        self.button_yes.SetPosition((self.GetWidth() / 2) - (self.button_yes.GetWidth()/2) - 50, 60)
        self.button_yes.SetText("Yes")
        self.button_yes.Show()

        self.button_no = ui.Button()
        self.button_no.SetParent(self)
        self.button_no.SetEvent(ui.__mem_func__(self.on_button_no))
        self.button_no.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
        self.button_no.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
        self.button_no.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
        self.button_no.SetPosition((self.GetWidth() / 2) - (self.button_no.GetWidth()/2) + 50, 60)
        self.button_no.SetText("No")
        self.button_no.Show()

        self.fn_callback = None

        self.Show()

    def set_title(self, title):
        self.SetTitleName(title)

    def set_desc(self, text):
        self.text_lines[0].SetText(text)

    def set_callback(self, func):
        self.fn_callback = func

    def on_button_yes(self):
        if self.fn_callback:
            self.fn_callback(True)
        self.Close()

    def on_button_no(self):
        if self.fn_callback:
            self.fn_callback(False)
        self.Close()

    def Close(self):
        self.Hide()
        ui.BoardWithTitleBar.__del__(self)
