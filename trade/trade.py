import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, time
import pytz
import time
import warnings

warnings.filterwarnings('ignore')

# --- KONFIGURASI UTAMA ---
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_H1
MAGIC_NUMBER = 12345

# --- KONFIGURASI MANAJEMEN RISIKO ---
RISK_PERCENT = 2.0
RR_RATIO = 2.0
MIN_LOT = 0.01
ATR_PERIOD = 14
RISK_MULTIPLIER = 1.5
REWARD_MULTIPLIER = 3.0

# --- KONFIGURASI FILTER & BATASAN ---
# Waktu Trading Umum (WIB)
TRADING_START_TIME = time(5, 0, 0)
TRADING_END_TIME = time(23, 59, 0)
MIDNIGHT_CLOSE_TIME = time(0, 0, 10)

# --- PENAMBAHAN: FILTER SESI TRADING ---
# Hanya trade di jam-jam likuiditas tinggi (Sesi London & New York)
TRADING_SESSION_START_TIME = time(13, 0, 0) # <-- ANDA BISA UBAH INI
TRADING_SESSION_END_TIME = time(22, 0, 0)   # <-- ANDA BISA UBAH INI

# --- PENAMBAHAN: FILTER KEPERCAYAAN MODEL ---
# Hanya trade jika model yakin di atas persentase ini
MODEL_CONFIDENCE_THRESHOLD = 0.70 # <-- ANDA BISA UBAH INI (0.70 = 70%)

# Batasan Harian
MAX_TRADES_PER_DAY = 3
MAX_DAILY_LOSS_PERCENT = 5.0
MAX_CONSECUTIVE_LOSSES = 3

# Batasan Akun
MAX_DRAWDOWN_PERCENT = 15.0

# Filter Spread
MAX_SPREAD_MULTIPLIER = 3.0

# --- FILE MODEL ---
MODEL_BUY_FILE = "model_buy.pkl"
MODEL_SELL_FILE = "model_sell.pkl"

# --- STATE MANAGEMENT ---
class DailyState:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.date = datetime.now(pytz.timezone("Asia/Jakarta")).date()
        self.trades_today = 0
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.initial_balance = self._get_initial_balance()

    def _get_initial_balance(self):
        account = mt5.account_info()
        return account.balance if account else 0

    def is_new_day(self):
        return datetime.now(pytz.timezone("Asia/Jakarta")).date() != self.date

    def update(self, pnl):
        self.daily_pnl += pnl
        self.trades_today += 1
        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

# --- FUNGSI-FUNGSI PENDUKUNG ---

def connect_mt5():
    if not mt5.initialize():
        print("initialize() gagal, error code =", mt5.last_error())
        return False
    print("Berhasil terhubung ke MetaTrader 5")
    return True

def get_account_info():
    return mt5.account_info()

def get_candles(symbol, timeframe, num_candles):
    candles = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if candles is None:
        print("Gagal mendapatkan candle, error:", mt5.last_error())
        return None
    df = pd.DataFrame(candles)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

def add_features(df):
    df.ta.rsi(length=14, append=True)
    df.ta.stoch(k=14, d=3, append=True)
    df.ta.sma(length=20, append=True)
    df.ta.sma(length=50, append=True)
    df.ta.ema(length=100, append=True)
    df.ta.atr(length=ATR_PERIOD, append=True)
    df.ta.bbands(length=20, std=2, append=True)
    df.ta.adx(length=14, append=True)
    return df.dropna()

def calculate_lot_size(entry_price, sl_price):
    account_info = get_account_info()
    if not account_info: return MIN_LOT
    balance = account_info.balance
    risk_amount = balance * (RISK_PERCENT / 100.0)
    
    symbol_info = mt5.symbol_info(SYMBOL)
    if not symbol_info: return MIN_LOT
        
    tick_value = symbol_info.trade_tick_value
    sl_distance_points = abs(entry_price - sl_price) / symbol_info.point
    lot_size = risk_amount / (sl_distance_points * tick_value)
    
    lot_size = np.floor(lot_size * 100) / 100
    return max(lot_size, MIN_LOT)

