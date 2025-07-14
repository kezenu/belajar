from utils.validasi import buy_sell_validator as buse
def tambah(trade):
    tanggal = input("Masukan Tanggal (Contoh: 17-08-1945): ")
    pair = input("Pair (Misal: GBPUSD): ")
    posisi = buse("Posisi (1 = buy, 2 = sell):(1/2) : ")
    lot = float(input("Lot (Misal: 0.5): "))
    entry = float(input("Harga Entry: "))
    sl = float(input("Harga SL: "))
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
    trade.append(trade_baru)
    print("✅ Trade berhasil ditambahkan!")