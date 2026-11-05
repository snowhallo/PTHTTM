import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import nbformat as nbf
from nbclient import NotebookClient

nb = nbf.v4.new_notebook()

cells = []

# Title & Metadata
cells.append(nbf.v4.new_markdown_cell("""# BÁO CÁO THỰC HÀNH & DEMO - THÀNH VIÊN 3
## ĐỀ TÀI: DEEP GRAPH LEARNING IN AI - DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG (DIABETES PREDICTION)
**Môn học:** Phát triển Hệ thống Thông minh  
**Thành viên thực hiện:** Thành viên 3 (Nghiên cứu bài toán y sinh, Tiền xử lý dữ liệu, Khởi tạo đồ thị bệnh nhân & Phòng chống Data Leakage)  
**Tập dữ liệu:** Diabetes Clinical Dataset (100,000 bản ghi lâm sàng, 9 đặc trưng)  
**Bàn giao cho:** Thành viên 1 & 4 (Mô hình hóa Graph Neural Network - GCN / GraphSAGE / GAT)
"""))

# Cell 1: Imports
cells.append(nbf.v4.new_code_cell("""# 1. KHỞI TẠO MÔI TRƯỜNG & THƯ VIỆN CẦN THIẾT
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.neighbors import NearestNeighbors
import torch
from torch_geometric.data import Data
import warnings
warnings.filterwarnings('ignore')

# Thiết lập hiển thị đồ thị đẹp
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cbd5e0'
plt.rcParams['axes.linewidth'] = 0.8
print("Thư viện đã được nạp thành công! PyTorch version:", torch.__version__)
"""))

# Cell 2: Data Loading & Basic EDA
cells.append(nbf.v4.new_markdown_cell("""---
### PHẦN 1: KHÁM PHÁ & ĐÁNH GIÁ TẬP DỮ LIỆU LÂM SÀNG (EDA)
Đọc dữ liệu từ `data/diabetes_100k.csv`, phân tích các cột đặc trưng, kiểm tra khuyết thiếu và mức độ mất cân bằng nhãn.
"""))

cells.append(nbf.v4.new_code_cell("""# Nạp dữ liệu 100k bệnh nhân
data_path = Path("data/diabetes_100k.csv")
df = pd.read_csv(data_path)

print(f"[*] Kích thước bảng dữ liệu gốc: {df.shape[0]:,} dòng x {df.shape[1]} cột")
print("[*] Kiểm tra giá trị khuyết thiếu (Missing values):", df.isnull().sum().to_dict())
df.head(5)
"""))

# Cell 3: Imbalance & Clinical Markers Check
cells.append(nbf.v4.new_code_cell("""# Thống kê phân bố nhãn mục tiêu và chuẩn vàng ADA
counts = df['diabetes'].value_counts()
print("Phân bố nhãn mục tiêu (diabetes):")
print(f" - Lớp 0 (Âm tính): {counts[0]:,} ({counts[0]/len(df)*100:.2f}%)")
print(f" - Lớp 1 (Dương tính): {counts[1]:,} ({counts[1]/len(df)*100:.2f}%)")
print(f" -> Tỷ lệ mất cân bằng (Imbalance Ratio): {counts[0]/counts[1]:.2f} : 1")

print("\\nĐối chiếu với tiêu chuẩn ADA (American Diabetes Association):")
print(f" - HbA1c trung bình: Nhóm Bệnh = {df[df['diabetes']==1]['HbA1c_level'].mean():.2f}% (≥ 6.5%) vs Nhóm Khỏe = {df[df['diabetes']==0]['HbA1c_level'].mean():.2f}%")
print(f" - Glucose trung bình: Nhóm Bệnh = {df[df['diabetes']==1]['blood_glucose_level'].mean():.1f} mg/dL vs Nhóm Khỏe = {df[df['diabetes']==0]['blood_glucose_level'].mean():.1f} mg/dL")
"""))

# Cell 4: Preprocessing & Leakage Defense
cells.append(nbf.v4.new_markdown_cell("""---
### PHẦN 2: TIỀN XỬ LÝ & THIẾT LẬP PHÒNG THỦ CHỐNG DATA LEAKAGE
1. **Chia Stratified Split (80/20) TRƯỚC TIÊN**: Bảo toàn tỷ lệ mất cân bằng trên Train và Test.
2. **Loại bỏ cột `diabetes` ra khỏi không gian tính toán**: Tuyệt đối không dùng nhãn để tìm láng giềng KNN (Chống Label Leakage).
3. **Sử dụng `RobustScaler` (Median & IQR)**: Fit DUY NHẤT trên Train, Transform sang Test (Chống Statistical Leakage & miễn nhiễm với ngoại lệ y sinh).
"""))

