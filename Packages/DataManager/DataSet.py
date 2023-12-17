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

    def get_tracker_sets(self, search='*', min_data=10):
        temp = []
        objs = [obj for obj in self.printer.get_search(search) if len(obj.tracker.data['Date']) > min_data]
        [temp.extend(obj.tracker.data['Date']) for obj in objs]
        dates = list(set(temp))
        dates.sort()
        print(dates)


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
    db = DataBase()
    print(db.get_tracker_sets())
    '''from _Packages.csv_read import *
    def migrate_db():
        cLib.reset_stats()
        db = DataBase()
        for obj in db.printer.obj:
            print(obj.serial_no, get_tracker_set(obj.serial_no, obj.model.get_tracker_keys()))
            obj.update_tracker_batch(**get_tracker_set(obj.serial_no, obj.model.get_tracker_keys()))
    #migrate_db()
    db = DataBase()
    temp = db.printer.data_tracker_set('*')
    for key, val in temp.items():
        if key == 'Date':
            t = val[-1] - val[0]

            print(key, len(val), t.days, val)
        else:
            print(key, len(val), sum(val), val)'''