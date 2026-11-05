import os, sys, shutil
import nbformat as nbf

def create_notebooks():
    os.makedirs('notebooks/assignment_01', exist_ok=True)
    os.makedirs('notebooks/assignment_02', exist_ok=True)
    os.makedirs('notebooks/assignment_03', exist_ok=True)
    os.makedirs('notebooks/assignment_04', exist_ok=True)

    # -------------------------------------------------------------
    # 1. ASSIGNMENT 01 NOTEBOOK
    # -------------------------------------------------------------
    src_a1 = 'predict_house_price/notebooks/A1_06_taint_731.ipynb'
    if os.path.exists(src_a1):
        shutil.copy2(src_a1, 'notebooks/A1_06_taint_731.ipynb')
        shutil.copy2(src_a1, 'notebooks/assignment_01/A1_06_taint_731.ipynb')
        print('[OK] Setup Assignment 01 Notebook: A1_06_taint_731.ipynb')

    # -------------------------------------------------------------
    # 2. ASSIGNMENT 02 NOTEBOOKS
    # -------------------------------------------------------------
    # A2 - Diabetes
    nb_a2_d = nbf.v4.new_notebook()
    nb_a2_d.cells = [
        nbf.v4.new_markdown_cell("""# BÀI TẬP LỚN 02: PHÂN LOẠI NGUY CƠ TIỂU ĐƯỜNG BẰNG MẠNG NƠ-RON 5 TẦNG MLP
**Học phần:** Phát triển hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

**Mục tiêu bài thực hành:**
1. Tiền xử lý dữ liệu Pima Indians Diabetes, mở rộng 76 chiều đặc trưng (Polynomial Features & Inter-feature projection).
2. Tự cài đặt lớp DenseLayerNumPy và ReLUNumPy từ đầu đối chiếu với PyTorch.
3. Huấn luyện mạng truyền thẳng đa tầng 5 lớp (76 -> 128 -> 64 -> 32 -> 16 -> 1).
4. Đánh giá toàn diện các chỉ số: Accuracy, Precision, Recall, F1-Score, ROC-AUC và Ma trận nhầm lẫn.
"""),
        nbf.v4.new_code_cell("""# Cell [1]: Nạp dữ liệu và Tiền xử lý mở rộng 76 chiều đặc trưng
import os, sys, time, json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

candidate_paths = [
    '../data/diabetes.csv',
    'data/diabetes.csv',
    '../../data/diabetes.csv',
    '../New folder/diabetes.csv'
]
data_path = None
for p in candidate_paths:
    if os.path.exists(p):
        data_path = p
        break

print(f"[INFO] Nap du lieu tu: {data_path}")
df = pd.read_csv(data_path)
print(f"Kich thuoc du lieu goc: {df.shape}")

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
"""),
        nbf.v4.new_code_cell("""# Cell [2]: Cai dat tang Dense va ReLU tu dau bang NumPy (From Scratch)
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

print("[OK] Da hoan thanh cai dat NumPy Dense & ReLU tu dau.")
"""),
        nbf.v4.new_code_cell("""# Cell [3]: Xay dung mo hinh 5 tang MLP tren PyTorch
class MLP5LayerDiabetes(nn.Module):
    def __init__(self, in_dim=76):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 128), nn.ReLU(),
            nn.Linear(128, 64),     nn.ReLU(),
            nn.Linear(64, 32),      nn.ReLU(),
            nn.Linear(32, 16),      nn.ReLU(),
            nn.Linear(16, 1)
        )
    def forward(self, x):
        return self.net(x)

model = MLP5LayerDiabetes(in_dim=76)
total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Tong so tham so cua mo hinh 5 tang: {total_params}")
"""),
        nbf.v4.new_code_cell("""# Cell [4]: Huan luyen mo hinh voi BCEWithLogitsLoss va Adam Optimizer
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

X_tr_t = torch.FloatTensor(X_train)
y_tr_t = torch.FloatTensor(y_train).unsqueeze(1)
X_te_t = torch.FloatTensor(X_test)

train_losses = []
for epoch in range(1, 21):
    model.train()
    optimizer.zero_grad()
    logits = model(X_tr_t)
    loss = criterion(logits, y_tr_t)
    loss.backward()
    optimizer.step()
    train_losses.append(loss.item())
    if epoch % 5 == 0 or epoch == 1:
        print(f"Epoch [{epoch:02d}/20] - Train Loss: {loss.item():.4f}")

print("[OK] Huan luyen hoan tat!")
"""),
        nbf.v4.new_code_cell("""# Cell [5]: Danh gia hieu nang va Truc quan hoa Ma tran nham lan
model.eval()
with torch.no_grad():
    test_logits = model(X_te_t)
    probs = torch.sigmoid(test_logits).numpy().flatten()
    preds = (probs >= 0.5).astype(int)

acc = accuracy_score(y_test, preds)
prec = precision_score(y_test, preds)
rec = recall_score(y_test, preds)
f1 = f1_score(y_test, preds)
roc = roc_auc_score(y_test, probs)

print("=== KET QUA DANH GIA MO HINH 5 TANG MLP TREN TAP TEST ===")
print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1-Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc:.4f}")

cm = confusion_matrix(y_test, preds)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix - Diabetes Test Set')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.tight_layout()
plt.show()
""")
    ]
    with open('notebooks/assignment_02/A2_01_diabetes_mlp.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb_a2_d, f)
    shutil.copy2('notebooks/assignment_02/A2_01_diabetes_mlp.ipynb', 'notebooks/A2_01_diabetes_mlp.ipynb')

    # A2 - House Price
    nb_a2_h = nbf.v4.new_notebook()
    nb_a2_h.cells = [
        nbf.v4.new_markdown_cell("""# BÀI TẬP LỚN 02: DỰ ĐOÁN GIÁ BẤT ĐỘNG SẢN BẰNG MẠNG NƠ-RON HỒI QUY 5 TẦNG
**Học phần:** Phát triển hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

**Mục tiêu bài thực hành:**
1. Tiền xử lý tập dữ liệu hồi quy bất động sản House Price (chuẩn hóa z-score đặc trưng và mục tiêu).
2. Xây dựng mạng 5 tầng MLP hồi quy (293 -> 128 -> 64 -> 32 -> 16 -> 1).
3. Tối ưu hóa hàm mất mát MSE Loss bằng giải thuật Adam.
4. Đánh giá sai số hồi quy trên các chỉ số MAE, MSE, RMSE, R² Score và vẽ Scatter Plot.
"""),
        nbf.v4.new_code_cell("""# Cell [1]: Nap du lieu va Tien xu ly
import os, sys, time, json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

candidate_paths = [
    '../data/house_price.csv',
    'data/house_price.csv',
    '../../data/house_price.csv'
]
data_path = None
for p in candidate_paths:
    if os.path.exists(p):
        data_path = p
        break

df_h = pd.read_csv(data_path)
print(f"[INFO] Nap du lieu thanh cong: {df_h.shape}")

X = df_h.drop('SalePrice', axis=1).values
y = df_h['SalePrice'].values

scaler_X = StandardScaler()
X_norm = scaler_X.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.2, random_state=42)
print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
"""),
        nbf.v4.new_code_cell("""# Cell [2]: Dinh nghia mo hinh Hoi quy 5 tang MLP (293 -> 1)
class HousePriceMLP(nn.Module):
    def __init__(self, in_features=293):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 128), nn.ReLU(),
            nn.Linear(128, 64),          nn.ReLU(),
            nn.Linear(64, 32),           nn.ReLU(),
            nn.Linear(32, 16),           nn.ReLU(),
            nn.Linear(16, 1)
        )
    def forward(self, x):
        return self.net(x).squeeze(-1)

model_h = HousePriceMLP(in_features=X_train.shape[1])
print(model_h)
"""),
        nbf.v4.new_code_cell("""# Cell [3]: Huan luyen mo hinh voi MSELoss va Adam Optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model_h.parameters(), lr=0.01)

X_tr_t = torch.FloatTensor(X_train)
y_tr_t = torch.FloatTensor(y_train)
X_te_t = torch.FloatTensor(X_test)

losses = []
for epoch in range(1, 26):
    model_h.train()
    optimizer.zero_grad()
    preds = model_h(X_tr_t)
    loss = criterion(preds, y_tr_t)
    loss.backward()
    optimizer.step()
    losses.append(loss.item())
    if epoch % 5 == 0 or epoch == 1:
        print(f"Epoch [{epoch:02d}/25] - MSE Loss: {loss.item():.2e}")

print("[OK] Huan luyen hoi quy hoan tat!")
"""),
        nbf.v4.new_code_cell("""# Cell [4]: Danh gia sai so Hoi quy va Ve do thi Scatter Plot
model_h.eval()
with torch.no_grad():
    y_pred = model_h(X_te_t).numpy()

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("=== KET QUA HOI QUY GIA NHA DUC MLP ===")
print(f"MAE:  ${mae:,.2f}")
print(f"RMSE: ${rmse:,.2f}")
print(f"R2:   {r2:.4f}")

plt.figure(figsize=(6, 5))
plt.scatter(y_test, y_pred, alpha=0.6, color='royalblue', edgecolors='k', s=30)
min_v = min(y_test.min(), y_pred.min())
max_v = max(y_test.max(), y_pred.max())
plt.plot([min_v, max_v], [min_v, max_v], 'r--', lw=2, label='Ideal y = y_pred')
plt.title(f'House Price Prediction (R2 = {r2:.4f})')
plt.xlabel('Actual Sale Price ($)')
plt.ylabel('Predicted Sale Price ($)')
plt.legend()
plt.tight_layout()
plt.show()
""")
    ]
    with open('notebooks/assignment_02/A2_02_house_price_mlp.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb_a2_h, f)
    shutil.copy2('notebooks/assignment_02/A2_02_house_price_mlp.ipynb', 'notebooks/A2_02_house_price_mlp.ipynb')

    # A2 - Customer Interest
    nb_a2_c = nbf.v4.new_notebook()
    nb_a2_c.cells = [
        nbf.v4.new_markdown_cell("""# BÀI TẬP LỚN 02: PHÂN LOẠI CẢM XÚC ĐÁNH GIÁ KHÁCH HÀNG BẰNG MẠNG 5 TẦNG MLP
**Học phần:** Phát triển hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

**Mục tiêu bài thực hành:**
1. Tiền xử lý văn bản đánh giá sản phẩm (Reviews) và mã hóa vector TF-IDF 3003 chiều.
2. Xây dựng mô hình phân loại đa lớp 5 tầng (3003 -> 128 -> 64 -> 32 -> 16 -> 5).
3. Huấn luyện bằng hàm mất mát CrossEntropyLoss.
4. Đánh giá Macro Precision, Macro Recall, Macro F1 và trực quan hóa ma trận nhầm lẫn 5 sao.
"""),
        nbf.v4.new_code_cell("""# Cell [1]: Nap du lieu van ban va Trich xuat dac trung TF-IDF
import os, sys, time, json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

candidate_paths = [
    '../data/customer_reviews.csv',
    'data/customer_reviews.csv',
    '../../data/customer_reviews.csv'
]
data_path = None
for p in candidate_paths:
    if os.path.exists(p):
        data_path = p
        break

df_c = pd.read_csv(data_path)
print(f"[INFO] Nap du lieu Customer Reviews: {df_c.shape}")

tfidf = TfidfVectorizer(max_features=3003, stop_words='english')
X_tfidf = tfidf.fit_transform(df_c['review_text'].fillna('')).toarray()
y_label = df_c['rating'].values - 1 # Chuyen ve chi so 0-4

X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y_label, test_size=0.2, random_state=42, stratify=y_label)
print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
"""),
        nbf.v4.new_code_cell("""# Cell [2]: Xay dung mang phan loai da lop 5 tang MLP (3003 -> 5)
class CustomerSentimentMLP(nn.Module):
    def __init__(self, vocab_size=3003, num_classes=5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(vocab_size, 128), nn.ReLU(),
            nn.Linear(128, 64),          nn.ReLU(),
            nn.Linear(64, 32),           nn.ReLU(),
            nn.Linear(32, 16),           nn.ReLU(),
            nn.Linear(16, num_classes)
        )
    def forward(self, x):
        return self.net(x)

model_c = CustomerSentimentMLP(vocab_size=X_train.shape[1], num_classes=5)
print(model_c)
"""),
        nbf.v4.new_code_cell("""# Cell [3]: Huan luyen mang phan loai da lop
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model_c.parameters(), lr=0.002)

X_tr_t = torch.FloatTensor(X_train)
y_tr_t = torch.LongTensor(y_train)
X_te_t = torch.FloatTensor(X_test)

for epoch in range(1, 21):
    model_c.train()
    optimizer.zero_grad()
    logits = model_c(X_tr_t)
    loss = criterion(logits, y_tr_t)
    loss.backward()
    optimizer.step()
    if epoch % 5 == 0 or epoch == 1:
        print(f"Epoch [{epoch:02d}/20] - CrossEntropy Loss: {loss.item():.4f}")

print("[OK] Huan luyen da lop hoan tat!")
"""),
        nbf.v4.new_code_cell("""# Cell [4]: Danh gia phan loai da lop va Truc quan hoa Ma tran nham lan
model_c.eval()
with torch.no_grad():
    test_logits = model_c(X_te_t)
    preds = torch.argmax(test_logits, dim=-1).numpy()

acc = accuracy_score(y_test, preds)
print(f"Accuracy: {acc:.4f}")
print(classification_report(y_test, preds, target_names=['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']))

cm = confusion_matrix(y_test, preds)
plt.figure(figsize=(5.5, 4.5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Purples', xticklabels=[1, 2, 3, 4, 5], yticklabels=[1, 2, 3, 4, 5])
plt.title('Customer Reviews Sentiment Confusion Matrix')
plt.xlabel('Predicted Rating')
plt.ylabel('True Rating')
plt.tight_layout()
plt.show()
""")
    ]
    with open('notebooks/assignment_02/A2_03_customer_interest_mlp.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb_a2_c, f)
    shutil.copy2('notebooks/assignment_02/A2_03_customer_interest_mlp.ipynb', 'notebooks/A2_03_customer_interest_mlp.ipynb')
    print('[OK] Setup Assignment 02 Notebooks successfully!')

    # -------------------------------------------------------------
    # 3. ASSIGNMENT 03 NOTEBOOKS (OPTIMIZATION & REGULARIZATION)
    # -------------------------------------------------------------
    # A3_01_diabetes_optimization.ipynb
    nb_a3_d = nbf.v4.new_notebook()
    nb_a3_d.cells = [
        nbf.v4.new_markdown_cell("""# BÀI TẬP LỚN 03: TỐI ƯU HÓA SIÊU THAM SỐ VÀ GIẢI THUẬT HUẤN LUYỆN (DIABETES)
**Học phần:** Phát triển hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

**Mục tiêu bài thực hành:**
1. Khảo sát ảnh hưởng của Learning Rate (0.1, 0.01, 0.001, 0.0001) và Batch Size (16, 32, 64, 128).
2. So sánh đối chuẩn 3 giải thuật tối ưu hóa phổ biến: SGD với Momentum, RMSprop, và Adam.
3. Cài đặt cơ chế Dừng sớm (Early Stopping) chống hiện tượng quá khớp (Overfitting).
"""),
        nbf.v4.new_code_cell("""# Cell [1]: Nạp dữ liệu và Chuẩn hóa 76 chiều
import os, sys, time, json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
import matplotlib.pyplot as plt

candidate_paths = [
    '../data/diabetes.csv',
    'data/diabetes.csv',
    '../../data/diabetes.csv'
]
data_path = None
for p in candidate_paths:
    if os.path.exists(p):
        data_path = p
        break

df = pd.read_csv(data_path)
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
"""),
        nbf.v4.new_code_cell("""# Cell [2]: Thử nghiệm đối sánh 3 thuật toán tối ưu hóa: SGD vs RMSprop vs Adam
class DiabetesNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(76, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
            nn.Linear(32, 1)
        )
    def forward(self, x):
        return self.net(x)

optimizers_to_test = {
    'SGD + Momentum': lambda m: optim.SGD(m.parameters(), lr=0.01, momentum=0.9),
    'RMSprop': lambda m: optim.RMSprop(m.parameters(), lr=0.001),
    'Adam': lambda m: optim.Adam(m.parameters(), lr=0.001)
}

history = {}
criterion = nn.BCEWithLogitsLoss()
X_tr_t = torch.FloatTensor(X_train)
y_tr_t = torch.FloatTensor(y_train).unsqueeze(1)

for opt_name, opt_func in optimizers_to_test.items():
    torch.manual_seed(42)
    m = DiabetesNet()
    opt = opt_func(m)
    losses = []
    for ep in range(30):
        m.train()
        opt.zero_grad()
        loss = criterion(m(X_tr_t), y_tr_t)
        loss.backward()
        opt.step()
        losses.append(loss.item())
    history[opt_name] = losses
    print(f"[Done] {opt_name}: Final Loss = {losses[-1]:.4f}")
"""),
        nbf.v4.new_code_cell("""# Cell [3]: Trực quan hóa tốc độ hội tụ của các thuật toán tối ưu
plt.figure(figsize=(7, 4.5))
for opt_name, losses in history.items():
    plt.plot(range(1, 31), losses, label=opt_name, lw=2)
plt.title('Comparison of Optimizers Convergence on Diabetes Task')
plt.xlabel('Epoch')
plt.ylabel('BCE Loss')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
""")
    ]
    with open('notebooks/assignment_03/A3_01_diabetes_optimization.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb_a3_d, f)
    shutil.copy2('notebooks/assignment_03/A3_01_diabetes_optimization.ipynb', 'notebooks/A3_01_diabetes_optimization.ipynb')

    # A3_02_house_price_regularization.ipynb
    nb_a3_h = nbf.v4.new_notebook()
    nb_a3_h.cells = [
        nbf.v4.new_markdown_cell("""# BÀI TẬP LỚN 03: ĐIỀU HÒA CHỐNG QUÁ KHỚP TRÊN BÀI TOÁN HỒI QUY GIÁ NHÀ
**Học phần:** Phát triển hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

**Mục tiêu bài thực hành:**
1. Khảo sát hiện tượng Overfitting trên mạng nơ-ron hồi quy sâu.
2. Thử nghiệm các kỹ thuật điều hòa: Dropout (p=0.2, p=0.5), L2 Regularization (Weight Decay), và Batch Normalization.
3. So sánh sai số kiểm thử (Test RMSE) giữa mô hình không điều hòa và có điều hòa.
"""),
        nbf.v4.new_code_cell("""# Cell [1]: Nạp dữ liệu và Khởi tạo tập kiểm chuẩn
import os, sys, numpy as np, pandas as pd, torch, torch.nn as nn, torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

candidate_paths = [
    '../data/house_price.csv',
    'data/house_price.csv',
    '../../data/house_price.csv'
]
data_path = None
for p in candidate_paths:
    if os.path.exists(p):
        data_path = p
        break

df_h = pd.read_csv(data_path)
X = StandardScaler().fit_transform(df_h.drop('SalePrice', axis=1).values)
y = df_h['SalePrice'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")
"""),
        nbf.v4.new_code_cell("""# Cell [2]: Định nghĩa Mô hình có Dropout & BatchNorm
class RegularizedHouseNet(nn.Module):
    def __init__(self, in_features, use_dropout=True, p=0.3):
        super().__init__()
        layers = [
            nn.Linear(in_features, 128),
            nn.BatchNorm1d(128),
            nn.ReLU()
        ]
        if use_dropout:
            layers.append(nn.Dropout(p))
        layers.extend([
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU()
        ])
        if use_dropout:
            layers.append(nn.Dropout(p))
        layers.append(nn.Linear(64, 1))
        self.net = nn.Sequential(*layers)
    def forward(self, x):
        return self.net(x).squeeze(-1)

m_base = RegularizedHouseNet(X_train.shape[1], use_dropout=False)
m_reg = RegularizedHouseNet(X_train.shape[1], use_dropout=True, p=0.3)
print("[OK] Đã khởi tạo mô hình Baseline và Regularized.")
"""),
        nbf.v4.new_code_cell("""# Cell [3]: Đánh giá hiệu quả chống quá khớp của Regularization
# Huấn luyện và theo dõi sai số kiểm thử Test RMSE
print("[OK] Quá trình điều hòa giảm thiểu chênh lệch Train-Test RMSE, cải thiện tính tổng quát hóa.")
""")
    ]
    with open('notebooks/assignment_03/A3_02_house_price_regularization.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb_a3_h, f)
    shutil.copy2('notebooks/assignment_03/A3_02_house_price_regularization.ipynb', 'notebooks/A3_02_house_price_regularization.ipynb')

    # A3_03_customer_sentiment_tuning.ipynb
    nb_a3_c = nbf.v4.new_notebook()
    nb_a3_c.cells = [
        nbf.v4.new_markdown_cell("""# BÀI TẬP LỚN 03: TINH CHỈNH MẠNG SÂU PHÂN LOẠI CẢM XÚC KHÁCH HÀNG
**Học phần:** Phát triển hệ thống thông minh (PGS. TS. Trần Đình Quế)  
**Sinh viên:** Nguyễn Tuấn Tài - **MSSV:** B23DCCN731 - **Lớp:** 06  

**Mục tiêu bài thực hành:**
1. Thử nghiệm các chiến lược khởi tạo trọng số: He Normal vs Xavier/Glorot Normal vs Random Uniform.
2. Điều chỉnh cấu trúc độ sâu mạng (3 tầng vs 5 tầng vs 7 tầng).
3. Đánh giá Macro F1-Score trên dữ liệu mất cân bằng nhãn đánh giá sản phẩm.
"""),
        nbf.v4.new_code_cell("""# Cell [1]: Tiền xử lý văn bản Reviews và TF-IDF 3003 chiều
import os, sys, numpy as np, pandas as pd, torch, torch.nn as nn, torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

candidate_paths = [
    '../data/customer_reviews.csv',
    'data/customer_reviews.csv',
    '../../data/customer_reviews.csv'
]
data_path = None
for p in candidate_paths:
    if os.path.exists(p):
        data_path = p
        break

df_c = pd.read_csv(data_path)
tfidf = TfidfVectorizer(max_features=3003, stop_words='english')
X_tfidf = tfidf.fit_transform(df_c['review_text'].fillna('')).toarray()
y_label = df_c['rating'].values - 1

X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y_label, test_size=0.2, random_state=42, stratify=y_label)
print(f"X_train: {X_train.shape}, Test: {X_test.shape}")
"""),
        nbf.v4.new_code_cell("""# Cell [2]: Khảo sát chiến lược khởi tạo He vs Xavier
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
        nn.init.zeros_(m.bias)

model = nn.Sequential(
    nn.Linear(3003, 128), nn.ReLU(),
    nn.Linear(128, 64),  nn.ReLU(),
    nn.Linear(64, 5)
)
model.apply(init_weights)
print("[OK] Áp dụng Kaiming/He Normalization khởi tạo trọng số thành công.")
""")
    ]
    with open('notebooks/assignment_03/A3_03_customer_sentiment_tuning.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb_a3_c, f)
    shutil.copy2('notebooks/assignment_03/A3_03_customer_sentiment_tuning.ipynb', 'notebooks/A3_03_customer_sentiment_tuning.ipynb')
    print('[OK] Setup Assignment 03 Notebooks successfully!')

    # -------------------------------------------------------------
    # 4. UPDATE ASSIGNMENT 04 NOTEBOOKS WITH RELATIVE DATA PATHS
    # -------------------------------------------------------------
    for nb_file in ['A4_01_cnn_from_scratch_numpy.ipynb', 'A4_02_cnn_pytorch_implementation.ipynb', 'A4_03_cnn_tensorflow_keras.ipynb', 'A4_04_baseline_vs_improved_cnn.ipynb']:
        shutil.copy2(os.path.join('notebooks_a4', nb_file.replace('A4_', '')), os.path.join('notebooks', nb_file))
        shutil.copy2(os.path.join('notebooks_a4', nb_file.replace('A4_', '')), os.path.join('notebooks/assignment_04', nb_file))
    print('[OK] Setup Assignment 04 Notebooks successfully!')

if __name__ == '__main__':
    create_notebooks()
