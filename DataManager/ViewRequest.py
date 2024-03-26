from datetime import datetime as dt, date, timedelta

class InputReceiverBase(object):
    def __init__(self):
        self.arr = (InputReceiverBase.string_value, InputReceiverBase.num_value, InputReceiverBase.checkbox, InputReceiverBase.date)

    def builder(self, types=[], names=[], defaults=[]):
        resolver = [self.arr[t](self, n, d) for t, n, d in zip(types, names, defaults)]
        def receiver(recv):
            return {key: val for key, val in [res(recv) for res in resolver]}
        return receiver

    # 2
    def checkbox(self, name, default):
        def check(recv, name=name, default=default):
            if recv is None:
                return (name, default)
            else:
                return (name, recv.get(name, False) == 'on')
        return check

    # 3
    def date(self, name, default):
        def date_(recv, name=name, default=default):
            if recv is None or not recv.get(name, False):
                return (name, default)
            else:
                return (name, recv.get(name))
        return date_
 
    # 0
    def string_value(self, name, default):
        def string(recv, name=name, default=default):
            if recv is None or not recv.get(name, False):
                return (name, default)
            else:
                return (name, recv.get(name))
        return string

    # 1
    def num_value(self, name, default):
        def num(recv, name=name, default=default):
            if recv is None or not recv.get(name, False):
                return (name, default)
            else:
                return (name, int(recv.get(name)))
        return num



initial_view = {'plot': {
                        'names': ['key', 'search', 'past', 'befor', 'interval', 'incr', 'group', 'avg', 'group_key'],
                        'types': [0, 0, 3, 3, 1, 2, 2, 2, 2],
                        'defaults': ['Prints', '*', '2022-01-01', dt.today().date().strftime('%Y-%m-%d'), 14, True, False, False, False]
                        }
                }

inrec_plot = InputReceiverBase().builder(**initial_view['plot'])

