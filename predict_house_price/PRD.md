# Product Requirements Document (PRD)

## 1. Thông Tin Dự Án & Định Danh Học Thuật
- **Học viện:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)
- **Môn học:** Phát triển Hệ thống Thông minh (Intelligent System Development)
- **Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế (`quetd@ptit.edu.vn`)
- **Mã lớp:** `06` | **Họ và tên:** `taint` | **Mã định danh:** `731`
- **Tên tệp báo cáo nộp bài:** `A1_06_taint.731.PDF`
- **Sổ tay thực nghiệm học máy:** `notebooks/A1_06_taint_731.ipynb`

## 2. Mục Tiêu Dự Án (Project Goals)
1. Sử dụng trực tiếp tập dữ liệu chính thức tải từ Kaggle: **[House Price Prediction Dataset Vietnam - 2024](https://www.kaggle.com/datasets/nguyentiennhan/vietnam-housing-dataset-2024)** (`vietnam_housing_dataset.csv` - 30,229 dòng dữ liệu BĐS thực tế).
2. Xây dựng Sổ tay Jupyter Notebook hoàn chỉnh, tự chứa, thực hiện tuần tự và chuẩn xác **5 Bước yêu cầu của Bài tập A1**:
   - **Bước 1:** Nạp dữ liệu *House Price Prediction Dataset Vietnam - 2024* (`data/vietnam_housing_dataset.csv` / `gianha.csv`), trích xuất thông tin địa lý (Tỉnh/Thành phố, Quận/Huyện từ trường Address), xử lý missing values, định nghĩa bài toán hình thức và bảng biểu diễn dữ liệu.
   - **Bước 2:** Xây dựng 3 Biểu đồ phân phối trọng tâm (Giá nhà, Diện tích sàn, Phân tầng giá theo Vị trí & Đặc tính nhà ở).
   - **Bước 3:** Huấn luyện Baseline (`DummyRegressor`) và 5 mô hình học máy truyền thống sử dụng phương thức `fit()`.
   - **Bước 4:** Thử nghiệm đánh giá 5 mô hình trên 5 độ đo (MAE, MSE, RMSE, R², MAPE), thực hiện 3 Thí nghiệm có kiểm soát và trả lời phần suy ngẫm học thuật (Reflection).
   - **Bước 5:** Triển khai mô hình tối ưu thành Giao diện Web Application (FastAPI backend + HTML5/CSS/JS frontend).
3. Xây dựng Giao diện Web trực quan (PropTech Web Dashboard) cho phép người dùng:
   - Nhập thông số thủ công của bất động sản (Diện tích, Tỉnh/TP, Quận/Huyện, Số phòng ngủ, Số phòng tắm, Số tầng, Mặt tiền, Đường vào...) để nhận kết quả định giá tức thì.
   - Kiểm tra, so sánh dự đoán trên các mẫu dữ liệu thực tế từ 30,229 mẫu của tập Kaggle.
   - Tính toán kế hoạch tài chính vay mua nhà ngân hàng (Mortgage) và xem phân tích độ nhạy của các đặc trưng.

## 3. Đối Tượng Sử Dụng (Target Users)
- Giảng viên chấm điểm & Đánh giá học thuật: Cần tính chuẩn xác, minh bạch, có đối chuẩn baseline và 3 thí nghiệm có kiểm soát.
- Người mua/Bán nhà & Chuyên viên BĐS: Cần công cụ ước tính giá nhà nhanh, minh bạch cơ sở định giá và hỗ trợ tính toán tài chính.

## 4. Đặc Tả Tệp Báo Cáo Học Thuật (`A1_06_taint_731_Report.md`)
Tệp báo cáo học thuật được biên soạn theo định dạng Markdown chuẩn (`A1_06_taint_731_Report.md`), giúp sinh viên dễ dàng chuyển đổi sang định dạng Word (.docx) và PDF phục vụ nộp bài:
- **Trang bìa học thuật chuẩn quy cách PTIT:** Quốc hiệu, Bộ TT&TT, Học viện Công nghệ Bưu chính Viễn thông, Khoa CNTT, Tên học phần, Tên đề tài, Giảng viên hướng dẫn (PGS. TS. Trần Đình Quế), Thông tin sinh viên (`06 • taint • 731`).
- **Nội dung cấu trúc chuẩn 5 Phần lớn:**
  1. *Phần 1: Định nghĩa Hệ thống, Nạp Dữ liệu Kaggle (30,229 mẫu) & Biểu diễn Đặc trưng $x \in \mathbb{R}^{38}$.*
  2. *Phần 2: Khảo sát & Trực quan hóa Phân phối Dữ liệu (3 Biểu đồ EDA chất lượng cao kèm phân tích kinh tế).*
  3. *Phần 3: Huấn luyện Baseline & 5 Mô hình Học máy truyền thống bằng phương thức `fit()`.*
  4. *Phần 4: Đánh giá Thực nghiệm trên 5 Độ đo, 3 Thí nghiệm có kiểm soát & Trả lời trọn vẹn phần Suy ngẫm học thuật (Reflection 7+8 câu hỏi).*
  5. *Phần 5: Triển khai Giao diện Web Application Dashboard, Kiểm thử 3 ca thực tế, Hình ảnh trực quan giao diện và Cam kết học thuật.*
- **Hình thức trình bày:** Bảng biểu kẻ vạch rõ ràng, công thức toán học LaTeX, phân tích lý giải số liệu chi tiết dưới từng hình.

## 5. Dọn Dẹp Sau Khi Hoàn Thành (Post-Implementation Cleanup)
- Dọn dẹp sạch sẽ toàn bộ các file tạm, script phụ hoặc artifact không cần thiết để giữ cây thư mục dự án gọn gàng, tinh gọn.
