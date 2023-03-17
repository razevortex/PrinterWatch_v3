import copy

from Packages.SubPkg.const.ConstantParameter import *
from Packages.SubPkg.csv_handles import *
from Packages.SubPkg.storage_data_handles import *
from Packages.SubPkg.foos import *
import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
from collections import defaultdict
from math import fsum

db_dict_template = {}
db_keys = ['TonerBK', 'TonerC', 'TonerM', 'TonerY', 'Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM']
for key in db_keys:
    db_dict_template[key] = 'NaN'

'''
CLASSES SECTION containing 
DataSet Class : used for process the databases to calculate implied values
    it has multiple functionalities to it first it gathers all data from the 
    different datasets of a ID then there are options for pruning parts of it
    or reduce the amount of timestamps by summarizing them, it also can preprocess
    values to get the difference between timestamps instead of the absolute values 
CartStoreTracker : used to process the data to evaluate the CartStored values
'''


class DataSet(object):
    def __init__(self, ID, headless=False, only_recent=False):
        if headless is not True:
            self.Const = {}
            self.Static = {}
            self.Statistics = {}
            # Data is struc [(index/TimeStamp, {key, val}), (...), ... ]
            self.get_device_data(ID)
        self.ID = ID
        self.Data = []
        self.get_struc_data(ID, only_recent=only_recent)
        self.processing = False
        self.ProcessedData = []

    def get_all(self, customized=False):
        t_dic = self.Const
        t_dic.update(self.Static)
        t_dic.update(self.Statistics)
        if customized is not False:
            t_dic['ID'] = t_dic['Serial_No']
            t_dic['Notes'] = 'NaN'
            orData = LibOverride()
            orData.updateDict(t_dic)
        if type(self.Data) == dict:
            t_dic.update(self.Data)
        return t_dic

    def cout_data(self):
        if self.processing:
            arr = self.ProcessedData
        else:
            arr = self.Data
        [print(d) for d in arr]

    def get_data(self):
        if self.processing:
            return self.ProcessedData
        else:
            return self.Data

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

            if line['Serial_No'] == id:

                for key in ['UsedBK_daily', 'UsedCYM_daily', 'PagesBK_daily', 'PagesCYM_daily', 'CostPerBK', 'CostPerCYM']:
                    self.Statistics[key] = line[key]
        spec = dbClientSpecs()
        spec.updateData()
        for line in spec.ClientData:
            if line['Serial_No'] == id:
                # Get and Add User / Location data
                string = user = loc = ''
                self.Static['Contact'] = line['Contact'] if line['Contact'] != 'NaN' else ''
                self.Static['Location'] = line['Location'] if line['Location'] != 'NaN' else ''
                # Get and Add a string with the used Cartidges
                string = ''
                for cart in ['CartBK', 'CartC', 'CartM', 'CartY']:
                    if line[cart] != 'NaN':
                        if string != '':
                            string += ';'
                        string += line[cart]
                        self.Static[cart] = line[cart]
                self.Static['Carts'] = string

    def addCartPrices(self, comb=False):
        t_dic = {}
        if comb is not False:
            t_dic['CartCYM'] = 0
        cost_dic = {'CartBK': 'NaN', 'CartC': 'NaN', 'CartY': 'NaN', 'CartM': 'NaN'}
        for key in self.Static.keys():
            if key.startswith('Cart') and key != 'Carts':
                cost_dic[key] = TONER_COST_DICT[self.Static[key]][1]
        print(cost_dic)
        return cost_dic

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
                    if key == 'Status_Report':
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

    def sum_data(self, periode='total'):
        arr_t = []
        if self.processing is not False:
            data = self.ProcessedData
        else:
            data = self.Data
        if periode == 'total':
            first = data[0][1]
            dic_t = {}
            for key in first.keys():
                dic_t[key] = 0
            for index, dic in data:
                for key in dic.keys():
                    dic_t[key] += dic[key]
                arr_t.append((index, copy.deepcopy(dic_t)))
        else:
            if periode == 'week':
                add = dt.timedelta(weeks=1)
            if periode == 'month':
                add = relativedelta(months=1)
            dic_t = {}
            for key in data[0][1]:
                dic_t[key] = 0
            date = dt.date.fromisoformat(data[0][0])
            day = date + add
            last = dt.date.fromisoformat(data[-1][0]) if len(data) > 2 else date
            sum_dic = data[0][1]
            index = str(date)
            while date <= last:
                end_index = str(date)
                date = date + dt.timedelta(days=1)
                if date == day:
                    index += f' - {end_index}'
                    arr_t.append((index, sum_dic))
                    sum_dic = copy.deepcopy(dic_t)
                    index = str(date)
                    day = date + add
                for t, d in data:
                    if dt.date.fromisoformat(t) == date:
                        for key in d.keys():
                            sum_dic[key] += d[key]
            index += f' - {end_index}'
            arr_t.append((index, sum_dic))
            print(arr_t)
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
            return f"{self.Static['Contact']}, {self.Static['Location']}, {self.Static['IP']}"

    def detail_og_or_data(self):
        og_dic = copy.deepcopy(self.Const)
        og_dic.update(self.Static)
        og_dic['Notes'] = 'Notes'
        for key in ['Serial_No', 'IP', 'Device', 'Contact', 'Location', 'Notes']:
            if og_dic[key] == '':
                og_dic[key] = key
        return og_dic

    def back2raw(self):
        self.processing = False


