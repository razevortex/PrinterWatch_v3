from printerwatch.PrinterRequest.StaticVar import *
from printerwatch.Libs.main import *
from printerwatch.PrinterRequest.snmp_foos import _snmp_get


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
        try:
            self._request(oid)
        except:
            pass

    def _request(self, oids):
        for key, val in oids.items():
            #  Request and Calculation of Toner fill left
            if key == 'Toner':
                for k, v in val[0].items():
                    _max = 1 / int(_snmp_get(self.data['ip'], v).strip()) * 100
                    _fill = int(_snmp_get(self.data['ip'], val[1][k]).strip()) * _max
                    self.tracker_data[k] = int(_fill)
            #  Request of the Page counts
            else:
                got = _snmp_get(self.data['ip'], val)
                self.tracker_data[key] = int(got.strip())


if '__main__' == __name__:
    pass
