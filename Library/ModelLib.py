from printerwatch.Library.BaseLib import Lib, DB_DIR, Path
from printerwatch.Library.Items.Models import Model

class PrintermodelLib(Lib):
    file = Path(DB_DIR, 'modelslib.json')
    
    def __init__(self):
        self.item = Model
        self.obj = []
        self.ids = []
        self._load()

    def add_new(self, **kwargs):
        try:
            temp = self.item(**kwargs)
            if not temp.id in self.ids:
                self.ids.append(temp.id)
                self.obj.append(temp)
                self.save()
            else:
                print(f'id: {temp.id} already exists')
        except:
            print(f'exception during PrintermodelLib.add_new({kwargs})')

# Execution Sandbox
if __name__ == '__main__':
    mLib = PrintermodelLib()
    print(mLib)
    print(mLib.obj[0].color)
