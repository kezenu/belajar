from functools import reduce
profit = [100, 200, -50, 30]

# Target: 280

print(reduce(lambda x, y: x + y, profit))

pair = ["BTCUSD", "XAUUSD", "EURUSD"]

# Target: "BTCUSD,XAUUSD,EURUSD"
print(reduce(lambda x, y: x + "," + y, pair))

nama = ["ali", "budi", "cecep"]


# Target: 13
x = len(reduce(lambda x, y: x + y, nama))
print(x)
