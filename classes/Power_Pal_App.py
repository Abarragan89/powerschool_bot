from tkinter import *
from classes.frames.Welcome_Frame import Welcome_Frame
from classes.frames.Dashboard import Dashboard
from classes.frames.Take_Attendance import Take_Attendance
from classes.frames.Attendance_Audit import Attendance_Audit
from classes.frames.Documents import Documents

class Power_Pal_App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Power Pal")
        self.maxsize(520, 480) 
        self.minsize(550, 480) 
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Dictionary to hold frame instances
        self.frames = {}

        for F in (Welcome_Frame, Dashboard, Take_Attendance, Documents, Attendance_Audit):
            # Get name of class
            frame = F(self)  # `self` is PowerPalApp
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            for col in range(12):
                frame.columnconfigure(col, weight=1)
        self.choose_opening_frame()
        
    def show_frame(self, frame_name):
        """Show a frame for a given name."""
        frame = self.frames[frame_name]
        frame.tkraise()
    
    def choose_opening_frame(self):
        """Check crendentials.txt see if present to load welcome or dashboard"""
        try:
            with open('data/credentials.txt') as file:
                # Read contents of file to determien if dashboard or welcome frame
                file_lines = file.readlines()
                if len(file_lines) == 2:
                    self.show_frame('Dashboard')
                else:
                    self.show_frame('Welcome_Frame')
        except:
            self.show_frame('Welcome_Frame')
        
        