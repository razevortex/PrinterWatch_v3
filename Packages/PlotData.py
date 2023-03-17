from Packages.StrucData import *
from Packages.SubPkg.csv_handles import *
from datetime import datetime as dt

cli = dbClient()
cli.updateData()
print(cli.ClientData)
cli_ids = [line['Serial_No'] for line in cli.ClientData]
print(cli_ids)
test_id = 'L875533842'

#data = DataSet(test_id)
#head = data.get_all(customized=True)


def create_obj(obj_id):
    data = DataSet(obj_id)
    t_obj = basic_head(data.get_all(customized=True))
    t_obj['MONTHLY_AVG'] = avg_month_calc(data)
    t_obj['AVG_PER_MONTH'] = avg_per_month(t_obj['MONTHLY_AVG'])
    #print(t_obj)
    cout(t_obj)
    return t_obj

def prepair_chart_data(val):
    t_label = []
    bw_dataset = {'label': 'BW', 'data': [], 'backgroundColor': '#888888', 'borderColor': '#000000'}
    col_dataset = {'label': 'BCYM', 'data': [], 'backgroundColor': '#888888', 'borderColor': '#0088FF'}
    for label, val_set in val:
        t_label.append(label)
        bw_dataset['data'].append(val_set[bw_dataset['label']])
        col_dataset['data'].append(val_set[col_dataset['label']])
    return {'labels': t_label, 'datasets': [bw_dataset, col_dataset]}


def prepair_chart_obj(obj):
    details = info_box(obj)
    conf = {'type': 'bar',
            'data': prepair_chart_data(obj['MONTHLY_AVG']),
            'options': {'plugins': {'title': {'display': True, 'text': obj['ID']}},
                       'scales': {'x': {'stacked': True}, 'y': {'stacked': True}}}}
    print(details)
    print(conf)
    return [details, conf]
def info_box(obj):
    string = '<p>'
    head = [f"{key} : {val}" for key, val in obj.items() if 'AVG' not in key]
    for line in head:
        string += line
        string += '</br>'
    string += f'avg cost per Page = {obj["AVG_PAGE_COST"]} </br>'
    string += f'Overall monthly AVG = {obj["AVG_PER_MONTH"]} Pages </p>'
    return string

def cout(obj):
    print('')
    print('<------------------------------------------------------------->')
    print('')
    head = [f"{key}*TAB*{val}" for key, val in obj.items() if 'AVG' not in key]
    [print(t_item) for t_item in head]
    print('')
    #print(f'Average Page Cost {obj["AVG_PAGE_COST"]}')
    print('')
    print('List of Month with AVG:')
    #print('Date, BW, BCYM, Total')
    h_arr = [f'{add_spaceing(val)}*TAB*' for val in ('Date', 'BW', 'BCYM', 'Total')]
    t_str = ''
    for val in h_arr:
        t_str += val
    #print('Date*TAB*BW*TAB*BCYM*TAB*Total')
    print(t_str)
    for date, val_dict in obj['MONTHLY_AVG']:
        t_list =[]
        date = date.replace(' ', '')
        if len(date) <= 6:
            date = f'0{date}'
        t_list.append(date.replace(' ', ''))
        for key in ('BW', 'BCYM', 'Total'):
            try:
                t_list.append(val_dict[key])
            except:
                t_list.append('-')
        t_string = f'{t_list[0]} *TAB*'
        for val in t_list[1:]:
            #spaceing = ''
            #if len(str(val)) < 4:
            #    for i in range(len(str(val)), 5):
            #        spaceing += ' '
            t_string += f'{add_spaceing(val)}*TAB*'
        print(t_string)
    print('')
    try:
        print(f'Page-€*TAB*{obj["AVG_PAGE_COST"]["BK"]}*TAB*{obj["AVG_PAGE_COST"]["CYM"]}')
    except:
        print('No avg € per page data avaible')
    #print(list(obj['MONTHLY_AVG'][0].keys()))
    #[print(list(line.values())) for line in obj['MONTHLY_AVG']]
    #print('')
    #print(f'In {len(obj["MONTHLY_AVG"])} months:')
    print(f'{obj["AVG_PER_MONTH"]} Pages avg per month')

def add_spaceing(val):
    spaceing = ''
    if len(str(val)) < 7:
        for i in range(len(str(val)), 8):
            spaceing += ' '
    return f'{val}{spaceing}'

def basic_head(head):
    t_dic = {}
    t_dic['ID'] = head['Serial_No'] if head['Serial_No'] != 'NaN' else head['ID']
    t_dic['LOCAL'] = f"{head['Contact']} / {head['Location']}"
    t_dic['IP'] = head['IP']
    t_dic['DEVICE'] = head['Device']
    try:
        t_dic['AVG_PAGE_COST'] = {'BK': f"{head['CostPerBK']}€", 'CYM': f"{head['CostPerCYM']}€"}
    except:
        t_dic['AVG_PAGE_COST'] = 'No Data Avaible'
    #print(t_dic)
    return t_dic


def avg_month_calc(data):
    page_keys = (('Printed_BW', 'Copied_BW'), ('Printed_BCYM', 'Copied_BCYM'))
    t_dict = {}
    for entry in data.Data:
        time_stamp = dt.strptime(entry[0].split(' ')[0], "%Y-%m-%d")
        time_key = f'{time_stamp.month}, {time_stamp.year}'
        if time_key not in list(t_dict.keys()):
            t_dict[time_key] = (entry[1], entry[1])
        else:
            t_dict[time_key] = (t_dict[time_key][0], entry[1])
    t_arr = []
    for key, val in t_dict.items():
        #print(key)
        first, last = val
        t_avg_dict = {}
        for key_pair in page_keys:
            avg_val = 0
            for k in key_pair:
                val_key = k.split('_')[1]
                if first[k] != 'NaN' and last[k] != 'NaN':
                    avg_val += last[k] - first[k]
                t_avg_dict[val_key] = avg_val
        t_avg_dict['Total'] = sum(t_avg_dict.values())
        t_arr.append((key, t_avg_dict))
    return t_arr


def avg_per_month(monthly_avg_list):
    totals = [month[1]['Total'] for month in monthly_avg_list]
    #print(totals)
    val = sum(totals) // len(totals)
    return val


def walk_all_clients(cli_ids):
    for cli in cli_ids:
        create_obj(cli)
        #prepair_chart_obj(create_obj(cli))


walk_all_clients(cli_ids)
#create_obj(test_id)
#print(data.Statistics)
#cost_stat = dbStats()
#for line in cost_stat.ClientData:
#    if line['Serial_No'] == test_id:
#        print(line)

#data.get_device_data(test_id)
#print(data.Static)
#print(data.Statistics)
'''

t_dict = {}
for entry in data.Data:
    time_stamp = dt.strptime(entry[0].split(' ')[0], "%Y-%m-%d")
    time_key = f'{time_stamp.month}, {time_stamp.year}'
    if time_key not in list(t_dict.keys()):
        t_dict[time_key] = (entry[1], entry[1])
    else:
        t_dict[time_key] = (t_dict[time_key][0], entry[1])

for key, val in t_dict.items():
    print(key)
    first, last = val
    t_avg_dict = {}
    for key_pair in page_keys:
        avg_val = 0
        for k in key_pair:
            val_key = k.split('_')[1]
            if first[k] != 'NaN' and last[k] != 'NaN':
                avg_val += last[k] - first[k]
            t_avg_dict[val_key] = avg_val
    print(t_avg_dict)
'''