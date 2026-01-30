import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, time
import pytz
import time

# --- KONFIGURASI ---
SYMBOL = "EURUSD"  # Ganti dengan simbol yang Anda tradingkan
TIMEFRAME = mt5.TIMEFRAME_M15  # Timeframe untuk analisis (misal: M15, H1)
RISK_PERCENT = 2.0  # Risiko per trade dalam persen (2%)
RR_RATIO = 2.0  # Rasio Risk/Reward (1:2)
MIN_LOT = 0.01  # Minimal lot size
MAGIC_NUMBER = 12345  # Magic number untuk mengidentifikasi order dari bot ini

# Parameter untuk identifikasi Order Block
SWING_LOOKBACK = 20  # Jumlah candle ke belakang untuk mencari swing high/low
STRONG_MOVE_CANDLES = 3  # Jumlah candle berturut-turut untuk mengkonfirmasi pergerakan kuat

# Zona Waktu Indonesia Barat (WIB)
WIB = pytz.timezone("Asia/Jakarta")

# --- FUNGSI-FUNGSI UTAMA ---

def connect_mt5():
    """Menghubungkan ke terminal MetaTrader 5."""
    if not mt5.initialize():
        print("initialize() gagal, error code =", mt5.last_error())
        return False
    print("Berhasil terhubung ke MetaTrader 5")
    return True

def get_account_info():
    """Mendapatkan informasi saldo akun."""
    account_info = mt5.account_info()
    if account_info is None:
        print("Gagal mendapatkan info akun, error:", mt5.last_error())
        return None
    return account_info

def get_candles(symbol, timeframe, num_candles):
    """Mengambil data candlestick."""
    candles = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if candles is None:
        print("Gagal mendapatkan candle, error:", mt5.last_error())
        return None
    df = pd.DataFrame(candles)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def identify_order_blocks(df):
    """
    Mengidentifikasi potensi Order Block dari DataFrame candle.
    Mengembalikan list dari dictionary yang berisi informasi OB.
    """
    order_blocks = []
    df['is_bullish'] = df['close'] > df['open']
    df['is_bearish'] = df['close'] < df['open']

    for i in range(SWING_LOOKBACK, len(df) - STRONG_MOVE_CANDLES):
        # --- Cari Bullish Order Block (Candle bearish sebelum rally kuat) ---
        if df['is_bearish'].iloc[i]:
            is_strong_move = True
            for j in range(i + 1, i + 1 + STRONG_MOVE_CANDLES):
                if not df['is_bullish'].iloc[j] or df['low'].iloc[j] < df['low'].iloc[i]:
                    is_strong_move = False
                    break
            
            if is_strong_move:
                ob_high = df['high'].iloc[i]
                ob_low = df['low'].iloc[i]
                order_blocks.append({
                    'type': 'bullish',
                    'high': ob_high,
                    'low': ob_low,
                    'index': i,
                    'time': df['time'].iloc[i]
                })

        # --- Cari Bearish Order Block (Candle bullish sebelum drop kuat) ---
        if df['is_bullish'].iloc[i]:
            is_strong_move = True
            for j in range(i + 1, i + 1 + STRONG_MOVE_CANDLES):
                if not df['is_bearish'].iloc[j] or df['high'].iloc[j] > df['high'].iloc[i]:
                    is_strong_move = False
                    break
            
            if is_strong_move:
                ob_high = df['high'].iloc[i]
                ob_low = df['low'].iloc[i]
                order_blocks.append({
                    'type': 'bearish',
                    'high': ob_high,
                    'low': ob_low,
                    'index': i,
                    'time': df['time'].iloc[i]
                })
    
    # Hanya kembalikan OB yang paling relevan (terbaru) untuk setiap tipe
    bullish_obs = [ob for ob in order_blocks if ob['type'] == 'bullish']
    bearish_obs = [ob for ob in order_blocks if ob['type'] == 'bearish']
    
    latest_bullish = max(bullish_obs, key=lambda x: x['index']) if bullish_obs else None
    latest_bearish = max(bearish_obs, key=lambda x: x['index']) if bearish_obs else None
    
    return [ob for ob in [latest_bullish, latest_bearish] if ob is not None]

