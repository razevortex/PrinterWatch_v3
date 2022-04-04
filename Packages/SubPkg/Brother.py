import requests
from bs4 import BeautifulSoup
from Packages.SubPkg.csv_handles import *
'''
Since Brother does not provide enough information (at least for me so far) to design a snmp request to get
all information wanted (especialy the toner fill values that only provide a handful states).

Thats why the Brother Methods use Web Scraping of the clients hosted web interface its codewise a bit 
tidius since the html on that pages obviously wasnt designed for that and doesnt provide unique tag id or name
further brother seems to follow a certain concept for this page but still different series/models can differ from 
slight changes to completly different.

Future Idea´s: there is a Export function on many (known to me) nodels, on the webinterface that will download
the data displayed on the interface as a .csv file what would sidestep the need of extract the data entirely 
and since csv format is widely used anyway in this project would help to get a clean single methode for all models
with this function 

'''

#                                   TO-DO
#   Working on implementing BrotherMFC9460
#   momentarly is included in the BrotherMFCDefault class
#   should get extracted in a seperate class after tested
#   and the methodsBrother(in this module) Foo needs to be updated
#   to return the according class to the RequestHandle module

dict_replacer = {'BrotherMFCDefault': ['<', '>', '=', '%', '(', ')',
                                       'class', '"items"', '"unit"', '"subhead"',
                                       'dt', 'dd', 'dl', 'span', 'Pages', '/List', 'pages',
                                       ' ', '.00', 'Cyan', 'Magenta', 'Yellow', 'Black'
                                       ],
                 'BrotherMFC9460': ['<', '>', '=', '%', '(', ')', 'CLASS', r'\n', 'TR', 'TD', 'NOWRAP', 'TABLE', 'COL',
                                    'SPACING', 'BORDER', 'DT', 'DD', 'DD', 'SPAN', 'Pages', 'ALIGN', 'pages', 'Doner',
                                    r'&nbsp;', ' ', '.00', 'Cyan', 'Magenta', 'Yellow', 'Black', '&nbsp;']
}
dict_index_list = {'BrotherMFCDefault': [2, 5],
                   'BrotherMFC9460': ['other']}
toner_color_tag = [['BK'], ['BK', 'C', 'M', 'Y']]


# methodsBrother returns the class refered by the ModelSpecs Libary to the methodsManuf function of
# of the RequestHandle.ClientGet class
def methodsBrother(method_index):
    if 'BrotherMFCDefault' == method_index:
        return BrotherMFCDefault
    if 'BrotherMFC9460' == method_index:
        return BrotherMFC9460


