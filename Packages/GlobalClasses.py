from time import perf_counter_ns as nsec

class LockedSlots(object):
    __slots__ = ('_locked')

    def __init__(self, *args):
        args = args + ('_locked',)
        self.__setattr__('_locked', args)


    def __getattribute__(self, item):
        if item == '_locked':
            try:
                return super().__getattribute__(item)
            except:
                return ()
        else:
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if not (key in self._locked):
            super().__setattr__(key, value)


class LockedClass(object):
    __slots__ = '_locked'
    def __init__(self, *args):
        args = args + ('_locked',)
        self.__setattr__('_locked', args)


    def __getattribute__(self, item):
        if item == '_locked':
            try:
                return super().__getattribute__(item)
            except:
                return ()
        else:
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if not (key in self._locked):
            super().__setattr__(key, value)


class TaskInterval(object):
    '''
    list of task obj [ {name: str, last_time: int, interval: int, event: method/function},...]
    '''
    def __init__(self, args):
        self.tasks = []
        for arg in args:
            self.__setattr__(arg[0], [None, arg[1], arg[2]])
            self.tasks.append(arg[0])

    def get_sec(self):
        return int(nsec() * .000000001)

    def trigger(self):
        for task in self.tasks:
            t_old, interval, event = self.__getattribute__(task)
            if t_old is None:
                event()
                t_old = self.get_sec()
                print(task)
            elif self.get_sec() - t_old > interval:
                event()
                t_old = self.get_sec()
                print(task)
            self.__setattr__(task, [t_old, interval, event])


if __name__ == '__main__':

    class test(LockedClass):
        __slots__ = 'a', 'b'
        def __init__(self):
            self.a = 1
            self.b = 2
            super().__init__(*('a', '_locked'))

        def __repr__(self):
            return f'{self.a}, {self.b}'
    t = test()
    t.a = 2
    t.b = 4
    print(t)