def my_decorator(func):
    def wrapper(*args,**kwargs):
        print("Before the function runs")
        func(*args,**kwargs)
        print("After the function runs")
        return func(*args,**kwargs)
    return wrapper

@my_decorator
def add(a,b):
    return a+b

print(add(5,5))
