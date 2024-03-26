from printerwatch.Library.Items.Base import Obj
from printerwatch.Library.Items.Tracker import PrinterTracker as Tracker

class Printer(Obj):
	__name__ = 'Printer Item'
	mandatory = ('serial_no', 'model')
	propertys = ('id', 'active', 'cart', 'printermodel', 'manufacturer', 'tracker_keys')
	__slots__ = 'serial_no', 'display_name', 'model', 'cartridges', 'ip', 'tracker', 'location', 'contact', 'notes'

	def __init__(self, path, mLib, cLib, **kwargs):
		model = kwargs.get('model')
		kwargs.update({'model': mLib.get(model)})
		super().__init__(**kwargs)
		self.cartridges = [cLib.get(c) for c in (self.cartridges, self.model.cartridges)[self.cartridges == []]]
		self.tracker = Tracker(path, self.serial_no)

	def __eq__(self, other):
		if type(other) == str:
			if other.startswith('-'):
				return not (other[1:].casefold() in str(self))
			else:
				return other.casefold() in str(self)

	def __repr__(self):
		msg = f'{self.__name__} => {self.serial_no}:\n'
		msg += f'	{self.manufacturer} {self.printermodel}\n' 
		msg += '	' + ''.join([f'[{c.color}:{c.id}]' for c in self.cartridges]) + '\n'
		msg += f'{self.tracker}\n'
		for key in ('ip', 'location', 'contact', 'notes'):
			msg += '	' + self.__getattribute__(key) + '\n'
		return msg

	@property
	def tracker_keys(self):
		a = (['B'], ['C', 'Y', 'M'])
		b = (['Prints'], ['ColorPrints'])
		c = (['Copies'], ['ColorCopies'])
		keys = a[0] + b[0] if not self.model.copie else a[0] + b[0] + c[0]
		return ['Date'] + keys if not self.model.color else ['Date'] + keys + a[1] + b[1] if not self.model.copie else ['Date'] + keys + a[1] + b[1] + c[1]

	@property
	def printermodel(self):
		return self.model.name
	
	@property
	def manufacturer(self):
		return self.model.manufacturer
	
	@property
	def cart(self):
		return {cart.color: cart for cart in self.cartridges}

	@property
	def active(self):
		return self.ip != ''
	
	@property
	def id(self):
		return self.serial_no
	
# Execution Sandbox
if __name__ == '__main__':
	pass
