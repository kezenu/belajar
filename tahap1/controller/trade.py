from utils.validasi import buy_sell_validator, validasi_tanggal, float_validasi
from utils.validasi import Validator_SLTP
from utils.database import buat, lihat


def trade_input():
    data_list = lihat()
    tanggal = validasi_tanggal("Masukan Tanggal (Contoh: 17-08-1945): ")
    pair = input("Pair (Misal: GBPUSD): ")
    posisi = buy_sell_validator("Posisi (1 = buy, 2 = sell):(1/2) : ")
    lot = float_validasi("Lot (Misal: 0.5): ")
    entry = float_validasi("Harga Entry: ")
    validasi_sltp = Validator_SLTP(entry, posisi)
    sl = validasi_sltp.validator_sl(" Masukan SL :")
    tp = validasi_sltp.validator_tp("Masukan TP :")
    hasil = float_validasi("Profit/Loss (USD): ")
    catatan = input("Catatan (opsional): ")
    return Trade(data_list, tanggal, pair, posisi, lot, entry, sl, tp, hasil, catatan)

class Trade:
    # fungsi inisialisasi untuk input trade
    def __init__(self, data_list, tanggal, pair, posisi, lot, entry, sl, tp, hasil, catatan):
        self.data_list = data_list
        self.tanggal = tanggal
        self.pair = pair
        self.posisi = posisi
        self.lot = lot
        self.entry = entry
        self.sl = sl
        self.tp = tp
        self.hasil = hasil
        self.catatan = catatan

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
                    self.data_list.append(self.to_dict())
                    buat(self.data_list)
                    print("✅ Trade berhasil ditambahkan!")
                    return
                if pilihan not in "y" or "n":
                    print("Mohon masukan input yang benar")
            except ValueError as e:
                print(f"Input tidak valid {e}")