from tahap1.controller.trade import Trade
from tahap1.controller.tradebook import riwayat
from utils.validasi import menu_validator

while True:
    print("\n=== CATATAN TRADING ===")
    print("1. Tambah Trade")
    print("2. Lihat Semua Trade")
    print("0. Keluar")
    pilihan = menu_validator("Masukan Pilihan : ")
    
    if pilihan == 0:
        break
    elif pilihan == 1:
       trade = Trade()
       trade.save_json()
    elif pilihan == 2:
        riwayat()
    else:
        print("pilihan tidak valid")