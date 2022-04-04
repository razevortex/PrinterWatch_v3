from Packages.SubPkg.const.ConstantParameter import TONER_COST_DICT, header, statistics_key_type, statistics_grouping_vals, statistics_grouping_dict, statistics_variable_grouping_method, ROOT, data_dict_template
import datetime as dt
from Packages.SubPkg.csv_handles import *
from Packages.SubPkg.foos import *
import pandas as pd


def data_template():
    t_dict = {}
    for value in header['statistics']:
        t_dict[value] = 'NaN'
    return t_dict


def no_NaN(data, value_list, listed=False):
    if listed is not True:
        for value in value_list:
            if data[value] == 'NaN':
                return False
        return True
    else:
        for line in data:
            for value in value_list:
                if line[value] == 'NaN':
                    return False
        return True


def float_depth(temp, depth=3):
    temp = str(temp)
    n = temp.index('.')
    n += depth
    return temp[0:n]


def update_statisticsCSV():
    cli = dbClient()
    cli.updateData()
    t_dic = data_template()
    listed = []
    for line in cli.ClientData:
        id = line['Serial_No']
        t_dic = data_template()
        t_dic.update(get_head_data(line))
        t_dic.update(get_cart_cost(id))
        t_dic.update(get_request_data(id))
        t_dic.update(get_per_data(t_dic))
        listed.append(t_dic)
    data = type_converter(listed, convert_to_='false')
    return data


def type_to(data, convert_to='string'):
    if convert_to == 'string':
        return str(data)
    if convert_to == 'float':
        return float(data)
    if convert_to == 'int':
        return int(data)


def type_converter(data, listed=True, convert_to_='true'):
    if listed:
        for line in data:
            for key in list(line.keys()):
                if no_NaN(line, [key], listed=False):
                    if convert_to_ == 'true':
                        line[key] = type_to(line[key], convert_to=statistics_key_type[key])
                    else:
                        line[key] = type_to(line[key], convert_to='string')
        return data
    else:
        for key in list(data.keys()):
            if no_NaN(data, [key], listed=False):
                if convert_to_ == 'true':
                    data[key] = type_to(data[key], convert_to=statistics_key_type[key])
                else:
                    data[key] = type_to(data[key], convert_to='string')
        return data


def get_head_data(line):
    t_dic = {}
    head = ['Serial_No', 'IP', 'Manufacture', 'Model']
    for data in head:
        t_dic[data] = line[data]
    return t_dic


def get_cart_cost(id):
    spec = dbClientSpecs()
    data = spec.getEntry('id', id)
    t_dic = {}
    if data['CartBK'] != 'NaN':
        t_dic['CostBK'] = TONER_COST_DICT[data['CartBK']][1]
    if no_NaN(data, ['CartC', 'CartM', 'CartY']):
        temp = 0
        for cart in ['CartC', 'CartM', 'CartY']:
            temp += TONER_COST_DICT[data[cart]][1]
        temp = temp / 3
        t_dic['CostCYM'] = float_depth(temp)
    return t_dic


def get_request_data(id):
    db = dbRequest(id)
    t_dic = {}
    start = db.ClientData[0]
    rest = db.ClientData[1::]
    last = db.ClientData[-1]
    x = dt.datetime.now() - dt.datetime.fromisoformat(start['Time_Stamp'])
    t_dic['DaysTotal'] = x.days
    for data_set in [['TonerBK'], ['TonerC', 'TonerM', 'TonerY']]:
        if no_NaN(db.ClientData, data_set, listed=True):
            value = 0
            for data in data_set:
                n = int(start[data])
                for line in rest:
                    if int(line[data]) < n:
                        value += n - int(line[data])
                    n = int(line[data])
                if 'BK' in data:
                    if value != 0:
                        t_dic['UsedBK'] = value
                    value = 0
                else:
                    if value != 0:
                        t_dic['UsedCYM'] = value
    for data_set in [['Printed_BW', 'Copied_BW'], ['Printed_BCYM', 'Copied_BCYM']]:
        string = data_set[0].split('_')
        string = string[1]
        temp = 0
        for data in data_set:
            if no_NaN(db.ClientData, [data], listed=True):
                temp += int(last[data]) - int(start[data])
        if 'BW' in string and temp > 0:
            t_dic['PagesBK'] = temp
        if 'BCYM' in string and temp > 0:
            t_dic['PagesCYM'] = temp
    return t_dic


