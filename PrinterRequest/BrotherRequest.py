import requests
from bs4 import BeautifulSoup
from printerwatch.PrinterRequest.StaticVar import *
from printerwatch.Libs.main import *


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
        t_dict = {'Copies': {}, 'Prints': {}}
        for i, t in enumerate(temp):
            if i == 2 or i == 5:
                for dd, dt in zip(t.find_all('dd'), t.find_all('dt')):
                    self._req0_toner(dd, dt)
                    #if i == 5 and 'page'.casefold() in str(dd.text).casefold():
                    if 'page'.casefold() in str(dd.text).casefold():
                        in_tag = self._req0_pages(dd, dt)
                    elif in_tag:

                        t_dict[in_tag][str(dt.text)] = str(dd.text).strip()
        self.merge_dict(t_dict)
        print(self.tracker_data)
        # remove unwanted html content except of the '/' what is used to close tags in html

    def _req0_pages(self, dd, dt):
        if str(dt.text) in ('Copy', 'Print'):
            in_tag = 'Copies' if str(dt.text).startswith('C') else 'Prints'
        else:
            in_tag = False
        return in_tag

    def _req0_toner(self, dd, dt):
        if '**' in dt.text:
            for col in ('B', 'C', 'M', 'Y'):
                if col in str(dt.text).split(' ')[-1]:
                    val = str(dd.text)
                    for rem in ('(', ')', '%', '"', "'"):
                        val = val.replace(rem, '')
                    val = val.split('.')[0]
                    self.tracker_data[col] = int(val)

    def merge_dict(self, t_dict):
        #print('merge dict', t_dict)
        for key, val in t_dict.items():
            for k, v in val.items():
                if k in ('Color', 'Colour', 'B&W'):
                    if 'sided' not in k:
                        k = 'Color' + key if k != 'B&W' else key
                        self.tracker_data[k] = v

    def request_1(self):
        soup = self.get_soup(1)
        table = soup.find('table', cellpadding="1")
        self.tracker_data = {'C': 29, 'M': 30, 'Y': 31, 'B': 32, 'ColorCopies': 51, 'Copies': 52, 'ColorPrints': 54, 'Prints': 55}
        trow = table.find_all('tr')
        for i, tr in enumerate(trow):
            if 29 <= i <=32:
                self.tracker_data['CMYB'[i-29]] = str(tr).count('■') * 10
            if i in (51, 52, 54, 55):
                diff = 51 if i < 53 else 52
                td = tr.find('td', class_="elem")

                self.tracker_data[('ColorCopies', 'Copies', 'ColorPrints', 'Prints')[i-diff]] = int(str(td.text).strip())
        print(self.tracker_data)


# Execution Sandbox
if __name__ == '__main__':
    pass