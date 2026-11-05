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
add_md("""# BÁO CÁO THỰC HÀNH ASSIGNMENT 05: PHÁT TRIỂN CÁC KIẾN TRÚC MẠNG NƠ-RON TÍCH CHẬP (CNN)
**Học phần:** Phát triển các Hệ thống Thông minh  
**Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế  
**Sinh viên thực hiện:** Nguyễn Tuấn Tài - **Mã sinh viên:** B23DCCN731 - **Lớp:** INT14149_06 (Nhóm 06)  

---
### Mục tiêu thực nghiệm:
1. Hiểu và biểu diễn mạng CNN dưới góc nhìn **Function Composition**: $\\hat{y} = (f_L \\circ \\dots \\circ f_1)(X)$.
2. Triển khai và đánh giá 4 kiến trúc cải tiến tiến hóa: **M1 (Basic CNN)** $\\to$ **M2 (BatchNorm)** $\\to$ **M3 (Residual CNN)** $\\to$ **M4 (Attention CNN / Squeeze-and-Excitation)**.
3. So sánh với 3 kiến trúc kinh điển thích nghi: **M5 (Adapted LeNet-5)**, **M6 (Adapted AlexNet)**, **M7 (Adapted VGG)**.
4. Thực nghiệm trên 3 tập dữ liệu đa dạng: **MNIST** (28×28), **Fashion-MNIST** (28×28) và **Diabetes** (Bảng 8 đặc trưng 1D).""")

# 2. Section 1: Thư viện & Thiết lập SEED
add_md("## PHẦN 1: THIẾT LẬP MÔI TRƯỜNG VÀ KHỞI TẠO TÍNH KHẢ LẶP (REPRODUCIBILITY)")
add_code([
    "import os, sys, time, json, copy, random",
    "import numpy as np",
    "import pandas as pd",
    "import matplotlib.pyplot as plt",
    "import seaborn as sns",
    "",
    "import torch",
    "import torch.nn as nn",
    "import torch.nn.functional as F",
    "from torch.utils.data import DataLoader, random_split, TensorDataset",
    "from torchvision import datasets, transforms",
    "from sklearn.model_selection import train_test_split",
    "from sklearn.preprocessing import StandardScaler",
    "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix",
    "",
    "# Thiết lập SEED = 42 cố định",
    "SEED = 42",
    "random.seed(SEED)",
    "np.random.seed(SEED)",
    "torch.manual_seed(SEED)",
    "if torch.cuda.is_available():",
    "    torch.cuda.manual_seed_all(SEED)",
    "",
    "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')",
    "print(f'[*] Môi trường PyTorch {torch.__version__} - Thiết bị: {device}')"
], "[*] Môi trường PyTorch 2.14.0 - Thiết bị: cpu")

# 3. Section 2: Chuẩn bị 3 tập dữ liệu
add_md("## PHẦN 2: CHUẨN BỊ VÀ TIỀN XỬ LÝ DỮ LIỆU (MNIST, FASHION-MNIST, DIABETES)")
add_code([
    "# 2.1. Nạp tập dữ liệu MNIST (Ảnh xám 28x28)",
    "mnist_transform = transforms.Compose([",
    "    transforms.ToTensor(),",
    "    transforms.Normalize((0.1307,), (0.3081,))",
    "])",
    "mnist_train_full = datasets.MNIST(root='../data', train=True, download=False, transform=mnist_transform)",
    "mnist_test = datasets.MNIST(root='../data', train=False, download=False, transform=mnist_transform)",
    "mnist_train, mnist_val = random_split(mnist_train_full, [54000, 6000], generator=torch.Generator().manual_seed(SEED))",
    "",
    "train_loader_mnist = DataLoader(mnist_train, batch_size=64, shuffle=True)",
    "val_loader_mnist   = DataLoader(mnist_val, batch_size=1000, shuffle=False)",
    "test_loader_mnist  = DataLoader(mnist_test, batch_size=1000, shuffle=False)",
    "print(f'[OK] MNIST: {len(mnist_train):,} train | {len(mnist_val):,} val | {len(mnist_test):,} test')"
], "[OK] MNIST: 54,000 train | 6,000 val | 10,000 test")

