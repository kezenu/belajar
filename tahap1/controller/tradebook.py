from utils.database import lihat

class Tradebook:
    def __init__(self):
        self.trades = lihat()

    def lihat(self):
            if not self.trades:
                print("❗ Belum ada riwayat trade.")
            else:
                print("\n=== RIWAYAT TRADE ===")
                for i, item in enumerate(self.trades, start=1):
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
    
    # fumgsi untuk mencari data dari database dengan kata kunci pair dan menampilkannya
    def cari_by_pair(self, pair):
        hasil = [x for x in self.trades if x['pair'].lower() == pair.lower()]
        if not hasil:
            print(f"Tidak ada trade dengan pair: {pair}")
        else:
            print(f"\n=== HASIL PENCARIAN UNTUK PAIR {pair.upper()} ===")
            for i, item in enumerate(hasil, start=1):
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
