import keyring
from cryptography.fernet import Fernet
import os
from utils.get_data_file import get_data_file 

SERVICE_NAME = 'Power_Pal_App'
KEY_NAME = "fernet_key"
CREDENTIALS_FILE = get_data_file("data/credentials.txt")

def get_key():
    """Retrieve or generate the encryption key from keyring."""
    stored_key = keyring.get_password(SERVICE_NAME, KEY_NAME)

    # If key is not in keyring, generate and store it
    if stored_key is None:
        key = Fernet.generate_key()
        keyring.set_password(SERVICE_NAME, KEY_NAME, key.decode())  # Store as string
    else:
        key = stored_key.encode()  # Convert back to bytes
    
    return key

def encrypt_and_save_credentials(username, password):
    """Encrypt and save username & password to a file."""
    # 1. f.encrypt() = takes the bytes returned from encode()
    # 2. The returned salted bytes are now decoded() and back into string
    # 3. decode() = turns bytes into string
    # Encrypt the username and password (byte objects passed to Fernet)
    key = get_key() # get the same key from keyring

    f = Fernet(key)
    encrypted_username = f.encrypt(username.encode()).decode()
    encrypted_password = f.encrypt(password.encode()).decode()

    # Ensure the directory exists creates the data directory if doesn't exist
    os.makedirs(os.path.dirname(CREDENTIALS_FILE), exist_ok=True)

    # Save the encrypted credentials to a file
    with open(CREDENTIALS_FILE, "w") as file:
        file.write(f"{encrypted_username}\n{encrypted_password}")

def load_and_decrypt_credentials():
    """Load encrypted credentials from file and decrypt them."""
    key = get_key()  # Use the same key retrieved from keyring
    f = Fernet(key)

    # Read the encrypted credentials from the file
    with open(CREDENTIALS_FILE, "r") as file:
        encrypted_username, encrypted_password = file.read().splitlines()

    # Decrypt the username and password
    username = f.decrypt(encrypted_username.encode()).decode()
    password = f.decrypt(encrypted_password.encode()).decode()

    return (username, password)