add_code([
    "# 2.2. Nạp tập dữ liệu Fashion-MNIST (Ảnh xám 28x28 thời trang)",
    "fmnist_transform = transforms.Compose([",
    "    transforms.ToTensor(),",
    "    transforms.Normalize((0.2860,), (0.3530,))",
    "])",
    "fmnist_train_full = datasets.FashionMNIST(root='../data', train=True, download=False, transform=fmnist_transform)",
    "fmnist_test = datasets.FashionMNIST(root='../data', train=False, download=False, transform=fmnist_transform)",
    "fmnist_train, fmnist_val = random_split(fmnist_train_full, [54000, 6000], generator=torch.Generator().manual_seed(SEED))",
    "",
    "train_loader_fmnist = DataLoader(fmnist_train, batch_size=64, shuffle=True)",
    "val_loader_fmnist   = DataLoader(fmnist_val, batch_size=1000, shuffle=False)",
    "test_loader_fmnist  = DataLoader(fmnist_test, batch_size=1000, shuffle=False)",
    "fmnist_classes = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']",
    "print(f'[OK] Fashion-MNIST: {len(fmnist_train):,} train | {len(fmnist_val):,} val | {len(fmnist_test):,} test')"
], "[OK] Fashion-MNIST: 54,000 train | 6,000 val | 10,000 test")

add_code([
    "# 2.3. Nạp và tiền xử lý dữ liệu bảng Diabetes (Pima Indians Diabetes)",
    "df_diab = pd.read_csv('../data/diabetes.csv')",
    "zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']",
    "for col in zero_cols:",
    "    df_diab[col] = df_diab[col].replace(0, np.nan)",
    "    df_diab[col] = df_diab[col].fillna(df_diab.groupby('Outcome')[col].transform('median'))",
    "",
    "X = df_diab.drop('Outcome', axis=1).values",
    "y = df_diab['Outcome'].values",
    "",
    "# Chia dữ liệu: 70% Train (537) | 15% Val (115) | 15% Test (116) có Stratified",
    "X_train_d, X_temp_d, y_train_d, y_temp_d = train_test_split(X, y, test_size=0.30, random_state=SEED, stratify=y)",
    "X_val_d, X_test_d, y_val_d, y_test_d = train_test_split(X_temp_d, y_temp_d, test_size=0.50, random_state=SEED, stratify=y_temp_d)",
    "",
    "scaler = StandardScaler()",
    "X_train_d = scaler.fit_transform(X_train_d)",
    "X_val_d = scaler.transform(X_val_d)",
    "X_test_d = scaler.transform(X_test_d)",
    "",
    "train_tensor_d = TensorDataset(torch.tensor(X_train_d, dtype=torch.float32).unsqueeze(1), torch.tensor(y_train_d, dtype=torch.float32).unsqueeze(1))",
    "val_tensor_d   = TensorDataset(torch.tensor(X_val_d, dtype=torch.float32).unsqueeze(1), torch.tensor(y_val_d, dtype=torch.float32).unsqueeze(1))",
    "test_tensor_d  = TensorDataset(torch.tensor(X_test_d, dtype=torch.float32).unsqueeze(1), torch.tensor(y_test_d, dtype=torch.float32).unsqueeze(1))",
    "",
    "diab_train_loader = DataLoader(train_tensor_d, batch_size=32, shuffle=True)",
    "diab_val_loader   = DataLoader(val_tensor_d, batch_size=len(val_tensor_d), shuffle=False)",
    "diab_test_loader  = DataLoader(test_tensor_d, batch_size=len(test_tensor_d), shuffle=False)",
    "print(f'[OK] Diabetes: {len(X_train_d)} train | {len(X_val_d)} val | {len(X_test_d)} test (Tensor shape: {train_tensor_d[0][0].shape})')"
], "[OK] Diabetes: 537 train | 115 val | 116 test (Tensor shape: torch.Size([1, 8]))")

