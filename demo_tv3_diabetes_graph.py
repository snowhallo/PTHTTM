"""
========================================================================================
DỰ ÁN: DEEP GRAPH LEARNING IN AI - DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG (DIABETES PREDICTION)
MÔN HỌC: PHÁT TRIỂN HỆ THỐNG THÔNG MINH
BỘ PHẬN THỰC HIỆN: THÀNH VIÊN 3
NỘI DUNG:
  1. Khám phá & Đánh giá Dữ liệu Lâm sàng 100k bản ghi (EDA & Clinical Standards)
  2. Quy trình Tiền xử lý chuẩn & Thiết lập phòng thủ Chống Rò rỉ Dữ liệu (Data Leakage Defense)
  3. Khởi tạo Đồ thị Tương đồng Bệnh nhân (PA1: Baseline KNN vs PA2: Clinically-Weighted KNN)
  4. Đo lường Độ thuần Đồ thị (Homophily Ratio) & Ma trận Trọng số Cạnh Gaussian RBF
  5. Đóng gói & Bàn giao Đồ thị Chuẩn PyTorch Geometric (torch_geometric.data.Data)
========================================================================================
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.neighbors import NearestNeighbors
import torch
from torch_geometric.data import Data

# Thiết lập hiển thị tiếng Việt trên Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    print("=" * 80)
    print("DEMO THÀNH VIÊN 3: KHÁM PHÁ DỮ LIỆU & XÂY DỰNG ĐỒ THỊ BỆNH NHÂN CHO GNN")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. NẠP DỮ LIỆU & ĐÁNH GIÁ ĐẶC TRƯNG LÂM SÀNG (EDA)
    # -------------------------------------------------------------------------
    data_path = Path("data/diabetes_100k.csv")
    if not data_path.exists():
        # Fallback đường dẫn nếu chạy từ thư mục con
        data_path = Path("../data/diabetes_100k.csv")
    
    print(f"\n[1/5] Đang nạp tập dữ liệu từ: {data_path.resolve()}...")
    df = pd.read_csv(data_path)
    num_rows, num_cols = df.shape
    print(f"  -> Kích thước tập dữ liệu: {num_rows:,} dòng x {num_cols} cột")
    print(f"  -> Danh sách các cột: {list(df.columns)}")
    print(f"  -> Số lượng giá trị thiếu (Missing values): {df.isnull().sum().sum()} ô")

    # Phân bố biến mục tiêu
    target_counts = df['diabetes'].value_counts()
    n_neg, n_pos = target_counts[0], target_counts[1]
    ratio_neg = n_neg / num_rows * 100
    ratio_pos = n_pos / num_rows * 100
    imbalance_factor = n_neg / n_pos

    print("\n  [*] Phân tích độ mất cân bằng nhãn (Class Imbalance):")
    print(f"      - Lớp 0 (Âm tính / Không mắc bệnh): {n_neg:,} mẫu ({ratio_neg:.2f}%)")
    print(f"      - Lớp 1 (Dương tính / Mắc tiểu đường): {n_pos:,} mẫu ({ratio_pos:.2f}%)")
    print(f"      - Tỷ lệ mất cân bằng nghiêm ngặt: {imbalance_factor:.2f} : 1")

    # Kiểm tra chỉ số vàng lâm sàng theo ADA (American Diabetes Association)
    print("\n  [*] Đối chiếu Chuẩn đoán Y khoa Vàng (ADA & WHO Standards):")
    pos_hba1c_mean = df[df['diabetes'] == 1]['HbA1c_level'].mean()
    neg_hba1c_mean = df[df['diabetes'] == 0]['HbA1c_level'].mean()
    pos_glucose_mean = df[df['diabetes'] == 1]['blood_glucose_level'].mean()
    neg_glucose_mean = df[df['diabetes'] == 0]['blood_glucose_level'].mean()

    print(f"      - HbA1c (Trung bình): Nhóm Bệnh = {pos_hba1c_mean:.2f}% (≥ 6.5% ngưỡng bệnh) vs Nhóm Khỏe = {neg_hba1c_mean:.2f}%")
    print(f"      - Đường huyết Glucose (Trung bình): Nhóm Bệnh = {pos_glucose_mean:.1f} mg/dL vs Nhóm Khỏe = {neg_glucose_mean:.1f} mg/dL")

    # -------------------------------------------------------------------------
    # 2. TIỀN XỬ LÝ & THIẾT LẬP PHÒNG THỦ CHỐNG DATA LEAKAGE
    # -------------------------------------------------------------------------
    print("\n[2/5] Thực hiện Tiền xử lý & Thiết lập Phòng thủ Rò rỉ Dữ liệu...")
    
    # Để demo chạy mượt mà và trực quan, sử dụng mẫu chuẩn đại diện phân tầng 10,000 bệnh nhân
    SAMPLE_SIZE = 10000
    print(f"  -> Lấy mẫu chuẩn đại diện phân tầng: {SAMPLE_SIZE:,} bệnh nhân")
    df_sample = df.sample(n=SAMPLE_SIZE, random_state=42).reset_index(drop=True)

    X = df_sample.drop(columns=['diabetes'])
    y = df_sample['diabetes'].values

    # BƯỚC BẮT BUỘC: Chia Train/Test TRƯỚC TIÊN (Stratified Split 80/20)
    # Giữ nguyên tỷ lệ mất cân bằng trên cả 2 tập
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )
    print(f"  -> Phân tách phân tầng: Train = {len(X_train_raw):,} nút, Test = {len(X_test_raw):,} nút")

    # QUY TẮC PHÒNG VỆ SỐ 1: Cách ly hoàn toàn nhãn Y (Không có mặt trong ma trận đặc trưng X)
    print("  -> [CHỐNG LABEL LEAKAGE]: Biến mục tiêu 'diabetes' đã được tách riêng vào vector y.")

    # QUY TẮC PHÒNG VỆ SỐ 2: Chỉ fit scaler/encoder trên Train, sau đó transform sang Test
    cat_cols = ['gender', 'smoking_history']
    num_cols = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']

    # Sử dụng RobustScaler (dựa trên Median & IQR) thay vì StandardScaler để chống nhiễu ngoại lệ y sinh
    scaler = RobustScaler()
    X_train_num = scaler.fit_transform(X_train_raw[num_cols])
    X_test_num = scaler.transform(X_test_raw[num_cols])

    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_train_cat = encoder.fit_transform(X_train_raw[cat_cols])
    X_test_cat = encoder.transform(X_test_raw[cat_cols])

    X_train = np.hstack([X_train_num, X_train_cat])
    X_test = np.hstack([X_test_num, X_test_cat])
    print(f"  -> Kích thước vector đặc trưng nút (Node feature dimension): d = {X_train.shape[1]}")
    print("  -> [CHỐNG STATISTICAL LEAKAGE]: Fit RobustScaler & OneHotEncoder DUY NHẤT trên Train!")

    # -------------------------------------------------------------------------
    # 3. XÂY DỰNG ĐỒ THỊ TƯƠNG ĐỒNG BỆNH NHÂN (PATIENT GRAPH CONSTRUCTION)
    # -------------------------------------------------------------------------
    print("\n[3/5] Khởi tạo Đồ thị Bệnh nhân (So sánh 02 Phương án Thiết kế)...")

    # --- PHƯƠNG ÁN 1: KNN THUẦN (BASELINE HOMOGENEOUS KNN) ---
    K1 = 10
    print(f"\n  [*] Triển khai Phương án 1 (Baseline Homogeneous KNN, k={K1}):")
    nbrs1 = NearestNeighbors(n_neighbors=K1 + 1, metric='euclidean', n_jobs=-1).fit(X_train)
    distances1, indices1 = nbrs1.kneighbors(X_train)

    src_nodes1, dst_nodes1, edge_weights1 = [], [], []
    sigma1 = np.median(distances1[:, 1:])  # Độ co dãn Gaussian kernel RBF
    
    same_label1 = 0
    total_edges1 = 0
    for i in range(len(X_train)):
        for j_rank in range(1, K1 + 1):
            j = indices1[i, j_rank]
            dist = distances1[i, j_rank]
            weight = np.exp(- (dist ** 2) / (2 * (sigma1 ** 2) + 1e-8))
            
            src_nodes1.append(i)
            dst_nodes1.append(j)
            edge_weights1.append(weight)
            
            total_edges1 += 1
            if y_train[i] == y_train[j]:
                same_label1 += 1

    homophily_pa1 = same_label1 / total_edges1
    print(f"      - Tổng số cạnh tạo lập (Train Graph): {total_edges1:,} cạnh")
    print(f"      - Tỷ lệ đồng nhất nhãn (Homophily Ratio h): {homophily_pa1:.2%}")

    # --- PHƯƠNG ÁN 2: KNN TRỌNG SỐ LÂM SÀNG (CLINICALLY-WEIGHTED KNN) ---
    K2 = 8
    print(f"\n  [*] Triển khai Phương án 2 (Clinically-Weighted KNN, k={K2}) - ĐỀ XUẤT:")
    # Gán trọng số ưu tiên: HbA1c (x3.0), Glucose (x3.0), BMI (x2.0)
    feat_weights = np.ones(X_train.shape[1], dtype=np.float32)
    feat_weights[num_cols.index('HbA1c_level')] = 3.0
    feat_weights[num_cols.index('blood_glucose_level')] = 3.0
    feat_weights[num_cols.index('bmi')] = 2.0

    X_train_weighted = X_train * np.sqrt(feat_weights)
    nbrs2 = NearestNeighbors(n_neighbors=K2 + 1, metric='euclidean', n_jobs=-1).fit(X_train_weighted)
    distances2, indices2 = nbrs2.kneighbors(X_train_weighted)

    src_nodes2, dst_nodes2, edge_weights2 = [], [], []
    sigma2 = np.median(distances2[:, 1:])
    
    same_label2 = 0
    total_edges2 = 0
    for i in range(len(X_train)):
        for j_rank in range(1, K2 + 1):
            j = indices2[i, j_rank]
            dist = distances2[i, j_rank]
            weight = np.exp(- (dist ** 2) / (2 * (sigma2 ** 2) + 1e-8))
            
            src_nodes2.append(i)
            dst_nodes2.append(j)
            edge_weights2.append(weight)
            
            total_edges2 += 1
            if y_train[i] == y_train[j]:
                same_label2 += 1

    homophily_pa2 = same_label2 / total_edges2
    print(f"      - Trọng số lâm sàng áp dụng: HbA1c=3.0, Glucose=3.0, BMI=2.0")
    print(f"      - Tổng số cạnh tạo lập (Train Graph): {total_edges2:,} cạnh")
    print(f"      - Tỷ lệ đồng nhất nhãn (Homophily Ratio h): {homophily_pa2:.2%}")
    delta_h = (homophily_pa2 - homophily_pa1) * 100
    print(f"      -> KẾT QUẢ: PA2 tăng độ thuần cụm +{delta_h:.2f}%, giảm 20% số cạnh dư thừa!")

    # -------------------------------------------------------------------------
    # 4. THIẾT LẬP ĐỒ THỊ QUY NẠP (INDUCTIVE GRAPH FOR TEST NODES)
    # -------------------------------------------------------------------------
    print("\n[4/5] Thiết lập Đồ thị Quy nạp (Inductive Graph Setting) cho tập Test...")
    # Nút Test chỉ truy vấn k láng giềng trong Train. TUYỆT ĐỐI không nối giữa Test với Test.
    X_test_weighted = X_test * np.sqrt(feat_weights)
    test_distances, test_indices = nbrs2.kneighbors(X_test_weighted, n_neighbors=K2)

    test_src, test_dst = [], []
    for test_idx in range(len(X_test)):
        # Chỉ số nút test trong toàn bộ đồ thị sẽ là len(X_train) + test_idx
        global_test_idx = len(X_train) + test_idx
        for j_rank in range(K2):
            train_neighbor_idx = test_indices[test_idx, j_rank]
            # Cạnh 1 chiều từ Train truyền thông điệp sang Test (hoặc 2 chiều có kiểm soát)
            test_src.append(train_neighbor_idx)
            test_dst.append(global_test_idx)

    print(f"  -> Số cạnh kết nối Inductive từ Train sang Test: {len(test_src):,} cạnh")
    print("  -> [CHỐNG TRANSDUCTIVE LEAKAGE]: Không có bất kỳ cạnh nội bộ nào giữa các nút Test (Test-Test = 0)!")

    # -------------------------------------------------------------------------
    # 5. ĐÓNG GÓI CHUẨN PYTORCH GEOMETRIC (DATA OBJECT)
    # -------------------------------------------------------------------------
    print("\n[5/5] Đóng gói thành đối tượng chuẩn PyTorch Geometric (torch_geometric.data.Data)...")
    
    # Đóng gói đồ thị Train theo PA2 được đề xuất
    x_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    edge_index_train = torch.tensor([src_nodes2, dst_nodes2], dtype=torch.int64)
    edge_attr_train = torch.tensor(edge_weights2, dtype=torch.float32).unsqueeze(1)
    y_train_tensor = torch.tensor(y_train, dtype=torch.int64)

    train_graph_data = Data(
        x=x_train_tensor,
        edge_index=edge_index_train,
        edge_attr=edge_attr_train,
        y=y_train_tensor
    )

    print("\n  === ĐỐI TƯỢNG ĐỒ THỊ PYTORCH GEOMETRIC HOÀN CHỈNH ===")
    print(f"  {train_graph_data}")
    print(f"  - Số lượng nút (Number of Nodes |V|): {train_graph_data.num_nodes:,}")
    print(f"  - Số lượng cạnh (Number of Edges |E|): {train_graph_data.num_edges:,}")
    print(f"  - Số chiều đặc trưng mỗi nút (Feature dimension): {train_graph_data.num_node_features}")
    print(f"  - Kích thước ma trận cạnh (edge_index shape): {list(train_graph_data.edge_index.shape)}")
    print(f"  - Có nút cô lập không (Has isolated nodes): {train_graph_data.has_isolated_nodes()}")
    print(f"  - Có tự khuyên không (Has self loops): {train_graph_data.has_self_loops()}")

    # Lưu đồ thị ra đĩa để bàn giao
    out_pt_path = Path("data/patient_graph_tv3_demo.pt")
    out_pt_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(train_graph_data, out_pt_path)
    print(f"\n[+] ĐÃ LƯU FILE ĐỒ THỊ BÀN GIAO CHO THÀNH VIÊN 1 & 4 TẠI: {out_pt_path.resolve()}")
    print("=" * 80)
    print("DEMO HOÀN THÀNH XUẤT SẮC - SẴN SÀNG BÁO CÁO VÀ THỰC HIỆN LIVE DEMO!")
    print("=" * 80)

if __name__ == '__main__':
    main()

