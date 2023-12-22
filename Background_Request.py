import bs4
from webinterface._Packages.GlobalClasses import TaskInterval
from webinterface._Packages.PrinterObject.main import *
from webinterface._Packages.PrinterRequest.main import PrinterRequest as req

back_log_size = 100


def report_msg(msg: str):
    if msg in ('start', 'stop'):
        return f"run {msg} at: {dt.now().strftime('%d.%m.%Y %H:%M:%S')}"
    else:
        return f"Exception at: {dt.now().strftime('%d.%m.%Y %H:%M:%S')} => during: {msg}\n"


def report(msg):
    lines = []
    if path.exists('/home/razevortex/PrinterWatch_v3/bg_err_log.txt'):
        with open('/home/razevortex/PrinterWatch_v3/bg_err_log.txt', 'r') as f:
            lines = [line for line in f.readlines()]
    if len(lines) > back_log_size:
        lines = lines[-back_log_size:]
    lines.append(report_msg(msg))
    with open('/home/razevortex/PrinterWatch_v3/bg_err_log.txt', 'w') as f:
        f.write(''.join(lines))


def on_watch():
    report('start')
    for ip, serial in [(obj.ip, obj.serial_no) for obj in pLib.get_search('*', result=object) if obj.active]:
        try:
            req(ip)
        except:
            report(serial)
    report('stop')


on_watch()
