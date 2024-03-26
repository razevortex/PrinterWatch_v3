from datetime import datetime as dt
from pathlib import Path
from os import path
from json import loads, dumps
from printerwatch.GlobalClasses import create_file as cfile

class BaseDict(dict):
	KEYS = 'B', 'C', 'Y', 'M', 'Prints', 'ColorPrints', 'Copies', 'ColorCopies', 'Date'
	
	def __init__(self, **kwargs):
		kwargs = self._typeing(**kwargs)
		super().__init__(**kwargs)
	
	def _typeing(self, **kwargs):
		for key, val in kwargs.items():
			if key != 'Date':
				if type(val) == str:
					try:
						kwargs[key] = int(val)
					except:
						kwargs[key] = None
		return kwargs
	
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
	
	def __iadd__(self, other: dict):
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
				temp += {'Date': date_}
				a, b = self._get_date(date_), other._get_date(date_)
				for key in [key for key in BaseDict.KEYS if key != 'Date']:
					temp += {key: sum([_dict.get(key, 0) for _dict in (a, b)])}
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
			self[key][len(self[key]) - 1] += kwargs.get(key)
			if new:
				self[key].append(0)
	
	def _of_key(self, keys='*'):
		if keys == '*':
			return self
		else:
			return DataDict(**{key: val for key, val in self.items() if key in keys})
	
	
    def _get_slice(self, a, b):
        start, end = None, None
        for i, d in enumerate(self['Date'])
            if start is None:
                if d >= b:
                    return False
                elif d >= a:
                    start = i
            if not start is None and end is None:
                if d > b:
                    return slice(start, i -1, None)
        return slice(start, None, None)

    def _cut_frame(self, a, b, keys='*', key_merged=False):
        keys = keys + ['Date']
        keys = [key for key in self.keys() if key in keys]
        sli = self.get_slice(a, b)
        if not sli is None:
            if key_merged:
                m = [sum(val) for val in zip(*[self[key][sli] for key in keys if key != 'Date'])]
                return self['Date'][sli], m
            else:
                return {key: self[key][sli] for key in keys]}

    def frame_sum(self, i, cut, temp, frame):
        for key in temp.keys():
            if key != 'Date':
                frame[key][i] = sum(temp[key][:cut])
                temp[key] = temp[key][cut:]
            else:
                temp[key] = temp[key][cut:]
        return frame, temp

    def framed(self, timeframe, keys='*'):
        keys = self.keys() if keys == '*' else keys
        temp = self._cut_frame(timeframe[0], timeframe[-1], keys=keys)
        frame = {key: [0 for _ in range(len(timeframe))] for key in keys}
        for i, t in enumerate(timeframe[1:]):
            for cut in range(len(temp))
                if temp['Date'][cut] > t:
                    frame, temp = self.frame_sum(i, cut-1, temp, frame)


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
            if key != 'Date':
                if key in 'BCYM':
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
    ext = '*_tracker.json'
    dt_string_forms = ('%d.%m.%Y', '%d.%m.%Y %H:%M')
    
    def __init__(self, _path, printer):
        self.name = printer + '_tracker'
        self.file = Path(_path, PrinterTracker.ext.replace('*', printer))
        if path.exists(self.file):
            data, cur = self.load()
            self.data = DataDict(**{key: val for key, val in data.items()})
            self.current = CurrentDict(**{key: val for key, val in cur.items()})
        with open(self.file, 'w') as f:
            f.write(dumps(self._to_json()))
       
    def __repr__(self):
        return f'Tracker:\n{str(self.current)}\n{str(self.data)}\n'

    @property
    def meta(self):
        if len(self.data['Date']) < 1:
            return len(self.data['Date']), None, None
        else:
            return len(self.data['Date']), self.data['Date'][0], self.data['Date'][-1]

    def sub_data(self, amount=None, past=None, befor=None, keys='*'):
        if amount is None:
            amount = 2
        if self.meta[0] < amount:
            return False
        return self.data._of_timeframe(past, befor, keys=keys)

    def update(self, dict_obj, carts=()):
        print('update')
        if not (self.current['Date'] is None):
            if (dict_obj['Date'] <= self.current['Date']):
                return
        print(self.data)
        delta = self.current.update(**dict_obj)
        print(delta)
        if not (delta is None):
            cLib.update(carts, delta)
            cLib.save()
            if self.data['Date']:
                self.data.update(**delta)
            else:
                self.data += delta
        print(self.data)
        print('end update')

    def save(self):
        if not path.exists(self.file):
            cfile.lib(self.name)
        with open(self.file, 'w') as f:
            f.write(dumps(self._to_json()))

    def load(self):
        with open(self.file, 'r') as f:
            dict_obj = loads(f.read())
        data, cur = dict_obj['data'], dict_obj['current']
        data = self.data_fix(data, cur)
        cur['Date'] = self.dt_from_string(cur['Date'])
        data['Date'] = [self.dt_from_string(d, obj_type='date') for d in data['Date']]
        return data, cur

    def data_fix(self, data, cur):
        dates = []
        for d in data['Date']:
            if d not in dates:
                dates.append(d)
        for key in data.keys():
            if key != 'Date':
                print(cur[key], sum(data[key]))

        if len(set([len(v) for v in data.values()])) != 1:
            [print(key, len(val)) for key, val in data.items()]
            t_data = {key: [0 for _ in range(len(dates))] for key in data.keys() if key != 'Date'}
            for k, l in [(k, len(v)) for k, v in data.items() if k != 'Date']:
                if len(dates) < l:
                    for i, d in enumerate(dates):
                        for j in range(len(data[k])):
                            if data['Date'][j] == d:
                                t_data[k][i] += data[k][j]

        else:
            t_data = {key: [0 for _ in range(len(dates))] for key in data.keys() if key != 'Date'}
            for d in data['Date']:
                if d not in dates:
                    dates.append(d)
            if len(dates) != len(data['Date']):
                for i, d in enumerate(dates):
                    for j in range(len(data['Date'])):
                        if data['Date'][j] == d:
                            for key in t_data.keys():
                                t_data[key][i] += data[key][j]
        t_data['Date'] = dates
        [print(key, len(val), val) for key, val in t_data.items()]
        return t_data
                        
                


    def dt_from_string(self, string, obj_type='datetime'):
        return dt.strptime(string, PrinterTracker.dt_string_forms[('date', 'datetime').index(obj_type)])

    def _to_json(self):
        data = {}
        for key, val in self.data.items():
            if key == 'Date':
                val = [v.strftime(PrinterTracker.dt_string_forms[0]) for v in val]
            data[key] = val
        cur = {}
        for key, val in self.current.items():
            if key == 'Date' and val is not None:
                val = val.strftime(PrinterTracker.dt_string_forms[1])
            cur[key] = val
        return {'data': data, 'current': cur}
