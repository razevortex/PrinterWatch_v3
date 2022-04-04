import copy
import csv
import datetime as dt
import os
import pandas as pd
if __name__ == '__main__':
    from const.ConstantParameter import *

else:
    from .const.ConstantParameter import *



class HandleDB(object):
    _for_ini = ('timestamps(bool)', 'csv.file', 'header', 'id_key')

    def __init__(self, _for_ini):
        if _for_ini[0]:
            self.TimeStamps = True
        else:
            self.TimeStamps = False
        self.CSV = _for_ini[1]
        self.Header = copy.deepcopy(_for_ini[2])
        self.Entry_ID = _for_ini[3]
        self.ClientData = ({})
        self.ClientPack = ([], ({}))
        self.Empty = False
        if self.CSV:
            self.Empty = self.create_file()

    def create_file(self):
        if os.path.exists(f'{self.CSV}') is not True:
            with open(f'{self.CSV}', 'x', newline='') as csvfile:
                file_writer = csv.DictWriter(csvfile, fieldnames=self.Header)
                file_writer.writeheader()
            return True
        else:
            return False

    def updateData(self):
        with open(self.CSV, 'r', newline='', encoding='ISO-8859-1') as client_csv:
            reading = csv.DictReader(client_csv, fieldnames=self.Header)
            t_arr = []
            for row in reading:
                t_dic = {}
                for col in self.Header:
                    if col != row[col]:
                        t_dic[col] = row[col]
                if len(t_dic) == len(self.Header):
                    t_arr.append(t_dic)
        self.ClientData = t_arr
        self.ClientPack = (self.Header, self.ClientData)

    def cleanCSV(self):
        # this method keeps the db clean and will remove evantualy included duplicates and other unwanted lines
        # the first part here looks for duplicates
        with open(self.CSV, 'r', newline='', encoding='ISO-8859-1') as client_csv:
            reading = csv.DictReader(client_csv, fieldnames=self.Header)
            t_arr = []
            last_row = {}
            for key in self.Header:
                last_row[key] = 'NaN'
            for row in reading:
                t_dic = {}
                if row != last_row:
                    for col in self.Header:
                        if col != row[col]:
                            t_dic[col] = row[col]
                    if len(t_dic) == len(self.Header):
                        t_arr.append(t_dic)
                last_row = row
            # here its looking for lines where NaN values sliped in on values that are useualy trackable
            tt_arr = t_arr
            for col in self.Header:
                t_arr = tt_arr
                tt_arr = []
                val = 0
                firstline = t_arr[0]
                if firstline[col] == 'NaN':
                    val = 'NaN'
                for row in t_arr:
                    if row[col] == 'NaN':
                        if row[col] == val:
                            tt_arr.append(row)
                    else:
                        tt_arr.append(row)
            t_arr = tt_arr
        # this part rewrites the cleaned csv
        with open(self.CSV, 'w', newline='', encoding='ISO-8859-1') as client_csv:
            writeing = csv.DictWriter(client_csv, fieldnames=self.Header)
            writeing.writeheader()
            writeing.writerows(t_arr)

    def updateCSV(self):
        with open(self.CSV, 'w', newline='', encoding='ISO-8859-1') as client_csv:
            writeing = csv.DictWriter(client_csv, fieldnames=self.Header)
            writeing.writeheader()
            writeing.writerows(self.ClientData)
            print('updated CSV')

    def getEntry(self, *args):
        mode, key_val = args
        if mode == 'id':
            for i in self.ClientData:
                if self.TimeStamps:
                    timestamp, t_data = i
                else:
                    t_data = i
                if t_data[self.Entry_ID] == key_val:
                    return t_data
            print('no entry with this keyword was found')
            return False
        if mode == 'col':
            col = []
            data = {}
            for i in self.ClientData:
                t_data = i
                col.append(t_data[key_val])
            data[key_val] = col
            return data

    def addingEntry(self, add):
        self.updateData()
        data = []
        id_existed = False
        if len(add) == len(self.Header):
            for i in self.ClientData:
                t_data = i
                if add[self.Entry_ID] == t_data[self.Entry_ID]:
                    data.append(add)
                    id_existed = True
                else:
                    data.append(i)
            if id_existed:
                message = 'Serial Number already existed, entry was updated'
            else:
                data.append(add)
                message = 'New entry was added'
            self.ClientData = data
            self.ClientPack = (self.Header, self.ClientData)
            self.updateCSV()
            return message
        else:
            return error_code[1]


class dbClient(HandleDB):
    def __init__(self):
        csv = fr'{ROOT}db/clients.csv'
        _for_ini = (False,
                    csv,
                    header['client_db'],
                    'Serial_No'
                   )
        super().__init__(_for_ini)
        if self.create_file():
            self.updateData()


