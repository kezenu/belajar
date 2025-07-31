import pandas as pd

"""
1. Hitung profit per trade berdasarkan posisi:
    Buy: (exit - entry) * qty
    Sell: (entry - exit) * qty
2. Tambahkan kolom profit ke dalam DataFrame.
3. Hitung metrik performa:
    Total profit
    Jumlah trade profit / loss
    Rata-rata profit per trade
    Akurasi winrate dalam persen
4. (Bonus) Hitung total profit per pair (groupby("pair"))

"""

data = [
    {"pair": "BTCUSDT", "entry": 50000, "exit": 52000, "qty": 0.01, "side": "buy"},
    {"pair": "ETHUSDT", "entry": 1800, "exit": 1700, "qty": 0.1, "side": "sell"},
    {"pair": "BTCUSDT", "entry": 51000, "exit": 50500, "qty": 0.01, "side": "buy"},
    {"pair": "ETHUSDT", "entry": 1750, "exit": 1800, "qty": 0.1, "side": "buy"},
]
df = pd.DataFrame(data)

def profit(row):
    if row['side'] == "buy":
        return (row['exit'] - row['entry']) * row['qty']
    elif row['side'] == 'sell':
        return (row['entry'] - row['exit']) * row['qty']
    else:
        None

df['profit'] = df.apply(profit, axis=1)

df_sum = df['profit'].sum()
df_profit = [f"Total Profit / Loss : {p}" for p in df['profit'] if len(p) >0]
print(f" Total Profit : {df_sum}")
print(df_profit)