from Packages.Libs.StaticVar import *
from Packages.GlobalClasses import LockedSlots
from json import dumps, loads
from pathlib import Path
from os import path

#  Just a Container of a Cart-Type
class _CartridgeModel(LockedSlots):
    __slots__ = 'name', 'manufacturer', 'color', 'price', 'global_stats'

    def __init__(self, **kwargs):
        [self.__setattr__(key, val) for key, val in kwargs.items()]
        if not kwargs.get('global_stats', False):
            self.__setattr__('global_stats', {'Pages': 0, 'Toner': 0})
        super().__init__('name', 'manufacturer', 'color')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'  name = {self.name}\n  manufacturer = {self.manufacturer}\n  color = {self.color}\n  global_stats = {self.global_stats}\n'

    def update(self, **kwargs):
        self.global_stats['Toner'] += kwargs.get(self.color, 0)
        for key, val in [(key, val) for key, val in kwargs.items() if key != 'Date']:
            if self.color == 'B' and key in ('Prints', 'Copies'):
                self.global_stats['Pages'] += val
            if key.startswith('Color'):
                self.global_stats['Pages'] += val

    def reset_stats(self):
        self.__setattr__('global_stats', {'Pages': 0, 'Toner': 0})

    def export(self):
        return {slot: self.__getattribute__(slot) for slot in self.__slots__}


#  a Lib of the Cartridges
class CartridgesLib(object):
    obj = []
    name_index = []
    file = Path(DB_DIR, 'cartlib.json')
    
    def __init__(self):

        self.load()
            
    def __repr__(self):
        msg = 'Cartridges Lib :\n\n'
        for sub in CartridgesLib.obj:
            msg += f'{str(sub)}\n'
        return msg

    def save(self):
        temp = self._import()
        try:
            with open(CartridgesLib.file, 'w') as f:
                f.write(dumps(self._export()))
        except:
            with open(CartridgesLib.file, 'w') as f:
                f.write(dumps(temp))

    def _export(self):
        '''
        self to obj for json
        @return: list(dict)
        '''
        return [obj.export() for obj in CartridgesLib.obj]

    def _import(self):
        with open(CartridgesLib.file, 'r') as f:
            return loads(f.read())

    def load(self):
        if path.exists(CartridgesLib.file):
            for obj in self._import():
                if obj['name'] not in CartridgesLib.name_index:
                    CartridgesLib.obj += [_CartridgeModel(**obj)]
                    CartridgesLib.name_index += [obj['name']]
    
    def build_new(self, name='name', manufacturer='manufacturer', color='color', price=-1):
        if name not in CartridgesLib.name_index and name != 'name':
            kwargs = {'name': name, 'manufacturer': manufacturer, 'color': color, 'price': price, 'global_stats': {'pages': 0, 'usage': 0}}
            cart = _CartridgeModel(**kwargs)
            CartridgesLib.obj.append(cart)
            CartridgesLib.name_index.append(cart.name)
        self.save()

    def get(self, *args):
        if args[0] == '*':
            return CartridgesLib.obj
        return [CartridgesLib.obj[CartridgesLib.name_index.index(arg)] for arg in args if arg in CartridgesLib.name_index]

    def get_filtered_set(self, **kwargs):
        arr = []
        for obj in CartridgesLib.obj:
            add = True
            for key, val in [(key, val) for key, val in kwargs.items() if
                             key in ('name', 'manufacturer', 'color')]:
                if add:
                    add = (val == obj.__getattribute__(key))
            if add:
                arr.append(obj)
        return arr

    def update(self, carts:tuple, data:dict) -> None:
        for i, obj in enumerate(CartridgesLib.name_index):
            if obj in carts:
                CartridgesLib.obj[i].update(**data)
        self.save()

    def reset_stats(self, carts='*'):
        for obj in self.get(carts):
            obj.reset_stats()
            CartridgesLib.obj[CartridgesLib.name_index.index(obj.name)] = obj
        self.save()