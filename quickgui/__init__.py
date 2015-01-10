import os, sys
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, MODULE_PATH)

import wx


# create an app, note that the app could be already created (i.e. by an IDE):
app = wx.GetApp()
if app is None:
    app = wx.App(False)
    main_loop = app.MainLoop
else:
    # app and main loop is already created and executed by a third party tool
    main_loop = lambda: None


from quickgui import *
from quickgui import __doc__
from version import __version__
