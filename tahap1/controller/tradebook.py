from utils.database import lihat

def riwayat():
    trade = lihat()
    if not trade:
        print("❗ Belum ada riwayat trade.")
    else:
        print("\n=== RIWAYAT TRADE ===")
        for i, item in enumerate(trade, start=1):
            print(f"\nTrade #{i}")
            print(f"Tanggal : {item['tanggal']}")
            print(f"Pair    : {item['pair']}")
            print(f"Posisi  : {item['posisi']}")
            print(f"Lot     : {item['lot']}")
            print(f"Entry   : {item['entry']}")
            print(f"SL      : {item['SL']}")
            print(f"TP      : {item['TP']}")
            print(f"Hasil   : {item['hasil']} USD")
            print(f"Catatan : {item['catatan']}")

class Tradebook:
    def __init__(self):
        self.trade = lihat()
        
