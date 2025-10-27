def add(a, b):
    return a + b

def add_multiply(a, b):
    c = add(a, b)
    d = c * 2
    print(d)
    return d

def add_div(a, b):
    c = add(a, b)
    e = c / 2
    print(e)
    return e

add_multiply(4,6)