from controller.trade import Trade
from controller.tradebook import Tradebook
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
        tradebook = Tradebook()
        tradebook.lihat()
    else:
        print("pilihan tidak valid")