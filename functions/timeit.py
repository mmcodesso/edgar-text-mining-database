from functools import wraps
import time

def timeit(f):
    @wraps(f)
    def wrapper(*args, **kw):
        start_time = time.time()
        result = f(*args, **kw)
        end_time = time.time()
        print("{} took {:.2f} seconds."
              .format(f.__name__, end_time-start_time))
        return result
    return wrapper