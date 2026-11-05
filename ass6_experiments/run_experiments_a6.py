import os, sys, time, json
sys.stdout.reconfigure(encoding='utf-8')
os.environ['KERAS_BACKEND'] = 'torch'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

import keras
from keras import layers, models

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# -------------------------------------------------------------
# 1. THIẾT LẬP HỆ THỐNG VÀ THẨM MỸ ĐỒ HỌA
# -------------------------------------------------------------
SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['font.size'] = 9

os.makedirs('ass6_experiments/plots', exist_ok=True)
os.makedirs('ass6_experiments/artifacts', exist_ok=True)
os.makedirs('ass6_experiments/rendered_cells', exist_ok=True)

print("=== BẮT ĐẦU CHUỖI THỰC NGHIỆM ASSIGNMENT 06 (RNN TIME-SERIES) ===")

# -------------------------------------------------------------
# 2. LOAD VÀ TIỀN XỬ LÝ 2 BỘ DỮ LIỆU
# -------------------------------------------------------------
print("\n--- 2.1. Đọc và khám phá dữ liệu Cổ phiếu Amazon (AMZN) ---")
df_stock = pd.read_csv('data/assignment_06/amzn_stock.csv')
df_stock['Date'] = pd.to_datetime(df_stock['Date'])
df_stock.sort_values('Date', inplace=True)
df_stock.reset_index(drop=True, inplace=True)
print(f"AMZN Stock records: {len(df_stock)} từ {df_stock['Date'].min().strftime('%Y-%m-%d')} đến {df_stock['Date'].max().strftime('%Y-%m-%d')}")
print(df_stock[['Open', 'High', 'Low', 'Close', 'Volume']].describe().round(2))

print("\n--- 2.2. Đọc và khám phá dữ liệu Hành vi tiêu thụ năng lượng theo giờ ---")
df_energy = pd.read_csv('data/assignment_06/hourly_energy_consumption.csv')
df_energy['Datetime'] = pd.to_datetime(df_energy['Datetime'])
df_energy.sort_values('Datetime', inplace=True)
df_energy.drop_duplicates(subset=['Datetime'], inplace=True)
df_energy.reset_index(drop=True, inplace=True)

# Lấy 10,000 giờ gần nhất để đại diện cho hơn 1 năm hành vi liên tục (chu kỳ 24h, 7 ngày và 4 mùa)
df_energy_sub = df_energy.iloc[-10000:].copy().reset_index(drop=True)
print(f"Energy Hourly records (Full): {len(df_energy)}, Sub-sample phân tích & huấn luyện: {len(df_energy_sub)}")
print(df_energy_sub['PJME_MW'].describe().round(2))

# -------------------------------------------------------------
# 3. SINH CÁC BIỂU ĐỒ KHÁM PHÁ DỮ LIỆU (EDA)
# -------------------------------------------------------------
print("\n--- 3. Xuất các biểu đồ phân tích EDA ---")

