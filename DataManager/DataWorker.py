from printerwatch.DataManager.DataSet import DataBase
from datetime import datetime as dt, date, timedelta
from json import dumps

db = DataBase()


class responseObj(object):
    def __init__(self, keylist, name, default={}):
        self._keylist, self._name = keylist, name
        if keylist != '*':
            [self.__setattr__(key, val) for key, val in default.items() if key in keylist]
        else:
            [self.__setattr__(key, val) for key, val in default.items()]

    def get_(self, req):
        [self.__setattr__(key, val) for key, val in req.items() if (self._keylist == '*') or key in self._keylist]
    
    def get_return(self):
        return {key: val for key, val in self.__dict__.items() if (self._keylist == '*') or key in self._keylist} 


class ResponseHandler(object):
    def __init__(self, view, *args):
        [self.__setattr__(arg.name, arg) for arg in args]



class DataObject(object):
    def __init__(self, past='2022-01-01', befor=None, interval=2, search='*', key='Prints', incr=True, group=False):
        befor = dt.now().date() if befor is None else dt.strptime(befor, '%Y-%m-%d').date()
        self.timeframe = self.timearr((dt.strptime(past, '%Y-%m-%d').date(), befor), timedelta(days=int(interval)))
        self.incr = incr
        self.group = group
        self.search = search
        self.key = key

    def __repr__(self):
        return '\n'.join([f'{key}: {val}' for key, val in self.__dict__.items()])

    def merge_keys(self, merge_name, keys='*'):
        temp = {}
        for key, data in self.data.items():
            temp[merge_name] = [sum(zipped) for zipped in zip([v for k, v in data.items() if k in keys or keys == '*'])]

    def plot_builder(self):
        ''' does call data_pruning ''' 
        temp = [{'label': name, 'data': data} for name, data in self.data_pruning()]
        return {'labels': [date.strftime('%d.%m.%Y') for date in self.timeframe], 'datasets': temp}


    def data_pruning(self):
        #                   not grouped
        if self.group is False:
            return [(obj.display_name, self.framer(obj.tracker.data['Date'], obj.tracker.data[self.key])) for obj in self.search_filter() if obj.tracker.data['Date']]
        #                   grouped
        else:
            temp = [self.framer(obj.tracker.data['Date'], obj.tracker.data[self.key]) for obj in self.search_filter() if obj.tracker.data['Date']]
            arr = []
            for d in range(len(self.timeframe)):
                arr.append(sum([t[d] for t in temp]))
            return ((self.search, arr),)

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
        if self.search is None:
            return db.printer
        else:
            return db.printer.get_search(self.search)


class PrinterView(object):
    def __init__(self, **kwargs):
        #self.printerkeys = ['serial_no'
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
            db.printer.update_obj(dict(kwargs))
        print(' Data Worker Update End! ')
        
    def _selecting(self, **kwargs):
        # get index of the obj 
        if kwargs == {}:
            x = self.x   # if no request set 0
        else:
            if kwargs.get('select', False) != kwargs.get('serial_no', False):   # if select dropdown was changed use selected objs index
                x = db.printer.name_index.index(kwargs.get('select'))
            else:
                x = db.printer.name_index.index(kwargs.get('serial_no'))  # else use the previous objs index
                if kwargs.get('next', False):   # and in/decrement it if next or back was used
                    x += 1
                elif kwargs.get('back', False):
                    x += -1 
        for i, key in enumerate(['back', 'selected', 'next']): 
                if key == 'selected':
                    self.context.update(db.printer.obj[x + i - 1].get_context_obj())
                    self.context[key] = {'serial_no': db.printer.obj[x + i - 1].serial_no, 'display_name': db.printer.obj[x + i - 1].display_name}
                else:
                    self.context[key] = db.printer.obj[x + i - 1].serial_no
        temp = {'serial_no': db.printer.obj[x + i - 1].serial_no, 'display_name': db.printer.obj[x + i - 1].display_name}
        self.context['selectable'] = [temp] + [{'serial_no': obj.serial_no, 'display_name': obj.display_name} for obj in db.printer.obj]
        self.x = x
    
    def _cart_state(self):
        state = db.printer.obj[self.x].tracker.current
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
    