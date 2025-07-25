from utils.validasi import (
    buy_sell_validator,
    validasi_tanggal,
    float_validasi,
    ValidatorSLTP,
)
from utils.database import simpan, lihat

def trade_input():
    """Mengumpulkan input trade dari user dan membuat instance Trade."""
    trades = lihat()
    tanggal = validasi_tanggal("Masukkan Tanggal (Contoh: 17-08-1945): ")
    pair = input("Pair (Misal: GBPUSD): ")
    posisi = buy_sell_validator("Posisi (1 = Buy, 2 = Sell): ")
    lot = float_validasi("Lot (Misal: 0.5): ")
    entry = float_validasi("Harga Entry: ")
    validator = ValidatorSLTP(entry, posisi)
    sl = validator.validator_sl("Masukkan SL: ")
    tp = validator.validator_tp("Masukkan TP: ")
    hasil = float_validasi("Profit/Loss (USD): ")
    catatan = input("Catatan (opsional): ")

    return Trade(trades, tanggal, pair, posisi, lot, entry, sl, tp, hasil, catatan)

class Trade:
    """Representasi satu entri trade."""

    def __init__(self, trades, tanggal, pair, posisi, lot, entry, sl, tp, hasil, catatan):
        self.trades = trades
        self.tanggal = tanggal
        self.pair = pair
        self.posisi = posisi
        self.lot = lot
        self.entry = entry
        self.sl = sl
        self.tp = tp
        self.hasil = hasil
        self.catatan = catatan

    def to_dict(self):
        """Konversi objek ke bentuk dict (untuk disimpan)."""
        return {
            "tanggal": self.tanggal,
            "pair": self.pair,
            "posisi": self.posisi,
            "lot": self.lot,
            "entry": self.entry,
            "SL": self.sl,
            "TP": self.tp,
            "hasil": self.hasil,
            "catatan": self.catatan
        }

    def tampilan_ringkasan(self):
        """Menampilkan ringkasan trade (sebelum disimpan)."""
        data = self.to_dict()
        print("\n=== RINGKASAN TRADE ===")
        for k, v in data.items():
            print(f"{k.capitalize():8} : {v}")

    def save_json(self):
        """Konfirmasi dan simpan trade ke file JSON."""
        self.tampilan_ringkasan()
        while True:
            pilihan = input("Apakah anda yakin ingin menyimpan? (y/n): ").lower()
            if pilihan == "y":
                self.trades.append(self.to_dict())
                simpan(self.trades)
                print("✅ Trade berhasil ditambahkan!")
                return
            elif pilihan == "n":
                print("❌ Penyimpanan dibatalkan.")
                return
            else:
                print("❗ Mohon masukkan 'y' atau 'n'.")