def place_order(action, sl_price, tp_price):
    symbol_info = mt5.symbol_info(SYMBOL)
    if not symbol_info or not symbol_info.visible:
        if not mt5.symbol_select(SYMBOL, True):
            print("Gagal memilih simbol", SYMBOL)
            return

    tick = mt5.symbol_info_tick(SYMBOL)
    current_spread_points = tick.ask - tick.bid
    
    if action == 'BUY':
        sl_price_adjusted = sl_price - current_spread_points
        entry_price_for_calc = tick.ask
    else: # SELL
        sl_price_adjusted = sl_price + current_spread_points
        entry_price_for_calc = tick.bid

    lot = calculate_lot_size(entry_price_for_calc, sl_price_adjusted)
    
    price = entry_price_for_calc
    request = {
        "action": mt5.TRADE_ACTION_DEAL, "symbol": SYMBOL, "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if action == 'BUY' else mt5.ORDER_TYPE_SELL,
        "price": price, "sl": sl_price_adjusted, "tp": tp_price, "deviation": 10,
        "magic": MAGIC_NUMBER, "comment": f"ML Bot {action}",
        "type_time": mt5.ORDER_TIME_GTC, "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"order_send gagal, retcode={result.retcode}, {result.comment}")
    else:
        print(f"Order {action} {lot:.2f} {SYMBOL} berhasil dibuka pada harga {price:.5f} (SL disesuaikan untuk spread)")

def get_open_positions():
    return mt5.positions_get(symbol=SYMBOL, magic=MAGIC_NUMBER)

def close_all_positions():
    open_positions = get_open_positions()
    for pos in open_positions:
        symbol = pos.symbol
        order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if pos.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(symbol).ask
        request = {
            "action": mt5.TRADE_ACTION_DEAL, "symbol": symbol, "volume": pos.volume,
            "type": order_type, "position": pos.ticket, "price": price,
            "deviation": 10, "magic": MAGIC_NUMBER, "comment": "Bot close trade",
            "type_time": mt5.ORDER_TIME_GTC, "type_filling": mt5.ORDER_FILLING_IOC,
        }
        mt5.order_send(request)

# --- PERUBAHAN: FUNGSI WAKTU TRADING YANG DIPERBARUI ---
def is_trading_time():
    """Memeriksa apakah saat ini berada dalam jam trading umum dan sesi trading yang diizinkan."""
    now_wib = datetime.now(pytz.timezone("Asia/Jakarta")).time()
    
    # Cek jam trading umum
    in_general_time = TRADING_START_TIME <= now_wib <= TRADING_END_TIME
    
    # Cek sesi trading spesifik
    in_session_time = TRADING_SESSION_START_TIME <= now_wib <= TRADING_SESSION_END_TIME
    
    if not in_general_time:
        print("Di luar jam trading umum (05:00 - 23:59 WIB). Menunggu...")
        return False
        
    if not in_session_time:
        print(f"Di luar jam sesi trading ({TRADING_SESSION_START_TIME.strftime('%H:%M')} - {TRADING_SESSION_END_TIME.strftime('%H:%M')} WIB). Menunggu...")
        return False
        
    return True

def is_spread_normal():
    symbol_info = mt5.symbol_info(SYMBOL)
    if not symbol_info: return False
    
    tick = mt5.symbol_info_tick(SYMBOL)
    current_spread_points = tick.ask - tick.bid
    average_spread_points = symbol_info.spread * symbol_info.point
    
    if current_spread_points > (average_spread_points * MAX_SPREAD_MULTIPLIER):
        print(f"SPREAD TERLALU LEBAR: Current={current_spread_points/ symbol_info.point:.1f}, Avg={average_spread_points/ symbol_info.point:.1f}. Trade dibatalkan.")
        return False
        
    return True

def check_all_safeguards(state, account_info):
    if account_info:
        peak_balance = max(account_info.balance, state.initial_balance)
        current_drawdown = (peak_balance - account_info.balance) / peak_balance * 100
        if current_drawdown >= MAX_DRAWDOWN_PERCENT:
            print(f"STOP TOTAL: Max Drawdown tercapai ({current_drawdown:.2f}% >= {MAX_DRAWDOWN_PERCENT}%)")
            return False

    if (state.daily_pnl / state.initial_balance * 100) <= -MAX_DAILY_LOSS_PERCENT:
        print(f"STOP HARI INI: Max Daily Loss tercapai ({state.daily_pnl:.2f})")
        return False

    if state.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
        print(f"STOP HARI INI: Max Consecutive Losses tercapai ({state.consecutive_losses})")
        return False

    if state.trades_today >= MAX_TRADES_PER_DAY:
        print(f"STOP HARI INI: Max Trades per Day tercapai ({state.trades_today})")
        return False

    if not is_spread_normal():
        return False

    return True

# --- PERUBAHAN: FUNGSI PREDIKSI DENGAN FILTER KEPERCAYAAN ---
def predict_signal(models, feature_columns):
    df = get_candles(SYMBOL, TIMEFRAME, 100)
    if df is None or len(df) < 50:
        return None
        
    df_features = add_features(df)
    latest_features = df_features[feature_columns].iloc[-1:].values

    buy_model, sell_model = models
    
    # Gunakan predict_proba untuk mendapatkan probabilitas
    buy_proba = buy_model.predict_proba(latest_features)[0]
    sell_proba = sell_model.predict_proba(latest_features)[0]
    
    # Probabilitas untuk kelas '1' (sinyal) ada di index ke-1
    buy_confidence = buy_proba[1]
    sell_confidence = sell_proba[1]
    
    print(f"Kepercayaan Model: BUY={buy_confidence:.2%}, SELL={sell_confidence:.2%}")

    if buy_confidence >= MODEL_CONFIDENCE_THRESHOLD:
        print(f"Sinyal BUY terdeteksi dan melewati threshold ({MODEL_CONFIDENCE_THRESHOLD:.2%})")
        return 'BUY'
    if sell_confidence >= MODEL_CONFIDENCE_THRESHOLD:
        print(f"Sinyal SELL terdeteksi dan melewati threshold ({MODEL_CONFIDENCE_THRESHOLD:.2%})")
        return 'SELL'
        
    print(f"Tidak ada sinyal yang melewati threshold kepercayaan.")
    return None

# --- FUNGSI UTAMA ---
def main():
    if not connect_mt5():
        return

    try:
        buy_model = joblib.load(MODEL_BUY_FILE)
        sell_model = joblib.load(MODEL_SELL_FILE)
        print("Model berhasil dimuat.")
    except FileNotFoundError:
        print(f"ERROR: File model tidak ditemukan. Jalankan Fase 2 terlebih dahulu.")
        mt5.shutdown()
        return

    feature_columns = buy_model.feature_names_in_
    state = DailyState()
    
    try:
        while True:
            now_wib = datetime.now(pytz.timezone("Asia/Jakarta"))
            print(f"\n--- Cek Pukul {now_wib.strftime('%H:%M:%S')} WIB ---")

            if state.is_new_day():
                print("Hari baru, mereset state harian.")
                state.reset()

            if now_wib.time() >= MIDNIGHT_CLOSE_TIME and now_wib.time() < time(0, 1, 0):
                print("Sekarang pukul 00:00 WIB. Menutup semua posisi...")
                close_all_positions()
                time.sleep(60)
                continue

            # Fungsi is_trading_time sekarang sudah mencakup filter sesi
            if not is_trading_time():
                time.sleep(60)
                continue

            if get_open_positions():
                print("Ada posisi terbuka. Menunggu...")
                time.sleep(60)
                continue

            account_info = get_account_info()
            if not check_all_safeguards(state, account_info):
                time.sleep(60)
                continue

            print("Aman untuk trading. Melakukan prediksi...")
            signal = predict_signal((buy_model, sell_model), feature_columns)
            
            if signal:
                print(f"EKSEKUSI SIGNAL: {signal}")
                tick = mt5.symbol_info_tick(SYMBOL)
                if not tick: continue
                
                current_price = tick.ask if signal == 'BUY' else tick.bid
                atr = get_candles(SYMBOL, TIMEFRAME, ATR_PERIOD + 2)[f'ATRr_{ATR_PERIOD}'].iloc[-1]
                
                if signal == 'BUY':
                    sl_price = current_price - (RISK_MULTIPLIER * atr)
                    tp_price = current_price + (REWARD_MULTIPLIER * atr)
                else: # SELL
                    sl_price = current_price + (RISK_MULTIPLIER * atr)
                    tp_price = current_price - (REWARD_MULTIPLIER * atr)
                
                place_order(signal, sl_price, tp_price)
            
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nBot dihentikan oleh pengguna.")
    finally:
        mt5.shutdown()
        print("Koneksi ke MetaTrader 5 ditutup.")

if __name__ == "__main__":
    main()