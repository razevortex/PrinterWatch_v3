class Obj(object):
	mandatory = ()
	propertys = ()
	__slots__ = 'static'
	def __init__(self, **kwargs):
		self.static = []
		[self.__setattr__(key, val) for key, val in kwargs.items() if key in self.__slots__]
		self.__setattr__('static', self.mandatory)

	def __str__(self):
		msg = ''
		for key in self.__slots__ + self.propertys:
			if type(self.__getattribute__(key)) not in (list, bool):
				msg += str(self.__getattribute__(key)) + '\n'
			elif type(self.__getattribute__(key)) == bool:
				msg += key + '\n'
			else:
				msg += ' '.join([str(obj) for obj in self.__getattribute__(key)]) + '\n'
		return msg.casefold()
	
	def __getattribute__(self, item):
		if item == 'static':
			try:
				return super().__getattribute__(item)
			except:
				return ()
		else:
			return super().__getattribute__(item)

	def __setattr__(self, key, val):
		if not (key in self.static):
			super().__setattr__(key, val)

	def update_attr(self, **kwargs):
		[self.__setattr__(key, val) for key, val in kwargs.items() if key in self.__slots__]
		
	@classmethod
	def load(cls, **kwargs):
		for key in cls.mandatory:
			if key not in kwargs.keys():
				return None
		return cls(**kwargs)
		
	@property
	def id(self):
		return '' # will be individual set for each obj
	
	def export(self):
		temp = {'id': self.id}
		for slot in self.__slots__:
			if slot != 'static':
				if isinstance(self.__getattribute__(slot), Base):
					temp[slot] = self.__getattribute__(slot).id
				elif type(self.__getattribute__(slot)) is list:
					temp[slot] = [obj if not isinstance(obj, Base) else obj.id for obj in self.__getattribute__(slot)]
				else:
					temp[slot] = str(self.__getattribute__(slot))
		return temp


# Execution Sandbox
if __name__ == '__main__':
	pass
