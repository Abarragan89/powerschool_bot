from pathlib import Path


def get_data_file(filename):
    base_dir = Path.home() / "Library" / "Application Support" / "YourAppName"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / filename