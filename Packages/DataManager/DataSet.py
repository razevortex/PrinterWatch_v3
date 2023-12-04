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
    db = DataBase()
    db.print_()
    print(db)