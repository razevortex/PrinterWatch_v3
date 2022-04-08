from Packages.SubPkg.csv_handles import *
from Packages.SubPkg.foos import *

db_dict_template = {}
db_keys = ['TonerBK', 'TonerC', 'TonerM', 'TonerY', 'Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM']
for key in db_keys:
    db_dict_template[key] = 'NaN'

class DataSet(object):
    def __init__(self, ID, headless=False, only_recent=False):
        if headless is not True:
            self.Const = {}
            self.Static = {}
            self.Statistics = {}
            # Data is struc [(index/TimeStamp, {key, val}), (...), ... ]
            self.get_device_data(ID)
        self.Data = []
        self.get_struc_data(ID, only_recent=only_recent)
        self.processing = False
        self.ProcessedData = []

    def get_recent_dict(self):
        t_dic = self.Const
        t_dic.update(self.Static)
        t_dic.update(self.Statistics)
        if type(self.Data) == dict:
            t_dic.update(self.Data)
            return t_dic

    def get_device_data(self, id):
        cli = dbClient()
        cli.updateData()
        for line in cli.ClientData:
            if line['Serial_No'] == id:
                self.Const['Serial_No'] = line['Serial_No']
                self.Const['Device'] = f"{line['Manufacture']} {line['Model']}"
                self.Static['IP'] = line['IP']
        stat = dbStats()
        for line in stat.ClientData:
            for key in ['UsedBK_daily', 'UsedCYM_daily', 'PagesBK_daily', 'PagesCYM_daily', 'CostPerBK', 'CostPerCYM']:
                self.Statistics[key] = line[key]
        spec = dbClientSpecs()
        spec.updateData()
        for line in spec.ClientData:
            if line['Serial_No'] == id:
                # Get and Add User / Location data
                string = user = loc = ''
                if line['Contact'] != 'NaN':
                    self.Static['Contact'] = line['Contact']
                if line['Location'] != 'NaN':
                    self.Static['Location'] = line['Location']
                # Get and Add a string with the used Cartidges
                string = ''
                for cart in ['CartBK', 'CartC', 'CartM', 'CartY']:
                    if line[cart] != 'NaN':
                        if string != '':
                            string += ';'
                        string += line[cart]
                self.Static['Carts'] = string

    def get_struc_data(self, id, only_recent=False):
        db = dbRequest(id)
        self.Data = []
        if only_recent is not True:
            for line in db.ClientData:
                dic_t = copy.deepcopy(db_dict_template)
                index = line['Time_Stamp']
                for key in db_keys:
                    if line[key] != 'NaN':
                        dic_t[key] = int(line[key])
                        if len(line['Status_Report']) > 14:
                            line['Status_Report'] = str(line['Status_Report'])[:14]
                self.Data.append((index, dic_t))
        else:
            line = db.ClientData[-1]
            if len(line['Status_Report']) > 14:
                line['Status_Report'] = str(line['Status_Report'])[:14]
            self.Data = line


    def light_Data(self, reduce='time', key=''):
        if self.processing is not False:
            data = self.ProcessedData
        else:
            data = self.Data
        arr_t = []
        if reduce == 'time':
            dates = []
            for index, dic in data:
                date = index.split(' ')
                date = date[0]
                if date not in dates:
                    arr_t.append((date, dic))
                    dates.append(date)
            #self.processing = True
            #self.ProcessedData = arr_t
        elif reduce == 'keys':
            if type(key) == list:
                for index, dic in data:
                    dic_t = {}
                    for k in key:
                        dic_t[k] = dic[k]
                    arr_t.append((index, dic_t))
            else:
                for index, dic in data:
                    arr_t.append((index, {key: dic[key]}))
        self.processing = True
        self.ProcessedData = arr_t

    def diff_Data(self):
        if self.processing is not False:
            data = self.ProcessedData
        else:
            data = self.Data
        t, v = data[0]
        template = {}
        for key in v.keys():
            template[key] = 0
        '''        template = {'TonerBK': 0, 'TonerC': 0, 'TonerM': 0, 'TonerY': 0, 'Printed_BW': 0, 'Printed_BCYM': 0,
                    'Copied_BW': 0, 'Copied_BCYM': 0}
        '''
        index, dic_1 = data[0]
        arr_t = [(index, template)]
        hold = dic_1
        for index, dic in data[1:]:
            diff = copy.deepcopy(template)
            for key in dic.keys():
                if hold[key] != 'NaN':
                    hold, diff = calculate_diff(key, hold, dic, diff)
            arr_t.append((index, diff))
        self.processing = True
        self.ProcessedData = arr_t

    def combine_keys(self, combine, to):
        if self.processing is not False:
            data = self.ProcessedData
        else:
            data = self.Data
        arr_t = []
        for index, dic in data:
            dic_t = {to: 0}
            for key in dic.keys():
                if key in combine:
                    if dic[key] != 'NaN':
                        dic_t[to] += dic[key]
                else:
                    dic_t[key] = dic[key]
            arr_t.append((index, dic_t))
        self.processing = True
        self.ProcessedData = arr_t

    def sum_data(self):
        if self.processing is not False:
            data = self.ProcessedData
        else:
            data = self.Data
        first = data[0][1]
        dic_t = {}
        for key in first.keys():
            dic_t[key] = 0
        arr_t = []
        for index, dic in data:
            for key in dic.keys():
                dic_t[key] += dic[key]
            arr_t.append((index, copy.deepcopy(dic_t)))
        self.processing = True
        self.ProcessedData = arr_t

    def table_data(self):
        if self.processing is not False:
            data = self.ProcessedData
        else:
            data = self.Data
        arr_t = []
        for index, dic in data:
            dic_t = {'Time_Stamp': index}
            dic_t.update(dic)
            arr_t.append(dic_t)
        return arr_t

    def head_data(self, line='1'):
        if line == '1':
            return f"{self.Const['Serial_No']}, {self.Const['Device']}"
        if line == '2':
            return f"{self.Static['UserLoc']}, {self.Static['IP']}"

