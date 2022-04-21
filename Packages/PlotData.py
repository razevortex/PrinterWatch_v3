import copy

from Packages.SubPkg.csv_handles import *
from Packages.SubPkg.foos import *
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as opy
from Packages.SubPkg.foos import list_of_dicts_sorting as lods


def filteredTableContent(filter, json=True, **kwargs):
    cli = dbClient()
    cli.updateData()
    if filter == '' and json is not True:
        arr = []
        for line in cli.ClientData:
            arr.append(line['Serial_No'])
        return get_timetrack_dict(arr)
    else:
        spec = dbClientSpecs()
        spec.updateData()
        t_list = []
        keys = ['Serial_No', 'IP', 'Manufacture', 'Model', 'Toner_Fill', 'Location', 'Contact', 'Notes']
        for client in cli.ClientData:
            t_dict = {}
            for _client in spec.ClientData:
                if client['Serial_No'] == _client['Serial_No']:
                    t_dict = client
                    t_dict.update(_client)
            cut_dict = {}
            for key in keys:
                if key == 'Toner_Fill':
                    cut_dict[key] = string_recent_toner_fill(t_dict)
                else:
                    cut_dict[key] = t_dict[key]
                cut_dict['status'] = string_recent_status(t_dict)
            cut_dict['ID'] = cut_dict['Serial_No']
            override = LibOverride()
            cut_dict = override.updateDict(cut_dict)
            if json:
                if 'WJW' in cut_dict['Serial_No']:
                    sn = cut_dict['Serial_No']
                    cut_dict['Serial_No'] = '<a href="https://tool.wjwgmbh.de/index.php/panel/showItem/*" target="_blank"> * </a>'.replace('*', sn)

            if filter == '':
                t_list.append(cut_dict)
            else:
                for val in cut_dict.values():
                    if type(val) == list:
                        for sub in val:
                            if filter.casefold() in sub.casefold():
                                t_list.append(cut_dict)
                    else:
                        if filter.casefold() in val.casefold():
                            t_list.append(cut_dict)
                            break
        if json is not False:
            return data_struc4JSON(t_list)
        else:
            arr = []
            for line in t_list:
                arr.append(line['Serial_No'])
            return get_timetrack_dict(arr)

def data_struc4JSON(dic_list):
    result_list = []
    for entry in dic_list:
        t_dic = {'sno': entry['Serial_No']}
        t_dic['id'] = entry['ID']
        t_dic['device'] = f'{entry["Manufacture"]} {entry["Model"]}'
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
        t_dic['toner'] = entry['Toner_Fill']

        string = entry['status']
        t_dic['status'] = string if len(string) < 12 else string[:11]

        if entry['Notes'] != 'NaN':
            t_dic['notes'] = entry['Notes']
        else:
            t_dic['notes'] = ''
        result_list.append(t_dic)
    return result_list


def string_carts(dic):
    string = ''
    for cart in ['CartBK', 'CartC', 'CartM', 'CartY']:
        if dic[cart] != 'NaN':
            if string != '':
                string += ', '
            string += dic[cart]
    return string


def string_recent_toner_fill(dic):
    id = dic['Serial_No']
    data = dbRequest(id)
    try:
        recent = data.ClientData[-1]
        arr = []
        for key in recent.keys():
            if key.startswith('Toner'):
                if recent[key] != 'NaN':
                    arr.append(recent[key])
                else:
                    arr.append('')
        arr.append(string_carts(dic))
        return arr
    except:
        return ''


def string_recent_status(dic):
    id = dic['Serial_No']
    data = dbRequest(id)
    try:
        recent = data.ClientData[-1]
        return recent['Status_Report']
    except:
        return ''

template = {'TonerBK': 0, 'TonerC': 0, 'TonerM': 0, 'TonerY': 0, 'Printed_BW': 0, 'Printed_BCYM': 0, 'Copied_BW': 0, 'Copied_BCYM': 0}

def calculate_diff(key, old, new, diff):
    if key.startswith('Toner'):
        if int(new[key]) <= int(old[key]):
            diff[key] = int(old[key]) - int(new[key])
    if key.endswith('BW'):
        diff['BW'] = int(new[key]) - int(old[key])
    if key.endswith('BCYM'):
        diff['BCYM'] = int(new[key]) - int(old[key])
    old[key] = new[key]
    return old, diff

'''
insert a list of Serial No 
'''
def get_timetrack_dict(printer_set, sort='continues'):
    data_sink = []
    for client in printer_set:
        data = dbRequest(client)
        t_dic = {'TonerBK': 0, 'TonerC': 0, 'TonerM': 0, 'TonerY': 0, 'BW': 0, 'BCYM': 0}
        hold = {}
        print(client)
        for key in template.keys():
            first = data.ClientData[0]
            hold[key] = first[key]
        for line in data.ClientData[1:]:
            diff_dic = copy.deepcopy(t_dic)
            for key in template.keys():
                if hold[key] != 'NaN':
                    hold, diff_dic = calculate_diff(key, hold, line, diff_dic)
            data_sink.append((line['Time_Stamp'], diff_dic))
    if sort == 'continues':
        timetrack = []
        t_dic = {'Time_Stamp': '', 'TonerBK': 0, 'TonerC': 0, 'TonerM': 0, 'TonerY': 0, 'BW': 0, 'BCYM': 0}
        data_sink = sorted(data_sink)
        daily = []
        days = []
        for line in data_sink:
            string = line[0]
            date = string.split(' ')[0]
            daily.append((date, line[1]))
            days.append(date)
        days = list(set(days))
        t_dataset = []
        for day in days:
            daily_sum = {'TonerBK': 0, 'TonerC': 0, 'TonerM': 0, 'TonerY': 0, 'BW': 0, 'BCYM': 0}
            for data in daily:
                if data[0] == day:
                    val = data[1]
                    for key in daily_sum.keys():
                        daily_sum[key] += val[key]
            t_dataset.append((day, daily_sum))
        line_plot_data = {'index': [], 'pages': []}
        val = 0
        for line in sorted(t_dataset):
            line_plot_data['index'].append(line[0])
            t = line[1]
            val += t['BW'] + t['BCYM']
            line_plot_data['pages'].append(val)
        return line_plot_data['index'], line_plot_data['pages']

if __name__ == '__main__':
    print(filteredTableContent('', json=False))


