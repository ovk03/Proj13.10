"""imlements logging wrapper"""
"""Onni Kolkka 
150832953 (student number)
created 12.12.2022 14.59
"""

def log(func):
    import time
    def wrapper(*args,**kwargs):
        t1=-time.time()
        result = func(*args,**kwargs)
        t1 += time.time()
        print(f"function: \"{func.__name__}\" executed" if t1<0.01 else f"function: \"{func.__name__}\" executed in {t1}")
        return result
    return wrapper

def print_info(a):
    print()