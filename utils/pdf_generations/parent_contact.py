import json
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from utils.get_data_file import get_data_file 
from utils.string_manipulations import format_phone_number, first_name_last_initial
from utils.open_file_in_preview import open_file_in_preview


def generate_parent_contact():
    """Open file dialog to let the user choose where to save"""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save PDF As",
        initialfile="parent_contact.pdf"
    )
    
    if not file_path:  # If user cancels, stop execution
        return

    width, height = letter
    # Swap the height and width values to make it landscape
    width, height = height, width
    starting_height = height - 40
    left_edge = 20
    right_edge = width - 20

    # Create canvas and set constant variables for height
    c = canvas.Canvas(file_path, pagesize=(width, height))


    # Add title and set top horizontal line
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2.0, height - 37, "Parent Contact")

    # Create column headings
    c.setFont("Helvetica", 13)
    c.drawString(112, starting_height - 18 ,"Contact #1") 
    c.drawString(443, starting_height - 18 ,"Contact #2") 
    # sub fields
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(125, starting_height - 38 ,"Name") 
    c.drawString(197, starting_height - 38 ,"Phone") 
    c.drawString(325, starting_height - 38 ,"Email")
    # Contact 2
    c.drawString(455, starting_height - 38 ,"Name") 
    c.drawString(527, starting_height - 38 ,"Phone") 
    c.drawString(655, starting_height - 38 ,"Email") 


    # Get Student Data
    with open(get_data_file('data/class_demo.txt'), 'r') as file:
        content = file.read()
        student_demo_json = json.loads(content)


    # Loop through students to add name and bottom line (top line only if it is first student)
    c.setFont("Helvetica", 10.5)
    for num, index in enumerate(student_demo_json):
        # Student name
        student_name = student_demo_json[index].get('name', 'Unknown Student')
        c.drawString(23, starting_height - 60 - (20 * int(num)), first_name_last_initial(student_name))
        
        # Contact One information
        contact_one = student_demo_json[index].get('contact_one', {})
        contact_one_name = contact_one.get('name', '')
        if contact_one_name and ',' in contact_one_name:
            contact_one_first = contact_one_name.split(',')[1].strip()
        else:
            contact_one_first = contact_one_name
        
        c.drawString(110, starting_height - 60 - (20 * int(num)), contact_one_first)
        c.drawString(182, starting_height - 60 - (20 * int(num)), format_phone_number(contact_one.get('phone', '')) if contact_one.get('phone') else "")
        c.drawString(255, starting_height - 60 - (20 * int(num)), contact_one.get('email', '') or "")
        
        # Contact # 2
        # check if contact two exists
        contact_2 = student_demo_json[index].get('contact_two')

        # only populate if contact exists
        if contact_2:
            contact_two_name = contact_2.get('name', '')
            if contact_two_name and ',' in contact_two_name:
                contact_two_first = contact_two_name.split(',')[1].strip()
            else:
                contact_two_first = contact_two_name
                
            c.drawString(440, starting_height - 60 - (20 * int(num)), contact_two_first)
            c.drawString(512, starting_height - 60 - (20 * int(num)), format_phone_number(contact_2.get('phone', '')) if contact_2.get('phone') else "")
            c.drawString(585, starting_height - 60 - (20 * int(num)), contact_2.get('email', '') or "")
        
        # Draw the line below the name
        line_y = starting_height - 60 - (20 * int(num))
        c.line(left_edge, line_y - 4, right_edge, line_y - 4)
        # if it is the first item, it needs a top line as well
        if num == 0:
            c.line(left_edge, line_y + 20, right_edge, line_y + 20)
    
    # Vertical line separating name and contact_name
    c.line(110, starting_height, 110, line_y - 4)

    # Making vertical lines to the right
    c.line(180, starting_height - 20, 180, line_y - 4)
    c.line(252, starting_height - 20, 250, line_y - 4)
    # Center Line
    # Draw Center line separating two contacts
    c.setLineWidth(2)
    c.line(441, starting_height, 441, line_y - 4) # 441 is center of contacts
    c.setLineWidth(1)
    c.line(510, starting_height - 20, 510, line_y - 4)
    c.line(583, starting_height - 20, 583, line_y - 4)
    # vertical line closing box on right
    c.line(right_edge, starting_height, right_edge, line_y - 4)

    
    # vertical line cutting contact vs contact fields cells
    c.line(110, starting_height - 20, width - 20,  starting_height - 20)

    # Draw the line closing up the names on the left
    c.line(left_edge, line_y - 4, left_edge, starting_height)
    

    # Make Headings
    # Top line
    c.line(left_edge, starting_height, right_edge, starting_height)

    # Save the PDF file
    c.showPage() # stop painting page

    # List all emails on second page for easy copy and paste
    c.setFont("Helvetica", 13)
    c.drawCentredString(width / 2, starting_height, 'All Contact Emails')
    c.setFont("Helvetica", 10.5)
    for num, index in enumerate(student_demo_json):
        contact_one = student_demo_json[index].get('contact_one', {})
        contact_one_email = contact_one.get('email', '') or ""
        c.drawString(100, starting_height - 30 - (15 * int(num)), contact_one_email)
        
        # Contact # 2
        # check if contact two exists
        contact_2 = student_demo_json[index].get('contact_two')

        # only populate if contact exists
        if contact_2:
            contact_two_email = contact_2.get('email', '') or ""
            c.drawString(400, starting_height - 30 - (15 * int(num)), contact_two_email)
    
    
    c.save() # save file

    open_file_in_preview(file_path)