def get_per_data(data):
    t_dic = copy.deepcopy(data)
    if no_NaN(t_dic, ['PagesBK', 'UsedBK']):
        pages = int(t_dic['PagesBK'])
        value = int(t_dic['PagesBK']) / t_dic['DaysTotal']
        t_dic['PagesBK_daily'] = float_depth(value)
        if no_NaN(t_dic, ['PagesCYM', 'UsedCYM']):
            pages += int(t_dic['PagesCYM'])
            value = int(t_dic['PagesCYM']) / t_dic['DaysTotal']
            t_dic['PagesCYM_daily'] = float_depth(value)
            value = int(t_dic['UsedCYM']) / t_dic['DaysTotal']
            value = value / 3
            t_dic['UsedCYM_daily'] = float_depth(value)
        if int(t_dic['UsedBK']) != 0:
            value = 100 / int(t_dic['UsedBK']) * pages
            t_dic['PagesPerBK'] = float_depth(value)
            value = int(t_dic['UsedBK']) / t_dic['DaysTotal']
            t_dic['UsedBK_daily'] = float_depth(value)
    if no_NaN(t_dic, ['PagesCYM', 'UsedCYM']):
        pages = t_dic['PagesCYM']
        if int(t_dic['UsedCYM']) != 0:
            value = 100 / int(t_dic['UsedCYM']) * pages
            t_dic['PagesPerCYM'] = float_depth(value)
    if no_NaN(t_dic, ['PagesPerBK', 'CostBK']):
        value = float(t_dic['CostBK']) / float(t_dic['PagesPerBK'])
        t_dic['CostPerBK'] = float_depth(value, depth=4)
    if no_NaN(t_dic, ['PagesPerCYM', 'CostCYM']):
        value = float(t_dic['CostCYM']) / float(t_dic['PagesPerCYM'])
        t_dic['CostPerCYM'] = float_depth(value, depth=4)
    return t_dic


def to_average(data_list):
    n = len(data_list)
    if n == 0:
        return None
    else:
        val = sum(data_list) / n
    return float_depth(val, depth=4)


class dbExcel(object):
    def __init__(self):
        csv = fr'{ROOT}\excel_sheets\recent_stats.csv'
        _for_ini = (False,
                    csv,
                    [],
                    'Serial_No'
                   )
        if _for_ini[0]:
            self.TimeStamps = True
        else:
            self.TimeStamps = False
        self.CSV = _for_ini[1]
        self.Exel = self.CSV.replace('.csv', '.xlsx')
        data = data_dict_template()
        data = get_recent_data(data)
        head = list(data[0].keys())
        head.append('ID')
        head.append('Statistics')
        head.extend(header['ext'])
        self.Header = head
        self.Entry_ID = _for_ini[3]
        self.ClientData = data
        self.ClientPack = ([], ({}))
        self.Empty = False
        if self.CSV:
            self.Empty = self.create_file()

    def create_file(self):
        if os.path.exists(f'{self.CSV}') is not True:
            with open(f'{self.CSV}', 'x', newline='') as csvfile:
                file_writer = csv.DictWriter(csvfile, fieldnames=self.Header)
                file_writer.writeheader()
            return True
        else:
            return False

    def update_csv(self):
        data = update_statisticsCSV()
        statistic_db = dbStats()
        for line in data:
            statistic_db.addEntry(line)

    def update_excel(self):
        self.update_csv()
        data = data_dict_template()
        self.ClientData = get_recent_data(data)
        stats = dbStats()
        seperator = {'Statistics': '|'}
        for client in self.ClientData:
            client.update(seperator)
            for stat_data in stats.ClientData:
                if client['Serial_No'] == stat_data['Serial_No']:
                    client.update(stat_data)
        with open(self.CSV, 'w', newline='') as client_csv:
            writeing = csv.DictWriter(client_csv, fieldnames=self.Header)
            writeing.writeheader()
            writeing.writerows(self.ClientData)
            print('updated CSV')
        file = pd.read_csv(self.CSV, encoding='unicode_escape')
        file.to_excel(self.Exel, index=None, header=True)


def export_data_to_excel():
    create_stat_model_groups()
    xlsx = dbExcel()
    xlsx.update_excel()


def create_stat_model_groups():
    stats = dbStats()
    arr = []
    models = []
    for line in stats.ClientData:
        if line['Model'] not in models:
            models.append(line['Model'])
    for model in models:

        data_set = []
        for line in stats.ClientData:
            if line['Model'] == model:
                data_set.append(line)
        t_dic = {'Model': model, 'num': len(data_set)}
        for key in statistics_variable_grouping_method.keys():
            for value in statistics_variable_grouping_method[key]:
                try:
                    t_dic[value] = model_group_method(data_set, key, value)
                except:
                    t_dic[value] = 'invalid'
        arr.append(t_dic)
    model_to_datasheet(arr)


def model_group_method(data_set, method, value):
    temp = []
    for line in data_set:
        if line[value] != 'NaN':
            temp.append(float(line[value]))
    if method == 'sum_val':
        return float_depth(sum(temp), depth=4)
    elif method == 'single_val':
        return temp[0]
    elif method == 'average_val':
        return float_depth(sum(temp) / len(temp), depth=4)


def model_to_datasheet(arr):
    csv_file = fr'{ROOT}\excel_sheets\recent_model_stats.csv'
    excel_file = fr'{ROOT}\excel_sheets\recent_model_stats.xlsx'
    stat_group = dbStatsGroup()
    stat_group.ClientData = arr
    stat_group.updateCSV()
    file = pd.read_csv(csv_file, encoding='unicode_escape')
    file.to_excel(excel_file, index=None, header=True)


if __name__ == '__main__':
    arr = create_stat_model_groups()