# RequestDB is somewhat unique as its init needs a arg Serial_No to select the corresponding csv file
class dbRequest(HandleDB):
    def __init__(self, id):
        csv = fr'{ROOT}db/{id}.csv'
        _for_ini = (False,
                    csv,
                    header['request_db'],
                    'Time_Stamp'
                    )
        super().__init__(_for_ini)
        try:
            self.cleanCSV()
        except:
            print('wasnt cleaned')
        self.updateData()
    # the get entry method of this handle only needs one arg the time_stamp it should search for alternative
    # 'recent' can be passed to just get the last entry

    def getEntry(self, key_val):
        if key_val == 'recent':
            return self.ClientData[-1]
        else:
            for row in self.ClientData:
                if row[self.Entry_ID] == key_val:
                    return row
            return error_code[0]

    def sum_col(self, sum_val, preprocessing='absolut'):
        if 'Toner' in sum_val:
            preprocessing = 'diff'
        else:
            preprocessing = 'relative'
        t_list = []
        data = copy.deepcopy(self.ClientData)
        for line in data:
            temp = line['Time_Stamp'].split(' ')
            line['Time_Stamp'] = temp[0]
        data_store = data[0]
        rest = data[1::]
        if preprocessing == 'relative':
            for line in rest:
                t_val = []
                for val in sum_val:
                    if line[val] != 'NaN' and data_store[val] != 'NaN':
                        if 'Toner' in val:
                            if int(data_store[val]) > int(line[val]):
                                t_val.append(int(data_store[val]) - int(line[val]))
                            else:
                                t_val.append(0)
                        else:
                            t_val.append(int(line[val]) - int(data_store[val]))
                        data_store[val] = line[val]
                t_val.append(line['Time_Stamp'])
                t_list.append(t_val)
        elif preprocessing == 'diff':
            for line in rest:
                t_val = []
                for val in sum_val:
                    if line[val] != 'NaN':
                        if int(data_store[val]) > int(line[val]):
                            t_val.append(int(data_store[val]) - int(line[val]))
                        else:
                            t_val.append(0)
                        data_store[val] = line[val]
                t_val.append(line['Time_Stamp'])
                t_list.append(t_val)
        temp_val_sum = []
        for line in t_list:
            temp = line[:-1:]
            x = 0
            for t in temp:
                x += int(t)
            temp_val_sum.append([x, line[-1]])
        temp_date_sum = []
        if len(temp_val_sum) > 2:
            temp = temp_val_sum[0]
            rest = temp_val_sum[1::]
            for line in rest:
                if line[1] == temp[1]:
                    temp[0] = temp[0] + line[0]
                else:
                    temp_date_sum.append(temp)
                    temp = line
            if temp_date_sum[-1][1] != temp[1]:
                temp_date_sum.append(temp)
        return temp_date_sum

    def getPlottingData(self, req_val, *args):
        t_dict = {}
        if args:
            arg = args[0]
        else:
            arg = 'absolute'
        for re_da in req_val:
            if re_da == 'TotalPages':
                sum_val = ['Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM']
                t_dict[re_da] = self.sum_col(sum_val, preprocessing='relative')
            elif re_da == 'TonerAll':
                sum_val = ['TonerBK', 'TonerC', 'TonerM', 'TonerY']
                t_dict[re_da] = self.sum_col(sum_val, preprocessing='diff')
            elif re_da == 'TonerCYM':
                sum_val = ['TonerC', 'TonerM', 'TonerY']
                t_dict[re_da] = self.sum_col(sum_val, preprocessing='diff')
            elif re_da == 'MonochromePages':
                sum_val = ['Printed_BW', 'Copied_BW']
                t_dict[re_da] = self.sum_col(sum_val, preprocessing='relative')
            elif re_da == 'ColoredPages':
                sum_val = ['Printed_BCYM', 'Copied_BCYM']
                t_dict[re_da] = self.sum_col(sum_val, preprocessing='relative')
            else:
                sum_val = [re_da]
                if 'Toner' in sum_val:
                    prep = 'diff'
                else:
                    prep = 'relative'
                t_dict[re_da] = self.sum_col(sum_val, preprocessing=prep)
        return t_dict

    def addingEntry(self, add):
        self.updateData()
        if len(self.ClientData) == 0:
            self.ClientData = [add]
            self.ClientPack = (self.Header, self.ClientData)
            self.updateCSV()
            return
        last = self.getEntry('recent')
        redundant_data = True
        for key, val in last.items():
            if key != 'Time_Stamp':
                if str(last[key]) != str(add[key]):
                    redundant_data = False
                    data = []
                    for i in self.ClientData:
                        data.append(i)
                    data.append(add)
                    self.ClientData = data
                    self.ClientPack = (self.Header, self.ClientData)
                    self.updateCSV()
                    print('new entry was made')
                    return
        if redundant_data:
            data = []
            for i in self.ClientData:
                data.append(i)
            data[-1] = add
            self.ClientData = data
            self.ClientPack = (self.Header, self.ClientData)
            self.updateCSV()
            print('redundant data last entry was updated')


