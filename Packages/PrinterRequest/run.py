import sys
sys.path.insert(0, '/home/razevortex/PycharmProjects/PrinterWatch_v3')

from Packages.PrinterRequest.main import *
from Packages.GlobalClasses import TaskInterval


def basic_run():
    print(pLib.obj[0])
    i, n = 0, len([obj for obj in pLib.obj if obj.active])
    for serial_no, ip in [(obj.serial_no, obj.ip) for obj in pLib.obj if obj.active]:
        print(f'run: {i}/{n}')
        i += 1
        try:
            PrinterRequest(ip)
        except:
            print(f'{serial_no} with {ip} request failed')

task = {'basic_run': [300, basic_run]}
Events = TaskInterval(**task)

Events.trigger()

