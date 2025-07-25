profit = [120, 0, -50, 100]
# Gunakan any() untuk mengecek:
# Apakah ada trade yang hasilnya negatif?

a = any(x < 0 for x in profit)
print(a)

hasil = [10, 20, 30, 40]
# Gunakan all() untuk mengecek:
# Apakah semua hasil bernilai positif?

b = all(x < 0 for x in hasil)
print(b)

catatan = ["oke", "baik", "", "mantap"]
# Gunakan any() untuk mengecek:
# Apakah ada catatan yang kosong (string kosong)?

c = any(x == "" for x in catatan)
print(c)

nama = ["wisnu", "budi", "sanjaya"]
# Gunakan all() untuk mengecek:
# Apakah semua nama dimulai dengan huruf kecil?
# Hint: pakai string method .islower()

d = all(map(lambda x :x.islower(), nama))
print(d)

# Pair harus terdiri dari 6 huruf kapital (misalnya: BTCUSD, EURUSD)
# Harus semua huruf kapital (.isupper())
# Panjangnya harus 6 karakter

pair = ["BTCUSD", "XAUusd", "EURUSD", "GBPJPY"]

# Output yang diharapkan: False
# Karena "XAUusd" tidak semua huruf kapital
