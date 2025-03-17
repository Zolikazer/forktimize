import time

from monitoring.logger import PERF_LOGGER


def benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        PERF_LOGGER.info(f"⏱️ {func.__name__} took {duration:.6f} seconds")
        return result

    return wrapper
