from printerwatch.PrinterRequest.run import basic_run
from time import perf_counter_ns as nsec

def tracker_clean_duplicates():
    db_dir = Path('/srv/servme/db/jsons')
    for p in [Path(db_dir, file) for file in os.listdir(db_dir) if 'tracker' in file]:
        with open(p, 'r') as f:
            temp = loads(f.read())
        temp['data'] = merge_duplicates(temp['data'])
        valid, t = True, None
        for key, val in temp['data'].items():
            if t is None:
                t = len(val)
            if t != len(val):
                valid = False
        if valid:
            with open(p, 'w') as f:
                f.write(dumps(temp))

def merge_duplicates(data):
    t_dict = {key: [] for key in data.keys()}
    dates = []
    for d in data['Date']:
        if d not in dates:
            dates.append(d)
    for key in t_dict.keys():
        if key == 'Date':
            t_dict[key] = dates
        else:
            t_dict[key] = [0 for _ in range(len(dates))]
    for i, d in enumerate(data['Date']):
        for key in [key for key in t_dict.keys() if key != 'Date']:
            if i < len(data[key]):
                t_dict[key][t_dict['Date'].index(d)] += data[key][i]
    return t_dict


last = 0
while True:
    if nsec() - last > 300 * (10 ** 9):
        last = nsec()
        basic_run()
        tracker_clean_duplicates()
