import sys
#sys.path.insert(0, '/home/razevortex/PycharmProjects/PrinterWatch_v3')

from printerwatch.PrinterRequest.main import *
from printerwatch.GlobalClasses import TaskInterval
from printerwatch.PrinterObject.main import PrinterLib

def basic_run():
    pLib = PrinterLib()
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

