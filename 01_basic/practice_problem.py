#classify children age group into child, adult, senior

user_age = int(input("Give me a age value: "))

def get_your_age_group(age):
    if (age < 13):
        print("You are in child group")
    elif(age < 20):
        print("You are in Teenager group")
    elif(age < 59):
        print("You are in Adult group")
    else:
        print("Welcome to senior citizen group")

get_your_age_group(user_age)