import pandas as pd

path_json = "C:\\Users\\admal\\Documents\\GitHub\\belajar\\tahap1\\data\\data.json"
path_csv = "C:\\Users\\admal\\Documents\\GitHub\\belajar\\tahap1\\data\\csv\\data.csv"
df = pd.read_json(path_json)

x = df.to_csv(path_csv, index=False)