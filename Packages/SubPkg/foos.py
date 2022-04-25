'''if __name__ == '__main__':
    from const.ConstantParameter import *
    from csv_handles import *
    from Dev.data_validation import DataValidation
else:'''
'''from .const.ConstantParameter import *
from .Brother import *
from .Kyocera import *
from .csv_handles import *'''
from Packages.SubPkg.const.ConstantParameter import *
from Packages.SubPkg.Brother import *
from Packages.SubPkg.Kyocera import *
from Packages.SubPkg.csv_handles import *
import re
from functools import wraps
import datetime as dt
import subprocess as sp
from subprocess import Popen

# from .Dev.processing_time import FooRunTime
''' for checking the run time of a function uncomment the import above and use the wrapper @FooRunTime on the function
@FooRunTime
def foo():
    return None
'''

#
#                                       END OF IMPORT

def update_override(wjw_dic_list):
    cli = dbClient()
    cli.updateData()
    arr = []
    for line in cli.ClientData:
        arr.append(line['Serial_No'])
    oRide = LibOverride()
    or_list = []
    non_list = []
    for dic in wjw_dic_list:
        if dic['Serial_No'] in arr:
            id = dic['Serial_No']
            dic['Serial_No'] = dic['WJW']
            for key in dic.keys():
                if dic[key] == 'default' or dic[key] == 'aaaa_wjw_allgemain noname':
                    dic[key] = ''
            oRide.addEntry(id, dic)
            or_list.append(dic)
        else:
            non_list.append(dic)
    print(or_list)
    print(non_list)
    print(oRide.ClientData)

# get_recent_data is used up on start to get the last stored data of the monitored clients
def get_filter():
    client = dbClient()
    client.updateData()
    filter_dic = {'Manufacture': [], 'Model': []}
    for line in client.ClientData:
        for x in ['Manufacture', 'Model']:
            filter_dic[x].append(line[x])


def get_recent_data(temp):
    clients = dbClient()
    client_list_of_dicts = []
    # checking if there are already stored data or is it maybe the first run this might get obsolete when a
    # initial setup dialog up on first start gets implemented
    if clients.Empty is not True:
        data = []
        client = dbClient()
        client.updateData()
        for clients in client.ClientData:
            db = dbRequest(clients['Serial_No'])
            temp = db.getEntry('recent')
            clients.update(temp)
            spec = dbClientSpecs()
            spec.updateData()
            temp = spec.getEntry('id', clients['Serial_No'])
            clients.update(temp)
            override = LibOverride()
            if override.getEntry(temp['Serial_No']):
                clients.update(override.getEntry(temp['Serial_No']))
            data.append(clients)
        return data


def list_of_dicts_sorting(list, sort_key):
    def takeKey(elem):
        return elem[1]
    temp = []
    for dict in list:
        temp.append([dict, dict[sort_key]])
    temp.sort(key=takeKey)
    sorted_list = []
    for entry in temp:
        sorted_list.append(entry[0])
    return sorted_list


def running(disable):
    if disable:
        return disable
    else:
        now = dt.datetime.now()
        weekday = now.strftime('%A')
        if weekday == 'Friday':
            working_hours = (now.replace(hour=7, minute=30), now.replace(hour=15))
        else:
            working_hours = (now.replace(hour=7, minute=30), now.replace(hour=16, minute=30))
        if working_hours[0] < now < working_hours[1]:
            return True
        else:
            return False

def run_background_requests(request_active):
    if request_active == False:
        request_active = Popen(["python", "Background_Request.py"], creationflags=sp.CREATE_NEW_CONSOLE)
        return request_active

def check_on_requests(request_active):
    if request_active == False:
        request_active = Popen(["python", "Background_Request.py"], creationflags=sp.CREATE_NEW_CONSOLE)
        return request_active
    else:
        if request_active.poll():
            #print(request_active.poll())
            request_active = False
            return request_active


