from Packages.PrinterRequest.imports import sp
from Packages.csv_read import model_ip

def _snmp_walk(ip, oid):
	command = f'snmpwalk -v1 -c public {ip} {oid} mgmt'
	response = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE).communicate()[0]
	try:
		return [tuple(res.split(':')) for res in response.decode('utf-8').split('\n')]
	except:
		return 'NaN'

def _snmp_get(ip, oid):
	command = f'snmpget -v 1 -c public {ip} {oid}'
	response = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE).communicate()[0]
	try:
		response = response.decode('utf-8').split(':')[1]
		return response.replace('"', '').strip()
	except:
		return 'NaN'

# the error procedure is only a placeholder solution
def SNMP_MIB(ip, mib: dict) -> dict:
	got = {key: _snmp_get(ip, val) for key, val in mib.items()}
	for val in got.values():
		if val == 'NaN':
			return {'error': 'NaN'}
	return got


def test_oid(oid):
	result = {}
	for ip, model in model_ip.items():
		if not (model in result.keys()):
			result[model] = [_snmp_get(ip, oid)]
		else:
			result[model].append(_snmp_get(ip, oid))
	[print(f'{key} : {val}') for key, val in result.items()]

if __name__ == '__main__':

	def test(ip, oid='1.3.6.1.2.1'):
		ip = [{"serial_no": "E74552K5J157940", "model": "MFC-9142CDN", "ip": "172.20.10.94", "location": "", "contact": "", "tracker": "E74552K5J157940_tracker.json"},
			  {"serial_no": "E79028F1N485578", "model": "MFC-L3750CDW", "ip": "172.20.10.59", "location": "", "contact": "", "tracker": "E79028F1N485578_tracker.json"},
			  {"serial_no": "E79032E1N463928", "model": "MFC-L3770CDW", "ip": "172.20.20.78", "location": "", "contact": "", "tracker": "E79032E1N463928_tracker.json"},
			  {"serial_no": "E79028J1N561453", "model": "MFC-L3750CDW", "ip": "172.20.10.51", "location": "", "contact": "", "tracker": "E79028J1N561453_tracker.json"},
			  {"serial_no": "E79028J0N197622", "model": "MFC-L3750CDW", "ip": "172.20.22.124", "location": "", "contact": "", "tracker": "E79028J0N197622_tracker.json"},
			  {"serial_no": "E79028D1N429426", "model": "MFC-L3750CDW", "ip": "192.168.201.70", "location": "", "contact": "", "tracker": "E79028D1N429426_tracker.json"},
			  {"serial_no": "E79028K2N115210", "model": "MFC-L3750CDW", "ip": "172.20.20.82", "location": "", "contact": "", "tracker": "E79028K2N115210_tracker.json"}][ip]['ip']
		print(_snmp_walk(ip, oid))

	def write_txt(name, text):
		with open(name, 'w') as f:
			f.write(text)

	def get_walks():
		for ip, model in model_ip.items():
			name = f'/home/razevortex/PycharmProjects/PrinterWatch_v3/snmp_walks/{model}_{ip}.txt'
			text = ''.join([f'{line}\n' for line in _snmp_walk(ip, '1.3.6.1.2.1')])
			write_txt(name, text)


	def get_this_walk(ip):
		name = f'/home/razevortex/PycharmProjects/PrinterWatch_v3/snmp_walks/{ip}.txt'
		text = ''.join([f'{line}\n' for line in _snmp_walk(ip, '1.3.6.1')])
		write_txt(name, text)

	get_this_walk('172.20.10.113')