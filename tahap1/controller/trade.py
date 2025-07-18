from utils.validasi import buy_sell_validator, validasi_tanggal
from utils.validasi import Validator_SLTP
from utils.database import buat, lihat

class Trade:
    # fungsi inisialisasi untuk input trade
    def __init__(self):
        self.db = lihat()
        self.tanggal = validasi_tanggal("Masukan Tanggal (Contoh: 17-08-1945): ")
        self.pair = input("Pair (Misal: GBPUSD): ")
        self.posisi = buy_sell_validator("Posisi (1 = buy, 2 = sell):(1/2) : ")
        self.lot = float(input("Lot (Misal: 0.5): "))
        self.entry = float(input("Harga Entry: "))
        validasi_sltp = Validator_SLTP(self.entry, self.posisi)
        self.sl = validasi_sltp.validator_sl(" Masukan SL :")
        self.tp = validasi_sltp.validator_tp("Masukan TP :")
        self.hasil = float(input("Profit/Loss (USD): "))
        self.catatan = input("Catatan (opsional): ")

    # memastikan masukan user berbentuk dict
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
    
    # tampilan ringkasan saat user mendapat konfirmasi, disa digunakan berulang
    def tampilan_ringkasan(self):
        data = self.to_dict()
        print(f"Tanggal : {data['tanggal']}")
        print(f"Pair    : {data['pair']}")
        print(f"Posisi  : {data['posisi']}")
        print(f"Lot     : {data['lot']}")
        print(f"Entry   : {data['entry']}")
        print(f"SL      : {data['SL']}")
        print(f"TP      : {data['TP']}")
        print(f"Hasil   : {data['hasil']} USD")
        print(f"Catatan : {data['catatan']}")

    # menyimpan data ke database saat user telah konfirmasi
    def save_json(self):
        self.tampilan_ringkasan()
        while True:
            try:
                pilihan = input("Apakah anda yakin (y/n) : ")
                if pilihan == "y":
                    self.db.append(self.to_dict())
                    buat(self.db)
                    print("✅ Trade berhasil ditambahkan!")
                    return
                else:
                    return
            except ValueError as e:
                print(f"Input tidak valid {e}")