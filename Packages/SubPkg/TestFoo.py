from pathlib import Path
from datetime import datetime as dt, timedelta
self = Path(__file__).absolute()

def string_time(string):
    form = '%Y-%m-%d %H:%M:%S'
    return dt.strptime(string.split('.')[0], form)

def time_string(date):
    form = '%Y-%m-%d %H:%M:%S'
    return date.strftime(form)

class CSV(object):
    __slots__ = 'keys', 'values'

    def __init__(self, *args):
        if len(args) == 1:
            args = args[0][0], args[0][1:]
        self.keys = args[0]
        self.values = args[1]

    def get_row(self, row_index, out=list):
        if row_index < len(self.values):
            if out == dict:
                return {k: v for k, v in zip(self.keys, self.values[row_index])}
            if out == list:
                return self.values[row_index]

    def _key_index(self, col):
        if type(col) == int and col < len(self.keys):
            return col
        if type(col) == str and col in self.keys:
            return self.keys.index(col)
        return False

    def get_col(self, col: int | str, out=list):
        if self._key_index(col) is not False:
            i = self._key_index(col)
            if out == dict:
                return {self.keys[i]: [row[i] for row in self.values]}
            if out == list:
                return [row[i] for row in self.values]

    def get_all(self, axis, out=list):
        '''
        get all table elements
        @param axis: 0=rows 1=columns
        @param out: dict/list
        @return: dict/list
        '''
        if axis == 0:
            if out == dict:
                return [{key: col[i] for i, key in enumerate(self.keys)} for col in self.values]
            elif out == list:
                return self.values
        elif axis == 1:
            if out == dict:
                temp = {}
                for i, key in enumerate(self.keys):
                    temp[key] = [col[i] for col in self.values]
                return temp
            elif out == list:
                return [[col[i] for col in self.values] for i in range(len(self.keys))]


def reader(filename):
    with open(filename, 'r') as f:
        return [line.split(',') for line in f.readlines()]

def rebuild_client_db(cli_index):
    cli = CSV(reader('db\clients.csv'))
    model = cli.get_col(3, list)[cli_index]
    printer_obj = prn_mod_lib.get(model)
    cli_db = CSV(reader(f'db/{cli.get_col(0, list)[cli_index]}.csv'))
    csv_keys = 'TonerBK', 'TonerC', 'TonerM', 'TonerY', 'Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM', 'Time_Stamp'
    obj_keys = 'B', 'C', 'Y', 'M', 'Prints', 'ColorPrints', 'Copies', 'ColorCopies', 'date'
    csv2obj = [(c[i], o[i]) for c, o in zip(csv_keys, obj_keys)]
    db = []
    iss = [i for i, col in enumerate(cli_db.get_row(0, dict)) if col in csv_keys]
    iss.append(9)
    for row in range(len(cli_db.get_col(0, list))):
        t_dict = {}
        for key, i in zip(obj_keys, iss):
            if key != 'date':
                t_dict[key] = cli_db.get_col(i, list)[row]
            if key == 'date':
                t_dict[key] = string_time(cli_db.get_col(i, list)[row])
            db.append(t_dict)
    return db

def feed_printer_obj(cli_index, foo=rebuild_client_db):
    cli = CSV(reader('db\clients.csv'))
    serial = cli.get_col(0, list)[cli_index]
    model = prn_mod_lib.get(cli.get_col(3, list)[cli_index])
    printer_obj = Printer(serial, cli.get_col(3, list)[cli_index])
    db = foo(cli_index)

    for entrie in db:
        printer_obj.add_data(**entrie)

if __name__ == '__main__':
    pass
