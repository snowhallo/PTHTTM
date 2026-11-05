# Implementation Plan Document (ImplementationPlan)

## Giai đoạn 1: Nạp Dữ Liệu Gốc Kaggle & Hoàn Thiện Sổ Tay Jupyter Notebook (`notebooks/A1_06_taint_731.ipynb`)
- [ ] Tự động nạp trực tiếp tập dữ liệu chính thức `data/vietnam_housing_dataset.csv` (30,229 dòng) từ Kaggle (`nguyentiennhan/vietnam-housing-dataset-2024`).
- [ ] Bước 1: Trích xuất các đặc trưng địa lý (`City`, `District` từ `Address`), xây dựng pipeline xử lý khuyết thiếu (`SimpleImputer`), định nghĩa bài toán hình thức và bảng biểu diễn dữ liệu.
- [ ] Bước 2: Xây dựng 3 Biểu đồ phân phối trọng tâm (Giá nhà, Diện tích sàn, Phân tầng giá theo Vị trí & Hướng nhà/Pháp lý).
- [ ] Bước 3: Huấn luyện Baseline đối chuẩn (`DummyRegressor(strategy='mean')`) và 5 mô hình ML (`Linear Regression`, `Ridge Regression`, `Decision Tree`, `Random Forest`, `Gradient Boosting`) bằng phương thức `fit()`.
- [ ] Bước 4: Đánh giá 5 độ đo (MAE, MSE, RMSE, R², MAPE), 3 thí nghiệm có kiểm soát (So sánh mô hình, Khảo sát siêu tham số $n\_estimators$, Khảo sát biểu diễn vị trí) và trả lời phần suy ngẫm học thuật (Reflection).
- [ ] Bước 5: Xuất bản `models/best_model.joblib`, kiểm thử 3 test cases thực tế và tích hợp Web Widget tương tác trực tiếp trong cell.

## Giai đoạn 2: Xây dựng Giao diện Web Application Dashboard (`web/` & `server/`)
- [ ] Xây dựng Backend FastAPI (`server/main.py`) nạp mô hình `models/best_model.joblib`.
- [ ] Cung cấp REST API `/api/predict`, `/api/sample-data` (trả về các mẫu BĐS thực tế trong 30,229 dòng Kaggle), `/api/calculate-mortgage`, `/api/metrics`.
- [ ] Xây dựng Giao diện Web Dashboard (`web/index.html`) theo phong cách Modern PropTech (Slate Dark `#0F172A`, Emerald `#059669`, Royal `#2563EB`):
  - Form nhập liệu thủ công đầy đủ các thuộc tính căn nhà.
  - Hộp chọn nhanh các mẫu dữ liệu thực tế từ tập Kaggle để test mô hình và so sánh giá thực tế vs giá dự đoán.
  - Thẻ hiển thị giá định giá, đơn giá/m², khoảng tin cậy $\pm 5\%$, thanh đóng góp đặc trưng.
  - Công cụ tính toán vay mua nhà trả góp ngân hàng (Mortgage).
  - Tab xem 3 biểu đồ phân phối EDA và bảng đối chuẩn 5 mô hình ML.

## Giai đoạn 3: Biên Soạn Báo Cáo Học Thuật Chi Tiết Định Dạng Markdown (`A1_06_taint_731_Report.md`)
- [ ] Biên soạn tệp báo cáo Markdown `A1_06_taint_731_Report.md` chuẩn mực cấu trúc sinh viên PTIT (để người dùng dễ dàng chuyển sang Word/DOCX và PDF):
  - *Trang bìa học thuật chuẩn:* Bộ TT&TT / PTIT - Khoa CNTT, Đề tài A1, Giảng viên hướng dẫn PGS. TS. Trần Đình Quế, Sinh viên `taint`, Mã lớp `06`, Định danh `731`.
  - *Phần 1:* Tuyên bố bài toán hình thức, Sơ đồ khối hệ thống thông minh, Bảng biểu diễn 12 đặc trưng từ 30,229 mẫu Kaggle sang vector $x \in \mathbb{R}^{38}$.
  - *Phần 2:* 3 Biểu đồ phân phối EDA (Giá, Diện tích, Vị trí & Đặc tính) kèm đoạn phân tích thống kê và ý nghĩa kinh tế dưới từng hình.
  - *Phần 3:* Cơ sở lý thuyết 5 thuật toán học máy, phương thức `fit()`, và bảng đối chuẩn tham số.
  - *Phần 4:* Bảng đánh giá 5 độ đo (MAE, MSE, RMSE, R², MAPE), 3 Thí nghiệm có kiểm soát (biểu đồ so sánh) và trả lời trọn vẹn 15 câu hỏi suy ngẫm học thuật (7 câu bản chất thông minh + 8 câu biểu diễn).
  - *Phần 5:* Phân hệ Web Application Dashboard, 3 ca kiểm thử thực tế, phân tích sai số, kết luận và cam kết liêm chính học thuật.

## Giai đoạn 4: Kiểm Thử Toàn Diện & Dọn Dẹp File Thừa
- [ ] Chạy kiểm thử tự động toàn bộ 7 cells của Jupyter Notebook qua `src/test_notebook_execution.py` đảm bảo 100% không lỗi.
- [ ] Chạy kiểm thử tự động API server qua `tests/test_api.py`.
- [ ] Dọn dẹp sạch sẽ các tệp tạm / file thừa không cần thiết trong thư mục dự án.
- [ ] Cung cấp các file script 1-Click `run_jupyter.bat` và `run_webapp.bat`.
