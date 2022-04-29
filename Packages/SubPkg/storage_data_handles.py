from Packages.SubPkg.csv_handles import *
from Packages.SubPkg.foos import float_depth
from Packages.SubPkg.const.ConstantParameter import ROOT


class CartridgeStorage(object):
    def __init__(self):
        self.file = f'{ROOT}db/cartStorage.txt'
        self.virtual_storage = self.Storage2Dict()

    def Storage2Dict(self):
        t_dic = {}
        with open(self.file, 'r') as storage:
            string = storage.readline()
            item_list = string.split(',')
            for item in [entry.split(':') for entry in [t for t in item_list if t != '']]:
                if type(item) == list and len(item) == 2:
                    t_dic[item[0]] = int(item[1])
                    print(t_dic)
        return t_dic

    def update_vs(self, deltas_dict):
        for key, val in deltas_dict.items():
            if key in self.virtual_storage.keys():
                self.virtual_storage[key] += val

    def get_delta_zero_dict(self):
        t_dic = {}
        for key in self.virtual_storage:
            t_dic[key] = 0
        return t_dic

    def restore_vs(self):
        self.virtual_storage = self.Storage2Dict()


    def Dict2Storage(self):
        string = ''
        i = 0
        for key, val in self.virtual_storage.items():
            if i > 0:
                string += f',{key}:{val}'
            else:
                string += f'{key}:{val}'
            i += 1
        with open(self.file, 'w') as storage:
            storage.write(string)
