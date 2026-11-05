# Project Task Tracker (Tracker)

## Nhat Ky Tien Do va Nhiem Vu

- [x] Nạp trực tiếp tập dữ liệu chính thức [House Price Prediction Dataset Vietnam - 2024](https://www.kaggle.com/datasets/nguyentiennhan/vietnam-housing-dataset-2024) (`vietnam_housing_dataset.csv` - **30,229 bản ghi BĐS thực tế**).
- [x] Xây dựng và hoàn thiện Sổ tay Jupyter Notebook 5 bước (`notebooks/A1_06_taint_731.ipynb`):
  - [x] Bước 1: Nạp data Kaggle, xử lý missing values, định nghĩa bài toán hình thức & bảng biểu diễn đặc trưng $x \in \mathbb{R}^{38}$.
  - [x] Bước 2: 3 Biểu đồ phân phối EDA (Giá nhà, Diện tích sàn, Vị trí & Đặc tính).
  - [x] Bước 3: Huấn luyện Baseline (`DummyRegressor`) + 5 Mô hình ML bằng phương thức `fit()`.
  - [x] Bước 4: Đánh giá trên 5 độ đo (MAE, MSE, RMSE, R², MAPE), 3 Thí nghiệm có kiểm soát và trả lời trọn vẹn 15 câu hỏi Suy ngẫm học thuật (Reflection).
  - [x] Bước 5: Xuất bản `models/best_model.joblib`, 3 test cases demo và Web Widget tương tác trực tiếp trong cell.
- [x] Xây dựng Giao diện Web Application Dashboard (`web/index.html` & `server/main.py`):
  - [x] Backend FastAPI phản hồi < 15ms.
  - [x] Form nhập liệu thủ công đầy đủ 10 thuộc tính BĐS.
  - [x] Hộp chọn nhanh 10 căn nhà mẫu thực tế từ tập Kaggle để test mô hình và đối chiếu giá thực tế vs giá dự đoán.
  - [x] Công cụ tính toán vay mua nhà trả góp ngân hàng (Mortgage).
  - [x] Tab xem bảng 5 độ đo và phân tích đặc trưng.
- [x] Biên soạn Báo cáo Học thuật chi tiết chuẩn sinh viên PTIT: `A1_06_taint_731_Report.md`.
- [x] Kiểm thử tự động toàn diện:
  - [x] `src/test_notebook_execution.py` (Chạy 7 cells notebook đạt 100% không lỗi).
  - [x] `tests/test_api.py` (Chạy 5 API endpoints đạt 100% pass).
- [x] Dọn dẹp sạch sẽ toàn bộ các file tạm/thừa không cần thiết.
- [x] Cung cấp các file script 1-Click: `run_jupyter.bat` và `run_webapp.bat`.
