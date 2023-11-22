from Requests.snmp_request import _snmp_walk, _snmp_get
from Requests.StaticVars import *


class Kyocera(object):
	def __init__(self, obj):
		self.ip = obj.ip
		model = obj.model
		self.toner_max, self.toner_fill = kyocera_toner_color if model.color else kyocera_toner_bw
		if model.color:
			self.pages = taskalfa_pages if 'TASK' in model.name else ecosys_pages
		else:
			self.pages = {key: val for key, val in kyocera_pages.items() if key in model.get_tracker_keys()}

	def _get_toner(self):
		max_ = {key: _snmp_get(self.ip, val) for key, val in self.toner_max.items()}
		fill_ = {key: _snmp_get(self.ip, val) for key, val in self.toner_fill.items()}
		return {key: int(100 / int(max_[key]) * int(fill_[key])) for key in max_.keys() if key in fill_.keys()}

	def _get_pages(self):
		print(self.pages.items())
		return {key: int(_snmp_get(self.ip, val)) for key, val in self.pages.items()}

	def get(self):
		t_dict = self._get_toner()
		print(t_dict)
		t_dict.update(self._get_pages())
		return t_dict