class CartStoreTracker(object):
    def __init__(self):
        self.storage_handle = CartridgeStorage()
        self.data_list = self.get_data_from_cache()
        self.date = dt.date.today()
        self.data = []
        self.delta = ''
        self.colors = {'BK': '#000000', 'C': '#00ffff', 'Y': '#FFFF00', 'M': '#FF00FF'}
        self.plot_timeline = []
        self.plot = []
        self.table_data = []

    def get_data_from_cache(self):
        cache = Cached('recentCached')
        cache.updateData()
        stats = Cached('client_stats')
        stats.updateData()
        t_arr = []
        for line in cache.ClientData:
            for stat in stats.ClientData:
                if stat['Serial_No'] == line['ID']:
                    for v in ['BK', 'C', 'Y', 'M']:
                        if line[f'Cart{v}'] != '':
                            t_dic = {line[f'Cart{v}']: (line[f'Toner{v}'], stat[f'Toner{v}PerDay'])}
                            if 'NaN' not in t_dic.values():
                                t_arr.append(t_dic)
        return t_arr

    def list_of_cart_types(self):
        self.create_table_data()
        t_arr = []
        for line in self.table_data:
            t_arr.append(line['cTyp'])
        for color in ['BK', 'C', 'M', 'Y', 'S', 'K']:
            if color == 'K':
                t_arr = [typ.rstrip(color) for typ in t_arr]
            else:
                t_arr = [typ.replace(color, '') for typ in t_arr]
        return list(set(t_arr))

    def process_line(self, line):
        for key, val in line.items():
            a, b = val
            a = float(a) - float(b)
            if a <= 0:
                val = (100, b)
                self.delta[key] -= 1
            else:
                val = (a, b)
        return {key: val}

    def create_table_data(self):
        end = copy.deepcopy(self.storage_handle.virtual_storage)
        self.storage_handle.restore_vs()
        start = copy.deepcopy(self.storage_handle.virtual_storage)
        for key in sorted(list(start.keys())):
            t_dic = {'cTyp': key, 'cStore': start[key], 'cLow': str(start[key] - end[key]), 'cNew': end[key]}
            self.table_data.append(t_dic)

    def process_time(self, days, filter_mode='Only changing'):
        self.data.append((self.date, copy.deepcopy(self.storage_handle.virtual_storage)))
        for day in range(days):
            self.date = self.date + dt.timedelta(days=1)
            self.delta = self.storage_handle.get_delta_zero_dict()
            print(self.delta, self.data)
            self.data_list = [self.process_line(line) for line in self.data_list]
            self.storage_handle.update_vs(self.delta)
            self.data.append((self.date, copy.deepcopy(self.storage_handle.virtual_storage)))
        self.create_table_data()
        key_list = list(self.delta.keys())
        self.plot_timeline = [str(date[0]) for date in self.data]
        self.plot = []
        for key in key_list:
            t_dic = {}
            t_dic['label'] = key
            t_dic['data'] = [date[1][key] for date in self.data]
            self.filter_mode_condition(key, t_dic, filter_mode)
        return self.plot_timeline, self.plot

    def filter_mode_condition(self, key, t_dic, filter_mode):
        if filter_mode == 'Only changing':
            if len(set(t_dic['data'])) > 1:
                self.create_plot(key, t_dic)
        else:
            if filter_mode in key:
                self.create_plot(key, t_dic)

    def create_plot(self, key, t_dic):
        for k in self.colors.keys():
            if k in key:
                t_dic['borderColor'] = self.colors[k]
        t_dic['pointRadius'] = 1

        t_dic['lineTension'] = 0.2
        self.plot.append(t_dic)


