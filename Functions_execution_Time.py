import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end - start:.6f} seconds")
        return result
    return wrapper
@measure_time
def func1():
    sum([i for i in range(1000000)])

@measure_time
def func2():
    time.sleep(0.5)

@measure_time
def func3():
    [x**2 for x in range(500000)]

func1()
func2()
func3()
