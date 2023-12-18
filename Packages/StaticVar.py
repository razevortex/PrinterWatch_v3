from pathlib import Path


def get_main_path():
    p = '/'
    for dir in str(Path.cwd()).split('/'):
        if dir == 'PrinterWatch_v3':
            p = Path(p, dir)
            return p
        p = Path(p, dir)


ROOT = get_main_path()

try:
    DB_DIR = Path(*[ROOT, 'jsons'])
    LOG_DIR = Path(*[ROOT, 'logs'])
except:
    ROOT = '/home/razevortex/PycharmProjects/PrinterWatch_v3'
    DB_DIR = Path(*[ROOT, 'jsons'])
    LOG_DIR = Path(*[ROOT, 'logs'])