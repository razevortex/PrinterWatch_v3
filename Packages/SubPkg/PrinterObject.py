from PrinterObj.PrinterModelLib import *
from PrinterObj.TrackerMod import *
from PrinterObj.CartridgeLib import *
from PrinterObj.ConstantVars import *
from TestFoo import *
from pathlib import Path

self = Path(__file__).absolute()

class Printer(object):
    def __init__(self, serial_no, model, **kwargs):
        self.serial_no = serial_no
        self.model = PrinterLib().get(model)
        self.ip = kwargs.get('ip', '')
        self.location = kwargs.get('location', '')
        self.contact = kwargs.get('contact', '')
        if kwargs.get('tracker', False):
            self.tracker = TrackerObj.load(kwargs.get('tracker'))
        else:
            self.tracker = TrackerObj.load(self.model._create_data_keys())

    def obj4json(self):
        t_dict = {'serial_no': self.serial_no, 'model': self.model.name, 'ip': self.ip, 'location': self.location,
                  'contact': self.contact, 'tracker': self.tracker.export()}
        return t_dict

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
        self.tracker.update(**kwargs)

    def update_tracker_batch(self, **kwargs):
        '''
        Update the trackers with multiple values at once
        @param kwargs: {tracker_keys: [value_list]}
        @return: None
        '''
        self.tracker.batch_(**kwargs)

if __name__ == '__main__':
    from TestFoo import *
    from PrinterObj.PrinterModelLib import _PrinterModel
    _PrinterModel.cart_lib = CartridgesLib

    def set_carts_lib(carts_lib):
        cli = CSV(reader('db\clients.csv'))
        arr = []
        for i, serial in enumerate(cli.get_col(0, list)):
            spec = CSV(reader('db\client_specs.csv'))
            for j, spec_serial in enumerate(spec.get_col(0, list)):
                if serial == spec_serial:
                    arr.append([cli.get_col(2, list)[i]] + spec.get_row(j)[1:5])
                    break
        arr = [[(line[i], line[0], ('B', 'C', 'M', 'Y')[i - 1]) for line in arr] for i in range(1, 5)]
        arr = arr[0] + arr[1] + arr[2] + arr[3]
        included = ['NaN']
        for cart in arr:
            if cart[0] not in included:
                carts_lib().build_new(*cart)
                included.append(cart[0])

    def set_prnmodel_lib(prn_lib):
        cli = CSV(reader('db\clients.csv'))
        arr, included = [], []
        for ser, man, mod in zip(cli.get_col(0, list), cli.get_col(2, list), cli.get_col(3, list)):
            if mod not in included:
                arr.append([ser, mod, man])
                included.append(mod)
        spec = CSV(reader('db\client_specs.csv'))
        for i, model in enumerate(arr):
            for j, ser in enumerate(spec.get_col(0, list)):
                if ser == model[0]:
                    carts = tuple(t for t in spec.get_row(j, list)[1:5] if t != 'NaN')
                    color = True if len(carts) > 1 else False
                    cli_db = CSV(reader(f'db/{cli.get_col(0, list)[j]}.csv'))
                    if 'NaN' in cli_db.get_col('Copied_BW', list):
                        copie = False
                    else:
                        copie = True
                    arr[i] = model[1:] + [carts, color, copie]
                    c = arr[i][2][0]
                    if len(arr[i][2]) > 1:
                        c += arr[i][2][1]
                    print(f'{arr[i][0]},{c}')
                    prn_lib().build_new(*arr[i])

    def build_printer(index):
        cli = CSV(reader('db\clients.csv'))
        printer = cli.get_row(index, dict)
        temp = Printer(printer['Serial_No'], printer['Model'], ip=printer['IP'])
        tracker_keys, serial = temp.tracker.tracker_keys, temp.serial_no
        cli_db = CSV(reader(f'db/{cli.get_col(0, list)[index]}.csv'))
        csv_keys = 'TonerBK', 'TonerC', 'TonerM', 'TonerY', 'Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM',\
            'Status',   'Time_Stamp'
        obj_keys = 'B', 'C', 'Y', 'M', 'Prints', 'ColorPrints', 'Copies', 'ColorCopies', 'stat', 'date'
        csv2obj = [(i, key) for i, key in enumerate(obj_keys) if key in tracker_keys]
        t_dict = {}
        #for row in range(len(cli_db.get_col(0, list))):
        for i, key in csv2obj:
            if key != 'date':
                t_dict[key] = cli_db.get_col(i, list)
            if key == 'date':
                t_dict[key] = [string_time(date) for date in cli_db.get_col(i, list)]
        temp.update_tracker_batch(**t_dict)
        #temp._print()
        return temp

    set_carts_lib(CartridgesLib)
    set_prnmodel_lib(PrinterLib)
    print(CartridgesLib())
    print(PrinterLib())
    catch_err = []
    for i in range(63):
        print('------------', i)
        try:
            obj = build_printer(i)
            t_dict = obj.obj4json()
            [print(f'{key}: {val}') for key, val in t_dict.items()]
        except:
            catch_err.append(i)
            print(f'\n\n An error occured --------- {i}')
    print(catch_err)