## HypoModPython
##
## Started 5/11/18
## Continued 24/8/22
##
## Duncan MacGregor
##
## AgentModPy
## Started 21/5/25 in ZJE Haining


import wx
from HypoModPy.hypomain import HypoMain


class HypoApp(wx.App):
    def OnInit(self):
        pos = wx.DefaultPosition
        size = wx.Size(400, 500)
        mainpath = ""
        respath = ""
        modname = "Agent"

        self.mainwin = HypoMain("HypoMod", pos, size, respath, mainpath, modname)
        self.SetTopWindow(self.mainwin)
        self.mainwin.Show()
        self.mainwin.SetFocus()
        return True

app = HypoApp(False)
app.MainLoop()





