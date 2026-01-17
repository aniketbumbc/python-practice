# List array 

friends = ["Mike", "Bun", "John", "Criag", "Mice"]

print(len(friends));

friends.append("Boss")
print(friends.count("Boss"))
friends.pop()
friends.pop(2)
friends.insert(2,"Baban")

print(friends)
print(friends.count("Boss"))

# for x in friends:
#     print(x)


# for i in enumerate(friends):
#     print(i)

# for i in range(len(friends)):
#     print(friends[i]);


# for x in range(4):
#     print(x)

## Object that never change tuple 

tuple_exm = (1,2,3,4)

print(tuple_exm)


a,b,c,d = tuple_exm

# for x in tuple_exm:
#     print(x)

print (a+b+c)