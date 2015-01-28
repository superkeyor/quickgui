#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "jerryzhujian9@gmail.com"

__doc__ = """Rapidly create GUI without any knowledge of wxpython
=============================================
jerryzhujian9_at_gmail.com
Tested under python 2.7
To see your python version
in terminal: python -V
or in python: import sys; print (sys.version)

inspired by gui2py, easygui
=============================================
Install:
1) Requires wxPython 2.9.2.4 (tested under canopy)
2) or you can install it first manually from
    http://sourceforge.net/projects/wxpython/files/wxPython/2.9.2.4/
Then https://pypi.python.org/pypi/quickgui
pip install quickgui
method 1&2 run: python myscript.py is fine
3) For anacoda python (wxPython 3.0 tested)
but remember to run: pythonw myscript.py instead of python myscript.py

Usage:
import quickgui as q

Message(msg, seconds=10), message
    Displays a timed modal message box, timeout and cancel returns 0, ok returns 1
XPrinter()
    Display a window to capture print output
    if on, both terminal and window (updating gui will greatly increase script execution time)
    if off, only terminal

    Methods: on/off

    Examples:
        xprinter = XPrinter()
        xprinter.on()
        print 'will be shown on window'
        xprinter.off()
        print 'will be shown in terminal'
        xprinter.on()
        print 'on window again'

        for x in range(100):
            print "I am a line of " + str(x)
            # time.sleep(0.01)   
            
alert, confirm, getfile, setfile, getdir, inputs
Alert(message, title="", icon="exclamation")
    # Shows a simple pop-up modal dialog.
    # icon = "exclamation", "error", "question", "info"
Confirm(message="", title="", default=False, ok=False, cancel=False)
    # Asks for confirmation (yes/no or ok and cancel), returns True or False or None.
    # show yes/no by default
    # default sets the default button
    # ok shows OK; cancel shows Cancel

GetFile(directory='', filename='', multiple=False, wildcard='All Files (*.*)|*.*', title="Select file(s)")
    # Shows a dialog to select files to open, return path(s) if accepted.
    # wildcard format: 'BMP files (*.bmp)|*.bmp|GIF files (*.gif)|*.gif'
                        'Pictures (*.jpeg,*.png)|*.jpeg;*.png
SetFile(directory='', filename='', overwrite=False, wildcard='All Files (*.*)|*.*', title="Save"):
    # Shows a dialog to select file to save, return path(s) if accepted.
    # overwrite seems not work?
GetDir(path="", title='Select a directory')
    # Shows a dialog to choose a directory.

values = Inputs(items=[], instruction='Click the button to read the help.', title='Ask for inputs')
    # Flexible dialog for user inputs.
    # Returns a value for each row in a list, e.g. [u'1001', u'female', u'', []]
        # textbox accepts a string or str(default) and returns a string or eval(string)
        # checkbox returns a bool
        # radiobox returns a string or ''
        # combobox returns a string or ''
        # listbox returns a list of strings or []
    # If cancels, returns None

    items = [('ID:', ''),
        ('ID:', 'siu8505'),
        ('ID:', 1001),
        ('IDs:', [1001, 1002]),                             ->textbox   (internally converts data types)
                                                            the first element is the label
                                                            the second is the default value (e.g. an empty string, number or a list)

        ('Logical Switch:', 'Checked?', False),             ->checkBox  (True/False)
        ('Gender:', ['Female', 'Male'], 0),                 ->radiobox  (0,1; -1 does not work)
        ('Race:', ['Black', 'White', 'Other'], -1),         ->combobox  (-1 selects none)
        ('Majors:\n(Can select more than one)',('Psychology','Math','Biology'), 0), ->listbox (multiple)
                                                            the first is the label
                                                            the second is the options:
                                                                a string makes it a checkbox
                                                                a list with two elements makes a radiobox
                                                                a list with more than two elements makes a combobox
                                                                a tuple makes a listbox with multiple choice enabled
                                                            the third is the default value (True/False, index of the list or tuple)

        (''),                                               ->blank line
                                                            just an empty string

        ({'Selecte Input Directory...': "GetDir()"},''),    
        ({'Selecte Output Directory...': "GetDir()"},''),   
        ({'Save as...': "SetFile()"},''),                   ->button
        ({'Selecte Files...': "GetFile(multiple=True)"},[]),->listbox (disabled)
        ({"Output File Name(*.csv):": "SetFile(directory='%s', filename='output.csv', wildcard='CSV Files (*.csv)|*.csv')" % os.getcwd()}, '')]
                                                            the general form is: ({button label: function in a string}, result from function is a str or list)
                                                            the first is a dict with the key is the label, the value is the button event function
                                                            the second is the type of the returned value from the button function
                                                                '' means the button function returns a string
                                                                [] means the button fucntion returns a list

    values = Inputs(items=items)    # returns a list of inputs in the order displayed on the GUI (the insertion of blank line, i.e. ('') in the above example, does not interfere the order of returned values)
"""


