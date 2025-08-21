
def square_of_num(num):
    return num ** 2

ans = square_of_num(4)



# polymorphism in python

def multiply(value1, value2):
    return value1 * value2

result = multiply(10,2)
resultA = multiply(10,'a')

print(result)
print(resultA)

# lambda functions

cube = lambda x: x ** 3
test = lambda : print("Hello Python welcome to lambda")
addition = lambda x,y: x +y

# print(cube(3))
# test()
# print(addition(100,300))

def sum_all(*args):
    return sum(args)

# print(sum_all(1,2))
# print(sum_all(1,2,4,5))

# generator function even generator 
# The yield keyword turns the function into a generator.

# Each time the generator is called (e.g. in a for loop), it resumes where it left off and returns the next value.

# Unlike return, which ends the function, yield pauses the function's state.

def generator(num):
    for i in range(2, num + 1,2):
        yield i
    
# for num in generator(10):
#     print(num)

# recursive function


def recursive_factorial(num):
    if(num == 0):
        return 1
    else:
        return (num) * recursive_factorial(num-1)


print(recursive_factorial(6))