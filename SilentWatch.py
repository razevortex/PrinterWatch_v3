from printerwatch.PrinterRequest.run import basic_run
from time import perf_counter_ns as nsec


def tracker_clean_duplicates():
    db_dir = Path('/srv/servme/db/jsons')
    for p in [Path(db_dir, file) for file in os.listdir(db_dir) if 'tracker' in file]:
        with open(p, 'r') as f:
            temp = loads(f.read())
        temp['data'] = merge_duplicates(temp['data'])
        with open(p, 'w') as f:
            f.write(dumps(temp))


def merge_duplicates(data):
    for i in range(len(data['Date'])-1):
        if i + 1 >= len(data['Date']):
            return data
        while data['Date'][i] == data['Date'][i+1]:
            for key in data.keys():
                if key == 'Date':
                    data[key].pop(i+1)
                elif len(data[key]) >= i + 1:
                    data[key][i] = int(data[key][i]) + int(data[key].pop(i+1))
            if i + 1 >= len(data['Date']):
                return data
    return data


last = 0
while True:
    if nsec() - last > 300 * (10 ** 9):
        last = nsec()
        basic_run()
        tracker_clean_duplicates()