# Hình EDA 1: Biến động giá cổ phiếu Amazon kèm đường trung bình MA30 & MA90
fig, ax = plt.subplots(figsize=(9.2, 4.2), dpi=150)
df_stock['MA30'] = df_stock['Close'].rolling(30).mean()
df_stock['MA90'] = df_stock['Close'].rolling(90).mean()
ax.plot(df_stock['Date'], df_stock['Close'], label='Giá đóng cửa thực tế (Close)', color='#2B6CB0', lw=1.2)
ax.plot(df_stock['Date'], df_stock['MA30'], label='Đường trung bình MA-30 ngày', color='#DD6B20', lw=1.2, linestyle='--')
ax.plot(df_stock['Date'], df_stock['MA90'], label='Đường trung bình MA-90 ngày', color='#38A169', lw=1.2, linestyle=':')
ax.set_title('BIẾN ĐỘNG GIÁ CỔ PHIẾU AMAZON (AMZN) QUA 5 NĂM (2021 - 2026)', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Thời gian', fontsize=8.5)
ax.set_ylabel('Giá cổ phiếu (USD)', fontsize=8.5)
ax.legend(fontsize=8)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_eda_01_amzn_price_trend.png', bbox_inches='tight')
plt.close()
print("[OK] Hình EDA 1: fig_eda_01_amzn_price_trend.png")

# Hình EDA 2: Phân phối lợi suất hàng ngày (Daily Returns) & Khối lượng giao dịch
fig, axes = plt.subplots(1, 2, figsize=(10, 4.0), dpi=150)
df_stock['Return'] = df_stock['Close'].pct_change()
sns.histplot(df_stock['Return'].dropna(), kde=True, ax=axes[0], color='#3182CE', bins=40)
axes[0].set_title('Phân phối Lợi suất Hàng ngày AMZN', fontsize=9.5, fontweight='bold')
axes[0].set_xlabel('Tỷ lệ thay đổi giá (Daily Return)', fontsize=8.5)
axes[0].set_ylabel('Tần suất (Count)', fontsize=8.5)
axes[0].grid(True, linestyle=':', alpha=0.6)

axes[1].plot(df_stock['Date'], df_stock['Volume'] / 1e6, color='#805AD5', lw=1.0)
axes[1].set_title('Khối lượng Giao dịch Hàng ngày (Triệu cổ phiếu)', fontsize=9.5, fontweight='bold')
axes[1].set_xlabel('Thời gian', fontsize=8.5)
axes[1].set_ylabel('Volume (Triệu)', fontsize=8.5)
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.suptitle('PHÂN PHỐI LỢI SUẤT VÀ KHỐI LƯỢNG GIAO DỊCH CỔ PHIẾU AMAZON', fontsize=10.5, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_eda_02_amzn_returns_volume.png', bbox_inches='tight')
plt.close()
print("[OK] Hình EDA 2: fig_eda_02_amzn_returns_volume.png")

# Hình EDA 3: Chuỗi thời gian tiêu thụ năng lượng theo giờ và chu kỳ 24h
fig, axes = plt.subplots(2, 1, figsize=(9.5, 5.2), dpi=150)
axes[0].plot(df_energy_sub['Datetime'], df_energy_sub['PJME_MW'], color='#2B6CB0', lw=0.8)
axes[0].set_title('Chuỗi thời gian Phụ tải Tiêu thụ Điện năng Hàng giờ (PJME_MW)', fontsize=9.5, fontweight='bold')
axes[0].set_ylabel('Công suất (MW)', fontsize=8.5)
axes[0].grid(True, linestyle=':', alpha=0.6)

# Trích xuất 1 tuần điển hình (168 giờ) để thấy rõ nhịp sinh học khách hàng
sample_week = df_energy_sub.iloc[-168:].copy()
axes[1].plot(sample_week['Datetime'], sample_week['PJME_MW'], marker='o', markersize=2.5, color='#DD6B20', lw=1.2)
axes[1].set_title('Hành vi Tiêu thụ Chi tiết trong 1 Tuần Điển hình (168 Giờ)', fontsize=9.5, fontweight='bold')
axes[1].set_xlabel('Thời gian (Giờ / Ngày)', fontsize=8.5)
axes[1].set_ylabel('Công suất (MW)', fontsize=8.5)
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.suptitle('PHÂN TÍCH CHU KỲ VÀ TÍNH MÙA VỤ CỦA DỮ LIỆU TIÊU THỤ THEO GIỜ', fontsize=10.5, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_eda_03_energy_cycles.png', bbox_inches='tight')
plt.close()
print("[OK] Hình EDA 3: fig_eda_03_energy_cycles.png")

# Hình EDA 4: Mức tiêu thụ trung bình theo giờ trong ngày & theo ngày trong tuần
fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.0), dpi=150)
df_energy_sub['Hour'] = df_energy_sub['Datetime'].dt.hour
df_energy_sub['DayOfWeek'] = df_energy_sub['Datetime'].dt.day_name()
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

hourly_mean = df_energy_sub.groupby('Hour')['PJME_MW'].mean()
axes[0].plot(hourly_mean.index, hourly_mean.values, marker='s', color='#38A169', lw=1.5)
axes[0].set_title('Hành vi Tiêu thụ Trung bình theo 24 Giờ trong Ngày', fontsize=9.5, fontweight='bold')
axes[0].set_xlabel('Giờ trong ngày (0 - 23h)', fontsize=8.5)
axes[0].set_ylabel('Công suất TB (MW)', fontsize=8.5)
axes[0].set_xticks(range(0, 24, 2))
axes[0].grid(True, linestyle=':', alpha=0.6)

daily_mean = df_energy_sub.groupby('DayOfWeek')['PJME_MW'].mean().reindex(days_order)
axes[1].bar(range(7), daily_mean.values, color='#4299E1', edgecolor='#1A365D', width=0.55)
axes[1].set_title('Mức Tiêu thụ Trung bình theo Ngày trong Tuần', fontsize=9.5, fontweight='bold')
axes[1].set_xticks(range(7))
axes[1].set_xticklabels(['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN'], fontsize=8.5)
axes[1].set_ylabel('Công suất TB (MW)', fontsize=8.5)
axes[1].set_ylim(daily_mean.min() * 0.9, daily_mean.max() * 1.05)
axes[1].grid(axis='y', linestyle=':', alpha=0.6)

plt.suptitle('ĐẶC TÍNH HÀNH VI KHÁCH HÀNG THEO GIỜ VÀ THEO NGÀY TRONG TUẦN', fontsize=10.5, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_eda_04_energy_hourly_daily_patterns.png', bbox_inches='tight')
plt.close()
print("[OK] Hình EDA 4: fig_eda_04_energy_hourly_daily_patterns.png")

# -------------------------------------------------------------
# 4. CHUẨN BỊ CHUỖI TRƯỢT THỜI GIAN (SLIDING WINDOW DATASET)
# -------------------------------------------------------------
def create_sliding_windows(data_series, window_size=30):
    X, y = [], []
    for i in range(len(data_series) - window_size):
        X.append(data_series[i : i + window_size])
        y.append(data_series[i + window_size])
    return np.array(X), np.array(y)

# 4.1. Chuẩn bị dữ liệu Cổ phiếu AMZN
scaler_stock = MinMaxScaler(feature_range=(0, 1))
stock_prices = df_stock['Close'].values.reshape(-1, 1)
stock_scaled = scaler_stock.fit_transform(stock_prices)

WINDOW_STOCK = 30 # Dùng 30 ngày giao dịch trước để dự đoán ngày tiếp theo
X_stock, y_stock = create_sliding_windows(stock_scaled, WINDOW_STOCK)

# Time-series split: 80% Train, 10% Val, 10% Test
n_stock = len(X_stock)
train_end_s = int(n_stock * 0.8)
val_end_s = int(n_stock * 0.9)

X_train_s, y_train_s = X_stock[:train_end_s], y_stock[:train_end_s]
X_val_s, y_val_s     = X_stock[train_end_s:val_end_s], y_stock[train_end_s:val_end_s]
X_test_s, y_test_s   = X_stock[val_end_s:], y_stock[val_end_s:]
print(f"\nAMZN Sliding Windows (Lookback={WINDOW_STOCK}): Train={len(X_train_s)}, Val={len(X_val_s)}, Test={len(X_test_s)}")

# 4.2. Chuẩn bị dữ liệu Tiêu thụ Năng lượng
scaler_energy = MinMaxScaler(feature_range=(0, 1))
energy_vals = df_energy_sub['PJME_MW'].values.reshape(-1, 1)
energy_scaled = scaler_energy.fit_transform(energy_vals)

WINDOW_ENERGY = 48 # Dùng 48 giờ (2 ngày) trước để dự đoán giờ tiếp theo
X_energy, y_energy = create_sliding_windows(energy_scaled, WINDOW_ENERGY)

n_energy = len(X_energy)
train_end_e = int(n_energy * 0.8)
val_end_e = int(n_energy * 0.9)

X_train_e, y_train_e = X_energy[:train_end_e], y_energy[:train_end_e]
X_val_e, y_val_e     = X_energy[train_end_e:val_end_e], y_energy[train_end_e:val_end_e]
X_test_e, y_test_e   = X_energy[val_end_e:], y_energy[val_end_e:]
print(f"Energy Sliding Windows (Lookback={WINDOW_ENERGY}): Train={len(X_train_e)}, Val={len(X_val_e)}, Test={len(X_test_e)}")

# -------------------------------------------------------------
# 5. ĐỊNH NGHĨA VÀ HUẤN LUYỆN MÔ HÌNH BẰNG PYTORCH
# -------------------------------------------------------------
print("\n=== [GIAI ĐOẠN 1: THỬ NGHIỆM PYTORCH (RNN, LSTM, GRU)] ===")

class PyTorchRNNModel(nn.Module):
    def __init__(self, mode='rnn', input_size=1, hidden_size=64, num_layers=2):
        super().__init__()
        self.mode = mode.lower()
        if self.mode == 'rnn':
            self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        elif self.mode == 'lstm':
            self.rnn = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        elif self.mode == 'gru':
            self.rnn = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        
    def forward(self, x):
        out, _ = self.rnn(x)
        # Lấy hidden state ở bước thời gian cuối cùng
        last_out = out[:, -1, :]
        return self.fc(last_out)

def train_eval_pytorch(model, X_tr, y_tr, X_va, y_va, X_te, y_te, scaler, epochs=20, lr=0.001, batch_size=32):
    train_loader = DataLoader(TensorDataset(torch.tensor(X_tr, dtype=torch.float32), torch.tensor(y_tr, dtype=torch.float32)), batch_size=batch_size, shuffle=False)
    val_loader = DataLoader(TensorDataset(torch.tensor(X_va, dtype=torch.float32), torch.tensor(y_va, dtype=torch.float32)), batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(TensorDataset(torch.tensor(X_te, dtype=torch.float32), torch.tensor(y_te, dtype=torch.float32)), batch_size=batch_size, shuffle=False)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    best_val_loss = float('inf')
    best_weights = None
    history = {'train_loss': [], 'val_loss': []}
    
    t0 = time.time()
    for ep in range(epochs):
        model.train()
        t_loss = 0.0
        for x, y in train_loader:
            optimizer.zero_grad()
            pred = model(x)
            loss = criterion(pred, y)
            loss.backward()
            optimizer.step()
            t_loss += loss.item() * len(y)
        train_loss = t_loss / len(X_tr)
        
        model.eval()
        v_loss = 0.0
        with torch.no_grad():
            for x, y in val_loader:
                pred = model(x)
                loss = criterion(pred, y)
                v_loss += loss.item() * len(y)
        val_loss = v_loss / len(X_va)
        
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_weights = model.state_dict().copy()
            
    train_time = time.time() - t0
    model.load_state_dict(best_weights)
    
    # Đánh giá trên test set
    model.eval()
    y_preds = []
    with torch.no_grad():
        for x, _ in test_loader:
            pred = model(x)
            y_preds.append(pred.numpy())
    y_preds = np.vstack(y_preds)
    
    # Đưa về thang đo ban đầu
    y_true_orig = scaler.inverse_transform(y_te)
    y_pred_orig = scaler.inverse_transform(y_preds)
    
    mse = mean_squared_error(y_true_orig, y_pred_orig)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true_orig, y_pred_orig)
    r2 = r2_score(y_true_orig, y_pred_orig)
    params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    return {
        'params': params,
        'time': train_time,
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'history': history,
        'preds': y_pred_orig.flatten().tolist()
    }

# -------------------------------------------------------------
# 6. ĐỊNH NGHĨA VÀ HUẤN LUYỆN MÔ HÌNH BẰNG KERAS
# -------------------------------------------------------------
print("\n=== [GIAI ĐOẠN 2: THỬ NGHIỆM KERAS (RNN, LSTM, GRU)] ===")

def build_keras_model(mode='rnn', window_size=30, hidden_size=64):
    model = models.Sequential()
    mode = mode.lower()
    if mode == 'rnn':
        model.add(layers.SimpleRNN(hidden_size, return_sequences=True, input_shape=(window_size, 1)))
        model.add(layers.SimpleRNN(hidden_size, return_sequences=False))
    elif mode == 'lstm':
        model.add(layers.LSTM(hidden_size, return_sequences=True, input_shape=(window_size, 1)))
        model.add(layers.LSTM(hidden_size, return_sequences=False))
    elif mode == 'gru':
        model.add(layers.GRU(hidden_size, return_sequences=True, input_shape=(window_size, 1)))
        model.add(layers.GRU(hidden_size, return_sequences=False))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(1))
    return model

def train_eval_keras(model, X_tr, y_tr, X_va, y_va, X_te, y_te, scaler, epochs=20, lr=0.001, batch_size=32):
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=lr), loss='mse')
    
    t0 = time.time()
    hist = model.fit(
        X_tr, y_tr,
        validation_data=(X_va, y_va),
        epochs=epochs,
        batch_size=batch_size,
        verbose=0
    )
    train_time = time.time() - t0
    
    y_preds = model.predict(X_te, verbose=0)
    
    y_true_orig = scaler.inverse_transform(y_te)
    y_pred_orig = scaler.inverse_transform(y_preds)
    
    mse = mean_squared_error(y_true_orig, y_pred_orig)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true_orig, y_pred_orig)
    r2 = r2_score(y_true_orig, y_pred_orig)
    params = model.count_params()
    
    return {
        'params': params,
        'time': train_time,
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'history': {
            'train_loss': [float(x) for x in hist.history['loss']],
            'val_loss': [float(x) for x in hist.history['val_loss']]
        },
        'preds': y_pred_orig.flatten().tolist()
    }

