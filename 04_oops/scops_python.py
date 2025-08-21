username = 'mike' # global scope 

def scope_testing():
    username = 'Bob inside function' # function scope 
    city = "Baltimore"
    print(username)
    print (city)


# print(city) this is not accessible here
scope_testing()
# print(username)

x = 88

def calc(y):
    z = x + y
    return z

result = calc(100)
# print(result)

m = 200

def calc2():
    global m # global variable access here using keyword
    m = 300

# calc2()
# print(m)

# closure concept 

def func1():
    x = 9900
    def func2():
        print(x)
    return func2 # pass reference fucn2

result_func1 = func1()
result_func1()

def power_cal(num):
    def actual(x):
        return x ** num
    return actual


get_result = power_cal(3);
get_result2 = power_cal(4);

print(get_result(2))
print(get_result2(3))