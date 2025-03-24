import json
from pathlib import Path

storage_dir = Path("storage")
storage_dir.mkdir(exist_ok=True)
file_path = storage_dir / "data.json"

def load_data():
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_message(username, message, timestamp):
    data = load_data()
    data[timestamp] = {"username": username, "message": message}
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
