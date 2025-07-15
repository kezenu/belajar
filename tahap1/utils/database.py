import json

PATH = "tahap1/data/data.json"

def lihat():
    with open(PATH, "r") as f:
        return json.load(f)

def buat(data):
    with open(PATH, "w") as f:
        return json.dump(data, f, indent=2)