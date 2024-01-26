from printerwatch.PrinterRequest.run import basic_run
from time import perf_counter_ns as nsec

last = 0
while True:
    if nsec() - last > 300 * (10 ** 9):
        last = nsec()
        basic_run()
