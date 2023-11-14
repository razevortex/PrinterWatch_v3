class _PrinterModel(object):
    __slots__ = 'name', 'manufacturer', 'cartridges', 'color', 'copie'
    cart_lib = None
    def __init__(self, name:str, manufacturer:str, cartridges:tuple, color:bool, copie:bool):
        self.name = name
        self.manufacturer = manufacturer
        self.cartridges = tuple([_PrinterModel.cart_lib().get(this) for this in cartridges])
        self.color = color
        self.copie = copie

    def __str__(self):
        temp = f'{self.manufacturer}\n{self.name}\n'.join([f'{cart}\n' for cart in self.cartridges])
        if self.color:
            temp += 'Color\n'
        if self.copie:
            temp += 'Copie\n'
        return temp
    
    @classmethod
    def load(cls, name:str, manufacturer:str, cartridges:tuple, color:bool, copie:bool, cart_lib):
        cartridges = tuple(cart_lib().get(cart) for cart in cartridges)
        return cls(name, manufacturer, cartridges, color, copie)

    def export(self):
        return [self._export_sub(slot) for slot in self.__slots__]

    def _export_sub(self, key):
        if key == cartridges:
            return (cart.name for cart in self.__getattribute__(key))
        else:
            return self.__getattribute__(key)

    def _create_data_keys(self):
        toner_keys = (['B'], ['C', 'Y', 'M'])
        print_keys = (['Prints'], ['ColorPrints'])
        copie_keys = (['Copies'], ['ColorCopies'])
        keys = toner_keys[0] + print_keys[0] if not self.copie else toner_keys[0] + print_keys[0] + copie_keys[0]
        if self.color:
            keys += toner_keys[1] + print_keys[1] if not self.copie else toner_keys[1] + print_keys[1] + copie_keys[1]
        return ['date'] + keys

    def _create_tracker(self):
        for k in self._create_data_keys:
            if len(k) == 1:
                arr.append(_TonerCounter(k))
            else:
                arr.append(_PageCounter(k))
        arr = [_DateCounter('date')] + arr
        return Tracker(*arr)


##  a Lib of all _PrinterModel
class PrinterLib(object):
    obj = []
    name_index = []

    def __repr__(self):
        return ''.join([f'{typ.name}:> \n{typ.manufacturer}\n{typ.cartridges}\n{typ.color}\n{typ.copie}\n' for typ in PrinterLib.obj])

    def build_new(self, name:str, manufacturer:str, cartridges:tuple, color:bool, copie:bool):
        if name not in PrinterLib.name_index:
            class printer(_PrinterModel):
                __name__ = name

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

            prt = printer(name, manufacturer, cartridges, color, copie)
            PrinterLib.obj.append(prt)
            PrinterLib.name_index.append(prt.__name__)

    def export(self):
        return [obj.export() for obj in PrinterLib.obj]

    def load(self, export, cart_lib):
        for obj in export:
            args = list(obj) + [cart_lib]
            obj = _PrinterModel.load(*args)
            if obj.name not in PrinterLib.name_index:
                PrinterLib().obj.append(obj)
                PrinterLib.name_index.append(obj.name)

    def get(self, name):
        try:
            return PrinterLib.obj[PrinterLib.name_index.index(name)]
        except:
            return None


if __name__ == '__main__':
    pass
