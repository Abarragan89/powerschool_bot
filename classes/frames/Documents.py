from utils.pdf_generations.assignment_list import generate_assignment_list
from utils.pdf_generations.parent_contact import generate_parent_contact
from utils.pdf_generations.homework_chart import generate_homework_chart
from utils.pdf_generations.student_demograhics import generate_student_demographics
from tkinter import ttk

class Documents(ttk.Frame):
    def __init__(self, root_app):
        super().__init__(padding=10)
        
        # Set frame to grid and stretch it across the parent
        self.grid(sticky="nsew") 

        # Configure the columns in the frame for centering content
        for col in range(12):
            self.columnconfigure(col, weight=1)

        # Back to Dashbord Btn
        back_to_dashboard = ttk.Button(self, text='Back', command=lambda: root_app.show_frame('Dashboard'), width=4)
        back_to_dashboard.grid(row=0, column=0, sticky='wn')

        # Documents Title
        self.frame_title = ttk.Label(self, text="Document Downloads", font=("Helvetica", 22))
        self.frame_title.grid(column=0, row=0, columnspan=12, pady=(0, 30))
        
        # Download Assignment Checklist
        assignment_checklist = ttk.Button(self, text='Assignment Checklist', command=generate_assignment_list, width=15)
        assignment_checklist.grid(column=0, row=1, columnspan=5)
        
        # Download Homework Checklist
        assignment_checklist = ttk.Button(self, text='Homework Chart', command=generate_homework_chart, width=15)
        assignment_checklist.grid(column=0, row=2, columnspan=5, pady=(30, 0))

        # Download Parent Contact
        parent_contact = ttk.Button(self, text='Parent Contact', command=generate_parent_contact, width=15)
        parent_contact.grid(column=6, row=1, columnspan=5)

        # Download Student Demographics
        parent_contact = ttk.Button(self, text='Student Demographics', command=generate_student_demographics, width=15)
        parent_contact.grid(column=6, row=2, columnspan=5, pady=(30, 0))