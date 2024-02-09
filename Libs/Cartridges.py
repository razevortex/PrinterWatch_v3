from json import dumps, loads
from os import path
from pathlib import Path
from .StaticVar import DB_DIR
from printerwatch.GlobalClasses import LockedSlots


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
    
    @property
    def id(self):
        return f'{self.manufacturer} {self.name}'

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

    def _id(self, string):
        if type(string) == dict:
            return ' '.join([string.get('manufacturer', ''), string.get('name', '')])
        elif isinstance(string, _CartridgeModel):
            return string.id
        elif type(string) == str:
            return string
        else:
            return ''
            
    def _exists(self, this):
        return self._id(this) in self.name_index
        
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
                if not self._exists(obj): #f"{obj['manufacturer']} {obj['name']}" not in CartridgesLib.name_index:
                    CartridgesLib.obj += [_CartridgeModel(**obj)]
                    CartridgesLib.name_index += [CartridgesLib.obj[-1].id] #[obj['name']]
    
    def build_new(self, name='name', manufacturer='manufacturer', color='color', price=-1):
        if not self._exists(f'{manufacturer} {name}') and name != 'name':
            kwargs = {'name': name, 'manufacturer': manufacturer, 'color': color, 'price': price, 'global_stats': {'pages': 0, 'usage': 0}}
            CartridgesLib.obj += [_CartridgeModel(**kwargs)]
            CartridgesLib.name_index += [CartridgesLib.obj[-1].id]
            #cart = _CartridgeModel(**kwargs)
            #CartridgesLib.obj.append(cart)
            #CartridgesLib.name_index.append(cart.name)
        self.save()

    def get_select_context(self, *args):
        temp = []
        for arg in args:
            for i, name in enumerate(self.name_index):
                if name.endswith(arg):
                    temp.append(self.obj[i].id)
        return {arg.color: {'selected': arg.id, 'options': [c.id for c in CartridgesLib.obj if c.color == arg.color]} for arg in self.get(*args)}
        
    def get(self, *args):
        if args[0] == '*':
            return self.obj
        return [self.obj[self.name_index.index(arg)] for arg in args if arg in self.name_index]

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

    def get_types_view(self):
        temp = {typ: {'color': [], 'manufacturer': ''} for typ in set(list([name.rstrip('BKCYM') for name in CartridgesLib.name_index]))}
        view = {}
        for obj in CartridgesLib.obj:
            key = obj.name.rstrip('BKCYMS')
            if key not in view.keys():
                view[key] = {'color': [], 'manufacturer': [], 'member': []}
            for val in ('color', 'manufacturer'):
                view[key][val] = list(set(view[key][val] + [obj.__getattribute__(val)]))
            view[key]['member'] += [obj.name]
        return view

