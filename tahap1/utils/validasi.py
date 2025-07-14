a = "Input tidak valid"

def menu_validator(prompt):
    while True:
        try:
            pilihan = int(input(prompt))
            if 0 <= pilihan <= 2:
                return pilihan
            else:
                print("❗ Pilihan tidak tersedia.")
        except ValueError as e:
            print(f"{a} : {e}")

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

class Validator_SLTP:
    def __init__(self, entry, posisi, prompt):
        self.entry = entry
        self.posisi = posisi
        self.prompt = prompt
    
    def validator_sltp(self):
        while True:
            try:
                sltp = float(input(self.prompt))
                return sltp
            except ValueError as e:
                print(f"{a} : {e}")
    
    def validator_sl(self):
        while True:
            try:
                sl = float(input(self.prompt))
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
