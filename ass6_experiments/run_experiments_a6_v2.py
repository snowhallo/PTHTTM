import os, sys, json, time
sys.stdout.reconfigure(encoding='utf-8')
os.environ['KERAS_BACKEND'] = 'torch'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

import keras
from keras import layers, models

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -------------------------------------------------------------
# 0. THIẾT LẬP THƯ MỤC VÀ STYLE
# -------------------------------------------------------------
os.makedirs('ass6_experiments/plots_v2', exist_ok=True)
os.makedirs('ass6_experiments/artifacts', exist_ok=True)

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI']
plt.rcParams['axes.unicode_minus'] = False

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

print("=== BẮT ĐẦU CHUỖI THỰC NGHIỆM ASSIGNMENT 06 (V2 THEO CHUẨN TRUNGND) ===")

# -------------------------------------------------------------
# 1. NẠP DỮ LIỆU ĐÃ TIỀN XỬ LÝ
# -------------------------------------------------------------
# Dataset 1: Customer Behavior theo ngày (305 ngày)
df_cust = pd.read_csv('data/assignment_06/customer_behavior_daily.csv')
df_cust['Date'] = pd.to_datetime(df_cust['Date'])
df_cust.sort_values('Date', inplace=True)
df_cust.reset_index(drop=True, inplace=True)

print(f"[*] Customer Behavior records: {len(df_cust)} mốc thời gian từ {df_cust['Date'].min().strftime('%Y-%m-%d')} đến {df_cust['Date'].max().strftime('%Y-%m-%d')}")
print(df_cust.describe().round(2))

# Dataset 2: AAPL Stock (1,259 phiên giao dịch)
df_aapl = pd.read_csv('data/assignment_06/aapl_stock_5yr.csv')
df_aapl['date'] = pd.to_datetime(df_aapl['date'])
df_aapl.sort_values('date', inplace=True)
df_aapl.reset_index(drop=True, inplace=True)

print(f"\n[*] AAPL Stock records: {len(df_aapl)} phiên giao dịch từ {df_aapl['date'].min().strftime('%Y-%m-%d')} đến {df_aapl['date'].max().strftime('%Y-%m-%d')}")
print(df_aapl.describe().round(2))

# -------------------------------------------------------------
# 2. XUẤT CÁC BIỂU ĐỒ EDA VÀ SƠ ĐỒ PIPELINE (HÌNH 1 ĐẾN HÌNH 13)
# -------------------------------------------------------------
print("\n--- 2. Xuất các biểu đồ phân tích EDA & Sơ đồ phương pháp luận ---")

# Hình 1: Pipeline tổng thể của Assignment 06
fig, ax = plt.subplots(figsize=(10.5, 3.8), dpi=150)
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)

boxes = [
    (1.0, 1.5, "1. DỮ LIỆU\n• Online Retail (541k)\n• S&P 500 AAPL (1,259)", "#EBF8FF", "#3182CE"),
    (3.5, 1.5, "2. TIỀN XỬ LÝ\n• Làm sạch, groupby ngày\n• Split 70/15/15 theo time\n• StandardScaler tách X, y", "#FEFCBF", "#D69E2E"),
    (6.0, 1.5, "3. MÔ HÌNH\n• Seq length = 20\n• PyTorch BasicRNN(64)\n• Keras SimpleRNN(64)", "#C6F6D5", "#38A169"),
    (8.5, 1.5, "4. ĐỐI CHUẨN\n• MAE, MSE, RMSE, R²\n• So sánh PyTorch vs Keras\n• Trực quan hóa dự đoán", "#FED7D7", "#E53E3E")
]

for x, y, text, bg, border in boxes:
    ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.6', facecolor=bg, edgecolor=border, lw=1.5))

# Mũi tên liên kết
for i in range(len(boxes) - 1):
    ax.annotate('', xy=(boxes[i+1][0] - 1.1, 1.5), xytext=(boxes[i][0] + 1.1, 1.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='#4A5568'))

ax.set_title("HÌNH 1. PIPELINE TỔNG THỂ CỦA ASSIGNMENT 06", fontsize=11, fontweight='bold', color='#1A365D')
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_01.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 1: fig_01.png")

# Hình 2: Cấu trúc Basic RNN many-to-one
fig, ax = plt.subplots(figsize=(9.5, 4.0), dpi=150)
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)

ax.text(5.0, 3.6, "CẤU TRÚC BASIC RNN (MANY-TO-ONE)", ha='center', fontsize=11, fontweight='bold', color='#1A365D')

