from pathlib import Path
import os

def get_data_file(filename):
    base_dir = Path.home() / "Library" / "Application Support" / "PowerSchoolPal"
    os.makedirs(base_dir, exist_ok=True)
    return base_dir / filename