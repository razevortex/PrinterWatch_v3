from json import dumps


class LineData(dict):
	def __init__(self):
		super().__init__({'labels': [], 'datasets':[]})

	def setup(self, labels:list):
		self['labels'] = labels

	def add_dataset(self, name, data, borderColor=None, backgroundColor=None):
		if len(data) == len(self['labels']):
			temp = {'label': name, 'data': data}
			if borderColor is not None:
				temp.update({'borderColor': borderColor})
			if backgroundColor is not None:
				temp.update({'backgroundColor': backgroundColor})
			self['datasets'].append(temp)

	def create(self):
		return {key: val for key, val in self.items()}


class BarData(dict):
	def __init__(self):
		self.key_set = {}
		super().__init__({'labels': [], 'datasets':[]})

	def setup(self, key_set:list):
		for key in key_set:
			self.key_set[key] = []

	def add_dataset(self, name:str, data:dict):
		'''
			name: str
			data: dict {key: int, key: int, ...}
		'''
		self['labels'].append(name)
		for key in self.key_set.keys():
			self.key_set[key].append(data.get(key, 0))

	def create(self):
		self['datasets'] = [{'label': key, 'data': val} for key, val in self.key_set.items()]
		return {key: val for key, val in self.items()}


class ChartObject(dict):
	data_class = {'line': LineData(), 'bar': BarData()}
	def __init__(self, _type):
		super().__init__({"type": _type, "data": self.set_data(_type)})

	def set_data(self, _type):
		return ChartObject.data_class[_type]

	def dumped(self):
		return {key: dumps(val.create()) for key, val in self.items()}

	@classmethod
	def setup(cls, type, setup):
		temp = cls(type)
		temp.setup(setup)
		return temp
