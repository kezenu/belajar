#  BAGIAN 1 MAP()

angka = [2, 3, 4, 5]
# Hasil yang diinginkan: [4, 9, 16, 25]

kuadrat = list(map(lambda x : x ** 2, angka))
print(kuadrat)

nama = ["ali", "budi", "cecep"]
# Hasil: ['ALI', 'BUDI', 'CECEP']

nama_besar = list(map(lambda x: x.upper(), nama))
print(nama_besar)

pair = ["btc", "xauusd", "eurusd", "gbpjpy"]
# Hasil: [3, 6, 6, 6]

pair_besar = (list(map(lambda x:len(x), pair)))
print(pair_besar)


profit = [120, 300.5, -90, 45]
# Hasil: ['120 USD', '300.5 USD', '-90 USD', '45 USD']

profit_usd = list(map(lambda x: str(x) + " USD", profit))
print(profit_usd)

# Diberikan:
nama = ["wisnu", "sanjaya", "budi"]

# Target:
# ['wisnu (5)', 'sanjaya (7)', 'budi (4)']
nama_len = list(map(lambda x: x + f" ({str(len(x))})", nama))
print(nama_len)

# Diberikan:
angka = [1, 2, 3, 4, 5]

# Output contoh:
# ['Angka 1 adalah bilangan ganjil', 'Angka 2 adalah bilangan genap', ...]
angka_ganjil_genap = list(map(lambda x: f" {x} adalah bilangan {'genap' if x % 2 == 0 else 'ganjil'}", angka))
print(angka_ganjil_genap)

def kali_3(x):
    return x *3

print(list(map(kali_3, angka)))