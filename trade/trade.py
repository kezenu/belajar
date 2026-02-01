# ===============================
# PRODUCTION-GRADE ML TRADING BOT (FIXED VERSION)
# ===============================

import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import numpy as np
import joblib
from datetime import datetime, time, timedelta
import pytz
import warnings
import time as dt
import os
import logging

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- KONFIGURASI ---
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_H1
MAGIC_NUMBER = 12345
TIMEZONE = pytz.timezone("Asia/Jakarta")

# Manajemen Risiko
RISK_PERCENT = 2.0
MIN_LOT = 0.01
ATR_PERIOD = 14
RISK_MULTIPLIER = 1.5
REWARD_MULTIPLIER = 1.0
LOSS_COOLDOWN_MINUTES = 30

# Filter & Batasan
TRADING_SESSION_START = time(13, 0)
TRADING_SESSION_END = time(22, 0)
MIDNIGHT_CLOSE = time(0, 0, 10)
MODEL_CONFIDENCE_THRESHOLD = 0.70
MAX_TRADES_PER_DAY = 3
MAX_DAILY_LOSS_PERCENT = 5.0
MAX_CONSECUTIVE_LOSSES = 3
MAX_DRAWDOWN_PERCENT = 15.0
MAX_SPREAD_MULTIPLIER = 3.0

# File
MODEL_BUY_FILE = "model_buy.pkl"
MODEL_SELL_FILE = "model_sell.pkl"
JOURNAL_FILE = "trade_journal.csv"
STATE_FILE = "bot_state.json"

# --- STATE MANAGEMENT ---
class DailyState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.date = datetime.now(TIMEZONE).date()
        self.trades_today = 0
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.last_loss_time = None
        acc = mt5.account_info()
        self.initial_balance = acc.balance if acc else 0.0
        self.peak_balance = self._load_peak_balance()

    def _load_peak_balance(self):
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r') as f:
                    import json
                    data = json.load(f)
                    return max(data.get('peak_balance', self.initial_balance), self.initial_balance)
        except Exception as e:
            logging.warning(f"Gagal memuat state dari file: {e}")
        return self.initial_balance

    def _save_peak_balance(self):
        try:
            with open(STATE_FILE, 'w') as f:
                import json
                json.dump({'peak_balance': self.peak_balance}, f)
        except Exception as e:
            logging.error(f"Gagal menyimpan state ke file: {e}")

    def update(self, pnl):
        self.daily_pnl += pnl
        self.trades_today += 1
        if pnl < 0:
            self.consecutive_losses += 1
            self.last_loss_time = datetime.now(TIMEZONE)
        else:
            self.consecutive_losses = 0
        
        current_balance = self._get_current_balance()
        if current_balance > self.peak_balance:
            self.peak_balance = current_balance
            self._save_peak_balance()

    def _get_current_balance(self):
        acc = mt5.account_info()
        return acc.balance if acc else 0.0

    def cooldown_active(self):
        if not self.last_loss_time:
            return False
        return datetime.now(TIMEZONE) < self.last_loss_time + timedelta(minutes=LOSS_COOLDOWN_MINUTES)

# --- JOURNALING ---
def init_journal():
    if not os.path.exists(JOURNAL_FILE):
        pd.DataFrame(columns=[
            'open_time', 'action', 'lot_size', 'entry_price', 'sl_price', 'tp_price',
            'close_time', 'exit_price', 'pnl', 'exit_reason'
        ]).to_csv(JOURNAL_FILE, index=False)

def log_trade(trade_data: dict):
    try:
        df_new = pd.DataFrame([trade_data])
        df_new.to_csv(JOURNAL_FILE, mode='a', header=False, index=False)
    except Exception as e:
        logging.error(f"Gagal menulis ke journal: {e}")

# --- MT5 HELPERS ---
def connect_mt5():
    if not mt5.initialize():
        logging.error(f"Gagal menghubungkan MT5, error: {mt5.last_error()}")
        return False
    logging.info("Berhasil terhubung ke MetaTrader 5")
    return True

def get_candles(n=200):
    rates = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 0, n)
    if rates is None:
        logging.error(f"Gagal mendapatkan candle: {mt5.last_error()}")
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

def add_features(df):
    df.ta.rsi(14, append=True)
    df.ta.sma(20, append=True)
    df.ta.sma(50, append=True)
    df.ta.ema(100, append=True)
    df.ta.atr(ATR_PERIOD, append=True)
    df.ta.adx(14, append=True)
    # Nama kolom ATR dari pandas_ta adalah 'ATRr_14'
    return df.dropna()

# --- RISK ENGINE ---
def calculate_lot(entry, sl):
    acc = mt5.account_info()
    sym = mt5.symbol_info(SYMBOL)
    if not acc or not sym: return MIN_LOT
    if acc.balance < 0: return MIN_LOT
    
    risk_amt = acc.balance * (RISK_PERCENT / 100)
    sl_points = abs(entry - sl) / sym.point
    if sl_points == 0: return MIN_LOT

    lot = risk_amt / (sl_points * sym.trade_tick_value)
    lot = round(lot / sym.volume_step) * sym.volume_step
    lot = max(sym.volume_min, min(lot, sym.volume_max))
    
    if acc.margin_free < (lot * sym.margin_initial):
        logging.warning("Margin tidak cukup. Menggunakan lot minimum.")
        return MIN_LOT
    return lot

def spread_ok():
    sym = mt5.symbol_info(SYMBOL)
    tick = mt5.symbol_info_tick(SYMBOL)
    if not sym or not tick: return False
    
    spread_points = (tick.ask - tick.bid) / sym.point
    avg_spread_points = sym.spread
    return spread_points <= avg_spread_points * MAX_SPREAD_MULTIPLIER

