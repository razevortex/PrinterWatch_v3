from printerwatch.Library.Items.Base import Obj

class Model(Obj):
	mandatory = ('name', 'manufacturer', 'cartridges', 'color', 'copie')
	propertys = ('id', )
	__slots__ = 'name', 'manufacturer', 'cartridges', 'color', 'copie'
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	@property
	def id(self):
		return f'{self.name}'

# Declarations n Definitions

# Execution Sandbox
if __name__ == '__main__':
	pass
