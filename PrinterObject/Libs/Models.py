from json import dumps, loads
from os import path
from pathlib import Path
from .StaticVar import DB_DIR
from printerwatch.GlobalClasses import LockedSlots


class _PrinterModel(LockedSlots):
	"""
	The _PrinterModel is a Container of data that are immutable but is essential for the creation of the
	mutable Tracking objects of the PrinterObject
	"""
	__slots__ = ('name', 'manufacturer', 'cartridges', 'color', 'copie')

	def __init__(self, **kwargs):
		[self.__setattr__(key, val) for key, val in kwargs.items()]
		super().__init__('name', 'manufacturer', 'cartridges', 'color', 'copie')
	

	def __str__(self):
		temp = f'{self.manufacturer} {self.name}\nCart-Type:{self.cartridges}\nFeatures: '
		if self.color:
			temp += 'Color, '
		if self.copie:
			temp += 'Copie'
		return temp
	
	def export(self):
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
	file = Path(DB_DIR, 'modelslib.json')
	
	def __init__(self):
		self.load()
	
	def __repr__(self):
	    return ''.join([f'{typ.name}:>\n{str(typ)}\n\n' for typ in ModelLib.obj])

	# Build New Rework
	def build_new(self, name: str = '', manufacturer: str = '', cartridges: tuple = (), color: bool = False, copie: bool = False):
	    cartridges = [f'{manufacturer} {c}' for c in cartridges]
	    if name not in self.name_index:
	        kwargs = {'name': name, 'manufacturer': manufacturer, 'cartridges': cartridges, 'color': color, 'copie': copie}
	        model = _PrinterModel(**kwargs)
	        ModelLib.obj.append(model)
	        ModelLib.name_index.append(model.name)
	    self.save()
	
	def save(self):
		temp = self._import()
		try:
			with open(ModelLib.file, 'w') as f:
				f.write(dumps(self._export()))
		except:
			print('An Error Occured file wasnt saved')
			with open(ModelLib.file, 'w') as f:
				f.write(dumps(temp))

	def _export(self):
		return [obj.export() for obj in ModelLib.obj]
	
	def _import(self):
		with open(ModelLib.file, 'r') as f:
			return loads(f.read())
	
	def load(self):
		if path.exists(ModelLib.file):
			for obj in self._import():
				if obj['name'] not in ModelLib.name_index:
					ModelLib.obj += [_PrinterModel(**obj)]
			ModelLib.name_index += [obj.name for obj in ModelLib.obj]
	
	def get(self, model):
		if model in ModelLib.name_index:
			return ModelLib.obj[ModelLib.name_index.index(model)]
		if model == '*':
			return ModelLib.obj

	def get_filtered_set(self, **kwargs):
		arr = []
		for obj in ModelLib.obj:
			add = True
			for key, val in [(key, val) for key, val in kwargs.items() if key in ('name', 'manufacturer', 'cartridges', 'color', 'copie')]:
				if add:
					add = (val == obj.__getattribute__(key)) if key != 'cartridges' else (val in obj.__getattribute__(key))
			if add:
				arr.append(obj)
		return arr

	def get_tracker_keys(self, model):
		return self.get(model).get_tracker_keys()
