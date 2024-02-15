from printerwatch.DataManager.DataSet import DataBase
from datetime import datetime as dt, date, timedelta
from json import dumps

db = DataBase()

class reqObj(object):
    def __init__(self, **kwargs):
        [self.__setattr__(key, val) for key, val in kwargs.items()]

    def __repr__(self):
        
        return 'req:\n' + '\n'.join([f'{key}: {val}' for key, val in self.__dict__.items()])
    
    def __setattr__(self, key, val):
        if type(val) == list:
            if len(val) == 1:
                val = val[0]
        super().__setattr__(key, val)
        
    def __getattribute__(self, key):
        return super().__getattribute__(key)

    def __getattr__(self, key):
        return False
        
    def build(self, *args):
        if len(args) == 0:
            return {key: val for key, val in self.__dict__.items()}
        else:
            return {key: self.__getattribute__(key) for key in args}
            
    def merge_keys_to(self, mergin:list, to:str):
        self.__setattr__(to, [self.__getattribute__(key) for key in mergin if self.__getattribute__(key)])
        
    def add(self, req):
        [self.__setattr__(key, val) for key, val in req.items()]
        
    def get_return(self):
        return {key: val for key, val in self.__dict__.items()} 

    def if_key(self, key):
        return key in self.__dict__.keys()

# depricated
class responseObj(object):
    def __init__(self, default={'token': {'timetoken': '', 'username': ''}}):
        [self.__setattr__(key, val) for key, val in default.items()]

    def __repr__(self):
        return '\n'.join([f'{key}: {val}' for key, val in self.__dict__.items()])
    
    def get_(self, req):
        print('\n'.join([f'{key}: {val}' for key, val in req.items()]))
        [self.__setattr__(key, val) for key, val in req.items()]
    
    def get_return(self):
        return {key: val for key, val in self.__dict__.items()} 

    def if_key(self, key):
        return key in self.__dict__.keys()

class ResponseHandler(object):
    def __init__(self, view, *args):
        [self.__setattr__(arg.name, arg) for arg in args]



