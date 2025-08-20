f = open('test_script.py')
# next = f.__next__()
# line = f.readline()
#line_next = f.readline()

for line in f:
    print(line)


# print(next)
# print(line_next)
myList = [1,2,3,4]

I = iter(myList)

print(I.__next__())
print(I.__next__())
print(I.__next__())
print(I.__next__())
print(I.__next__()) # throw StopIteration exception
