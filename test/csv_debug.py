from Packages.SubPkg.csv_handles import *
import datetime as dt

'''
id = '01.05.2022'
now = dt.date.today()
if '.' in id:
    date_tup = id.split('.')
    date_tup = date_tup[::-1]
    y, m, d = (date_tup[0], date_tup[1], date_tup[2])
    print(y, m, d)
    ts = dt.date(year=int(y), month=int(m), day=int(d))
    delta = ts - now
    print(delta.days)

'''

if __name__ == '__main__':
    log = Logging()
    [print(entry) for entry in log.processedEntrys()]