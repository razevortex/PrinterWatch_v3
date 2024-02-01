from printerwatch.Libs.Cartridges import *
from printerwatch.Libs.Models import *

mLib = ModelLib()
cLib = CartridgesLib()

def test():
    print(mLib)
    print(cLib)
if __name__ == '__main__':
    print(mLib)
    print(cLib)
    #arr_ = [obj.name.rstrip('BKCYM') for obj in cLib.obj]
    #print(set(arr_))
    print(cLib.get_types_view())
