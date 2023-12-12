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
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            self.__setattr__(key, (self.get_sec(), val))
        self.tasks = kwargs.keys()

    def get_sec(self):
        return int(nsec() * .000000001)

    def trigger(self):
        for task in self.tasks:

            temp = self.__getattribute__(task)
            if self.get_sec() - temp[0] > temp[1]:
                print(f'triggered => {task}')
                self.__setattr__(task, (self.get_sec(), temp[1]))
                return task
        return False

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