# Data Schema & Pipeline Representation (Schema)

## 1. Cấu Trúc Tập Dữ Liệu Gốc Tải Từ Kaggle (`data/vietnam_housing_dataset.csv`)
Tập dữ liệu chính thức từ Kaggle (`nguyentiennhan/vietnam-housing-dataset-2024`) gồm 30,229 dòng và 12 cột:

| Tên Cột Gốc | Kiểu Dữ Liệu | Không Rỗng (Non-Null) | Mô Tả & Ý Nghĩa |
|---|---|---|---|
| `Address` | string / object | 30,229 (100%) | Địa chỉ chi tiết (chứa tên đường, phường, quận/huyện, tỉnh/thành phố) |
| `Area` | float | 30,229 (100%) | Diện tích đất / sàn xây dựng ($m^2$) |
| `Frontage` | float | 18,665 (61.7%) | Chiều rộng mặt tiền tiếp giáp đường (mét) |
| `Access Road` | float | 16,932 (56.0%) | Chiều rộng đường / ngõ dẫn vào nhà (mét) |
| `House direction` | string | 8,990 (29.7%) | Hướng nhà (Đông, Tây, Nam, Bắc, Đông Nam...) |
| `Balcony direction` | string | 5,246 (17.4%) | Hướng ban công |
| `Floors` | float | 26,626 (88.1%) | Số tầng xây dựng |
| `Bedrooms` | float | 25,067 (82.9%) | Số lượng phòng ngủ |
| `Bathrooms` | float | 23,155 (76.6%) | Số lượng phòng tắm / WC |
| `Legal status` | string | 25,723 (85.1%) | Tình trạng pháp lý (Have certificate, Sale contract...) |
| `Furniture state` | string | 16,110 (53.3%) | Tình trạng nội thất (Full, Basic, Empty...) |
| **`Price`** | float | 30,229 (100%) | **Biến Mục Tiêu: Giá nhà thực tế (Tỷ VNĐ)** |

## 2. Tiền Xử Lý Dữ Liệu & Kỹ Thuật Đặc Trưng (Feature Engineering)
1. **Trích xuất Vị trí:**
   - `City`: Tách từ thành phần cuối cùng của `Address` (ví dụ: *Hồ Chí Minh*, *Hà Nội*, *Đà Nẵng*, *Hưng Yên*...).
   - `District`: Tách từ thành phần kế cuối của `Address` (ví dụ: *Gò Vấp*, *Cầu Giấy*, *Quận 7*, *Sơn Trà*...).
2. **Xử lý Khuyết thiếu (Missing Values Imputation):**
   - Biến số học (`Area`, `Frontage`, `Access Road`, `Floors`, `Bedrooms`, `Bathrooms`): Sử dụng `SimpleImputer(strategy='median')`.
   - Biến phân loại (`City`, `District`, `Legal status`, `House direction`): Sử dụng `SimpleImputer(strategy='constant', fill_value='Chưa xác định')`.
3. **Chuẩn hóa & Mã hóa:**
   - Chuẩn hóa số học qua `StandardScaler()`.
   - Mã hóa One-Hot qua `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` $\to$ Vector đặc trưng đầu vào $x \in \mathbb{R}^{d}$.
