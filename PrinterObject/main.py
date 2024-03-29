from json import dumps, loads
from os import path
from .StaticVar import *
from printerwatch.GlobalClasses import LockedClass
from printerwatch.Libs.main import cLib, mLib
from printerwatch.PrinterObject.Logs import Logger
from printerwatch.PrinterObject.Tracker import PrinterTracker


class Printer(LockedClass):
    def __init__(self, **kwargs):
        print('printer :', kwargs)
        self.active = kwargs.get('active', True)
        self.serial_no = kwargs.get('serial_no')
        self.model = mLib.get(kwargs.get('model'))
        self.display_name = kwargs.get('display_name', self.serial_no)
        self.notes = kwargs.get('notes', '')
        self.ip = kwargs.get('ip', '')
        self.location = kwargs.get('location', '')
        self.contact = kwargs.get('contact', '')
        cart = kwargs.get('cartridges', [])
        if cart == []:
            cart = self.set_default_carts()
        #print(self.serial_no, cLib.get(*kwargs.get('cartridges', self.model.cartridges))) 
        self.cartridges = cLib.get(*cart) #*kwargs.get('cartridges', self.model.cartridges))
        self.cartridges = [c.id for c in self.cartridges]
        self.tracker = PrinterTracker(self.serial_no, self.model.name)
        super().__init__('serial_no', 'model')

    def set_default_carts(self):
        return [f'{self.manufacturer} {cart}' for cart in self.model.cartridges]
            
    @property
    def manufacturer(self):
        return self.model.manufacturer

    @property
    def model_(self):
        return self.model.name

    @property
    def cart_fill(self):
        return {key: val for key, val in self.tracker.current.__dict__.items() if key in 'BCYM'}

    @property
    def counter(self):
        return {key: val for key, val in self.tracker.current.__dict__.items() if not key in 'BCYM' and key != "Date"}
     

        
    def get_context_obj(self):
        temp = {'manufacturer': self.manufacturer, 'model': self.model_}
        temp.update({key: self.__dict__[key] for key, val in self.__dict__.items() if key in ('serial_no', 'display_name', 'ip', 'cartridges', 'location', 'contact', 'active', 'notes')})
        temp['cartridges'] = cLib.get_select_context(*temp['cartridges'])
        return {'obj': temp, 'counter': self.counter, 'carts': self.cart_fill}
    


    def update_data(self, kwargs):
        for key, val in [(key, val) for key, val in kwargs.items() if key in self.__dict__.keys()]:
            old = self.__getattribute__(key)
            self.__setattr__(key, val)
            Logger(self.serial_no).logging(key, old, self.__getattribute__(key))

    def __str__(self):
        return f'{self.serial_no}\n{self.model}\n{self.display_name}\n{self.ip}\n{self.location}\n{self.contact}\n{self.notes}\n'
        
    @property
    def search_ref(self):
        return self.__str__().casefold()
        
    def string_compare(self, search_query):
        '''
        A Match function for Search/Filter Query´s
        :param search_query: string 
        :return: bool
        '''
        keys = (search_query, ) if ' ' not in search_query else search_query.split(' ') 
        for key in keys:
            if (key.startswith('-') and key[1:].casefold() in self.search_ref) or (not key.startswith('-') and key.casefold() not in self.search_ref):
                return False
        return True 
        
    #def match_search(self, string:str):
    #    for arg in string.split('&&'):
    #        if not self.string_compare(arg, str(self)):
    #            return None
    #    return self

    def save_tracker(self):
        self.tracker.save()

    def export(self):
        return {'serial_no': self.serial_no, 'model': self.model.name, 'active': self.active,
                'display_name': self.display_name, 'cartridges': self.cartridges, 'ip': self.ip,
                'location': self.location, 'contact': self.contact, 'notes': self.notes}
        
    def _print(self):
        print(self.serial_no)
        print(self.ip)
        print(self.model)
        print(str(self.tracker))

    def update_tracker(self, **kwargs):
        '''
        Update the trackers with one value per tracker
        @param kwargs: {tracker_keys: value}
        @return: None
        '''
        print('in update tracker method')
        self.tracker.update(kwargs, carts=self.cartridges)
        self.save_tracker()

    def update_tracker_batch(self, **kwargs):
        '''
        Update the trackers with multiple values at once
        @param kwargs: {tracker_keys: [value_list]}
        @return: None
        '''
        for i in range(len(kwargs.get('Date', []))):
            temp = {key: val[i] for key, val in kwargs.items()}
            self.tracker.update(temp, carts=self.cartridges)
        self.save_tracker()

    def get_data_tracker(self):
        return self.tracker.data


class PrinterLib(object):
    obj = []
    name_index = []
    file = Path(DB_DIR, 'printer.json')
    
    def __init__(self):
        if path.exists(PrinterLib.file):
            self.load()
    
    def __repr__(self):
        msg = ''
        for obj in PrinterLib.obj:
            msg += str(obj) + '\n' + str(obj.tracker) + '\n\n'
        return msg

    #def get_context(self, printer=PrinterLib.name_index[0], ):
    #    temp = [p.displayname for p in PrinterLib.obj]
        
    def add_new(self, **kwargs):
        if kwargs.get('serial_no', False) and not kwargs.get('serial_no', False) in self.name_index:
            print(kwargs)
            new = Printer(**kwargs)
            print(new)
            PrinterLib.obj.append(new)
            PrinterLib.name_index.append(new.serial_no)
            print(self.name_index)
            self.save()

    def get_obj(self, name):
        if name in PrinterLib.name_index:
            return PrinterLib.obj[PrinterLib.name_index.index(name)]
        return None

    def update_obj(self, obj):
        for i, obj_ in enumerate(PrinterLib.obj):
            if obj_.serial_no == obj['serial_no']:
                print('old')
                print(PrinterLib.obj[i].update_data(obj))
                PrinterLib.obj[i].update_data(obj)
                print('new')
                print(PrinterLib.obj[i].update_data(obj))
        self.save()

    def save(self):
        temp = self._import()
        try:
            with open(PrinterLib.file, 'w') as f:
                f.write(dumps(self._export()))
        except:
            print('An Error Occured file wasnt saved')
            with open(PrinterLib.file, 'w') as f:
                f.write(dumps(temp))

    def get_search(self, this):
        if this == '*':
            return self.obj
        return [obj for obj in self.obj if obj.string_compare(this)]


    def data_tracker_set(self, search):
        obj_set = self.get_search(search)
        data = obj_set[0].tracker.data
        for obj in obj_set[1:]:
            data = data + obj.tracker.data
        return data

    def _export(self):
        '''
        self to obj for json
        @return: list(dict)
        '''
        
        return [obj.export() for obj in PrinterLib.obj]
    
    def _import(self):
        if PrinterLib.file is not None:
            with open(PrinterLib.file, 'r') as f:
                return loads(f.read())
    
    def load(self):
        for obj in self._import():
            if obj['serial_no'] not in PrinterLib.name_index:
                PrinterLib.obj += [Printer(**obj)]
                PrinterLib.name_index += [obj['serial_no']]


pLib = PrinterLib()
if __name__ == '__main__':
    print(pLib)