def check_for_trigger(order_blocks, current_price, last_candle):
    """Memeriksa apakah harga menyentuh salah satu Order Block."""
    if not order_blocks:
        return None

    for ob in order_blocks:
        if ob['type'] == 'bullish':
            # Trigger buy jika harga turun ke area OB
            if last_candle['low'] <= ob['low']:
                print(f"Trigger BUY terdeteksi di OB Bullish (Low: {ob['low']})")
                return {
                    'action': 'BUY',
                    'entry_price': current_price,
                    'sl_price': ob['low'] - 10 * mt5.symbol_info(SYMBOL).point, # SL sedikit di bawah OB low
                    'ob_info': ob
                }
        elif ob['type'] == 'bearish':
            # Trigger sell jika harga naik ke area OB
            if last_candle['high'] >= ob['high']:
                print(f"Trigger SELL terdeteksi di OB Bearish (High: {ob['high']})")
                return {
                    'action': 'SELL',
                    'entry_price': current_price,
                    'sl_price': ob['high'] + 10 * mt5.symbol_info(SYMBOL).point, # SL sedikit di atas OB high
                    'ob_info': ob
                }
    return None

def calculate_lot_size(sl_price, entry_price):
    """Menghitung ukuran lot berdasarkan risiko 2%."""
    account_info = get_account_info()
    if not account_info:
        return 0.01

    balance = account_info.balance
    risk_amount = balance * (RISK_PERCENT / 100.0)
    
    symbol_info = mt5.symbol_info(SYMBOL)
    if symbol_info is None:
        print("Symbol info tidak ditemukan")
        return 0.01
        
    tick_value = symbol_info.trade_tick_value
    tick_size = symbol_info.trade_tick_size
    points_per_tick = tick_size / symbol_info.point
    
    sl_distance_points = abs(entry_price - sl_price) / symbol_info.point
    lot_size = risk_amount / (sl_distance_points * tick_value)
    
    # Pembulatan ke bawah ke mikro lot terdekat
    lot_size = np.floor(lot_size * 100) / 100
    
    # Pastikan lot tidak kurang dari minimal
    if lot_size < MIN_LOT:
        lot_size = MIN_LOT
        
    print(f"Perhitungan Lot: Balance={balance:.2f}, Risk={risk_amount:.2f}, SL Points={sl_distance_points:.1f}, Lot={lot_size:.2f}")
    return lot_size

def place_order(signal):
    """Menempatkan order ke MetaTrader 5."""
    symbol_info = mt5.symbol_info(SYMBOL)
    if symbol_info is None:
        print(SYMBOL, "tidak ditemukan, tidak bisa melakukan order")
        return

    if not symbol_info.visible:
        print(SYMBOL, "tidak terlihat, mencoba untuk menampilkannya")
        if not mt5.symbol_select(SYMBOL, True):
            print("symbol_select({}}) gagal, error", mt5.last_error())
            return

    lot = calculate_lot_size(signal['sl_price'], signal['entry_price'])
    tp_distance = abs(signal['entry_price'] - signal['sl_price']) * RR_RATIO
    
    if signal['action'] == 'BUY':
        price = mt5.symbol_info_tick(SYMBOL).ask
        sl = signal['sl_price']
        tp = price + tp_distance
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": SYMBOL,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 10,
            "magic": MAGIC_NUMBER,
            "comment": "OB Bot Buy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    else: # SELL
        price = mt5.symbol_info_tick(SYMBOL).bid
        sl = signal['sl_price']
        tp = price - tp_distance
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": SYMBOL,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 10,
            "magic": MAGIC_NUMBER,
            "comment": "OB Bot Sell",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_send gagal, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
    else:
        print(f"Order {signal['action']} {lot:.2f} {SYMBOL} berhasil dibuka pada harga {price:.5f}")

def get_open_positions():
    """Mendapatkan posisi terbuka untuk simbol dan magic number tertentu."""
    positions = mt5.positions_get(symbol=SYMBOL, magic=MAGIC_NUMBER)
    if positions is None:
        print("Tidak ada posisi terbuka, error code=", mt5.last_error())
    elif len(positions) > 0:
        print(f"Ditemukan {len(positions)} posisi terbuka.")
        return positions
    return []

