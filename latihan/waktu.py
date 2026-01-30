from datetime import datetime, timedelta

# mengambil waktu sekarang
now = datetime.now()
print(now)  # Contoh: 2025-07-31 21:48:23.456789

#  membuat waktu manual (yy, mm, dd, hh, mm, ss)
dt = datetime(2025, 7, 31, 9, 30)  # jam 09:30 pagi
print(dt)

# akses waktu tertentu
print(dt.year)   # 2025
print(dt.month)  # 7
print(dt.day)    # 31
print(dt.hour)   # 9
print(dt.minute) # 30

#  menghitung selisih waktu
a = datetime(2025, 7, 31, 9, 0)
b = datetime(2025, 7, 31, 10, 0)
selisih = b - a
print(selisih)           # 1:00:00
print(selisih.total_seconds())  # 3600

# manipulasi waktu
dt = datetime(2025, 7, 31, 9, 0)

dt_plus_5min = dt + timedelta(minutes=5)
dt_minus_1hr = dt - timedelta(hours=1)

print(dt_plus_5min)
print(dt_minus_1hr)


# String ke datetime
dt_str = "2025-07-31 09:00"
dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
print(dt)

# Datetime ke string
dt_str_new = dt.strftime("%d/%m/%Y %H:%M")
print(dt_str_new)  # 31/07/2025 09:00
