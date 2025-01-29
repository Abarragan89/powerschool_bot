from tkinter import *
from classes.Welcome_Frame import Welcome_Frame

class Power_Pal_App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Power Pal")
        self.geometry("500x400")
        self.maxsize(500, 400)
        self.minsize(400, 300)  
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Dictionary to hold frame instances
        self.frames = {}

        for F in (Welcome_Frame,):
            # Get name of class
            frame_name = F.__name__
            frame = F(parent=self)
            self.frames[frame_name] = frame
            frame.grid(sticky="nsew")
            for col in range(12):
                frame.columnconfigure(col, weight=1)
        
        def show_frame(self, frame_name):
            # Hide all frames
            for frames in self.frames.values():
                frame.grid_forget()
            
            # Show the selected frame
            frame = self.frames[frame_name]
            frame.grid(sticky="nsew")
        