import time
from functools import wraps

# FooRunTime is a little Helper for development purpose to check the time a function needs to run and print it to console
def FooRunTime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        go = time.perf_counter()
        run = func(*args, **kwargs)
        fin = time.perf_counter()
        print(f'{func.__module__}, {func.__name__}:{go - fin} seconds')
        return run
    return wrapper