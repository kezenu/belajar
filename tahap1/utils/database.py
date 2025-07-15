import os
import json

PATH = "tahap1/data/data.json"

def lihat():
    if not os.path.exists(PATH):
        return []
    with open(PATH,"r") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
        except json.JSONDecodeError:
            return []
        

def buat(data):
    with open(PATH, "w") as f:
        json.dump(data, f, indent=2)