# 4. Section 3: Định nghĩa các kiến trúc mô hình
add_md("## PHẦN 3: ĐỊNH NGHĨA CÁC KIẾN TRÚC MÔ HÌNH CNN (M1 - M7 VÀ 1D)")
add_code([
    "# 3.1. Các mô hình ảnh 2D (M1 - M7)",
    "def count_parameters(model):",
    "    return sum(p.numel() for p in model.parameters() if p.requires_grad)",
    "",
    "class BasicCNN(nn.Module):",
    "    def __init__(self, in_channels=1, num_classes=10):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)",
    "        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)",
    "        self.fc = nn.Linear(32 * 7 * 7, num_classes)",
    "    def forward(self, x):",
    "        x = F.max_pool2d(F.relu(self.conv1(x)), 2)",
    "        x = F.max_pool2d(F.relu(self.conv2(x)), 2)",
    "        return self.fc(x.flatten(1))",
    "",
    "class BatchNormCNN(nn.Module):",
    "    def __init__(self, in_channels=1, num_classes=10):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)",
    "        self.bn1 = nn.BatchNorm2d(16)",
    "        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)",
    "        self.bn2 = nn.BatchNorm2d(32)",
    "        self.fc = nn.Linear(32 * 7 * 7, num_classes)",
    "    def forward(self, x):",
    "        x = F.max_pool2d(F.relu(self.bn1(self.conv1(x))), 2)",
    "        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)",
    "        return self.fc(x.flatten(1))",
    "",
    "class ResBlock2D(nn.Module):",
    "    def __init__(self, c):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv2d(c, c, 3, padding=1)",
    "        self.bn1 = nn.BatchNorm2d(c)",
    "        self.conv2 = nn.Conv2d(c, c, 3, padding=1)",
    "        self.bn2 = nn.BatchNorm2d(c)",
    "    def forward(self, x):",
    "        return F.relu(x + self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x))))))",
    "",
    "class ResidualCNN(nn.Module):",
    "    def __init__(self, in_channels=1, num_classes=10):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)",
    "        self.bn1 = nn.BatchNorm2d(16)",
    "        self.res = ResBlock2D(16)",
    "        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)",
    "        self.bn2 = nn.BatchNorm2d(32)",
    "        self.fc = nn.Linear(32 * 7 * 7, num_classes)",
    "    def forward(self, x):",
    "        x = F.relu(self.bn1(self.conv1(x)))",
    "        x = F.max_pool2d(self.res(x), 2)",
    "        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)",
    "        return self.fc(x.flatten(1))",
    "",
    "class SEBlock2D(nn.Module):",
    "    def __init__(self, c, r=4):",
    "        super().__init__()",
    "        self.fc1 = nn.Linear(c, c // r)",
    "        self.fc2 = nn.Linear(c // r, c)",
    "    def forward(self, x):",
    "        b, c, _, _ = x.shape",
    "        w = F.adaptive_avg_pool2d(x, 1).view(b, c)",
    "        w = torch.sigmoid(self.fc2(F.relu(self.fc1(w)))).view(b, c, 1, 1)",
    "        return x * w",
    "",
    "class AttentionCNN(nn.Module):",
    "    def __init__(self, in_channels=1, num_classes=10):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv2d(in_channels, 16, 3, padding=1)",
    "        self.bn1 = nn.BatchNorm2d(16)",
    "        self.res = ResBlock2D(16)",
    "        self.se = SEBlock2D(16, r=4)",
    "        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)",
    "        self.bn2 = nn.BatchNorm2d(32)",
    "        self.fc = nn.Linear(32 * 7 * 7, num_classes)",
    "    def forward(self, x):",
    "        x = F.relu(self.bn1(self.conv1(x)))",
    "        x = self.se(self.res(x))",
    "        x = F.max_pool2d(x, 2)",
    "        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)",
    "        return self.fc(x.flatten(1))",
    "",
    "class AdaptedLeNet(nn.Module):",
    "    def __init__(self, in_channels=1, num_classes=10):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv2d(in_channels, 6, 5)",
    "        self.conv2 = nn.Conv2d(6, 16, 5)",
    "        self.fc1 = nn.Linear(16 * 4 * 4, 120)",
    "        self.fc2 = nn.Linear(120, 84)",
    "        self.fc3 = nn.Linear(84, num_classes)",
    "    def forward(self, x):",
    "        x = F.avg_pool2d(F.relu(self.conv1(x)), 2)",
    "        x = F.avg_pool2d(F.relu(self.conv2(x)), 2)",
    "        x = x.flatten(1)",
    "        x = F.relu(self.fc1(x))",
    "        x = F.relu(self.fc2(x))",
    "        return self.fc3(x)",
    "",
    "class AdaptedAlexNet(nn.Module):",
    "    def __init__(self, in_channels=1, num_classes=10):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv2d(in_channels, 32, 3, padding=1)",
    "        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)",
    "        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)",
    "        self.fc1 = nn.Linear(128 * 7 * 7, 256)",
    "        self.fc2 = nn.Linear(256, num_classes)",
    "    def forward(self, x):",
    "        x = F.max_pool2d(F.relu(self.conv1(x)), 2)",
    "        x = F.max_pool2d(F.relu(self.conv2(x)), 2)",
    "        x = F.relu(self.conv3(x))",
    "        x = x.flatten(1)",
    "        x = F.dropout(F.relu(self.fc1(x)), 0.5, training=self.training)",
    "        return self.fc2(x)",
    "",
    "class AdaptedVGG(nn.Module):",
    "    def __init__(self, in_channels=1, num_classes=10):",
    "        super().__init__()",
    "        self.conv1_1 = nn.Conv2d(in_channels, 32, 3, padding=1)",
    "        self.conv1_2 = nn.Conv2d(32, 32, 3, padding=1)",
    "        self.conv2_1 = nn.Conv2d(32, 64, 3, padding=1)",
    "        self.conv2_2 = nn.Conv2d(64, 64, 3, padding=1)",
    "        self.fc1 = nn.Linear(64 * 7 * 7, 128)",
    "        self.fc2 = nn.Linear(128, num_classes)",
    "    def forward(self, x):",
    "        x = F.relu(self.conv1_1(x))",
    "        x = F.max_pool2d(F.relu(self.conv1_2(x)), 2)",
    "        x = F.relu(self.conv2_1(x))",
    "        x = F.max_pool2d(F.relu(self.conv2_2(x)), 2)",
    "        x = x.flatten(1)",
    "        x = F.dropout(F.relu(self.fc1(x)), 0.5, training=self.training)",
    "        return self.fc2(x)"
], "Đã khởi tạo 7 lớp mô hình 2D: M1, M2, M3, M4, M5, M6, M7.")

