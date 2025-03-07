import time
from functools import wraps


def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱ Execution Time: {end_time - start_time:.2f} seconds")
        return result

    return wrapper
