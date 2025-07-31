from tkinter import ttk
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
        welcome_text = ttk.Label(self, text="Welcome to PowerPal", font=("Helvetica", 22))
        welcome_text.grid(column=0, row=0, columnspan=12, pady=5)

        # Take Attendance Link
        go_to_attendance_btn = ttk.Button(
            self, 
            text="Take Attendance", 
            command=lambda: root_app.show_frame('Take_Attendance'),
            width=15
        )
        go_to_attendance_btn.grid(column=0, row=1, columnspan=5, pady=(20, 0))
        
        # Documents Link
        go_to_documents_btn = ttk.Button(
            self, 
            text="Download Docs", 
            command=lambda: root_app.show_frame('Documents'),
            width=15
        )
        go_to_documents_btn.grid(column=6, row=1, columnspan=5, pady=(20, 0))

        # Attendance audit Link
        # attendance_audit_btn = ttk.Button(
        #     self, 
        #     text="Attendance Audit", 
        #     command=lambda: root_app.show_frame('Attendance_Audit'),
        #     width=15
        # )
        # attendance_audit_btn.grid(column=0, row=2, columnspan=5, pady=(30, 0))

        # Update Credentials
        update_credentials_btn = ttk.Button(
            self, 
            text="Update Credentials", 
            command=lambda: root_app.show_frame('Update_Credentials'),
            width=15
        )
        update_credentials_btn.grid(column=0, row=2, columnspan=5, pady=(30, 0))

        # Update Student Demographics
        update_student_demographics = ttk.Button(
            self, 
            text="Update Students", 
            command=get_student_demographics,
            width=15
        )
        update_student_demographics.grid(column=5, row=2, columnspan=12, pady=(30,0))