class DataObject(object):
    def __init__(self, past='2022-01-01', befor=None, interval=2, search='*', key='Prints', incr=True, group=False):
        befor = dt.now().date() if befor is None else dt.strptime(befor, '%Y-%m-%d').date()
        self.timeframe = self.timearr((dt.strptime(past, '%Y-%m-%d').date(), befor), timedelta(days=int(interval)))
        self.incr = incr
        self.group = group
        self.search = self.search_code(search)
        self.key = key  # Tracker keys & Carts

    def search_code(self, string):
        if not self.group:
            return string
        else:
            if ';' in string:
                return [s.strip() for s in string.split(';')]
            else:
                return [string, ]
    
    def __repr__(self):
        return '\n'.join([f'{key}: {val}' for key, val in self.__dict__.items()])

    def merge_keys(self, merge_name, keys='*'):
        temp = {}
        for key, data in self.data.items():
            temp[merge_name] = [sum(zipped) for zipped in zip([v for k, v in data.items() if k in keys or keys == '*'])]

    def plot_builder(self):
        ''' does call data_pruning ''' 
        if self.key != 'Carts':
            temp = [{'label': name, 'data': data} for name, data in self.data_pruning()]
            return {'data': dumps({'labels': [date.strftime('%d.%m.%Y') for date in self.timeframe], 'datasets': temp}), 'type': dumps('line')}
        else:
            temp = self.cart_data()
            return {'data': dumps({'labels': temp['label'], 'datasets': [{'label': 'Cart', 'data': temp['data']}]}), 'type': dumps('bar')}
            
    def cart_data(self):
        if self.group is False:
            temp = {'label': [], 'data': []}
            for label, data in [(obj.id, obj.efficency) for obj in self.search_filter()]:
                temp['label'].append(label)
                temp['data'].append(int(data))
            return temp
        else:
            groups = {'label': [], 'data': []}
            for key, val in self.search_filter().items():
                groups['label'].append(key)
                temp = [obj.efficency for obj in val]
                groups['data'].append(sum(temp) // len(temp))
            return groups
            
    def data_pruning(self):
        #                   not grouped
        if self.group is False:
            return [(obj.display_name, self.framer(obj.tracker.data['Date'], obj.tracker.data[self.key])) for obj in self.search_filter()]
        #                   grouped
        else:
            groups = []
            for key, val in self.search_filter().items():
                temp = [self.framer(obj.tracker.data['Date'], obj.tracker.data[self.key]) for obj in val]
                arr = []
                for d in range(len(self.timeframe)):
                    arr.append(sum([t[d] for t in temp if t]))
                groups.append((key, arr))
            return groups

    def framer(self, date, vals):
        if date[0].date() > self.timeframe[-1]:
            return False
        i, temp, arr = 0, 0, []
        for t in range(len(self.timeframe)):
            while i < len(vals) and date[i].date() < self.timeframe[t]:
                if t > 0:
                    temp += vals[i]
                i += 1
            arr += [temp]
            temp = 0 if self.incr is not True else temp
        return arr

    def timearr(self, timeframe, interval):
        t = [dt.strptime(t, "%Y-%m-%d").date() if type(t) == str else t for t in timeframe]
        timearr = []
        while t[0] < t[1]:
             timearr += [t[0]]
             t[0] += interval
        return timearr

    def search_filter(self):
        if self.key != 'Carts':
            if self.search is None:
                return db.printer.obj
            elif type(self.search) == str:
                return [obj for obj in db.printer.get_search(self.search) if obj.tracker.data['Date']]
            elif type(self.search) == list:
                return {s: [obj for obj in db.printer.get_search(s) if obj.tracker.data['Date']] for s in self.search}
        else:
            if self.search is None:
                return db.cartridges.obj
            elif type(self.search) == str:
                return [obj for obj in db.cartridges.get_search(self.search)]
            elif type(self.search) == list:
                return {s: [obj for obj in db.cartridges.get_search(s)] for s in self.search}
                
class PrinterView(object):
    def __init__(self, **kwargs):
        self.db = DataBase()
        self.context = {}
        self.x = 0
        self._update(**kwargs)
        self._selecting(**kwargs)
        self._cart_state()
        
    def _update(self, **kwargs):
        print(' Data Worker Update Start: ')
        if kwargs.get('serial_no', False):
            
            #t = {'serial_no': kwargs.get('serial_no')}
            #t.update({key: val for key, val in kwargs.items()})
            #print(t)
            #db.printer.update_obj(t)
            self.db.printer.update_obj(dict(kwargs))
        print(' Data Worker Update End! ')
        
    def _selecting(self, **kwargs):
        # get index of the obj 
        if not kwargs.get('select', False) and not kwargs.get('serial_no', False):
            x = self.x   # if no request set 0
        else:
            if kwargs.get('select', False) != kwargs.get('serial_no', False):   # if select dropdown was changed use selected objs index
                x = self.db.printer.name_index.index(kwargs.get('select'))
            else:
                x = self.db.printer.name_index.index(kwargs.get('serial_no'))  # else use the previous objs index
                if kwargs.get('next', False):   # and in/decrement it if next or back was used
                    x += 1
                elif kwargs.get('back', False):
                    x += -1 
        for i, key in enumerate(['back', 'selected', 'next']): 
                j = (x + i - 1) % len(self.db.printer.obj)
                if key == 'selected':
                    self.context.update(self.db.printer.obj[j].get_context_obj())
                    self.context[key] = {'serial_no': self.db.printer.obj[j].serial_no, 'display_name': self.db.printer.obj[j].display_name}
                else:
                    self.context[key] = self.db.printer.obj[j].serial_no
        #temp = {'serial_no': self.db.printer.obj[j].serial_no, 'display_name': self.db.printer.obj[j].display_name}
        self.context['selectable'] = [{'serial_no': obj.serial_no, 'display_name': obj.display_name} for obj in self.db.printer.obj]
        self.x = x
    
    def _cart_state(self):
        state = self.db.printer.obj[self.x].tracker.current
        labels, data, color = [], [], []
        c = {'B': (0, 0, 0, 0.5), 'C': (0, 255, 255, 0.5), 'M': (255, 0, 255, 0.5), 'Y': (255, 255, 0, 0.5)}
        self.context['counter'] = {}
        for key, val in state.items():
            if key in 'BCYM':
                labels.append(key), data.append(val), color.append(f"rgba{c[key]}")
            elif key != 'Date':
                self.context['counter'][key] = val
        #temp = {'labels': labels, 'datasets': [{'label': 'Cartridge %', 'data': data, 'backgroundColor': color}]}
        #self.context['config'] = dumps({'type': 'bar', 'data': temp, 'options': {'scales': { 'y': { 'beginAtZero': True }}}})
        self.context['data'] = dumps({'labels': labels, 'datasets': [{'label': 'Cartridge %', 'data': data, 'backgroundColor': color}]})

class CartView(object):
    def __init__(self, **kwargs):
        self.db = DataBase()
        kwargs.update({key: val[0] for key, val in kwargs.items() if type(val) == list})
        print(kwargs)
        self.selectable = self.db.cartridges.name_index
        self.x = 0
        self._selecting(**kwargs)
        print(self.x)
        obj = self.db.cartridges.obj[self.x]
        [self.__setattr__(key, val) for key, val in obj.get_context().items()]

    @property
    def context(self):
        return {key: val for key, val in self.__dict__.items()}
    
    def _selecting(self, **kwargs):
    
        if not kwargs.get('select', False) and not kwargs.get('cart_id', False):
            pass
     
        else:
            if kwargs.get('select', False) != kwargs.get('cart_id', False):   # if select dropdown was changed use selected objs index
                self.x = self.db.cartridges.name_index.index(kwargs.get('select'))
            else:
                self.x = self.db.cartridges.name_index.index(kwargs.get('cart_id'))  # else use the previous objs index
                self._saveing(**kwargs)
        self.x += int(kwargs.get('next', False) == 'Next') - int(kwargs.get('back', False) == 'Back')
        self.x = self.x + len(self.db.cartridges.name_index) if self.x < 0 else self.x % len(self.db.cartridges.name_index)
         
       
    
    def _saveing(self, **kwargs):
        temp = {'price': kwargs.get('price', -1)}
        if kwargs.get('reset', False) == '1':
            temp['reset'] = True
        self.db.cartridges.obj[self.x].edit(**temp)
        #db.cartridges.save()
                
