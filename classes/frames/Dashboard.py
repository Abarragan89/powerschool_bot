from tkinter import ttk
from utils.take_attendance import take_attendance

class Dashboard(ttk.Frame):
    def __init__(self, root_app):
        # initi the Frame Class 
        super().__init__()

        # Set frame to grid and stretch it across the parent
        self.grid(sticky="nsew") 

        # Configure the columns in the frame for centering content
        for col in range(12):
            self.columnconfigure(col, weight=1)
        
        # Dashboard Title
        welcome_text = ttk.Label(self, text="Dashboard", font=("Helvetica", 22))
        welcome_text.grid(column=0, row=0, columnspan=12, pady=5)

        # Initialize Btn
        go_to_attendance_btn = ttk.Button(
            self, 
            text="Take Attendance", 
            command=lambda: root_app.show_frame('Take_Attendance')
        )
        go_to_attendance_btn.grid(column=0, row=4, columnspan=12, pady=(20, 0))
