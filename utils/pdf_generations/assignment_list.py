from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# from utils.get_students import first_name_last_initial
import json 

c = canvas.Canvas("data/assignment_list.pdf", pagesize=letter)

width, height = letter

with open('data/class_demo.txt', 'r') as file:
    content = file.read() 
    student_demo_json = json.loads(content)

def first_name_last_initial(student_name):
    last_name, first_name = student_name.split(", ")
    last_name = last_name.split(" ")[0]
    first_name = first_name.split(" ")[0]
    return f"{first_name } {last_name[0]}."

def draw_title_and_names(c):
    starting_height = height - 50
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2.0, height - 45, "Assignment Checklist")
    c.line(20, starting_height, width - 40, starting_height)

    # Loop through students to 
    c.setFont("Helvetica", 12)
    for num, index in enumerate(student_demo_json):
        c.drawString(23, height - 160 - (23 * int(num)), first_name_last_initial(student_demo_json[index]['name']))
        # Draw the line below the name
        line_y = height - 160 - (23 * int(num))
        c.line(20, line_y - 4, width - 40, line_y - 4)
        # if it is the first item, it needs a top line as well
        if num == 0:
            c.line(20, line_y + 20, width - 40, line_y + 20)
    
    
    # Find the space for the date after looping
    length_of_students = len(student_demo_json)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(23, height - 160 - (23 * (length_of_students)), "Date")
    line_y = height - 160 - (23 * (length_of_students)) # place after the last name entry
    c.line(20, line_y - 4, width - 40, line_y - 4)

    # Draw the line closing up the names on the left
    c.line(20, line_y - 4, 20, starting_height)

    # Draw vertical lines
    cols = 15
    col_width = width / cols
    for i in range(3, cols):
        x = i * col_width
        c.line(x, starting_height, x, line_y - 4)


draw_title_and_names(c)
c.showPage()
c.save()