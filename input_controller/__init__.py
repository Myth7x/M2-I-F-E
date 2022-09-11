from _utils import LogTxt

import ui, wndMgr, app, ime

class input_controller(ui.Window):
    def __init__(self, parent):
        ui.Window.__init__(self, layer="TOP_MOST")
        self.AddFlag('not_pick')
        self.SetParent(parent)
        self.SetSize(*(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight()))
        self.SetPosition(0, 0)
        self.Show()
        self.Lock()

    def __del__(self):
        ui.Window.__del__(self)
    
    def OnKeyDown(self, key):
        LogTxt(__name__, "OnKeyDown! %s" % key)

    def OnIMEUpdate(self):
        LogTxt(__name__, "OnIMEUpdate! %s" % ime.GetText(False))

    def OnUpdate(self):
        pass