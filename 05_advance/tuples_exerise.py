# tuple data type immutable sequence of values.
# can not add or delete once created. 

demo_tuple = (1,2,3,4,5,4,2,1,10,4,4)
print(demo_tuple)
print(type(demo_tuple))

print(demo_tuple[1:3])
print(demo_tuple.index(4))

print(demo_tuple.count(4))

# check list palindrome or not 

list_one = [1,2,4,2,1]

def isListPalindrome(dummyList):
    copy_list = dummyList[::]
    copy_list.reverse()
    print(copy_list)
    if(copy_list == dummyList):
        print("YES it is palindrome")
    else:
         print("NOT it is palindrome")





isListPalindrome(list_one)
isListPalindrome(["a","v","f"])

for index,value in enumerate(demo_tuple):
    print((index,value))