class BrotherMFCDefault(object):
    def __init__(self, Dict, Specs):
        '''

        :param Dict: the Dict that stores all collected Data in it at this point only containing Serial_No,
                    Manufacture, Model, and IP gets filled with all data and returned
        :param Specs: a Dict that is used to choose certain functions and parameter for the specific Model
        '''
        self.Method = Specs['MethodIndex']
        self.replacer = dict_replacer[self.Method]
        self.html_index_list = dict_index_list[self.Method]
        self._dict = Dict
        id = Dict['Serial_No']
        #clientSpecs = dbClientSpecs()
        #cS = clientSpecs.getEntry('id', id)
        #self._dict['Notes'] = cS['Notes']
        t = Specs['Cart'].split('+')
        cart_type = t[0]
        color_tag = toner_color_tag[int(Specs['Color'])]
        for tag in color_tag:
            dict_t = {f'Cart{tag}': f'{cart_type}{tag}'}
            if cart_type == 'TN-246' and tag == 'BK':
                dict_t = {f'Cart{tag}': 'TN-242BK'}
            if cart_type == 'TN-245' and tag == 'BK':
                dict_t = {f'Cart{tag}': 'TN-241BK'}
            self._dict.update(dict_t)
        self.get_vals()

    def get_vals(self):
        self.get_maintain_page_vals()
        self.get_status_page_vals()

    def return_dict(self):
        dic = self._dict
        return dic

    def get_status_page_vals(self):
        url = f'http://{self._dict["IP"]}/general/status.html'
        soup = self.get_soup(url)
        status = soup.find('div', id='moni_data')
        status = status.get_text().replace('  ', '')
        contact = soup.find('li', class_='contact')
        contact = contact.get_text().replace('\xa0', '').replace('Contact:', '')
        location = soup.find('li', class_='location')
        location = location.get_text().replace('\xa0', '').replace('Location:', '')
        dict_t = {'Status_Report': status, 'Location': location, 'Contact': contact}
        self._dict.update(dict_t)

    def get_maintain_page_vals(self):
        url = f'http://{self._dict["IP"]}/general/information.html?kind=item'
        soup = self.get_soup(url)
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
            table[0] = self.pop_empty_fields(table[0])
            table[1] = self.pop_empty_fields(table[1])
            if len(table[0]) == len(table[1]):
                t = len(table[0])
            else:
                return ('Error key/val in table doesnt match')
        self.extract_maintain_page_vals_to_dict(table, t)

    def extract_maintain_page_vals_to_dict(self, table, *args):
        t = args[0]
        for i in range(t):
            table[0][i] = table[0][i].replace('B&amp;W', 'BnW')
            table[0][i] = table[0][i].replace('\xa0', '')
            if self.get_Toner([table[0][i], table[1][i]]):
                self._dict.update(self.get_Toner([table[0][i], table[1][i]]))
            if i >= 3:
                temp = [[table[0][i - 2], table[1][i - 2]], [table[0][i - 1], table[1][i - 1]],
                        [table[0][i], table[1][i]]]
                if self.get_Pages_Color(temp):
                    self._dict.update(self.get_Pages_Color(temp))


    def get_soup(self, url):
        req = requests.get(url)
        return BeautifulSoup(req.content, 'html.parser')

    def get_Toner(self, field):
        if '**' in field[0]:
            string = field[0].replace('**', '')
            dict_t = {string: field[1]}
            return dict_t
        else:
            return False

    def get_Pages_Color(self, cutout_fields):
        if cutout_fields[0][0] in 'Print':
            dict_t = {'Printed_BCYM': cutout_fields[1][1], 'Printed_BW': cutout_fields[2][1]}
            return dict_t
        if cutout_fields[0][0] in 'Copy':
            dict_t = {'Copied_BCYM': cutout_fields[1][1], 'Copied_BW': cutout_fields[2][1]}
            return dict_t
        else:
            return False

    def pop_empty_fields(self, table):
        pop = []
        for i in range(len(table)):
            if table[i] == '':
                pop.append(i)
            pop = pop[::-1]
        if pop:
            for i in pop:
                table.pop(i)
        return table


class BrotherMFC9460(BrotherMFCDefault):
    def __init__(self, Dict, Specs):
        super().__init__(Dict, Specs)

    def get_status_page_vals(self):
        url = f'http://{self._dict["IP"]}/main/main.html'
        soup = self.get_soup(url)
        temp = soup.find_all('td', class_='location')
        dict_t = {'Status_Report': 'NaN'}
        for t in temp:
            t = t.text
            if t is not None:
                t = t.replace('\n', '*')
                t = t.split('**')
                x = []
                for d in t:
                    d = d.replace('*', '')
                    d = d.replace('\xa0', '')
                    x.append(d)
                dict_t[x[0]] = x[1]
        self._dict.update(dict_t)

    def get_maintain_page_vals(self):
        url = f'http://{self._dict["IP"]}/etc/mnt_info.html?kind=item'
        req = requests.get(url)
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
        self.extract_maintain_page_vals_to_dict(temp)

    def extract_maintain_page_vals_to_dict(self, table, *args):
        if self.Method == 'BrotherMFC9460':
            dict_t = {}
            for t in table:
                dict_t[t[0]] = t[1]
            self._dict.update(dict_t)

