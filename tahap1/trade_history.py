trade = []

while True:
    print("1. Tambah Trade")
    print("2. Lihat Semua Trade")
    print("0. Keluar")
    pilihan = int(input("Masukan Pilihan : "))
    if pilihan == 0:
        break
    elif pilihan == 1:
        tanggal = input("Masukan Tanggal ( Contoh: 17-08-1945): ")
        pair = str(input("Pair (Misal: GBPUSD) : "))
        # posisi = str(input("Posisi (Buy/ Sell) : "))
        # lot = float(input(" Lot (Misal: 0.5) : "))
        # entry = float(input("Masukan Harga Entry : "))
        # sl = float(input("Masukan harga SL : "))
        # tp = float(input("Masukan harga TP : "))
        # hasil = float(input("Masukan Profit/Loss dalam usd : "))
        # catatan = str(input("Catatan (Strategi, Alasan Entry, alasan psikologi atau yang lainnya) : "))
        trade_baru = {
            "tanggal": tanggal,
            "pair": pair,
            # "posisi": posisi,
            # "lot": lot,
            # "entry": entry,
            # "SL": sl,
            # "TP": tp,
            # "hasil": hasil,
            # "catatan": catatan
        }
        trade.append(trade_baru)
    elif pilihan == 2:
        for item in trade:
            if item == None:
                print("Tidak ada riwayat trade")
            else:
                for nomer, nama in enumerate(trade, start=1) :
                    print("=" * 30)
                    print(f"{nomer}. Tanggal : {item['tanggal']} \n Pair : {item['pair']}")
                    print("=" * 30)