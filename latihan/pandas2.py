import pandas as pd

data = {
    "tanggal": pd.date_range(start="2025-07-01", periods=20).strftime("%Y-%m-%d"),
    "open":   [100, 102, 105, 107, 110, 112, 115, 117, 119, 121,
               124, 122, 121, 123, 126, 128, 130, 129, 128, 127],
    "high":   [103, 106, 107, 110, 113, 116, 118, 120, 123, 124,
               127, 125, 123, 126, 129, 131, 133, 132, 130, 129],
    "low":    [99, 100, 102, 105, 108, 110, 113, 115, 117, 119,
               122, 120, 119, 121, 124, 126, 127, 125, 124, 123],
    "close":  [102, 104, 106, 108, 111, 114, 116, 119, 121, 120,
               123, 124, 120, 125, 127, 130, 129, 127, 126, 125],
    "volume": [1000, 1100, 1050, 1500, 1600, 1200, 1300, 1400, 1450, 1350,
               1500, 1550, 1250, 1350, 1400, 1450, 1500, 1380, 1320, 1280]
}

df = pd.DataFrame(data)

"""
✅ Tahap 3: Soal (dengan data baru)
1. Tambahkan kolom MA3 → rata-rata 3 hari terakhir dari close

2. Tambahkan kolom kondisi_candle → bullish, bearish, atau doji

3. Hitung jumlah masing-masing kondisi

4. Tambahkan kolom ma_gap = close - MA3
(boleh abaikan NaN pertama)
"""

df = pd.DataFrame(data)
print(df)

# moving average 3
df['ma3'] = df['close'].rolling(window=3).mean()
print(df)

# kolom kondisi candle
df['candlestik'] = ['bullish' if o < c else 'bearish' for o, c in zip(df['open'], df['close'])]
print(df)

