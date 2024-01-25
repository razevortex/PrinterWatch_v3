from json import dumps
from datetime import timedelta, datetime as dt, date
from printerwatch.GlobalClasses import TaskInterval
from printerwatch.PrinterObject.main import pLib, cLib, mLib


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


    def plot_builder(self, key, mods, search=None, timeframe=None, interval=2):
        print(mods)
        if not timeframe is None:
            tarr = self.timearr(timeframe, interval)
            print(tarr)
            print(mods)
            temp = [{'label': name, 'data': data} for name, data in self.data_pruning(key, search=search, timearr=tarr)]
            return {'labels': [date.strftime('%d.%m.%Y') for date in tarr], 'datasets': self.apply_mods(temp, mods)}
            

    def apply_mods(self, data, mods):
        [print(d) for d in data]
        if mods[0] == mods[1] == 0:
            return data
        if mods[0]:
            for j in range(len(data)):
                name, d = data[j]
                data[j] = name, [sum(d[0:i]) for i in range(len(d))]
        if mods[1]:
            data = data[:][1]
            return 'group', [sum(all_d) for all_d in zip(data[:])]
        return data
        

    def data_pruning(self, key, search=None, timearr=None):
        return [(obj.display_name, self.framer(obj.tracker.data['Date'], obj.tracker.data[key], timearr)) for obj in self.search_filter(search)]


    def framer(self, date, vals, timearr):
        if date[0].date() > timearr[-1]:
            return False
        i, temp, arr = 0, 0, []
        for t in range(len(timearr)):
            while i < len(vals) and date[i].date() < timearr[t]:
                if t > 0:
                    temp += vals[i]
                i += 1
            arr += [temp]
            temp = 0
        return arr

    def timearr(self, timeframe, interval):
        t = [dt.strptime(t, "%Y-%m-%d").date() for t in timeframe]
        timearr = []
        while t[0] < t[1]:
             timearr += [t[0]]
             t[0] += timedelta(days=interval)
        return timearr

    def search_filter(self, search):
        if search is None:
            return self.printer
        else:
            return self.printer.get_search(search)

if __name__ == '__main__':
    db = DataBase()
    print(db.generate_plot('Prints'))
    print(db.generate_plot('Prints', timeframe=timedelta(days=28)))
    '''from _printerwatch.csv_read import *
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
from json import dumps
from datetime import timedelta, datetime as dt, date
from printerwatch.GlobalClasses import TaskInterval
from printerwatch.PrinterObject.main import pLib, cLib, mLib


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


    def plot_builder(self, key, search=None, timeframe=None, interval=2):
        if not timeframe is None:
            tarr = self.timearr(timeframe, interval)
            print(tarr)
            temp = [{'label': name, 'data': data} for name, data in self.data_pruning(key, search=search, timearr=tarr)]
            return {'labels': [date.strftime('%d.%m.%Y') for date in tarr], 'datasets': temp}
            

    def data_pruning(self, key, search=None, timearr=None):
        return [(obj.display_name, self.framer(obj.tracker.data['Date'], obj.tracker.data[key], timearr)) for obj in self.search_filter(search)]

    def framer(self, date, vals, timearr):
        print(date)
        print(vals)
        if date[0].date() > timearr[-1]:
            return False
        i, temp, arr = 0, 0, []
        for t in range(len(timearr)):
            while i < len(vals) and date[i].date() < timearr[t]:
                if t > 0:
                    temp += vals[i]
                i += 1
                
            arr += [temp]
            temp = 0
        return arr

    def timearr(self, timeframe, interval):
        t = [dt.strptime(t, "%Y-%m-%d").date() for t in timeframe]
        timearr = []
        while t[0] < t[1]:
             timearr += [t[0]]
             t[0] += timedelta(days=interval)
        return timearr

    def search_filter(self, search):
        if search is None:
            return self.printer
        else:
            return self.printer.get_search(search)

if __name__ == '__main__':
    db = DataBase()
    print(db.generate_plot('Prints'))
    print(db.generate_plot('Prints', timeframe=timedelta(days=28)))
    '''from _printerwatch.csv_read import *
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
