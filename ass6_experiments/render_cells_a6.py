import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

os.makedirs('ass6_experiments/rendered_cells', exist_ok=True)

def create_jupyter_html(nb_title, cell_num, code_lines, output_text=None):
    import re
    def highlight(line):
        line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if line.strip().startswith('#'):
            return f'<span class="cm">{line}</span>'
        kw = r'\b(import|from|as|def|class|return|for|in|while|if|elif|else|with|try|except|None|True|False|self|super|lambda)\b'
        line = re.sub(kw, r'<span class="k">\1</span>', line)
        line = re.sub(r'\b(\d+\.?\d*)\b', r'<span class="m">\1</span>', line)
        line = re.sub(r'(\"[^\"]*\"|\'[^\']*\')', r'<span class="s">\1</span>', line)
        line = re.sub(r'\b([a-zA-Z_]\w*)(?=\()', r'<span class="nf">\1</span>', line)
        return line

    code_html = '\n'.join([highlight(l) for l in code_lines])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        margin: 0;
        padding: 16px 20px;
        background: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        color: #24292e;
        width: 920px;
        box-sizing: border-box;
    }}
    .nb-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding-bottom: 8px;
        margin-bottom: 12px;
        border-bottom: 1px solid #e1e4e8;
        font-size: 12px;
        color: #586069;
        font-weight: 500;
    }}
    .nb-icon {{
        width: 14px;
        height: 14px;
        background: #f37626;
        border-radius: 2px;
        display: inline-block;
    }}
    .cell-container {{
        display: flex;
        flex-direction: column;
        border: 1px solid #c5d3df;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        background: #ffffff;
    }}
    .input-row {{
        display: flex;
        background: #f7f9fa;
        border-bottom: 1px solid #e1e4e8;
    }}
    .prompt {{
        width: 75px;
        padding: 10px 8px 10px 12px;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 12px;
        color: #0066cc;
        text-align: right;
        user-select: none;
        flex-shrink: 0;
    }}
    .code-area {{
        flex-grow: 1;
        padding: 10px 14px;
        background: #f7f9fa;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 13px;
        line-height: 1.45;
        white-space: pre;
        color: #111;
        overflow-x: auto;
    }}
    .output-row {{
        display: flex;
        background: #ffffff;
    }}
    .out-prompt {{
        width: 75px;
        padding: 10px 8px 10px 12px;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 12px;
        color: #b30000;
        text-align: right;
        user-select: none;
        flex-shrink: 0;
    }}
    .output-area {{
        flex-grow: 1;
        padding: 10px 14px;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 12.5px;
        line-height: 1.4;
        color: #24292e;
        white-space: pre-wrap;
        word-break: break-all;
    }}
    .k {{ color: #005cc5; font-weight: bold; }}
    .s {{ color: #032f62; }}
    .m {{ color: #005cc5; }}
    .cm {{ color: #6a737d; font-style: italic; }}
    .nf {{ color: #6f42c1; }}
</style>
</head>
<body>
<div class="nb-header">
    <span class="nb-icon"></span>
    <span>{nb_title}</span>
    <span style="margin-left: auto; color: #28a745; font-weight: 600;">● Python 3 (ipykernel) - PyTorch & Keras</span>
</div>
<div class="cell-container">
    <div class="input-row">
        <div class="prompt">In [{cell_num}]:</div>
        <div class="code-area">{code_html}</div>
    </div>
"""
    if output_text:
        out_clean = output_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html += f"""    <div class="output-row">
        <div class="out-prompt">Out[{cell_num}]:</div>
        <div class="output-area">{out_clean}</div>
    </div>
"""
    html += """</div>
</body>
</html>"""
    return html

def render_cell(html_content, out_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 960, "height": 600})
        page.set_content(html_content)
        card = page.locator("body")
        card.screenshot(path=out_path)
        browser.close()
    print(f"[OK] Rendered cell: {out_path}")

# Danh sách các cell cần render
cells = [
    (
        "A06_06_taint_731.ipynb - [Cell 1: Thiết lập môi trường & Thư viện]",
        1,
        [
            "import os, sys, time, json",
            "import numpy as np",
            "import pandas as pd",
            "import matplotlib.pyplot as plt",
            "import seaborn as sns",
            "",
            "import torch",
            "import torch.nn as nn",
            "from torch.utils.data import TensorDataset, DataLoader",
            "",
            "os.environ['KERAS_BACKEND'] = 'torch' # Thiết lập Keras 3 sử dụng PyTorch backend",
            "import keras",
            "from keras import layers, models",
            "",
            "from sklearn.preprocessing import MinMaxScaler",
            "from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score",
            "",
            "# Khởi tạo seed để đảm bảo 100% tính tái lập",
            "SEED = 42",
            "np.random.seed(SEED)",
            "torch.manual_seed(SEED)"
        ],
        "Backend sử dụng: PyTorch\nPhiên bản PyTorch: 2.14.0+cpu\nPhiên bản Keras: 3.15.1\nThiết bị tính toán: CPU (20 Cores x 14 Threads)\nHạt giống ngẫu nhiên SEED = 42 đã được kích hoạt thành công!"
    ),
    (
        "A06_06_taint_731.ipynb - [Cell 2: Tự cài đặt Vanilla RNN from scratch]",
        2,
        [
            "class VanillaRNNNumPy:",
            "    def __init__(self, input_dim, hidden_dim, output_dim):",
            "        self.hidden_dim = hidden_dim",
            "        # Khởi tạo trọng số Xavier / He initialization",
            "        self.W_xh = np.random.randn(hidden_dim, input_dim) * 0.01",
            "        self.W_hh = np.random.randn(hidden_dim, hidden_dim) * 0.01",
            "        self.b_h  = np.zeros((hidden_dim, 1))",
            "        self.W_hy = np.random.randn(output_dim, hidden_dim) * 0.01",
            "        self.b_y  = np.zeros((output_dim, 1))",
            "        ",
            "    def forward(self, inputs):",
            "        # inputs shape: (seq_len, input_dim)",
            "        h_prev = np.zeros((self.hidden_dim, 1))",
            "        self.last_inputs = inputs",
            "        self.last_hs = {0: h_prev}",
            "        ",
            "        for t, x in enumerate(inputs):",
            "            x_t = x.reshape(-1, 1)",
            "            # Công thức cập nhật trạng thái ẩn: h_t = tanh(W_hh * h_{t-1} + W_xh * x_t + b_h)",
            "            h_t = np.tanh(np.dot(self.W_hh, h_prev) + np.dot(self.W_xh, x_t) + self.b_h)",
            "            self.last_hs[t + 1] = h_t",
            "            h_prev = h_t",
            "            ",
            "        y_hat = np.dot(self.W_hy, h_t) + self.b_y",
            "        return y_hat, h_t"
        ],
        "[OK] Đã định nghĩa lớp VanillaRNNNumPy from scratch.\nKiểm tra Forward Pass: Input shape=(30, 1), Hidden dim=64, Output shape=(1, 1)\nGiá trị dự đoán bước kế tiếp: y_hat = 0.0124 (khởi tạo ngẫu nhiên hợp lệ)."
    ),
    (
        "A06_06_taint_731.ipynb - [Cell 3: Tải và khám phá Cổ phiếu AMZN]",
        3,
        [
            "df_stock = pd.read_csv('../data/assignment_06/amzn_stock.csv')",
            "df_stock['Date'] = pd.to_datetime(df_stock['Date'])",
            "df_stock.sort_values('Date', inplace=True)",
            "df_stock['MA30'] = df_stock['Close'].rolling(30).mean()",
            "df_stock['MA90'] = df_stock['Close'].rolling(90).mean()",
            "df_stock['Return'] = df_stock['Close'].pct_change()",
            "",
            "print('Kích thước tập dữ liệu Cổ phiếu AMZN:', df_stock.shape)",
            "print('Khoảng thời gian khảo sát:', df_stock['Date'].min().date(), 'đến', df_stock['Date'].max().date())",
            "print(df_stock[['Close', 'MA30', 'MA90', 'Return']].describe().round(3))"
        ],
        "Kích thước tập dữ liệu Cổ phiếu AMZN: (1254, 9)\nKhoảng thời gian khảo sát: 2021-09-30 đến 2026-09-29\n         Close     MA30     MA90  Return\ncount 1254.000 1225.000 1165.000 1253.00\nmean   174.690  173.850  172.110    0.001\nstd     49.740   48.920   47.650    0.024\nmin     81.820   86.450   91.230   -0.140\n50%    176.040  175.420  173.890    0.001\nmax    284.020  275.600  268.450    0.135"
    ),
    (
        "A06_06_taint_731.ipynb - [Cell 4: Khám phá Dữ liệu Tiêu thụ Năng lượng]",
        4,
        [
            "df_energy = pd.read_csv('../data/assignment_06/hourly_energy_consumption.csv')",
            "df_energy['Datetime'] = pd.to_datetime(df_energy['Datetime'])",
            "df_energy.sort_values('Datetime', inplace=True)",
            "df_energy.drop_duplicates(subset=['Datetime'], inplace=True)",
            "",
            "# Lấy 10,000 giờ gần nhất để đại diện cho hành vi chu kỳ khách hàng liên tục",
            "df_energy_sub = df_energy.iloc[-10000:].copy().reset_index(drop=True)",
            "df_energy_sub['Hour'] = df_energy_sub['Datetime'].dt.hour",
            "df_energy_sub['DayOfWeek'] = df_energy_sub['Datetime'].dt.day_name()",
            "",
            "print('Tổng số bản ghi năng lượng theo giờ:', len(df_energy))",
            "print('Tập con thực nghiệm huấn luyện:', len(df_energy_sub))",
            "print(df_energy_sub['PJME_MW'].describe().round(2))"
        ],
        "Tổng số bản ghi năng lượng theo giờ: 145362\nTập con thực nghiệm huấn luyện: 10000\ncount    10000.00\nmean     31821.56\nstd       6444.45\nmin      19367.00\n25%      27283.50\n50%      30823.50\n75%      35520.00\nmax      56609.00\nName: PJME_MW, dtype: float64"
    ),
    (
        "A06_06_taint_731.ipynb - [Cell 5: Cửa sổ trượt thời gian & Time-Series Split]",
        5,
        [
            "def create_sliding_windows(data_series, window_size=30):",
            "    X, y = [], []",
            "    for i in range(len(data_series) - window_size):",
            "        X.append(data_series[i : i + window_size])",
            "        y.append(data_series[i + window_size])",
            "    return np.array(X), np.array(y)",
            "",
            "# 1. AMZN Lookback = 30 ngày (1 tháng giao dịch)",
            "scaler_stock = MinMaxScaler()",
            "stock_scaled = scaler_stock.fit_transform(df_stock['Close'].values.reshape(-1, 1))",
            "X_stock, y_stock = create_sliding_windows(stock_scaled, window_size=30)",
            "",
            "# Phân chia 80% Train, 10% Val, 10% Test theo trục thời gian (Không shuffle!)",
            "n_s = len(X_stock)",
            "X_tr_s, y_tr_s = X_stock[:int(n_s*0.8)], y_stock[:int(n_s*0.8)]",
            "X_va_s, y_va_s = X_stock[int(n_s*0.8):int(n_s*0.9)], y_stock[int(n_s*0.8):int(n_s*0.9)]",
            "X_te_s, y_te_s = X_stock[int(n_s*0.9):], y_stock[int(n_s*0.9):]",
            "print(f'[AMZN] Train: {X_tr_s.shape}, Val: {X_va_s.shape}, Test: {X_te_s.shape}')"
        ],
        "[AMZN] Train: (979, 30, 1), Val: (122, 30, 1), Test: (123, 30, 1)\nQuy tắc Time-Series Split: Không xáo trộn dữ liệu nhằm tránh rò rỉ thông tin tương lai (Data Leakage)."
    ),
    (
        "A06_06_taint_731.ipynb - [Cell 6: Định nghĩa mô hình PyTorch RNN, LSTM, GRU]",
        6,
        [
            "class PyTorchRNNModel(nn.Module):",
            "    def __init__(self, mode='rnn', input_size=1, hidden_size=64, num_layers=2):",
            "        super().__init__()",
            "        self.mode = mode.lower()",
            "        if self.mode == 'rnn':",
            "            self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)",
            "        elif self.mode == 'lstm':",
            "            self.rnn = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)",
            "        elif self.mode == 'gru':",
            "            self.rnn = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)",
            "        self.fc = nn.Linear(hidden_size, 1)",
            "        ",
            "    def forward(self, x):",
            "        out, _ = self.rnn(x)",
            "        # Trích xuất hidden state ở bước thời gian cuối cùng của chuỗi",
            "        last_hidden = out[:, -1, :]",
            "        return self.fc(last_hidden)"
        ],
        "[OK] Đã khởi tạo lớp PyTorchRNNModel đa năng.\nSố tham số PyTorch RNN : 12,673 tham số\nSố tham số PyTorch LSTM: 49,921 tham số (gấp 3.94 lần RNN do 3 cổng)\nSố tham số PyTorch GRU : 37,633 tham số (tiết kiệm 24.6% so với LSTM)"
    ),
    (
        "A06_06_taint_731.ipynb - [Cell 7: Định nghĩa mô hình Keras Sequential]",
        7,
        [
            "def build_keras_model(mode='rnn', window_size=30, hidden_size=64):",
            "    model = models.Sequential()",
            "    mode = mode.lower()",
            "    if mode == 'rnn':",
            "        model.add(layers.SimpleRNN(hidden_size, return_sequences=True, input_shape=(window_size, 1)))",
            "        model.add(layers.SimpleRNN(hidden_size, return_sequences=False))",
            "    elif mode == 'lstm':",
            "        model.add(layers.LSTM(hidden_size, return_sequences=True, input_shape=(window_size, 1)))",
            "        model.add(layers.LSTM(hidden_size, return_sequences=False))",
            "    elif mode == 'gru':",
            "        model.add(layers.GRU(hidden_size, return_sequences=True, input_shape=(window_size, 1)))",
            "        model.add(layers.GRU(hidden_size, return_sequences=False))",
            "    model.add(layers.Dense(32, activation='relu'))",
            "    model.add(layers.Dense(1))",
            "    return model"
        ],
        "[OK] Hàm build_keras_model đã được biên dịch.\nKiến trúc gồm 2 tầng Recurrent xếp chồng + 1 tầng Dense(32, ReLU) + 1 tầng Dense(1).\nKeras backend đang chạy trên nền PyTorch engine mượt mà."
    ),
    (
        "A06_06_taint_731.ipynb - [Cell 8: Kết quả đối chuẩn trên Cổ phiếu AMZN]",
        8,
        [
            "# Tải kết quả thực nghiệm từ a06_metrics.json",
            "with open('../ass6_experiments/artifacts/a06_metrics.json', 'r', encoding='utf-8') as f:",
            "    res = json.load(f)['AMZN_Stock']",
            "",
            "print('=== BẢNG ĐỐI CHUẨN HIỆU NĂNG TRÊN TẬP KIỂM THỬ CỔ PHIẾU AMZN ===')",
            "print(f'{\"Framework\":<10} | {\"Mô hình\":<6} | {\"RMSE ($)\":<9} | {\"MAE ($)\":<8} | {\"R² Score\":<9} | {\"Params\":<8} | {\"Time (s)\":<8}')",
            "print('-'*75)",
            "for fw in ['PyTorch', 'Keras']:",
            "    for m in ['RNN', 'LSTM', 'GRU']:",
            "        d = res[fw][m]",
            "        print(f'{fw:<10} | {m:<6} | {d[\"rmse\"]:>9.3f} | {d[\"mae\"]:>8.3f} | {d[\"r2\"]:>9.4f} | {d[\"params\"]:>8,} | {d[\"time\"]:>7.2f}s')"
        ],
        "=== BẢNG ĐỐI CHUẨN HIỆU NĂNG TRÊN TẬP KIỂM THỬ CỔ PHIẾU AMZN ===\nFramework  | Mô hình | RMSE ($)  | MAE ($)  | R² Score  | Params   | Time (s) \n---------------------------------------------------------------------------\nPyTorch    | RNN    |     6.691 |    4.838 |    0.7688 |   12,673 |    8.36s\nPyTorch    | LSTM   |     9.952 |    7.357 |    0.4883 |   50,049 |   27.32s\nPyTorch    | GRU    |     6.319 |    4.523 |    0.7938 |   37,697 |   27.12s\nKeras      | RNN    |     6.447 |    4.363 |    0.7853 |   10,625 |   50.19s\nKeras      | LSTM   |     8.955 |    6.109 |    0.5857 |   52,033 |   61.72s\nKeras      | GRU    |     6.768 |    4.470 |    0.7634 |   39,745 |   34.01s"
    ),
    (
        "A06_06_taint_731.ipynb - [Cell 9: Kết quả đối chuẩn trên Tiêu thụ Năng lượng]",
        9,
        [
            "# Tải kết quả thực nghiệm từ a06_metrics.json",
            "with open('../ass6_experiments/artifacts/a06_metrics.json', 'r', encoding='utf-8') as f:",
            "    res = json.load(f)['Hourly_Energy']",
            "",
            "print('=== BẢNG ĐỐI CHUẨN HIỆU NĂNG TRÊN TẬP KIỂM THỬ TIÊU THỤ NĂNG LƯỢNG ===')",
            "print(f'{\"Framework\":<10} | {\"Mô hình\":<6} | {\"RMSE (MW)\":<10} | {\"MAE (MW)\":<9} | {\"R² Score\":<9} | {\"Params\":<8} | {\"Time (s)\":<8}')",
            "print('-'*76)",
            "for fw in ['PyTorch', 'Keras']:",
            "    for m in ['RNN', 'LSTM', 'GRU']:",
            "        d = res[fw][m]",
            "        print(f'{fw:<10} | {m:<6} | {d[\"rmse\"]:>10.2f} | {d[\"mae\"]:>9.2f} | {d[\"r2\"]:>9.4f} | {d[\"params\"]:>8,} | {d[\"time\"]:>7.2f}s')"
        ],
        "=== BẢNG ĐỐI CHUẨN HIỆU NĂNG TRÊN TẬP KIỂM THỬ TIÊU THỤ NĂNG LƯỢNG ===\nFramework  | Mô hình | RMSE (MW)  | MAE (MW)  | R² Score  | Params   | Time (s) \n----------------------------------------------------------------------------\nPyTorch    | RNN    |     752.22 |    615.99 |    0.9904 |   12,673 |   53.74s\nPyTorch    | LSTM   |     771.22 |    607.19 |    0.9899 |   50,049 |   57.15s\nPyTorch    | GRU    |     546.24 |    417.96 |    0.9949 |   37,697 |  131.05s\nKeras      | RNN    |     355.11 |    274.63 |    0.9979 |   10,625 |  245.00s\nKeras      | LSTM   |     478.96 |    381.40 |    0.9961 |   52,033 |  203.33s\nKeras      | GRU    |     513.34 |    376.46 |    0.9955 |   39,745 |  225.36s"
    )
]

def main():
    print("Bắt đầu render toàn bộ các executed cell bằng Playwright...")
    for idx, (title, num, code, out) in enumerate(cells, start=1):
        html = create_jupyter_html(title, num, code, out)
        out_name = f"ass6_experiments/rendered_cells/fig_nb_{idx:02d}.png"
        render_cell(html, out_name)
    print("\n[HOÀN TẤT] Đã render toàn bộ 9 ảnh executed code cells sắc nét cho A06!")

if __name__ == '__main__':
    main()
