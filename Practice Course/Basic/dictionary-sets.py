students = {
    "mike": 50,
    "bun": 100,
    "john": 200,
    "mice": 23
}

print(students)
print(students["bun"])

students["Yahoo"] = 4120

print(students)
students.pop("bun")
print(students)

# for k in students:
#     print(k)

# for k in students.values():
#     print(k)

for k,v in students.items():
    print("Key: ",k);
    print("Value", v)

print(students.items())
students.update({"Buny":333})

print(students)
print(students.get("mike"))



# sets in python 

s = {1,3,4,23,4,224}
set_exam = set();

s.add(343)



print(type(s))
print(3 in s)
print(len(s))


## reverse string

def reverse_str(str):
    len_str = len(str); 
    split_str = list(str)
    mid = len_str / 2

    for x in range(int(mid)):
        temp = split_str[x]
        split_str[x] = split_str[len_str - x- 1]
        split_str[len_str - x- 1] = temp

    print("".join(split_str))



reverse_str("aniket") 
reverse_str("mike")    
reverse_str("nicework")  