fuse = [('TonerC', 'TonerM', 'TonerY'),
         ('Printed_BW', 'Copied_BW'),
         ('Printed_BCYM', 'Copied_BCYM')]
to = ['TonerCYM', 'BW', 'BCYM']
ttt = {'BCYM': 0, 'BW': 0, 'TonerCYM': 0, 'TonerBK': 0}

def get_global_timeline():
    cli = dbClient()
    cli.updateData()
    time_index = []
    for line in cli.ClientData:
        id = line['Serial_No']
        container = DataSet(id, headless=True)
        container.light_Data()
        for day in container.ProcessedData:
            time_index.append(day[0])
    time_index = list(set(time_index))
    time_index = sorted(time_index)
    return time_index

def neutral_timeline():
    arr_t = []
    for i in get_global_timeline():
        arr_t.append((i, 0))
    return arr_t

def get_group_id_set(filter='', filter_for='Manufacture'):
    cli = dbClient()
    cli.updateData()
    dic_t = {}
    if filter == '':
        clients = cli.ClientData

    else:
        arr_t = []
        for line in cli.ClientData:
            specs = dbClientSpecs()
            specs.updateData()
            t_dic = line
            for spe in specs.ClientData:
                if spe['Serial_No'] == line['Serial_No']:
                    t_dic.update(spe)
                    t_dic['ID'] = t_dic['Serial_No']
                    override = LibOverride()
                    t_dic = override.updateDict(t_dic)
            for key, val in t_dic.items():
                if filter.casefold() in val.casefold():
                    arr_t.append(line)
        clients = arr_t
    arr_t = []
    for line in clients:
        arr_t.append(line[filter_for])
    arr_t = list(set(arr_t))
    arr_t = sorted(arr_t)
    for key in arr_t:
        grouped = []
        for line in cli.ClientData:
            if line[filter_for] == key:
                grouped.append(line['Serial_No'])
        dic_t[key] = grouped
    return dic_t


