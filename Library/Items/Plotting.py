from datetime import datetime as dt, timedelta

class PlotData(object):
	__slots__ = 'Prints', 'ColorPrints', 'Copies', 'ColorCopies', 'ID', 'Name', 'SearchStr', 'TrackStart'
	def __init__(self, **kwargs):
		[self.__setattr__(slot, kwargs.get(slot, None)) for slot in self.__slots__]

	def __repr__(self):
		return '\n'.join([f'{slot}: {self.__getattribute__(slot)}' for slot in self.TrackerKeys])

	def __eq__(self, search:str):
		for word in search.split(' '):
			if word.startswith('-') and word[1:].casefold() in self.SearchStr:
				return False
			if not word.startswith('-') and not word.casefold() in self.SearchStr:
				return False
		return True

	@classmethod
	def build_new(cls, obj):
		t = ' '.join([str(obj.__getattribute__(item)).casefold() for item in ('serial_no', 'display_name', 'ip', 'location', 'contact', 'notes', 'printermodel', 'manufacturer')])

		temp = {'ID': obj.id, 'SearchStr': t, 'Name': obj.display_name}
		d = obj.tracker.data
		temp['TrackStart'] = d['Date'][0]
		temp_track = {key: [0 for i in range((dt.now().date() - temp['TrackStart'].date()).days)] for key in d.keys() if key != 'Date'}
		pos = temp['TrackStart']
		a_day = timedelta(days=1)
		print('days:', (dt.now().date() - temp['TrackStart'].date()).days)
		#[print(key, len(temp_track[key])) for key in temp_track.keys()]
		for i in range((dt.now().date() - temp['TrackStart'].date()).days):
			p = [j for j, v in enumerate(d['Date']) if v.date() == pos.date()]
			#print('p =>', p)
			for key in temp_track.keys():
				temp_track[key][i] = sum([d[key][j] for j in p])
			pos += a_day
		temp.update(temp_track)
		temp['TrackStart'] = temp['TrackStart'].date().strftime('%d.%m.%Y') 
		return cls(**temp)

	@property
	def TrackerKeys(self):
		return [slot for slot in ('Prints', 'ColorPrints', 'Copies', 'ColorCopies') if not self.__getattribute__(slot) is None]

	@property
	def AllKeys(self):
		 return self.TrackerKeys + ['ID', 'Name', 'SearchStr', 'TrackStart']

	@property
	def TotalPages(self):
		temp = [self.__getattribute__(slot) for slot in self.__slots__ if self.__getattribute__(slot)]
		return [sum(vals) for vals in zip(*temp)]

	@property
	def Date(self):
		return dt.strptime(self.TrackStart, '%d.%m.%Y').date()

	def export(self):
		return {key: self.__getattribute__(key) for key in self.AllKeys}
		
	def timeframe(self, start, end, steps, keys):
		temp = {key: [] for key in keys if key in self.TrackerKeys}
		end = dt.now().date() if end > dt.now().date() else end
		delta = timedelta(days=steps)
		while start < self.Date:
			[temp[key].append(None) for key in temp.keys()]
			start += delta
		while start + delta < end:
			sli = slice((start - self.Date).days, (start - self.Date).days + steps, None)
			[temp[key].append(sum(self.__getattribute__(key)[sli])) for key in temp.keys()]
			start += delta
		return temp

