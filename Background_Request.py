from Packages.RequestHandle import *
from Packages.SubPkg.foos import *
from Packages.SubPkg.const.ConstantParameter import data_dict_template, run_interval
from Packages.SubPkg.csv_handles import *
import time
import datetime as dt


def coffee_break(min, start):
    sec = int(min * 60)
    running_for = time.time() - start
    early = running_for - sec
    print('run & early', running_for, early)
    arr = get_pending_ip()
    t_arr = []
    for t_dic in arr:
        cli = {'IP': t_dic['IP']}
        get = ClientGet(cli)
        data = get.snmp_run_main()
        if data_dict_to_store(data) is not True:
            t_dic['TRIED'] = int(t_dic['TRIED']) + 1
            t_arr.append(t_dic)
    update_ip_form(t_arr)
    if early < 0:
        now = write_timestamp_to_com()
        print(f'wrote {now} to com')
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

