from tkinter import ttk
from utils.init_classroom import initialize_create_class

class Welcome_Frame(ttk.Frame):
    def __init__(self, root_app):
        # initi the Frame Class 
        super().__init__(padding=10)

        # Set frame to grid and stretch it across the parent
        self.grid(sticky="nsew") 

        # Configure the columns in the frame for centering content
        for col in range(12):
            self.columnconfigure(col, weight=1)
        
        # Welcome Title
        welcome_text = ttk.Label(self, text="Welcome to Power Pal!", font=("Helvetica", 24))
        welcome_text.grid(column=0, row=0, columnspan=12, pady=10)

        # Instructions Text
        instructions_text = ttk.Label(
            self, 
            text="Please provide your PowerSchool username and password. We will only ask for this once and only save it locally on your computer.", 
            wraplength=420,  # Set the maximum width for wrapping
            justify="center",  # Center the text within the label
            font=("Helvetica", 13)
        )
        instructions_text.grid(column=0, row=1, columnspan=12, pady=(10, 30))

        # User Name Entry
        username_label = ttk.Label(self, text="Username", font=("Helvetica", 13))
        username_label.grid(column=3, row=2, sticky='w', padx=5)
        self.username = ttk.Entry(self)
        self.username.grid(column=3, row=3)

        # User Password Entry
        password_label = ttk.Label(self, text="Password", font=("Helvetica", 13))
        password_label.grid(column=6, row=2, sticky='w', padx=5)
        self.password = ttk.Entry(self, show="*")
        self.password.grid(column=6, row=3)

        # Initialize Btn
        initialize_btn = ttk.Button(
            self, 
            text="Initialize", 
            command=lambda: initialize_create_class(self.username.get(), self.password.get(), root_app)
        )
        initialize_btn.grid(column=0, row=4, columnspan=12, pady=(20, 0))