def method_selector(specs_lib, manufacture, model):
    Specs = specs_lib.getEntry('id', model)
    if manufacture == 'Brother':
        return methodsBrother(Specs['MethodIndex'])


def add_ip(pending, get_class):
    if pending != '':
        ip = pending[0]
        get = get_class(ip)
        data = get.snmp_run_main()
        status = data_dict_to_store(data)
        pending.remove(ip)
        return pending, len(pending), (ip['IP'], status)

def DataValidation(func):
    @wraps(func)
    def data_validation(data):
        #if data is not True:
        #    return False
        reference = data_dict_template()
        if data is None:

            return 'non'
        elif type(data).__name__ is type(reference).__name__:

            return 'typ'
        elif len(data.items()) < len(reference.items()):

            return 'len'
        for key, val in data.items():
            if key not in list(reference.keys()):

                return f'{key} not in reference keys'
            elif val is None or val == '':
                data[key] = 'NaN'
        data_handle = func(data)

        return data_handle
    return data_validation


@DataValidation
def data_dict_to_store(data_dict):
    now = dt.datetime.now()
    data_dict['Time_Stamp'] = now
    client = {}
    request = {}
    specs = {}
    print(f'Client S.n.:{data_dict["Serial_No"]} IP:{data_dict["IP"]} . . . ')
    for key, var in data_dict.items():
        if var is None or var == '' or var is False:
            data_dict[key] = 'NaN'
    for key in header['client_db']:
        client[key] = data_dict[key]
    print(f'data for client.csv: {client}')
    db = dbClient()
    db.addingEntry(client)
    for key in header['request_db']:
        request[key] = data_dict[key]
    print(f'data for its {data_dict["Serial_No"]}.csv: {request}')
    db = dbRequest(data_dict['Serial_No'])
    toner_replaced(db.ClientData[-1], data_dict)
    db.addingEntry(request)
    for key in header['client_specs']:
        specs[key] = data_dict[key]
    print(f'data for client_specs.csv: {specs}')
    db = dbClientSpecs()
    db.addingEntry(specs)
    return True

def toner_replaced(last_line, new_line):
    replaced_toner = {'TonerBK', 'TonerC', 'TonerM', 'TonerY'}
    for key in replaced_toner:
        if new_line[key] != 'NaN':
            if int(new_line[key]) > int(last_line[key]):
                cart = key.replace('Toner', 'Cart')
                temp = add_to_Storage(new_line[cart], "-1", Storage2Dict())
                UpdateStorage(temp)

def calc(store, low):
    new = int(store) - int(low)
    return str(new)


def add_to_Storage(typ, num, db_dict):
    new = int(db_dict[typ]) + int(num)
    db_dict[typ] = str(new)
    return db_dict


def Storage2Dict():
    t_dic = {}
    with open(f'{ROOT}db/cartStorage.txt', 'r') as storage:
        string = storage.readline()
        item_list = string.split(',')
        for item in [entry.split(':') for entry in [t for t in item_list if t != '']]:
            if type(item) == list and len(item) == 2:
                t_dic[item[0]] = item[1]
                print(t_dic)
    return t_dic


def UpdateStorage(dic):
    string = ''
    for key, val in dic.items():
        string += f'{key}:{val},'
    string.rstrip(',')
    with open(f'{ROOT}db/cartStorage.txt', 'w') as storage:
        storage.write(string)


def float_depth(float_num, depth=3):
    try:
        string = str(float_num)
        string += '00000'
        point = string.index('.') + depth
        string = string[0:point]
        return float(string)
    except:
        return float_num


def read_snmp_response(file):
    with open(file) as infile:
        arr = []
        temp = []
        for line in infile:
            line = line.rstrip('\n')
            arr_proc = re.split(' = |::|: ', line)
            temp.append(arr_proc)
        for a in range(0, len(temp)):
            if len(temp[a]) == 4 and temp[a][3]:
                if temp[a][2] == 'STRING':
                    t = (str(temp[a][1]), str(temp[a][3].replace('"', '')))
                    arr.append(t)
                if temp[a][2] == 'Counter32' or temp[a][2] == 'INTEGER':
                    t = (str(temp[a][1]), str(int(re.search(r'\d+', temp[a][3]).group())))
                    arr.append(t)
    return arr


