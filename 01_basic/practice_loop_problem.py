# count positive number

numbers_list = [1,3,-2,-4,-7,-8,5,6,9,10];

def count_positive(list):
    count = 0
    for num in list:
        if(num > 0):
            count += 1
    print(count)


# count_positive(numbers_list)

user_number = int(input("Please enter number"))

def calculate_sum_even(num):
    sum = 0
    for i in range(num):
        if( i % 2 == 0):
            sum += 1

    print("The sum of even number is ", sum)

calculate_sum_even(user_number)