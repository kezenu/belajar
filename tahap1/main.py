from controller.trade import Trade
from controller.tradebook import Tradebook
from utils.validasi import menu_validator


# menu utama
while True:
    print("\n=== CATATAN TRADING ===")
    print("1. Tambah Trade")
    print("2. Lihat Semua Trade")
    print("3. Cari trade")
    print("4. Hapus trade")
    print("0. Keluar")
    pilihan = menu_validator("Masukan Pilihan : ")
    
    if pilihan == 0: # pilihan 0 untuk keluar dari aplikasi
        break
    elif pilihan == 1: # menambahkan trade ke jurnal
        trade = Trade()
        trade.save_json()
    elif pilihan == 2: # Melihat semua transaksi
        tradebook = Tradebook()
        tradebook.lihat()
    elif pilihan == 3: # Mencari trade yang telah tersimpan dengan kata kunci pair
        tradebook = Tradebook()
        pair = input("Masukan pair yang ingin dicari : ")
        tradebook.cari_by_pair(pair)
    elif pilihan == 4: # Menghapus trade yang telah disimpan dengan kata kunci urutan
        pass
    else:
        print("pilihan tidak valid")