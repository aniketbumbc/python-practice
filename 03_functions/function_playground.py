
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

print(sum_all(1,2))
print(sum_all(1,2,4,5))