# --- SIGNAL & EXECUTION ---
def predict_signal(buy_model, sell_model, feature_cols):
    df_features = add_features(get_candles())
    if df_features is None or len(df_features) < 50: return None
    
    x = df_features[feature_cols].iloc[-1:].values
    buy_p = buy_model.predict_proba(x)[0][1]
    sell_p = sell_model.predict_proba(x)[0][1]
    
    print(f"CONF → BUY {buy_p:.2%} | SELL {sell_p:.2%}")

    if buy_p >= MODEL_CONFIDENCE_THRESHOLD: return "BUY"
    if sell_p >= MODEL_CONFIDENCE_THRESHOLD: return "SELL"
    return None

def place_order(signal, atr):
    tick = mt5.symbol_info_tick(SYMBOL)
    sym = mt5.symbol_info(SYMBOL)
    if not tick or not sym: return None

    price = tick.ask if signal == "BUY" else tick.bid
    sl = price - atr * RISK_MULTIPLIER if signal == "BUY" else price + atr * RISK_MULTIPLIER
    tp = price + atr * REWARD_MULTIPLIER if signal == "BUY" else price - atr * REWARD_MULTIPLIER

    lot = calculate_lot(price, sl)
    if lot is None: return None

    request = {
        'action': mt5.TRADE_ACTION_DEAL, 'symbol': SYMBOL, 'volume': lot,
        'type': mt5.ORDER_TYPE_BUY if signal == "BUY" else mt5.ORDER_TYPE_SELL,
        'price': price, 'sl': sl, 'tp': tp, 'deviation': 10,
        'magic': MAGIC_NUMBER, 'comment': 'ML Bot',
        'type_filling': sym.filling_mode,
    }
    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        logging.info(f"Order {signal} {lot:.2f} {SYMBOL} berhasil @ {price:.5f}")
        return result.order
    else:
        logging.error(f"Order gagal: {result.comment}")
        return None

# --- MONITORING & STATE UPDATE (FIXED) ---
def monitor_and_close_positions(state):
    """Monitor posisi, update state, dan tutup jika perlu."""
    open_positions = mt5.positions_get(symbol=SYMBOL, magic=MAGIC_NUMBER)
    if not open_positions:
        return

    # Untuk sementara, asumsikan hanya satu posisi terbuka
    pos = open_positions[0]
    current_tick = mt5.symbol_info_tick(SYMBOL)
    if not current_tick: return

    current_price = current_tick.bid if pos.type == mt5.POSITION_TYPE_BUY else current_tick.ask
    pnl = 0
    exit_reason = ""

    if pos.type == mt5.POSITION_TYPE_BUY:
        pnl = (current_price - pos.price_open) / mt5.symbol_info(SYMBOL).point
        if current_price <= pos.sl or current_price >= pos.tp:
            exit_reason = "SL" if current_price <= pos.sl else "TP"
    else:
        pnl = (pos.price_open - current_price) / mt5.symbol_info(SYMBOL).point
        if current_price >= pos.sl or current_price <= pos.tp:
            exit_reason = "SL" if current_price >= pos.sl else "TP"

    now = datetime.now(TIMEZONE)
    if not exit_reason and now.time() >= MIDNIGHT_CLOSE.time():
        exit_reason = "MIDNIGHT CLOSE"
    
    if exit_reason:
        # Tutup posisi
        close_req = {
            'action': mt5.TRADE_ACTION_DEAL, 'symbol': pos.symbol,
            'position': pos.ticket, 'volume': pos.volume,
            'type': mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            'price': current_price, 'deviation': 10, 'magic': MAGIC_NUMBER,
            'comment': f'Bot close ({exit_reason})', 'type_filling': mt5.symbol_info(SYMBOL).filling_mode
        }
        mt5.order_send(close_req)
        logging.info(f"Posisi {pos.ticket} ditutup. Alasan: {exit_reason}. PnL: {pnl:.2f}")
        
        # PERBAIKAN: Update state yang dilewatkan sebagai argumen
        state.update(pnl)
        logging.info(f"Daily PnL updated: {state.daily_pnl:.2f}")


# --- MAIN LOOP (FIXED) ---
def main():
    if not connect_mt5(): return

    init_journal()
    buy_model = joblib.load(MODEL_BUY_FILE)
    sell_model = joblib.load(MODEL_SELL_FILE)
    feature_cols = buy_model.feature_names_in_
    
    # PERBAIKAN 1: Hanya ada SATU state object yang digunakan di seluruh bot
    state = DailyState()

    while True:
        now = datetime.now(TIMEZONE)
        if now.date() != state.date:
            state.reset()

        # PERBAIKAN 2: Monitor dipanggil di SETIAP awal loop, tanpa syarat
        monitor_and_close_positions(state)

        if state.cooldown_active():
            dt.sleep(60); continue

        if not (TRADING_SESSION_START <= now.time() <= TRADING_SESSION_END):
            dt.sleep(60); continue

        # PERBAIKAN 2: Cek posisi terbuka SETELAH monitor
        if mt5.positions_get(symbol=SYMBOL, magic=MAGIC_NUMBER):
            dt.sleep(60); continue

        if not spread_ok():
            dt.sleep(60); continue

        signal = predict_signal(buy_model, sell_model, feature_cols)
        if not signal:
            dt.sleep(30); continue

        df_atr = add_features(get_candles())
        atr = df_atr[f'ATRr_{ATR_PERIOD}'].iloc[-1]
        place_order(signal, atr)
        
        dt.sleep(10)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Bot dihentikan oleh pengguna.")
    finally:
        mt5.shutdown()
        logging.info("Koneksi MT5 ditutup.")