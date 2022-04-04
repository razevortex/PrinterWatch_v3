from Packages.RequestHandle import *
from Packages.SubPkg.foos import running, get_recent_data, data_dict_to_store
from Packages.SubPkg.const.ConstantParameter import data_dict_template, run_interval
from Packages.SubPkg.csv_handles import *
import time


def coffee_break(min, start):
    sec = int(min * 60)
    running_for = time.time() - start
    early = running_for - sec
    print('run & early', running_for, early)
    t_dic = get_pending_ip()
    try_again = {}
    for key, val in t_dic.items():
        cli = {'IP': key}
        get = ClientGet(cli)
        data = get.snmp_run_main()
        print(data)
        if data_dict_to_store(data) is not True:
            count = int(val) + 1
            try_again[key] = count
    print(try_again)
    update_ip_form(try_again)
    if early < 0:
        print(f'doin´ ma {early / 60} minute coffee  break!')
        early = early * -1
        time.sleep(early)


while running(True):
    start = time.time()
    clients = dbClient()
    clients.updateData()
    listed = clients.ClientData
    progress = 0

    for cli in listed:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(f'request cycle progress : {progress}/{len(listed)}')
        get = ClientGet(cli)

        data = get.snmp_run_main()
        print(data)
        data_dict_to_store(data)
        progress += 1
    coffee_break(run_interval, start)

