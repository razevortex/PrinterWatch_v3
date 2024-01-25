from pathlib import Path

ROOT = Path("/srv/servme/db")

try:
    DB_DIR = Path(*[ROOT, 'jsons'])
    LOG_DIR = Path(*[ROOT, 'logs'])
except:
    ROOT = '/srv/servme/'
    DB_DIR = Path(*[ROOT, 'jsons'])
    LOG_DIR = Path(*[ROOT, 'logs'])

if __name__ == '__main__':
    print(f'{ROOT}\n{DB_DIR}\n{LOG_DIR}')
