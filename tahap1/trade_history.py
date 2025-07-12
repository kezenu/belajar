trade = []

while True:
    print("\n=== CATATAN TRADING ===")
    print("1. Tambah Trade")
    print("2. Lihat Semua Trade")
    print("0. Keluar")
    pilihan = int(input("Masukan Pilihan : "))

    if pilihan == 0:
        break

    elif pilihan == 1:
        tanggal = input("Masukan Tanggal (Contoh: 17-08-1945): ")
        pair = input("Pair (Misal: GBPUSD): ")
        posisi = input("Posisi (Buy/Sell): ")
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

    elif pilihan == 2:
        if not trade:
            print("❗ Belum ada riwayat trade.")
        else:
            print("\n=== RIWAYAT TRADE ===")
            for i, item in enumerate(trade, start=1):
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
