# count positive number

numbers_list = [1,3,-2,-4,-7,-8,5,6,9,10];

def count_positive(list):
    count = 0
    for num in list:
        if(num > 0):
            count += 1
    print(count)


# count_positive(numbers_list)

# user_number = int(input("Please enter number"))

def calculate_sum_even(num):
    sum = 0
    for i in range(num):
        if( i % 2 == 0):
            sum += 1

    print("The sum of even number is ", sum)

#calculate_sum_even(user_number)


number_three = 3

def number_table(num):
    for i in range(1,11):
        if(i == 5):
            continue
        print(num, 'X', i, '=', num * i)


# number_table(number_three)

# reverse string loop

def reverse_str(str):
    revr_str = ''
    for char in str:
        revr_str = char + revr_str

    print(revr_str)


# reverse_str('aniket')
# reverse_str('bunny')
# reverse_str('gfedcba')


# find first non-repeating char

def first_non_repeat_char(str):
    for char in str:
        if (str.count(char) == 1):
            print('The char is ', char)
            break


# first_non_repeat_char("teeter")

# Factorial calculator

def factorial_cal(num):
    result = 1
    while(num  > 0):
        result = result * num
        num = num - 1
    
    print(result)


# factorial_cal(12)

# check number is prime or not


def isPrime(num):
    isPrime_num = True
    for i in range(2,num):
        if(num % i == 0):
            isPrime_num = False
        break

    print(isPrime_num)

       


# isPrime(11)

# implement exponential backoff strategy that
# doubles the wait between retries, starting from 1 sec but waits after 5 retries

import time

wait_time = 1
max_retries = 5
attempts = 0

while attempts < max_retries:
    print("Attempts", attempts + 1 , "wait time ",wait_time)
    time.sleep(wait_time)
    wait_time *= 2
    attempts += 1