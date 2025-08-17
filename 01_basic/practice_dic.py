student_info = {"roll_number": 43, "city":"baltimore", "state": "MD"} 
# print(student_info)

print(student_info.get("roll_number"))
print(student_info["city"])

student_info["roll_number"] = "30"
# print(student_info)

for key in student_info:
    print(key, student_info[key])

for key,values in student_info.items():
    print("key : ", key)
    print("values: ", values)

if "city" in student_info:
    print("Yes city is there")
else:
    print("No city")

print(len(student_info))

student_info_copy = student_info.copy()
print(student_info_copy)

squared_num = {x:x**2 for x in range(10)}
print(squared_num)

keys=["state", "name", "roll_num"]
default_values = "test"

new_dict = dict.fromkeys(keys,default_values)
print(new_dict)