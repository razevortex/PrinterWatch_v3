from printerwatch.Library.CartridgeLib import CartLib as cLib
from printerwatch.Library.ModelLib import PrintermodelLib as mLib
from printerwatch.Library.PrinterLib import PrinterLib as pLib


class DB(object):
    def __init__(self):
        self.cart, self.model = cLib(), mLib()
        pLib.cLib, pLib.mLib = self.cart, self.model
        self.printer = pLib()

    def __repr__(self):
        msg = ''
        for lib in (self.cart, self.model, self.printer):
            msg += f'{lib.__name__} => [{lib.len}]:\n' 
            msg += '\n   '.join([f'{obj.__name__} > {obj}' for obj in lib.obj]) + '\n'
        return msg

    def add_new(self, sub_lib, **kwargs):
        tlib = {'cart': self.cart, 'model': self.model}[sub_lib]
        for key in tlib.item.mandatory:
            if not key in kwargs.keys():
                return
            if key == 'cartridges':
                for c in kwargs[key]:
                    if not c in cLib.ids:
                        return
        tlib.add_new(**kwargs)
        