'''
FUNCTION SECTION 
Function that handle the stored data and process them to be presented in the web application
most of them depending on the classes above
'''

# **_timeline functions generate a array of timestamps for presentations that include a
# over time aspect like line plots


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


# if there are a multiple of ids data needed this function gets the grouped ids
# for the used textinput/filter and/or the chosen filter for manufactures, models
# and generates list/s with the according ids
def get_group_id_set(filter='', filter_for='Manufacture'):
    cli = dbClient()
    cli.updateData()
    if filter == '' or filter == '*':
        clients = cli.ClientData
    else:
        clients = []
        for line in cli.ClientData:
            dSet = DataSet(line['Serial_No'])
            for key, val in dSet.get_all(customized=True).items():
                if filter.casefold() in val.casefold():
                    clients.append(line)
    group_dict = defaultdict(list)
    for temp in [{line[filter_for]: line['Serial_No']} for line in clients]:
        for key, val in temp.items():
            group_dict[key].append(val)
    return group_dict

# these are used in the following function if the grouped ids values need to fuse
# certain values like colored toner or Printed/Copied
fuse = [('TonerC', 'TonerM', 'TonerY'),
        ('Printed_BW', 'Copied_BW'),
        ('Printed_BCYM', 'Copied_BCYM')]
to = ['TonerCYM', 'PagesBW', 'PagesBCYM']
ttt = {'BCYM': 0, 'BW': 0, 'TonerCYM': 0, 'TonerBK': 0}


# uses the id-groups lists from the previous function and merges the
# data_key values to a single dataset
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
            v = 0    # is inserted if no timeline entry exists to keep consistency
            for index, dic in container.ProcessedData:
                if index == time:
                    v = dic[data_key]     # the value on the current timestamp
            arr_sub_t.append(v)
        arr_t.append(arr_sub_t)    # bundel all timeline listed values
    # sum vals of each timestamp together and add it to previous to create a progressive list of the value
    fused = []
    val = 0
    for summing in zip(*arr_t):
        val += sum(summing)
        fused.append(val)
    return fused


####
######      Start of the CHART.JS object creation functions and needed vars like color tables

colors = ['#000054', '#5400fe', '#a90000', '#a9a9fe', '#fe5454', '#0000fe', '#5454a9',
          '#a900a9', '#a9fe54', '#fe54fe', '#005454', '#54a900', '#a95400', '#a9fefe',
          '#fea954', '#0054fe', '#54a9a9', '#a954a9', '#fe0054', '#fea9fe', '#00a954',
          '#54fea9', '#a9a900', '#fe00fe', '#fefe54']

### creating a pie chart object


def create_plot_data(group, filter, data_key):
    id_set = get_group_id_set(filter=filter, filter_for=group)
    time_line = neutral_timeline()
    arr_t = []
    for key in id_set.keys():
        dic_t = {}
        group_data = create_group_data(id_set[key], data_key, time_line)
        dic_t['data'] = group_data
        spec = dbClientSpecs()
        label = key
        # start changes for useing loc cont as label

        t_label = ''
        for client_spec in spec.ClientData:
            if client_spec['Serial_No'] == key:
                if client_spec['Location'] != 'NaN':
                    t_label += client_spec['Location']
                if client_spec['Contact'] != 'NaN':
                    t_label += client_spec['Contact']
        if t_label != '':
            label = t_label
        # end changes useing loc cont as label
        dic_t['label'] = label
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

pie_chart_key_dict = {'Total_BW': ('Printed_BW', 'Copied_BW'),
                      'Total_BCYM': ('Printed_BCYM', 'Copied_BCYM'),
                      'Total_Output': ('Printed_BW', 'Copied_BW',
                                       'Printed_BCYM', 'Copied_BCYM')}


