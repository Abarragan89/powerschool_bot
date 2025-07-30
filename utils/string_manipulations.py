import json

from utils.get_data_file import get_data_file


def get_student_list():
    try:
        with open(get_data_file('data/class_demo.txt')) as file:
            class_data_json = json.load(file)
            return [student['name'].strip() for __, student in class_data_json.items()]
    except:
        return []

def first_name_last_initial(student_name):
    last_name, first_name = student_name.split(", ")
    last_name = last_name.split(" ")[0]
    first_name = first_name.split(" ")[0]
    return f"{first_name } {last_name[0]}."

def format_phone_number(digitString):
    """formats phones numbers: 818-555-5555"""
    formattedNumer = []

    # Only take numbers
    for char in digitString:
        if char.isdigit():
            formattedNumer.append(char)
    
    # Add hyphens
    formattedNumer.insert(3, '-')
    formattedNumer.insert(7, '-')
    
    # Return string
    return "".join(formattedNumer)