def close_all_positions():
    """Menutup semua posisi terbuka untuk bot ini."""
    open_positions = get_open_positions()
    if not open_positions:
        return
        
    for pos in open_positions:
        symbol = pos.symbol
        if pos.type == mt5.POSITION_TYPE_BUY:
            order_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
        else:
            order_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": pos.volume,
            "type": order_type,
            "position": pos.ticket,
            "price": price,
            "deviation": 10,
            "magic": MAGIC_NUMBER,
            "comment": "Bot close trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Gagal menutup posisi {}, error: {}".format(pos.ticket, result.comment))
        else:
            print(f"Posisi {pos.ticket} berhasil ditutup.")

def is_trading_time():
    """Memeriksa apakah saat ini adalah waktu trading."""
    now_wib = datetime.now(WIB).time()
    start_time = time(5, 0, 0)  # 05:00 WIB
    end_time = time(0, 0, 0)    # 00:00 WIB (tengah malam)
    
    # Jika sebelum tengah malam
    if now_wib >= start_time:
        return True
    # Jika setelah tengah malam (logika untuk jam 00:00 - 04:59)
    if now_wib < end_time:
        return False
        
    return True # Default, seharusnya tidak terjadi

# --- FUNGSI UTAMA (MAIN LOOP) ---
def main():
    if not connect_mt5():
        return

    print("Bot Trading Order Block dimulai. Tekan Ctrl+C untuk berhenti.")
    
    try:
        while True:
            now_wib = datetime.now(WIB)
            print(f"\n--- Cek Pukul {now_wib.strftime('%H:%M:%S')} WIB ---")

            # 1. Logika Penutupan di Tengah Malam
            if now_wib.hour == 0 and now_wib.minute == 0:
                print("Sekarang pukul 00:00 WIB. Menutup semua posisi...")
                close_all_positions()
                time.sleep(60) # Tunggu 1 menit untuk melewati tengah malam
                continue

            # 2. Cek Waktu Trading
            if not is_trading_time():
                print("Di luar jam trading (05:00 - 23:59 WIB). Menunggu...")
                time.sleep(60) # Cek lagi setiap 1 menit
                continue

            # 3. Cek Posisi Terbuka
            open_positions = get_open_positions()
            if open_positions:
                print("Ada posisi terbuka. Menunggu hingga TP/SL tercapai.")
                time.sleep(60) # Cek lagi setiap 1 menit
                continue

            # 4. Jika tidak ada posisi, lakukan analisis
            print("Tidak ada posisi terbuka. Melakukan analisis Order Block...")
            candles_df = get_candles(SYMBOL, TIMEFRAME, SWING_LOOKBACK + STRONG_MOVE_CANDLES + 10)
            if candles_df is None or len(candles_df) < SWING_LOOKBACK:
                print("Data candle tidak cukup untuk analisis.")
                time.sleep(60)
                continue
            
            last_candle = candles_df.iloc[-2] # Gunakan candle yang sudah tutup
            current_price = mt5.symbol_info_tick(SYMBOL).bid
            
            # Identifikasi Order Block
            order_blocks = identify_order_blocks(candles_df)
            
            if not order_blocks:
                print("Tidak ada Order Block yang teridentifikasi.")
                time.sleep(60)
                continue
                
            print(f"Ditemukan {len(order_blocks)} Order Block potensial.")
            for ob in order_blocks:
                print(f"  - {ob['type'].capitalize()} OB pada {ob['time'].strftime('%Y-%m-%d %H:%M')} (High: {ob['high']:.5f}, Low: {ob['low']:.5f})")

            # Cek apakah ada trigger
            signal = check_for_trigger(order_blocks, current_price, last_candle)
            
            if signal:
                place_order(signal)
            
            # Tunggu sebelum siklus berikutnya untuk menghindari spam
            time.sleep(10) # Cek setiap 10 detik saat dalam jam trading

    except KeyboardInterrupt:
        print("\nBot dihentikan oleh pengguna.")
    finally:
        mt5.shutdown()
        print("Koneksi ke MetaTrader 5 ditutup.")

if __name__ == "__main__":
    main()