# -------------------------------------------------------------
# 7. CHẠY TOÀN BỘ 12 LƯỢT THỰC NGHIỆM ĐỐI CHUẨN
# -------------------------------------------------------------
metrics_results = {
    'AMZN_Stock': {'PyTorch': {}, 'Keras': {}},
    'Hourly_Energy': {'PyTorch': {}, 'Keras': {}}
}

models_list = ['RNN', 'LSTM', 'GRU']

print("\n--- 7.1. Chạy 6 mô hình trên dữ liệu Cổ phiếu AMZN ---")
for m_name in models_list:
    # PyTorch
    pt_m = PyTorchRNNModel(mode=m_name, input_size=1, hidden_size=64, num_layers=2)
    res_pt = train_eval_pytorch(pt_m, X_train_s, y_train_s, X_val_s, y_val_s, X_test_s, y_test_s, scaler_stock, epochs=25)
    metrics_results['AMZN_Stock']['PyTorch'][m_name] = res_pt
    print(f"[PyTorch {m_name:<4}] AMZN -> RMSE: {res_pt['rmse']:.3f} | MAE: {res_pt['mae']:.3f} | R2: {res_pt['r2']:.4f} | Time: {res_pt['time']:.2f}s")
    
    # Keras
    ke_m = build_keras_model(mode=m_name, window_size=WINDOW_STOCK, hidden_size=64)
    res_ke = train_eval_keras(ke_m, X_train_s, y_train_s, X_val_s, y_val_s, X_test_s, y_test_s, scaler_stock, epochs=25)
    metrics_results['AMZN_Stock']['Keras'][m_name] = res_ke
    print(f"[Keras   {m_name:<4}] AMZN -> RMSE: {res_ke['rmse']:.3f} | MAE: {res_ke['mae']:.3f} | R2: {res_ke['r2']:.4f} | Time: {res_ke['time']:.2f}s")

