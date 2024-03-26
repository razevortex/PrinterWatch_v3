from datetime import datetime as dt, timedelta
from printerwatch.DataManager.ChartTemplate import *
from printerwatch.Library.DataBase import *


class group_key_merger(dict):
    def __init__(self, keys):
        super().__init__({key: [] for key in keys})

    def merge_data(self, data):
        for key in self.keys():
            if len(self[key]) == 0:
                self[key] = data.get(key, [])
            elif key in data.keys():
                self[key] = [self[key][i] + data[key][i] for i in range(len(self[key]))]

    @classmethod
    def make(cls, keys, data):
        new = cls(keys)
        new.merge_data(data)
        return new

class RequestHandle(object):
    def __init__(self, past='2022-01-01', befor=None, interval=2, search='*', key='Prints', incr=True, group=False, avg=False, group_key=False):
        self.db = DB()
        self.group, self.incr, self.avg, self.group_key = group, incr, avg, group_key
        befor = dt.now().date() if befor is None else dt.strptime(befor, '%Y-%m-%d').date()
        self.timeframe = self._timeframe((dt.strptime(past, '%Y-%m-%d').date(), befor), timedelta(days=int(interval)))
        self.key_name = key
        self.keys = self._keys(key)
        self.datasets = self._search(search)

    def build_line_chart(self):
        temp = ChartObject('line')
        for data in self.datasets:
            print('datasets data')
            print(data)
            [temp['data'].add_dataset(key, val) for key, val in data.items()]
        print(temp)


    def _search(self, search):
        # < _merge_group, _data_pruning
        search = list(search.split(';'))
        if 'Carts' not in self.keys:
            arr = []
            database = self.db.printer
            if self.group:
                for query in search:
                    temp = [self._data_pruning(obj.tracker.data) for obj in database.search(query)]
                    print(temp)
                    arr.append((query, self._merge_group(temp))) 
                print(arr)
                return arr #[self._merge_group([(query, [self._data_pruning(obj.tracker.data)]) for obj in database.search(query)]) for query in search]
            else:

                for query in search:
                    for result in database.search(query):
                        [arr.append((result.id, self._data_pruning(result.tracker.data)))]
                [print(a[0]) for a in arr]
                return arr 
 
    def _merge_group(self, groups):
        # > _search
        temp = {}
        for key in self.keys:
            print(groups)
            if len(groups) > 1:
                #[print(items[0]) for items in zip([mem[key] for mem in groups])]

                temp[key] = [sum(items[0]) for items in zip([mem[key] for mem in groups if mem[key]])]
            else:
                temp[key] = groups[0][key]
        print(temp)
        return temp

    def _keys(self, key):
        validkeys = ['Prints', 'ColorPrints', 'Copies', 'ColorCopies', 'Carts']
        if 'Group' in key:
            if key.startswith('Total'):
                return tuple(validkeys[:4])
            if key.startswith('Color'):
                return tuple(validkeys[1::2])
            else:
                return tuple(validkeys[0:4:2])
        else:
            if key in validkeys:
                self.group_key = True
                return (key, )

    def _timeframe(self, timeframe, interval):
        t = [dt.strptime(t, "%Y-%m-%d").date() if type(t) == str else t for t in timeframe]
        timearr = []
        while t[0] < t[1]:
             timearr += [t[0]]
             t[0] += interval
        return timearr

    def _data_pruning(self, data):
        dates = data['Date']
        if dates[0].date() > self.timeframe[-1]:
            return False
        vals = {key: data[key] for key in self.keys}
        i, temp, data_ = 0, {key: 0 for key in self.keys}, {key: [] for key in self.keys}
        for t in range(len(self.timeframe)):
            while i < len(dates) and dates[i].date() < self.timeframe[t]:
                        
                if t > 0:
                    for key in self.keys:
                        if len(vals[key]) > i:
                            temp[key] += vals[key][i]
                i += 1
            for key in self.keys:
                data_[key].append(temp[key])
                temp[key] = 0
        return data_ if self.group_key is False else group_key_merger.make(self.keys, data_)

