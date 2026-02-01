import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import warnings

warnings.filterwarnings('ignore')

# --- KONFIGURASI ---
DATA_FILE = "EURUSD_16385_data.csv" # File yang dihasilkan dari Fase 1
MODEL_BUY_FILE = "model_buy.pkl"
MODEL_SELL_FILE = "model_sell.pkl"

# --- FUNGSI-FUNGSI UTAMA ---

def load_and_prepare_data(filepath):
    """Memuat data dan memisahkan fitur serta target."""
    print(f"Memuat data dari '{filepath}'...")
    df = pd.read_csv(filepath, index_col='time', parse_dates=True)
    
    # Pilih kolom yang akan digunakan sebagai fitur
    # Kita tidak menggunakan kolom OHLCV asli, hanya indikatornya
    feature_columns = [
        'RSI_14', 'STOCHk_14_3_3', 'STOCHd_14_3_3',
        'SMA_20', 'SMA_50', 'EMA_100',
        'ATRr_14', 'BBL_20_2.0_2.0', 'BBM_20_2.0_2.0', 'BBU_20_2.0_2.0', 'BBB_20_2.0_2.0', 'BBP_20_2.0_2.0',
        'ADX_14'
    ]
    
    # Pastikan semua kolom fitur ada di DataFrame
    for col in feature_columns:
        if col not in df.columns:
            raise ValueError(f"Kolom fitur '{col}' tidak ditemukan di data. Pastikan Fase 1 berjalan dengan benar.")
            
    X = df[feature_columns]
    
    # Target kita adalah label yang sudah dibuat
    y_buy = df['buy_signal']
    y_sell = df['sell_signal']
    
    print("Data berhasil dimuat dan dipisahkan.")
    return X, y_buy, y_sell, feature_columns

def train_and_evaluate_model(X, y, model_name="Model"):
    """Melatih, mengevaluasi, dan mengembalikan model yang sudah dilatih."""
    print(f"\n--- Melatih {model_name} ---")
    
    # Cek distribusi label
    print("Distribusi label:")
    print(y.value_counts(normalize=True))
    
    # Bagi data menjadi data latih (80%) dan data uji (20%)
    # Stratify=y memastikan proporsi label 0 dan 1 sama di data latih dan uji
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Inisialisasi model Random Forest
    # n_estimators: jumlah pohon di hutan
    # random_state: untuk hasil yang konsisten
    # class_weight='balanced': membantu menangani ketidakseimbangan data (sinyal 1 jauh lebih sedikit)
    model = RandomForestClassifier(
        n_estimators=100, 
        random_state=42, 
        class_weight='balanced',
        n_jobs=-1 # Gunakan semua CPU core
    )
    
    print("Melatih model... (ini mungkin memakan waktu beberapa menit)")
    model.fit(X_train, y_train)
    print("Pelatihan selesai.")
    
    # Evaluasi model dengan data uji
    print("\n--- Evaluasi Performa Model ---")
    y_pred = model.predict(X_test)
    
    print(f"Laporan Klasifikasi untuk {model_name}:")
    print(classification_report(y_test, y_pred))
    
    # Tampilkan feature importance (fitur mana yang paling penting)
    feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\n10 Fitur Paling Penting:")
    print(feature_importances.head(10))
    
    return model

def save_model(model, filename):
    """Menyimpan model yang sudah dilatih ke file."""
    joblib.dump(model, filename)
    print(f"\nModel berhasil disimpan ke '{filename}'")

# --- EKSEKUSI UTAMA ---
if __name__ == "__main__":
    try:
        # 1. Muat dan siapkan data
        X, y_buy, y_sell, features = load_and_prepare_data(DATA_FILE)
        
        # 2. Latih model untuk sinyal BUY
        buy_model = train_and_evaluate_model(X, y_buy, model_name="Model Sinyal BUY")
        
        # 3. Latih model untuk sinyal SELL
        sell_model = train_and_evaluate_model(X, y_sell, model_name="Model Sinyal SELL")
        
        # 4. Simpan model yang sudah dilatih
        save_model(buy_model, MODEL_BUY_FILE)
        save_model(sell_model, MODEL_SELL_FILE)
        
        print("\n--- Fase 2 Selesai ---")
        print("Model BUY dan SELL telah dilatih dan disimpan.")
        print("Anda sekarang siap untuk Fase 3: Integrasi ke Bot Trading.")
        
    except FileNotFoundError:
        print(f"\nERROR: File '{DATA_FILE}' tidak ditemukan.")
        print("Pastikan Anda sudah menjalankan skrip '1_data_preparation.py' terlebih dahulu.")
    except ValueError as e:
        print(f"\nERROR: {e}")
        print("Pastikan data yang dihasilkan Fase 1 lengkap dan tidak ada masalah.")
    except Exception as e:
        print(f"\nTerjadi error tidak terduga: {e}")
