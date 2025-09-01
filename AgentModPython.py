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
from HypoModPy.hypomain import *



app = wx.App(False)
pos = wx.DefaultPosition
size = wx.Size(400, 500)
mainpath = ""
respath = ""
modname = "Agent"
mainwin = HypoMain("HypoMod", pos, size, respath, mainpath, modname)
mainwin.Show()
mainwin.SetFocus()
go_foreground()
app.MainLoop()



