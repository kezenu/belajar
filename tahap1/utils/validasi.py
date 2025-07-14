a = "input tidak valid"
def menu_validator(promt):
    while True:
        try:
            pilihan = int(input(promt))
            if 0 <= pilihan <= 2:
                return pilihan
            else:
                print("pilihan tidak tersedia")
                continue
        except ValueError as e:
            print(f"Pilihan tidak valid {e}")

def buy_sell_validator(promt):
    while True:
        try:
            buysell = int(input(promt))
            if buysell == 1:
                return "Buy"
            elif buysell == 2:
                return "Sell"
            else:
                print("Mohon hanya masukan 1 atau 2")
        except ValueError as e:
            print(f"{a} : {e}")

class Validator_SLTP:
    def __init__(self, entry, posisi, promt):
        self.entry = entry
        self.posisi = posisi
        self.promt = promt
    
    def validator_sltp(self):
        while True:
            try:
                sltp = float(input(self.promt))
                return sltp
            except ValueError as e:
                print(f"{a} : {e}")
    
    def validator_sl(self):
        while True:
            try:
                sl = float(input(self.promt))
                if self.posisi == "Buy":
                    if sl < self.posisi:
                        return sl
                    elif sl > self.posisi:
                        print("Saat Buy SL harus dibawah entry")
                        continue
                    else:
                        print("SL tidak valid")
                elif self.posisi == "Sell":
                    if sl > self.posisi:
                        return sl
                    elif sl < self.posisi:
                        print("Saat Sell, SL harus diatas entry")
                        continue
                    else:
                        print("SL tidak valid")
            except ValueError as e:
                print(f"{a} : {e}")