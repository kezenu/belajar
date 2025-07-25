angka = [120, 450, 50, 30, 700]
# Output: [700, 450, 120, 50, 30]

a = sorted(angka, reverse=True)
print(a)

pair = ["btc", "eurusd", "xauusd", "doge"]
# Output: ['btc', 'doge', 'eurusd', 'xauusd']

b = sorted(pair, key=lambda x: len(x))
print(b)

trades = [
    {"pair": "btc", "hasil": 50},
    {"pair": "xauusd", "hasil": -20},
    {"pair": "eurusd", "hasil": 100}
]
# Output: urut dari hasil paling besar ke kecil

c = sorted(trades, key=lambda x: x['hasil'], reverse=True)
print(c)