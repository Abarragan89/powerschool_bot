from tkinter import *
from tkinter import ttk
from take_attendance import take_attendance

# Initialize Window
root = Tk()
root.title = "Power Pal"
root.geometry("500x400")
# root.maxsize(500, 400)
# root.minsize(400,300)

# Create a Frame
welcome_frame = ttk.Frame(root, padding=10)
welcome_frame.grid()

# Welcome Text
welcome_text = Label(welcome_frame, text="Welcome to Power Pal!")
welcome_text.grid(column=0, row=0, columnspan=12)

# User Name Entry
username = ttk.Entry(welcome_frame)
username.grid(column=0, row=1)

# username.pack()

# User Password Entry
password = ttk.Entry(welcome_frame)
password.grid(column=6, row=1)

# ttk.Button(frm, text="update", command=root.update).grid(column=1, row=0)


root.mainloop()