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
        self.tardy_students = {}

        # Absent Students container
        self.absent_students = []

        # Disabled items
        self.disabled_items = set()

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
        self.populate_listboxes()

        # Take Attendance Btn
        take_attendance_btn = ttk.Button(self, text='Submit Attendance', command=self.submit_attendance)
        take_attendance_btn.grid(row=4, column=6)

        # Back to Dashbord Btn
        back_to_dashboard = ttk.Button(self, text='Dashboard', command=lambda: root_app.show_frame('Dashboard'))
        back_to_dashboard.grid(row=4, column=0)
    
    def populate_listboxes(self):
        for student in self.student_roster:
            self.tardy_listbox.insert(tk.END, f" {first_name_last_initial(student)}")
            self.absent_listbox.insert(tk.END, f" {first_name_last_initial(student)}")

    def on_tardy_select(self, event):
        # Make two sets to find out the newly added student
        current_tardy_list = set(self.tardy_students)
        selected_tardy = set(self.student_roster[index] for index in self.tardy_listbox.curselection())

        # Find the difference between two sets (the new student) 
        current_student = selected_tardy.difference(current_tardy_list)

        # only run this if there is an actual difference
        if len(current_student) > 0:
            current_student = current_student.pop()
            if f"tardy_{current_student}" in self.disabled_items:
                print('made a match.com')
                student_index = self.student_roster.index(current_student)
                self.tardy_listbox.selection_clear(student_index)
                return

        # clear out the tardy list
        self.tardy_students = []

        # Get Selected Indexes
        selected = self.tardy_listbox.curselection()

        # populate the absent array
        for num, student in enumerate(self.student_roster):
            # This puts the students full name rather than the abbreviated name in array
            if num in selected:
                self.tardy_students.append(student)
            # Dim out the selected in the alternate list
            if num in selected:
                self.absent_listbox.itemconfig(num, fg="gray")
                self.disabled_items.add(f"absent_{student}")
            else:
                self.absent_listbox.itemconfig(num, fg="white")
                if f"absent_{student}" in self.disabled_items:  # Check before removing
                    self.disabled_items.remove(f"absent_{student}")
            
    def on_absent_select(self, event):
        # Make two sets to find out the newly added student
        current_absent_list = set(self.absent_students)
        selected_absent = set(self.student_roster[index] for index in self.absent_listbox.curselection())
        current_student = selected_absent.difference(current_absent_list)
        
        # only run this if there is an actual difference
        if len(current_student) > 0:
            current_student = current_student.pop()
            if f"absent_{current_student}" in self.disabled_items:
                student_index = self.student_roster.index(current_student)
                self.absent_listbox.selection_clear(student_index)
                return
            
        # clear out the absent list
        self.absent_students = []

        # Get Selected Indexes
        selected = self.absent_listbox.curselection()

        # populate the absent array
        for num, student in enumerate(self.student_roster):
            # This puts the students full name rather than the abbreviated name in array
            if num in selected:
                self.absent_students.append(student)
            # Dim out the selected in the alternate list
            if num in selected:
                self.tardy_listbox.itemconfig(num, fg="gray")
                self.disabled_items.add(f"tardy_{student}")
            else:
                self.tardy_listbox.itemconfig(num, fg="white")
                if f"tardy_{student}" in self.disabled_items:  # Check before removing
                    self.disabled_items.remove(f"tardy_{student}")

    
    def submit_attendance(self):
        # take_attendance(self.tardy_students, self.absent_students)
        print(f"tardy students", self.tardy_students)
        print(f"absent students", self.absent_students)
        print(f"disabled items ", self.disabled_items)

