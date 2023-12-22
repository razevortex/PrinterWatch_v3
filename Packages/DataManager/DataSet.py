from json import dumps
from datetime import timedelta
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
        return dates, objs

    def merged_time_frames(self, objs, key_, dates):
        datasets = []
        for obj in objs:
            data = []
            for start, end in dates:
                val = obj.tracker.data._of_timeframe(start, end, keys=(key_, ))
                if val:
                    val = sum(val[key_])
                else:
                    val = 0
                data.append(val)
            datasets.append({'label': obj.display_name, 'data': data})
        return {'labels': [date[0].strftime('%d.%m.%Y') for date in dates], 'datasets': datasets}

    def make_time_frames(self, dates, timeframe):
        frame_start, frame_end = dates[0], dates[0] + timeframe
        temp = [(frame_start, frame_end)]
        while frame_end < dates[-1]:
            frame_start, frame_end = frame_end, frame_end + timeframe
            temp += [(frame_start, frame_end)]
        return temp

    def generate_plot(self, key, search='*', min_data=10, timeframe=None):
        dates, objs = self.get_tracker_sets(search=search, min_data=min_data)
        if timeframe is not None:
            dates = self.make_time_frames(dates, timeframe)
            return self.merged_time_frames(objs, key, dates)
        datasets = []
        for obj in objs:
            data = [0] * len(dates)
            for date, val in zip(obj.tracker.data['Date'], obj.tracker.data[key]):
                data[dates.index(date)] = val
            datasets.append({'label': obj.display_name, 'data': data})
        return {'labels': [date.strftime('%d.%m.%Y') for date in dates], 'datasets': datasets}

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
    print(db.generate_plot('Prints'))
    print(db.generate_plot('Prints', timeframe=timedelta(days=28)))
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