import pandas as pd
import datetime

path_json = "C:\\Users\\admal\\Documents\\GitHub\\belajar\\tahap1\\data\\data.json"

def eksport_csv():
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nama_file = f"tahap1/data/csv/data {tanggal}.csv"
    df = pd.read_json(path_json)
    df.to_csv(nama_file, index=False)
    print(f"Eksport CSV Berhasil, disimpan di {nama_file}")

eksport_csv()