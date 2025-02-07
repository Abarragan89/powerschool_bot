from tkinter import ttk
import tkinter as tk
from utils.string_manipulations import get_student_list, first_name_last_initial
from utils.take_attendance import take_attendance

class Take_Attendance(ttk.Frame):
    def __init__(self, root_app):
        super().__init__(padding=10)

        # Set frame to grid and stretch it across the parent
        self.grid(sticky="nsew") 

        # Configure the columns in the frame for centering content
        for col in range(12):
            self.columnconfigure(col, weight=1)
        
        # Get Array of Student Names
        try:
            self.student_roster = get_student_list()
        except:
            self.student_roster = []
        # Tardy Students container
        self.tardy_students = {}

        # Absent Students container
        self.absent_students = []

        # Disabled items
        self.disabled_items = set()

        # Attendance Title
        self.frame_title = ttk.Label(self, text="Take Attendance", font=("Helvetica", 22))
        self.frame_title.grid(column=0, row=0, columnspan=12, pady=(0, 10))
        
        # ListBoxes Labels 
        tardy_label = tk.Label(self, text='Tardy', font=('Helvetica', 16), justify="center")
        tardy_label.grid(row=1, column=7, columnspan=6, pady=(0, 3))
        absent_label = tk.Label(self, text='Absent', font=('Helvetica', 16), justify="center")
        absent_label.grid(row=1, column=0, columnspan=6, pady=(0, 3))

        # Absent Listbox
        self.absent_listbox = tk.Listbox(
            self, 
            selectmode=tk.MULTIPLE, 
            height=22, 
            width=22,  
            font=('Helvetica', 14), 
            exportselection=False
        )
        self.absent_listbox.grid(row=2, column=0, columnspan=5, rowspan=5)
        self.absent_listbox.bind("<<ListboxSelect>>", self.on_absent_select)

        # Tardy Listbox
        self.tardy_listbox = tk.Listbox(
            self, 
            selectmode=tk.MULTIPLE, 
            height=22, 
            width=22, 
            font=('Helvetica', 14), 
            exportselection=False
        )
        self.tardy_listbox.grid(row=2, column=7, columnspan=5, rowspan=5)
        self.tardy_listbox.bind("<<ListboxSelect>>", self.on_tardy_select)
        
        # Populate the listbox with the full roster
        self.populate_listboxes()

        # Back to Dashbord Btn
        back_to_dashboard = ttk.Button(self, text='Back', command=lambda: root_app.show_frame('Dashboard'), width=4)
        back_to_dashboard.grid(row=0, column=0, sticky='wn')
        
        # Take Attendance Btn
        take_attendance_btn = ttk.Button(self, text='Submit Attendance', command=self.submit_attendance)
        take_attendance_btn.grid(row=2, column=6, sticky='s', rowspan=2)

        # Clear Btn
        clear_selection_btn = ttk.Button(self, text='Clear', command=self.clear_selection, width=4)
        clear_selection_btn.grid(row=3, column=6, rowspan=2, sticky='s')
    
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
    
    def clear_selection(self):
        for index in range(len(self.student_roster)):
            # Clear selections in both listboxes
            self.tardy_listbox.select_clear(index)
            self.absent_listbox.select_clear(index)
            # Clear the UI dimmed items
            self.tardy_listbox.itemconfig(index, fg="white")
            self.absent_listbox.itemconfig(index, fg="white")
            # Clear the list of Absent and Tardy students
            self.absent_students = []
            self.tardy_students = []
            # Clear the disabled items set
            self.disabled_items.clear()

    def submit_attendance(self):
        take_attendance(self.tardy_students, self.absent_students)
