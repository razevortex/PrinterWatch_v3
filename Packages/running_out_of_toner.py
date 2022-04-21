from Packages.SubPkg.csv_handles import *
from Packages.SubPkg.foos import float_depth
from Packages.SubPkg.const.ConstantParameter import ROOT

def reverse_run(req_list, val, toner):
    x = 0
    for line in req_list[-1::-1]:
        if line[toner] == val[toner]:
            x = dt.datetime.now() - dt.datetime.fromisoformat(line['Time_Stamp'])
        else:
            if x == 0:
                return x
            else:
                return int(x.days)

def brother_calculated_precision(req_list, stat, key):
    if key.endswith('BK'):
        stat_daily = float(stat['UsedBK_daily'])
    else:
        stat_daily = float(stat['UsedCYM_daily'])
    latest_val = req_list[-1]
    days = reverse_run(req_list, latest_val, key)
    first_entry = req_list[0]
    total_days = dt.datetime.now() - dt.datetime.fromisoformat(first_entry['Time_Stamp'])
    try:
        if total_days.days > 30:
            used_since = days * stat_daily
            if used_since > 10:
                return 9
            else:
                return used_since
        else:
            return 0
    except:

        return 0

def get_used_toner_types():
    arr = []
    spec = dbClientSpecs()
    for line in spec.ClientData:
        for key in line.keys():
           if 'Cart' in key:
               if line[key] != 'NaN':
                   arr.append(line[key])
    t_list = []
    unique_list = list(set(arr))
    sorted_list = sorted(unique_list)
    for cart in sorted_list: #list(set(arr)):
        t_list.append({'cTyp': cart})
    return add_storage(t_list)

def add_storage(data_list):
    arr = []
    store = Storage2Dict()
    for line in data_list:
        line['cStore'] = store[line['cTyp']]
        arr.append(line)
    return arr

'''        for key, val in line.items():
            dic[val] = '0'
        for key, val in line.items():
             = dic[val]
            arr.append(line)
    return arr
'''
def till_then(days):
    toner = {'TonerBK': '', 'TonerC': '', 'TonerM': '', 'TonerY': ''}
    cli = dbClient()
    cli.updateData()
    spec = dbClientSpecs()
    cartrides_needed = []
    needed_dict = {}
    for client in cli.ClientData:
        req = dbRequest(client['Serial_No'])
        t_dic = copy.deepcopy(toner)
        v_dic = copy.deepcopy(toner)
        stats = dbStats()
        for stat in stats.ClientData:
            if stat['Serial_No'] == client['Serial_No']:
                for key in t_dic.keys():
                    if key in ['TonerBK', 'TonerC', 'TonerM', 'TonerY']:
                        calc = 0
                        if client['Manufacture'] == 'Brother':
                            calc = brother_calculated_precision(req.ClientData, stat, key)
                        line = req.ClientData[-1]
                        if line[key] != 'nan' and line[key] != 'NaN':
                            if key.endswith('BK'):
                                if float(int(line[key]) - calc) / float(stat['UsedBK_daily']) < days:
                                    print(client)
                                    print(f"{float_depth(float(int(line[key]) - calc))} % {key} are estimated to run out in "
                                          f"{float_depth(float(int(line[key]) - calc) / float(stat['UsedBK_daily']), depth=2)} days...")
                                    cart = key.replace('Toner', 'Cart')
                                    for line in spec.ClientData:
                                        if line['Serial_No'] == client['Serial_No']:
                                            cartrides_needed.append(line[cart])
                            else:
                                if float(int(line[key]) - calc) / float(stat['UsedCYM_daily']) < days:
                                    print(client)
                                    v_dic[key] = int(line[key]) - calc / float(stat['UsedCYM_daily'])
                                    print(f"{float_depth(float(int(line[key]) - calc))} % {key} estimated to run out in "
                                          f"{float_depth(float(int(line[key]) - calc) / float(stat['UsedCYM_daily']), depth=2)} days...")
                                    cart = key.replace('Toner', 'Cart')
                                    for line in spec.ClientData:
                                        if line['Serial_No'] == client['Serial_No']:
                                            cartrides_needed.append(line[cart])

    key_set = list(set(cartrides_needed))
    for key in key_set:
        needed_dict[key] = cartrides_needed.count(key)
    return needed_dict

def cart_state(days):
    t_arr = []
    low = till_then(days)
    for cart in get_used_toner_types():
        cart['cLow'] = '0'
        cart['cNew'] = cart['cStore']
        if cart['cTyp'] in low.keys():
            cart['cLow'] = low[cart['cTyp']]
            cart['cNew'] = calc(cart['cStore'], cart['cLow'])
        t_arr.append(cart)
    return t_arr


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
    i = 0
    for key, val in dic.items():
        if i > 0:
            string += f',{key}:{val}'
        else:
            string += f'{key}:{val}'
        i += 1
    with open(f'{ROOT}db/cartStorage.txt', 'w') as storage:
        storage.write(string)


if __name__ == '__main__':

    print(Storage2Dict())
    #cart_list = []
    #for line in cart_state(0):
    #    cart_list.append(line['cTyp'])
    #print(cart_list)
