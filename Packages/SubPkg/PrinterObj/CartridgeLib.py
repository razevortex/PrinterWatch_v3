from pathlib import Path

self = Path(__file__).absolute()

##  Just a Container of a Cart-Type
class _CartridgeModel(object):
    __slots__ = 'name', 'manufacturer', 'color', 'price'

    def __repr__(self):
        return self.__str__()
        #f' CartridgeModel:\n  name = {self.name}\n  manufacturer = {self.manufacturer}\n color = {self.color}'

    def __str__(self):
        return f'\n  name = {self.name}\n  manufacturer = {self.manufacturer}\n  color = {self.color}\n'

    def __init__(self, name='name', manufacturer='manufacturer', color='color', price=-1):
        self.name = name
        self.manufacturer = manufacturer
        self.color = color
        self.price = price

    def export(self):
        return {slot: self.__getattribute__(slot) for slot in self.__slots__}
        #return dict(name=self.name, manufacturer=self.manufacturer, color=self.color, price=self.price)

##  a Lib of the Cartridges
class CartridgesLib(object):
    obj = []
    name_index = []

    def __repr__(self):
        msg = 'Cartridges Lib :\n\n'
        for sub in [f'{str(typ)}\n' for typ in CartridgesLib.obj]:
            msg += ' ' + sub + '\n'
        return msg

    def export(self):
        return [obj.export() for obj in CartridgesLib.obj]

    def load(self, export):
        for obj in export:
            self.build_new(**obj)

    def build_new(self, name='name', manufacturer='manufacturer', color='color', price=-1):
        if name not in CartridgesLib.name_index and name != 'name':

            class Cart(_CartridgeModel):
                __name__ = name

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

            cart = Cart(name, manufacturer, color, price)
            CartridgesLib.obj.append(cart)
            CartridgesLib.name_index.append(cart.__name__)

    def get(self, name):
        try:
            if type(name) == str:
                return CartridgesLib.obj[CartridgesLib.name_index.index(name)]
            elif type(name) == tuple:
                return tuple(CartridgesLib.obj[CartridgesLib.name_index.index(n)] for n in name)
        except:
            return None

if __name__ == '__main__':
    for i in range(10):
        CartridgesLib().build_new(f'name{i}', f'manufacturer{i}', f'color{i}')
    print(CartridgesLib())
    print(CartridgesLib().get(('name3', 'name4', 'name2')))
    exported_lib = CartridgesLib().export()
    print(exported_lib)
    CartridgesLib.obj, CartridgesLib.name_index = [], []
    print(CartridgesLib())
    CartridgesLib().load(exported_lib)
    print(CartridgesLib())
