from datetime import datetime

ERROR_MSG = "❗ Input tidak valid"

def menu_validator(prompt: str) -> int:
    """Validasi input menu (0-5)."""
    while True:
        try:
            pilihan = int(input(prompt))
            if 0 <= pilihan <= 6:
                return pilihan
            print("❗ Pilihan tidak tersedia.")
        except ValueError as e:
            print(f"{ERROR_MSG} : {e}")

def buy_sell_validator(prompt: str) -> str:
    """Validasi input posisi: 1 (Buy) atau 2 (Sell)."""
    while True:
        try:
            pilihan = int(input(prompt))
            if pilihan == 1:
                return "Buy"
            elif pilihan == 2:
                return "Sell"
            print("❗ Mohon hanya masukkan 1 (Buy) atau 2 (Sell)")
        except ValueError as e:
            print(f"{ERROR_MSG} : {e}")

def validasi_tanggal(prompt: str) -> str:
    """Validasi input tanggal dalam format dd-mm-yyyy."""
    while True:
        try:
            tanggal = input(prompt)
            format_tanggal = "%d-%m-%Y"
            objek_tanggal = datetime.strptime(tanggal, format_tanggal)
            return str(objek_tanggal.date())
        except Exception as e:
            print(f"{ERROR_MSG} : {e}")

def float_validasi(prompt: str) -> float:
    """Validasi input angka desimal."""
    while True:
        try:
            return float(input(prompt))
        except ValueError as e:
            print(f"{ERROR_MSG} : {e}")

class ValidatorSLTP:
    """
    Validasi SL dan TP berdasarkan posisi Buy/Sell dan harga entry.
    """

    def __init__(self, entry: float, posisi: str):
        self.entry = entry
        self.posisi = posisi

    def validator_sltp(self, prompt: str) -> float:
        """Input float biasa (tanpa validasi posisi)."""
        while True:
            try:
                return float(input(prompt))
            except ValueError as e:
                print(f"{ERROR_MSG} : {e}")

    def validator_sl(self, prompt: str) -> float:
        """Validasi SL harus benar posisi terhadap entry."""
        while True:
            try:
                sl = float(input(prompt))
                if self.posisi == "Buy" and sl < self.entry:
                    return sl
                elif self.posisi == "Sell" and sl > self.entry:
                    return sl
                else:
                    print("❗ SL tidak sesuai posisi (Buy → < entry, Sell → > entry)")
            except ValueError as e:
                print(f"{ERROR_MSG} : {e}")

    def validator_tp(self, prompt: str) -> float:
        """Validasi TP harus benar posisi terhadap entry."""
        while True:
            try:
                tp = float(input(prompt))
                if self.posisi == "Buy" and tp > self.entry:
                    return tp
                elif self.posisi == "Sell" and tp < self.entry:
                    return tp
                else:
                    print("❗ TP tidak sesuai posisi (Buy → > entry, Sell → < entry)")
            except ValueError as e:
                print(f"{ERROR_MSG} : {e}")
