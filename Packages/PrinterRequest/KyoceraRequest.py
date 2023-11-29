from Packages.PrinterRequest.snmp_foos import _snmp_get
from imports import *
from Packages.csv_read import model_ip
from Packages.PrinterRequest.snmp_foos import *
from Packages.PrinterRequest.StaticVar import kyocera_toner_bw, kyocera_toner_color, kyocera_pages, taskalfa_pages, ecosys_pages
from Packages.PrinterObject.main import pLib
from Packages.Libs.main import *


class KyoceraReq(object):
    def __init__(self, data):
        self.data = data
        self.tracker_data = {}
        model = mLib.get(self.data['model'])
        oid = kyocera_toner_bw if not model.color else kyocera_toner_color
        oid.update(kyocera_pages)
        if 'taskalfa'.casefold() in model.name.casefold():
            oid.update(taskalfa_pages)
        if 'ecosys'.casefold() in model.name.casefold():
            oid.update(ecosys_pages)
        print(oid)
        self._request(oid)

    def _request(self, oids):
        print(oids)
        for key, val in oids.items():
            if key == 'Toner':
                for k, v in val[0].items():
                    _max = 1 / int(_snmp_get(self.data['ip'], v).strip()) * 100
                    _fill = int(_snmp_get(self.data['ip'], val[1][k]).strip()) * _max
                    self.tracker_data[k] = int(_fill)
            else:
                got = _snmp_get(self.data['ip'], val)
                print(got)
                #if got == 'NaN':
                #    self.tracker_data = None
                #    return
                #else:
                try:
                    self.tracker_data[key] = int(got.strip())
                except:
                    self.tracker_data[key] = val

if '__main__' == __name__:
    from Packages.PrinterRequest.DefaultRequest import AdvRequest
    for key, val in model_ip.items():
        t = AdvRequest(key)
        if t.valid():
            if t.data['manufacturer'] == 'Kyocera':
                print('Kyocera')
                result = KyoceraReq(t.data)
                print(result.data, result.tracker_data)