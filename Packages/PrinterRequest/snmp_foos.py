from imports import sp

def _snmp_walk(ip, oid):
	command = f'snmpwalk -v1 -c public {ip} {oid} mgmt'
	response = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE).communicate()[0]
	try:
		return [[res.split(':')] for res in response.decode('utf-8').split('\n')]
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
