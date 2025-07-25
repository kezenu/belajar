from functools import reduce

nama = ["ali", "budi", "cecep"]
profit = [120, -30, 90]

# Output:
# [('ali', 120), ('budi', -30), ('cecep', 90)]
a = list(zip(nama, profit))
print(a)

pair = ["btc", "eth", "sol"]
entry = [30000, 1800, 25]
hasil = [100, -50, 200]

# Output:
# [('btc', 30000, 100), ('eth', 1800, -50), ('sol', 25, 200)]

b = list(zip(pair, entry, hasil))
print(b)

nama = ["wisnu", "budi"]
profit = [100, -20]

# Output:
# Wisnu menghasilkan 100 USD
# Budi menghasilkan -20 USD
c = list(map(lambda x, y: f"{x} menghasilkan {y}", nama, profit))
print(c)