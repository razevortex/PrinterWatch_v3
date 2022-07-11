import os
import subprocess
from Packages.SubPkg.foos import *
import datetime as dt
from Packages.RequestHandle import *
PATH = '/home/razevortex/django_printerwatch/'


def run_ext():
    os.system('python /home/razevortex/django_printerwatch/test/run.py')


def new_client(ip):
    dic = {'IP': ip}
    get = ClientGet(dic)
    data = get.snmp_run_main()
    data['Serial_No'] = dt.datetime.now()
    print(data)


if __name__ == '__main__':
    run_background_requests(0)
