import pandas as pd
from datetime import datetime, timedelta

# Simulasi data candle 1 menit
start = datetime(2025, 7, 31, 9, 0)
data = []

for i in range(30):  # 30 candle 1-menit
    time = start + timedelta(minutes=i)
    open_ = 100 + i
    high = open_ + 2
    low = open_ - 1
    close = open_ + (i % 3 - 1)
    data.append({
        "time": time,
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
    })

df = pd.DataFrame(data)
df.set_index("time", inplace=True)

print(df)

df_5min = df.resample("3min").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last"
})

print(df_5min)
