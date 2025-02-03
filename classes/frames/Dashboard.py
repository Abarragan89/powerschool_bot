from tkinter import ttk
from tkcalendar import Calendar
from utils.get_student_demographics import get_student_demographics


class Dashboard(ttk.Frame):
    def __init__(self, root_app):
        # initi the Frame Class 
        super().__init__(padding=10)

        # Set frame to grid and stretch it across the parent
        self.grid(sticky="nsew") 

        # Configure the columns in the frame for centering content
        for col in range(12):
            self.columnconfigure(col, weight=1)
        
        # Dashboard Title
        welcome_text = ttk.Label(self, text="Dashboard", font=("Helvetica", 22))
        welcome_text.grid(column=0, row=0, columnspan=12, pady=5)

        # Take Attendance Link
        go_to_attendance_btn = ttk.Button(
            self, 
            text="Take Attendance", 
            command=lambda: root_app.show_frame('Take_Attendance')
        )
        go_to_attendance_btn.grid(column=0, row=4, columnspan=12, pady=(20, 0))

        # Update Student Demographics
        update_student_demographics = ttk.Button(
            self, 
            text="Update Student Demographics", 
            command=get_student_demographics
        )
        update_student_demographics.grid(column=0, row=5, columnspan=12)

        # Calendar 
        # cal = Calendar(self, width=20, background="white", foreground="black")
        # cal.grid()
