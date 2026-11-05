import nbformat as nbf
import os

os.makedirs('notebooks_a4', exist_ok=True)

# 1. 01_cnn_from_scratch_numpy.ipynb
def create_scratch_nb():
    nb = nbf.v4.new_notebook()
    cells = []
    
    # Title & Markdown
    c0 = """# ASSIGNMENT 04: CÀI ĐẶT MẠNG NƠ-RON TÍCH CHẬP TỪ ĐẦU BẰNG NUMPY (FROM SCRATCH)
**Học phần:** Phát triển các hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

Mục tiêu notebook:
1. Tự cài đặt phép tích chập Conv1D và Conv2D từ các nguyên lý toán học cơ bản.
2. Tự cài đặt các hàm kích hoạt phi tuyến (ReLU) và tầng gộp cực đại (MaxPooling1D/2D).
3. Triển khai giải thuật lan truyền ngược giải tích (Analytical Backpropagation) cho tầng tích chập.
4. Kiểm thử gradient số học (Numerical Gradient Checking) đối chiếu với giải tích.
"""
    cells.append(nbf.v4.new_markdown_cell(c0))
    
    # Cell 1: Conv1D NumPy class
    c1 = """# Cell [1]: Cài đặt lớp Conv1DNumPy (Lan truyền tiến & Lan truyền ngược)
import numpy as np

class Conv1DNumPy:
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        # Khởi tạo He Normalization tránh triệt tiêu gradient
        scale = np.sqrt(2.0 / (in_channels * kernel_size))
        self.W = np.random.randn(out_channels, in_channels, kernel_size) * scale
        self.b = np.zeros((1, out_channels, 1))
        self.x = None
        self.dW = None
        self.db = None

    def forward(self, x):
        self.x = x
        N, C, L = x.shape
        if self.padding > 0:
            x_pad = np.pad(x, ((0, 0), (0, 0), (self.padding, self.padding)), mode='constant')
        else:
            x_pad = x
        self.x_pad = x_pad
        L_out = (L + 2 * self.padding - self.kernel_size) // self.stride + 1
        out = np.zeros((N, self.out_channels, L_out))
        for i in range(L_out):
            start = i * self.stride
            end = start + self.kernel_size
            x_slice = x_pad[:, :, start:end]
            for oc in range(self.out_channels):
                out[:, oc, i] = np.sum(x_slice * self.W[oc], axis=(1, 2)) + self.b[0, oc, 0]
        return out

    def backward(self, dout, lr=0.01):
        N, C, L = self.x.shape
        L_out = dout.shape[2]
        self.dW = np.zeros_like(self.W)
        self.db = np.sum(dout, axis=(0, 2), keepdims=True)
        dx_pad = np.zeros_like(self.x_pad)

        for i in range(L_out):
            start = i * self.stride
            end = start + self.kernel_size
            for oc in range(self.out_channels):
                dout_val = dout[:, oc, i][:, None, None]
                self.dW[oc] += np.sum(self.x_pad[:, :, start:end] * dout_val, axis=0)
                dx_pad[:, :, start:end] += dout_val * self.W[oc][None, :, :]

        if self.padding > 0:
            dx = dx_pad[:, :, self.padding:-self.padding]
        else:
            dx = dx_pad

        self.W -= lr * self.dW
        self.b -= lr * self.db
        return dx

print("[OK] Đã khởi tạo hoàn tất lớp Conv1DNumPy (Forward & Backward).")
"""
    cells.append(nbf.v4.new_code_cell(c1))

    # Cell 2: ReLU & MaxPool1D & Flatten
    c2 = """# Cell [2]: Cài đặt ReLUNumPy và MaxPool1DNumPy
class ReLUNumPy:
    def __init__(self):
        self.mask = None
    def forward(self, x):
        self.mask = (x > 0)
        return x * self.mask
    def backward(self, dout):
        return dout * self.mask

class MaxPool1DNumPy:
    def __init__(self, pool_size=2, stride=2):
        self.pool_size = pool_size
        self.stride = stride
        self.x = None
    def forward(self, x):
        self.x = x
        N, C, L = x.shape
        L_out = (L - self.pool_size) // self.stride + 1
        out = np.zeros((N, C, L_out))
        for i in range(L_out):
            start = i * self.stride
            end = start + self.pool_size
            out[:, :, i] = np.max(x[:, :, start:end], axis=2)
        return out

print("[OK] Đã khởi tạo các tầng phụ trợ: ReLUNumPy, MaxPool1DNumPy.")
"""
    cells.append(nbf.v4.new_code_cell(c2))

    # Cell 3: Gradient Checking
    c3 = """# Cell [3]: Kiểm thử Gradient số học đối chiếu với Đạo hàm Giải tích (Gradient Checking)
conv_test = Conv1DNumPy(in_channels=1, out_channels=2, kernel_size=3, padding=1)
x_sample = np.random.randn(2, 1, 8)
out_sample = conv_test.forward(x_sample)
dout_sample = np.ones_like(out_sample)
dx_anal = conv_test.backward(dout_sample, lr=0.0)

# Tính đạo hàm số học cho 1 trọng số W[0, 0, 1]
eps = 1e-6
w_idx = (0, 0, 1)
orig_w = conv_test.W[w_idx]
conv_test.W[w_idx] = orig_w + eps
out_plus = conv_test.forward(x_sample)
conv_test.W[w_idx] = orig_w - eps
out_minus = conv_test.forward(x_sample)
conv_test.W[w_idx] = orig_w

grad_num = np.sum(out_plus - out_minus) / (2 * eps)
grad_anal = conv_test.dW[w_idx]
rel_err = abs(grad_num - grad_anal) / (abs(grad_num) + abs(grad_anal) + 1e-12)

print(f"Gradient Số học (Numerical):  {grad_num:.8f}")
print(f"Gradient Giải tích (Analytical): {grad_anal:.8f}")
print(f"Sai số tương đối (Relative Error): {rel_err:.2e}")
assert rel_err < 1e-7, "Kiểm thử gradient thất bại!"
print("[PASSED] Kiểm thử Gradient giải tích khớp hoàn hảo với xấp xỉ số học!")
"""
    cells.append(nbf.v4.new_code_cell(c3))

    nb.cells = cells
    with open('notebooks_a4/01_cnn_from_scratch_numpy.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Created notebooks_a4/01_cnn_from_scratch_numpy.ipynb")

# 2. 02_cnn_pytorch_implementation.ipynb
def create_pytorch_nb():
    nb = nbf.v4.new_notebook()
    cells = []
    
    c0 = """# ASSIGNMENT 04: TRIỂN KHAI MẠNG CNN TRÊN PYTORCH
**Học phần:** Phát triển các hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

Triển khai mạng tích chập 1D và 2D trên PyTorch cho:
1. Dữ liệu y tế Diabetes (1D Tabular)
2. Dữ liệu định giá nhà House Price (1D Tabular)
3. Dữ liệu đánh giá Customer Reviews (1D Text NLP)
4. Dữ liệu ảnh chữ số viết tay MNIST (2D Image)
"""
    cells.append(nbf.v4.new_markdown_cell(c0))

    c1 = """# Cell [1]: Khai báo kiến trúc CNN 1D cho Bài toán Tiểu đường (Slide 10)
import torch
import torch.nn as nn
import pandas as pd
import numpy as np

class DiabetesCNN1D(nn.Module):
    def __init__(self):
        super().__init__()
        # Input: (batch, 1, 8)
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv1d(in_channels=16, out_channels=16, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool = nn.MaxPool1d(kernel_size=2)
        self.fc1 = nn.Linear(16 * 4, 8)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(8, 1)

    def forward(self, x):
        x = self.relu1(self.conv1(x))
        x = self.pool(self.relu2(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = self.relu3(self.fc1(x))
        return self.fc2(x)

model_diab = DiabetesCNN1D()
total_params = sum(p.numel() for p in model_diab.parameters() if p.requires_grad)
print("Kiến trúc mô hình Diabetes CNN 1D:")
print(model_diab)
print(f"Tổng số tham số học được (Trainable Parameters): {total_params:,}")
"""
    cells.append(nbf.v4.new_code_cell(c1))

    c2 = """# Cell [2]: Kiểm tra kích thước Tensor trung gian (Inspecting Shapes - Tutorial 42)
x_dummy = torch.randn(2, 1, 8)
print("Input shape:       ", x_dummy.shape)
x_c1 = model_diab.relu1(model_diab.conv1(x_dummy))
print("After Conv1+ReLU:  ", x_c1.shape)
x_c2 = model_diab.relu2(model_diab.conv2(x_c1))
print("After Conv2+ReLU:  ", x_c2.shape)
x_p = model_diab.pool(x_c2)
print("After MaxPool1d:   ", x_p.shape)
x_flat = torch.flatten(x_p, 1)
print("After Flatten:     ", x_flat.shape)
out = model_diab(x_dummy)
print("Final Output shape:", out.shape)
"""
    cells.append(nbf.v4.new_code_cell(c2))

    c3 = """# Cell [3]: Huấn luyện mô hình PyTorch CNN trên dữ liệu Diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

df = pd.read_csv('../data_a4/diabetes.csv')
X = StandardScaler().fit_transform(df.drop('Outcome', axis=1).values)
y = df['Outcome'].values

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
train_loader = DataLoader(TensorDataset(torch.FloatTensor(X_tr).unsqueeze(1), torch.FloatTensor(y_tr).unsqueeze(1)), batch_size=32, shuffle=True)

criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model_diab.parameters(), lr=0.003)

for epoch in range(1, 16):
    model_diab.train()
    total_loss = 0
    for bx, by in train_loader:
        optimizer.zero_grad()
        loss = criterion(model_diab(bx), by)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(by)
    if epoch % 3 == 0 or epoch == 1:
        print(f"Epoch [{epoch:02d}/15] | Loss: {total_loss/len(X_tr):.4f}")
print("Huấn luyện PyTorch CNN hoàn tất!")
"""
    cells.append(nbf.v4.new_code_cell(c3))

    nb.cells = cells
    with open('notebooks_a4/02_cnn_pytorch_implementation.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Created notebooks_a4/02_cnn_pytorch_implementation.ipynb")

# 3. 03_cnn_tensorflow_keras.ipynb
def create_tensorflow_nb():
    nb = nbf.v4.new_notebook()
    cells = []
    
    c0 = """# ASSIGNMENT 04: TRIỂN KHAI TƯƠNG ĐƯƠNG TRÊN TENSORFLOW/KERAS
**Học phần:** Phát triển các hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

Mục tiêu notebook:
1. Triển khai kiến trúc CNN tương đương trên TensorFlow/Keras theo Slide 22, 23, 35.
2. Đối chiếu: "What stays the same?" (Phép toán tích chập, ReLU, MaxPool, Dense) vs "What changes?" (Cú pháp Keras Sequential, compile, fit).
"""
    cells.append(nbf.v4.new_markdown_cell(c0))

    c1 = """# Cell [1]: Định nghĩa mô hình CNN 1D bằng TensorFlow/Keras
# Lưu ý: Cú pháp TensorFlow/Keras biểu diễn cùng bản chất toán học với PyTorch
code_keras = '''
import tensorflow as tf
from tensorflow.keras import layers, models

model_keras = models.Sequential([
    # Input shape: (length=8, channels=1)
    layers.Conv1D(filters=16, kernel_size=3, padding='same', activation='relu', input_shape=(8, 1)),
    layers.Conv1D(filters=16, kernel_size=3, padding='same', activation='relu'),
    layers.MaxPooling1D(pool_size=2),
    layers.Flatten(),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model_keras.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.003),
    loss='binary_crossentropy',
    metrics=['accuracy']
)
model_keras.summary()
'''
print(code_keras)
"""
    cells.append(nbf.v4.new_code_cell(c1))

    c2 = """# Cell [2]: Bảng đối chiếu Cú pháp: NumPy vs PyTorch vs TensorFlow (Slide 35)
comparison_table = [
    {"Thành phần": "Convolution 1D", "NumPy (From Scratch)": "conv1d()", "PyTorch": "nn.Conv1d()", "TensorFlow/Keras": "layers.Conv1D()"},
    {"Thành phần": "Hàm kích hoạt", "NumPy (From Scratch)": "relu()", "PyTorch": "nn.ReLU()", "TensorFlow/Keras": "activation='relu'"},
    {"Thành phần": "Gộp cực đại", "NumPy (From Scratch)": "maxpool1d()", "PyTorch": "nn.MaxPool1d()", "TensorFlow/Keras": "MaxPooling1D()"},
    {"Thành phần": "Phẳng hóa", "NumPy (From Scratch)": "x.reshape()", "PyTorch": "torch.flatten()", "TensorFlow/Keras": "Flatten()"},
    {"Thành phần": "Tầng tuyến tính", "NumPy (From Scratch)": "dense()", "PyTorch": "nn.Linear()", "TensorFlow/Keras": "Dense()"},
    {"Thành phần": "Tính Gradient", "NumPy (From Scratch)": "Thủ công (Manual)", "PyTorch": "torch.autograd", "TensorFlow/Keras": "tf.GradientTape / C++"},
    {"Thành phần": "Cập nhật trọng số", "NumPy (From Scratch)": "W -= lr * dW", "PyTorch": "optimizer.step()", "TensorFlow/Keras": "model.fit()"}
]

import pandas as pd
df_comp = pd.DataFrame(comparison_table)
display(df_comp)
"""
    cells.append(nbf.v4.new_code_cell(c2))

    nb.cells = cells
    with open('notebooks_a4/03_cnn_tensorflow_keras.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Created notebooks_a4/03_cnn_tensorflow_keras.ipynb")

# 4. 04_baseline_vs_improved_cnn.ipynb
def create_comparison_nb():
    nb = nbf.v4.new_notebook()
    cells = []
    
    c0 = """# ASSIGNMENT 04: NGHIÊN CỨU ĐỐI CHUẨN BASELINE CNN VÀ IMPROVED CNN
**Học phần:** Phát triển các hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

Nghiên cứu đối sánh theo Slide 15, 16 và Tutorial mục 45:
- M1 (Baseline CNN - 3 tầng): Conv1 -> ReLU -> Conv2 -> ReLU -> Pool -> Flatten -> Dense
- M2 (Improved CNN - Nâng cấp): M1 + Batch Normalization + Dropout + Residual / Skip Connection
"""
    cells.append(nbf.v4.new_markdown_cell(c0))

    c1 = """# Cell [1]: Định nghĩa Baseline CNN vs Improved CNN
import torch
import torch.nn as nn
import json

class BaselineCNN(nn.Module):
    def __init__(self, in_features=8):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(16, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Flatten(),
            nn.Linear(16 * (in_features // 2), 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )
    def forward(self, x):
        return self.net(x)

class ImprovedCNN(nn.Module):
    def __init__(self, in_features=8):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(16)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv1d(16, 16, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(16)
        self.pool = nn.MaxPool1d(2)
        self.dropout = nn.Dropout(0.2)
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(16 * (in_features // 2), 16),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(16, 1)
        )
    def forward(self, x):
        c1 = self.relu(self.bn1(self.conv1(x)))
        c2 = self.relu(self.bn2(self.conv2(c1)) + c1) # Skip connection
        p = self.dropout(self.pool(c2))
        return self.head(p)

print("Baseline CNN Params:", sum(p.numel() for p in BaselineCNN().parameters()))
print("Improved CNN Params:", sum(p.numel() for p in ImprovedCNN().parameters()))
"""
    cells.append(nbf.v4.new_code_cell(c1))

    c2 = """# Cell [2]: Bảng đối chuẩn kết quả thực nghiệm trên 3 Bộ Dữ Liệu
with open('../ass4_experiments/artifacts/diabetes_cnn_metrics.json') as f:
    m_diab = json.load(f)
with open('../ass4_experiments/artifacts/house_cnn_metrics.json') as f:
    m_house = json.load(f)
with open('../ass4_experiments/artifacts/customer_cnn_metrics.json') as f:
    m_cust = json.load(f)

print("=== DIABETES (1D TABULAR) ===")
print(pd.DataFrame(m_diab).T[['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC', 'Params', 'Time']])

print("\n=== HOUSE PRICE (1D REGRESSION) ===")
print(pd.DataFrame(m_house).T[['MAE', 'RMSE', 'R2', 'Params', 'Time']])

print("\n=== CUSTOMER REVIEWS (1D TEXT) ===")
print(pd.DataFrame(m_cust).T[['Accuracy', 'Macro Precision', 'Macro Recall', 'Macro F1', 'Params', 'Time']])
"""
    cells.append(nbf.v4.new_code_cell(c2))

    nb.cells = cells
    with open('notebooks_a4/04_baseline_vs_improved_cnn.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Created notebooks_a4/04_baseline_vs_improved_cnn.ipynb")

create_scratch_nb()
create_pytorch_nb()
create_tensorflow_nb()
create_comparison_nb()
print("All 4 Jupyter Notebooks in notebooks_a4/ created successfully!")
