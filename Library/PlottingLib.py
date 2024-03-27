from printerwatch.Library.Items.Plotting import PlotData as pd
from printerwatch.Library.BaseLib import *

class PlotLib(Lib):
	file = Path(DB_DIR, 'plotcache.json')
	def __init__(self):
		self.item = pd
		self.obj = []
		self.ids = []
		self._load()

	def get(self, search):
		return [obj for obj in self.obj if obj == search]

	def build_cache(self, plib):
		for obj in plib.obj:
			self.obj.append(self.item.build_new(obj))
			self.ids.append(self.obj[-1].ID)
		self._save()

	def _save(self):
		with open(PlotLib.file, 'w') as f:
			f.write(dumps([obj.export() for obj in self.obj]))

	def _import(self):
		with open(PlotLib.file, 'r') as f:
			return loads(f.read())

	def _load(self):
		if exists(PlotLib.file):
			for obj in self._import():
				temp = self.item(**obj)
				self.obj += [temp]
				self.ids += [temp.id]


# Execution Sandbox
if __name__ == '__main__':
	pass


