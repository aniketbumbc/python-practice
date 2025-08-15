import math
import random
num1 = 2
num2 = 5
num3 = 10

print(num1 + num2 + num3)
print((num2 + num1) * num3)
print(num1,num3,num2)

# repr, string and print difference

print(math.floor(4.9))
print(math.floor(4.1))
print(math.trunc(4.9)) # towards 0 

print(oct(num1))
print(hex(num1))
print(bin(num1))

print(random.random())
print(random.randint(1,10))

studentsRollNumbers = [40,41,42,43,44,45,50,51]
print(random.choice(studentsRollNumbers))
studentNames = ['a','b','c','d']
random.shuffle(studentNames)
print(studentNames)