def create_pie_chart(group, filter, data_key):
    id_set = get_group_id_set(filter=filter, filter_for=group)
    labels = list(id_set.keys())
    t_dic = {}
    for label in labels:
        t_dic[label] = 0
    time_line = neutral_timeline()
    for key in id_set.keys():
        for keys in pie_chart_key_dict[data_key]:
            if type(create_group_data(id_set[key], keys, time_line)[-1]) == int:
                t_dic[key] += create_group_data(id_set[key], keys, time_line)[-1]
    color = []
    for i in range(0, len(list(t_dic.keys()))):
        color.append(colors[i % len(colors)])
    dataset = [{'label': data_key, 'data': list(t_dic.values()), 'backgroundColor': color, 'hoverOffset': 4}]
    plot_type = 'pie'
    conf = {'type': plot_type, 'data': {'labels': list(t_dic.keys()), 'datasets': dataset}, }
    return conf

'''# a little milestone to remember i first used the code below but noticed i got the total 
    values of the printer not the total values of the recorded time window then i re noticed hey
    the line plot has the values i want as the last value of the line i reused the approache 
    of the plot and adjusted a few thinks to fit for this pie chart and OMFREAKINGOD 
    worked 100% first try.
    Maybe i can improve the bar chart also.
    
    For now i bath in the 'like a pro' sunshine of my accomplishment till, soon there will
    be a lot of collapsing everthing around me and hours of unsuccesful bughuntin till i manage 
    to find the stupid nooby fail i managed to sneak in somehow and didnt noticed the issue hours of
    codeing later ahh that joy :)
   #################################################################################     
    for key in labels:
        t_dic[key] = []
        for id in id_set[key]:
            for line in chached_lib.ClientData:
                if id == line['Serial_No']:
                    for keys in pie_chart_key_dict[data_key]:
                        val = 0
                        if line[keys].casefold() != 'NaN'.casefold():
                            val += int(line[keys])
                        t_dic[key].append(val)
    data = {}
    for key, value in t_dic.items():

        if type(value) == list:
            data[key] = sum(value)# / int(len(value) + 1)
        else:
            if value.casefold() != 'NaN'.casefold():
                data[key] = value
    labels = []
    t_data = []
    color = []
    i = 0
    for key, value in data.items():

        if value > 0.0:
            labels.append(key)
            t_data.append(value)
            color.append(colors[i % len(colors)])
            i += 1

    dataset = [{'label': data_key, 'data': t_data, 'backgroundColor': color, 'hoverOffset': 4}]
    plot_type = 'pie'
    conf = {'type': plot_type, 'data': {'labels': labels, 'datasets': dataset}, }
    return conf
    '''


def create_bar_data(group, filter, data_key):
    id_set = get_group_id_set(filter=filter, filter_for=group)
    labels = list(id_set.keys())
    chached_stats = Cached('client_stats')
    chached_stats.updateData()
    t_dic = {}
    for key in labels:
        t_dic[key] = []
        for id in id_set[key]:
            for line in chached_stats.ClientData:
                if id == line['Serial_No']:
                    if line[data_key].casefold() != 'NaN'.casefold():
                       t_dic[key].append(float(line[data_key]))
    data = {}
    for key, value in t_dic.items():

        if type(value) == list:
            data[key] = sum(value) / int(len(value) + 1)
        else:
            if value.casefold() != 'NaN'.casefold():
                data[key] = value
    labels = []
    t_data = []
    color = []
    i = 0
    for key, value in data.items():

        if value > 0.0:
            labels.append(key)
            t_data.append(value)
            color.append(colors[i % len(colors)])
            i += 1
    dataset = [{'label': data_key, 'data': t_data, 'backgroundColor': color, 'borderWidth': 1}]
    plot_type = 'bar'
    conf = {'type': plot_type, 'data': {'labels': labels, 'datasets': dataset}, 'options': {}}
    return conf


