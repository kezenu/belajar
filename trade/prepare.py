import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime
import pandas_ta as ta
import warnings

# Matikan peringatan agar output lebih bersih
warnings.filterwarnings('ignore')

# --- KONFIGURASI DATA ---
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_H1  # Timeframe H1 sering digunakan untuk analisis semacam ini
NUM_CANDLES = 5000  # Ambil 5000 candle untuk data latih yang cukup

# --- KONFIGURASI LABEL (TARGET) ---
# Kita gunakan ATR untuk menentukan risiko secara dinamis
ATR_PERIOD = 14
RISK_MULTIPLIER = 1.5  # SL = 1.5 * ATR
REWARD_MULTIPLIER = 3.0 # TP = 3.0 * ATR (untuk RR 1:2)
LOOK_FORWARD_WINDOW = 20 # Cek 20 candle ke depan untuk melihat apakah TP/SL tercapai

def get_historical_data(symbol, timeframe, num_candles):
    """Mengambil data historis dari MT5 dan mengembalikan DataFrame."""
    print("Menghubungkan ke MetaTrader 5...")
    if not mt5.initialize():
        print("Gagal menghubungkan MT5, error:", mt5.last_error())
        return None

    # Ambil data dari tanggal yang paling lama ke sekarang
    candles = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    mt5.shutdown()
    
    if candles is None:
        print("Gagal mengambil data candle, error:", mt5.last_error())
        return None
        
    # Konversi ke DataFrame
    df = pd.DataFrame(candles)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    
    print(f"Berhasil mengambil {len(df)} candle untuk {symbol}.")
    return df

def add_features(df):
    """Menambahkan indikator teknis sebagai fitur ke DataFrame."""
    print("Menambahkan fitur (indikator teknis)...")
    
    # Momentum Indicators
    df.ta.rsi(length=14, append=True)
    df.ta.stoch(k=14, d=3, append=True)
    
    # Trend Indicators
    df.ta.sma(length=20, append=True)
    df.ta.sma(length=50, append=True)
    df.ta.ema(length=100, append=True)
    
    # Volatility Indicators
    df.ta.atr(length=ATR_PERIOD, append=True)
    df.ta.bbands(length=20, std=2, append=True)
    
    # Volume Indicators (jika ada)
    df.ta.adx(length=14, append=True)
    
    # Hapus baris dengan NaN yang dihasilkan oleh perhitungan indikator di awal
    df.dropna(inplace=True)
    
    print(f"Fitur berhasil ditambahkan. Total fitur: {len(df.columns)}")
    return df

def create_labels(df):
    """Membuat label target (buy_signal, sell_signal) berdasarkan RR 1:2 di masa depan."""
    print("Membuat label target...")
    
    # Inisialisasi kolom label dengan 0
    df['buy_signal'] = 0
    df['sell_signal'] = 0
    
    # Iterasi melalui setiap candle untuk membuat label
    # Kita mulai dari awal dan berhenti sebelum akhir agar ada 'masa depan' yang diperiksa
    for i in range(len(df) - LOOK_FORWARD_WINDOW):
        
        # --- Data untuk candle saat ini (i) ---
        current_close = df['close'].iloc[i]
        current_atr = df[f'ATRr_{ATR_PERIOD}'].iloc[i] # pandas-ta menggunakan ATRr (percent)
        
        # Jika ATR adalah 0, lewati untuk menghindari pembagian dengan nol
        if current_atr == 0:
            continue
            
        # --- Hitung level TP dan SL untuk BUY ---
        buy_sl = current_close - (RISK_MULTIPLIER * current_atr)
        buy_tp = current_close + (REWARD_MULTIPLIER * current_atr)
        
        # --- Hitung level TP dan SL untuk SELL ---
        sell_sl = current_close + (RISK_MULTIPLIER * current_atr)
        sell_tp = current_close - (REWARD_MULTIPLIER * current_atr)
        
        # --- Lihat ke masa depan ---
        future_df = df.iloc[i+1 : i+1+LOOK_FORWARD_WINDOW]
        
        # --- Logika untuk BUY SIGNAL ---
        # Cari candle pertama di masa depan yang menyentuh TP atau SL
        buy_tp_hit_index = future_df[future_df['high'] >= buy_tp].first_valid_index()
        buy_sl_hit_index = future_df[future_df['low'] <= buy_sl].first_valid_index()
        
        # Jika TP tercapai dan (SL tidak tercapai ATAU TP tercapai lebih dulu)
        if buy_tp_hit_index is not None and (buy_sl_hit_index is None or buy_tp_hit_index < buy_sl_hit_index):
            df.loc[df.index[i], 'buy_signal'] = 1
            
        # --- Logika untuk SELL SIGNAL ---
        sell_tp_hit_index = future_df[future_df['low'] <= sell_tp].first_valid_index()
        sell_sl_hit_index = future_df[future_df['high'] >= sell_sl].first_valid_index()
        
        # Jika TP tercapai dan (SL tidak tercapai ATAU TP tercapai lebih dulu)
        if sell_tp_hit_index is not None and (sell_sl_hit_index is None or sell_tp_hit_index < sell_sl_hit_index):
            df.loc[df.index[i], 'sell_signal'] = 1
            
    print("Label berhasil dibuat.")
    return df

# --- EKSEKUSI UTAMA ---
if __name__ == "__main__":
    # 1. Ambil data historis
    data = get_historical_data(SYMBOL, TIMEFRAME, NUM_CANDLES)
    
    if data is not None:
        # 2. Tambahkan fitur
        data_with_features = add_features(data)
        
        # 3. Buat label
        final_data = create_labels(data_with_features)
        
        # 4. Simpan ke file CSV
        output_filename = f"{SYMBOL}_{TIMEFRAME}_data.csv"
        final_data.to_csv(output_filename)
        
        print("\n--- Proses Selesai ---")
        print(f"Data final telah disimpan ke '{output_filename}'")
        
        # Tampilkan sampel hasil
        print("\n5 baris pertama data:")
        print(final_data.head())
        
        print("\n5 baris terakhir data:")
        print(final_data.tail())
        
        # Tampilkan statistik label
        print("\nStatistik Label:")
        print("Buy Signal (1 vs 0):")
        print(final_data['buy_signal'].value_counts(normalize=True))
        print("\nSell Signal (1 vs 0):")
        print(final_data['sell_signal'].value_counts(normalize=True))
