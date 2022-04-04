import subprocess as sp
import re
import os

from Packages.SubPkg.Kyocera import KyoceraDefault

if __name__ == '__main__':
    from subs.const.ConstantParameter import *
    from subs.Brother import *
    from subs.csv_handles import *
    from subs.foos import *
else:
    from .SubPkg.const.ConstantParameter import *
    from .SubPkg.Brother import *
    from .SubPkg.csv_handles import *
    from .SubPkg.foos import *

mib = mib_head_snmp


class ClientGet(object):
    def __init__(self, dict):
        self.dict = data_dict_template()
        self.dict.update(dict)
        try:
            cliSpec = dbClientSpecs()
            for line in cliSpec.ClientData:
                if line['Serial_No'] == dict['Serial_No']:
                    self.dict['Notes'] = line['Notes']
        except:
            self.dict['Notes'] = 'NaN'
        self.for_dump = [fr'{ROOT}\temp\{self.snmp_run_main}.txt']

    def run_snmp(self, ip, oid):
        command = f'snmpwalk -v1 -c public {ip} {oid} mgmt'
        p = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE).communicate()[0]
        return self.process_answer(p)

    def process_answer(self, answer):
        temp = answer.decode('utf-8')
        temp = temp.split(':')
        try:
            string = temp[1]
            string = string.replace('"', '')
            string = string.strip()
        except:
            string = 'NaN'
        return string

    def snmp_run_main(self):
        rec = self.run_snmp(self.dict["IP"], '1.3.6.1.2.1.1.1.0')
        if 'KYOCERA' in rec:
            oid = {'Manufacture': 'Kyocera', 'Model': '1.3.6.1.2.1.43.5.1.1.16.1',
                   'Serial_No': '1.3.6.1.2.1.43.5.1.1.17.1'}
            for key in ['Model', 'Serial_No']:
                oid[key] = self.run_snmp(self.dict['IP'], oid[key])
            get_kyocera = KyoceraDefault(self.dict)
            self.dict.update(get_kyocera.return_dict())
            return self.dict
        elif 'Brother' in rec:
            oid = {'Manufacture': 'Brother', 'Model': '1.3.6.1.2.1.25.3.2.1.3.1',
                   'Serial_No': '1.3.6.1.2.1.43.5.1.1.17.1'}
            for key in ['Model', 'Serial_No']:
                oid[key] = self.run_snmp(self.dict['IP'], oid[key])
            specs_lib = SpecsLib(self.dict['Manufacture'])
            for i in specs_lib.ClientData:
                if i['Model'] in self.dict['Model']:
                    self.dict['Model'] = i['Model']
                    specs_method = method_selector(specs_lib, self.dict['Manufacture'], self.dict['Model'])
                    method = specs_method(self.dict, i)
                    self.dict.update(method.return_dict())
                    print(self.dict)
                    return self.dict

