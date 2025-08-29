#### List in python 

letters = ['a','b','c','d','e']
list_numbers = list(range(5,15))
list_letters = [chr(i) for i in range(ord('B'), ord('L'))]
list_new_letters = list('abcdefghi')

# for i,letter in enumerate(letters):
#     print(f"Then index is {i} and value {letter}")


og_list_new = list_new_letters[::-1] # reverse list 

# print(list_numbers)
# print(list_letters)
# print(list_new_letters)
print("before",og_list_new)

# add and remove items

og_list_new.append("J")
og_list_new.insert(3,"fff")

print("after",og_list_new)

og_list_new.pop()

print("after pop",og_list_new)

og_list_new.remove('fff')

print(og_list_new)

# delete range of items

# del og_list_new[2:4]

# print(og_list_new)

# find item list 

if 'a' in og_list_new:
    print(og_list_new.index('a'))

 # count item
print(og_list_new.count('d'))   