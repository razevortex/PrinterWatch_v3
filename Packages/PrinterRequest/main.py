import time
from datetime import datetime as dt
from Packages.PrinterRequest.snmp_foos import *
from Packages.csv_read import model_ip
from Packages.Libs.main import mLib, cLib
from Packages.PrinterRequest.BrotherRequest import BrotherReq
from Packages.PrinterRequest.KyoceraRequest import KyoceraReq
from Packages.PrinterRequest.DefaultRequest import *
from time import perf_counter_ns as nsec


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
			else:
				pLib.add_new(**temp.data) #temp.data['serial_no'], temp.data['model'], **temp.data)
				self.printer = pLib.get_obj(temp.data['serial_no'])
			i = ('Brother', 'Kyocera').index(temp.data['manufacturer'])
			self.response = (BrotherReq, KyoceraReq)[i](temp.data)

	def update_tracker(self):
		if self.response:
			t_dict = self.response.tracker_data
			t_dict['Date'] = dt.now()
			self.printer.update_tracker(**self.response.tracker_data)

	def __repr__(self):
		if self.printer is not None and self.response is not None:
			msg = f'printer:\n{str(self.printer)}\nresponse:\n{self.response.data}\ntracker:\n{self.response.tracker_data}\n---------------------------------------\n'
		else:
			msg = f'No Success IP:{self.ip}\n---------------------------------------\n'
		return msg


if __name__ == '__main__':
	for key in model_ip.keys():
		got = PrinterRequest(key)
		print(got)