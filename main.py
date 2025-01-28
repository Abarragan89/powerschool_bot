from tkinter import *
from tkinter import ttk
from take_attendance import take_attendance

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World").grid(column=0, row=0)
ttk.Button(frm, text="Initialize", command=take_attendance).grid(column=1, row=0)

root.mainloop()