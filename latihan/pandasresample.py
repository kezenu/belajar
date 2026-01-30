import pandas as pd
from datetime import datetime, timedelta

"""
🧠 Tugasmu:
1. Resample jadi candle 3-menit
Gunakan fungsi .resample("3min")
Buat DataFrame baru bernama df_3min
Gunakan agg: open → first, high → max, low → min, close → last
2. Tambahkan kolom range:
range = high - low (per candle 3 menit)
3. Tambahkan kolom direction:
Jika close > open → "bullish"
Jika close < open → "bearish"
Jika sama → "doji"
4 Tampilkan 6 baris pertama dari df_3min dengan kolom:
open, high, low, close, range, direction
🎁 Bonus (opsional):
5 Berapa jumlah bullish, bearish, dan doji? (gunakan .value_counts()
"""


start = datetime(2025, 7, 31, 9, 0)
data = []

from datetime import datetime, timedelta

start = datetime(2025, 7, 31, 9, 0)
data = []

# Harga awal
price = 100

for i in range(18):  # 18 menit
    time = start + timedelta(minutes=i)
    
    # Fluktuasi harga: tiap 3 menit berubah arah
    if (i // 3) % 2 == 0:
        # Fase naik
        open_ = price
        close = open_ + 1
    else:
        # Fase turun
        open_ = price
        close = open_ - 1
    
    high = max(open_, close) + 1
    low = min(open_, close) - 1
    
    price = close  # update harga utk menit berikutnya

    data.append({"time": time, "open": open_, "high": high, "low": low, "close": close})
df = pd.DataFrame(data).set_index("time")

df_3min = df.resample('3min').agg({
    'open' : 'first',
    'low' : 'min',
    'high' : 'max',
    'close' : 'last'
})

df_3min['range'] = df_3min['high'] - df_3min['low']

def direction(row):
    if row['close'] > row['open']:
        return "Bullish"
    elif row['close'] < row['open']:
        return "Bearish"
    else:
        return "Doji"

df_3min['direction'] = df_3min.apply(direction, axis=1)
print(df)
print(df_3min)
print(df_3min.value_counts('direction'))

df = df.sort_index()
df_3min =  df_3min.sort_index()

df_join = pd.merge_asof(df, df_3min[['direction']], left_index=True, right_index=True)
df_join.rename(columns={'direction': 'direction_3m'}, inplace=True)
print(df_join)