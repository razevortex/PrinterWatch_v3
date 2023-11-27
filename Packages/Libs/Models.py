from imports import *


class _PrinterModel(object):
	"""
	The _PrinterModel is a Container of data that are immutable but is essential for the creation of the
	mutable Tracking objects of the PrinterObject
	"""
	__slots__ = ('name', 'manufacturer', 'cartridges', 'color', 'copie', 'locked')

	def __init__(self, **kwargs):
		super().__init__()
		[self.__setattr__(key, val) for key, val in kwargs.items()]
		self.locked = True
	
	def __setattr__(self, key, val):
		try:
			if self.__getattribute__('locked'):
				pass
		except:
			super().__setattr__(key, val)

	def __str__(self):
		temp = f'{self.manufacturer}\n{self.name}\nCart-Type:{self.cartridges}\nFeatures: '
		if self.color:
			temp += 'Color, '
		if self.copie:
			temp += 'Copie'
		return temp
	
	def _export(self):
		return {slot: self._export_sub(slot) for slot in self.__slots__}
	
	def _export_sub(self, slot):
		if slot == 'cartridges':
			return list(self.__getattribute__(slot))
		else:
			return self.__getattribute__(slot)
	
	def get_tracker_keys(self):
		toner_keys = (['B'], ['C', 'Y', 'M'])
		print_keys = (['Prints'], ['ColorPrints'])
		copie_keys = (['Copies'], ['ColorCopies'])
		keys = toner_keys[0] + print_keys[0] if not self.copie else toner_keys[0] + print_keys[0] + copie_keys[0]
		if self.color:
			keys += toner_keys[1] + print_keys[1] if not self.copie else toner_keys[1] + print_keys[1] + copie_keys[1]
		return ['Date'] + keys


class ModelLib(object):
	obj = []
	name_index = []
	file = DB_DIR + '\modelslib.json'
	
	def __init__(self):
		if path.exists(ModelLib.file):
			self.load_(self._import())
	
	def __repr__(self):
		return ''.join([f'{typ.name}:>\n{str(typ)}\n\n' for typ in ModelLib.obj])
	
	# Build New Rework
	
	def build_new(self, name: str = '', manufacturer: str = '', cartridges: tuple = (), color: bool = False, copie: bool = False):
		if name not in ModelLib.name_index:
			kwargs = {'name': name, 'manufacturer': manufacturer, 'cartridges': cartridges, 'color': color, 'copie': copie}
			model = _PrinterModel(**kwargs)
			ModelLib.obj.append(model)
			ModelLib.name_index.append(model.name)
		self.save_(self._export())
	
	def save_(self, port: list[dict]):
		if ModelLib.file is not None:
			with open(ModelLib.file, 'w') as f:
				f.write(dumps(port))
	
	def _export(self):
		return [obj._export() for obj in ModelLib.obj]
	
	def _import(self):
		if ModelLib.file is not None:
			with open(ModelLib.file, 'r') as f:
				return loads(f.read())
	
	def load_(self, port: list[dict]):
		for obj in port:
			if obj['name'] not in ModelLib.name_index:
				ModelLib.obj += [_PrinterModel(**obj)]
		ModelLib.name_index += [obj.name for obj in ModelLib.obj]
	
	def get(self, model):
		if model in ModelLib.name_index:
			return ModelLib.obj[ModelLib.name_index.index(model)]

	def get_tracker_keys(self, model):
		return self.get(model).get_tracker_keys()
