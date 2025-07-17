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