import wx
from wx.lib import dialogs

# http://wxpython-users.1045709.n5.nabble.com/Close-Exit-and-Destroy-td2330883.html
# close(), destroy()
# You use Close() when you want to programatically tell the frame to go
# close itself, and is functionally the same as the user telling it to
# close itself with the "X" button.

# Destroy() tells wx to delete the C++ object instance that corresponds to
# the frame.  Normally it will destroy itself when it closes in the
# default EVT_CLOSE event handler, but if you catch the EVT_CLOSE yourself
# you either need to call Destroy in your handler, or call event.Skip so
# the default handler will still run.  The EVT_CLOSE handler is where you
# would normally put the code that checks for open files, asks the user if
# she wants to save them or cancel, etc.  Based on the user's response you
# can veto the close if you want. 

def Alert(message, title="", icon="exclamation", scrolled=False, parent=None):
    """
    Alert(message, title="", icon="exclamation")
    # Shows a simple pop-up modal dialog.
    # icon = "exclamation", "error", "question", "info"
    """
    if not scrolled:
        icons = {'exclamation': wx.ICON_EXCLAMATION, 'error': wx.ICON_ERROR,
             'question': wx.ICON_QUESTION, 'info': wx.ICON_INFORMATION}
        style = wx.OK | icons[icon]
        result = dialogs.messageDialog(parent, message, title, style)
    else:
        result = dialogs.scrolledMessageDialog(parent, message, title)
alert = Alert

def Confirm(message="", title="", default=False, ok=False, cancel=False,
            parent=None):
    """
    Confirm(message="", title="", default=False, ok=False, cancel=False)
    # Asks for confirmation (yes/no or ok and cancel), returns True or False or None.
    # show yes/no by default
    # default sets the default button
    # ok shows OK; cancel shows Cancel
    """
    style = wx.CENTRE
    if ok:
        style |= wx.OK 
    else:
        style |= wx.YES | wx.NO
        if default:
            style |= wx.YES_DEFAULT
        else:
            style |= wx.NO_DEFAULT
    if cancel:
        style |= wx.CANCEL
    result = dialogs.messageDialog(parent, message, title, style)
    if cancel and result.returned == wx.ID_CANCEL:
        return None
    return result.accepted  # True or False
confirm = Confirm

def GetFile(directory='', filename='', multiple=False, wildcard='All Files (*.*)|*.*',
            title="Select file(s)", parent=None):
    """
    GetFile(directory='', filename='', multiple=False, wildcard='All Files (*.*)|*.*', title="Select file(s)")
    # Shows a dialog to select files to open, return path(s) if accepted.
    # wildcard format: 'BMP files (*.bmp)|*.bmp|GIF files (*.gif)|*.gif'
                        'Pictures (*.jpeg,*.png)|*.jpeg;*.png

    """
    style = wx.FD_OPEN
    if multiple:
        style |= wx.FD_MULTIPLE
    result = wx.FileDialog(parent, title, directory, filename, wildcard,
                                style)
    if result.ShowModal() == wx.ID_CANCEL:
        return None
    else:
        if multiple:
            return result.GetPaths()
        else:
            return result.GetPath()
getfile = GetFile

