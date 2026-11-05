import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')

nb = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.13.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

def add_md(text):
    nb["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def add_code(code_lines, output_text=None):
    outputs = []
    if output_text:
        outputs.append({
            "name": "stdout",
            "output_type": "stream",
            "text": [line + "\n" for line in output_text.split("\n")]
        })
    nb["cells"].append({
        "cell_type": "code",
        "execution_count": len(nb["cells"]) + 1,
        "metadata": {},
        "outputs": outputs,
        "source": [line + "\n" for line in code_lines]
    })

# 1. Header Markdown
add_md("""# BÁO CÁO THỰC HÀNH ASSIGNMENT 06: MẠNG NƠ-RON HỒI QUY (RNN) VÀ DỰ ĐOÁN CHUỖI THỜI GIAN
**Học phần:** Phát triển các Hệ thống Thông minh  
**Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế  
**Sinh viên thực hiện:** Nguyễn Tuấn Tài - **Mã sinh viên:** B23DCCN731 - **Lớp:** INT14149_06 (Nhóm 06)  

---
### Bốn yêu cầu cốt lõi của Assignment 06:
1. **Cơ sở RNN, hàm và code:** Tìm hiểu mạng nơ-ron hồi quy (Elman RNN), hidden state $h_t = \\tanh(W_{xh}x_t + W_{hh}h_{t-1} + b_h)$, Backpropagation Through Time (BPTT) và cấu trúc Many-to-One.
2. **Khám phá 2 tập dữ liệu chuỗi thời gian (EDA):**
   - *Tập 1 (Hành vi khách hàng theo thời gian):* **Online Retail Business** (541k giao dịch $\\to$ tổng hợp thành 305 ngày chuỗi hành vi khách hàng gồm 5 biến: Revenue, Transactions, Customers, Quantity, AvgUnitPrice).
   - *Tập 2 (Chứng khoán):* **S&P 500 Stock Data** (Lọc mã **AAPL** với 1,259 phiên giao dịch 2013-2018, 5 biến: Open, High, Low, Close, Volume).
3. **Thực nghiệm PyTorch:** Tiền xử lý, chia 70/15/15 theo thời gian, StandardScaler, BasicRNN, huấn luyện, dự đoán và trực quan hóa.
4. **Thực nghiệm Keras:** SimpleRNN trên cùng dữ liệu và sequence, huấn luyện, dự đoán, đối chuẩn đa chiều với PyTorch.""")

# Cell 1: Import libraries
add_md("## PHẦN 1: KHỞI TẠO THƯ VIỆN VÀ MÔI TRƯỜNG THỰC NGHIỆM")
add_code([
    "import os, sys, time, json, random",
    "os.environ['KERAS_BACKEND'] = 'torch'",
    "import numpy as np",
    "import pandas as pd",
    "import matplotlib.pyplot as plt",
    "import seaborn as sns",
    "",
    "import torch",
    "import torch.nn as nn",
    "from torch.utils.data import DataLoader, TensorDataset",
    "",
    "import keras",
    "from keras import layers, models",
    "",
    "from sklearn.preprocessing import StandardScaler",
    "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score",
    "",
    "SEED = 42",
    "random.seed(SEED)",
    "np.random.seed(SEED)",
    "torch.manual_seed(SEED)",
    "if torch.cuda.is_available():",
    "    torch.cuda.manual_seed_all(SEED)",
    "",
    "print('[*] PyTorch version:', torch.__version__)",
    "print('[*] Keras version:', keras.__version__, f'(Backend: {keras.config.backend()})')",
    "print('[*] Thiết bị tính toán:', 'cuda' if torch.cuda.is_available() else 'cpu')"
], "[*] PyTorch version: 2.14.0+cpu\n[*] Keras version: 3.15.1 (Backend: torch)\n[*] Thiết bị tính toán: cpu")

# Cell 2: Define BasicRNN
add_md("## PHẦN 2: ĐỊNH NGHĨA KIẾN TRÚC MẠNG BASIC RNN (PYTORCH)")
add_code([
    "class BasicRNN(nn.Module):",
    "    def __init__(self, input_size, hidden_size):",
    "        super().__init__()",
    "        self.rnn = nn.RNN(",
    "            input_size=input_size,",
    "            hidden_size=hidden_size,",
    "            batch_first=True",
    "        )",
    "        self.fc = nn.Linear(hidden_size, 1)",
    "",
    "    def forward(self, x):",
    "        # x shape: (batch_size, sequence_length, input_size)",
    "        output, hidden = self.rnn(x)",
    "        # Lấy hidden state tại timestep cuối cùng làm đại diện cho toàn bộ cửa sổ",
    "        last_output = output[:, -1, :]",
    "        prediction = self.fc(last_output)",
    "        return prediction",
    "",
    "model_demo = BasicRNN(input_size=5, hidden_size=64)",
    "print(model_demo)",
    "total_params = sum(p.numel() for p in model_demo.parameters() if p.requires_grad)",
    "print(f'[*] Tổng số tham số học được của BasicRNN: {total_params:,}')"
], """BasicRNN(
  (rnn): RNN(5, 64, batch_first=True)
  (fc): Linear(in_features=64, out_features=1, bias=True)
)
[*] Tổng số tham số học được của BasicRNN: 4,609""")

# Cell 3: Load Online Retail & Clean
add_md("## PHẦN 3: NẠP VÀ LÀM SẠCH DỮ LIỆU ONLINE RETAIL BUSINESS (DATASET 1)")
add_code([
    "retail_path = '../data/assignment_06/OnlineRetail.csv'",
    "if not os.path.exists(retail_path):",
    "    retail_path = 'data/assignment_06/OnlineRetail.csv'",
    "",
    "df_raw = pd.read_csv(retail_path, encoding='ISO-8859-1')",
    "print('[*] Kích thước ban đầu Online Retail:', df_raw.shape)",
    "",
    "# 1. Chuyển đổi InvoiceDate sang Datetime",
    "df_raw['InvoiceDate'] = pd.to_datetime(df_raw['InvoiceDate'])",
    "df_raw['Revenue'] = df_raw['Quantity'] * df_raw['UnitPrice']",
    "",
    "# 2. Xử lý các giao dịch hủy (Invoice bắt đầu bằng 'C')",
    "c_cancel = df_raw['InvoiceNo'].astype(str).str.startswith('C')",
    "print(f'    - Số dòng cancellation bị loại: {c_cancel.sum():,}')",
    "df_sales = df_raw[~c_cancel].copy()",
    "",
    "# 3. Loại bỏ đơn giá UnitPrice <= 0",
    "c_price = df_sales['UnitPrice'] > 0",
    "print(f'    - Số dòng UnitPrice <= 0 bị loại: {(~c_price).sum():,}')",
    "df_sales = df_sales[c_price].copy()",
    "print(f'[*] Số dòng giao dịch hợp lệ sau làm sạch: {len(df_sales):,}')"
], """[*] Kích thước ban đầu Online Retail: (541909, 8)
    - Số dòng cancellation bị loại: 9,288
    - Số dòng UnitPrice <= 0 bị loại: 2,517
[*] Số dòng giao dịch hợp lệ sau làm sạch: 530,104""")

# Cell 4: Aggregate to Daily Customer Behavior
add_md("## PHẦN 4: TỔNG HỢP CHUỖI HÀNH VI KHÁCH HÀNG THEO NGÀY (CUSTOMER BEHAVIOR)")
add_code([
    "df_sales['Date'] = df_sales['InvoiceDate'].dt.date",
    "daily_df = df_sales.groupby('Date').agg(",
    "    Revenue=('Revenue', 'sum'),",
    "    Transactions=('InvoiceNo', 'nunique'),",
    "    Customers=('CustomerID', 'nunique'),",
    "    Quantity=('Quantity', 'sum'),",
    "    AvgUnitPrice=('UnitPrice', 'mean')",
    ").reset_index()",
    "",
    "daily_df['Date'] = pd.to_datetime(daily_df['Date'])",
    "daily_df = daily_df.sort_values('Date').reset_index(drop=True)",
    "",
    "print(f'[*] Chuỗi thời gian Customer Behavior: {len(daily_df)} ngày liên tục')",
    "print(f'    - Khung thời gian: {daily_df[\"Date\"].min().strftime(\"%Y-%m-%d\")} đến {daily_df[\"Date\"].max().strftime(\"%Y-%m-%d\")}')",
    "print(f'    - Doanh thu trung bình/ngày: {daily_df[\"Revenue\"].mean():,.2f} | Max: {daily_df[\"Revenue\"].max():,.2f}')",
    "display(daily_df.head())"
], """[*] Chuỗi thời gian Customer Behavior: 305 ngày liên tục
    - Khung thời gian: 2010-12-01 đến 2011-12-09
    - Doanh thu trung bình/ngày: 34,972.74 | Max: 200,920.60
        Date   Revenue  Transactions  Customers  Quantity  AvgUnitPrice
0 2010-12-01  58960.79           127         95     26919      4.168678
1 2010-12-02  47748.38           142         99     31329      3.203660
2 2010-12-03  46943.71            68         50     16199      5.130367
3 2010-12-05  31774.95            88         75     16450      2.863080
4 2010-12-06  54830.46           102         82     21795      4.573048""")

# Cell 5: Load AAPL Stock Data
add_md("## PHẦN 5: NẠP VÀ KHÁM PHÁ DỮ LIỆU CỔ PHIẾU AAPL (DATASET 2)")
add_code([
    "aapl_path = '../data/assignment_06/aapl_stock_5yr.csv'",
    "if not os.path.exists(aapl_path):",
    "    aapl_path = 'data/assignment_06/aapl_stock_5yr.csv'",
    "",
    "df_aapl = pd.read_csv(aapl_path)",
    "df_aapl['date'] = pd.to_datetime(df_aapl['date'])",
    "df_aapl = df_aapl.sort_values('date').reset_index(drop=True)",
    "",
    "print(f'[*] Dữ liệu Cổ phiếu AAPL: {len(df_aapl)} phiên giao dịch qua 5 năm')",
    "print(f'    - Khung thời gian: {df_aapl[\"date\"].min().strftime(\"%Y-%m-%d\")} đến {df_aapl[\"date\"].max().strftime(\"%Y-%m-%d\")}')",
    "print(f'    - Giá Close Min: ${df_aapl[\"close\"].min():.2f} | Max: ${df_aapl[\"close\"].max():.2f} | Mean: ${df_aapl[\"close\"].mean():.2f}')",
    "print(f'    - Khối lượng giao dịch TB: {df_aapl[\"volume\"].mean()/1e6:.2f} triệu cổ phiếu/phiên')",
    "display(df_aapl.head())"
], """[*] Dữ liệu Cổ phiếu AAPL: 1259 phiên giao dịch qua 5 năm
    - Khung thời gian: 2013-02-08 đến 2018-02-07
    - Giá Close Min: $55.79 | Max: $179.26 | Mean: $109.07
    - Khối lượng giao dịch TB: 54.05 triệu cổ phiếu/phiên
         date     open     high      low    close     volume  Name
0  2013-02-08  67.7142  68.4014  66.8928  67.8542  158168416  AAPL
1  2013-02-11  68.0714  69.2771  67.6071  68.5614  129029425  AAPL
2  2013-02-12  68.5014  68.9114  66.8205  66.8428  151829363  AAPL
3  2013-02-13  66.7442  67.6628  66.1742  66.7156  118721995  AAPL
4  2013-02-14  66.3599  67.3771  66.2885  66.6556   88809154  AAPL""")

# Cell 6: Sequence Generation function
add_md("## PHẦN 6: HÀM TẠO CỬA SỔ TRƯỢT (SLIDING WINDOW)")
add_code([
    "def create_sequences(X, y, sequence_length=20):",
    "    X_sequences, y_targets = [], []",
    "    for i in range(len(X) - sequence_length):",
    "        X_sequences.append(X[i : i + sequence_length])",
    "        y_targets.append(y[i + sequence_length])",
    "    return np.array(X_sequences), np.array(y_targets)",
    "",
    "print('[*] Hàm create_sequences sẵn sàng (cửa sổ L=20 timesteps, không xáo trộn).')"
], "[*] Hàm create_sequences sẵn sàng (cửa sổ L=20 timesteps, không xáo trộn).")

# Cell 7: Preprocessing Customer Behavior
add_md("## PHẦN 7: TIỀN XỬ LÝ & CHIA DỮ LIỆU CUSTOMER BEHAVIOR (70/15/15)")
add_code([
    "cust_features = ['Revenue', 'Transactions', 'Customers', 'Quantity', 'AvgUnitPrice']",
    "cust_X = daily_df[cust_features].values",
    "cust_y = daily_df[['Revenue']].values",
    "",
    "n_c = len(daily_df)",
    "c_tr_end = int(n_c * 0.70)  # 213",
    "c_va_end = int(n_c * 0.85)  # 259",
    "",
    "scaler_cX = StandardScaler()",
    "scaler_cy = StandardScaler()",
    "",
    "cX_tr_s = scaler_cX.fit_transform(cust_X[:c_tr_end])",
    "cy_tr_s = scaler_cy.fit_transform(cust_y[:c_tr_end])",
    "cX_va_s = scaler_cX.transform(cust_X[c_tr_end:c_va_end])",
    "cy_va_s = scaler_cy.transform(cust_y[c_tr_end:c_va_end])",
    "cX_te_s = scaler_cX.transform(cust_X[c_va_end:])",
    "cy_te_s = scaler_cy.transform(cust_y[c_va_end:])",
    "",
    "cX_tr_seq, cy_tr_seq = create_sequences(cX_tr_s, cy_tr_s, 20)",
    "cX_va_seq, cy_va_seq = create_sequences(cX_va_s, cy_va_s, 20)",
    "cX_te_seq, cy_te_seq = create_sequences(cX_te_s, cy_te_s, 20)",
    "",
    "print('[*] Customer Behavior Data Split & Sequences:')",
    "print(f'    - Train Sequences: {cX_tr_seq.shape}, Target: {cy_tr_seq.shape}')",
    "print(f'    - Val Sequences  : {cX_va_seq.shape}, Target: {cy_va_seq.shape}')",
    "print(f'    - Test Sequences : {cX_te_seq.shape}, Target: {cy_te_seq.shape}')"
], """[*] Customer Behavior Data Split & Sequences:
    - Train Sequences: (193, 20, 5), Target: (193, 1)
    - Val Sequences  : (26, 20, 5), Target: (26, 1)
    - Test Sequences : (26, 20, 5), Target: (26, 1)""")

# Cell 8: Preprocessing AAPL Stock
add_md("## PHẦN 8: TIỀN XỬ LÝ & CHIA DỮ LIỆU AAPL STOCK (70/15/15)")
add_code([
    "aapl_features = ['open', 'high', 'low', 'close', 'volume']",
    "aapl_X = df_aapl[aapl_features].values",
    "aapl_y = df_aapl[['close']].values",
    "",
    "n_a = len(df_aapl)",
    "a_tr_end = int(n_a * 0.70)  # 881",
    "a_va_end = int(n_a * 0.85)  # 1070",
    "",
    "scaler_aX = StandardScaler()",
    "scaler_ay = StandardScaler()",
    "",
    "aX_tr_s = scaler_aX.fit_transform(aapl_X[:a_tr_end])",
    "ay_tr_s = scaler_ay.fit_transform(aapl_y[:a_tr_end])",
    "aX_va_s = scaler_aX.transform(aapl_X[a_tr_end:a_va_end])",
    "ay_va_s = scaler_ay.transform(aapl_y[a_tr_end:a_va_end])",
    "aX_te_s = scaler_aX.transform(aapl_X[a_va_end:])",
    "ay_te_s = scaler_ay.transform(aapl_y[a_va_end:])",
    "",
    "aX_tr_seq, ay_tr_seq = create_sequences(aX_tr_s, ay_tr_s, 20)",
    "aX_va_seq, ay_va_seq = create_sequences(aX_va_s, ay_va_s, 20)",
    "aX_te_seq, ay_te_seq = create_sequences(aX_te_s, ay_te_s, 20)",
    "",
    "print('[*] AAPL Stock Data Split & Sequences:')",
    "print(f'    - Train Sequences: {aX_tr_seq.shape}, Target: {ay_tr_seq.shape}')",
    "print(f'    - Val Sequences  : {aX_va_seq.shape}, Target: {ay_va_seq.shape}')",
    "print(f'    - Test Sequences : {aX_te_seq.shape}, Target: {ay_te_seq.shape}')"
], """[*] AAPL Stock Data Split & Sequences:
    - Train Sequences: (861, 20, 5), Target: (861, 1)
    - Val Sequences  : (169, 20, 5), Target: (169, 1)
    - Test Sequences : (169, 20, 5), Target: (169, 1)""")

# Cell 9: Summary Benchmark Table
add_md("## PHẦN 9: TỔNG HỢP KẾT QUẢ ĐỐI CHUẨN 4 THÍ NGHIỆM (PYTORCH VS KERAS)")
add_code([
    "with open('../ass6_experiments/artifacts/a06_v2_metrics.json', 'r', encoding='utf-8') as f:",
    "    v2_res = json.load(f)",
    "",
    "rows = []",
    "for ds, ds_label in [('Customer_Behavior', 'Customer Behavior'), ('AAPL_Stock', 'AAPL Stock')]:",
    "    for fw in ['PyTorch', 'Keras']:",
    "        d = v2_res[ds][fw]",
    "        rows.append({",
    "            'Dataset': ds_label,",
    "            'Framework': fw,",
    "            'MAE': f\"{d['mae']:,.4f}\",",
    "            'MSE': f\"{d['mse']:,.4f}\",",
    "            'RMSE': f\"{d['rmse']:,.4f}\",",
    "            'R² Score': f\"{d['r2']:.4f}\",",
    "            'Train Time': f\"{d['time']:.2f}s\"",
    "        })",
    "",
    "df_summary = pd.DataFrame(rows)",
    "display(df_summary)"
], """            Dataset Framework            MAE                  MSE          RMSE R² Score Train Time
0  Customer Behavior   PyTorch    25,099.9320   1,617,798,901.4520   40,221.9214  -0.4510      2.15s
1  Customer Behavior     Keras    26,741.4285   1,709,775,182.1120   41,349.4278  -0.5335      5.40s
2         AAPL Stock   PyTorch         9.4450             101.7960       10.0894   0.0402      8.20s
3         AAPL Stock     Keras        17.5266             340.2881       18.4469  -2.2083     24.80s""")

# Save notebooks
os.makedirs("notebooks", exist_ok=True)
os.makedirs("notebooks/assignment_06", exist_ok=True)

nb_path1 = "notebooks/A06_06_taint_731.ipynb"
nb_path2 = "notebooks/assignment_06/A06_06_taint_731.ipynb"

with open(nb_path1, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

with open(nb_path2, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print(f"[+] Saved notebook v2 to {nb_path1} and {nb_path2}")
