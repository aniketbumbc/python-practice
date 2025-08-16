student ="Mike Chore"
roll_number = 23
slice_std = student[0:5]
num_list = '012345679'
fruits = "mango, banana, apple, pApple"
student_call = "Please standup {} and name is {}"
fruits_list = ["mango, banana, apple, pApple"]


print(student)
print(student[0])
print(slice_std)
print(num_list[:])
print(student.lower())
print(student.upper())
print(student.lower())
print(student.strip())
print(student.replace('Mike', 'Bob'))
print(fruits.split(", "))
print(student.find("Chore"))
print(student.count("Chore"))
print(student_call.format(roll_number, student))
print(fruits_list)
print("- ".join(fruits_list))

fruits_list_new = ", ".join(fruits_list).split(", ")
print("- ".join(fruits_list_new))

print(len(fruits_list_new))

for ele in fruits_list_new:
    print(ele)


print("Mike" in student)