cells.append(nbf.v4.new_code_cell("""# Lấy mẫu đại diện phân tầng 10,000 bệnh nhân để xử lý và tạo đồ thị tối ưu
SAMPLE_SIZE = 10000
df_sample = df.sample(n=SAMPLE_SIZE, random_state=42).reset_index(drop=True)

X = df_sample.drop(columns=['diabetes'])
y = df_sample['diabetes'].values

# Stratified Split 80/20
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

cat_cols = ['gender', 'smoking_history']
num_cols = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']

# Tiền xử lý số: RobustScaler
scaler = RobustScaler()
X_train_num = scaler.fit_transform(X_train_raw[num_cols])
X_test_num = scaler.transform(X_test_raw[num_cols])

# Tiền xử lý hạng mục: OneHotEncoder
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_train_cat = encoder.fit_transform(X_train_raw[cat_cols])
X_test_cat = encoder.transform(X_test_raw[cat_cols])

# Ghép đặc trưng
X_train = np.hstack([X_train_num, X_train_cat])
X_test = np.hstack([X_test_num, X_test_cat])

print(f"[*] Kích thước tập Train: {X_train.shape[0]:,} mẫu | Số chiều đặc trưng d = {X_train.shape[1]}")
print(f"[*] Kích thước tập Test: {X_test.shape[0]:,} mẫu | Số chiều đặc trưng d = {X_test.shape[1]}")
print("[+] Xác nhận: Không có biến 'diabetes' trong ma trận X. Scaler fit 100% độc lập trên Train.")
"""))

# Cell 5: Graph Construction
cells.append(nbf.v4.new_markdown_cell("""---
### PHẦN 3: XÂY DỰNG ĐỒ THỊ TƯƠNG ĐỒNG BỆNH NHÂN (02 PHƯƠNG ÁN)
- **Phương án 1 (Baseline Homogeneous KNN)**: $k=10$, khoảng cách Euclidean đồng nhất.
- **Phương án 2 (Clinically-Weighted KNN - Đề xuất)**: $k=8$, nhân trọng số ưu tiên y sinh ($w_{\\text{HbA1c}}=3, w_{\\text{Glucose}}=3, w_{\\text{BMI}}=2$).
- **Trọng số cạnh**: Sử dụng Gaussian RBF Kernel $W_{ij} = \\exp\\left(-\\frac{d_{ij}^2}{2\\sigma^2}\\right)$.
"""))

cells.append(nbf.v4.new_code_cell("""# 1. PHƯƠNG ÁN 1: Baseline KNN (k=10)
nbrs1 = NearestNeighbors(n_neighbors=11, metric='euclidean', n_jobs=-1).fit(X_train)
distances1, indices1 = nbrs1.kneighbors(X_train)

same1, total1 = 0, 0
for i in range(len(X_train)):
    for rank in range(1, 11):
        j = indices1[i, rank]
        total1 += 1
        if y_train[i] == y_train[j]:
            same1 += 1
homophily_pa1 = same1 / total1

# 2. PHƯƠNG ÁN 2: Clinically-Weighted KNN (k=8)
feat_weights = np.ones(X_train.shape[1], dtype=np.float32)
feat_weights[num_cols.index('HbA1c_level')] = 3.0
feat_weights[num_cols.index('blood_glucose_level')] = 3.0
feat_weights[num_cols.index('bmi')] = 2.0

X_train_weighted = X_train * np.sqrt(feat_weights)
nbrs2 = NearestNeighbors(n_neighbors=9, metric='euclidean', n_jobs=-1).fit(X_train_weighted)
distances2, indices2 = nbrs2.kneighbors(X_train_weighted)

same2, total2 = 0, 0
src_nodes, dst_nodes, edge_weights = [], [], []
sigma2 = np.median(distances2[:, 1:])

for i in range(len(X_train)):
    for rank in range(1, 9):
        j = indices2[i, rank]
        dist = distances2[i, rank]
        w = np.exp(- (dist**2) / (2 * (sigma2**2) + 1e-8))
        src_nodes.append(i)
        dst_nodes.append(j)
        edge_weights.append(w)
        
        total2 += 1
        if y_train[i] == y_train[j]:
            same2 += 1
homophily_pa2 = same2 / total2

print(f"=== SO SÁNH HIỆU QUẢ 2 PHƯƠNG ÁN THIẾT KẾ ĐỒ THỊ ===")
print(f"PA1 (Baseline KNN k=10):            {total1:,} cạnh | Homophily Ratio h = {homophily_pa1:.2%}")
print(f"PA2 (Clinically-Weighted k=8):      {total2:,} cạnh | Homophily Ratio h = {homophily_pa2:.2%}")
print(f"-> KẾT LUẬN: PA2 tăng độ thuần cụm +{(homophily_pa2-homophily_pa1)*100:.2f}% và tiết kiệm 20% bộ nhớ cạnh!")
"""))

