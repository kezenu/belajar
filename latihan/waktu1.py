from datetime import datetime, timedelta


"""
🚀 Tugas Mini untuk Latihan:
Buatlah kode berikut:
Tampilkan waktu sekarang
Tambahkan 15 menit dari waktu sekarang
Tampilkan dalam format 31/07/2025 09:15
"""

sekarang = datetime.now()
tambah15 = sekarang + timedelta(minutes=15)
oke = tambah15.strftime("%d/%m/%Y %H:%M")
print(oke)