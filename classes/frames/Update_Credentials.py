from tkinter import ttk
from utils.cryption import encrypt_and_save_credentials


def handle_update_credentials(username, password, self):
    """Function to handle updating credentials."""
    if not username or not password:
        # Show an error message if username or password is empty
        error_label = ttk.Label(self, text="Username and Password cannot be empty.", foreground="red")
        error_label.grid(column=0, row=5, columnspan=12, pady=(10, 0))
        return
    
    # wrape the encryption in try block to catch any errors
    try:
        # Encrypt and save the credentials
        encrypt_and_save_credentials(username, password)
    except Exception as e:  
        # Show an error message if encryption fails
        error_label = ttk.Label(self, text=f"Error saving credentials: {str(e)}", foreground="red")
        error_label.grid(column=0, row=5, columnspan=12, pady=(10, 0))
        return
    # If successful, show a success message
    success_label = ttk.Label(self, text="Credentials updated successfully!", foreground="green")
    success_label.grid(column=0, row=5, columnspan=12, pady=(10, 0))
    self.username.delete(0, 'end')  # Clear the username entry
    self.password.delete(0, 'end')  # Clear the password entry

class Update_Credentials(ttk.Frame):
    def __init__(self, root_app):
        # initi the Frame Class 
        super().__init__(padding=10)

        # Set frame to grid and stretch it across the parent
        self.grid(sticky="nsew") 

        # Configure the columns in the frame for centering content
        for col in range(12):
            self.columnconfigure(col, weight=1)

        # Back to Dashbord Btn
        back_to_dashboard = ttk.Button(self, text='Back', command=lambda: root_app.show_frame('Dashboard'), width=4)
        back_to_dashboard.grid(row=0, column=0, sticky='wn')
        
        # Welcome Title
        welcome_text = ttk.Label(self, text="Update Credentials", font=("Helvetica", 24))
        welcome_text.grid(column=0, row=0, columnspan=12, pady=10)

        # Instructions Text
        instructions_text = ttk.Label(
            self, 
            text="Update your PowerSchool username and password below.", 
            wraplength=420,  # Set the maximum width for wrapping
            justify="center",  # Center the text within the label
            font=("Helvetica", 13)
        )
        instructions_text.grid(column=0, row=1, columnspan=12, pady=(10, 30))

        # User Name Entry
        username_label = ttk.Label(self, text="Username", font=("Helvetica", 13))
        username_label.grid(column=0, row=2, sticky='w', padx=5)
        self.username = ttk.Entry(self)
        self.username.grid(column=0, row=3)

        # User Password Entry
        password_label = ttk.Label(self, text="Password", font=("Helvetica", 13))
        password_label.grid(column=8, row=2, sticky='w', padx=5)
        self.password = ttk.Entry(self, show="*")
        self.password.grid(column=8, row=3)

        # Initialize Btn
        initialize_btn = ttk.Button(
            self, 
            text="Update", 
            # command=lambda: get_student_demographics(self.username.get(), self.password.get(), root_app)
            command=lambda: handle_update_credentials(self.username.get(), self.password.get(), self)
        )
        initialize_btn.grid(column=0, row=4, columnspan=12, pady=(20, 0))
