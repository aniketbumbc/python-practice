fruits_list = ["Mango", "Banana", "Apple", "Papaya", "Grapes", "Orange", "Pineapple", "Guava"]
print(fruits_list)
print(fruits_list[2:6])
# print(frozenset[2:])
print(fruits_list[2:3])
fruits_list[2:3] = ["banana cake"]
# print(fruits_list)

# for ele in fruits_list:
#     print(ele)

fruits_list.append("sweet potato")

print(fruits_list)

if "sweet" in fruits_list:
    print("Yess !!!")
else:
    print("Nooo !!")

fruits_list.insert(1, "green potato")

print(fruits_list)

new_fruits_list = fruits_list.copy()

print(new_fruits_list)

student_list = ['s1', 's2','s3']
student_list_one = student_list
student_list_two = student_list.copy()

student_list_one.append('s4')
student_list_two.append('s5')

print(student_list)
print(student_list_one)
print(student_list_two)

squared_nums = [x**2 for x in range(10)]

print(squared_nums)