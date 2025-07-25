# profit = [120, -30, 0, 200, -50]
# # Buatlah list baru berisi hanya angka positif dari profit menggunakan list comprehension.

# angka_posistif = [x for x in profit if x >= 0]
# print(angka_posistif)

# pair = ["btc", "xauusd", "eurusd", "doge"]
# # Buat list baru berisi huruf kapital dari setiap pair, tapi hanya jika panjangnya 6 huruf.
# list_baru = [x.upper() for x in pair if len(x) == 6]
# print(list_baru)

# # #  Ujian 1

pair = ["BTCUSD", "xauusd", "DOGE", "ADA", "EURUSD", "SOL", "gbpjpy"]
profit = [120, -50, 70, -10, 150, 0, 200]

# ['BTCUSD menghasilkan 120 USD', 'EURUSD menghasilkan 150 USD']

# Tapi hanya untuk pair yang memenuhi:
# Panjang karakter tepat 6 huruf, dan
# Semua huruf kapital (uppercase)
# Dan profit-nya positif (> 0)

list_baru = zip(pair, profit)
hasil = [f"{a} menghasilkan {b} USD" for a, b in list_baru if len(a) == 6 and a.isupper() and b > 0]
print(hasil)

