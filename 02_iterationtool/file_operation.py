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
#print(I.__next__()) # throw StopIteration exception

D = {'a':1, 'b':2}

for key in D.keys():
    print(key)

I = iter(D);
print(next(I))
print(next(I))
# print(next(I))  throw StopIteration exception

R = range(5)
IR =iter(R)

print(next(IR))
print(next(IR))
print(next(IR))
print(next(IR))
print(next(IR))
# print(next(IR)) throw StopIteration exception
