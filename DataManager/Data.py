from json import dumps, loads
import os
from datetime import timedelta, datetime as dt, date
from printerwatch.Library.DataBase import cLib, mLib, pLib, DB
from printerwatch.Library.PlottingLib import PlotLib

class DataProcessing(DB):
	cachefile = 'db.json'

	def __init__(self):
		super().__init__()
		self.cache = PlotLib()

	def build_cache(self):
		self.cache.build_cache(self.printer)

	def reload(self):
		self.cart, self.model = cLib(), mLib()
		pLib.cLib, pLib.mLib = self.cart, self.model
		self.printer = pLib()

	def print_(self):
		print(self.cartridges)
		print(self.printer_models)
		print(self.printer)

	def merged_tracker_data(self, search='*'):
		temp = None
		for obj in self.printer.get_search(search, result='tracker'):
			try:
				if temp is None:
					temp = obj.data.time_prune()
				else:
					temp = temp + obj.data.time_prune()
			except:
					print('err => merged_tracker_data')
		return temp

	def get_tracker_sets(self, search='*', min_data=10):
		temp = []
		objs = [obj for obj in self.printer.get_search(search) if len(obj.tracker.data['Date']) > min_data]
		[temp.extend(obj.tracker.data['Date']) for obj in objs]
		dates = list(set(temp))
		dates.sort()
		return dates, objs

	def merged_time_frames(self, objs, key_, dates):
		datasets = []
		for obj in objs:
			data = []
			for start, end in dates:
				val = obj.tracker.data._of_timeframe(start, end, keys=(key_, ))
				if val:
					val = sum(val[key_])
				else:
					val = 0
				data.append(val)
			datasets.append({'label': obj.display_name, 'data': data})
		return {'labels': [date[0].strftime('%d.%m.%Y') for date in dates], 'datasets': datasets}

	def make_time_frames(self, dates, timeframe):
		frame_start, frame_end = dates[0], dates[0] + timeframe
		temp = [(frame_start, frame_end)]
		while frame_end < dates[-1]:
			frame_start, frame_end = frame_end, frame_end + timeframe
			temp += [(frame_start, frame_end)]
		return temp

	def generate_plot(self, key, search='*', min_data=10, timeframe=None):
		dates, objs = self.get_tracker_sets(search=search, min_data=min_data)
		if timeframe is not None:
			dates = self.make_time_frames(dates, timeframe)
			return self.merged_time_frames(objs, key, dates)
		datasets = []
		for obj in objs:
			data = [0] * len(dates)
			for date, val in zip(obj.tracker.data['Date'], obj.tracker.data[key]):
				data[dates.index(date)] = val
			datasets.append({'label': obj.display_name, 'data': data})
		return {'labels': [date.strftime('%d.%m.%Y') for date in dates], 'datasets': datasets}

	def __repr__(self):
		msg = f'Cartridges[{len(self.cartridges.name_index)}]: {self.cartridges.name_index}\n'
		msg += f'Models[{len(self.printer_models.name_index)}]: {self.printer_models.name_index}\n'
		msg += f'Printer[{len(self.printer.name_index)}]: {self.printer.name_index}\n'
		return msg

	def get_overview_table(self, keys=('display_name', 'model', 'ip', 'cartridges')):
		arr = []
		for obj in self.printer.obj:
			arr.append({key: obj.export()[key] for key in keys})
		return dumps(list(keys)), dumps(arr)


	def plot_builder(self, key, mods, search=None, timeframe=None, interval=2):
		if not timeframe is None:
			tarr = self.timearr(timeframe, interval)
			temp = [{'label': name, 'data': data} for name, data in self.data_pruning(key, search=search, timearr=tarr)]
			return {'labels': [date.strftime('%d.%m.%Y') for date in tarr], 'datasets': self.apply_mods(temp, mods)}
			

	def apply_mods(self, data, mods):
		[print(d) for d in data]
		if mods[0] == mods[1] == 0:
			return data
		if mods[0]:
			for j in range(len(data)):
				name, d = data[j]
				data[j] = name, [sum(d[0:i]) for i in range(len(d))]
		if mods[1]:
			data = data[:][1]
			return 'group', [sum(all_d) for all_d in zip(data[:])]
		return data
		

	def data_pruning(self, key, search=None, timearr=None):
		return [(obj.display_name, self.framer(obj.tracker.data['Date'], obj.tracker.data[key], timearr)) for obj in self.search_filter(search)]


	def framer(self, date, vals, timearr):
		if date[0].date() > timearr[-1]:
			return False
		i, temp, arr = 0, 0, []
		for t in range(len(timearr)):
			while i < len(vals) and date[i].date() < timearr[t]:
				if t > 0:
					temp += vals[i]
				i += 1
			arr += [temp]
			temp = 0
		return arr

	def timearr(self, timeframe, interval):
		t = [dt.strptime(t, "%Y-%m-%d").date() for t in timeframe]
		timearr = []
		while t[0] < t[1]:
			 timearr += [t[0]]
			 t[0] += timedelta(days=interval)
		return timearr

	def lib_by_key(self, key):
		return {'p': self.printer, 'm': self.printer_models, 'c': self.cartridges}[key]

	def get_search_attr(self, attr:str, lib_='p'):
		t_dict = {}
		for obj in self.lib_by_key(lib_).obj:
			if obj.__getattribute__(attr) in t_dict.keys():
				t_dict[obj.__getattribute__(attr)].append(obj)
			else:
				t_dict[obj.__getattribute__(attr)] = [obj]
		return t_dict

	def get_search_groups(self, search, lib_='p'):
		lib = self.lib_by_key(lib_)
		t_dict = {key: lib.get_search(key) for key in [s.strip() for s in search.split(';')]}
		return t_dict
		
	def get_search_clients(self, search, lib_='p'):
		lib = self.lib_by_key(lib_)
		temp = []
		[temp.extend(lib.get_search(key)) for key in [s.strip() for s in search.split(';')]]
		return {obj.id if lib_ == 'c' else obj.display_name: obj for obj in temp}


