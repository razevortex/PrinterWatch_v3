import copy
from json import dumps

from Packages.GlobalClasses import TaskInterval
from Packages.PrinterObject.main import pLib, cLib, mLib


class DataBase(object):
    def __init__(self):
        self.printer = pLib
        self.printer_models = mLib
        self.cartridges = cLib

    def print_(self):
        print(self.cartridges)
        print(self.printer_models)
        print(self.printer)

    def merged_tracker_data(self, search='*'):
        temp = None
        for obj in self.printer.get_search(search, result='tracker'):
            try:
                if temp is None:
                    temp = obj.data.time_prune()
                else:
                    temp = temp + obj.data.time_prune()
            except:
                    print('err => merged_tracker_data')
        return temp

    def get_tracker_sets(self, search='*', befor=None, past=None, min_data=None, keys='*'):
        temp = []
        if type(keys) == list and not 'Date' in keys:
            keys.append('Date')
        objs = {obj.display_name: obj.tracker.sub_data(amount=min_data, befor=befor, past=past, keys=keys) for obj in self.printer.get_search(search)}
        [temp.extend(tracker['Date']) for tracker in objs.values() if tracker]
        dates = list(set(temp))
        dates.sort()
        data_set = {}
        for name, obj in objs.items():
            if obj:
                temp = {key: [] for key in obj.keys() if key != 'Date'}
                for date in dates:
                    if date in obj['Date']:
                        for key in temp.keys():
                            temp[key].append(obj[key][obj['Date'].index(date)])
                    else:
                        for key in temp.keys():
                            temp[key].append(0)
                data_set[name] = temp

        return data_set, dates

    def __repr__(self):
        msg = f'Cartridges[{len(self.cartridges.name_index)}]: {self.cartridges.name_index}\n'
        msg += f'Models[{len(self.printer_models.name_index)}]: {self.printer_models.name_index}\n'
        msg += f'Printer[{len(self.printer.name_index)}]: {self.printer.name_index}\n'
        return msg

    def get_overview_table(self, keys=('display_name', 'model', 'ip', 'cartridges')):
        arr = []
        for obj in self.printer.obj:
            arr.append({key: obj.export()[key] for key in keys})
        return dumps(list(keys)), dumps(arr)


if __name__ == '__main__':
    from datetime import datetime as dt, timedelta
    befor = dt.now()
    past = befor - timedelta(days=100)
    db = DataBase()
    befor, past = [dt.strptime(input(f'{t} (in format dd.mm.yy):'), '%d.%m.%y') for t in ('befor', 'past')]


    test_set, dates = db.get_tracker_sets(befor=befor, past=past, keys=['Prints', 'B'])
    print('Dates', len(dates), ''.join([date.strftime('%d.%m.%y') + " | " for date in dates]))
    for key, val in test_set.items():
        print(key)
        for k, v in val.items():
            print(k, len(v), v)
