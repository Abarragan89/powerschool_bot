from classes.Welcome_Frame import Welcome_Frame
from classes.Power_Pal_App import Power_Pal_App



if __name__ == "__main__":
    app = Power_Pal_App()

    

    app.mainloop()




# # Configure root grid
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# # Create a Frame
# welcome_frame = ttk.Frame(root, padding=10)
# welcome_frame.grid(sticky="nsew")  # Center the frame in the root window

# # Configure the columns in the frame for centering content
# for col in range(12):
#     welcome_frame.columnconfigure(col, weight=1)

# # Welcome Text
# welcome_text = Label(welcome_frame, text="Welcome to Power Pal!", font=("Helvetica", 24))
# welcome_text.grid(column=0, row=0, columnspan=12, pady=10)

# # Instructions Text
# instructions_text = Label(
#     welcome_frame, 
#     text="Please provide your PowerSchool username and password. We will only ask for this once and only save it locally on your computer.", 
#     wraplength=420,  # Set the maximum width for wrapping
#     justify="center",  # Center the text within the label
#     font=("Helvetica", 13)
# )
# instructions_text.grid(column=0, row=1, columnspan=12, pady=(10, 30))  # Center across 12 columns

# # User Name Entry
# username_label = ttk.Label(welcome_frame, text="Username", font=("Helvetica", 13))
# username_label.grid(column=3, row=2, sticky='w', padx=5)
# username = ttk.Entry(welcome_frame)
# username.grid(column=3, row=3)

# # User Password Entry
# password_label = ttk.Label(welcome_frame, text="Password", font=("Helvetica", 13))
# password_label.grid(column=6, row=2, sticky='w', padx=5)
# password = ttk.Entry(welcome_frame, show="*")
# password.grid(column=6, row=3)



# # Initialize Btn
# initialize_btn = ttk.Button(welcome_frame, text="Initialize", command=lambda: create_class(username.get(), password.get()))
# initialize_btn.grid(column=0, row=4, columnspan=12, pady=(20, 0))



# Start the main loop
root.mainloop()
