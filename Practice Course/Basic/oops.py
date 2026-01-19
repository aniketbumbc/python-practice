# class python
# self
# static method


class Employee:
    name= 'bunny'
    age = 34
    salary = 3434
    def getInfo(self):
        print(f"the name is {self.name} and age {self.age}")
    @staticmethod    
    def getPrint():
        print("Printing From Class")


# emp1 = Employee()
# print(emp1.name)
# print(emp1.age)
# emp1.getInfo()
# emp1.getPrint()


# constructor in python

class Students:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        print("Constructor is called")
    
    def printHello(self):
        print("Jello")
        print("name", self.name)
        print("name", self.age)



s1 = Students("Bunny", 334)

s1.printHello()


class Calculator:
    def __init__(self,number):
        self.sqNumber = number

    def getSquare(self):
        print(f"Square number is  {self.sqNumber * self.sqNumber}")
    
    def qube(self):
        print(f"Square number is  {self.sqNumber * self.sqNumber * self.sqNumber}")



c1 = Calculator(10)
c2 = Calculator(20)

c1.getSquare();
c2.qube()

    