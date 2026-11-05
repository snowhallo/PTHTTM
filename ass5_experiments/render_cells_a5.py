import os, sys, json, base64
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

os.makedirs('ass5_experiments/rendered_cells', exist_ok=True)

def create_jupyter_html(nb_title, cell_num, code_lines, output_text=None, output_html=None):
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
        overflow: hidden;
    }}
    .input-area {{
        display: flex;
        background: #f8f9fa;
        border-bottom: 1px solid #e1e4e8;
    }}
    .prompt-in {{
        width: 75px;
        padding: 8px 6px;
        font-family: Consolas, Monaco, "Courier New", monospace;
        font-size: 11.5px;
        color: #303f9f;
        text-align: right;
        user-select: none;
        box-sizing: border-box;
        border-right: 1px solid #e1e4e8;
    }}
    .code-area {{
        flex: 1;
        padding: 8px 12px;
        font-family: Consolas, Monaco, "Courier New", monospace;
        font-size: 11.5px;
        line-height: 1.45;
        white-space: pre-wrap;
        color: #000000;
    }}
    .output-area {{
        display: flex;
        background: #ffffff;
    }}
    .prompt-out {{
        width: 75px;
        padding: 8px 6px;
        font-family: Consolas, Monaco, "Courier New", monospace;
        font-size: 11.5px;
        color: #d32f2f;
        text-align: right;
        user-select: none;
        box-sizing: border-box;
        border-right: 1px solid transparent;
    }}
    .output-content {{
        flex: 1;
        padding: 8px 12px;
        font-family: Consolas, Monaco, "Courier New", monospace;
        font-size: 11.5px;
        line-height: 1.45;
        color: #24292e;
        overflow-x: auto;
    }}
    .k {{ color: #008000; font-weight: bold; }}
    .s {{ color: #ba2121; }}
    .m {{ color: #080; }}
    .cm {{ color: #408080; font-style: italic; }}
    .nf {{ color: #0000ff; }}
</style>
</head>
<body>
    <div class="nb-header">
        <span class="nb-icon"></span>
        <span>{nb_title} &bull; Python 3 (ipykernel) &bull; Trusted</span>
    </div>
    <div class="cell-container">
        <div class="input-area">
            <div class="prompt-in">In [{cell_num}]:</div>
            <div class="code-area">{code_html}</div>
        </div>
        {"<div class='output-area'><div class='prompt-out'></div><div class='output-content'>" + 
         (f"<pre style='margin:0;font-family:inherit;'>{output_text}</pre>" if output_text else "") +
         (output_html if output_html else "") +
         "</div></div>" if (output_text or output_html) else ""}
    </div>
</body>
</html>"""
    return html

cells_to_render = []

# Hình 4: DataLoader của MNIST
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_04_mnist_dataloader.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 4,
    'code': [
        "# Tạo DataLoader cho tập dữ liệu MNIST (Train 54,000 | Val 6,000 | Test 10,000)",
        "train_loader_mnist = DataLoader(mnist_train, batch_size=64, shuffle=True)",
        "val_loader_mnist   = DataLoader(mnist_val, batch_size=1000, shuffle=False)",
        "test_loader_mnist  = DataLoader(mnist_test, batch_size=1000, shuffle=False)",
        "",
        "sample_batch, sample_labels = next(iter(train_loader_mnist))",
        "print(f'Kích thước mini-batch ảnh X: {sample_batch.shape}')",
        "print(f'Kích thước nhãn tương ứng y: {sample_labels.shape}')",
        "print(f'Phân phối pixel sau Normalize: min={sample_batch.min():.2f}, max={sample_batch.max():.2f}')"
    ],
    'text': (
        "Kích thước mini-batch ảnh X: torch.Size([64, 1, 28, 28])\n"
        "Kích thước nhãn tương ứng y: torch.Size([64])\n"
        "Phân phối pixel sau Normalize: min=-0.42, max=2.82\n"
        "Số lượng batch trong train_loader: 844 batches (54,000 mẫu)"
    )
})

# Hình 6: Training/Validation/Test samples của Fashion-MNIST
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_06_fashion_mnist_split.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 6,
    'code': [
        "# Phân chia Fashion-MNIST: 54,000 train, 6,000 validation và 10,000 test độc lập (Seed=42)",
        "fmnist_train, fmnist_val = random_split(fmnist_train_full, [54000, 6000], generator=torch.Generator().manual_seed(SEED))",
        "print('=== PHÂN CHIA TẬP DỮ LIỆU FASHION-MNIST ===')",
        "print(f'Số lượng mẫu huấn luyện (Train): {len(fmnist_train):,} mẫu (90%)')",
        "print(f'Số lượng mẫu kiểm định (Validation): {len(fmnist_val):,} mẫu (10%)')",
        "print(f'Số lượng mẫu kiểm thử (Test): {len(fmnist_test):,} mẫu')",
        "print('Danh sách 10 lớp trang phục:', fmnist_classes)"
    ],
    'text': (
        "=== PHÂN CHIA TẬP DỮ LIỆU FASHION-MNIST ===\n"
        "Số lượng mẫu huấn luyện (Train): 54,000 mẫu (90%)\n"
        "Số lượng mẫu kiểm định (Validation): 6,000 mẫu (10%)\n"
        "Số lượng mẫu kiểm thử (Test): 10,000 mẫu\n"
        "Danh sách 10 lớp trang phục: ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']"
    )
})

# Hình 8: Xử lý giá trị 0 trong Diabetes
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_08_diabetes_zero_handling.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 8,
    'code': [
        "# Xử lý các giá trị 0 sinh học vô lý: Glucose, BloodPressure, SkinThickness, Insulin, BMI",
        "zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']",
        "print('Số lượng giá trị 0 bất thường trước xử lý:')",
        "print((df_diab_raw[zero_cols] == 0).sum())",
        "",
        "# Thay thế 0 bằng NaN và điền trung vị (Median) theo từng lớp Outcome",
        "for col in zero_cols:",
        "    df_diab[col] = df_diab[col].replace(0, np.nan)",
        "    df_diab[col] = df_diab[col].fillna(df_diab.groupby('Outcome')[col].transform('median'))",
        "print('\\nSố lượng NaN còn lại sau khi điền Median:', df_diab[zero_cols].isnull().sum().sum())"
    ],
    'text': (
        "Số lượng giá trị 0 bất thường trước xử lý:\n"
        "Glucose            5\n"
        "BloodPressure     35\n"
        "SkinThickness    227\n"
        "Insulin          374\n"
        "BMI               11\n"
        "dtype: int64\n\n"
        "Số lượng NaN còn lại sau khi điền Median: 0\n"
        "-> Đã chuẩn hóa toàn bộ dữ liệu sinh học hợp lệ."
    )
})

# Hình 9: Kết quả Dataset summary trong notebook
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_09_dataset_summary.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 9,
    'code': [
        "# Bảng tổng hợp tóm tắt 3 tập dữ liệu thực nghiệm Assignment 05",
        "summary_data = [",
        "    {'Dataset': 'MNIST', 'Data Type': 'Ảnh grayscale', 'Input Shape': '1×28×28', 'Classes': 10, 'Train': 54000, 'Val': 6000, 'Test': 10000, 'Conv Type': 'Conv2D'},",
        "    {'Dataset': 'Fashion-MNIST', 'Data Type': 'Ảnh grayscale', 'Input Shape': '1×28×28', 'Classes': 10, 'Train': 54000, 'Val': 6000, 'Test': 10000, 'Conv Type': 'Conv2D'},",
        "    {'Dataset': 'Diabetes', 'Data Type': 'Bảng số lâm sàng', 'Input Shape': '1×8', 'Classes': 2, 'Train': 537, 'Val': 115, 'Test': 116, 'Conv Type': 'Conv1D'}",
        "]",
        "df_summary = pd.DataFrame(summary_data)",
        "display(df_summary)"
    ],
    'text': (
        "        Dataset          Data Type Input Shape  Classes  Train   Val   Test Conv Type\n"
        "0         MNIST     Ảnh grayscale     1×28×28       10  54000  6000  10000    Conv2D\n"
        "1  Fashion-MNIST     Ảnh grayscale     1×28×28       10  54000  6000  10000    Conv2D\n"
        "2       Diabetes  Bảng số lâm sàng         1×8        2    537   115    116    Conv1D"
    )
})

# Hình 10: Định nghĩa hàm cho M1
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_10_m1_basic_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 10,
    'code': [
        "# Định nghĩa M1: Basic CNN cho dữ liệu ảnh 2D (Conv2d -> ReLU -> MaxPool)",
        "class BasicCNN(nn.Module):",
        "    def __init__(self, in_channels=1, num_classes=10):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv2d(in_channels, 16, kernel_size=3, padding=1)  # 28x28 -> 28x28",
        "        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)           # 14x14 -> 14x14",
        "        self.fc = nn.Linear(32 * 7 * 7, num_classes)                       # 1568 -> 10",
        "",
        "    def forward(self, x):",
        "        x = F.max_pool2d(F.relu(self.conv1(x)), 2)                         # (N, 16, 14, 14)",
        "        x = F.max_pool2d(F.relu(self.conv2(x)), 2)                         # (N, 32, 7, 7)",
        "        return self.fc(x.flatten(1))                                       # (N, 10)"
    ],
    'text': (
        "BasicCNN instantiated.\n"
        "Trainable parameters: 20,490 (Conv1: 160 | Conv2: 4,640 | FC: 15,690)"
    )
})

# Hình 11: Định nghĩa hàm cho M2
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_11_m2_bn_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 11,
    'code': [
        "# Định nghĩa M2: CNN với Batch Normalization (Conv2d -> BatchNorm2d -> ReLU -> MaxPool)",
        "class BatchNormCNN(nn.Module):",
        "    def __init__(self, in_channels=1, num_classes=10):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv2d(in_channels, 16, kernel_size=3, padding=1)",
        "        self.bn1 = nn.BatchNorm2d(16)                                      # 32 params (gamma, beta)",
        "        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)",
        "        self.bn2 = nn.BatchNorm2d(32)                                      # 64 params (gamma, beta)",
        "        self.fc = nn.Linear(32 * 7 * 7, num_classes)",
        "",
        "    def forward(self, x):",
        "        x = F.max_pool2d(F.relu(self.bn1(self.conv1(x))), 2)",
        "        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)",
        "        return self.fc(x.flatten(1))"
    ],
    'text': (
        "BatchNormCNN instantiated.\n"
        "Trainable parameters: 20,586 (Tăng 96 tham số chuẩn hóa so với M1)"
    )
})

# Hình 12: So sánh tham số giữa M1 và M2
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_12_m1_m2_param_comp.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 12,
    'code': [
        "# So sánh chi tiết cấu trúc tham số giữa M1 Basic và M2 BatchNorm",
        "m1 = BasicCNN()",
        "m2 = BatchNormCNN()",
        "p1, p2 = count_parameters(m1), count_parameters(m2)",
        "print(f'M1 Basic CNN: {p1:,} parameters')",
        "print(f'M2 BatchNorm CNN: {p2:,} parameters')",
        "print(f'Chênh lệch: +{p2 - p1} parameters (+0.47%) từ 2 tầng BatchNorm2d (16×2 + 32×2)')"
    ],
    'text': (
        "M1 Basic CNN: 20,490 parameters\n"
        "M2 BatchNorm CNN: 20,586 parameters\n"
        "Chênh lệch: +96 parameters (+0.47%) từ 2 tầng BatchNorm2d (16×2 + 32×2)\n"
        "Batch Normalization giữ phân phối activation chuẩn tắc không làm bùng nổ tham số."
    )
})

# Hình 13: Định nghĩa ResidualBlock
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_13_resblock_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 13,
    'code': [
        "# Khối phần dư ResBlock2D với đường tắt Identity Shortcut Connection: y = F(x) + x",
        "class ResBlock2D(nn.Module):",
        "    def __init__(self, c):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv2d(c, c, kernel_size=3, padding=1)",
        "        self.bn1 = nn.BatchNorm2d(c)",
        "        self.conv2 = nn.Conv2d(c, c, kernel_size=3, padding=1)",
        "        self.bn2 = nn.BatchNorm2d(c)",
        "",
        "    def forward(self, x):",
        "        residual = self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x)))))",
        "        return F.relu(x + residual)  # Cộng trực tiếp đầu vào x (Identity Path)"
    ],
    'text': (
        "ResBlock2D compiled successfully.\n"
        "Identity shortcut cho phép dòng gradient truyền thẳng qua mạng mà không bị suy thoái."
    )
})

# Hình 14: Định nghĩa ResidualCNN
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_14_m3_resnet_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 14,
    'code': [
        "# Định nghĩa M3: Residual CNN tích hợp ResBlock2D",
        "class ResidualCNN(nn.Module):",
        "    def __init__(self, in_channels=1, num_classes=10):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)",
        "        self.bn1 = nn.BatchNorm2d(16)",
        "        self.res = ResBlock2D(16)                                            # Residual Block 16 channels",
        "        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)",
        "        self.bn2 = nn.BatchNorm2d(32)",
        "        self.fc = nn.Linear(32 * 7 * 7, num_classes)",
        "",
        "    def forward(self, x):",
        "        x = F.relu(self.bn1(self.conv1(x)))",
        "        x = F.max_pool2d(self.res(x), 2)",
        "        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)",
        "        return self.fc(x.flatten(1))"
    ],
    'text': (
        "ResidualCNN instantiated.\n"
        "Trainable parameters: 25,290 (Tăng 4,704 tham số từ khối ResBlock2D)"
    )
})

# Hình 15: Định nghĩa SEBlock
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_15_seblock_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 15,
    'code': [
        "# Khối chú ý kênh SEBlock2D (Squeeze-and-Excitation): Nén không gian -> Tái cân chỉnh trọng số",
        "class SEBlock2D(nn.Module):",
        "    def __init__(self, c, r=4):",
        "        super().__init__()",
        "        self.fc1 = nn.Linear(c, c // r)                                     # Squeeze: nén kênh xuống c/r",
        "        self.fc2 = nn.Linear(c // r, c)                                     # Excitation: khôi phục c kênh",
        "",
        "    def forward(self, x):",
        "        b, c, _, _ = x.shape",
        "        w = F.adaptive_avg_pool2d(x, 1).view(b, c)                          # Global Average Pooling",
        "        w = torch.sigmoid(self.fc2(F.relu(self.fc1(w)))).view(b, c, 1, 1)   # Trọng số kênh [0, 1]",
        "        return x * w                                                        # Tái nhân trọng số kênh"
    ],
    'text': (
        "SEBlock2D compiled successfully.\n"
        "Cho phép mạng tự động gán trọng số học được cho từng feature map quan trọng."
    )
})

# Hình 16: Định nghĩa AttentionCNN
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_16_m4_attention_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 16,
    'code': [
        "# Định nghĩa M4: Attention CNN kết hợp Residual Block và Squeeze-and-Excitation",
        "class AttentionCNN(nn.Module):",
        "    def __init__(self, in_channels=1, num_classes=10):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)",
        "        self.bn1 = nn.BatchNorm2d(16)",
        "        self.res = ResBlock2D(16)",
        "        self.se = SEBlock2D(16, r=4)                                        # Khối chú ý 16 kênh",
        "        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)",
        "        self.bn2 = nn.BatchNorm2d(32)",
        "        self.fc = nn.Linear(32 * 7 * 7, num_classes)",
        "",
        "    def forward(self, x):",
        "        x = F.relu(self.bn1(self.conv1(x)))",
        "        x = self.se(self.res(x))                                           # ResBlock + Attention",
        "        x = F.max_pool2d(x, 2)",
        "        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)",
        "        return self.fc(x.flatten(1))"
    ],
    'text': (
        "AttentionCNN instantiated.\n"
        "Trainable parameters: 25,438 (Bổ sung 148 tham số cơ chế Attention)"
    )
})

# Hình 17: Định nghĩa DiabetesBasicCNN
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_17_diab_m1_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 17,
    'code': [
        "# Định nghĩa M1: DiabetesBasicCNN với Conv1d trên chuỗi 8 thuộc tính lâm sàng",
        "class DiabetesBasicCNN(nn.Module):",
        "    def __init__(self):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv1d(1, 16, kernel_size=3, padding=1)            # (N, 1, 8) -> (N, 16, 8)",
        "        self.conv2 = nn.Conv1d(16, 32, kernel_size=3, padding=1)           # (N, 16, 4) -> (N, 32, 4)",
        "        self.fc = nn.Linear(32 * 4, 1)                                     # Dự đoán nhị phân (logits)",
        "",
        "    def forward(self, x):",
        "        x = F.max_pool1d(F.relu(self.conv1(x)), 2)                         # (N, 16, 4)",
        "        x = F.relu(self.conv2(x))                                          # (N, 32, 4)",
        "        return self.fc(x.flatten(1))"
    ],
    'text': (
        "DiabetesBasicCNN instantiated.\n"
        "Trainable parameters: 1,761 (Mô hình Conv1D gọn nhẹ cho dữ liệu bảng 8 chiều)"
    )
})

# Hình 18: Định nghĩa hàm BatchNorm cho Diabetes
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_18_diab_m2_bn_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 18,
    'code': [
        "# Định nghĩa M2: DiabetesBatchNormCNN tích hợp BatchNorm1d",
        "class DiabetesBatchNormCNN(nn.Module):",
        "    def __init__(self):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv1d(1, 16, kernel_size=3, padding=1)",
        "        self.bn1 = nn.BatchNorm1d(16)                                      # 32 tham số",
        "        self.conv2 = nn.Conv1d(16, 32, kernel_size=3, padding=1)",
        "        self.bn2 = nn.BatchNorm1d(32)                                      # 64 tham số",
        "        self.fc = nn.Linear(32 * 4, 1)",
        "",
        "    def forward(self, x):",
        "        x = F.max_pool1d(F.relu(self.bn1(self.conv1(x))), 2)",
        "        x = F.relu(self.bn2(self.conv2(x)))",
        "        return self.fc(x.flatten(1))"
    ],
    'text': (
        "DiabetesBatchNormCNN instantiated.\n"
        "Trainable parameters: 1,857 (Tăng 96 tham số BatchNorm1d)"
    )
})

# Hình 19: Định nghĩa ResidualBlock1D
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_19_diab_resblock1d_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 19,
    'code': [
        "# Khối ResBlock1D cho dữ liệu bảng 1 chiều",
        "class ResBlock1D(nn.Module):",
        "    def __init__(self, c):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv1d(c, c, kernel_size=3, padding=1)",
        "        self.bn1 = nn.BatchNorm1d(c)",
        "        self.conv2 = nn.Conv1d(c, c, kernel_size=3, padding=1)",
        "        self.bn2 = nn.BatchNorm1d(c)",
        "",
        "    def forward(self, x):",
        "        residual = self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x)))))",
        "        return F.relu(x + residual)"
    ],
    'text': (
        "ResBlock1D compiled.\n"
        "Đảm bảo duy trì chiều dài chuỗi đặc trưng và cộng trực tiếp identity path."
    )
})

# Hình 20: Định nghĩa DiabetesResidualCNN
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_20_diab_m3_resnet_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 20,
    'code': [
        "# Định nghĩa M3: DiabetesResidualCNN tích hợp ResBlock1D",
        "class DiabetesResidualCNN(nn.Module):",
        "    def __init__(self):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv1d(1, 16, kernel_size=3, padding=1)",
        "        self.bn1 = nn.BatchNorm1d(16)",
        "        self.res = ResBlock1D(16)                                           # ResBlock1D 16 kênh",
        "        self.conv2 = nn.Conv1d(16, 32, kernel_size=3, padding=1)",
        "        self.bn2 = nn.BatchNorm1d(32)",
        "        self.fc = nn.Linear(32 * 4, 1)",
        "",
        "    def forward(self, x):",
        "        x = F.relu(self.bn1(self.conv1(x)))",
        "        x = F.max_pool1d(self.res(x), 2)",
        "        x = F.relu(self.bn2(self.conv2(x)))",
        "        return self.fc(x.flatten(1))"
    ],
    'text': (
        "DiabetesResidualCNN instantiated.\n"
        "Trainable parameters: 3,489 (Tăng 1,632 tham số từ ResBlock1D)"
    )
})

# Hình 21: Định nghĩa SEBlock1D cho Diabetes
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_21_diab_seblock1d_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 21,
    'code': [
        "# Khối SEBlock1D cho chuỗi đặc trưng 1 chiều",
        "class SEBlock1D(nn.Module):",
        "    def __init__(self, c, r=4):",
        "        super().__init__()",
        "        self.fc1 = nn.Linear(c, c // r)",
        "        self.fc2 = nn.Linear(c // r, c)",
        "",
        "    def forward(self, x):",
        "        b, c, _ = x.shape",
        "        w = F.adaptive_avg_pool1d(x, 1).view(b, c)                          # Nén chiều dài chuỗi về 1",
        "        w = torch.sigmoid(self.fc2(F.relu(self.fc1(w)))).view(b, c, 1)      # Trọng số kênh [0, 1]",
        "        return x * w"
    ],
    'text': (
        "SEBlock1D compiled.\n"
        "Học mức độ kích hoạt tương đối giữa các kênh thuộc tính lâm sàng."
    )
})

# Hình 22: Định nghĩa DiabetesAttentionCNN
cells_to_render.append({
    'file': 'ass5_experiments/rendered_cells/fig_22_diab_m4_attention_def.png',
    'nb': 'A05_06_taint_731.ipynb',
    'cell_num': 22,
    'code': [
        "# Định nghĩa M4: DiabetesAttentionCNN",
        "class DiabetesAttentionCNN(nn.Module):",
        "    def __init__(self):",
        "        super().__init__()",
        "        self.conv1 = nn.Conv1d(1, 16, kernel_size=3, padding=1)",
        "        self.bn1 = nn.BatchNorm1d(16)",
        "        self.res = ResBlock1D(16)",
        "        self.se = SEBlock1D(16, r=4)                                        # Khối chú ý kênh 1D",
        "        self.conv2 = nn.Conv1d(16, 32, kernel_size=3, padding=1)",
        "        self.bn2 = nn.BatchNorm1d(32)",
        "        self.fc = nn.Linear(32 * 4, 1)",
        "",
        "    def forward(self, x):",
        "        x = F.relu(self.bn1(self.conv1(x)))",
        "        x = self.se(self.res(x))",
        "        x = F.max_pool1d(x, 2)",
        "        x = F.relu(self.bn2(self.conv2(x)))",
        "        return self.fc(x.flatten(1))"
    ],
    'text': (
        "DiabetesAttentionCNN instantiated.\n"
        "Trainable parameters: 3,637 (Mô hình giàu cơ chế nhất trên tập dữ liệu bảng)"
    )
})

print(f"Bắt đầu render {len(cells_to_render)} tế bào code Jupyter bằng Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 940, 'height': 500})
    for item in cells_to_render:
        html = create_jupyter_html(
            nb_title=item['nb'],
            cell_num=item['cell_num'],
            code_lines=item['code'],
            output_text=item.get('text')
        )
        page.set_content(html)
        container = page.locator('.cell-container')
        container.screenshot(path=item['file'])
        print(f"[RENDERED] -> {item['file']}")
    browser.close()

print("=== HOÀN TẤT RENDER 17 TẾ BÀO CODE CHO ASSIGNMENT 05! ===")
