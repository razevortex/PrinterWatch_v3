from json import dumps, loads
from datetime import datetime as dt, timedelta
from os import path
from Packages.PrinterObject.StaticVar import *
from Packages.Libs.main import cLib, mLib

class BaseDict(dict):
    KEYS = 'B', 'C', 'Y', 'M', 'Prints', 'ColorPrints', 'Copies', 'ColorCopies', 'Date'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return '<DICT>\n' + ''.join([f'{key} : {val}\n' for key, val in self.items()])
    
    def __missing__(self, key):
        if key in BaseDict.KEYS:
            self[key] = []
            return self[key]
        else:
            return {key: []}


class DataDict(BaseDict):
    """
    This dict stores the value changes over time as a dict(key:list) and has some altered functionalities
    """
    def __str__(self):
        return '<DICT>\n' + ''.join([f'{key} [{len(val)}] : {val}\n' for key, val in self.items()])
    
    def __iadd__(self, other:dict):
        for key, val in [(key, val) for key, val in other.items() if key in BaseDict.KEYS]:
            if type(val) == list:
                self[key] += val
            else:
                self[key] += [val]
        return self
    
    def __add__(self, other):
        if isinstance(other, DataDict):
            arr = self['Date'] + other['Date']
            arr = list(set(arr))
            arr.sort()
            temp = DataDict()
            for date_ in arr:
                temp['Date'] += date_
                a, b = self._get_date(date_), other._get_date(date_)
                for key in [key for key in BaseDict.KEYS if key != 'Date']:
                    temp[key] += sum([_dict.get(key, 0) for _dict in (a, b)])
            return temp
    
    def _get_date(self, date):
        if date in self.get('Date', []):
            return {key: val[self['Date'].index(date)] for key, val in self.items() if key != 'Date'}
        else:
            return {key: 0 for key, val in self.items() if key != 'Date'}
        
    def update(self, **kwargs):
        new = False if (kwargs.get('Date', self['Date'][0]) in self['Date']) else True
        if kwargs.get('Date') not in self['Date'] and not (kwargs.get('Date') is None):
            self['Date'].append(kwargs.get('Date'))
        for key in [key for key in BaseDict.KEYS if key != 'Date' and key in kwargs.keys()]:
            self[key][len(self[key])-1] += kwargs.get(key)
            if new:
                self[key].append(0)
            

# Since the Tracker (except the Date tracker) is to track the value changes over given time but initial will get the
# absolute value there is some preprocessing done by this foo´s
def cart_update(cur, val):
    if type(val) == int and 0 <= val <= 100:
        if cur is None:
            return val, 0
        return val, cur - val if cur >= val else 100 - val + cur
    else:
        return cur, 0


def page_update(cur, val):
    if cur is None:
        return val, 0
    elif type(val) == int and val >= cur:
        return val, val - cur
    else:
        return cur, 0


def date_update(cur, val):
    if isinstance(val, dt):
        return val, val.date()
    else:
        return cur, cur.date()


class CurrentDict(BaseDict):
    """
    This is Dict stores the current values like dict(key, val) also it is preprocessing incoming data to the delta values and passing them on from there
    """
    def update(self, **kwargs) -> dict:
        delta = {}
        for key, val in [(key, val) for key, val in kwargs.items() if key in self.keys()]:
            if self[key] != val:
                if key == 'Date':
                    self[key], delta[key] = date_update(self[key], val)
                elif key in 'BCYM':
                    self[key], delta[key] = cart_update(self[key], val)
                else:
                    self[key], delta[key] = page_update(self[key], val)
        return delta

    def __missing__(self, key):
        self[key] = None
        return self[key]



class PrinterTracker(object):
    """
    The Main Tracker Object contains the Current and Data dict´s handles the save and load updating Cartridge Objects global_stats
    """
    path_template = Path(DB_DIR, '*_tracker.json')
    dt_string_forms = ('%d.%m.%Y', '%d.%m.%Y %H:%M')
    
    def __init__(self, printer, model=''):
        self.file = str(PrinterTracker.path_template).replace('*', printer)
        if path.exists(self.file):
            data, cur = self.load()
            self.data = DataDict(**{key: val for key, val in data.items()})
            self.current = CurrentDict(**{key: val for key, val in cur.items()})
        else:
            self.data = DataDict(**{key: [] for key in mLib.get_tracker_keys(model)})
            self.current = CurrentDict(**{key: None for key in mLib.get_tracker_keys(model)})

    def __repr__(self):
        return f'Tracker:\n{str(self.current)}\n{str(self.data)}\n'
    
    def update(self, dict_obj, carts=()):
        delta = self.current.update(**dict_obj)
        if not (delta is None):
            cLib.update(carts, delta)
            cLib.save()
            if self.data['Date']:
                self.data.update(**delta)
            else:
                self.data += delta

    def save(self):
        with open(self.file, 'w') as f:
            f.write(dumps(self._to_json()))

    def load(self):
        with open(self.file, 'r') as f:
            dict_obj = loads(f.read())
        data, cur = dict_obj['data'], dict_obj['current']
        cur['Date'] = self.dt_from_string(cur['Date'])
        data['Date'] = [self.dt_from_string(d, obj_type='date') for d in data['Date']]
        return data, cur

    def dt_from_string(self, string, obj_type='datetime'):
        return dt.strptime(string, PrinterTracker.dt_string_forms[('date', 'datetime').index(obj_type)])

    def _to_json(self):
        data = {}
        for key, val in self.data.items():
            print(key, val)
            if key == 'Date':
                val = [v.strftime(PrinterTracker.dt_string_forms[0]) for v in val]
            data[key] = val
        cur = {}
        for key, val in self.current.items():
            if key == 'Date' and val is not None:
                val = val.strftime(PrinterTracker.dt_string_forms[1])
            cur[key] = val
        return {'data': data, 'current': cur}
