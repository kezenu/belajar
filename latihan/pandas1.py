import pandas as pd

data = {
    "tanggal": ["2025-07-21", "2025-07-22", "2025-07-23", "2025-07-24", "2025-07-25"],
    "open": [100, 105, 103, 110, 108],
    "high": [106, 108, 111, 115, 113],
    "low": [99, 102, 100, 109, 106],
    "close": [105, 107, 110, 112, 110],
    "volume": [1000, 1200, 1500, 1300, 1100]
}
df = pd.DataFrame(data)

print("Tugas 1, Tampilkan 3 data")
preview = df.head(3)
print(preview)

print("Soal 2: Tambahkan kolom baru range = high - low")
df['range'] = df['high'] - df['low']
print(df)

print("📌 Soal 3: Hitung rata-rata volume semua hari")
print(f" Rata-rata Volume adalaha : {df['volume'].mean()}")

print("📌 Soal 4: Filter semua baris yang close > open")
bull_candle = df[df['close'] > df['open']]
print(bull_candle)

print("Soal 5: Tambahkan kolom return (persentase return dari open ke close)")
# Rumus: (close - open)/open * 100

df['return'] = (df['close'] - df['open']) / df['open'] *100
print(df)

#  Tugas kedua Group dan agregate
# 📌 Soal 1: Tambahkan kolom baru hari dari kolom tanggal
# Hint: gunakan pd.to_datetime() lalu .dt.day_name()

df['hari'] =  pd.to_datetime(df['tanggal']).dt.day_name()
print(df)

# 📌 Soal 2: Hitung rata-rata return untuk tiap hari (Senin, Selasa, dst)
hari_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df_mean = df.groupby('hari')['return'].mean().reindex(hari_order)
print(df_mean)

#  Soal 3: Hitung total volume untuk setiap hari

df_sum = df.groupby('hari')['volume'].sum()
print(df_sum)

# 📌 Soal 4: Ambil hari dengan rata-rata return tertinggi
df_max = df_mean.max()
hari_terbaik = df_mean.idxmax()
print(f"Hari rata-rata tertinggi : {hari_terbaik} : {df_max}")