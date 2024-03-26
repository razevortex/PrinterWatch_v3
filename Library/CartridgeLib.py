from printerwatch.Library.BaseLib import Lib, DB_DIR, Path
from printerwatch.Library.Items.Cartridges import Cartridge

class CartLib(Lib):
    file = Path(DB_DIR, 'cartlib.json')
    def __init__(self):
        self.item = Cartridge
        self.obj = []
        self.ids = []
        self._load()

    def add_new(self, **kwargs):
        if kwargs.get('batch', False):
            temp = kwargs['name'].split('/')           
            sets = [{'name': temp[0] + name, 'color': col, 'manufacturer': kwargs['manufacturer']} for name, col in zip(temp[1:], kwargs['color'])]
            for kwarg in sets:
                self.add_new(**kwarg)
        else:
            try:
                temp = self.item(**kwargs)
                if not temp.id in self.ids:
                    self.ids.append(temp.id)
                    self.obj.append(temp)
                    self.save()
                else:
                    print(f'id: {temp.id} already exists') 
            except:
                print(f'exception during CartLib.add_new({kwargs})')



# Execution Sandbox
if __name__ == '__main__':
    cLib = CartLib()
    print(cLib)
