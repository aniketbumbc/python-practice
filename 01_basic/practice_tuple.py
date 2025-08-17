student_info = ("state", "city", "country")
print(student_info)
print(len(student_info))
more_info = ('dob', 'isCitizen')

all_info = student_info + more_info
print(all_info)

print(all_info.count("dob"))

(state, city,country) = student_info
print(state)
print(type(student_info))