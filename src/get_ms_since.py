import time

def get_ms_since(start_time):
    return round((time.time() - start_time) * 1000)
