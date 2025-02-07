import json
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from utils.string_manipulations import first_name_last_initial
from utils.open_file_in_preview import open_file_in_preview

def generate_assignment_list():
    # Open file dialog to let the user choose where to save
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save PDF As",
        initialfile="assignment_checklist.pdf"
    )
    
    if not file_path:  # If user cancels, stop execution
        return

    # Create canvas and set constant variables for height
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    starting_height = height - 50

    # Add title and set top horizontal line
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2.0, height - 45, "Assignment Checklist")
    c.line(20, starting_height, width - 40, starting_height)

    # Get Student Data
    with open('data/class_demo.txt', 'r') as file:
        content = file.read()
        student_demo_json = json.loads(content)

    # Loop through students to add name and bottom line (top line only if it is first student)
    c.setFont("Helvetica", 12)
    for num, index in enumerate(student_demo_json):
        c.drawString(23, height - 160 - (23 * int(num)), first_name_last_initial(student_demo_json[index]['name']))
        # Draw the line below the name
        line_y = height - 160 - (23 * int(num))
        c.line(20, line_y - 4, width - 40, line_y - 4)
        # if it is the first item, it needs a top line as well
        if num == 0:
            c.line(20, line_y + 20, width - 40, line_y + 20)
    
    # Determine the space for the date after looping through all students
    length_of_students = len(student_demo_json) # need this to determine how far down
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

    # Save the PDF file
    c.showPage()
    c.save()

    open_file_in_preview(file_path)