###
### CREATING A PRE-HANDLED DATABASE DURING BACKGROUND-REQUEST
def update_recentCache():
    cli = dbClient()
    cli.updateData()
    arr = []
    for line in cli.ClientData:
        recent = DataSet(line['Serial_No'], only_recent=True)
        t_recent = recent.get_all(customized=True)
        oRide = LibOverride()
        container = DataSet(line['Serial_No'], only_recent=False)
        if 'Brother' in container.Const['Device']:
            cache = Cached('client_stats')
            cache.updateData()
            for line in cache.ClientData:
                if line['Serial_No'] == container.Const['Serial_No']:
                    stat = line
                    break
            container.combine_keys(('Printed_BW', 'Copied_BW'), 'BW')
            container.combine_keys(('Printed_BCYM', 'Copied_BCYM'), 'BCYM')
            container.diff_Data()
            data = container.ProcessedData[::-1]
            t_dic = {'BK': 0, 'C': 0, 'Y': 0, 'M': 0}
            for key in t_dic.keys():
                i = 0
                toner = f'Toner{key}'
                line = data[i][1]
                if t_recent[toner] != 'NaN':
                    while line[toner] == 0:
                        if key == 'BK':
                            t_dic[key] += line['BW'] if line['BW'] != 'NaN' else 0
                        t_dic[key] += line['BCYM'] if line['BCYM'] != 'NaN' else 0
                        i += 1
                        if i > len(data) - 1:
                            break
                        else:
                            line = data[i][1]
                    if t_dic[key] != 0 and t_dic[key] != 'NaN':
                        t_dic[key] = (float(stat[f'Pp{key}']) / 10) / t_dic[key]
                        if int(t_recent[toner]) < 100:
                            t_recent[toner] = int(int(t_recent[toner]) + 10 - t_dic[key] if t_dic[key] < 10 else int(t_recent[toner]))
        arr.append(t_recent)
    cache = Cached('recentCached')
    cache.ClientData = arr
    cache.updateCSV()


def calculate_tonerPer(toner, pages, to):
    t_dic = {to: 0}
    if toner != 0 and pages != 0:
        cart = toner / 100
        pagesPer = pages / cart
        if '.' in str(pagesPer):
            point = str(pagesPer).index('.')
            point += 2
            pagesPer = str(pagesPer)[:point]
            t_dic = {to: float(pagesPer)}
        else:
            t_dic = {to: pagesPer}
    return t_dic


def calculate_pageCost(pagesPer, cartPrice, to):
    t_dic = {to: 0}
    if pagesPer != 0 and cartPrice != 0:
        pageCost = cartPrice / pagesPer
        if len(str(pageCost)) > 5:
            #point = str(pageCost).index('.')
            #point += 3
            pageCost = str(pageCost)[:5]
            t_dic = {to: float(pageCost)}
        else:
            t_dic = {to: pageCost}
    return t_dic


def cart_efficency(bw, bcym, b, c, y, m):
    t_dic = {}
    p_total = bw + bcym
    if 0 not in (p_total, b):
        t_dic['PpBK'] = float_depth(float(100 / b * p_total))
    if bcym != 0:
        for key, val in {'C': c, 'Y': y, 'M': m}.items():
            string = f'Pp{key}'
            if val != 0:
                t_dic[string] = float_depth(float(100 / val * bcym))
    return t_dic


def stats(t_dic, price_dict):
    result_dic = {}
    for key in cache_header['client_stats']:
        result_dic[key] = 'NaN'

    result_dic.update(
        {'Serial_No': t_dic['Serial_No'], 'Device': t_dic['Device'], 'DaysMonitored': t_dic['DaysWatched']})
    result_dic.update(
        cart_efficency(t_dic['BW'], t_dic['BCYM'], t_dic['TonerBK'], t_dic['TonerC'], t_dic['TonerY'], t_dic['TonerM']))
    for key, val in t_dic.items():
        if key != 'DaysWatched':
            string = f'{key}PerDay'
            if val != 0 and t_dic['DaysWatched'] != 0 and type(val) == int:
                result_dic[string] = float_depth(float(val / int(t_dic['DaysWatched'])))
    t_price = {'BK': 0, 'C': 0, 'M': 0, 'Y': 0}
    for key, val in result_dic.items():
        if key.startswith('Pp'):
            color_key = key.replace('Pp', '')
            if price_dict[f'Cart{color_key}'] != 'NaN':
                t_price[color_key] = float_depth(price_dict[f'Cart{color_key}'] / float(val), depth=4)
            else:
                t_price[color_key] = 'NaN'
    result_dic['CostPerBW'] = t_price['BK']
    if 'NaN' not in t_price.values():
        result_dic['CostPerBCYM'] = float_depth(fsum(t_price.values()), depth=4)
        if np.isnan(result_dic['CostPerBCYM']):
            result_dic['CostPerBCYM'] = 'NaN'
    return result_dic


