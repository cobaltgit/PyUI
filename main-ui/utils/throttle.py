import time
from functools import wraps

def limit_refresh(seconds=15):
    def decorator(func):
        last_called = [0]
        last_result = [None]

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_called[0] >= seconds:
                last_called[0] = now
                last_result[0] = func(*args, **kwargs)
            return last_result[0]
        return wrapper
    return decorator