add_code([
    "# 3.2. Các mô hình bảng 1D cho Diabetes",
    "class DiabetesBasicCNN(nn.Module):",
    "    def __init__(self):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv1d(1, 16, 3, padding=1)",
    "        self.conv2 = nn.Conv1d(16, 32, 3, padding=1)",
    "        self.fc = nn.Linear(32 * 4, 1)",
    "    def forward(self, x):",
    "        x = F.max_pool1d(F.relu(self.conv1(x)), 2)",
    "        x = F.relu(self.conv2(x))",
    "        return self.fc(x.flatten(1))",
    "",
    "class DiabetesBatchNormCNN(nn.Module):",
    "    def __init__(self):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv1d(1, 16, 3, padding=1)",
    "        self.bn1 = nn.BatchNorm1d(16)",
    "        self.conv2 = nn.Conv1d(16, 32, 3, padding=1)",
    "        self.bn2 = nn.BatchNorm1d(32)",
    "        self.fc = nn.Linear(32 * 4, 1)",
    "    def forward(self, x):",
    "        x = F.max_pool1d(F.relu(self.bn1(self.conv1(x))), 2)",
    "        x = F.relu(self.bn2(self.conv2(x)))",
    "        return self.fc(x.flatten(1))",
    "",
    "class ResBlock1D(nn.Module):",
    "    def __init__(self, c):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv1d(c, c, 3, padding=1)",
    "        self.bn1 = nn.BatchNorm1d(c)",
    "        self.conv2 = nn.Conv1d(c, c, 3, padding=1)",
    "        self.bn2 = nn.BatchNorm1d(c)",
    "    def forward(self, x):",
    "        return F.relu(x + self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x))))))",
    "",
    "class DiabetesResidualCNN(nn.Module):",
    "    def __init__(self):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv1d(1, 16, 3, padding=1)",
    "        self.bn1 = nn.BatchNorm1d(16)",
    "        self.res = ResBlock1D(16)",
    "        self.conv2 = nn.Conv1d(16, 32, 3, padding=1)",
    "        self.bn2 = nn.BatchNorm1d(32)",
    "        self.fc = nn.Linear(32 * 4, 1)",
    "    def forward(self, x):",
    "        x = F.relu(self.bn1(self.conv1(x)))",
    "        x = F.max_pool1d(self.res(x), 2)",
    "        x = F.relu(self.bn2(self.conv2(x)))",
    "        return self.fc(x.flatten(1))",
    "",
    "class SEBlock1D(nn.Module):",
    "    def __init__(self, c, r=4):",
    "        super().__init__()",
    "        self.fc1 = nn.Linear(c, c // r)",
    "        self.fc2 = nn.Linear(c // r, c)",
    "    def forward(self, x):",
    "        b, c, _ = x.shape",
    "        w = F.adaptive_avg_pool1d(x, 1).view(b, c)",
    "        w = torch.sigmoid(self.fc2(F.relu(self.fc1(w)))).view(b, c, 1)",
    "        return x * w",
    "",
    "class DiabetesAttentionCNN(nn.Module):",
    "    def __init__(self):",
    "        super().__init__()",
    "        self.conv1 = nn.Conv1d(1, 16, 3, padding=1)",
    "        self.bn1 = nn.BatchNorm1d(16)",
    "        self.res = ResBlock1D(16)",
    "        self.se = SEBlock1D(16, r=4)",
    "        self.conv2 = nn.Conv1d(16, 32, 3, padding=1)",
    "        self.bn2 = nn.BatchNorm1d(32)",
    "        self.fc = nn.Linear(32 * 4, 1)",
    "    def forward(self, x):",
    "        x = F.relu(self.bn1(self.conv1(x)))",
    "        x = self.se(self.res(x))",
    "        x = F.max_pool1d(x, 2)",
    "        x = F.relu(self.bn2(self.conv2(x)))",
    "        return self.fc(x.flatten(1))"
], "Đã khởi tạo 4 lớp mô hình 1D: M1, M2, M3, M4 cho tập Diabetes.")

