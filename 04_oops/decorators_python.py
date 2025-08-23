import time

def timer(func):
    def wrapper(*args):
        print("Welcome to decorator function")
        start_time = time.time()
        result = func(*args)
        end_time = time.time()
        print(f"{func.__name__} running time is ${ end_time - start_time } time ")
        return result
    return wrapper



@timer
def test_function(n):
    time.sleep(n)
    print("Testing function wake up")


# test_function(2)


def debug_fun(func):
    def wrapper(*args):
        args_value = ', '.join(str(arg) for arg in args)
        print(f"the calling function is {func.__name__} and values are {args_value}")
        return func(*args)

    return wrapper


@debug_fun
def greet_meet(name,city):
    print(f"Welcome {name} in the big city of India {city} ")


greet_meet("Bunny", "Mumbai")