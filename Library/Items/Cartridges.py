from printerwatch.Library.Items.Base import Obj
import re

class Cartridge(Obj):
    mandatory = ('name', 'manufacturer', 'color')
    propertys = ('id', 'typ', 'avg_pages')
    __slots__ = 'name', 'manufacturer', 'color', 'price', 'global_stats'
    def __init__(self, **kwargs):
        if not kwargs.get('gobal_stats', False):
            kwargs['global_stats'] = {'Pages': 0, 'Toner': 0}
        super().__init__(**kwargs)

    @property
    def id(self):
        return f'{self.manufacturer} {self.name}'
    
    @property
    def typ(self):
        return re.findall(r'\d+', self.name)[0]
    
    @property
    def avg_pages(self):
        if self.global_stats['Toner'] != 0:
            temp = self.global_stats['Toner'] / 100
            if self.global_stats['Pages'] != 0:
                return self.global_stats['Pages'] // temp
        return 0
        
    def update_stats(self, **kwargs):
        self.global_stats['Toner'] += kwargs.get(self.color, 0)
        for key, val in kwargs.items():
            if self.color == 'B' and len(key) > 1:
                self.global_stats['Pages'] += kwargs[key]
            if self.color != 'B' and 'Color' in key:
                self.global_stats['Pages'] += kwargs[key]
                

# Execution Sandbox
if __name__ == '__main__':
    pass
