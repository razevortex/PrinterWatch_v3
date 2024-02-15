To Do List:
  Seperate The Lib Classes from there Objs
    - Objs Package with Cartridge.py, Model.py, Printer.py, Tracker.py (! Tracker needs to get the CartsObject passed directly and not just the ref)
    - Objs Package maybe a BaseObj.py for methods like search_strings, json export, a validation method?
    - Libs Package with cLib.py, mLib.py, pLib.py (should include the main Tracker class), BaseLib(see above BaseObj), __init__.py (should load the full Libs in some Struc)
    
