from utils.validasi import buy_sell_validator
from utils.validasi import Validator_SLTP
from utils.database import buat, lihat

class Trade:
    def __init__(self):
        self.db = lihat()
        self.tanggal = input("Masukan Tanggal (Contoh: 17-08-1945): ")
        self.pair = input("Pair (Misal: GBPUSD): ")
        self.posisi = buy_sell_validator("Posisi (1 = buy, 2 = sell):(1/2) : ")
        self.lot = float(input("Lot (Misal: 0.5): "))
        self.entry = float(input("Harga Entry: "))
        validasi_sltp = Validator_SLTP(self.entry, self.posisi)
        self.sl = validasi_sltp.validator_sl(" Masukan SL :")
        self.tp = validasi_sltp.validator_tp("Masukan TP :")
        self.hasil = float(input("Profit/Loss (USD): "))
        self.catatan = input("Catatan (opsional): ")

    def to_dict(self):
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
    
    def save_json(self):
        self.db.append(self.to_dict())
        buat(self.db)
        print("✅ Trade berhasil ditambahkan!")