class Flags(object):
	__slots__ = 'incr', 'avg', 'group_cli', 'group_key'
	def __init__(self, **kwargs):
		[self.__setattr__(slot, kwargs.get(slot, False)) for slot in self.__slots__]


class handle_request(object):
	def __init__(self, past='2022-01-01', befor=None, interval=2, search='*', key='Prints', incr=False, group_cli=False, group_key=False, avg=False):
		
		self.flag = Flags(**{'incr': incr, 'avg': avg, 'group_cli': group_cli, 'group_key': group_key})
		befor = dt.now().date() if befor is None else dt.strptime(befor, '%Y-%m-%d').date()
		self.timeframe = self.timearr((dt.strptime(past, '%Y-%m-%d').date(), befor), timedelta(days=int(interval)))
		self.key = self._get_key_groups(key)
		self.search = self._search_code(search)

	def _search_code(self, string):
		lib = 'p' if 'cart' not in self.key.casefold() else 'c'
		if not self.group:
			return DataProcessing().get_search_clients(string, lib_=lib)
		else:
			if string.startswith('!'):
				return DataProcessing().get_search_attr(string[1:], lib_=lib)   
			else:
				return DataProcessing().get_search_groups(string, lib_=lib)

	def _get_key_groups(self, key):
		keys = ['Prints', 'Copies'], ['ColorPrints', 'ColorCopies']
		return {'TotalGroup': keys[0] + keys[1], 'ColorGroup': keys[1], 'NonColorGroup': keys[0]}.get(key, (key, ))


	def key_handle(self, data):
		temp = {k: self.framer(data['Date'], data[k]) for k in self.key if k in data.keys()} 
		if self.flag.group_key:
			return {key: sum([temp[key][î] for key in temp.key()]) for i in range(len(temp[key[0]]))}
		else:
			return {key: sum(val) // len(val) for key, val in temp.items() if temp.get(key, False)}
		return self.framer(data['Date'], data[self.key[0]])


	def plot_builder(self):
		''' main function called after init '''
		''' does call data_pruning ''' 
		if not 'Carts' in self.key:
		
			temp = [{'label': name, 'data': data} for name, data in self.data_pruning()]
			if not self.flag.group_key:
				return {'data': dumps({'labels': [date.strftime('%d.%m.%Y') for date in self.timeframe], 
					'datasets': temp}), 'type': dumps('line')}
			else:
				data = {'labels': [obj['label'] for obj in temp], 'datasets': []}
				for key in self._get_key_groups():
					datasets = {'label': key, 'data': []}
					for obj in temp:
						pass
					
		else:
			temp = self.cart_data()
			return {'data': dumps({'labels': temp['label'], 'datasets': [{'label': 'Cart', 'data': temp['data']}]}), 'type': dumps('bar')}

	def data_pruning(self):
		#				   not grouped
		if self.flag.group_cli is False:
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



	def framer(self, date, vals, timearr):
		if date[0].date() > self.timeframe[-1]:
			return False
		i, temp, arr = 0, 0, []
		for t in range(len(self.timeframe)):
			while i < len(vals) and date[i].date() < self.timeframe[t]:
				if t > 0:
					temp += vals[i]
				i += 1
			arr += [temp]
			temp = 0 if self.flag.incr is not True else temp
		return arr

	def timearr(self, timeframe, interval):
		t = [dt.strptime(t, "%Y-%m-%d").date() for t in timeframe]
		timearr = []
		while t[0] < t[1]:
			 timearr += [t[0]]
			 t[0] += timedelta(days=interval)
		return timearr

	  
if __name__ == '__main__':
	db = DataBase()
	
