from tkinter import ttk
import tkinter as tk
from utils.get_students import get_student_list, first_name_last_initial
from utils.take_attendance import take_attendance

class Take_Attendance(ttk.Frame):
    def __init__(self, root_app):
        super().__init__()

        # Set frame to grid and stretch it across the parent
        self.grid(sticky="nsew") 

        # Configure the columns in the frame for centering content
        for col in range(12):
            self.columnconfigure(col, weight=1)
        
        # Get Array of Student Names
        self.student_roster = get_student_list()

        # Tardy Students container
        self.tardy_students = []

        #Absent Students container
        self.absent_students = []

        # Attendance Title
        self.frame_title = ttk.Label(self, text="Take Attendance", font=("Helvetica", 22))
        self.frame_title.grid(column=0, row=0, columnspan=12, pady=5)
        
        # ListBoxes Labels 
        tardy_label = tk.Label(self, text='Tardy', font=('Helvetica', 15), justify="center")
        tardy_label.grid(row=1, column=0, columnspan=6)
        absent_label = tk.Label(self, text='Absent', font=('Helvetica', 15), justify="center")
        absent_label.grid(row=1, column=6, columnspan=6)

        # Tardy Listbox
        self.tardy_listbox = tk.Listbox(
            self, 
            selectmode=tk.MULTIPLE, 
            height=15, 
            width=18, 
            font=('Helvetica', 14), 
            exportselection=False
        )
        self.tardy_listbox.grid(row=2, column=0, columnspan=6)
        self.tardy_listbox.bind("<<ListboxSelect>>", self.on_tardy_select)
        
        # Absent Listbox
        self.absent_listbox = tk.Listbox(
            self, 
            selectmode=tk.MULTIPLE, 
            height=15, 
            width=18,  
            font=('Helvetica', 14), 
            exportselection=False
        )
        self.absent_listbox.grid(row=2, column=6, columnspan=6)
        self.absent_listbox.bind("<<ListboxSelect>>", self.on_absent_select)

        # Populate the listbox with the full roster
        self.populate_listboxes(self.student_roster)

        take_attendance_btn = ttk.Button(self, text='Submit Attendance', command=self.submit_attendance)
        take_attendance_btn.grid(row=4, column=6)

    
    def populate_listboxes(self, students):
        for student in students:
            self.tardy_listbox.insert(tk.END, f" {first_name_last_initial(student)}")
            self.absent_listbox.insert(tk.END, f" {first_name_last_initial(student)}")

    def on_tardy_select(self, event):
        # clear out the tardy list
        self.tardy_students = []
        # populate list with new values
        selected = self.tardy_listbox.curselection()
        for index in selected:
            self.tardy_students.append(self.student_roster[index])

    def on_absent_select(self, event):
        # clear out the absent list
        self.absent_students = []
        # populate list with new values
        selected = self.absent_listbox.curselection()
        for index in selected:
            self.absent_students.append(self.student_roster[index])
    
    def submit_attendance(self):
        print(f"tardies {self.tardy_students}")
        print(f"absences {self.absent_students}")
        take_attendance(self.tardy_students, self.absent_students)

