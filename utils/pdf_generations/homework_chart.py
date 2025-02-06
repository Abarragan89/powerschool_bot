import json
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from utils.string_manipulations import first_name_last_initial

def first_name_last_initial(student_name):
    last_name, first_name = student_name.split(", ")
    last_name = last_name.split(" ")[0]
    first_name = first_name.split(" ")[0]
    return f"{first_name } {last_name[0]}."


def generate_homework_chart():
    # Open file dialog to let the user choose where to save
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save PDF As",
        initialfile="homework_chart.pdf"
    )
    
    if not file_path:  # If user cancels, stop execution
        return

    width, height = letter
    # Swap the height and width values to make it landscape
    width, height = height, width
    starting_height = height - 60
    left_edge = 20
    right_edge = width - 20

    # Create canvas and set constant variables for height
    c = canvas.Canvas(file_path, pagesize=(width, height))

    # Add title and set top horizontal line
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2.0, height - 28, "Homework Chart")

    # Get Student Data
    with open('data/class_demo.txt', 'r') as file:
        content = file.read()
        student_demo_json = json.loads(content)


    # Loop through students to add name and bottom line (top line only if it is first student)
    for num, index in enumerate(student_demo_json):
        days_of_the_week = ["F", "M", "T", "W", "Th"]
        c.setFont("Helvetica", 10.5)
        c.drawString(23, starting_height - 40 - (20 * int(num)), first_name_last_initial(student_demo_json[index]['name']))
        
        # Loop to make the 25 bubbles
        starting_bubble_position = 121
        for bubble_num in range (1, 26):
            # Make Bubble
            c.circle(starting_bubble_position, starting_height - 35 - (20 * int(num)), 8, stroke=1, fill=0)
            
            # Make Label only if it's the first entry student (only need to make field names once)
            if num == 0:
                c.setFont("Helvetica-Bold", 11)
                c.drawString(starting_bubble_position - 6, starting_height - 18, days_of_the_week[bubble_num % 5])

                # Make the "Week of ______" only if it is the first iteration of bubble only run this on first student iteration
                if bubble_num % 5 == 0:
                    c.drawString(starting_bubble_position - 110, starting_height + 5, "Week of ___________")
            
            # increaseing starting position for next bubble
            starting_bubble_position += 25

            # Give a little extra space between each group of 5 bubbles
            if bubble_num % 5 == 0:
                starting_bubble_position += 10
                    

        # Draw the line below the name
        line_y = starting_height - 40 - (20 * int(num))
        c.line(left_edge, line_y - 4, right_edge, line_y - 4)
        # if it is the first item, it needs a top line as well
        if num == 0:
            c.line(left_edge, line_y + 20, right_edge, line_y + 20)
    
    # First Vertical line separating name and contact_name
    c.line(110, starting_height, 110, line_y - 4)

    # Making vertical lines to the right
    c.line(240, starting_height, 240, line_y - 4)
    c.line(372, starting_height, 372, line_y - 4)
    c.line(510, starting_height, 510, line_y - 4)
    c.line(645, starting_height, 645, line_y - 4)

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