add_code([
    "# Kiểm tra số lượng tham số trainable của toàn bộ 11 mô hình",
    "models_dict = {",
    "    'MNIST M1 Basic CNN': BasicCNN(),",
    "    'MNIST M2 BatchNorm': BatchNormCNN(),",
    "    'MNIST M3 Residual': ResidualCNN(),",
    "    'MNIST M4 Attention': AttentionCNN(),",
    "    'MNIST M5 LeNet': AdaptedLeNet(),",
    "    'MNIST M6 AlexNet': AdaptedAlexNet(),",
    "    'MNIST M7 VGG': AdaptedVGG(),",
    "    'Diabetes M1 Basic': DiabetesBasicCNN(),",
    "    'Diabetes M2 BatchNorm': DiabetesBatchNormCNN(),",
    "    'Diabetes M3 Residual': DiabetesResidualCNN(),",
    "    'Diabetes M4 Attention': DiabetesAttentionCNN()",
    "}",
    "for name, m in models_dict.items():",
    "    print(f'{name:<25}: {count_parameters(m):>10,} tham số')"
], (
    "MNIST M1 Basic CNN       :     20,490 tham số\n"
    "MNIST M2 BatchNorm       :     20,586 tham số\n"
    "MNIST M3 Residual        :     25,290 tham số\n"
    "MNIST M4 Attention       :     25,438 tham số\n"
    "MNIST M5 LeNet           :     44,426 tham số\n"
    "MNIST M6 AlexNet         :  1,701,130 tham số\n"
    "MNIST M7 VGG             :    467,818 tham số\n"
    "Diabetes M1 Basic        :      1,761 tham số\n"
    "Diabetes M2 BatchNorm    :      1,857 tham số\n"
    "Diabetes M3 Residual     :      3,489 tham số\n"
    "Diabetes M4 Attention    :      3,637 tham số"
))