class dbClientSpecs(HandleDB):
    def __init__(self):
        csv = fr'{ROOT}db/client_specs.csv'
        _for_ini = (False,
                    csv,
                    header['client_specs'],
                    'Serial_No'
                    )
        super().__init__(_for_ini)
        if self.create_file():
            self.updateData()
        self.updateData()


class SpecsLib(HandleDB):
    def __init__(self, manufacturer):
        csv = fr'{ROOT}lib/{manufacturer}_ModelSpecs.csv'
        _for_ini = (False,
                    csv,
                    ['Model', 'Color', 'Scanner', 'Cart', 'MethodIndex'],
                    'Model'
                    )
        super().__init__(_for_ini)
        self.updateData()


class ConfigLib(HandleDB):
    def __init__(self):
        csv = fr'{ROOT}user/config.csv'
        _for_ini = (False,
                    csv,
                    header['config'],
                    'Config_ID'
                    )
        super().__init__(_for_ini)
        self.updateData()



class LibOverride(HandleDB):
    def __init__(self):
        csv = fr'{ROOT}lib/override.csv'
        _for_ini = (False,
                    csv,
                    header['override'],
                    'ID'
                    )
        super().__init__(_for_ini)
        self.updateData()


    def updateDict(self, data_dict):
        for line in self.ClientData:
            if data_dict['Serial_No'] == line['ID']:
                for key, val in line.items():
                    data_dict['ID'] = line['ID']
                    if key in list(data_dict.keys()):
                        if val != 'NaN':
                            data_dict[key] = val
        return data_dict

    def getEntry(self, key_val):
        for row in self.ClientData:
            if row[self.Entry_ID] == key_val:
                temp = {}
                print('found')
                for k in self.Header:
                    if row[k] != 'NaN':
                        temp[k] = row[k]
                print(temp)
                return temp
        return False

    def entry_template(self):
        t = {}
        for key in self.Header:
            t[key] = 'NaN'
        return t

    def addEntry(self, id, entry):
        add = self.entry_template()
        add['ID'] = id
        for key in entry.keys():
            if key in list(add.keys()):
                add[key] = entry[key]
        arr_t = []
        id_found = False
        for line in self.ClientData:
            if line['ID'] == add['ID']:
                id_found = True
                for key, val in add.items():
                    if val != 'NaN':
                        line[key] = val
                    if val == '':
                        line[key] = 'NaN'
            arr_t.append(line)
        if id_found is not True:
            arr_t.append(add)
        self.ClientData = arr_t
        self.updateCSV()


        '''
        add.update(entry)
        data = []
        
            data.append(line)
            if line[self.Entry_ID] == add['ID']:
                add.update(line)
                add.update(entry)
                line.update(add)
                self.updateCSV()
                print('override updated')
                return
        data.append(add)
        self.ClientData = data
        self.updateCSV()'''

class dbStats(HandleDB):
    def __init__(self):
        csv = fr'{ROOT}db/client_statistics.csv'
        _for_ini = (False,
                    csv,
                    header['statistics'],
                    'Serial_No'
                   )
        super().__init__(_for_ini)
        if self.create_file():
            self.updateData()
        self.updateData()

    def entry_template(self):
        t = {}
        for key in self.Header:
            t[key] = 'NaN'
        return t

    def addEntry(self, entry):
        add = self.entry_template()
        add.update(entry)
        print(add)
        data = []
        for line in self.ClientData:
            data.append(line)
            if line[self.Entry_ID] == add[self.Entry_ID]:
                add.update(line)
                add.update(entry)
                line.update(add)
                self.updateCSV()
                print('data updated')
                return
        data.append(add)
        self.ClientData = data
        self.updateCSV()
        print('data updated')

class dbStatsGroup(HandleDB):
    def __init__(self):
        csv = fr'{ROOT}excel_sheets/recent_model_stats.csv'
        _for_ini = (False,
                    csv,
                    header['statistics_group'],
                    'Serial_No'
                   )
        super().__init__(_for_ini)
        if self.create_file():
            self.updateData()
        self.updateData()
