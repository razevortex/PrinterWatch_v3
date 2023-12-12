from Packages.PrinterRequest.snmp_foos import _snmp_get
from Packages.PrinterRequest.imports import *
from Packages.csv_read import model_ip
from Packages.PrinterRequest.snmp_foos import *
from Packages.PrinterRequest.StaticVar import model_oid, model_dict
from Packages.PrinterObject.main import pLib
from Packages.Libs.main import *

manufacturer = list(set([m.manufacturer for m in mLib.get('*')]))


class BaseRequest(object):
    def __init__(self, ip):
        self.data = {'ip': ip}
        self.manufacturer = [{'model': '1.3.6.1.2.1.43.5.1.1.16.1', 'serial_no': '1.3.6.1.2.1.43.5.1.1.17.1'},
                             {'model': '1.3.6.1.2.1.25.3.2.1.3.1', 'serial_no': '1.3.6.1.2.1.43.5.1.1.17.1'}]
        self.mandatory = 'ip', 'serial_no', 'model', 'manufacturer'
        self._request()

    def valid(self):
        for key in self.mandatory:
            val = self.data.get(key, 'nan')
            if val == '' or val.casefold() == 'nan'.casefold():
                return False
        return True

    def _request(self, oids=False):
        got = _snmp_get(self.data['ip'], '1.3.6.1.2.1.1.1.0')
        for i, manufacturer in enumerate(('Kyocera', 'Brother')):
            if manufacturer.casefold() in got.casefold():
                self.data['manufacturer'] = manufacturer
                oids = self.manufacturer[i]
        if self.data.get('manufacturer', False) and oids:
            for key, val in oids.items():
                got = _snmp_get(self.data['ip'], val)
                if got != 'NaN':
                    if key == 'model':
                        for model in mLib.name_index:
                            if model.casefold() in got.casefold():
                                self.data[key] = model
                    if key == 'serial_no':
                        self.data[key] = got
                else:
                    return False
            return True
        else:
            return False


class AdvRequest(BaseRequest):
    def __init__(self, ip):
        super().__init__(ip)
        if self.valid():
            for model, oid in zip(model_oid, model_dict):
                if self.data['model'] in model:
                    self.data.update(self.added_request(oid))

    def added_request(self, _dict):
        t_dict = {}
        for key, val in _dict.items():
            got = _snmp_get(self.data['ip'], val)
            if not (got.count(' ') > 7 or got == 'NaN'):
                t_dict[key] = got
        return t_dict

class InitSNMP(object):
    def __init__(self, ip):
        self.ip = ip
        self.manufacturer = [{'model': '1.3.6.1.2.1.43.5.1.1.16.1',	'serial_no': '1.3.6.1.2.1.43.5.1.1.17.1'},
                             {'model': '1.3.6.1.2.1.25.3.2.1.3.1', 'serial_no': '1.3.6.1.2.1.43.5.1.1.17.1'}]
        self.model = (('ECOSYS M6635cidn', 'ECOSYS M3655idn', 'MFC-9142CDN', 'MFC-L3770CDW', 'MFC-L3750CDW',
                      'TASKalfa 3051ci', 'TASKalfa 5052ci', 'TASKalfa 4002i', 'MFC-9332CDW', 'MFC-L8650CDW',
                      'DCP-L3510CDW', 'MFC-9460CDN'),
                      ('MFC-9142CDN', 'MFC-L3750CDW', 'MFC-L3770CDW', 'MFC-L8650CDW', 'MFC-9342CDW'))
        self._dict = {'location': '1.3.6.1.2.1.1.6.0'}, {'contact': '1.3.6.1.2.1.1.4.0'}

    def _get_data(self):
        got = _snmp_get(self.ip, '1.3.6.1.2.1.1.1.0')
        temp = False
        result = {'ip': self.ip}
        for i, manufacturer in enumerate(('Kyocera', 'Brother')):
            if manufacturer.casefold() in got.casefold():
                result['manufacturer'] = manufacturer
                temp = self.manufacturer[i]
        if temp:
            for key, val in temp.items():
                got = _snmp_get(self.ip, val)
                if key == 'model':
                    for model in mLib.name_index:
                        if model.casefold() in got.casefold():
                            result[key] = model
                else:
                    if got != 'NaN':
                        result[key] = got
        if result.get('model', False):
            for group, _dict in zip(self.model, self._dict):
                if result['model'] in group:
                    result.update({key: _snmp_get(self.ip, val) for key, val in _dict.items()})
        for key, val in result.items():
            if val.count(' ') > 8:
                result[key] = ''
        return result

    def run(self):
        got = {key: val for key, val in self._get_data().items() if val not in (None, False, '')}
        if got.get('serial_no', False):
            pLib.update_obj(got)
            '''obj = pLib.get_obj(got.get('serial_no'))
            if not (obj is None):
                for key, val in got.items():
                    obj.__setattr__(key, val)
                print(obj)
                #if input('update?') == 'Y':
                pLib.update_obj(obj)'''

if __name__ == '__main__':
    for key, val in model_ip.items():
        req = AdvRequest(key)
        print(req.data) if req.valid() else print('err')

#test_oid('1.3.6.1.2.1.1.4.0')

