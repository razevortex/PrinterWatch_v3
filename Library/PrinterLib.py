from printerwatch.Library.BaseLib import Lib, DB_DIR, Path, exists
from printerwatch.Library.Items.Printer import Printer

class PrinterLib(Lib):
	file = Path(DB_DIR, 'printer.json')
	cLib, mLib = None, None
	def __init__(self):
		self.item = Printer
		self.obj = []
		self.ids = []
		self._load()

	def _load(self):
		if exists(self.file):
			for obj in self._import():
			    temp = self.item(DB_DIR, PrinterLib.mLib, PrinterLib.cLib, **obj)
			    if not self.get(temp.id):
			        self.obj += [temp]
			        self.ids += [temp.id]


# Execution Sandbox
if __name__ == '__main__':
	pLib = PrinterLib()
	print(pLib)

