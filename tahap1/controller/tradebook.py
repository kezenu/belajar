from utils.database import lihat

class Tradebook:
    def __init__(self):
        self.trade = lihat()

    def lihat(self):
            if not self.trade:
                print("❗ Belum ada riwayat trade.")
            else:
                print("\n=== RIWAYAT TRADE ===")
                for i, item in enumerate(self.trade, start=1):
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