# Sơ đồ unrolled qua thời gian
timesteps = ["x₁", "x₂", "...", "xₜ₋₁", "xₜ (t=20)"]
for idx, ts in enumerate(timesteps):
    x_pos = 1.5 + idx * 1.75
    # Input
    ax.text(x_pos, 0.8, ts, ha='center', va='center', fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle='circle,pad=0.4', facecolor='#E2E8F0', edgecolor='#718096'))
    # Hidden
    ax.text(x_pos, 2.0, f"h_{idx+1}" if idx < 2 else ("h_t" if idx == 4 else f"h_{ts}"),
            ha='center', va='center', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#BEE3F8', edgecolor='#3182CE'))
    # Mũi tên input -> hidden
    ax.annotate('', xy=(x_pos, 1.6), xytext=(x_pos, 1.2), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2B6CB0'))
    # Mũi tên hidden -> hidden
    if idx > 0:
        prev_x = 1.5 + (idx - 1) * 1.75
        ax.annotate('', xy=(x_pos - 0.45, 2.0), xytext=(prev_x + 0.45, 2.0),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='#2B6CB0'))

# Output từ hidden cuối
ax.text(8.5, 3.0, "ŷ (Output)", ha='center', va='center', fontsize=9.5, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#C6F6D5', edgecolor='#38A169'))
ax.annotate('', xy=(8.5, 2.7), xytext=(8.5, 2.35), arrowprops=dict(arrowstyle='->', lw=2, color='#276749'))

ax.text(5.0, 0.2, "Công thức: hₜ = tanh(W_xh · xₜ + W_hh · hₜ₋₁ + b_h)  |  ŷ = W_hy · h_T + b_y",
        ha='center', fontsize=9, fontstyle='italic', color='#4A5568')

plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_02.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 2: fig_02.png")

# Hình 3: Doanh thu theo ngày của Customer Behavior
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(df_cust['Date'], df_cust['Revenue'], color='#2B6CB0', lw=1.2)
ax.set_title('DOANH THU THEO NGÀY CỦA CUSTOMER BEHAVIOR (ONLINE RETAIL)', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Ngày giao dịch (2010 - 2011)', fontsize=8.5)
ax.set_ylabel('Doanh thu (GBP / Đơn vị tiền tệ)', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_03.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 3: fig_03.png")

# Hình 4: Số giao dịch theo ngày
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(df_cust['Date'], df_cust['Transactions'], color='#DD6B20', lw=1.2)
ax.set_title('SỐ LƯỢNG GIAO DỊCH (INVOICES) THEO NGÀY', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Ngày giao dịch', fontsize=8.5)
ax.set_ylabel('Số hóa đơn (Transactions)', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_04.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 4: fig_04.png")

# Hình 5: Số khách hàng duy nhất theo ngày
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(df_cust['Date'], df_cust['Customers'], color='#38A169', lw=1.2)
ax.set_title('SỐ KHÁCH HÀNG DUY NHẤT (UNIQUE CUSTOMERS) THEO NGÀY', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Ngày giao dịch', fontsize=8.5)
ax.set_ylabel('Số khách hàng (Customers)', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_05.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 5: fig_05.png")

# Hình 6: Tổng số lượng hàng bán theo ngày
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(df_cust['Date'], df_cust['Quantity'], color='#805AD5', lw=1.2)
ax.set_title('TỔNG SỐ LƯỢNG HÀNG BÁN (QUANTITY) THEO NGÀY', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Ngày giao dịch', fontsize=8.5)
ax.set_ylabel('Tổng số lượng sản phẩm', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_06.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 6: fig_06.png")

# Hình 7: Phân phối doanh thu hằng ngày
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=150)
sns.histplot(df_cust['Revenue'], kde=True, color='#3182CE', bins=35, ax=ax)
ax.set_title('PHÂN PHỐI DOANH THU HẰNG NGÀY (CUSTOMER BEHAVIOR)', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Doanh thu trong ngày', fontsize=8.5)
ax.set_ylabel('Tần số xuất hiện', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_07.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 7: fig_07.png")

# Hình 8: Ma trận tương quan các feature Customer Behavior
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=150)
corr_cust = df_cust[['Revenue', 'Transactions', 'Customers', 'Quantity', 'AvgUnitPrice']].corr()
sns.heatmap(corr_cust, annot=True, cmap='Blues', fmt='.2f', square=True, ax=ax, cbar_kws={'shrink': 0.8})
ax.set_title('MA TRẬN TƯƠNG QUAN CÁC ĐẶC TRƯNG CUSTOMER BEHAVIOR', fontsize=10, fontweight='bold', color='#1A365D')
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_08.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 8: fig_08.png")

# Hình 9: Giá đóng cửa AAPL theo thời gian
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(df_aapl['date'], df_aapl['close'], color='#2B6CB0', lw=1.2)
ax.set_title('GIÁ ĐÓNG CỬA CỔ PHIẾU AAPL THEO THỜI GIAN (2013 - 2018)', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Thời gian giao dịch', fontsize=8.5)
ax.set_ylabel('Giá đóng cửa (USD)', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_09.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 9: fig_09.png")

# Hình 10: Khối lượng giao dịch AAPL
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(df_aapl['date'], df_aapl['volume'] / 1e6, color='#DD6B20', lw=1.0)
ax.set_title('KHỐI LƯỢNG GIAO DỊCH CỔ PHIẾU AAPL THEO PHIÊN (TRIỆU CỔ PHIẾU)', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Thời gian giao dịch', fontsize=8.5)
ax.set_ylabel('Khối lượng (Triệu CP)', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_10.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 10: fig_10.png")

# Hình 11: Phân phối giá đóng cửa AAPL
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=150)
sns.histplot(df_aapl['close'], kde=True, color='#38A169', bins=35, ax=ax)
ax.set_title('PHÂN PHỐI GIÁ ĐÓNG CỬA CỔ PHIẾU AAPL', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Giá đóng cửa (USD)', fontsize=8.5)
ax.set_ylabel('Tần số xuất hiện', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_11.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 11: fig_11.png")

# Hình 12: Tương quan giữa các biến AAPL
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=150)
corr_aapl = df_aapl[['open', 'high', 'low', 'close', 'volume']].corr()
sns.heatmap(corr_aapl, annot=True, cmap='YlGnBu', fmt='.2f', square=True, ax=ax, cbar_kws={'shrink': 0.8})
ax.set_title('MA TRẬN TƯƠNG QUAN GIỮA CÁC BIẾN CỔ PHIẾU AAPL', fontsize=10, fontweight='bold', color='#1A365D')
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_12.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 12: fig_12.png")

# Hình 13: Pipeline chuẩn bị chuỗi thời gian
fig, ax = plt.subplots(figsize=(10.0, 4.0), dpi=150)
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)

ax.text(5.0, 3.6, "PIPELINE CHUẨN BỊ CHUỖI THỜI GIAN (TIME-SERIES PREPROCESSING)", ha='center', fontsize=11, fontweight='bold', color='#1A365D')

pipe_steps = [
    (1.5, 2.4, "Dataset Gốc\n(Customer/AAPL)", "#EDF2F7"),
    (3.5, 2.4, "Chia Thời gian\n70% / 15% / 15%", "#EBF8FF"),
    (5.5, 2.4, "StandardScaler\nFit Train, Trans V/T", "#FEFCBF"),
    (7.5, 2.4, "Sliding Window\nL=20 timesteps", "#C6F6D5"),
    (9.0, 2.4, "Tensor 3D\n(N, 20, 5)", "#FED7D7")
]

for x, y, text, bg in pipe_steps:
    ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=bg, edgecolor='#4A5568'))

for i in range(len(pipe_steps) - 1):
    ax.annotate('', xy=(pipe_steps[i+1][0] - 0.7, 2.4), xytext=(pipe_steps[i][0] + 0.7, 2.4),
                arrowprops=dict(arrowstyle='->', lw=1.8, color='#2B6CB0'))

ax.text(5.0, 1.0, 
        "Nguyên tắc vàng: Không xáo trộn (shuffle=False) để bảo tồn thứ tự thời gian.\n"
        "Tách riêng Scaler cho tập thuộc tính X và biến mục tiêu y để dễ dàng inverse_transform khi tính MAE, RMSE.",
        ha='center', fontsize=8.5, fontstyle='italic', color='#2D3748',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#F7FAFC', edgecolor='#CBD5E0'))

plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_13.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 13: fig_13.png")

# -------------------------------------------------------------
# 3. HÀM TẠO SEQUENCE & PIPELINE THỰC NGHIỆM CHUẨN MỰC
# -------------------------------------------------------------
def create_sequences(X, y, sequence_length=20):
    X_seq, y_seq = [], []
    for i in range(len(X) - sequence_length):
        X_seq.append(X[i : i + sequence_length])
        y_seq.append(y[i + sequence_length])
    return np.array(X_seq), np.array(y_seq)

# Lớp PyTorch BasicRNN chuẩn
class BasicRNN(nn.Module):
    def __init__(self, input_size=5, hidden_size=64):
        super().__init__()
        self.rnn = nn.RNN(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        
    def forward(self, x):
        out, _ = self.rnn(x)
        last_out = out[:, -1, :]
        return self.fc(last_out)

# Hàm huấn luyện PyTorch
def train_eval_pytorch_v2(X_tr, y_tr, X_va, y_va, X_te, y_te, scaler_y, epochs=50, lr=0.001, batch_size=16):
    model = BasicRNN(input_size=X_tr.shape[2], hidden_size=64)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    train_loader = DataLoader(TensorDataset(torch.tensor(X_tr, dtype=torch.float32), torch.tensor(y_tr, dtype=torch.float32)), batch_size=batch_size, shuffle=False)
    val_x_t = torch.tensor(X_va, dtype=torch.float32)
    val_y_t = torch.tensor(y_va, dtype=torch.float32)
    test_x_t = torch.tensor(X_te, dtype=torch.float32)
    
    train_losses, val_losses = [], []
    t0 = time.time()
    
    for epoch in range(epochs):
        model.train()
        r_loss = 0.0
        for bx, by in train_loader:
            optimizer.zero_grad()
            preds = model(bx)
            loss = criterion(preds, by)
            loss.backward()
            optimizer.step()
            r_loss += loss.item() * len(bx)
        ep_loss = r_loss / len(train_loader.dataset)
        train_losses.append(ep_loss)
        
        model.eval()
        with torch.no_grad():
            v_loss = criterion(model(val_x_t), val_y_t).item()
            val_losses.append(v_loss)
            
    train_time = time.time() - t0
    
    # Test prediction
    model.eval()
    with torch.no_grad():
        test_preds = model(test_x_t).numpy()
        
    y_test_orig = scaler_y.inverse_transform(y_te)
    preds_orig = scaler_y.inverse_transform(test_preds)
    
    mae = mean_absolute_error(y_test_orig, preds_orig)
    mse = mean_squared_error(y_test_orig, preds_orig)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test_orig, preds_orig)
    
    return {
        'mae': mae, 'mse': mse, 'rmse': rmse, 'r2': r2,
        'train_time': train_time,
        'train_loss': train_losses,
        'val_loss': val_losses,
        'actual': y_test_orig.flatten(),
        'preds': preds_orig.flatten(),
        'residuals': (y_test_orig.flatten() - preds_orig.flatten())
    }

# Hàm huấn luyện Keras
def train_eval_keras_v2(X_tr, y_tr, X_va, y_va, X_te, y_te, scaler_y, epochs=50, lr=0.001, batch_size=16):
    model = models.Sequential([
        layers.Input(shape=(X_tr.shape[1], X_tr.shape[2])),
        layers.SimpleRNN(64, activation='tanh', return_sequences=False),
        layers.Dense(1)
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=lr), loss='mse')
    
    t0 = time.time()
    hist = model.fit(
        X_tr, y_tr,
        validation_data=(X_va, y_va),
        epochs=epochs,
        batch_size=batch_size,
        shuffle=False,
        verbose=0
    )
    train_time = time.time() - t0
    
    test_preds = model.predict(X_te, verbose=0)
    y_test_orig = scaler_y.inverse_transform(y_te)
    preds_orig = scaler_y.inverse_transform(test_preds)
    
    mae = mean_absolute_error(y_test_orig, preds_orig)
    mse = mean_squared_error(y_test_orig, preds_orig)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test_orig, preds_orig)
    
    return {
        'mae': mae, 'mse': mse, 'rmse': rmse, 'r2': r2,
        'train_time': train_time,
        'train_loss': [float(x) for x in hist.history['loss']],
        'val_loss': [float(x) for x in hist.history['val_loss']],
        'actual': y_test_orig.flatten(),
        'preds': preds_orig.flatten(),
        'residuals': (y_test_orig.flatten() - preds_orig.flatten())
    }

# -------------------------------------------------------------
# 4. CHẠY 4 THÍ NGHIỆM CHÍNH
# -------------------------------------------------------------
results = {
    'Customer_Behavior': {},
    'AAPL_Stock': {}
}

# --- 4.1. Chuẩn bị dữ liệu Customer Behavior ---
print("\n--- 4.1. Tiền xử lý dữ liệu Customer Behavior (70/15/15) ---")
cust_features = ['Revenue', 'Transactions', 'Customers', 'Quantity', 'AvgUnitPrice']
cust_X = df_cust[cust_features].values
cust_y = df_cust[['Revenue']].values

n_c = len(df_cust)
c_tr_end = int(n_c * 0.70)  # 213
c_va_end = int(n_c * 0.85)  # 259
print(f"Customer points: Train={c_tr_end}, Val={c_va_end - c_tr_end}, Test={n_c - c_va_end}")

scaler_cX = StandardScaler()
scaler_cy = StandardScaler()

cX_train_s = scaler_cX.fit_transform(cust_X[:c_tr_end])
cy_train_s = scaler_cy.fit_transform(cust_y[:c_tr_end])

cX_val_s = scaler_cX.transform(cust_X[c_tr_end:c_va_end])
cy_val_s = scaler_cy.transform(cust_y[c_tr_end:c_va_end])

cX_test_s = scaler_cX.transform(cust_X[c_va_end:])
cy_test_s = scaler_cy.transform(cust_y[c_va_end:])

cX_tr_seq, cy_tr_seq = create_sequences(cX_train_s, cy_train_s, sequence_length=20)
cX_va_seq, cy_va_seq = create_sequences(cX_val_s, cy_val_s, sequence_length=20)
cX_te_seq, cy_te_seq = create_sequences(cX_test_s, cy_test_s, sequence_length=20)

print(f"Customer Sequences (L=20): Train={len(cX_tr_seq)}, Val={len(cX_va_seq)}, Test={len(cX_te_seq)}")

# Chạy PyTorch Customer
print("[*] Chạy PyTorch BasicRNN trên Customer Behavior...")
res_pt_cust = train_eval_pytorch_v2(cX_tr_seq, cy_tr_seq, cX_va_seq, cy_va_seq, cX_te_seq, cy_te_seq, scaler_cy, epochs=50)
results['Customer_Behavior']['PyTorch'] = res_pt_cust
print(f"    PyTorch -> MAE: {res_pt_cust['mae']:,.2f} | RMSE: {res_pt_cust['rmse']:,.2f} | R2: {res_pt_cust['r2']:.4f}")

# Chạy Keras Customer
print("[*] Chạy Keras SimpleRNN trên Customer Behavior...")
res_ke_cust = train_eval_keras_v2(cX_tr_seq, cy_tr_seq, cX_va_seq, cy_va_seq, cX_te_seq, cy_te_seq, scaler_cy, epochs=50)
results['Customer_Behavior']['Keras'] = res_ke_cust
print(f"    Keras   -> MAE: {res_ke_cust['mae']:,.2f} | RMSE: {res_ke_cust['rmse']:,.2f} | R2: {res_ke_cust['r2']:.4f}")


# --- 4.2. Chuẩn bị dữ liệu AAPL Stock ---
print("\n--- 4.2. Tiền xử lý dữ liệu AAPL Stock (70/15/15) ---")
aapl_features = ['open', 'high', 'low', 'close', 'volume']
aapl_X = df_aapl[aapl_features].values
aapl_y = df_aapl[['close']].values

n_a = len(df_aapl)
a_tr_end = int(n_a * 0.70)  # 881
a_va_end = int(n_a * 0.85)  # 1070
print(f"AAPL points: Train={a_tr_end}, Val={a_va_end - a_tr_end}, Test={n_a - a_va_end}")

scaler_aX = StandardScaler()
scaler_ay = StandardScaler()

aX_train_s = scaler_aX.fit_transform(aapl_X[:a_tr_end])
ay_train_s = scaler_ay.fit_transform(aapl_y[:a_tr_end])

aX_val_s = scaler_aX.transform(aapl_X[a_tr_end:a_va_end])
ay_val_s = scaler_ay.transform(aapl_y[a_tr_end:a_va_end])

aX_test_s = scaler_aX.transform(aapl_X[a_va_end:])
ay_test_s = scaler_ay.transform(aapl_y[a_va_end:])

aX_tr_seq, ay_tr_seq = create_sequences(aX_train_s, ay_train_s, sequence_length=20)
aX_va_seq, ay_va_seq = create_sequences(aX_val_s, ay_val_s, sequence_length=20)
aX_te_seq, ay_te_seq = create_sequences(aX_test_s, ay_test_s, sequence_length=20)

print(f"AAPL Sequences (L=20): Train={len(aX_tr_seq)}, Val={len(aX_va_seq)}, Test={len(aX_te_seq)}")

# Chạy PyTorch AAPL
print("[*] Chạy PyTorch BasicRNN trên AAPL Stock...")
res_pt_aapl = train_eval_pytorch_v2(aX_tr_seq, ay_tr_seq, aX_va_seq, ay_va_seq, aX_te_seq, ay_te_seq, scaler_ay, epochs=50)
results['AAPL_Stock']['PyTorch'] = res_pt_aapl
print(f"    PyTorch -> MAE: {res_pt_aapl['mae']:.4f} | RMSE: {res_pt_aapl['rmse']:.4f} | R2: {res_pt_aapl['r2']:.4f}")

# Chạy Keras AAPL
print("[*] Chạy Keras SimpleRNN trên AAPL Stock...")
res_ke_aapl = train_eval_keras_v2(aX_tr_seq, ay_tr_seq, aX_va_seq, ay_va_seq, aX_te_seq, ay_te_seq, scaler_ay, epochs=50)
results['AAPL_Stock']['Keras'] = res_ke_aapl
print(f"    Keras   -> MAE: {res_ke_aapl['mae']:.4f} | RMSE: {res_ke_aapl['rmse']:.4f} | R2: {res_ke_aapl['r2']:.4f}")


# -------------------------------------------------------------
# 5. XUẤT CÁC BIỂU ĐỒ KẾT QUẢ THỰC NGHIỆM (HÌNH 14 ĐẾN HÌNH 28)
# -------------------------------------------------------------
print("\n--- 5. Xuất các biểu đồ kết quả thực nghiệm (Hình 14 -> 28) ---")

# Hình 14: Loss train/validation của PyTorch trên Customer Behavior
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=150)
ax.plot(res_pt_cust['train_loss'], label='Train Loss', color='#2B6CB0', lw=1.5)
ax.plot(res_pt_cust['val_loss'], label='Validation Loss', color='#DD6B20', lw=1.5, linestyle='--')
ax.set_title('LOSS TRAIN/VALIDATION CỦA PYTORCH TRÊN CUSTOMER BEHAVIOR', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Epoch', fontsize=8.5)
ax.set_ylabel('MSE Loss', fontsize=8.5)
ax.legend(fontsize=8)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_14.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 14: fig_14.png")

# Hình 15: Doanh thu thật và dự đoán – PyTorch Customer Behavior
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(res_pt_cust['actual'], label='Doanh thu thật (Actual)', color='#1A202C', lw=1.8)
ax.plot(res_pt_cust['preds'], label='Dự đoán PyTorch BasicRNN', color='#E53E3E', lw=1.5, linestyle='--')
ax.set_title('DOANH THU THẬT VÀ DỰ ĐOÁN – PYTORCH CUSTOMER BEHAVIOR', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Mốc thời gian kiểm thử (Test Step)', fontsize=8.5)
ax.set_ylabel('Doanh thu', fontsize=8.5)
ax.legend(fontsize=8)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_15.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 15: fig_15.png")

# Hình 16: Sai số dự đoán – PyTorch Customer Behavior
fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=150)
ax.plot(res_pt_cust['residuals'], color='#C53030', marker='o', markersize=3, lw=1.2)
ax.axhline(0, color='gray', linestyle='--', alpha=0.7)
ax.set_title('SAI SỐ DỰ ĐOÁN (RESIDUALS = ACTUAL - PRED) – PYTORCH CUSTOMER BEHAVIOR', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Test Step', fontsize=8.5)
ax.set_ylabel('Sai số Doanh thu', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_16.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 16: fig_16.png")

# Hình 17: Loss train/validation của PyTorch trên AAPL
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=150)
ax.plot(res_pt_aapl['train_loss'], label='Train Loss', color='#2B6CB0', lw=1.5)
ax.plot(res_pt_aapl['val_loss'], label='Validation Loss', color='#DD6B20', lw=1.5, linestyle='--')
ax.set_title('LOSS TRAIN/VALIDATION CỦA PYTORCH TRÊN AAPL STOCK', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Epoch', fontsize=8.5)
ax.set_ylabel('MSE Loss', fontsize=8.5)
ax.legend(fontsize=8)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_17.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 17: fig_17.png")

# Hình 18: Giá đóng cửa thật và dự đoán – PyTorch AAPL
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(res_pt_aapl['actual'], label='Giá thật (Actual Close)', color='#1A202C', lw=1.8)
ax.plot(res_pt_aapl['preds'], label='Dự đoán PyTorch BasicRNN', color='#3182CE', lw=1.5, linestyle='--')
ax.set_title('GIÁ ĐÓNG CỬA THẬT VÀ DỰ ĐOÁN – PYTORCH AAPL', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Phiên kiểm thử (Test Step)', fontsize=8.5)
ax.set_ylabel('Giá cổ phiếu (USD)', fontsize=8.5)
ax.legend(fontsize=8)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_18.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 18: fig_18.png")

# Hình 19: Sai số dự đoán – PyTorch AAPL
fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=150)
ax.plot(res_pt_aapl['residuals'], color='#3182CE', lw=1.2)
ax.axhline(0, color='gray', linestyle='--', alpha=0.7)
ax.set_title('SAI SỐ DỰ ĐOÁN – PYTORCH AAPL', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Test Step', fontsize=8.5)
ax.set_ylabel('Sai số giá (USD)', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_19.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 19: fig_19.png")

# Hình 20: Loss train/validation của Keras trên Customer Behavior
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=150)
ax.plot(res_ke_cust['train_loss'], label='Train Loss', color='#2B6CB0', lw=1.5)
ax.plot(res_ke_cust['val_loss'], label='Validation Loss', color='#DD6B20', lw=1.5, linestyle='--')
ax.set_title('LOSS TRAIN/VALIDATION CỦA KERAS TRÊN CUSTOMER BEHAVIOR', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Epoch', fontsize=8.5)
ax.set_ylabel('MSE Loss', fontsize=8.5)
ax.legend(fontsize=8)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_20.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 20: fig_20.png")

# Hình 21: Doanh thu thật và dự đoán – Keras Customer Behavior
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(res_ke_cust['actual'], label='Doanh thu thật (Actual)', color='#1A202C', lw=1.8)
ax.plot(res_ke_cust['preds'], label='Dự đoán Keras SimpleRNN', color='#DD6B20', lw=1.5, linestyle='--')
ax.set_title('DOANH THU THẬT VÀ DỰ ĐOÁN – KERAS CUSTOMER BEHAVIOR', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Test Step', fontsize=8.5)
ax.set_ylabel('Doanh thu', fontsize=8.5)
ax.legend(fontsize=8)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_21.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 21: fig_21.png")

# Hình 22: Sai số dự đoán – Keras Customer Behavior
fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=150)
ax.plot(res_ke_cust['residuals'], color='#DD6B20', marker='s', markersize=3, lw=1.2)
ax.axhline(0, color='gray', linestyle='--', alpha=0.7)
ax.set_title('SAI SỐ DỰ ĐOÁN – KERAS CUSTOMER BEHAVIOR', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Test Step', fontsize=8.5)
ax.set_ylabel('Sai số Doanh thu', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_22.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 22: fig_22.png")

# Hình 23: Loss train/validation của Keras trên AAPL
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=150)
ax.plot(res_ke_aapl['train_loss'], label='Train Loss', color='#2B6CB0', lw=1.5)
ax.plot(res_ke_aapl['val_loss'], label='Validation Loss', color='#DD6B20', lw=1.5, linestyle='--')
ax.set_title('LOSS TRAIN/VALIDATION CỦA KERAS TRÊN AAPL STOCK', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Epoch', fontsize=8.5)
ax.set_ylabel('MSE Loss', fontsize=8.5)
ax.legend(fontsize=8)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_23.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 23: fig_23.png")

# Hình 24: Giá AAPL thật và dự đoán – Keras
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=150)
ax.plot(res_ke_aapl['actual'], label='Giá thật (Actual Close)', color='#1A202C', lw=1.8)
ax.plot(res_ke_aapl['preds'], label='Dự đoán Keras SimpleRNN', color='#DD6B20', lw=1.5, linestyle='--')
ax.set_title('GIÁ AAPL THẬT VÀ DỰ ĐOÁN – KERAS', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Phiên kiểm thử (Test Step)', fontsize=8.5)
ax.set_ylabel('Giá cổ phiếu (USD)', fontsize=8.5)
ax.legend(fontsize=8)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_24.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 24: fig_24.png")

# Hình 25: Sai số dự đoán AAPL – Keras
fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=150)
ax.plot(res_ke_aapl['residuals'], color='#DD6B20', lw=1.2)
ax.axhline(0, color='gray', linestyle='--', alpha=0.7)
ax.set_title('SAI SỐ DỰ ĐOÁN AAPL – KERAS', fontsize=10, fontweight='bold', color='#1A365D')
ax.set_xlabel('Test Step', fontsize=8.5)
ax.set_ylabel('Sai số giá (USD)', fontsize=8.5)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_25.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 25: fig_25.png")

# Hình 26: So sánh RMSE của bốn thí nghiệm
fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.2), dpi=150)
# Customer RMSE
axes[0].bar(['PyTorch', 'Keras'], [res_pt_cust['rmse'], res_ke_cust['rmse']], color=['#3182CE', '#DD6B20'], width=0.55)
axes[0].set_title('Customer Behavior - RMSE', fontsize=10, fontweight='bold')
axes[0].set_ylabel('RMSE (Doanh thu)', fontsize=8.5)
for i, v in enumerate([res_pt_cust['rmse'], res_ke_cust['rmse']]):
    axes[0].text(i, v * 1.02, f"{v:,.1f}", ha='center', fontsize=8.5, fontweight='bold')
axes[0].grid(axis='y', linestyle=':', alpha=0.6)

# AAPL RMSE
axes[1].bar(['PyTorch', 'Keras'], [res_pt_aapl['rmse'], res_ke_aapl['rmse']], color=['#3182CE', '#DD6B20'], width=0.55)
axes[1].set_title('AAPL Stock - RMSE', fontsize=10, fontweight='bold')
axes[1].set_ylabel('RMSE (USD)', fontsize=8.5)
for i, v in enumerate([res_pt_aapl['rmse'], res_ke_aapl['rmse']]):
    axes[1].text(i, v * 1.02, f"{v:.2f}", ha='center', fontsize=8.5, fontweight='bold')
axes[1].grid(axis='y', linestyle=':', alpha=0.6)

plt.suptitle('HÌNH 26. SO SÁNH RMSE CỦA BỐN THÍ NGHIỆM', fontsize=11, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_26.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 26: fig_26.png")

# Hình 27: So sánh R² của bốn thí nghiệm
fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.2), dpi=150)
axes[0].bar(['PyTorch', 'Keras'], [res_pt_cust['r2'], res_ke_cust['r2']], color=['#3182CE', '#DD6B20'], width=0.55)
axes[0].set_title('Customer Behavior - R²', fontsize=10, fontweight='bold')
axes[0].set_ylabel('Hệ số R²', fontsize=8.5)
axes[0].axhline(0, color='black', lw=0.8)
for i, v in enumerate([res_pt_cust['r2'], res_ke_cust['r2']]):
    axes[0].text(i, v - 0.08 if v < 0 else v + 0.03, f"{v:.4f}", ha='center', fontsize=8.5, fontweight='bold')
axes[0].grid(axis='y', linestyle=':', alpha=0.6)

axes[1].bar(['PyTorch', 'Keras'], [res_pt_aapl['r2'], res_ke_aapl['r2']], color=['#3182CE', '#DD6B20'], width=0.55)
axes[1].set_title('AAPL Stock - R²', fontsize=10, fontweight='bold')
axes[1].set_ylabel('Hệ số R²', fontsize=8.5)
axes[1].axhline(0, color='black', lw=0.8)
for i, v in enumerate([res_pt_aapl['r2'], res_ke_aapl['r2']]):
    axes[1].text(i, v - 0.08 if v < 0 else v + 0.03, f"{v:.4f}", ha='center', fontsize=8.5, fontweight='bold')
axes[1].grid(axis='y', linestyle=':', alpha=0.6)

plt.suptitle('HÌNH 27. SO SÁNH R² CỦA BỐN THÍ NGHIỆM', fontsize=11, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_27.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 27: fig_27.png")

# Hình 28: Hướng phát triển từ Basic RNN đến mô hình nâng cao
fig, ax = plt.subplots(figsize=(10.5, 4.0), dpi=150)
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)

evo_steps = [
    (1.5, 1.5, "BASIC RNN (M1)\n• 1 trạng thái ẩn hₜ\n• Phụ thuộc ngắn hạn\n• Bị Vanishing Gradient", "#E2E8F0", "#718096"),
    (4.0, 1.5, "LSTM / GRU (M2)\n• Cell State Cₜ (Cao tốc)\n• Gating fₜ, iₜ, oₜ / rₜ, zₜ\n• Nhớ dài hạn, ổn định", "#BEE3F8", "#3182CE"),
    (6.5, 1.5, "SEQ2SEQ & ATTN (M3)\n• Encoder - Decoder\n• Multi-step forecasting\n• Attention cơ chế tập trung", "#FEFCBF", "#D69E2E"),
    (9.0, 1.5, "TRANSFORMER (M4)\n• Self-Attention đa đầu\n• Temporal Fusion Trans\n• Song song hóa hoàn toàn", "#C6F6D5", "#38A169")
]

for x, y, text, bg, border in evo_steps:
    ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=bg, edgecolor=border, lw=1.5))

for i in range(len(evo_steps) - 1):
    ax.annotate('', xy=(evo_steps[i+1][0] - 1.1, 1.5), xytext=(evo_steps[i][0] + 1.1, 1.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='#2B6CB0'))

ax.set_title("HÌNH 28. HƯỚNG PHÁT TRIỂN TỪ BASIC RNN ĐẾN MÔ HÌNH NÂNG CAO", fontsize=11, fontweight='bold', color='#1A365D')
plt.tight_layout()
plt.savefig('ass6_experiments/plots_v2/fig_28.png', bbox_inches='tight')
plt.close()
print("[OK] Hình 28: fig_28.png")

# Lưu kết quả số liệu JSON
metrics_save = {
    'Customer_Behavior': {
        'PyTorch': {
            'mae': float(res_pt_cust['mae']),
            'mse': float(res_pt_cust['mse']),
            'rmse': float(res_pt_cust['rmse']),
            'r2': float(res_pt_cust['r2']),
            'time': float(res_pt_cust['train_time'])
        },
        'Keras': {
            'mae': float(res_ke_cust['mae']),
            'mse': float(res_ke_cust['mse']),
            'rmse': float(res_ke_cust['rmse']),
            'r2': float(res_ke_cust['r2']),
            'time': float(res_ke_cust['train_time'])
        }
    },
    'AAPL_Stock': {
        'PyTorch': {
            'mae': float(res_pt_aapl['mae']),
            'mse': float(res_pt_aapl['mse']),
            'rmse': float(res_pt_aapl['rmse']),
            'r2': float(res_pt_aapl['r2']),
            'time': float(res_pt_aapl['train_time'])
        },
        'Keras': {
            'mae': float(res_ke_aapl['mae']),
            'mse': float(res_ke_aapl['mse']),
            'rmse': float(res_ke_aapl['rmse']),
            'r2': float(res_ke_aapl['r2']),
            'time': float(res_ke_aapl['train_time'])
        }
    }
}

with open('ass6_experiments/artifacts/a06_v2_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(metrics_save, f, indent=4)
print("\n[+] ĐÃ LƯU TOÀN BỘ SỐ LIỆU VÀ XUẤT 28 HÌNH VẼ THỰC NGHIỆM V2 THÀNH CÔNG!")
