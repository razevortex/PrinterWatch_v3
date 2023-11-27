from imports import *
from snmp_foos import *
from BrotherRequest import Brother
from KyoceraRequest import Kyocera


class PrinterRequest(object):
	def __init__(self, printer_obj):
		self.result = {}
		self.printer = printer_obj
		model = printer_obj.model.name
		self.valid = printer_obj.serial_no == _snmp_get(printer_obj.ip, serial_no_oid[model])
		self.method = {'Brother': Brother, 'Kyocera': Kyocera}[printer_obj.model.manufacturer]

	def get(self):
		if self.valid:
			got = self.method.get()
			if type(got) == dict:
				got['date'] = dt.now()
				self.printer.update_tracker(got)

		else:
			return False
