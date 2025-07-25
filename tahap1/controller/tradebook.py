from utils.database import lihat, simpan
from controller.trade import Trade

class Tradebook:
    def __init__(self):
        """Inisialisasi Tradebook dengan data dari file JSON."""
        self.trades = lihat()

    def lihat(self):
        """Menampilkan seluruh riwayat trade."""
        if not self.trades:
            print("❗ Belum ada riwayat trade.")
            return

        print("\n=== RIWAYAT TRADE ===")
        for i, item in enumerate(self.trades, start=1):
            self._tampilkan_trade(i, item)

    def cari_by_pair(self, pair):
        """Mencari trade berdasarkan pair tertentu."""
        hasil = [x for x in self.trades if x['pair'].lower() == pair.lower()]
        if not hasil:
            print(f"Tidak ada trade dengan pair: {pair}")
            return

        print(f"\n=== HASIL PENCARIAN UNTUK PAIR {pair.upper()} ===")
        for i, item in enumerate(hasil, start=1):
            self._tampilkan_trade(i, item)

    def hapus_by_index(self, index):
        """Menghapus trade berdasarkan index dalam list."""
        if 0 <= index < len(self.trades):
            trade = self.trades[index]
            print("\n--- Data yang akan dihapus ---")
            for k, v in trade.items():
                print(f"{k.capitalize()} : {v}")

            konfirmasi = input("Yakin ingin dihapus? (y/n): ")
            if konfirmasi.lower() == "y":
                del self.trades[index]
                simpan(self.trades)
                print("✅ Trade berhasil dihapus.")
            else:
                print("❌ Dibatalkan.")
        else:
            print("❗ Index tidak ditemukan.")

    def performa_trade(self):
        """Menampilkan performa keseluruhan dari semua trade."""
        if not self.trades:
            print("Data Trading kosong")
            return

        total = len(self.trades)
        win = [x for x in self.trades if x["hasil"] > 0]
        los = [x for x in self.trades if x["hasil"] < 0]
        net_profit = sum(x["hasil"] for x in self.trades)
        total_win = sum(x["hasil"] for x in win)
        rata_rata = net_profit / total
        winrate = len(win) / total * 100
        best = max(self.trades, key=lambda x: x["hasil"])
        worst = min(self.trades, key=lambda x: x["hasil"])

        print(f"Total semua trade           : {total}")
        print(f"Total Win | Los             : {len(win)} | {len(los)}")
        print(f"Winrate                     : {winrate:.2f} %")
        print(f"Rata-rata hasil per trade   : {rata_rata:.2f} USD")
        print(f"Total profit                : {net_profit:.2f} USD")
        print(f"Trade terbaik               : {best['hasil']} USD ({best['pair']}) - {best['tanggal']}")
        print(f"Trade terburuk              : {worst['hasil']} USD ({worst['pair']}) - {worst['tanggal']}")

    def _tampilkan_trade(self, index, item):
        """Menampilkan 1 trade."""
        print(f"\nTrade #{index}")
        print(f"Tanggal : {item['tanggal']}")
        print(f"Pair    : {item['pair']}")
        print(f"Posisi  : {item['posisi']}")
        print(f"Lot     : {item['lot']}")
        print(f"Entry   : {item['entry']}")
        print(f"SL      : {item['SL']}")
        print(f"TP      : {item['TP']}")
        print(f"Hasil   : {item['hasil']} USD")
        print(f"Catatan : {item['catatan']}")
