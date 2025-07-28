from controller.trade import trade_input
from controller.tradebook import Tradebook
from utils.validasi import menu_validator

def tampilkan_menu():
    print("\n=== CATATAN TRADING ===")
    print("1. Tambah Trade")
    print("2. Lihat Semua Trade")
    print("3. Cari trade")
    print("4. Hapus trade")
    print("5. Performa trading")
    print("6. Eksport ke CSV")
    print("0. Keluar")

def handle_tambah_trade():
    trade = trade_input()
    trade.save_json()

def handle_lihat_trade():
    tb = Tradebook()
    tb.lihat()

def handle_cari_trade():
    tb = Tradebook()
    pair = input("Masukkan pair yang ingin dicari: ")
    tb.cari_by_pair(pair)

def handle_hapus_trade():
    tb = Tradebook()
    tb.lihat()
    try:
        index = int(input("Masukkan nomor trade yang ingin dihapus: ")) - 1
        tb.hapus_by_index(index)
    except ValueError:
        print("❗ Input harus berupa angka.")

def handle_performa():
    tb = Tradebook()
    tb.performa_trade()

def main():
    while True:
        tampilkan_menu()
        pilihan = menu_validator("Masukan Pilihan: ")

        if pilihan == 0:
            print("👋 Keluar dari program.")
            break
        elif pilihan == 1:
            handle_tambah_trade()
        elif pilihan == 2:
            handle_lihat_trade()
        elif pilihan == 3:
            handle_cari_trade()
        elif pilihan == 4:
            handle_hapus_trade()
        elif pilihan == 5:
            handle_performa()
        else:
            print("❗ Pilihan tidak valid.")

if __name__ == "__main__":
    main()
