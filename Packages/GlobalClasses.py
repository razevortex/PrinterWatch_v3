
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