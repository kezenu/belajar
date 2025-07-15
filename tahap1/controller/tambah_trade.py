from utils.validasi import buy_sell_validator
from utils.validasi import Validator_SLTP
from utils.database import buat, lihat


def tambah():
    db = lihat()
    tanggal = input("Masukan Tanggal (Contoh: 17-08-1945): ")
    pair = input("Pair (Misal: GBPUSD): ")
    posisi = buy_sell_validator("Posisi (1 = buy, 2 = sell):(1/2) : ")
    lot = float(input("Lot (Misal: 0.5): "))
    entry = float(input("Harga Entry: "))
    validasi_sltp = Validator_SLTP(entry, posisi,"Masukan SL : ")
    sl = validasi_sltp.validator_sl()
    tp = float(input("Harga TP: "))
    hasil = float(input("Profit/Loss (USD): "))
    catatan = input("Catatan (opsional): ")

    trade_baru = {
        "tanggal": tanggal,
        "pair": pair,
        "posisi": posisi,
        "lot": lot,
        "entry": entry,
        "SL": sl,
        "TP": tp,
        "hasil": hasil,
        "catatan": catatan
    }
    db.append(trade_baru)
    buat(db)
    print("✅ Trade berhasil ditambahkan!")