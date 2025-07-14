from controller.tambah_trade import tambah
from controller.riwayat_trade import riwayat
from data.data import data


while True:
    print("\n=== CATATAN TRADING ===")
    print("1. Tambah Trade")
    print("2. Lihat Semua Trade")
    print("0. Keluar")
    pilihan = int(input("Masukan Pilihan : "))
    
    if pilihan == 0:
        break

    elif pilihan == 1:
       tambah(data)

    elif pilihan == 2:
        riwayat(data)
    else:
        print("pilihan tidak valid")