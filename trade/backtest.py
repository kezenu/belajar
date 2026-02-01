import pandas as pd
import numpy as np
import joblib
from datetime import time
import pytz
import warnings

warnings.filterwarnings('ignore')

# --- KONFIGURASI (HARUS SAMA DENGAN BOT UTAMA) ---
DATA_FILE = "EURUSD_16385_data.csv" # Gunakan file data yang sama
MODEL_BUY_FILE = "model_buy.pkl"
MODEL_SELL_FILE = "model_sell.pkl"

# Filter Waktu
TRADING_SESSION_START_TIME = time(13, 0, 0) # WIB
TRADING_SESSION_END_TIME = time(22, 0, 0)   # WIB

# Filter Model
MODEL_CONFIDENCE_THRESHOLD = 0.70

# Batasan Harian
MAX_TRADES_PER_DAY = 3

# --- FUNGSI-FUNGSI PENDUKUNG ---

def load_data_and_models():
    """Memuat data dan model yang sudah dilatih."""
    try:
        df = pd.read_csv(DATA_FILE, index_col='time', parse_dates=True)
        # Konversi waktu ke WIB karena data dari MT5 biasanya UTC
        df.index = df.index.tz_localize('UTC').tz_convert('Asia/Jakarta')
        print(f"Data '{DATA_FILE}' berhasil dimuat. Zona waktu diubah ke WIB.")
        
        buy_model = joblib.load(MODEL_BUY_FILE)
        sell_model = joblib.load(MODEL_SELL_FILE)
        print("Model BUY dan SELL berhasil dimuat.")
        
        return df, buy_model, sell_model
    except FileNotFoundError as e:
        print(f"ERROR: File tidak ditemukan - {e}")
        return None, None, None

def is_trading_session(current_time):
    """Memeriksa apakah waktu saat ini ada di sesi trading."""
    return TRADING_SESSION_START_TIME <= current_time.time() <= TRADING_SESSION_END_TIME

def predict_signal(models, feature_columns, current_features):
    """Memprediksi sinyal berdasarkan probabilitas."""
    buy_model, sell_model = models
    
    # Ubah features menjadi DataFrame untuk menjaga nama kolom
    features_df = pd.DataFrame([current_features], columns=feature_columns)
    
    buy_proba = buy_model.predict_proba(features_df)[0]
    sell_proba = sell_model.predict_proba(features_df)[0]
    
    buy_confidence = buy_proba[1]
    sell_confidence = sell_proba[1]
    
    if buy_confidence >= MODEL_CONFIDENCE_THRESHOLD:
        return 'BUY', buy_confidence
    if sell_confidence >= MODEL_CONFIDENCE_THRESHOLD:
        return 'SELL', sell_confidence
        
    return None, 0.0

# --- EKSEKUSI BACKTEST FREKUENSI ---
def main():
    df, buy_model, sell_model = load_data_and_models()
    if df is None:
        return

    feature_columns = buy_model.feature_names_in_
    
    # State untuk simulasi
    total_trades = 0
    daily_trade_counts = []
    current_date = None
    trades_today = 0
    
    print("\n--- Memulai Backtest Frekuensi ---")
    print(f"Periode Data: {df.index.min().date()} hingga {df.index.max().date()}")
    
    # Iterasi melalui setiap candle di data historis
    for timestamp, row in df.iterrows():
        
        # Reset counter setiap hari
        if current_date != timestamp.date():
            if trades_today > 0:
                daily_trade_counts.append(trades_today)
            current_date = timestamp.date()
            trades_today = 0
        
        # Cek semua filter sebelum memprediksi
        if not is_trading_session(timestamp):
            continue
        if trades_today >= MAX_TRADES_PER_DAY:
            continue
            
        # Ambil fitur untuk candle saat ini
        current_features = row[feature_columns].values
        
        # Prediksi sinyal
        signal, confidence = predict_signal((buy_model, sell_model), feature_columns, current_features)
        
        if signal:
            total_trades += 1
            trades_today += 1
            print(f"Sinyal {signal} ditemukan pada {timestamp.strftime('%Y-%m-%d %H:%M')} dengan kepercayaan {confidence:.2%}")

    # Tambahkan trade count dari hari terakhir
    if trades_today > 0:
        daily_trade_counts.append(trades_today)
        
    # --- Tampilkan Hasil ---
    print("\n--- Hasil Backtest Frekuensi ---")
    print(f"Total sinyal yang ditemukan: {total_trades}")
    
    if not daily_trade_counts:
        print("Tidak ada hari dengan sinyal trading.")
        return
        
    avg_trades_per_day = np.mean(daily_trade_counts)
    avg_trades_per_week = avg_trades_per_day * 5 # Asumsi trading 5 hari seminggu
    
    print(f"Jumlah hari trading (dimana ada sinyal): {len(daily_trade_counts)} hari")
    print(f"Rata-rata trade per hari (hanya pada hari ada sinyal): {avg_trades_per_day:.2f}")
    print(f"Estimasi rata-rata trade per minggu: {avg_trades_per_week:.2f}")
    
    print("\nDistribusi trade per hari:")
    print(pd.Series(daily_trade_counts).describe())


if __name__ == "__main__":
    main()