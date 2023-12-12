from Packages.PrinterObject.main import pLib, cLib, mLib
from Packages.PrinterRequest.main import PrinterRequest as req
from Packages.GlobalClasses import TaskInterval

scheduler = TaskInterval(req=600)

class DataBase(object):
    def __init__(self):
        self.printer = pLib
        self.printer_models = mLib
        self.cartridges = cLib

    def print_(self):
        print(self.cartridges)
        print(self.printer_models)
        print(self.printer)

    def merged_tracker_data(self, search='*'):
        temp = None
        for obj in self.printer.get_search(search, result='tracker'):
            try:
                if temp is None:
                    temp = obj.data.time_prune()
                else:
                    temp = temp + obj.data.time_prune()
            except:
                    print('err => merged_tracker_data')
        return temp

    def gather_tracker_data(self):
        if scheduler.trigger() == 'req':
            for ip in self.printer.get_search('*', result='ip'):
                try:
                    req(ip)
                except:
                    print('err', ip)
            return True
        return False

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
        for got in db.printer.get_search('*', result=object):
            print(got)
            got.reset_tracker()
            print(got.serial_no)#, get_tracker_set(got.serial_no, got.model.get_tracker_keys()))
            try:
                got.update_tracker_batch(**get_tracker_set(got.serial_no, got.model.get_tracker_keys()))
            except:
                print('failed')

    #migrate_db()

    def listen():
        db = DataBase()

        while True:
            db.gather_tracker_data()


    #listen()

    db = DataBase()

    print(db.merged_tracker_data())
