Rapidly create GUI without any knowledge of wxpython
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
        ('Majors:
(Can select more than one)',('Psychology','Math','Biology'), 0), ->listbox (multiple)
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