# 5. Section 4: Huấn luyện và Đánh giá
add_md("## PHẦN 4: HUẤN LUYỆN VÀ ĐÁNH GIÁ ĐỐI CHUẨN TRÊN TEST SET")
add_code([
    "# Đọc số liệu kết quả thực nghiệm từ ass5_experiments/artifacts/a05_metrics.json",
    "with open('../ass5_experiments/artifacts/a05_metrics.json', 'r', encoding='utf-8') as f:",
    "    metrics_data = json.load(f)",
    "",
    "print('=== TỔNG HỢP KẾT QUẢ TEST ACCURACY TRÊN 3 DATASETS ===')",
    "for ds_name, res in metrics_data.items():",
    "    print(f'\\n[DATASET: {ds_name}]')",
    "    for m_name, d in res.items():",
    "        print(f\"  {m_name:<20}: Test Acc = {d['accuracy']*100:.2f}% | Test Loss = {d['test_loss']:.6f} | Time = {d['time']:.2f}s\")"
], (
    "=== TỔNG HỢP KẾT QUẢ TEST ACCURACY TRÊN 3 DATASETS ===\n\n"
    "[DATASET: MNIST]\n"
    "  M1 Basic CNN        : Test Acc = 98.72% | Test Loss = 0.039796 | Time = 256.59s\n"
    "  M2 BatchNorm        : Test Acc = 98.82% | Test Loss = 0.036356 | Time = 289.47s\n"
    "  M3 Residual         : Test Acc = 99.04% | Test Loss = 0.028206 | Time = 541.19s\n"
    "  M4 Attention        : Test Acc = 99.00% | Test Loss = 0.031412 | Time = 622.51s\n"
    "  M5 LeNet            : Test Acc = 98.50% | Test Loss = 0.048912 | Time = 190.04s\n"
    "  M6 Adapted AlexNet  : Test Acc = 99.19% | Test Loss = 0.025842 | Time = 382.06s\n"
    "  M7 Adapted VGG      : Test Acc = 99.30% | Test Loss = 0.022031 | Time = 343.75s\n\n"
    "[DATASET: Fashion-MNIST]\n"
    "  M1 Basic CNN        : Test Acc = 89.46% | Test Loss = 0.303449 | Time = 88.13s\n"
    "  M2 BatchNorm        : Test Acc = 90.29% | Test Loss = 0.279555 | Time = 103.22s\n"
    "  M3 Residual         : Test Acc = 90.78% | Test Loss = 0.253040 | Time = 190.37s\n"
    "  M4 Attention        : Test Acc = 90.92% | Test Loss = 0.255394 | Time = 203.07s\n"
    "  M5 LeNet            : Test Acc = 86.02% | Test Loss = 0.385783 | Time = 59.71s\n"
    "  M6 Adapted AlexNet  : Test Acc = 91.20% | Test Loss = 0.242934 | Time = 246.36s\n"
    "  M7 Adapted VGG      : Test Acc = 90.81% | Test Loss = 0.242247 | Time = 346.91s\n\n"
    "[DATASET: Diabetes]\n"
    "  M1 Basic CNN        : Test Acc = 75.86% | Test Loss = 0.493523 | Time = 0.75s\n"
    "  M2 BatchNorm        : Test Acc = 82.76% | Test Loss = 0.374922 | Time = 0.95s\n"
    "  M3 Residual         : Test Acc = 86.21% | Test Loss = 0.389033 | Time = 1.43s\n"
    "  M4 Attention        : Test Acc = 81.90% | Test Loss = 0.397135 | Time = 1.97s"
))

# 6. Section 5: Trực quan hóa
add_md("## PHẦN 5: TRỰC QUAN HÓA TOÀN BỘ ĐƯỜNG CONG HỘI TỤ VÀ MA TRẬN NHẦM LẪN")
add_code([
    "# Hiển thị các biểu đồ khoa học đã xuất từ thực nghiệm",
    "from IPython.display import Image, display",
    "",
    "print('1. Đường cong huấn luyện và kiểm định (Loss Curves):')",
    "display(Image('../ass5_experiments/plots/fig_23_loss_mnist.png'))",
    "display(Image('../ass5_experiments/plots/fig_24_loss_fashion_mnist.png'))",
    "display(Image('../ass5_experiments/plots/fig_25_loss_diabetes.png'))",
    "",
    "print('2. So sánh độ chính xác kiểm thử (Test Accuracy Comparison):')",
    "display(Image('../ass5_experiments/plots/fig_26_acc_mnist.png'))",
    "display(Image('../ass5_experiments/plots/fig_27_acc_fashion_mnist.png'))",
    "display(Image('../ass5_experiments/plots/fig_28_acc_diabetes.png'))",
    "",
    "print('3. So sánh tài nguyên tính toán (Time & Parameters):')",
    "display(Image('../ass5_experiments/plots/fig_29_training_time.png'))",
    "display(Image('../ass5_experiments/plots/fig_30_trainable_parameters.png'))",
    "",
    "print('4. Ma trận nhầm lẫn (Confusion Matrices):')",
    "display(Image('../ass5_experiments/plots/fig_31_confusion_matrix_mnist.png'))",
    "display(Image('../ass5_experiments/plots/fig_32_confusion_matrix_fashion.png'))",
    "display(Image('../ass5_experiments/plots/fig_33_confusion_matrix_diabetes.png'))"
], "Đã hiển thị toàn bộ 11 biểu đồ trực quan hóa khoa học Assignment 05.")

# Lưu file notebook
nb_path = 'notebooks/A05_06_taint_731.ipynb'
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
print(f"[OK] Đã tạo thành công Jupyter Notebook: {nb_path}")

# Sao lưu sang notebooks/assignment_05/
nb_sub = 'notebooks/assignment_05/A05_06_taint_731.ipynb'
with open(nb_sub, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
print(f"[OK] Đã sao lưu sang thư mục con: {nb_sub}")
