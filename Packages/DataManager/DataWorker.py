from Packages.DataManager.DataSet import DataBase
from datetime import datetime as dt, timedelta

db = DataBase()
befor, past = [dt.strptime(input(f'{t} (in format dd.mm.yy):'), '%d.%m.%y') for t in ('befor', 'past')]
keys = ['Prints']
test_set, dates = db.get_tracker_sets(befor=befor, past=past, keys=keys)


class DataObject(object):
    def __init__(self, befor=None, past=None, keys='*'):
        self.date, self.data = db.get_tracker_sets(befor=befor, past=past, keys=keys)

    def merge_keys(self, merge_name, keys='*'):
        temp = {}
        for key, data in self.data.items():
            temp[merge_name] = [sum(zipped) for zipped in zip([v for k, v in data.items() if k in keys or keys == '*'])]