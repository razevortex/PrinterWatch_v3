from printerwatch.Library.Items import *#Cartridges, Models, Printer, Tracker
from printerwatch.StaticVar import DB_DIR
from json import dumps, loads
from os.path import exists
from pathlib import Path

class Lib(object):
    __name__ = 'Base'
    file = Path(DB_DIR)
    def __init__(self):
        self.item = Base.Obj
        self.obj = []
        self.ids = []
        self._load()
    
    def __repr__(self):
        msg = self.__name__ + '=> ' + f'[{len(self.ids)}] => {self.ids}\n'
        msg += '\n'.join([str(obj) for obj in self.obj])
        return msg
    
    def save(self):
        temp = self._import()
        try:
            with open(self.file, 'w') as f:
                f.write(dumps(self._export()))
        except:
            with open(self.file, 'w') as f:
                f.write(dumps(temp))
    
    def _export(self):
        '''
        self to obj for json
        @return: list(dict)
        '''
        return [obj.export() for obj in self.obj]
    
    def _import(self):
        with open(self.file, 'r') as f:
            return loads(f.read())

    def _load(self):
        if exists(self.file):
            for obj in self._import():
                temp = self.item(**obj)
                if not self.get(temp.id):
                    self.obj += [temp]
                    self.ids += [temp.id]
                    
    def update(self, *args):
        for arg in args:
            if arg.get('id', False):
                self.obj[self.ids.index(arg.get('id', False))].update_attr(**arg)
        self.save()

    def get(self, string='*'):
        if string != '*' and string not in self.ids:
            return None
        else:
            return self.obj if string == '*' else self.obj[self.ids.index(string)]
    
    def search(self, string):
        string = [string, ] if ' ' not in string else string.split(' ')
        temp = []
        for obj in self.obj:
            if not (False in [obj == q for q in string]):
                temp.append(obj)
        return temp




# Execution Sandbox
if __name__ == '__main__':
    pass
