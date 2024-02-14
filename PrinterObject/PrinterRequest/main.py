from datetime import datetime as dt

from printerwatch.PrinterRequest.BrotherRequest import BrotherReq
from printerwatch.PrinterRequest.DefaultRequest import *
from printerwatch.PrinterRequest.KyoceraRequest import KyoceraReq
#from printerwatch.PrinterObject.main import *

class PrinterRequest(object):
	def __init__(self, ip):
		self.ip = ip
		self.printer = None
		self.response = None
		self.request(ip)
		self.update_tracker()

	def request(self, ip):
		temp = AdvRequest(ip)
		if temp.valid():
			if temp.data['serial_no'] in pLib.name_index:
				self.printer = pLib.get_obj(temp.data['serial_no'])
				if self.printer.ip != ip:
					pLib.update_obj({'serial_no': temp.data['serial_no'], 'ip': ip})
					self.printer = pLib.get_obj(temp.data['serial_no'])
			elif self.unknown_client(temp.data):
				self.printer = pLib.get_obj(temp.data['serial_no'])
				print('add success')
			else:
				print('add failed')
				return None
			i = ('Brother', 'Kyocera').index(temp.data['manufacturer'])
			self.response = (BrotherReq, KyoceraReq)[i](temp.data)
	
	def unknown_client(self, data):
		print(data)
		try:
			serial_no, model, ip = data['serial_no'], data['model'], ip
			pLib.add_new(serial_no, model, ip, **data)
			return True
		except:
			return False
	
	def update_tracker(self):
		if self.response:
			self.printer.update_tracker(**self.response.get_tracker_data())

	def __repr__(self):
		if self.printer is not None and self.response is not None:
			msg = f'printer:\n{str(self.printer)}\nresponse:\n{self.response.data}\ntracker:\n{self.response.tracker_data}\n---------------------------------------\n'
		else:
			msg = f'No Success IP:{self.ip}\n---------------------------------------\n'
		return msg


class RequestDummy(PrinterRequest):
	def __init__(self, ip):
		super().__init__(ip)
		
	def update_tracker(self):
		print(self.response)
		
if __name__ == '__main__':
	pass
