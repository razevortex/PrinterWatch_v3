from Packages.PrinterRequest.snmp_foos import *
from Packages.PrinterRequest.StaticVar import kyocera_toner_bw, kyocera_toner_color, kyocera_pages, taskalfa_pages, ecosys_pages
from Packages.PrinterObject.main import pLib
from Packages.Libs.main import *
from Packages.PrinterRequest.StaticVar import brother_urls
import requests
from bs4 import BeautifulSoup
import datetime as dt


class BrotherReq(object):

    def __init__(self, data):
        self.data = data
        self.tracker_data = {}
        model = mLib.get(self.data['model'])
        method_dict = {'default': self.request_0, 'MFC-9460CDN': self.request_1}
        print(model.name)
        if model.name in method_dict.keys():
            self.urls = brother_urls[model.name]
            method_dict[model.name]()

        else:
            self.urls = brother_urls['default']
            method_dict['default']()


    def get_soup(self, url):
        req = requests.get(f'http://{self.data["ip"]}{self.urls[url]}')
        return BeautifulSoup(req.content, 'html.parser')

    def request_0(self):
        soup = self.get_soup(1)
        # narrow the html content of specific areas with content we are looking for
        temp = soup.find_all('dl', class_='items')
        in_tag = False
        t_dict = {}
        for i, t in enumerate(temp):
            if i == 2 or i == 5:
                for dd, dt in zip(t.find_all('dd'), t.find_all('dt')):
                    if '**' in dt.text:
                        for col in ('B', 'C', 'M', 'Y'):
                            if col in str(dt.text).split(' ')[-1]:
                                val = str(dd.text)
                                for rem in ('(', ')', '%', '"', "'"):
                                    val = val.replace(rem, '')
                                val = val.split('.')[0]
                                self.tracker_data[col] = int(val)
                    if i == 5 and 'page'.casefold() in str(dd.text).casefold():
                        if str(dt.text) in ('Copy', 'Print'):
                            in_tag = 'Copies' if str(dt.text).startswith('C') else 'Prints'
                            t_dict[in_tag] = {}
                        else:
                            in_tag = False
                    elif in_tag:
                        t_dict[in_tag][str(dt.text)] = str(dd.text).strip()
        self.merge_dict(t_dict)
        print(self.tracker_data)
        # remove unwanted html content except of the '/' what is used to close tags in html

    def merge_dict(self, t_dict):
        for key, val in t_dict.items():
            for k, v in val.items():
                if k in ('Color', 'Colour', 'B&W'):
                    k = 'Color' + key if k != 'B&W' else key
                    self.tracker_data[k] = v

    def request_1(self):
        print('request1')

    """ 
    for cut in self.replacer:
            string = string.replace(cut, '')
        # cutting the string at the html tag sign '/' after merging eventual existing doubles '//'
        string_list = string.replace('//', '/').split('/')
        table = [string_list[0::2], string_list[1::2]]
        if len(table[0]) == len(table[1]):
            t = len(table[0])
        else:
            # checking for empty fields and poping them
            table[0] = pop_empty_fields(table[0])
            table[1] = pop_empty_fields(table[1])
            if len(table[0]) == len(table[1]):
                t = len(table[0])
            else:
                return ('Error key/val in table doesnt match')
        

        
 

  

    def get_Toner(self, field):
        if '**' in field[0]:
            key = field[0][-1] if field[0][-1] != 'K' else 'B'
            self.result.update({key: field[1]})

    def get_Pages_Color(self, cutout_fields):
        if cutout_fields[0][0] in 'Print':
            self.result.update({'ColorPrints': cutout_fields[1][1], 'Prints': cutout_fields[2][1]})
        if cutout_fields[0][0] in 'Copy':
            self.result.update({'ColorCopies': cutout_fields[1][1], 'Copies': cutout_fields[2][1]})

    def getMaintainPage(self, ip):
        pass


# Declarations n Definitions
def pop_empty_fields(table):
    pop = []
    for i in range(len(table)):
        if table[i] == '':
            pop.append(i)
        pop = pop[::-1]
    if pop:
        for i in pop:
            table.pop(i)
    return table


class Default(GetBrother):
    def getMaintainPage(self, ip):
        soup = self.get_soup(ip, self.urls[1])
        # narrow the html content of specific areas with content we are looking for
        temp = soup.find_all('dl', class_='items')
        string = str(temp[2])
        string += str(temp[5])
        # remove unwanted html content except of the '/' what is used to close tags in html
        for cut in self.replacer:
            string = string.replace(cut, '')
        # cutting the string at the html tag sign '/' after merging eventual existing doubles '//'
        string_list = string.replace('//', '/').split('/')
        table = [string_list[0::2], string_list[1::2]]
        if len(table[0]) == len(table[1]):
            t = len(table[0])
        else:
            # checking for empty fields and poping them
            table[0] = pop_empty_fields(table[0])
            table[1] = pop_empty_fields(table[1])
            if len(table[0]) == len(table[1]):
                t = len(table[0])
            else:
                return ('Error key/val in table doesnt match')
        return self.extract_maintain_page_vals_to_dict(table, t)

    def extract_maintain_page_vals_to_dict(self, table, *args):
        t = args[0]
        for i in range(t):
            table[0][i] = table[0][i].replace('B&amp;W', 'BnW')
            table[0][i] = table[0][i].replace('\xa0', '')
            self.get_Toner([table[0][i], table[1][i]])
            if i >= 3:
                temp = [[table[0][i - 2], table[1][i - 2]], [table[0][i - 1], table[1][i - 1]],
                        [table[0][i], table[1][i]]]
                self.get_Pages_Color(temp)
        return self.result


class MFC9460CDN(GetBrother):
    def getMaintainPage(self, ip):
        req = requests.get(f'http://{ip}{self.urls[1]}')
        table = str(req.content)
        main = table.split('<TD CLASS="PageTitle">')
        m = main[1]
        for r in self.replacer:
            m = m.replace(r, '')
        m = m.replace('/', '')
        m = m.split('"item"')
        tonerfill = []
        copy = []
        printed = []
        for i in m:
            if '"elem"' in i:
                i = i.replace(' ', '')
                x = i.split('"elem"')
                if 0 < len(copy) < 3:
                    x[0] = f'Copied_{x[0]}'
                    x[0] = x[0].replace('&', '')
                    x[0] = x[0].replace('Color', 'BCYM')
                    copy.append(x)
                if 0 < len(printed) < 3:
                    x[0] = f'Printed_{x[0]}'
                    x[0] = x[0].replace('&', '')
                    x[0] = x[0].replace('Color', 'BCYM')
                    printed.append(x)
                if 'Copy' in x[0]:
                    copy.append(x)
                if 'Print' in x[0] and 'Printed' not in x[0]:
                    printed.append(x)
                if '**' in x[0]:
                    col = x[0].replace('**', '')
                    if '*' not in col:
                        col = col.replace('K', 'BK')
                        toner = f'Toner{col}'
                        string = x[1].split(';')
                        counter = 0
                        for i in string:
                            if '0' in i:
                                counter += 1
                        counter = counter * 10
                        fill = str(counter)
                        x = [toner, fill]
                        tonerfill.append(x)
        printed.pop(0)
        copy.pop(0)
        temp = []
        temp.extend(tonerfill)
        temp.extend(printed)
        temp.extend(copy)
        return self.extract_maintain_page_vals_to_dict(temp)

    def extract_maintain_page_vals_to_dict(self, table, *args):
        if self.Method == 'BrotherMFC9460':
            dict_t = {}
            for t in table:
                dict_t[t[0]] = t[1]
            self.result.update(dict_t)
        return self.result"""


# Execution Sandbox
if __name__ == '__main__':
    from Packages.PrinterRequest.DefaultRequest import AdvRequest
    for key, val in model_ip.items():
        t = AdvRequest(key)
        if t.valid():
            if t.data['manufacturer'] == 'Brother':
                print('Brother')
                result = BrotherReq(t.data)
