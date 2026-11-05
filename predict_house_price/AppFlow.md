# Application Flow Document (AppFlow)

## 1. Luồng Người Dùng Trên Sổ Tay Jupyter Notebook
```
[Mở Jupyter Notebook: A1_06_taint_731.ipynb]
       ↓
[Bước 1: Nạp dữ liệu gianha.csv & xem bảng đặc trưng x ∈ ℝ³⁸]
       ↓
[Bước 2: Xem 3 biểu đồ phân phối dữ liệu EDA trực quan]
       ↓
[Bước 3: Chạy fit() Baseline + 5 Mô hình ML]
       ↓
[Bước 4: Xem bảng 5 độ đo, 3 thí nghiệm có kiểm soát & phần suy ngẫm]
       ↓
[Bước 5: Thử nghiệm định giá bằng Web Widget trực tiếp trong cell]
```

## 2. Luồng Người Dùng Trên Web Application Dashboard
```
[Truy cập http://127.0.0.1:8000/]
       ↓
[Header: Hiển thị thông tin Bài tập A1 • Mã lớp 06 • taint • 731]
       ↓
[Khu vực Form Định Giá]:
  - Tùy chọn 1: Bấm nút "Chọn mẫu thực tế từ tập dữ liệu" để nạp nhanh thông số
  - Tùy chọn 2: Nhập tay thủ công (Tỉnh/TP, Quận/Huyện, Loại nhà, Diện tích, PN, WC, Tầng, Mặt tiền...)
       ↓
[Bấm nút "ĐỊNH GIÁ NGAY"]
       ↓
[Hiển thị Thẻ Kết Quả Nổi Bật]:
  - Giá ước lượng lớn: xx.xx TỶ VNĐ
  - Đơn giá: ~ xx.x Triệu VNĐ / m²
  - Khoảng giá hợp lý (±5%): Min Tỷ - Max Tỷ
  - Biểu đồ thanh ngang Feature Contribution (Đặc trưng ảnh hưởng mạnh nhất)
       ↓
[Khu vực Công Cụ Tài Chính Vay Mua Nhà]:
  - Tùy chỉnh tỷ lệ vay, thời hạn, lãi suất
  - Xem số tiền trả tháng đầu, tổng lãi phải trả
       ↓
[Khu vực Đánh Giá Học Thuật & Nút Tải Báo Cáo PDF]
```
