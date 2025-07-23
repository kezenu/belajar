from datetime import datetime

# variabel a untuk kata yang berulang
a = "Input tidak valid"

# fungsi untuk validasi pada bagian menu agar tidak error saat user input diluar pilihan
def menu_validator(prompt):
    while True:
        try:
            pilihan = int(input(prompt))
            if 0 <= pilihan <= 4:
                return pilihan
            else:
                print("❗ Pilihan tidak tersedia.")
        except ValueError as e:
            print(f"{a} : {e}")

# fungsi untuk validasi masukan user pada buy sell, agar masukan hanya buy atau sell saja
def buy_sell_validator(prompt):
    while True:
        try:
            buysell = int(input(prompt))
            if buysell == 1:
                return "Buy"
            elif buysell == 2:
                return "Sell"
            else:
                print("❗ Mohon hanya masukan 1 (Buy) atau 2 (Sell)")
        except ValueError as e:
            print(f"{a} : {e}")

# validasi tanggal, untuk memastikan user memasukan tanggal sesuai dengan format standar, agar nanti mudah dikelola
def validasi_tanggal(prompt):
    while True:
        try:
            tanggal = input(prompt)
            format_tanggal = "%d-%m-%Y"
            objek_tanggal = datetime.strptime(tanggal, format_tanggal)
            hanya_tanggal = objek_tanggal.date()
            return str(hanya_tanggal)
        except Exception as e:
            print(f"{a} : {e}")

def float_validasi(prompt):
    while True:
        try:
            x = float(input(prompt))
            return x
        except ValueError as e:
            print(f" {a} : {e}")

# class atau fungsi agar user memasukan angka yang benar, contoh : saat buy tidak mungkin sl diatas harga entry, dan validasi agar memasukan angka 
class Validator_SLTP:
    def __init__(self, entry, posisi):
        self.entry = entry
        self.posisi = posisi

    def validator_sltp(self, prompt_sl):
        while True:
            try:
                sltp = float(input(prompt_sl))
                return sltp
            except ValueError as e:
                print(f"{a} : {e}")

    def validator_sl(self, prompt_sl):
        while True:
            try:
                sl = float(input(prompt_sl))
                if self.posisi == "Buy":
                    if sl < self.entry:
                        return sl
                    else:
                        print("❗ Saat Buy, SL harus di bawah entry")
                elif self.posisi == "Sell":
                    if sl > self.entry:
                        return sl
                    else:
                        print("❗ Saat Sell, SL harus di atas entry")
            except ValueError as e:
                print(f"{a} : {e}")

    def validator_tp(self, prompt_tp):
        while True:
            try:
                tp = float(input(prompt_tp))
                if self.posisi == "Buy":
                    if tp > self.entry:
                        return tp
                    else:
                        print("❗ Saat Buy, TP harus di atas entry")
                if self.posisi == "Sell":
                    if tp < self.entry:
                        return tp
                    else:
                        print("❗ Saat Sell, TP harus di bawah entry")
            except ValueError as e:
                print(f"{a} : {e}")
