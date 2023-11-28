from datetime import datetime as dt, timedelta

class CSV(object):
    __slots__ = 'keys', 'values'
    seperator = ','

    def __init__(self, *args):
        if len(args) == 1:
            args = args[0][0], args[0][1:]
        self.keys = args[0]
        self.values = args[1]

    @classmethod
    def reader(cls, filename):
        with open(filename, 'r') as f:
            return cls([line.split(',') for line in f.readlines()])

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

    def get_col(self, col , out=list):
        if self._key_index(col) is not False:
            i = self._key_index(col)
            if out == dict:
                return {self.keys[i]: [row[i] for row in self.values]}
            if out == list:
                return [row[i] for row in self.values]

    def get_datestring_col(self, col, out=list):
        return [dt.strptime(string.split('.')[0], '%Y-%m-%d %H:%M:%S') for string in self.get_col(col, out=out)]

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

cli = CSV.reader('/home/razevortex/PycharmProjects/PrinterWatch_v3/db/clients.csv')
model_ip = {key: val for key, val in zip(cli.get_col('IP'), cli.get_col('Model'))}