def SetFile(directory='', filename='', overwrite=False, wildcard='All Files (*.*)|*.*',
            title="Save", parent=None):
    """
    SetFile(directory='', filename='', overwrite=False, wildcard='All Files (*.*)|*.*', title="Save"):
    # Shows a dialog to select file to save, return path(s) if accepted.
    # overwrite seems not work?
    """
    style = wx.FD_SAVE
    if not overwrite:
        style |= wx.FD_OVERWRITE_PROMPT
    result = wx.FileDialog(parent, title, directory, filename, wildcard,
                                style)
    if result.ShowModal() == wx.ID_CANCEL:
        return None
    else:
        return result.GetPath()
setfile = SetFile

def GetDir(path="", title='Select a directory', parent=None):
    """
    GetDir(path="", title='Select a directory')
    # Shows a dialog to choose a directory.
    """
    result = wx.DirDialog(parent, title, path)
    if result.ShowModal() == wx.ID_CANCEL:
        return None
    else:
        return result.GetPath()
getdir = GetDir

class _Inputs(wx.Dialog):
    """a custom dialog
    values = Inputs(items=[], instruction='Click the button to read the help.', title='Ask for inputs')
    # Flexible dialog for user inputs.
    # Returns a value for each row in a list, e.g. [u'1001', u'female', u'', []]
        # textbox accepts a string or str(default) and returns a string or eval(string)
        # checkbox returns a bool
        # radiobox returns a string or ''
        # combobox returns a string or ''
        # listbox returns a list of strings or []
    # If cancels, returns None

    items = [('ID:', ''),
        ('ID:', 'siu8505'),
        ('ID:', 1001),
        ('IDs:', [1001, 1002]),                             ->textbox   (internally converts data types)
                                                            the first element is the label
                                                            the second is the default value (e.g. an empty string, number or a list)

        ('Logical Switch:', 'Checked?', False),             ->checkBox  (True/False)
        ('Gender:', ['Female', 'Male'], 0),                 ->radiobox  (0,1; -1 does not work)
        ('Race:', ['Black', 'White', 'Other'], -1),         ->combobox  (-1 selects none)
        ('Majors:\n(Can select more than one)',('Psychology','Math','Biology'), 0), ->listbox (multiple)
                                                            the first is the label
                                                            the second is the options:
                                                                a string makes it a checkbox
                                                                a list with two elements makes a radiobox
                                                                a list with more than two elements makes a combobox
                                                                a tuple makes a listbox with multiple choice enabled
                                                            the third is the default value (True/False, index of the list or tuple)

        (''),                                               ->blank line
                                                            just an empty string

        ({'Selecte Input Directory...': "GetDir()"},''),    
        ({'Selecte Output Directory...': "GetDir()"},''),   
        ({'Save as...': "SetFile()"},''),                   ->button
        ({'Selecte Files...': "GetFile(multiple=True)"},[]),->listbox (disabled)
        ({"Output File Name(*.csv):": "SetFile(directory='%s', filename='output.csv', wildcard='CSV Files (*.csv)|*.csv')" % os.getcwd()}, '')]
                                                            the general form is: ({button label: function in a string}, result from function is a str or list)
                                                            the first is a dict with the key is the label, the value is the button event function
                                                            the second is the type of the returned value from the button function
                                                                '' means the button function returns a string
                                                                [] means the button fucntion returns a list

    values = Inputs(items=items)    # returns a list of inputs in the order displayed on the GUI (the insertion of blank line, i.e. ('') in the above example, does not interfere the order of returned values)
    """

    def __init__(self, items=[], instruction='', title=''):
        instruction = str(instruction)
        wx.Dialog.__init__(self, None, -1, title=title, style=wx.DEFAULT_FRAME_STYLE)

        szrMain = wx.BoxSizer(wx.VERTICAL)  # default boxsizer
        szrSub = wx.FlexGridSizer(len(items)+1, 2, 15, 10)   # flexible gridsizer, +1 for help/cancel/ok buttons

        # parse items
        self.szrMain = szrMain
        self.widgets = []
        self.buttons = {}
        for item in items:
            # textbox
            if (len(item) == 2) and (type(item[0]) in [str]):
                (text, default) = item
                label = wx.StaticText(self, wx.ID_ANY, text, style=wx.ALIGN_RIGHT)
                szrSub.Add(label, 0, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)

                if default == None : default = '' # in order to display empty string in the textbox instead of "None"
                textbox = wx.TextCtrl(self, wx.ID_ANY, str(default), size=(len(str(default)*10),-1)) # try to convert to string if not a string
                self.widgets.append(textbox)
                szrSub.Add(textbox, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)

            # checkbox, radiobox, combobox, listbox
            elif len(item) == 3:
                (text, value, default) = item
                label = wx.StaticText(self, wx.ID_ANY, text, style=wx.ALIGN_RIGHT)
                szrSub.Add(label, 0, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)

                # checkbox
                if type(value) in [str] and value != '':
                    checkbox = wx.CheckBox(self, wx.ID_ANY, value)
                    checkbox.SetValue(default)
                    self.widgets.append(checkbox)
                    szrSub.Add(checkbox, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
                # radiobox
                elif (type(value) in [list]) and len(value) == 2:
                    radiobox = wx.RadioBox(self, wx.ID_ANY, "", choices=value, majorDimension=0, style=wx.RA_SPECIFY_ROWS)
                    radiobox.SetSelection(default)
                    self.widgets.append(radiobox)
                    szrSub.Add(radiobox, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
                # combobox
                elif (type(value) in [list]) and len(value) > 2:
                    combobox = wx.ComboBox(self, wx.ID_ANY, choices=value, style=wx.CB_DROPDOWN | wx.CB_READONLY)
                    combobox.SetSelection(default)
                    self.widgets.append(combobox)
                    szrSub.Add(combobox, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
                # listbox (multiple)
                elif type(value) in [tuple]:
                    listbox = wx.ListBox(self, wx.ID_ANY, choices=list(value), style=wx.LB_MULTIPLE)
                    listbox.SetSelection(default)
                    self.widgets.append(listbox)
                    szrSub.Add(listbox, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)

            # button with event
            elif (len(item) == 2) and (type(item[0]) in [dict]):
                text, fn, resultType = item[0].keys()[0], item[0].values()[0], type(item[1])

                btnEvent = wx.Button(self, wx.ID_ANY, text)
                if resultType in [str]:
                    bxEvent = wx.TextCtrl(self, wx.ID_ANY, '')
                    # bxEvent.Enable(False)
                elif resultType in [list]:
                    bxEvent = wx.ListBox(self, wx.ID_ANY, choices=[])
                    bxEvent.SetSelection(-1)
                    bxEvent.Enable(False)
                self.widgets.append(bxEvent)
                # this is the tricky part
                self.buttons[text] = [fn, resultType, bxEvent]
                btnEvent.Bind(wx.EVT_BUTTON, lambda event: self._fnEvent(event))
                szrSub.Add(btnEvent, 0, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
                szrSub.Add(bxEvent, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)

            # blank
            else:
                label = wx.StaticText(self, wx.ID_ANY, '', style=wx.ALIGN_RIGHT)
                szrSub.Add(label, 0, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
                label = wx.StaticText(self, wx.ID_ANY, '')
                szrSub.Add(label, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)

        btnHelp = wx.Button(self, wx.ID_HELP, "Help")
        ## msecs; Set the delay after which the tooltip disappears or how long a tooltip remains visible.
        ## May not be supported on all platforms (eg. Cocoa, GTK).
        #wx.ToolTip.SetAutoPop(10*60*1000)
        btnHelp.SetToolTip(wx.ToolTip(instruction))
        btnHelp.Bind(wx.EVT_BUTTON, lambda handler: Alert(instruction, title="Help", parent=None, scrolled=False, icon="info"))
        btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        szrHelpCancel = wx.FlexGridSizer(1, 2, 0, 10)
        szrHelpCancel.Add(btnHelp, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        szrHelpCancel.Add(btnCancel, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        szrSub.Add(szrHelpCancel, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        btnOK = wx.Button(self, wx.ID_OK, "OK")
        btnOK.SetDefault()
        szrSub.Add(btnOK, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        szrMain.Add(szrSub, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(szrMain)
        szrMain.Fit(self)   # auto resize the window to fit its contents
        self.Layout()   # update/redraw the frame
        self.Center()   # make it come up on the center of the screen

    def _fnEvent(self, event):
        button = event.GetEventObject()
        text = button.GetLabel()
        fn, resultType, theBox = self.buttons[text]
        
        result = eval(fn)
        if resultType in [str]:
            if result == None: result = ''
            theBox.SetValue(result)
        if resultType in [list]:
            if result == None: result = []
            theBox.Set(result)
        self.szrMain.Fit(self)
        self.Layout()
        self.Center()

    def return_values(self):
        values = []

        for widget in self.widgets:
            if type(widget) in [wx._controls.TextCtrl, wx._controls.CheckBox]:
                try:
                    values.append(eval(widget.GetValue())) # try to convert from string
                except:
                    values.append(widget.GetValue())
            elif type(widget) in [wx._controls.RadioBox, wx._controls.ComboBox]:
                values.append(widget.GetStringSelection())
            elif type(widget) in [wx._controls.ListBox]:
                if widget.IsEnabled():
                    values.append([widget.GetString(index) for index in widget.GetSelections()])
                else:
                    values.append([widget.GetString(index) for index in range(widget.GetCount())])

        return values


def Inputs(items=[], instruction='Click the button to read the help.', title='Ask for inputs'):
    """Flexible dialog for user inputs."""
    dlg = _Inputs(items=items, instruction=instruction, title=title)
    
    # communicate between dlg and this function
    # the dlg should also have a cancel button; if only has OK, then click the x close button returns wx.ID_OK
    if dlg.ShowModal() == wx.ID_OK:
        values = dlg.return_values()
    else:
        values = None
    dlg.Destroy()
    
    return values
inputs = Inputs


class _TimedMessageDialog(wx.Dialog):
    def __init__(self, message, title, ttl=10):
        wx.Dialog.__init__(self, None, -1, title,size=(400, 150))
        self.CenterOnScreen(wx.BOTH)
        self.timeToLive = ttl

        stdBtnSizer = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL) 
        stMsg = wx.StaticText(self, -1, message)
        self.stTTLmsg = wx.StaticText(self, -1, 'Closing this dialog box in %d s...'%self.timeToLive)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(stMsg, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox.Add(self.stTTLmsg,1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox.Add(stdBtnSizer,1, wx.ALIGN_CENTER|wx.TOP, 10)
        self.SetSizer(vbox)

        self.timer = wx.Timer(self)
        self.timer.Start(1000) #Generate a timer event every second
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)

    def onTimer(self, evt):
        self.timeToLive -= 1
        self.stTTLmsg.SetLabel('Close itself in %d s...'%self.timeToLive)

        if self.timeToLive <= 0:
            self.timer.Stop()
            self.Close()

def Message(msg, seconds=10):
    """Message(msg, seconds=10)
    Displays a timed modal message box
    timeout and cancel returns 0, ok returns 1
    """
    dlg = _TimedMessageDialog(msg, 'Message', seconds)               
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return 1
    else:
        return 0
message = Message

#####################################################################
# http://www.blog.pythonlibrary.org/2009/01/01/wxpython-redirecting-stdout-stderr/
# http://stackoverflow.com/questions/22211658/implementing-my-own-event-loop-in-a-wxpython-application
# http://wiki.wxpython.org/LongRunningTasks
# http://wiki.wxpython.org/Non-Blocking%20Gui
#####################################################################
class XPrinter(wx.Frame):
    """
    Display a window to capture print output
    if on, both terminal and window (updating gui will greatly increase script execution time)
    if off, only terminal

    Methods: on/off

    Examples:
        xprinter = XPrinter()
        xprinter.on()
        print 'will be shown on window'
        xprinter.off()
        print 'will be shown in terminal'
        xprinter.on()
        print 'on window again'

        for x in range(100):
            print "I am a line of " + str(x)
            # time.sleep(0.01)   
    """
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Welcome to this App!")
    
        # GUI stuff
        # Add a panel so it looks the correct on all platforms
        thePanel = wx.Panel(self, wx.ID_ANY)
        self.txtCtrl = wx.TextCtrl(thePanel, wx.ID_ANY, size=(300,100),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        self.txtCtrl.Enable(False)
        self.theBtn = wx.Button(thePanel, wx.ID_ANY, 'Close')
        # Add widgets to a sizer        
        theSizer = wx.BoxSizer(wx.VERTICAL)
        theSizer.Add(self.txtCtrl, 1, wx.ALL|wx.EXPAND, 5)
        theSizer.Add(self.theBtn, 0, wx.ALL|wx.CENTER, 5)
        thePanel.SetSizer(theSizer)
        self.Layout()
        self.Center()
        self.Show()
        self.theBtn.SetDefault()
        self.theBtn.SetFocus()
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.theBtn)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)

    def flush(self):    
        """force flushing/updating gui"""
        # make the size small enough to visually hide the splash
        # the timer interval cannot be too small, >=50 ms
        class _ModifiedTimedMessageDialog(wx.Dialog):
            def __init__(self, message, title, ttl=10):
                wx.Dialog.__init__(self, None, -1, title,size=(0, 0),style=wx.SYSTEM_MENU)
                self.CenterOnScreen(wx.BOTH)
                self.timeToLive = ttl
                self.timer = wx.Timer(self)
                self.timer.Start(100) #Generate a timer event every second
                self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
            def onTimer(self, evt):
                self.timeToLive -= 2
                if self.timeToLive <= 0:
                    self.timer.Stop()
                    self.Close()
        dlg = _ModifiedTimedMessageDialog('', 'flushing', 0)               
        dlg.ShowModal()

    def write(self, string):
        self.txtCtrl.WriteText(string)
        self.flush()

    # escape key to quit
    def OnKeyUP(self, evt):
        keyCode = evt.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.OnClose(evt)

    def OnClose(self,evt):
        self.Close()    

    def on(self):
        self._SetPrinter(1,self)

    def off(self):
        self._SetPrinter(0,self)

    def _SetPrinter(self, status, gui):
        """
        Prints output to both terminal and a gui log window globally.
        """
        import sys, datetime

        class Logger(object):
            def __init__(self, gui):
                self.gui = gui
                sys.stdout = sys.__stdout__
                self.terminal = sys.stdout
                self.log = self.gui
                # self.log.write("++++++++++\n")
                # self.log.write(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "\n")
                # self.log.flush()

            def write(self, message):
                self.terminal.write(message)
                self.log.write(message)
                self.log.flush()

            def off(self):
                # self.log.write(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "\n")
                # self.log.write("++++++++++\n")
                # self.log.write("\n")
                self.log.flush()
                sys.stdout = sys.__stdout__

        if status:
            # restore first if it has been changed
            try:
                sys.stdout.off()
            except AttributeError:
                pass

            sys.stdout = Logger(gui)
        else:
            try:
                sys.stdout.off()
            except AttributeError:
                pass


if __name__ == "__main__":
    app = wx.App(redirect=False)
    import os, time
    xprinter = XPrinter()
    xprinter.on()
    print 'will be shown on window'
    xprinter.off()
    print 'will be shown in terminal'
    xprinter.on()
    print 'on window again'

    xprinter.off()
    for x in range(100):
        print "I am a line of " + str(x)
        # time.sleep(0.01)
    
    # items = [('ID:', ''),
    #     ('ID:', 'uni30122133231231123235'),
    #     ('ID:', 1001),
    #     ('IDs:', [1001, 1002]),
    #     ('Logical Switch:', 'Checked?', False),
    #     ('Gender:', ['Female', 'Male'], 0),
    #     ('Race:', ['Black', 'White', 'Other'], -1),
    #     (''),
    #     ({'Selecte Input Directory...': "GetDir()"},''),
    #     ({'Selecte Output Directory...': "GetDir()"},''),
    #     ({'Save as...': "SetFile()"},''),
    #     ({'Selecte Files...': "GetFile(multiple=True)"},[]),
    #     ('Majors:\n(Can select more than one)',('Psychology','Math','Biology'), 0),
    #     ({"Output File Name(*.csv):": "SetFile(directory='%s', filename='output.csv', wildcard='CSV Files (*.csv)|*.csv')" % os.getcwd()}, '')]
    
    # values = Inputs(items=items, instruction=__doc__)
    # print values

    # put at the bottom to keep gui window alive
    # app.MainLoop()


