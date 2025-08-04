import json
import calendar
from datetime import datetime, date
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import gray, black
from utils.get_data_file import get_data_file
from utils.string_manipulations import first_name_last_initial
from utils.open_file_in_preview import open_file_in_preview

def generate_birthdays_calendar():
    # Open file dialog to let the user choose where to save
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save PDF As",
        initialfile="birthdays_calendar.pdf"
    )
    
    if not file_path:  # If user cancels, stop execution
        return

    # Create canvas
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Get current year
    current_year = datetime.now().year
    
    # Get Student Data and organize birthdays by month
    with open(get_data_file('data/class_demo.txt'), 'r') as file:
        content = file.read()
        student_demo_json = json.loads(content)
    
    # Organize birthdays by month and day
    birthdays_by_month = {}
    for student_id, student_data in student_demo_json.items():
        dob = student_data.get('dob')
        if dob:
            try:
                # Parse the date (format: MM/DD/YYYY)
                month, day, year = dob.split('/')
                month = int(month)
                day = int(day)
                
                if month not in birthdays_by_month:
                    birthdays_by_month[month] = {}
                if day not in birthdays_by_month[month]:
                    birthdays_by_month[month][day] = []
                
                name = first_name_last_initial(student_data['name'])
                birthdays_by_month[month][day].append(name)
            except:
                continue  # Skip invalid dates
    
    # Generate calendar for each month
    for month_num in range(1, 13):
        month_name = calendar.month_name[month_num]
        
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2.0, height - 50, f"{month_name} Birthdays")
        
        # Get calendar data for the month
        cal = calendar.Calendar(firstweekday=6)  # Start with Sunday
        month_days = list(cal.itermonthdates(current_year, month_num))
        
        # Calendar grid setup
        grid_start_x = 50
        grid_start_y = height - 150
        cell_width = (width - 100) / 7
        cell_height = 80
        
        # Draw day headers
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        c.setFont("Helvetica-Bold", 12)
        for i, day in enumerate(days):
            x = grid_start_x + (i * cell_width) + (cell_width / 2)
            y = grid_start_y + 10
            c.drawCentredString(x, y, day)
        
        # Draw grid and fill with dates
        for week in range(6):  # 6 weeks maximum
            for day in range(7):
                # Calculate position
                x = grid_start_x + (day * cell_width)
                y = grid_start_y - (week * cell_height)
                
                # Draw cell border
                c.rect(x, y - cell_height, cell_width, cell_height)
                
                # Get the date for this cell
                date_index = (week * 7) + day
                if date_index < len(month_days):
                    current_date = month_days[date_index]
                    day_num = current_date.day
                    
                    # Determine if this day is in current month
                    is_current_month = current_date.month == month_num
                    
                    # Set font and color based on whether it's current month
                    if is_current_month:
                        c.setFont("Helvetica-Bold", 14)
                        c.setFillColor(black)
                    else:
                        c.setFont("Helvetica", 10)
                        c.setFillColor(gray)
                    
                    # Draw day number
                    text_x = x + 5
                    text_y = y - 15
                    c.drawString(text_x, text_y, str(day_num))
                    
                    # Add birthday names if this is current month and has birthdays
                    if is_current_month and month_num in birthdays_by_month and day_num in birthdays_by_month[month_num]:
                        c.setFont("Helvetica", 8)
                        c.setFillColor(black)  # Black for names
                        
                        names = birthdays_by_month[month_num][day_num]
                        for i, name in enumerate(names):
                            name_y = text_y - 20 - (i * 10)
                            if name_y > y - cell_height + 5:  # Make sure name fits in cell
                                c.drawString(text_x, name_y, name)
                    
                    # Reset fill color
                    c.setFillColor(black)
        
        # Add page break except for last month
        if month_num < 12:
            c.showPage()
    
    # Save the PDF file
    c.showPage()
    c.save()

    open_file_in_preview(file_path)
