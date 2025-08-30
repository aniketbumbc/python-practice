number_list = [5,3,6,1,0,2]
alha_list = ['k','e','x','d']

# sort list ascending 

number_list.sort()
alha_list.sort()

# print(number_list)
# print(alha_list)
alha_list.sort(reverse=True)

number_list.sort(reverse=True)
# print(alha_list)
# print(number_list)

# removed duplicate from list

duplicate_number_list = [6,6,3,4,1,2,4,5,8,1]
clone_list = duplicate_number_list[::]

def removed_duplicate(numlist):
    temp_list =[]

    if len(numlist) == 0:
        print("Please check num list")

    for item in numlist:
        if item not in temp_list:
            temp_list.append(item)


    if len(temp_list):
        print(temp_list)


# removed_duplicate(duplicate_number_list)
# removed_duplicate([])

# print("clone_list",clone_list)

num_demo = [7, 8, 120, 25, 44, 20, 27]


# removed even number from list

def removed_even(numList):
    temp_list = [ x for x in numList if x % 2 != 0]
    print(temp_list)


removed_even(num_demo)