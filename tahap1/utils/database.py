import os
import json

DATA_DIR = "tahap1/data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")

def lihat():
    """Membaca data trade dari file JSON."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
        except json.JSONDecodeError:
            return []

def simpan(data):
    """Menyimpan data trade ke file JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
