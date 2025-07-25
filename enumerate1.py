nama = ["wisnu", "budi", "cecep"]

# Target Output:
# 1. wisnu
# 2. budi
# 3. cecep

for i, v in enumerate(nama, start=1):
    print(f"{i}. {v}")

pair = ["BTCUSD", "XAUUSD", "EURUSD"]
profit = [100, -20, 50]

# Output:
# Trade #1: BTCUSD hasil 100 USD
# Trade #2: XAUUSD hasil -20 USD
# Trade #3: EURUSD hasil 50 USD

for i, (p, h) in enumerate(zip(pair, profit), start=1):
    print(f"Trade {i}. {p} hasil {h}")

hasil = [120, -50, 300, -100]

# Tampilkan:
# Index ke-1 untung 120 USD
# Index ke-2 rugi -50 USD
# ...
untung_rugi = map(lambda x: f"{'untung' if x > 0 else 'rugi'}", hasil)
for i,(v, u) in enumerate(zip(hasil, untung_rugi), start=1):
    print(f"Index ke-{i} {v} {u} USD")