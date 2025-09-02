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

# list comprehension

fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

new_fruit_list = [ "hi "+ ele for ele in fruits if "a" in ele]
# print(new_fruit_list)

range_list = [y for y in range(10,20) if y > 15]
# print(range_list)


double_num_list = [num*2 for num in number_list]
# print(double_num_list)

# find vowel in list 

word = "Pythoni"
vowels = "aeiou"

result_vowel = [char for char in word if char in vowels]
print(result_vowel)

# Given a list of numbers, find the sum of all even numbers

numbers_list_cal = [16, 13, 24, 53, 67, 70]


def sum_even(numList):
    result = 0
    for num in numList:
        if (num % 2 == 0):
            result = result + num

        
    print(result)


sum_even(numbers_list_cal)