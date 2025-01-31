def get_student_list():
    with open('data/class_roster.txt') as file:
        return [student_name.strip() for student_name in file]

def first_name_last_initial(student_name):
    last_name, first_name = student_name.split(", ")
    last_name = last_name.split(" ")[0]
    first_name = first_name.split(" ")[0]
    return f"{first_name } {last_name[0]}."