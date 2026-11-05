# UI/UX Design System Guidelines (Design)

## 1. Phong Cách Thiết Kế (Design Philosophy)
- **Phong cách:** Modern PropTech Dark Dashboard (Hiện đại, Đẳng cấp, Đậm chất Công nghệ Tài chính Bất động sản).
- **Trải nghiệm người dùng:** Giao diện một trang (Single Screen Dashboard), tối ưu trải nghiệm nhập liệu, có phản hồi tức thì dưới 15ms khi bấm định giá, hỗ trợ các thẻ nổi đổ bóng mềm mượt và micro-interactions rõ nét.

## 2. Bảng Màu Chuẩn (Color Palette)
- **Nền chính (Background):** `#0F172A` (Deep Slate 900)
- **Nền thẻ (Surface Card):** `#1E293B` (Slate 800) với viền nhẹ `#334155` (Slate 700)
- **Màu chủ đạo 1 (Primary / Brand):** `#2563EB` (Royal Blue) & Gradient `#1D4ED8`
- **Màu chủ đạo 2 (Accent / Success / Valuation):** `#059669` (Emerald Green) & `#10B981`
- **Màu cảnh báo / Nổi bật (Highlight / Outlier):** `#DC2626` (Crimson Red) & `#F59E0B` (Amber)
- **Màu chữ chính (Text Primary):** `#F8FAFC` (Slate 50)
- **Màu chữ phụ (Text Muted):** `#94A3B8` (Slate 400)

## 3. Typography
- Font chữ: `Plus Jakarta Sans`, `Inter`, `system-ui`, sans-serif.
- Tiêu đề chính ($H_1$): `font-bold text-2xl tracking-tight text-white`
- Thẻ số liệu định giá: `font-extrabold text-3xl md:text-4xl text-emerald-400`
- Nhãn trường nhập liệu: `font-medium text-xs uppercase tracking-wider text-slate-300`

## 4. Cấu Trúc Bố Cục Giao Diện (Layout Hierarchy)
1. **Header Topbar:** Logo PropTech 2024, thông tin học viên `06 • taint • 731`, trạng thái mô hình Gradient Boosting ($R^2 = 0.9686$).
2. **Left Column (Form Nhập Liệu & Test Data):**
   - Hộp chọn nhanh mẫu dữ liệu thực tế từ tập Train/Test.
   - Form nhập thủ công 10 đặc trưng bất động sản (Tỉnh, Quận, Loại nhà, Diện tích, Số tầng, Phòng ngủ, Mặt tiền, Đường vào...).
   - Nút bấm `ĐỊNH GIÁ NGAY (PREDICT VALUE)` nổi bật.
3. **Right Column (Kết Quả & Phân Tích Chuyên Sâu):**
   - Thẻ định giá lớn (Giá tỷ VNĐ + Đơn giá triệu/m² + Khoảng tin cậy $\pm 5\%$).
   - Thanh phân tích đóng góp đặc trưng (Feature Contributions).
   - Công cụ tính vay ngân hàng (Mortgage Calculator: Trả góp tháng đầu, tổng lãi).
   - Tab chuyển xem 3 Biểu đồ phân phối thị trường EDA và Bảng so sánh 5 mô hình ML.
