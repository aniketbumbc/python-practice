
def calculate_homework(scores):
    sum_of_grades = 0

    for score in scores.values():
        sum_of_grades += score

    final_grade = round(sum_of_grades / len(scores),2)
    print(f'The final score is {final_grade}')
