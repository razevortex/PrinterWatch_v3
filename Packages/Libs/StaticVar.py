from pathlib import Path
DB_DIR = Path('/home/razevortex/PrinterWatch_v3/jsons')
DATA_KEYS_GROUPED = {'Pages': ('Prints', 'Copies', 'ColorPrints', 'ColorCopies'), 'Cartridges': ('B', 'C', 'M', 'Y'), 'Time': ('Date',)}
DATA_KEYS_LIST = ('Prints', 'Copies', 'ColorPrints', 'ColorCopies', 'B', 'C', 'M', 'Y', 'Date')

CART_MODEL_GROUP = [['TN-242BK', 'TN-246C', 'TN-246M', 'TN-246Y'], ['TN-247BK', 'TN-247C', 'TN-247M', 'TN-247Y'],
                    ['TK-8305K', 'TK-8305C', 'TK-8305M', 'TK-8305Y'], ['TK-8515K', 'TK-8515C', 'TK-8515M', 'TK-8515Y'],
                    ['TK-8505K', 'TK-8505C', 'TK-8505M', 'TK-8505Y'], ['TK-5280K', 'TK-5280C', 'TK-5280M', 'TK-5280Y'],
                    ['TN-241BK', 'TN-245C', 'TN-245M', 'TN-245Y'], ['TN-326BK', 'TN-326C', 'TN-326M', 'TN-326Y'],
                    ['TN-325BK', 'TN-325C', 'TN-325M', 'TN-325Y'],
                    ['TK-1140'], ['TK-3190'], ['TK-6325'], ['TK-130'], ['TK-170']]
