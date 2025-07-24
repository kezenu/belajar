from utils.database import lihat, buat
from controller.trade import Trade

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
    
    def hapus_by_index(self, index):
        if 0 <= index < len(self.trades):
            trade = self.trades[index]
            print("\n--- Data yang akan dihapus ---")
            for k, v in trade.items():
                print(f"{k.capitalize()} : {v}")
            konfirmasi = input("Yakin ingin dihapus? (y/n): ")
            if konfirmasi.lower() == "y":
                del self.trades[index]
                buat(self.trades)
                print("✅ Trade berhasil dihapus.")
            else:
                print("❌ Dibatalkan.")
        else:
            print("❗ Index tidak ditemukan.")

    def performa_trade(self):
        if not self.trades:
            print("Data Trading kosong")
            return
        
        total = len(self.trades)
        win = [x for x in self.trades if x["hasil"] > 0]
        los = [x for x in self.trades if x["hasil"] < 0]
        net_profit = sum([x["hasil"] for x in self.trades])
        total_win = sum([x["hasil"] for x in win])
        rata_rata = net_profit / total
        winrate = len(win) / total *100
        best = max(self.trades, key=lambda x: x["hasil"])
        worst = min(self.trades, key=lambda x: x["hasil"])
        print(f"Total semua trade           : {total}")
        print(f"Total Win | Los             : {len(win)} | {len(los)}")
        print(f"Winrate                     : {winrate:.2f} %")
        print(f"Rata-rata hasil per trade   : {rata_rata:.2f} USD")
        print(F"Total profit                : {net_profit:.2f} USD")
        print(f"Trade terbaik               : {best['hasil']} USD ({best['pair']}) - {best['tanggal']} ")
        print(f"Trade terburuk              : {worst['hasil']} USD ({worst['pair']}) - {worst['tanggal']} ")