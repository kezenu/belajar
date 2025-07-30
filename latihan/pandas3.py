import pandas as pd

"""
1 Jika:
close > ma3
dan rsi < 30
dan volume > 1500
dan close > open
Maka: entry_buy
2 Jika:
close < ma3
dan rsi > 70
dan volume > 1500
dan close < open
Maka: entry_sell
3 Jika:
RSI antara 45–55
dan volume < 1000
Maka: no_entry_zona_netral
Selain itu: wait

"""


data = {
    "open":   [100, 105, 110, 108, 115, 120, 117, 122, 119, 121],
    "high":   [103, 107, 113, 111, 118, 124, 119, 125, 121, 123],
    "low":    [98, 103, 108, 105, 113, 118, 114, 120, 117, 120],
    "close":  [102, 106, 111, 107, 116, 122, 115, 124, 118, 122],
    "volume": [1600, 1400, 1700, 800, 2000, 900, 1550, 1300, 950, 1800],
    "ma3":    [101, 105, 109, 110, 114, 121, 116, 120, 117, 120],
    "rsi":    [25, 48, 72, 52, 28, 50, 75, 35, 70, 85]
}

df = pd.DataFrame(data)

class Trade:
    def buy(self, row):
        if row['close'] > row['ma3'] and row['rsi'] < 30 and row['volume'] > 1500 and row['close'] > row['open']:
            return 'buy'
        elif row['close'] < row['ma3'] and row['rsi'] > 70 and row['volume'] > 1500 and row['close'] < row['open']:
            return 'sell'
        elif 45 <= row['rsi'] <= 55 and row['volume'] < 1000:
            return 'No Entry Zona Netral'
        else:
            return 'wait'
        
trade = Trade()
df['analisa'] = df.apply(trade.buy, axis=1)
print(df)