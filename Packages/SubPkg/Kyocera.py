import copy
from Packages.SubPkg.csv_handles import *
from .const.ConstantParameter import *
import subprocess as sp
import re

class KyoceraDefault(object):
    def __init__(self, Dict):
        '''

        :param Dict: the Dict that stores all collected Data in it at this point only containing Serial_No,
                    Manufacture, Model, and IP gets filled with all data and returned
        :param Specs: a Dict that is used to choose certain functions and parameter for the specific Model
        '''
        self._dict = Dict
        #id = Dict['Serial_No']
        #clientSpecs = dbClientSpecs()
        #cS = clientSpecs.getEntry('id', id)
        #self._dict['Notes'] = cS['Notes']
        #self.for_dump = []
        self.run_snmp_main()

    def kyocera_dic(self, dic):
        if dic['Model'] in ['TASKalfa 5052ci', 'TASKalfa 4550ci', 'TASKalfa 3051ci', 'ECOSYS M6635cidn']:
            max = {'TonerC': '1.3.6.1.2.1.43.11.1.1.8.1.1', 'TonerM': '1.3.6.1.2.1.43.11.1.1.8.1.2',
                   'TonerY': '1.3.6.1.2.1.43.11.1.1.8.1.3', 'TonerBK': '1.3.6.1.2.1.43.11.1.1.8.1.4'}
            fill = {'TonerC': '1.3.6.1.2.1.43.11.1.1.9.1.1', 'TonerM': '1.3.6.1.2.1.43.11.1.1.9.1.2',
                    'TonerY': '1.3.6.1.2.1.43.11.1.1.9.1.3', 'TonerBK': '1.3.6.1.2.1.43.11.1.1.9.1.4'}
            t_dict = {'CartC': '1.3.6.1.2.1.43.11.1.1.6.1.1', 'CartM': '1.3.6.1.2.1.43.11.1.1.6.1.2',
                      'CartY': '1.3.6.1.2.1.43.11.1.1.6.1.3', 'CartBK': '1.3.6.1.2.1.43.11.1.1.6.1.4'}
            if 'TASK' in dic['Model']:
                add = {'Printed_BW': '1.3.6.1.4.1.1347.42.3.1.2.1.1.1.1',
                       'Printed_BCYM': '1.3.6.1.4.1.1347.42.3.1.2.1.1.1.3',
                       'Copied_BW': '1.3.6.1.4.1.1347.42.3.1.2.1.1.2.1',
                       'Copied_BCYM': '1.3.6.1.4.1.1347.42.3.1.2.1.1.2.3',
                       'Status_Report': '1.3.6.1.4.1.1347.43.18.2.1.2.1.1',
                       'Contact': '1.3.6.1.2.1.1.6.0', 'Location': '1.3.6.1.2.1.1.5.0'}
            elif 'ECOSYS' in dic['Model']:
                add = {'Printed_BW': '1.3.6.1.4.1.1347.42.3.1.2.1.1.1.1',
                       'Printed_BCYM': '1.3.6.1.4.1.1347.42.3.1.2.1.1.1.2',
                       'Copied_BW': '1.3.6.1.4.1.1347.42.3.1.2.1.1.2.1',
                       'Copied_BCYM': '1.3.6.1.4.1.1347.42.3.1.2.1.1.2.2',
                       'Status_Report': '1.3.6.1.4.1.1347.43.18.2.1.2.1.1',
                       'Contact': '1.3.6.1.2.1.1.6.0', 'Location': '1.3.6.1.2.1.1.5.0'}
            t_dict.update(add)
        else:
            max = {'TonerBK': '1.3.6.1.2.1.43.11.1.1.8.1.1'}
            fill = {'TonerBK': '1.3.6.1.2.1.43.11.1.1.9.1.1'}
            t_dict = {'CartBK': '1.3.6.1.2.1.43.11.1.1.6.1.1'}
            if 'FS-1320D' in dic['Model']:
                add = {'Printed_BW': '1.3.6.1.4.1.1347.42.3.1.1.1.1.1',
                       'Copied_BW': '1.3.6.1.4.1.1347.42.3.1.1.1.1.2',
                       'Status_Report': 'enterprises.1347.43.18.2.1.2.1.1',
                       'Contact': '1.3.6.1.2.1.1.6.0', 'Location': '1.3.6.1.2.1.1.5.0'}
            else:
                add = {'Printed_BW': '1.3.6.1.4.1.1347.42.3.1.1.1.1.1',
                       'Copied_BW': '1.3.6.1.4.1.1347.42.3.1.1.1.1.2',
                       'Status_Report': '1.3.6.1.4.1.1347.43.18.2.1.2.1.1',
                       'Contact': '1.3.6.1.2.1.1.6.0', 'Location': '1.3.6.1.2.1.1.5.0'}
            t_dict.update(add)
        return t_dict, max, fill

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

    def run_snmp(self, ip, oid):
        command = f'snmpwalk -v1 -c public {ip} {oid} mgmt'
        p = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE).communicate()[0]
        return self.process_answer(p)

    def run_snmp_main(self):
        t_dic, max, fill = self.kyocera_dic(self._dict)
        for key in t_dic.keys():
            self._dict[key] = self.run_snmp(self._dict['IP'], t_dic[key])
        self._dict.update(self.toner_calc(max, fill))

    def return_dict(self):
        _dict = self._dict
        return _dict

    def toner_calc(self, max, fill):
        temp = {}
        for key in max.keys():
            try:
                m = int(self.run_snmp(self._dict['IP'], max[key]))
                f = int(self.run_snmp(self._dict['IP'], fill[key]))
                m = float(100 / m)
                t = int(m * f)
                temp[key] = t
            except:
                temp[key] = 'NaN'
        return temp