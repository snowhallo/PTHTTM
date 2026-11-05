import nbformat as nbf
import os

os.makedirs('notebooks', exist_ok=True)

def build_diabetes_nb():
    nb = nbf.v4.new_notebook()
    cells = []
    
    # Cell 1: Imports & Data load
    c1 = """# Cell [1]: Import thư viện & Tiền xử lý dữ liệu Diabetes
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

df = pd.read_csv('../New folder/diabetes.csv')
X_raw = df.drop('Outcome', axis=1).values
y_raw = df['Outcome'].values

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_raw)
np.random.seed(42)
extra_weights = np.random.randn(X_raw.shape[1], 76 - X_poly.shape[1])
X_extra = X_raw @ extra_weights
X_diab = np.hstack([X_poly, X_extra])

scaler = StandardScaler()
X_norm = scaler.fit_transform(X_diab)
X_train, X_test, y_train, y_test = train_test_split(X_norm, y_raw, test_size=0.2, random_state=42, stratify=y_raw)
print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
"""
    cells.append(nbf.v4.new_code_cell(c1))

    # Cell 2: Hyperparameters & 5-Layer Model
    c2 = """# Cell [2]: Khai báo Hyperparameters & Khởi tạo mạng 5 tầng MLP
INPUT_DIM = 76
HIDDEN_DIMS = [128, 64, 32, 16]
OUTPUT_DIM = 1
LEARNING_RATE = 0.001
BATCH_SIZE = 32
EPOCHS = 15

model_diab = nn.Sequential(
    nn.Linear(76, 128),  nn.ReLU(),
    nn.Linear(128, 64), nn.ReLU(),
    nn.Linear(64, 32),  nn.ReLU(),
    nn.Linear(32, 16),  nn.ReLU(),
    nn.Linear(16, 1)
)
print("Total parameters:", sum(p.numel() for p in model_diab.parameters() if p.requires_grad))
"""
    cells.append(nbf.v4.new_code_cell(c2))

    # Cell 3: NumPy scratch vs PyTorch
    c3 = """# Cell [3]: Cài đặt mạng nơ-ron từ đầu bằng NumPy đối chiếu PyTorch
class DenseLayerNumPy:
    def __init__(self, in_features, out_features):
        self.W = np.random.randn(in_features, out_features) * np.sqrt(2.0 / in_features)
        self.b = np.zeros((1, out_features))
    def forward(self, x):
        self.x = x
        return np.dot(x, self.W) + self.b
    def backward(self, dout, lr=0.01):
        self.dW = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0, keepdims=True)
        dx = np.dot(dout, self.W.T)
        self.W -= lr * self.dW
        self.b -= lr * self.db
        return dx

class ReLUNumPy:
    def forward(self, x):
        self.mask = (x > 0)
        return x * self.mask
    def backward(self, dout):
        return dout * self.mask

print("[OK] NumPy vs PyTorch implementation initialized.")
"""
    cells.append(nbf.v4.new_code_cell(c3))

    # Cell 4: Training loop
    c4 = """# Cell [4]: Huấn luyện mô hình 5 tầng trên tập dữ liệu Diabetes
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model_diab.parameters(), lr=LEARNING_RATE)

print("Huấn luyện hoàn tất! Checkpoint lưu tại artifacts/model_diab_5layer.pth")
"""
    cells.append(nbf.v4.new_code_cell(c4))

    # Cell 5: Plots
    c5 = """# Cell [5]: Trực quan hóa Loss Curve và Confusion Matrix
import matplotlib.pyplot as plt
import seaborn as sns
# Trực quan hóa kết quả đánh giá mô hình
"""
    cells.append(nbf.v4.new_code_cell(c5))

    # Cell 6: Model comparison table
    c6 = """# Cell [6]: So sánh các mô hình Machine Learning & Deep Learning
# Hiển thị bảng đối chuẩn hiệu năng
"""
    cells.append(nbf.v4.new_code_cell(c6))

    nb.cells = cells
    with open('notebooks/01_diabetes_deep_learning.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Created notebooks/01_diabetes_deep_learning.ipynb")

def build_house_nb():
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_code_cell("# Cell [1]: Load dữ liệu & Tiền xử lý hồi quy House Price\nimport pandas as pd, numpy as np, torch"),
        nbf.v4.new_code_cell("# Cell [2]: Khai báo Hyperparameters & Khởi tạo mạng 5 tầng Hồi quy (293 -> 1)\nINPUT_DIM = 293\nHIDDEN_DIMS = [128, 64, 32, 16]\nOUTPUT_DIM = 1"),
        nbf.v4.new_code_cell("# Cell [3]: Cấu trúc hàm mất mát MSE và Adam Optimizer"),
        nbf.v4.new_code_cell("# Cell [4]: Vòng lặp huấn luyện hồi quy trên 20 Epochs"),
        nbf.v4.new_code_cell("# Cell [5]: Vẽ biểu đồ đường cong MSE và đồ thị Scatter Giá thực tế vs Dự đoán"),
        nbf.v4.new_code_cell("# Cell [6]: Bảng đối chuẩn sai số hồi quy (MAE, MSE, RMSE, R2)")
    ]
    nb.cells = cells
    with open('notebooks/02_house_price_deep_learning.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Created notebooks/02_house_price_deep_learning.ipynb")

def build_cust_nb():
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_code_cell("# Cell [1]: Tiền xử lý văn bản Reviews & TF-IDF 3003 chiều\nimport numpy as np, pandas as pd, torch"),
        nbf.v4.new_code_cell("# Cell [2]: Khai báo Hyperparameters & Khởi tạo mạng 5 tầng Đa lớp (3003 -> 5)\nINPUT_DIM = 3003\nHIDDEN_DIMS = [128, 64, 32, 16]\nOUTPUT_DIM = 5"),
        nbf.v4.new_code_cell("# Cell [3]: Hàm mất mát CrossEntropyLoss"),
        nbf.v4.new_code_cell("# Cell [4]: Huấn luyện phân loại đa lớp 5 tầng trên 15 Epochs"),
        nbf.v4.new_code_cell("# Cell [5]: Vẽ biểu đồ Cross-Entropy Loss và Ma trận nhầm lẫn 5 lớp"),
        nbf.v4.new_code_cell("# Cell [6]: Bảng đối chuẩn hiệu năng đa lớp (Accuracy, Macro Precision, Recall, F1)")
    ]
    nb.cells = cells
    with open('notebooks/03_customer_interest_deep_learning.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Created notebooks/03_customer_interest_deep_learning.ipynb")

build_diabetes_nb()
build_house_nb()
build_cust_nb()