print("\n--- 7.2. Chạy 6 mô hình trên dữ liệu Tiêu thụ Năng lượng theo giờ ---")
for m_name in models_list:
    # PyTorch
    pt_m = PyTorchRNNModel(mode=m_name, input_size=1, hidden_size=64, num_layers=2)
    res_pt = train_eval_pytorch(pt_m, X_train_e, y_train_e, X_val_e, y_val_e, X_test_e, y_test_e, scaler_energy, epochs=15)
    metrics_results['Hourly_Energy']['PyTorch'][m_name] = res_pt
    print(f"[PyTorch {m_name:<4}] Energy -> RMSE: {res_pt['rmse']:.2f} MW | MAE: {res_pt['mae']:.2f} MW | R2: {res_pt['r2']:.4f} | Time: {res_pt['time']:.2f}s")
    
    # Keras
    ke_m = build_keras_model(mode=m_name, window_size=WINDOW_ENERGY, hidden_size=64)
    res_ke = train_eval_keras(ke_m, X_train_e, y_train_e, X_val_e, y_val_e, X_test_e, y_test_e, scaler_energy, epochs=15)
    metrics_results['Hourly_Energy']['Keras'][m_name] = res_ke
    print(f"[Keras   {m_name:<4}] Energy -> RMSE: {res_ke['rmse']:.2f} MW | MAE: {res_ke['mae']:.2f} MW | R2: {res_ke['r2']:.4f} | Time: {res_ke['time']:.2f}s")

# Lưu kết quả số liệu JSON
with open('ass6_experiments/artifacts/a06_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(metrics_results, f, indent=4)
print("\n[OK] Đã lưu kết quả thực nghiệm vào ass6_experiments/artifacts/a06_metrics.json")

# -------------------------------------------------------------
# 8. XUẤT CÁC BIỂU ĐỒ SO SÁNH KHOA HỌC
# -------------------------------------------------------------
print("\n--- 8. Xuất các biểu đồ đối chuẩn thực nghiệm ---")

# Hình 1: Cấu trúc toán học và dòng thông tin của RNN, LSTM, GRU
fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.0), dpi=150)
for ax in axes: ax.axis('off')

