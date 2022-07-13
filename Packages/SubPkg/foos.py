import os.path
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


def float_depth(float_num, depth=3):
    try:
        string = str(float_num)
        string += '00000'
        point = string.index('.') + depth
        string = string[0:point]
        return float(string)
    except:
        return float_num


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


def run_background_requests(last_update):
    if timestamp_from_com(diff=last_update, with_string=False) is not True:
        sp.call(["gnome-terminal", "-x", "python", f"{ROOT}Background_Request.py"])


def method_selector(specs_lib, manufacture, model):
    Specs = specs_lib.getEntry('id', model)
    if manufacture == 'Brother':
        return methodsBrother(Specs['MethodIndex'])


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
    try:
        toner_replaced(db.ClientData[-1], data_dict)
    except:
        print('not enough entries for foo toner replacement')
    db.addingEntry(request)
    for key in header['client_specs']:
        specs[key] = data_dict[key]
    print(f'data for client_specs.csv: {specs}')
    db = dbClientSpecs()
    db.addingEntry(specs)
    return True


def dict_key_translate(key_translation, dic, way=(0, 1)):
    b, a = way
    t_dic = {}
    try:
        for key_pair in key_translation:
            t_dic[key_pair[a]] = dic[key_pair[b]]
    except:
        for key_pair in key_translation:
            t_dic[key_pair[b]] = dic[key_pair[a]]
    return t_dic

'''
Functions handling CartridgeStorage 
'''

def toner_replaced(last_line, new_line):
    replaced_toner = {'TonerBK', 'TonerC', 'TonerM', 'TonerY'}
    for key in replaced_toner:
        if new_line[key] != 'NaN':
            if int(new_line[key]) > int(last_line[key]):
                cart = key.replace('Toner', 'Cart')
                temp = add_to_Storage(new_line[cart], "-1", Storage2Dict())
                UpdateStorage(temp)


def add_to_Storage(typ, num, db_dict):
    new = int(db_dict[typ]) + int(num)
    db_dict[typ] = str(new)
    return db_dict


def data_view_request_CartStorage(data_dict):
    t_dic = Storage2Dict()
    if data_dict['cart'] in list(t_dic.keys()):
        t_dic[data_dict['cart']] = int(data_dict['num']) + int(t_dic[data_dict['cart']])
        UpdateStorage(t_dic)


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


'''
END Cartridge Storage
START User Config / User Default Values (Forms)
'''

def create_new_conf(user):
    if not os.path.exists(f'{ROOT}user/{user}Config.txt'):
        with open(f'{ROOT}user/defaultConfig.txt', 'r') as default:
            lines = [line.strip() + '\n' for line in default.readlines()]
        with open(f'{ROOT}user/{user}Config.txt', 'w') as new_file:
            new_file.writelines(lines)
        os.chmod(f'{ROOT}user/{user}Config.txt', 0o777)


def read_conf(user, page):
    t_dic = {}
    string = ''
    create_new_conf(user)
    with open(f'{ROOT}user/{user}Config.txt', 'r') as conf:
        for line in conf.readlines():
            if page in line:
                string = line.replace(f'{page}=', '')
    if string != '':
        arr = [[key.strip(), val.strip()] for key, val in [entry.split(':') for entry in string.split(';')]]
        for pair in arr:
            t_dic[pair[0]] = pair[1]
    return t_dic


def write_conf(user, page, dict):
    newline = f'{page}='
    for key, val in dict.items():
        newline += f'{key}:{val};'
    newline = newline.rstrip(';')
    arr = []
    line_exists = False
    with open(f'{ROOT}user/{user}Config.txt', 'r') as conf:
        for line in conf.readlines():
            if page in line:
                arr.append(newline)
                line_exists = True
            else:
                arr.append(line.strip())
        if line_exists is not True:
            arr.append(newline)
    with open(f'{ROOT}user/{user}Config.txt', 'w') as conf:
        conf.writelines(line + '\n' for line in arr)

'''
END User Config
START Function for Handling IPs
'''


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
    already_existing = [line['IP'] for line in client.ClientData]
    #already_existing = client.getEntry('col', 'IP')
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

def remove_ip(ip):
    arr = get_pending_ip()
    t_arr = []
    for val in arr:
        if ip != val['IP']:
            t_arr.append(val)
    update_ip_form(t_arr)


def calculate_diff(key, old, new, diff):
    if key.startswith('Toner'):
        if new[key] <= old[key]:
            diff[key] = old[key] - new[key]
    if key.endswith('BW') or key.endswith('BCYM'):
        diff[key] = new[key] - old[key]
    old[key] = new[key]
    return old, diff

'''
END IP Functions
START Last Background Request Run Timestamp 
'''

def write_timestamp_to_com():
    now = dt.datetime.now()
    with open(f'{ROOT}static/com/last_update.txt', 'w') as update:
        update.write(str(now))
    return now

def timestamp_from_com(diff=10, with_string=True):
    with open(f'{ROOT}static/com/last_update.txt', 'r') as update:
        string = update.read()
    string = string.strip()
    now = dt.datetime.now()
    if with_string is not False:
        if dt.datetime.fromisoformat(string) + dt.timedelta(minutes=diff) > now:
            return 1, string
        else:
            return 0, string
    else:
        if dt.datetime.fromisoformat(string) + dt.timedelta(minutes=diff) > now:
            return True
        else:
            return False



if __name__ == '__main__':
    handle_ip_form('172.20.12.189')
    print(get_pending_ip())
    #update_override(wjw_data_dic)