def valid_ip(ip):
    t = ip.split('.')
    num = int(t[0])
    if 100 < num < 255:
        return True
    else:
        return False

def handle_ip_form(input):
    client = dbClient()
    client.updateData()
    already_existing = client.getEntry('col', 'IP')
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    #t = ip_pattern.search(input)[0]
    match = ip_pattern.findall(input)
    if type(match) == list:
        for t in match:
            if t not in already_existing:
                string = f'{t}:0;'
                with open(f'{ROOT}db/includeIP.txt', 'a') as ips:
                    ips.write(string)
    elif type(match) == str:
        if match not in already_existing:
            string = f'{match}:0;'
            with open(f'{ROOT}db/includeIP.txt', 'a') as ips:
                ips.write(string)

'''
def get_pending_ip(to_json=False):
    with open(f'{ROOT}db/includeIP.txt', 'r') as ips:
        data = ips.read()
        split = data.split(';')
        if to_json is not True:
            data = {}
        else:
            data = []
        for t in split:
            if to_json is not True:
                if t != '':
                    temp = t.split(':')
                    data[temp[0]] = temp[1]
            else:
                if t != '':
                    temp = t.split(':')
                    data.append({'IP': temp[0], 'TRIED': temp[1]})
    return data

'''

def get_pending_ip():
    with open(f'{ROOT}db/includeIP.txt', 'r') as ips:
        data = ips.read()
        split = data.split(';')
    arr = []
    for t in split:
        if t != '':
            temp = t.split(':')
            if type(temp) == list and len(temp) == 2:
                dic = {'IP': temp[0], 'TRIED': temp[1]}
                arr.append(dic)
    return arr

def update_ip_form(ip_arr):
    string = ''
    for ip_dict in ip_arr:
        string += f'{ip_dict["IP"]}:{ip_dict["TRIED"]};'
    with open(f'{ROOT}db/includeIP.txt', 'w') as ips:
        ips.write(string)

def test(file):
    string = ''
    with open(file, 'r') as t:
        for l in t:
            string += l
    with open(f'{ROOT}db/includeIP.txt', 'a') as ips:
        ips.write(string)

def import_ip_file(file):
    client = dbClient()
    client.updateData()
    already_existing = client.getEntry('col', 'IP')
    # opening and reading the file
    with open(file) as txt:
        string = txt.readlines()

    # declaring the regex patterns for IP addresses
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    valid_store = []
    # extracting the IP addresses
    temp = []
    for line in string:
        line = line.rstrip()
        print(line)
        x = True
        while x:
            try:
                t = ip_pattern.search(line)[0]
                print(t)
                temp.append(t)
                line = line.replace(t, '')
            except:
                x = False
    for ip in temp:
        if valid_ip(ip):
            if ip not in already_existing['IP']:
                valid_store.append(ip)
    return list(set(valid_store))

def calculate_diff(key, old, new, diff):
    if key.startswith('Toner'):
        if new[key] <= old[key]:
            diff[key] = old[key] - new[key]
    if key.endswith('BW') or key.endswith('BCYM'):
        diff[key] = new[key] - old[key]
    old[key] = new[key]
    return old, diff

def write_timestamp_to_com():
    now = dt.datetime.now()
    with open(f'{ROOT}static/com/last_update.txt', 'w') as update:
        update.write(str(now))
    return now

def timestamp_from_com(diff=10):
    with open(f'{ROOT}static/com/last_update.txt', 'r') as update:
        string = update.read()
    string = string.strip()
    now = dt.datetime.now()
    if dt.datetime.fromisoformat(string) + dt.timedelta(minutes=diff) > now:
        return 1, string
    else:
        return 0, string

#if __name__ == '__main__':
#    update_override(wjw_data_dic)
