from Packages.PrinterObject.main import pLib, cLib, mLib


class DataBase(object):
    def __init__(self):
        self.printer = pLib
        self.printer_models = mLib
        self.cartridges = cLib

    def print_(self):
        print(self.cartridges)
        print(self.printer_models)
        print(self.printer)

    def __repr__(self):
        msg = f'Cartridges[{len(self.cartridges.name_index)}]: {self.cartridges.name_index}\n'
        msg += f'Models[{len(self.printer_models.name_index)}]: {self.printer_models.name_index}\n'
        msg += f'Printer[{len(self.printer.name_index)}]: {self.printer.name_index}\n'
        return msg

if __name__ == '__main__':
    from Packages.csv_read import *
    def migrate_db():
        cLib.reset_stats()
        db = DataBase()
        for obj in db.printer.obj:
            print(obj.serial_no, get_tracker_set(obj.serial_no, obj.model.get_tracker_keys()))
            obj.update_tracker_batch(**get_tracker_set(obj.serial_no, obj.model.get_tracker_keys()))
    #migrate_db()
    db = DataBase()
    temp = db.printer.data_tracker_set('*')
    for key, val in temp.items():
        if key == 'Date':
            t = val[-1] - val[0]

            print(key, len(val), t.days, val)
        else:
            print(key, len(val), sum(val), val)