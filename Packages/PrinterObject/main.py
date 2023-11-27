from imports import *
from Tracker import PrinterTracker


class Printer(object):
    def __init__(self, **kwargs):
        self.serial_no = kwargs.get('serial_no')
        self.model = mLib.get(kwargs.get('model'))
        self.display_name = kwargs.get('display_name', self.serial_no)
        self.notes = kwargs.get('notes', '')
        self.ip = kwargs.get('ip', '')
        self.location = kwargs.get('location', '')
        self.contact = kwargs.get('contact', '')
        self.cartridges = cLib.get(kwargs.get('cartridges', self.model.cartridges))
        self.tracker = PrinterTracker(self.serial_no, self.model.name)

    def __str__(self):
        return f'{self.serial_no}\n{self.model}\n{self.display_name}\n{self.notes}\n{self.ip}\n{self.location}\n' \
               f'{self.contact}'
    
    @staticmethod
    def string_compare(arg, self_str):
        '''
        A Match function for Search/Filter Query´s
        :param arg: query
        :param self_str: str(self)
        :return: bool
        '''
        arg, self_str = (arg[1:-1], self_str) if arg[0] == arg[-1] == '"' else (arg.casefold(), self_str.casefold())
        match = (arg not in self_str) if arg.startswith('-') else (arg in self_str)
        return match

    def match_search(self, string:str):
        for arg in string.split('&&'):
            if not self.string_compare(arg, str(self)):
                return None
        return self

    def save_tracker(self):
        self.tracker.save()

    def export(self):
        self.save_tracker()
        return {'serial_no': self.serial_no, 'model': self.model.name, 'ip': self.ip, 'location': self.location,
                'contact': self.contact}
        
    def _print(self):
        print(self.serial_no)
        print(self.ip)
        print(self.model)
        print(str(self.tracker))

    def update_tracker(self, **kwargs):
        '''
        Update the trackers with one value per tracker
        @param kwargs: {tracker_keys: value}
        @return: None
        '''
        self.tracker.update(self.cartridges, **kwargs)
        self.save_tracker()
        
    def update_tracker_batch(self, **kwargs):
        '''
        Update the trackers with multiple values at once
        @param kwargs: {tracker_keys: [value_list]}
        @return: None
        '''
        for i in range(len(kwargs.get('Date', []))):
            temp = {key: val[i] for key, val in kwargs.items()}
            self.tracker.update(self.cartridges, **temp)
        self.save_tracker()


class PrinterLib(object):
    obj = []
    name_index = []
    file = Path(DB_DIR, 'printer.json')
    
    def __init__(self):
        if path.exists(PrinterLib.file):
            self.load()
    
    def __repr__(self):
        msg = ''
        for obj in PrinterLib.obj:
            msg += str(obj) + '\n' + str(obj.tracker) + '\n\n'
        return msg

    def add_new(self, serial_no, model, **kwargs):
        kwargs.update(dict(serial_no=serial_no, model=model))
        new = Printer(**kwargs)
        PrinterLib.obj.append(new)
        PrinterLib.name_index.append(new.serial_no)
        self._save()

    def _save(self):
        with open(PrinterLib.file, 'w') as f:
            f.write(dumps(self._export()))
    
    def _export(self):
        '''
        self to obj for json
        @return: list(dict)
        '''
        return [obj.export() for obj in PrinterLib.obj]
    
    def _import(self):
        if PrinterLib.file is not None:
            with open(PrinterLib.file, 'r') as f:
                return loads(f.read())
    
    def load(self):
        for obj in self._import():
            if obj['serial_no'] not in PrinterLib.name_index:
                PrinterLib.obj += [Printer(**obj)]
                PrinterLib.name_index += [obj['serial_no']]

if __name__ == '__main__':
    pLib = PrinterLib()
    print(pLib)