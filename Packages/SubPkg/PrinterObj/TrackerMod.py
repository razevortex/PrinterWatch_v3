from pathlib import Path
from datetime import datetime as dt, timedelta
self = Path(__file__).absolute()


#   TrackerObj Parents a group of Counter subclasses and its main purpose is to streamline the
#   update process of the collected incoming data further up in the main PrinterObj
#   TrackerObj are created by the PrinterModel and nested as property of the PrinterObj
class TrackerObj(object):
    __slots__ = 'trackers', 'tracker_keys'

    def __init__(self, *tracker):
        self.trackers = {obj.name: obj for obj in tracker}
        self.tracker_keys = self.trackers.keys()

    def __repr__(self):
        msg = 'TrackerObj =>\n'
        for tracker in self.trackers.values():
            msg += f'{tracker.name}[{len(tracker)}] > {tracker.current} > {tracker.data[:10]}...{tracker.data[-10:]}\n'
        return msg

    def export(self):
        return [tracker._export() for tracker in self.trackers.values()]

    @classmethod
    def load(self, tracker_dict):
        if type(tracker_dict) == dict:
            tracker = [_import_tracker(**_dict) for _dict in tracker_dict]
        if type(tracker_dict) == list:
            tracker = [_import_tracker(name=item, current=None, data=[]) for item in tracker_dict]
        return self(*tracker)

    def batch_(self, **kwargs):
        while len(kwargs.get('date')) > 1:
            kwarg = {}
            for key, val in kwargs.items():
                kwarg[key] = val.pop(0)

            self.update(**kwarg)
        #self.update(**kwargs)
        
    def update(self, **kwargs):
        '''
        update all counters
        @param kwargs: a dict with key:name of counter, val:new current value
        @return: None
        '''
        #   If not all keys delivered just esc to not mess with the dataset
        for key in self.tracker_keys:
            if key not in kwargs.keys():
                print('Err received not all keys')
                return
        #   The date is used a couple times and its more readable
        up_date = kwargs.get('date').date()
        #   If the data is still from the same day just update the deltas
        if (self.trackers['date'].current is None) or (self.trackers['date'].current == up_date):
            for key in self.tracker_keys:
                self.trackers[key].update(kwargs.get(key))
            return
        #  If there is a date gap in the data it is filled and then updated
        else:
            while self.trackers['date'].current < up_date:
                [self.trackers[key].fill_gap() for key in self.tracker_keys]
            [self.trackers[key].update(kwargs.get(key)) for key in self.tracker_keys]

# foo the Tracker_obj needs to rebuild its tracker from their exported data
def _import_tracker(**kwargs):
    name = kwargs.get('name')
    kwargs = {key: val for key, val in kwargs.items() if key != 'name'}
    if name == 'date':
        return _DateTracker(name, **kwargs)
    elif len(name) == 1:
        return _TonerTracker(name, **kwargs)
    else:
        return _PageTracker(name, **kwargs)

class _tracker(object):
    __slots__ = 'name', 'current', 'data'

    def __init__(self, name, current=None, data=[]):
        self.name, self.current, self.data = name, current, data

    def __len__(self):
        return len(self.data)

    def _export(self):
        #return {slot: self.__getattribute__(slot) for slot in self.__slots__}
        return dict(name=self.name, current=self.current, data=self.data)

    def update(self, current):
        current = int(current) if self.name != 'date' else current.date()
        if self.current is None:
            self.current = current
        if current != self.current:
            self._update(current)

    def _update(self, current):
        pass

    def fill_gap(self):
        if self.name == 'date':
            self.current += timedelta(days=1)
        self.add2data()

    def add2data(self):
        pass


class _TonerTracker(_tracker):
    __slots__ = 'delta'

    def __init__(self, name, current=None, data=[], delta=0):
        super().__init__(name, current=current, data=data)
        self.delta = delta

    def _update(self, current):
        self.delta += (self.current - current + 100) % 100
        self.current = current

    def add2data(self):
        self.data.append(self.delta)
        self.delta = 0


class _PageTracker(_tracker):
    __slots__ = 'delta'

    def __init__(self, name, current=None, data=[], delta=0):
        super().__init__(name, current=current, data=data)
        self.delta = delta

    def _update(self, current):
        self.delta += (current - self.current)
        self.current = current

    def add2data(self):
        self.data.append(self.delta)
        self.delta = 0


class _DateTracker(_tracker):
    def __init__(self, name, current=None, data=[]):
        super().__init__(name, current=current, data=data)

    def _update(self, current):
        if self.current < current:
            self.current = self.current + timedelta(days=1)
        elif self.current > current:
            self.current = current

    def add2data(self):
        if self.current not in self.data:
            self.data.append(self.current)

    def _export(self):
        t_dict = {}
        for t in [self._string_data(slot) for slot in self.__slots__]:
            t_dict.update(t)
        return t_dict

    def _string_data(self, name):
        form = '%d.%m.%Y'
        value = self.__getattribute__(name)
        if name == 'current':
            return {name: value.strftime(form)}
        elif name == 'data':
            return {name: [val.strftime(form) for val in value]}
        else:
            return {name: value}

if __name__ == '__main__':
    ##  Example and Test
    test = TrackerObj.load(['B', 'C', 'M', 'Y', 'Printed_BW', 'Printed_Color', 'date'])
    print(test)
    '''from random import randint as rng
    from datetime import datetime as dt, timedelta

    # one of each Tracker toner always has to be named with a single letter
    test_counter = _DateTracker('date'), _TonerTracker('B'), _PageTracker('pages')
    # creating the main tracker out of the seperate trackers as *arg since the amount is variable
    test = TrackerObj(*test_counter)

    # pages is meant to be the current pages value
    pages = 0
    # start date
    date = dt.now()
    # toner value is always just a random so no var
    # data stores the input data for later comparison
    data = []
    # the amount of data packets the tracker will get fed
    num_data = 100
    for i in range(num_data):
        dic_t = {} # the later **kwargs the tracker gets fed
        # and the creation of the random data
        pages += rng(0, 1000)
        if rng(0, 10) > 5:
            date = date + timedelta(days=rng(1, 3))
        dic_t['date'] = date
        dic_t['B'] = rng(0, 100)
        dic_t['pages'] = pages
        data.append(dic_t)
        # feeding
        test.update(**dic_t)

    print(test)

    tracker = test.export()
    print(tracker)
    loaded = TrackerObj.load(tracker)
    print(loaded)

    print(data)
    print([d['pages'] for d in data])'''
