harga = [500, 1500, 750, 2000, 1200]

# Target: [1500, 2000, 1200]
print(list(filter(lambda x: x > 1000, harga)))

pair = ["btc", "eth", "solana", "ada", "xrp", "doge"]

# Target: ['btc', 'eth', 'ada', 'xrp']
print(list(filter(lambda x: len(x) < 5, pair)))

hasil = [100, -20, 50, -50, 75]

# Target: [-20, -50]
print(list(filter(lambda x: x < 0 , hasil)))