def create_group_data(id_set, data_key, time_line, slim=True):
    fuse = to = False
    if data_key == 'BW':
        fuse = ('Printed_BW', 'Copied_BW')
        to = 'BW'
    elif data_key == 'BCYM':
        fuse = ('Printed_BCYM', 'Copied_BCYM')
        to = 'BCYM'
    elif data_key == 'CYM':
        fuse = ('TonerC', 'TonerM', 'TonerY')
        to = 'CYM'
    arr_t = []
    for id in id_set:
        container = DataSet(id, headless=True)
        if slim:
            container.light_Data()
            if fuse is not False:
                container.combine_keys(fuse, to)
            container.light_Data(reduce='keys', key=data_key)
        container.diff_Data()
        arr_sub_t = []
        # create list with timeline consistent differential values of each id
        for time, val in time_line:
            v = 0 # is inserted if no timeline entry exists to keep consistency
            for index, dic in container.ProcessedData:
                if index == time:
                    v = dic[data_key] # the value on the current timestamp
            arr_sub_t.append(v)
        arr_t.append(arr_sub_t) # bundel all timeline listed values

    # sum vals of each timestamp together and add it to previous to create a progressive list of the value
    fused = []
    val = 0
    for summing in zip(*arr_t):

        val += sum(summing)

        fused.append(val)
    return fused


colors = ['#000054', '#5400fe', '#a90000', '#a9a9fe', '#fe5454', '#0000fe', '#5454a9', '#a900a9', '#a9fe54', '#fe54fe', '#005454', '#54a900', '#a95400', '#a9fefe', '#fea954', '#0054fe', '#54a9a9', '#a954a9', '#fe0054', '#fea9fe', '#00a954', '#54fea9', '#a9a900', '#fe00fe', '#fefe54']


def create_plot_data(group, filter, data_key):
    id_set = get_group_id_set(filter=filter, filter_for=group)
    time_line = neutral_timeline()
    arr_t = []
    for key in id_set.keys():
        dic_t = {}
        group_data = create_group_data(id_set[key], data_key, time_line)
        dic_t['data'] = group_data
        dic_t['label'] = key
        arr_t.append(dic_t)
    data = []
    for i in range(len(arr_t)):
        dic = arr_t[i]
        dic['borderColor'] = colors[i % len(colors)]
        dash = i // len(colors) * 2
        dic['borderDash'] = [10, int(dash)]
        dic['pointRadius'] = 1
        dic['lineTension'] = 0.2
        data.append(dic)
    return data

def create_eff_stats(group, filter, toner='all'):
    '''
    toner= 'all'/'bk'/'cym'
    '''
    key_dict = {'all': ('TonerBK', 'CYM', 'BW', 'BCYM'),
                'bk': ('TonerBK', 'BW'),
                 'cym': ('CYM', 'BCYM')}




if __name__ == '__main__':
    #data_arr = create_plot_data('Serial_No', 'orga', 'BW')
    #for i in data_arr:
    #    print(i)

    cli = dbClient()
    cli.updateData()
    arr = []
    for line in cli.ClientData:
        struc = DataSet(line['Serial_No'], only_recent=True)
        recent = struc.get_recent_dict()
        oRide = LibOverride()
        recent['ID'] = recent['Serial_No']
        recent = oRide.updateDict(recent)
        arr.append(recent)
    for line in arr:
        print(line)
    print(list(arr[0].keys()))
    cache = recentCached()
    cache.ClientData = arr
    cache.updateCSV()
    cache.updateData()
    print(cache.ClientData)
#import os
#for f in os.listdir("/home/razevortex/django_printerwatch/chache"):
#    print(f)
