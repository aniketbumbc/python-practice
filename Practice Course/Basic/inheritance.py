class Employee:
    parentCompany = 'ITC'
    def show(self,name,salary):
        print(f" Then name is  {name} and the salary is {salary}")



class Programmer(Employee):
    company = 'google'
    def showLanguge(self):
        print(f"The name is {self.name} and he is good with {self.language}")



a = Programmer();

print(a.company, a.parentCompany)
a.show("Bunny", 3434)


# Multilevel inheritance


class School:
    def showSchool(self):
        print("Welcome to school")


class Batch(School):
     def showBatch(self):
        print("Welcome to Batch")

class Student(Batch):
     def showStudent(self):
        print("Welcome to Student")


s = School()
stu = Student()

s.showSchool()

stu.showBatch()
stu.showSchool()
stu.showStudent()