def create_stat_db():
    cli = dbClient()
    cli.updateData()
    t_arr = []
    for line in cli.ClientData:
        container = DataSet(line['Serial_No'])
        container.combine_keys(('Printed_BW', 'Copied_BW'), 'BW')
        container.combine_keys(('Printed_BCYM', 'Copied_BCYM'), 'BCYM')
        container.diff_Data()
        container.sum_data()
        start_date, last = container.get_data()[0][0], container.get_data()[-1]
        time_past = dt.datetime.fromisoformat(last[0]) - dt.datetime.fromisoformat(start_date)
        t_dic = last[1]
        t_dic['DaysWatched'] = time_past.days
        t_dic.update(container.Const)
        t_dic.update(container.Static)
        t_arr.append(stats(t_dic, container.addCartPrices()))
    cache = Cached('client_stats')
    cache.ClientData = t_arr
    cache.updateCSV()


###
### PRINTER MONITOR SPECIFIC FOO´s

def get_table_data(filter):
    cache = Cached('recentCached')
    cache.updateData()
    arr = []
    for line in cache.ClientData:
        if filter != '*':
            for val in line.values():
                if filter.casefold() in val.casefold():
                    arr.append(line)
                    break
        else:
            arr.append(line)
    return data_struc4JSON(arr)


def data_struc4JSON(dic_list):
    result_list = []
    for entry in dic_list:
        t_dic = {'sno': entry['Serial_No']}
        t_dic['uptodate'] = 'green'
        if dt.datetime.fromisoformat(entry['Time_Stamp']) + dt.timedelta(days=3) < dt.datetime.now():
            t_dic['uptodate'] = 'red'
        elif dt.datetime.fromisoformat(entry['Time_Stamp']) + dt.timedelta(days=1) < dt.datetime.now():
            t_dic['uptodate'] = 'orange'
        t_dic['id'] = entry['ID']
        t_dic['device'] = entry['Device']
        t_dic['ip'] = entry['IP']
        string = user = loc = ''
        if entry['Contact'] != 'NaN':
            user = entry['Contact']
        if entry['Location'] != 'NaN': # and entry['Location'] != entry['Contact']:
            loc = entry['Location']
        string += user
        if loc != user:
            string += f' {loc}'
        t_dic['userLoc'] = string
        toner_fill = []
        for key in ['TonerBK', 'TonerC', 'TonerY', 'TonerM']:
            if entry[key] != 'NaN':
                toner_fill.append(entry[key])
            else:
                toner_fill.append('')
        toner_fill.append(entry['Carts'])
        t_dic['toner'] = toner_fill
        string = entry['Status_Report']
        t_dic['status'] = string if len(string) < 12 else string[:11]
        if entry['Notes'] != 'NaN':
            t_dic['notes'] = entry['Notes']
        else:
            t_dic['notes'] = ''
        result_list.append(t_dic)
    return result_list
###
### END OF PRINTER MONITOR VIEW FOO´s


###
### PRINTER DETAILS SPECIFIC FOO´s


def get_device_detail(id):
    container = DataSet(id)
    container.light_Data()
    container.diff_Data()
    head_data = container.detail_og_or_data()
    fuse = [('Printed_BW', 'Copied_BW'),
                ('Printed_BCYM', 'Copied_BCYM')]
    to = ['PagesBW', 'PagesBCYM']
    for i in range(len(fuse)):
        container.combine_keys(fuse[i], to[i])
    container.sum_data()
    return head_data, container.table_data()


def get_details_data(id, config, fuseing):

    container = DataSet(id)
    container.light_Data()
    container.diff_Data()
    if fuseing == 'grouped':
        fuse = [('TonerC', 'TonerM', 'TonerY'),
                ('Printed_BW', 'Copied_BW'),
                ('Printed_BCYM', 'Copied_BCYM')]
        to = ['TonerCYM', 'PagesBW', 'PagesBCYM']
        for i in range(len(fuse)):
            container.combine_keys(fuse[i], to[i])
    if fuseing == 'seperated':
        fuse = [('Printed_BW', 'Copied_BW'),
                ('Printed_BCYM', 'Copied_BCYM')]
        to = ['PagesBW', 'PagesBCYM']
        for i in range(len(fuse)):
            container.combine_keys(fuse[i], to[i])
    container.sum_data(periode=config)
    return container.table_data(), container.head_data


if __name__ == '__main__':
    store = CartStoreTracker()
    print(store.list_of_cart_types())