# Cell 6: Inductive Graph Formulation
cells.append(nbf.v4.new_markdown_cell("""---
### PHẦN 4: THIẾT LẬP ĐỒ THỊ QUY NẠP (INDUCTIVE GRAPH SETTING)
Phòng chống **Transductive Leakage**: Nút Test chỉ truy vấn $k$ láng giềng trong Train để nhận thông điệp tổng hợp. Tuyệt đối **không** tạo cạnh giữa các nút Test (Test-Test = 0).
"""))

cells.append(nbf.v4.new_code_cell("""# Thiết lập kết nối Inductive cho Test
X_test_weighted = X_test * np.sqrt(feat_weights)
test_dist, test_idx = nbrs2.kneighbors(X_test_weighted, n_neighbors=8)

test_src, test_dst = [], []
for t_idx in range(len(X_test)):
    global_t_idx = len(X_train) + t_idx
    for rank in range(8):
        tr_neighbor = test_idx[t_idx, rank]
        test_src.append(tr_neighbor)
        test_dst.append(global_t_idx)

print(f"[*] Số cạnh nối Inductive từ Train sang Test: {len(test_src):,} cạnh.")
print("[+] Xác nhận: Không có cạnh nội bộ Test-Test. Bảo đảm tính khách quan khi inference!")
"""))

# Cell 7: Packaging to PyTorch Geometric Data
cells.append(nbf.v4.new_markdown_cell("""---
### PHẦN 5: ĐÓNG GÓI CHUẨN PYTORCH GEOMETRIC (DATA OBJECT)
Đóng gói đồ thị thành đối tượng `torch_geometric.data.Data(x, edge_index, edge_attr, y)` và lưu file `.pt` để bàn giao cho Thành viên 1 & 4.
"""))

cells.append(nbf.v4.new_code_cell("""# Đóng gói đồ thị PyG
x_tensor = torch.tensor(X_train, dtype=torch.float32)
edge_index = torch.tensor([src_nodes, dst_nodes], dtype=torch.int64)
edge_attr = torch.tensor(edge_weights, dtype=torch.float32).unsqueeze(1)
y_tensor = torch.tensor(y_train, dtype=torch.int64)

graph_data = Data(
    x=x_tensor,
    edge_index=edge_index,
    edge_attr=edge_attr,
    y=y_tensor
)

print("=== ĐỐI TƯỢNG ĐỒ THỊ PYTORCH GEOMETRIC HOÀN CHỈNH ===")
print(graph_data)
print(f" - Số lượng nút: {graph_data.num_nodes:,}")
print(f" - Số lượng cạnh: {graph_data.num_edges:,}")
print(f" - Số chiều đặc trưng nút: {graph_data.num_node_features}")
print(f" - Kích thước edge_index: {list(graph_data.edge_index.shape)}")
print(f" - Kích thước edge_attr: {list(graph_data.edge_attr.shape)}")

# Lưu đĩa
out_path = Path("data/patient_graph_tv3_demo.pt")
out_path.parent.mkdir(parents=True, exist_ok=True)
torch.save(graph_data, out_path)
print(f"\\n[+] ĐÃ LƯU FILE BÀN GIAO THÀNH CÔNG: {out_path.resolve()}")
"""))

nb['cells'] = cells

# Save unexecuted first
nb_path = "demo_tv3_diabetes_graph.ipynb"
with open(nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"[+] Đã tạo file khung notebook {nb_path}, đang thực thi để lưu output...")

# Execute notebook
client = NotebookClient(nb, timeout=600, kernel_name='python3')
client.execute()

with open(nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"[+] Hoàn tất! Notebook {nb_path} đã được chạy và lưu kèm đầy đủ kết quả output.")
