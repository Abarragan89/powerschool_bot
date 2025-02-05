import json
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# from utils.string_manipulations import format_phone_number, first_name_last_initial

def first_name_last_initial(student_name):
    last_name, first_name = student_name.split(", ")
    last_name = last_name.split(" ")[0]
    first_name = first_name.split(" ")[0]
    return f"{first_name } {last_name[0]}."

def format_phone_number(digitString):
    """formats phones numbers: 818555555"""
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

def generate_student_demographics():
    """Open file dialog to let the user choose where to save"""
    # file_path = filedialog.asksaveasfilename(
    #     defaultextension=".pdf",
    #     filetypes=[("PDF files", "*.pdf")],
    #     title="Save PDF As",
    #     initialfile="parent_contact.pdf"
    # )
    
    # if not file_path:  # If user cancels, stop execution
    #     return

    width, height = letter
    # Swap the height and width values to make it landscape
    width, height = height, width
    starting_height = height - 40
    left_edge = 20
    right_edge = width - 20

    # Create canvas and set constant variables for height
    c = canvas.Canvas('data/student_demo.pdf', pagesize=(width, height))


    # Add title and set top horizontal line
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2.0, height - 28, "Student Demographics")
    # fields
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(160, starting_height - 18 ,"Street") 
    c.drawString(310, starting_height - 18 ,"City") 
    c.drawString(395, starting_height - 18 ,"Zip")
    c.drawString(450, starting_height - 18 ,"Phone") 
    c.drawString(530, starting_height - 18 ,"DOB") 
    c.drawString(605, starting_height - 18 ,"Age (for cumulative record)") 


    # Get Student Data
    with open('data/class_demo.txt', 'r') as file:
        content = file.read()
        student_demo_json = json.loads(content)


    # Loop through students to add name and bottom line (top line only if it is first student)
    c.setFont("Helvetica", 10.5)
    for num, index in enumerate(student_demo_json):
        c.drawString(23, starting_height - 40 - (20 * int(num)), first_name_last_initial(student_demo_json[index]['name']))
        c.drawString(112, starting_height - 40 - (20 * int(num)), student_demo_json[index].get('street') or "") 
        c.drawString(280, starting_height - 40 - (20 * int(num)), student_demo_json[index].get('city') or "")
        c.drawString(385, starting_height - 40 - (20 * int(num)), student_demo_json[index].get('zip').split('-')[0] or "")
        c.drawString(435, starting_height - 40 - (20 * int(num)), student_demo_json[index].get('phone') or "")
        c.drawString(515, starting_height - 40 - (20 * int(num)), student_demo_json[index].get('dob') or "")

        # Draw the line below the name
        line_y = starting_height - 40 - (20 * int(num))
        c.line(left_edge, line_y - 4, right_edge, line_y - 4)
        # if it is the first item, it needs a top line as well
        if num == 0:
            c.line(left_edge, line_y + 20, right_edge, line_y + 20)
    
    # First Vertical line separating name and contact_name
    c.line(110, starting_height, 110, line_y - 4)

    # Making vertical lines to the right
    c.line(275, starting_height, 275, line_y - 4)
    c.line(380, starting_height, 380, line_y - 4)

    c.line(430, starting_height, 430, line_y - 4) 
    c.line(510, starting_height, 510, line_y - 4)
    c.line(580, starting_height, 583, line_y - 4)

    # vertical line closing box on right
    c.line(right_edge, starting_height, right_edge, line_y - 4)



    # Draw the line closing up the names on the left
    c.line(left_edge, line_y - 4, left_edge, starting_height)
    

    # Make Headings
    # Top line
    c.line(left_edge, starting_height, right_edge, starting_height)

    # Save the PDF file
    c.showPage() # stop painting page
    c.save() # save file

generate_student_demographics()