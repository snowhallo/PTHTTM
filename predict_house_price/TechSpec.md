# Technical Specification Document (TechSpec)

## 1. Kiến Trúc Tổng Thể (System Architecture)
Hệ thống gồm 2 thành phần chính:
1. **Machine Learning Core & Jupyter Notebook (`notebooks/A1_06_taint_731.ipynb`):**
   - Môi trường: Python 3.10+ / Anaconda Jupyter.
   - Thư viện cốt lõi: `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `joblib`, `IPython`.
   - Pipeline tiền xử lý: `ColumnTransformer` (`StandardScaler` cho biến số liên tục, `OneHotEncoder` cho biến phân loại danh nghĩa).
   - Mô hình tối ưu: `GradientBoostingRegressor(n_estimators=150, learning_rate=0.08, max_depth=5, random_state=731)`.
   - Lưu trữ mô hình: `models/best_model.joblib`.

2. **Web Application Service (`server/` & `web/`):**
   - **Backend:** `FastAPI` (Python ASGI Server via `uvicorn`), định tuyến RESTful API phục vụ định giá, tính vay và nạp mẫu dữ liệu kiểm thử.
   - **Frontend:** Single Page Application (SPA) xây dựng bằng HTML5 chuẩn ngữ nghĩa, Vanilla CSS hiện đại và Modern JavaScript (ES6+).
   - **Giao thức:** REST API qua `fetch()` dạng JSON.

## 2. Danh Sách API Endpoints
- `GET /`: Phục vụ giao diện Web Dashboard chính (`web/index.html`).
- `POST /api/predict`: Nhận JSON thuộc tính căn nhà $\to$ Trả về giá trị định giá (Tỷ VNĐ), đơn giá triệu/m², khoảng tin cậy $\pm 5\%$, và bóc tách mức độ đóng góp của từng đặc trưng.
- `GET /api/sample-data`: Trả về danh sách các mẫu dữ liệu thực tế trong tập dữ liệu để điền nhanh vào form kiểm thử.
- `POST /api/calculate-mortgage`: Nhận giá nhà, tỷ lệ vay %, thời hạn (năm), lãi suất % $\to$ Trả về bảng phân rã gốc + lãi hàng tháng.
- `GET /api/metrics`: Trả về bảng 5 độ đo của Baseline + 5 mô hình ML.
- `GET /api/download-report`: Tải về tệp báo cáo học thuật PDF `A1_06_taint.731.PDF`.

## 3. Quản Lý Môi Trường & Thực Thi
- File thực thi 1-Click: `run_jupyter.bat` (khởi chạy Jupyter Notebook) và `run_webapp.bat` (khởi chạy FastAPI server tại `http://127.0.0.1:8000/`).
