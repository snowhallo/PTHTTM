# BÀI TẬP LỚN A1: DỰ ĐOÁN GIÁ NHÀ VIỆT NAM 2024 VÀ TRIỂN KHAI ỨNG DỤNG WEB

**Học phần:** Phát triển Hệ thống Thông minh  
**Khoa:** Công nghệ Thông tin - Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế (`quetd@ptit.edu.vn`)  
**Sinh viên thực hiện:** `taint`  
**Mã lớp học phần:** `06`  
**Mã định danh 3 số cuối:** `731`  
**Tập dữ liệu:** Kaggle *House Price Prediction Dataset Vietnam - 2024* (`vietnam_housing_dataset.csv` - **30,229 bản ghi thực tế**)  

---

## 1. CẤU TRÚC THƯ MỤC DỰ ÁN

```
predict_house_price/
├── notebooks/
│   └── A1_06_taint_731.ipynb           # Sổ tay Jupyter 5 bước độc lập nộp bài
├── A1_06_taint_731_Report.md           # Báo cáo học thuật chi tiết chuẩn sinh viên PTIT
├── web/                                # Giao diện Web Application Dashboard (HTML/CSS/JS)
│   ├── index.html                      # Cấu trúc giao diện HTML5
│   ├── css/style.css                   # Định dạng giao diện CSS
│   └── js/app.js                       # Logic xử lý client-side (gọi API, tính toán, UI)
├── server/                             # Backend FastAPI Server (Mô hình phân tầng)
│   ├── main.py                         # API Router & Entry Point
│   ├── schemas.py                      # Pydantic Schemas (Validation dữ liệu & ChatRequest)
│   └── services/
│       └── neo4j_service.py            # Service Đồ thị tri thức Neo4j & Graph Chatbot (Cypher)
├── src/                                # Scripts kỹ thuật & Huấn luyện
│   ├── train.py                        # Pipeline nạp dữ liệu Kaggle & huấn luyện 5 mô hình
│   ├── create_notebook.py              # Script tự động sinh sổ tay notebook
│   └── test_notebook_execution.py      # Script kiểm thử tự động notebook (100% pass)
├── tests/
│   └── test_api.py                     # Bộ kiểm thử tự động các REST API Endpoints
├── data/
│   ├── vietnam_housing_dataset.csv     # Tập dữ liệu gốc từ Kaggle (30,229 bản ghi)
│   └── gianha.csv                      # Bản sao làm sạch dữ liệu
├── models/
│   ├── best_model.joblib               # Pipeline mô hình tối ưu Gradient Boosting
│   └── metrics.json                    # Bảng lưu trữ 5 độ đo thực nghiệm
├── requirements.txt                    # Danh sách các thư viện phụ thuộc
├── run_jupyter.bat                     # File thực thi nhanh 1-Click cho Jupyter Notebook
└── run_webapp.bat                      # File thực thi nhanh 1-Click cho Web Dashboard
```

---

## 2. YÊU CẦU HỆ THỐNG VÀ CÀI ĐẶT MÔI TRƯỜNG

### 2.1. Yêu cầu hệ thống:
- Hệ điều hành: Windows / macOS / Linux
- Python: Phiên bản **3.9+** trở lên (Khuyến nghị 3.10 - 3.12)

### 2.2. Cài đặt các thư viện phụ thuộc:
Mở Terminal / PowerShell / Command Prompt tại thư mục dự án và chạy:
```bash
cd D:\learning\phat_trien_he_thong_thong_minh\predict_house_price
pip install -r requirements.txt
```
*(Các thư viện chính gồm: `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `joblib`, `fastapi`, `uvicorn`, `notebook`, `ipywidgets`)*

---

## 3. HƯỚNG DẪN KHỞI CHẠY DỰ ÁN

### 3.1. Khởi chạy Sổ tay Thực nghiệm Jupyter Notebook (Nộp bài)

- **Cách 1: Chạy bằng dòng lệnh (Command Line):**
  ```bash
  python -m notebook notebooks/A1_06_taint_731.ipynb
  ```
  Trình duyệt sẽ tự động mở file notebook `A1_06_taint_731.ipynb`. Tại thanh công cụ menu, chọn **Cell** -> **Run All** để thực thi toàn bộ 7 cells.

- **Cách 2: Chạy nhanh bằng file batch:**
  Double-click vào tệp: `run_jupyter.bat`

---

### 3.2. Khởi chạy Giao diện Web Application Dashboard

- **Cách 1: Chạy bằng dòng lệnh (Command Line):**
  ```bash
  python -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload
  ```
  Sau khi terminal thông báo `Application startup complete`, mở trình duyệt web và truy cập:
  **http://127.0.0.1:8000/**

- **Cách 2: Chạy nhanh bằng file batch:**
  Double-click vào tệp: `run_webapp.bat`

---

### 3.3. Huấn luyện lại mô hình học máy (Re-train):
Nếu cần chạy lại pipeline huấn luyện trên dữ liệu Kaggle và cập nhật file `models/best_model.joblib`:
```bash
python src/train.py
```

---

### 3.4. Chạy kiểm thử tự động toàn bộ hệ thống:

- **Kiểm thử thực thi tự động toàn bộ 7 cells của Jupyter Notebook:**
  ```bash
  python src/test_notebook_execution.py
  ```
- **Kiểm thử tự động các REST API Endpoints:**
  ```bash
  python tests/test_api.py
  ```

---

## 4. KẾT QUẢ ĐỐI CHUẨN 5 MÔ HÌNH HỌC MÁY (TẬP TEST 6,034 MẪU)

| Mô hình Học máy | MAE (Tỷ VNĐ) | MSE | RMSE (Tỷ VNĐ) | R² Score (Max) | MAPE (%) (Min) | Ghi chú |
|---|---|---|---|---|---|---|
| **Baseline (Mean Dummy)** | 1.8093 | 4.7483 | 2.1791 | -0.0004 | 42.61% | Mô hình cơ sở đối chuẩn |
| **Linear Regression** | 1.4033 | 3.1185 | 1.7659 | 0.3430 | 30.40% | Hồi quy tuyến tính OLS |
| **Ridge Regression (L2)** | 1.4034 | 3.1185 | 1.7659 | 0.3430 | 30.40% | Chính quy hóa L2 ($\alpha=1.0$) |
| **Decision Tree Regressor** | 1.2336 | 2.6491 | 1.6276 | 0.4419 | 26.00% | Cây quyết định (`max_depth=12`) |
| **Random Forest Regressor** | 1.1153 | 2.1441 | 1.4643 | 0.5483 | 23.67% | Ensemble Bagging 100 cây |
| **Gradient Boosting (Triển khai)**| **1.1516** | **2.2131** | **1.4877** | **0.5338** | **24.71%** | **Mô hình sản xuất chính thức** |

---

## 5. TÀI LIỆU BÁO CÁO HỌC THUẬT

- Tệp báo cáo chi tiết đầy đủ 5 phần theo chuẩn sinh viên PTIT: [A1_06_taint_731_Report.md](A1_06_taint_731_Report.md)
- Bạn có thể chuyển đổi tệp Markdown này sang Word (`.docx`) hoặc xuất PDF để nộp bài theo yêu cầu.