# Box 1: Vanilla RNN
axes[0].text(0.5, 0.9, 'VANILLA RNN CELL', ha='center', fontsize=10, fontweight='bold', color='#1A365D', bbox=dict(boxstyle='round,pad=0.5', facecolor='#EBF8FF', edgecolor='#2B6CB0'))
axes[0].text(0.5, 0.45, 
             "Công thức cập nhật:\n"
             r"$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$" + "\n\n"
             r"$\hat{y}_t = W_{hy} h_t + b_y$" + "\n\n"
             "• 1 Trạng thái ẩn duy nhất (Hidden state)\n"
             "• Lan truyền BPTT gặp triệt tiêu gradient\n"
             "• Phù hợp với phụ thuộc ngắn hạn",
             ha='center', va='center', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'))

# Box 2: LSTM
axes[1].text(0.5, 0.9, 'LSTM CELL (3 CỔNG)', ha='center', fontsize=10, fontweight='bold', color='#744210', bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEFCBF', edgecolor='#D69E2E'))
axes[1].text(0.5, 0.45, 
             "Cơ chế 3 cổng điều khiển:\n"
             r"$f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)$ (Forget)" + "\n"
             r"$i_t = \sigma(W_i [h_{t-1}, x_t] + b_i)$ (Input)" + "\n"
             r"$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$ (Cell)" + "\n"
             r"$o_t = \sigma(W_o [h_{t-1}, x_t] + b_o)$ (Output)" + "\n"
             r"$h_t = o_t \odot \tanh(C_t)$" + "\n\n"
             "• Đường cao tốc Cell State $C_t$\n"
             "• Nhớ dài hạn cực tốt, chống vanishing grad",
             ha='center', va='center', fontsize=8.2, bbox=dict(boxstyle='round,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'))

# Box 3: GRU
axes[2].text(0.5, 0.9, 'GRU CELL (2 CỔNG)', ha='center', fontsize=10, fontweight='bold', color='#22543D', bbox=dict(boxstyle='round,pad=0.5', facecolor='#C6F6D5', edgecolor='#38A169'))
axes[2].text(0.5, 0.45, 
             "Cơ chế 2 cổng tinh gọn:\n"
             r"$z_t = \sigma(W_z [h_{t-1}, x_t] + b_z)$ (Update)" + "\n"
             r"$r_t = \sigma(W_r [h_{t-1}, x_t] + b_r)$ (Reset)" + "\n"
             r"$\tilde{h}_t = \tanh(W [r_t \odot h_{t-1}, x_t] + b)$" + "\n"
             r"$h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$" + "\n\n"
             "• Gộp Cell State vào Hidden State\n"
             "• Ít hơn 25% tham số so với LSTM\n"
             "• Tốc độ huấn luyện nhanh, hiệu quả cao",
             ha='center', va='center', fontsize=8.2, bbox=dict(boxstyle='round,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'))

plt.suptitle('HÌNH 1. SO SÁNH BẢN CHẤT TOÁN HỌC VÀ CẤU TRÚC NỘI TẠI CỦA RNN, LSTM VÀ GRU', fontsize=10.5, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_01_rnn_architectures_comparison.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 1: fig_01_rnn_architectures_comparison.png")

# Hình 2: Quy trình trượt cửa sổ thời gian (Sliding Window Protocol)
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)

ax.text(5.0, 3.6, 'KỸ THUẬT CỬA SỔ TRƯỢT THỜI GIAN (SLIDING LOOKBACK WINDOW)', ha='center', fontsize=11, fontweight='bold', color='#1A365D')

ax.text(3.0, 2.5, 'Cửa sổ quá khứ $X^{(i)} = [x_{t-L}, x_{t-L+1}, ..., x_{t-1}]$ (Lookback $L$ bước)', ha='center', fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='#BEE3F8', edgecolor='#3182CE'))
ax.text(8.0, 2.5, 'Mục tiêu $y^{(i)} = x_t$', ha='center', fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='#C6F6D5', edgecolor='#38A169'))
ax.annotate('', xy=(7.0, 2.5), xytext=(5.6, 2.5), arrowprops=dict(arrowstyle='->', lw=2, color='#2B6CB0'))

