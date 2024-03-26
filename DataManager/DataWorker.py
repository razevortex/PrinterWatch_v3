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
        try:
            return super().__getattribute__(key)
        except:
            return self.__getattr__(key)

    def __getattr__(self, key):
        return False
        
    def build(self, *args):
        if len(args) == 0:
            return {key: val for key, val in self.__dict__.items()}
        else:
            return {key: self.__getattribute__(key) for key in args}
            
    def merge_keys_to(self, mergin:list, to:str):
        self.__setattr__(to, [self.__getattribute__(key) for key in mergin if key in self.__dict__.keys()])
        
    def add(self, req):
        [self.__setattr__(key, val) for key, val in req.items()]
        
    def get_return(self):
        return {key: val for key, val in self.__dict__.items()} 

    def if_key(self, key):
        return key in self.__dict__.keys()
        
class ClientGroup(object):
    def __init__(self, groups, timeframe, keys):
        self.names = []
        self.obj = []
        
        for key, val in groups.items():
            
            
            print(key, self._data_pruning(keys, timeframe, val.tracker.data))
            self.names.append(key)
            self.obj.append(self._data_pruning(keys, timeframe, val.tracker.data))

        print('TIME FRAME -------------------', timeframe)
        
    def __repr__(self):
        msg = ''
        for i in range(len(self.names)):
            msg += f'{self.names[i]} =>\n'
            msg += '    ' + '\n    '.join([f'{key} => {val}' for key, val in self.obj[i].items()]) + '\n'
        return msg

    def _data_pruning(self, keys, timeframe, data):
        print("_data_pruning")
        print('key groups', self._get_key_groups(keys))
        return {k: self._time_pruning(d, data['Date'], timeframe) for key in self._get_key_groups(keys)}
    
    def _time_pruning(self, data, date, timeframe):
        print("_time_pruning")
        temp = {key: [] for key in data.keys()}
        
        for ts in self._time_frame_index(date, timeframe):
            if ts is None:
                [temp[key].append(0) for key in temp.keys()]
            else:
                [temp[key].append(sum(data[key][ts[0]:ts[1]])) for key in temp.keys()]
        return temp                
        
    def _time_frame_index(self, date, timeframe):
        print("_time_frame_index")
        if date[0].date() > self.timeframe[-1]:
            return False
        i, arr = 0, []
        for time in range(len(timeframe)):
            while i < len(date) and date[i].date() < timeframe[time]:
                i += 1
            arr.append(i if i != 0 else None)
        return [None if arr[i] is None else (0, arr[i]) if arr[i-1] is None else (arr[i-1], arr[i]) for i in range(1, len(arr))]
        
    def _get_key_groups(self, key):
        if key != 'Carts':
            keys = ['Prints', 'Copies'], ['ColorPrints', 'ColorCopies']
            return {'TotalGroup': keys[0] + keys[1], 'ColorGroup': keys[1], 'NonColorGroup': keys[0]}.get(key, [key, ])
        else:
            return key


class DataObject(object):
    def __init__(self, past='2022-01-01', befor=None, interval=2, search='*', key='Prints', incr=True, group=False, avg=False, group_key=False):
        befor = dt.now().date() if befor is None else dt.strptime(befor, '%Y-%m-%d').date()
        self.timeframe = self.timearr((dt.strptime(past, '%Y-%m-%d').date(), befor), timedelta(days=int(interval)))
        self.incr, self.group, self.avg, self.group_key = incr, group, avg, group_key
        self.key = key  # Tracker keys & Carts
        self.search = self.search_code(search)
        
    def search_code(self, string):
        lib = 'p' if 'cart' not in self.key.casefold() else 'c'
        if not self.group:
            return DataBase().get_search_clients(string, lib_=lib)
        else:
            if string.startswith('!'):
                return DataBase().get_search_attr(string[1:], lib_=lib)   
            else:
                return DataBase().get_search_groups(string, lib_=lib)
    
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
            if not self.group_key:
                return {'data': dumps({'labels': [date.strftime('%d.%m.%Y') for date in self.timeframe], 'datasets': temp}), 'type': dumps('line')}
            else:
                data = {'labels': [obj['label'] for obj in temp], 'datasets': []}
                for key in self._get_key_groups():
                    datasets = {'label': key, 'data': []}
                    for obj in temp:
                        pass
        else:
            temp = self.cart_data()
            return {'data': dumps({'labels': temp['label'], 'datasets': [{'label': 'Cart', 'data': temp['data']}]}), 'type': dumps('bar')}
            
    def cart_data(self):
        if self.group is False:
            temp = {'label': [], 'data': []}
            for label, data in [(key, val.efficency) for key, val in self.search.items()]:
                temp['label'].append(label)
                temp['data'].append(int(data))
            return temp
        else:
            groups = {'label': [], 'data': []}
            for key, val in self.search.items():
                groups['label'].append(key)
                temp = [obj.efficency for obj in val]
                groups['data'].append(sum(temp) // len(temp))
            return groups
    
    def _get_key_groups(self):
        keys = ['Prints', 'Copies'], ['ColorPrints', 'ColorCopies']
        return {'TotalGroup': keys[0] + keys[1], 'ColorGroup': keys[1], 'NonColorGroup': keys[0]}[self.key]
    
    def key_handle(self, data):
        if 'Group' in self.key:
            key = self._get_key_groups()
            temp = {k: self.framer(data['Date'], data[k]) for k in key if k in data.keys()}
            if self.group_key:
                return {key: sum([temp[key][i] for key in temp.keys()]) for i in range(len(temp[key[0]]))}
            else:
                return {key: sum(val) // len(val) for key, val in temp.items() if temp.get(key, False)}
        else:
            return self.framer(data['Date'], data[self.key])
            
    def data_pruning(self):
        #                   not grouped
        if self.group is False:
            return [(name, self.key_handle(obj.tracker.data)) for name, obj in self.search.items() if len(obj.tracker.data['Date'])>2]
        else:
            groups = []
            for key, val in self.search.items():
                key = key if type(key) == str else key.name
                temp = [self.framer(obj.tracker.data['Date'], obj.tracker.data[self.key]) for obj in val if len(obj.tracker.data['Date'])>2]
                arr = []
                for d in range(len(self.timeframe)):
                    if self.avg:
                        arr.append(sum([t[d] for t in temp if t]) // len(temp))
                    else:
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
                x = len(self.db.printer.name_index) + x if x < 0 else x if x < len(self.db.printer.name_index) else x - len(self.db.printer.name_index) 
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
                
