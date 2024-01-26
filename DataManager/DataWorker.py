from printerwatch.DataManager.DataSet import DataBase
from datetime import datetime as dt, date, timedelta

db = DataBase()

class DataObject(object):
    def __init__(self, past='2022-01-01', befor=None, interval=2, search='*', key='Prints', incr=True, group=False):
        befor = dt.now().date() if befor is None else dt.strptime(befor, '%Y-%m-%d').date()
        self.timeframe = self.timearr((dt.strptime(past, '%Y-%m-%d').date(), befor), timedelta(days=int(interval)))
        self.incr = incr
        self.group = group
        self.search = search
        self.key = key

    def __repr__(self):
        return '\n'.join([f'{key}: {val}' for key, val in self.__dict__.items()])

    def merge_keys(self, merge_name, keys='*'):
        temp = {}
        for key, data in self.data.items():
            temp[merge_name] = [sum(zipped) for zipped in zip([v for k, v in data.items() if k in keys or keys == '*'])]

    def plot_builder(self):
        ''' does call data_pruning ''' 
        temp = [{'label': name, 'data': data} for name, data in self.data_pruning()]
        return {'labels': [date.strftime('%d.%m.%Y') for date in self.timeframe], 'datasets': temp}


    def data_pruning(self):
        #                   not grouped
        if self.group is False:
            return [(obj.display_name, self.framer(obj.tracker.data['Date'], obj.tracker.data[self.key])) for obj in self.search_filter() if obj.tracker.data['Date']]
        #                   grouped
        else:
            temp = [self.framer(obj.tracker.data['Date'], obj.tracker.data[self.key]) for obj in self.search_filter() if obj.tracker.data['Date']]
            arr = []
            for d in range(len(self.timeframe)):
                arr.append(sum([t[d] for t in temp]))
            return ((self.search, arr),)

    def framer(self, date, vals):
        if date[0].date() > self.timeframe[-1]:
            return False
        i, temp, arr = 0, 0, []
        for t in range(len(self.timeframe)):
            while i < len(vals) and date[i].date() < self.timeframe[t]:
                if t > 0:
                    temp += vals[i]
                i += 1
            arr += [temp]
            temp = 0 if self.incr is not True else temp
        return arr

    def timearr(self, timeframe, interval):
        t = [dt.strptime(t, "%Y-%m-%d").date() if type(t) == str else t for t in timeframe]
        timearr = []
        while t[0] < t[1]:
             timearr += [t[0]]
             t[0] += interval
        return timearr

    def search_filter(self):
        if self.search is None:
            return db.printer
        else:
            return db.printer.get_search(self.search)