ax.text(3.0, 1.3, 'Cửa sổ trượt tiếp theo $X^{(i+1)} = [x_{t-L+1}, ..., x_t]$ (Dịch 1 bước thời gian)', ha='center', fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='#E2E8F0', edgecolor='#A0AEC0'))
ax.text(8.0, 1.3, 'Mục tiêu $y^{(i+1)} = x_{t+1}$', ha='center', fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEFCBF', edgecolor='#D69E2E'))
ax.annotate('', xy=(7.0, 1.3), xytext=(5.9, 1.3), arrowprops=dict(arrowstyle='->', lw=2, color='#718096'))

note = ("Sliding Window chuyển đổi bài toán chuỗi thời gian không cấu trúc thành bài toán Học có giám sát (Supervised Learning):\n"
        "Input tensor kích thước (N, Sequence_Length, Features) -> Output tensor (N, 1). Không shuffle để bảo toàn thứ tự nhân quả.")
ax.text(5.0, 0.4, note, ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#4A5568', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F7FAFC', edgecolor='#CBD5E0'))

plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_02_sliding_window_mechanism.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 2: fig_02_sliding_window_mechanism.png")

# Hình 3: So sánh đường dự đoán trên tập Test AMZN (PyTorch & Keras vs Actual)
y_test_s_orig = scaler_stock.inverse_transform(y_test_s).flatten()
fig, axes = plt.subplots(2, 1, figsize=(9.5, 6.0), dpi=150)
test_dates_s = df_stock['Date'].iloc[-len(y_test_s_orig):].values

# PyTorch
axes[0].plot(test_dates_s, y_test_s_orig, label='Giá thực tế (Ground Truth)', color='#1A202C', lw=1.8)
axes[0].plot(test_dates_s, metrics_results['AMZN_Stock']['PyTorch']['RNN']['preds'], label='PyTorch Vanilla RNN', color='#E53E3E', lw=1.2, linestyle='--')
axes[0].plot(test_dates_s, metrics_results['AMZN_Stock']['PyTorch']['LSTM']['preds'], label='PyTorch LSTM', color='#3182CE', lw=1.4)
axes[0].plot(test_dates_s, metrics_results['AMZN_Stock']['PyTorch']['GRU']['preds'], label='PyTorch GRU', color='#38A169', lw=1.4, linestyle='-.')
axes[0].set_title('Dự đoán Giá Cổ phiếu AMZN bằng PYTORCH trên Tập Test Set', fontsize=9.5, fontweight='bold', color='#1A365D')
axes[0].set_ylabel('Giá cổ phiếu (USD)', fontsize=8.5)
axes[0].legend(fontsize=8, loc='upper left')
axes[0].grid(True, linestyle=':', alpha=0.6)

# Keras
axes[1].plot(test_dates_s, y_test_s_orig, label='Giá thực tế (Ground Truth)', color='#1A202C', lw=1.8)
axes[1].plot(test_dates_s, metrics_results['AMZN_Stock']['Keras']['RNN']['preds'], label='Keras Vanilla RNN', color='#E53E3E', lw=1.2, linestyle='--')
axes[1].plot(test_dates_s, metrics_results['AMZN_Stock']['Keras']['LSTM']['preds'], label='Keras LSTM', color='#3182CE', lw=1.4)
axes[1].plot(test_dates_s, metrics_results['AMZN_Stock']['Keras']['GRU']['preds'], label='Keras GRU', color='#38A169', lw=1.4, linestyle='-.')
axes[1].set_title('Dự đoán Giá Cổ phiếu AMZN bằng KERAS trên Tập Test Set', fontsize=9.5, fontweight='bold', color='#7B341E')
axes[1].set_xlabel('Thời gian giao dịch', fontsize=8.5)
axes[1].set_ylabel('Giá cổ phiếu (USD)', fontsize=8.5)
axes[1].legend(fontsize=8, loc='upper left')
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.suptitle('HÌNH 3. SO SÁNH ĐƯỜNG DỰ ĐOÁN GIÁ CỔ PHIẾU AMAZON GIỮA PYTORCH VÀ KERAS', fontsize=10.5, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_03_amzn_predictions_comparison.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 3: fig_03_amzn_predictions_comparison.png")

# Hình 4: So sánh đường dự đoán trên tập Test Tiêu thụ Năng lượng (PyTorch & Keras vs Actual)
y_test_e_orig = scaler_energy.inverse_transform(y_test_e).flatten()
# Lấy 168 giờ đầu của test set (1 tuần) để hiển thị chi tiết trực quan sắc nét
zoom_len = 168
test_dates_e_zoom = df_energy_sub['Datetime'].iloc[-len(y_test_e_orig) : -len(y_test_e_orig) + zoom_len].values

fig, axes = plt.subplots(2, 1, figsize=(9.5, 6.0), dpi=150)

# PyTorch
axes[0].plot(test_dates_e_zoom, y_test_e_orig[:zoom_len], label='Phụ tải thực tế (Actual MW)', color='#1A202C', lw=1.8)
axes[0].plot(test_dates_e_zoom, metrics_results['Hourly_Energy']['PyTorch']['RNN']['preds'][:zoom_len], label='PyTorch RNN', color='#E53E3E', lw=1.2, linestyle='--')
axes[0].plot(test_dates_e_zoom, metrics_results['Hourly_Energy']['PyTorch']['LSTM']['preds'][:zoom_len], label='PyTorch LSTM', color='#3182CE', lw=1.4)
axes[0].plot(test_dates_e_zoom, metrics_results['Hourly_Energy']['PyTorch']['GRU']['preds'][:zoom_len], label='PyTorch GRU', color='#38A169', lw=1.4, linestyle='-.')
axes[0].set_title('Dự đoán Phụ tải Năng lượng theo Giờ bằng PYTORCH (1 Tuần Test Set)', fontsize=9.5, fontweight='bold', color='#1A365D')
axes[0].set_ylabel('Công suất (MW)', fontsize=8.5)
axes[0].legend(fontsize=8, loc='upper right')
axes[0].grid(True, linestyle=':', alpha=0.6)

# Keras
axes[1].plot(test_dates_e_zoom, y_test_e_orig[:zoom_len], label='Phụ tải thực tế (Actual MW)', color='#1A202C', lw=1.8)
axes[1].plot(test_dates_e_zoom, metrics_results['Hourly_Energy']['Keras']['RNN']['preds'][:zoom_len], label='Keras RNN', color='#E53E3E', lw=1.2, linestyle='--')
axes[1].plot(test_dates_e_zoom, metrics_results['Hourly_Energy']['Keras']['LSTM']['preds'][:zoom_len], label='Keras LSTM', color='#3182CE', lw=1.4)
axes[1].plot(test_dates_e_zoom, metrics_results['Hourly_Energy']['Keras']['GRU']['preds'][:zoom_len], label='Keras GRU', color='#38A169', lw=1.4, linestyle='-.')
axes[1].set_title('Dự đoán Phụ tải Năng lượng theo Giờ bằng KERAS (1 Tuần Test Set)', fontsize=9.5, fontweight='bold', color='#7B341E')
axes[1].set_xlabel('Thời gian (Giờ / Ngày)', fontsize=8.5)
axes[1].set_ylabel('Công suất (MW)', fontsize=8.5)
axes[1].legend(fontsize=8, loc='upper right')
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.suptitle('HÌNH 4. SO SÁNH ĐƯỜNG DỰ ĐOÁN HÀNH VI TIÊU THỤ NĂNG LƯỢNG GIỮA PYTORCH VÀ KERAS', fontsize=10.5, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_04_energy_predictions_comparison.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 4: fig_04_energy_predictions_comparison.png")

# Hình 5: Đường cong Loss huấn luyện và kiểm định (Train/Val Loss qua các Epochs)
fig, axes = plt.subplots(2, 2, figsize=(10, 6.5), dpi=150)

# AMZN PyTorch
for m in models_list:
    axes[0, 0].plot(metrics_results['AMZN_Stock']['PyTorch'][m]['history']['train_loss'], label=f'Train {m}')
    axes[0, 0].plot(metrics_results['AMZN_Stock']['PyTorch'][m]['history']['val_loss'], label=f'Val {m}', linestyle='--')
axes[0, 0].set_title('AMZN Stock - PyTorch Loss', fontsize=9.5, fontweight='bold')
axes[0, 0].set_ylabel('MSE Loss', fontsize=8.5)
axes[0, 0].legend(fontsize=7, loc='upper right')
axes[0, 0].grid(True, linestyle=':', alpha=0.6)

# AMZN Keras
for m in models_list:
    axes[0, 1].plot(metrics_results['AMZN_Stock']['Keras'][m]['history']['train_loss'], label=f'Train {m}')
    axes[0, 1].plot(metrics_results['AMZN_Stock']['Keras'][m]['history']['val_loss'], label=f'Val {m}', linestyle='--')
axes[0, 1].set_title('AMZN Stock - Keras Loss', fontsize=9.5, fontweight='bold')
axes[0, 1].legend(fontsize=7, loc='upper right')
axes[0, 1].grid(True, linestyle=':', alpha=0.6)

# Energy PyTorch
for m in models_list:
    axes[1, 0].plot(metrics_results['Hourly_Energy']['PyTorch'][m]['history']['train_loss'], label=f'Train {m}')
    axes[1, 0].plot(metrics_results['Hourly_Energy']['PyTorch'][m]['history']['val_loss'], label=f'Val {m}', linestyle='--')
axes[1, 0].set_title('Hourly Energy - PyTorch Loss', fontsize=9.5, fontweight='bold')
axes[1, 0].set_xlabel('Epoch', fontsize=8.5)
axes[1, 0].set_ylabel('MSE Loss', fontsize=8.5)
axes[1, 0].legend(fontsize=7, loc='upper right')
axes[1, 0].grid(True, linestyle=':', alpha=0.6)

# Energy Keras
for m in models_list:
    axes[1, 1].plot(metrics_results['Hourly_Energy']['Keras'][m]['history']['train_loss'], label=f'Train {m}')
    axes[1, 1].plot(metrics_results['Hourly_Energy']['Keras'][m]['history']['val_loss'], label=f'Val {m}', linestyle='--')
axes[1, 1].set_title('Hourly Energy - Keras Loss', fontsize=9.5, fontweight='bold')
axes[1, 1].set_xlabel('Epoch', fontsize=8.5)
axes[1, 1].legend(fontsize=7, loc='upper right')
axes[1, 1].grid(True, linestyle=':', alpha=0.6)

plt.suptitle('HÌNH 5. ĐƯỜNG CONG HỘI TỤ LOSS HUẤN LUYỆN VÀ KIỂM ĐỊNH (TRAIN VS VALIDATION LOSS)', fontsize=10.5, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_05_loss_convergence_comparison.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 5: fig_05_loss_convergence_comparison.png")

# Hình 6: Biểu đồ cột so sánh RMSE và MAE giữa các mô hình trên cả 2 bài toán
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), dpi=150)

# AMZN RMSE & MAE
models_labels = ['PT-RNN', 'PT-LSTM', 'PT-GRU', 'KE-RNN', 'KE-LSTM', 'KE-GRU']
rmse_amzn = [
    metrics_results['AMZN_Stock']['PyTorch']['RNN']['rmse'],
    metrics_results['AMZN_Stock']['PyTorch']['LSTM']['rmse'],
    metrics_results['AMZN_Stock']['PyTorch']['GRU']['rmse'],
    metrics_results['AMZN_Stock']['Keras']['RNN']['rmse'],
    metrics_results['AMZN_Stock']['Keras']['LSTM']['rmse'],
    metrics_results['AMZN_Stock']['Keras']['GRU']['rmse'],
]
mae_amzn = [
    metrics_results['AMZN_Stock']['PyTorch']['RNN']['mae'],
    metrics_results['AMZN_Stock']['PyTorch']['LSTM']['mae'],
    metrics_results['AMZN_Stock']['PyTorch']['GRU']['mae'],
    metrics_results['AMZN_Stock']['Keras']['RNN']['mae'],
    metrics_results['AMZN_Stock']['Keras']['LSTM']['mae'],
    metrics_results['AMZN_Stock']['Keras']['GRU']['mae'],
]
x = np.arange(len(models_labels))
w = 0.35
axes[0].bar(x - w/2, rmse_amzn, w, label='RMSE (USD)', color='#3182CE', edgecolor='#1A365D')
axes[0].bar(x + w/2, mae_amzn, w, label='MAE (USD)', color='#ED8936', edgecolor='#7B341E')
axes[0].set_title('Sai số Dự đoán Cổ phiếu AMZN', fontsize=9.5, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(models_labels, rotation=25, ha='right', fontsize=8)
axes[0].set_ylabel('Sai số (USD)', fontsize=8.5)
axes[0].legend(fontsize=8)
axes[0].grid(axis='y', linestyle=':', alpha=0.6)

# Energy R2 Score
r2_energy = [
    metrics_results['Hourly_Energy']['PyTorch']['RNN']['r2'],
    metrics_results['Hourly_Energy']['PyTorch']['LSTM']['r2'],
    metrics_results['Hourly_Energy']['PyTorch']['GRU']['r2'],
    metrics_results['Hourly_Energy']['Keras']['RNN']['r2'],
    metrics_results['Hourly_Energy']['Keras']['LSTM']['r2'],
    metrics_results['Hourly_Energy']['Keras']['GRU']['r2'],
]
colors_r2 = ['#4299E1', '#3182CE', '#2B6CB0', '#F6AD55', '#ED8936', '#DD6B20']
bars = axes[1].bar(models_labels, r2_energy, color=colors_r2, width=0.55, edgecolor='#2D3748')
axes[1].set_title('Hệ số Xác định R² trên Dữ liệu Tiêu thụ Năng lượng', fontsize=9.5, fontweight='bold')
axes[1].set_xticks(x)
axes[1].set_xticklabels(models_labels, rotation=25, ha='right', fontsize=8)
axes[1].set_ylabel('Điểm R² (Càng gần 1.0 càng tốt)', fontsize=8.5)
axes[1].set_ylim(min(r2_energy) - 0.05, 1.0)
axes[1].grid(axis='y', linestyle=':', alpha=0.6)
for bar, val in zip(bars, r2_energy):
    axes[1].text(bar.get_x() + bar.get_width()/2., val + 0.005, f'{val:.4f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

plt.suptitle('HÌNH 6. ĐỐI CHUẨN HIỆU NĂNG SAI SỐ (RMSE, MAE) VÀ HỆ SỐ XÁC ĐỊNH R²', fontsize=10.5, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_06_metrics_benchmarking.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 6: fig_06_metrics_benchmarking.png")

# Hình 7: So sánh thời gian huấn luyện và số tham số giữa các mô hình
fig, axes = plt.subplots(1, 2, figsize=(10, 4.0), dpi=150)
params_list = [
    metrics_results['AMZN_Stock']['PyTorch']['RNN']['params'],
    metrics_results['AMZN_Stock']['PyTorch']['LSTM']['params'],
    metrics_results['AMZN_Stock']['PyTorch']['GRU']['params'],
    metrics_results['AMZN_Stock']['Keras']['RNN']['params'],
    metrics_results['AMZN_Stock']['Keras']['LSTM']['params'],
    metrics_results['AMZN_Stock']['Keras']['GRU']['params']
]
axes[0].bar(models_labels, params_list, color='#718096', width=0.55, edgecolor='#1A202C')
axes[0].set_title('Số Tham số Huấn luyện (Trainable Parameters)', fontsize=9.5, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(models_labels, rotation=25, ha='right', fontsize=8)
axes[0].set_ylabel('Số lượng tham số', fontsize=8.5)
axes[0].grid(axis='y', linestyle=':', alpha=0.6)
for i, v in enumerate(params_list):
    axes[0].text(i, v + max(params_list)*0.02, f'{v:,}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

times_amzn = [
    metrics_results['AMZN_Stock']['PyTorch']['RNN']['time'],
    metrics_results['AMZN_Stock']['PyTorch']['LSTM']['time'],
    metrics_results['AMZN_Stock']['PyTorch']['GRU']['time'],
    metrics_results['AMZN_Stock']['Keras']['RNN']['time'],
    metrics_results['AMZN_Stock']['Keras']['LSTM']['time'],
    metrics_results['AMZN_Stock']['Keras']['GRU']['time']
]
axes[1].bar(models_labels, times_amzn, color='#38A169', width=0.55, edgecolor='#22543D')
axes[1].set_title('Thời gian Huấn luyện AMZN (25 Epochs)', fontsize=9.5, fontweight='bold')
axes[1].set_xticks(x)
axes[1].set_xticklabels(models_labels, rotation=25, ha='right', fontsize=8)
axes[1].set_ylabel('Thời gian (giây)', fontsize=8.5)
axes[1].grid(axis='y', linestyle=':', alpha=0.6)
for i, v in enumerate(times_amzn):
    axes[1].text(i, v + max(times_amzn)*0.02, f'{v:.2f}s', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

plt.suptitle('HÌNH 7. CHI PHÍ TÍNH TOÁN: SỐ THAM SỐ VÀ THỜI GIAN HUẤN LUYỆN', fontsize=10.5, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_07_computational_cost.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 7: fig_07_computational_cost.png")

# Hình 8: Phân tích phần dư sai số (Residuals = Actual - Predicted)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.0), dpi=150)
res_amzn_lstm = y_test_s_orig - np.array(metrics_results['AMZN_Stock']['PyTorch']['LSTM']['preds'])
res_energy_gru = y_test_e_orig - np.array(metrics_results['Hourly_Energy']['PyTorch']['GRU']['preds'])

sns.histplot(res_amzn_lstm, kde=True, ax=axes[0], color='#2B6CB0', bins=30)
axes[0].axvline(0, color='red', linestyle='--', lw=1.2)
axes[0].set_title('Phần dư Sai số: PyTorch LSTM trên AMZN', fontsize=9.5, fontweight='bold')
axes[0].set_xlabel('Sai số (Actual - Predicted) USD', fontsize=8.5)
axes[0].set_ylabel('Tần suất', fontsize=8.5)
axes[0].grid(True, linestyle=':', alpha=0.6)

sns.histplot(res_energy_gru, kde=True, ax=axes[1], color='#38A169', bins=30)
axes[1].axvline(0, color='red', linestyle='--', lw=1.2)
axes[1].set_title('Phần dư Sai số: PyTorch GRU trên Energy', fontsize=9.5, fontweight='bold')
axes[1].set_xlabel('Sai số (Actual - Predicted) MW', fontsize=8.5)
axes[1].set_ylabel('Tần suất', fontsize=8.5)
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.suptitle('HÌNH 8. PHÂN TÍCH PHÂN PHỐI PHẦN DƯ SAI SỐ DỰ ĐOÁN (RESIDUAL ANALYSIS)', fontsize=10.5, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('ass6_experiments/plots/fig_08_residuals_analysis.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 8: fig_08_residuals_analysis.png")

print("\n=== HOÀN TẤT THỰC NGHIỆM VÀ XUẤT TOÀN BỘ SỐ LIỆU & BIỂU ĐỒ! ===")
