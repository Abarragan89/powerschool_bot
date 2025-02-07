import os
import subprocess
import sys

def open_file_in_preview(file_path):
    # Open the generated PDF file
    if sys.platform == "win32":
        os.startfile(file_path)  # Windows
    elif sys.platform == "darwin":
        subprocess.run(["open", file_path])  # macOS
    else:
        subprocess.run(["xdg-open", file_path])  # Linux