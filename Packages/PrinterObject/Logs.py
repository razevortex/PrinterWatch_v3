from datetime import datetime as dt
from json import dumps, loads
from os import path
from pathlib import Path

from Packages.PrinterObject.StaticVar import LOG_DIR


def timestamp():
    return dt.now().strftime('%d.%m.%Y %H:%M:%S')

class Logger(object):
    def __init__(self, serial_no):
        self.file = Path(LOG_DIR, f'{serial_no}.json')
        self.log = self._read()

    def _read(self):
        if path.exists(self.file):
            with open(self.file, 'r') as f:
                return loads(f.read())
        else:
            return []

    def _write(self):
        with open(self.file, 'w') as f:
            f.write(dumps(self.log))

    def logging(self, key, old, new):
        if old != new:
            self.log.append([timestamp(), key, old, new])
            print(self.log)
            self._write()
