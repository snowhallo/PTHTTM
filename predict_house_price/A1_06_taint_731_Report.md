# BỘ THÔNG TIN VÀ TRUYỀN THÔNG
# HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG (PTIT)
## KHOA CÔNG NGHỆ THÔNG TIN

---

<br>

<div align="center">

# BÁO CÁO BÀI TẬP LỚN A1
### HỌC PHẦN: PHÁT TRIỂN HỆ THỐNG THÔNG MINH

## ĐỀ TÀI:
# XÂY DỰNG VÀ TRIỂN KHAI HỆ THỐNG DỰ ĐOÁN GIÁ NHÀ VIỆT NAM (2024) TRÊN NỀN TẢNG WEB

<br>

**Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế (`quetd@ptit.edu.vn`)  
**Sinh viên thực hiện:** `taint`  
**Mã lớp học phần:** `06`  
**Mã định danh 3 số cuối:** `731`  
**Sổ tay thực nghiệm:** `notebooks/A1_06_taint_731.ipynb`  
**Nguồn dữ liệu:** Kaggle *House Price Prediction Dataset Vietnam - 2024* (30,229 mẫu)  

<br>

*Hà Nội, 2024*

</div>

---

<div style="page-break-after: always;"></div>

# MỤC LỤC BÁO CÁO

- [PHẦN 1: TỔNG QUAN BÀI TOÁN, NẠP DỮ LIỆU VÀ BIỂU DIỄN ĐẶC TRƯNG](#phần-1-tổng-quan-bài-toán-nạp-dữ-liệu-và-biểu-diễn-đặc-trưng)
  - [1.1. Phát biểu bài toán hình thức](#11-phát-biểu-bài-toán-hình-thức)
  - [1.2. Nguồn dữ liệu thực tế Kaggle (30,229 mẫu)](#12-nguồn-dữ-liệu-thực-tế-kaggle-30229-mẫu)
  - [1.3. Sơ đồ luồng xử lý của hệ thống](#13-sơ-đồ-luồng-xử-lý-của-hệ-thống)
  - [1.4. Bảng biểu diễn dữ liệu đầu vào](#14-bảng-biểu-diễn-dữ-liệu-đầu-vào)
- [PHẦN 2: KHẢO SÁT VÀ TRỰC QUAN HÓA PHÂN PHỐI DỮ LIỆU](#phần-2-khảo-sát-và-trực-quan-hóa-phân-phối-dữ-liệu)
  - [2.1. Biểu đồ 1: Phân phối Giá nhà (Price Distribution)](#21-biểu-đồ-1-phân-phối-giá-nhà-price-distribution)
  - [2.2. Biểu đồ 2: Phân phối Diện tích sàn xây dựng (Area Distribution)](#22-biểu-đồ-2-phân-phối-diện-tích-sàn-xây-dựng-area-distribution)
  - [2.3. Biểu đồ 3: Phân tầng giá theo Vị trí Tỉnh/Thành phố](#23-biểu-đồ-3-phân-tầng-giá-theo-vị-trí-tỉnhthành-phố)
- [PHẦN 3: XÂY DỰNG 5 MÔ HÌNH HỌC MÁY VÀ PHƯƠNG THỨC FIT()](#phần-3-xây-dựng-5-mô-hình-học-máy-và-phương-thức-fit)
  - [3.1. Phân chia tập dữ liệu và tiền xử lý](#31-phân-chia-tập-dữ-liệu-và-tiền-xử-lý)
  - [3.2. Thiết lập mô hình đối chuẩn Baseline](#32-thiết-lập-mô-hình-đối-chuẩn-baseline)
  - [3.3. Huấn luyện 5 mô hình học máy truyền thống](#33-huấn-luyện-5-mô-hình-học-máy-truyền-thống)
- [PHẦN 4: THỬ NGHIỆM ĐÁNH GIÁ 5 ĐỘ ĐO VÀ SUY NGẪM HỌC THUẬT](#phần-4-thử-nghiệm-đánh-giá-5-độ-đo-và-suy-ngẫm-học-thuật)
  - [4.1. Định nghĩa toán học 5 độ đo hồi quy](#41-định-nghĩa-toán-học-5-độ-đo-hồi-quy)
  - [4.2. Bảng kết quả thực nghiệm 5 mô hình](#42-bảng-kết-quả-thực-nghiệm-5-mô-hình)
  - [4.3. Ba Thí nghiệm có kiểm soát (Controlled Experiments)](#43-ba-thí-nghiệm-có-kiểm-soát-controlled-experiments)
  - [4.4. Trả lời phần Suy ngẫm học thuật bắt buộc (Reflection)](#44-trả-lời-phần-suy-ngẫm-học-thuật-bắt-buộc-reflection)
- [PHẦN 5: TRIỂN KHAI GIAO DIỆN WEB VÀ KIỂM THỬ DỮ LIỆU THỰC TẾ](#phần-5-triển-khai-giao-diện-web-và-kiểm-thử-dữ-liệu-thực-tế)
  - [5.1. Lưu trữ Pipeline mô hình tối ưu](#51-lưu-trữ-pipeline-mô-hình-tối-ưu)
  - [5.2. Thực nghiệm 3 trường hợp đầu vào thực tế](#52-thực-nghiệm-3-trường-hợp-đầu-vào-thực-tế)
  - [5.3. Giao diện Web Application Dashboard](#53-giao-diện-web-application-dashboard)
  - [5.4. Hướng dẫn Cài đặt Môi trường và Khởi chạy bằng Dòng lệnh (Command Line)](#54-hướng-dẫn-cài-đặt-môi-trường-và-khởi-chạy-bằng-dòng-lệnh-command-line)
  - [5.5. Kết luận và Cam kết liêm chính học thuật](#55-kết-luận-và-cam-kết-liêm-chính-học-thuật)

---

<div style="page-break-after: always;"></div>

# PHẦN 1: TỔNG QUAN BÀI TOÁN, NẠP DỮ LIỆU VÀ BIỂU DIỄN ĐẶC TRƯNG

## 1.1. Phát biểu bài toán hình thức
Bài toán định giá bất động sản được mô hình hóa dưới dạng một bài toán Học có giám sát (Supervised Regression Learning):
- Không gian đầu vào: $\mathcal{X} \subset \mathbb{R}^{d}$ ($d = 38$ sau khi chuẩn hóa và mã hóa One-Hot), đại diện cho các thuộc tính vật lý, vị trí địa lý và pháp lý của bất động sản.
- Không gian đầu ra: $\mathcal{Y} = \mathbb{R}^+$ biểu diễn giá bán thị trường ước tính theo đơn vị Tỷ VNĐ.
- Mục tiêu học máy: Tìm hàm ánh xạ $f_\theta: \mathcal{X} \to \mathcal{Y}$ bằng cách tối thiểu hóa hàm mất mát trên tập dữ liệu huấn luyện:
$$\theta^* = \arg\min_\theta \frac{1}{N} \sum_{i=1}^N \mathcal{L}(y_i, f_\theta(x_i)) + \Omega(\theta)$$

## 1.2. Nguồn dữ liệu thực tế Kaggle (30,229 mẫu)
Dự án sử dụng tập dữ liệu từ Kaggle: House Price Prediction Dataset Vietnam - 2024 (`vietnam_housing_dataset.csv` do tác giả Nguyễn Tiến Nhân xuất bản).
- Quy mô: 30,229 bản ghi tin đăng bất động sản nhà ở tại Việt Nam.
- Phạm vi địa lý: Bao phủ các đô thị như TP. Hồ Chí Minh, Hà Nội, Hưng Yên, Đà Nẵng, Bình Dương...

## 1.3. Sơ đồ luồng xử lý của hệ thống
```
[Dữ liệu đầu vào: Diện tích, Vị trí (Quận, Tỉnh), Số phòng ngủ, Số tầng, Mặt tiền...]
       ↓
[Tiền xử lý: SimpleImputer + StandardScaler(Số học) + OneHotEncoder(Phân loại) -> x in R^38]
       ↓
[Mô hình học máy: Gradient Boosting Regressor (Huấn luyện fit() trên 80% Train)]
       ↓
[Kết quả dự đoán: y_pred (Tỷ VNĐ) + Khoảng tin cậy +-5% + Phân tích Feature Importance]
       ↓
[Triển khai: Giao diện Web Application (FastAPI) & Interactive Web Widget]
```

## 1.4. Bảng biểu diễn dữ liệu đầu vào
Nguyên tắc: *Biểu diễn quyết định lượng thông tin có thể học được (Representation determines what information is available to learning)*.

| STT | Tên Đặc Trưng | Kiểu Gốc | Xử Lý Khuyết Thiếu | Biểu Diễn Mô Hình (Model Input) | Ý Nghĩa Thực Tế |
|:---:|---|---|---|---|---|
| 1 | `area` | float | Giữ nguyên (100% full) | Standardized Float (StandardScaler) | Diện tích sàn sử dụng ($m^2$) |
| 2 | `frontage` | float | SimpleImputer(median) | Standardized Float | Độ rộng mặt tiền tiếp giáp đường (m) |
| 3 | `access_road`| float | SimpleImputer(median) | Standardized Float | Độ rộng đường/ngõ vào nhà (m) |
| 4 | `floors` | float | SimpleImputer(median) | Standardized Float | Tổng số tầng xây dựng |
| 5 | `bedroom` | float | SimpleImputer(median) | Standardized Float | Số lượng phòng ngủ |
| 6 | `bathroom` | float | SimpleImputer(median) | Standardized Float | Số lượng phòng vệ sinh |
| 7 | `city` | string | Trích xuất từ Address | One-Hot Encoded (6 chiều) | Tỉnh / Thành phố |
| 8 | `district` | string | Trích xuất từ Address | One-Hot Encoded (25 chiều) | Quận / Huyện |
| 9 | `legal_status`| string | Điền 'Chưa xác định' | One-Hot Encoded (3 chiều) | Tình trạng pháp lý |
| 10 | `house_direction`| string | Điền 'Chưa xác định' | One-Hot Encoded (9 chiều) | Hướng nhà |
| - | **`price_billion`**| **float** | **Target ($y \in \mathbb{R}^+$)** | **Biến Mục Tiêu** | **Giá bán thực tế (Tỷ VNĐ)** |

---

<div style="page-break-after: always;"></div>

# PHẦN 2: KHẢO SÁT VÀ TRỰC QUAN HÓA PHÂN PHỐI DỮ LIỆU

## 2.1. Biểu đồ 1: Phân phối Giá nhà (Price Distribution)
- Đặc điểm thống kê: Phân phối giá nhà có dạng lệch phải (Right-skewed) với giá trị trung vị $\text{Median} = 5.90$ Tỷ VNĐ và giá trị trung bình $\text{Mean} = 5.88$ Tỷ VNĐ.
- Ý nghĩa: Phân khúc giao dịch tập trung trong khoảng từ 3.5 Tỷ đến 8.0 Tỷ VNĐ, phản ánh thực tế phân khúc nhà ở tại các đô thị Việt Nam.

## 2.2. Biểu đồ 2: Phân phối Diện tích sàn xây dựng (Area Distribution)
- Đặc điểm thống kê: Diện tích sàn có tứ phân vị $Q_1 = 40.0 m^2$, $Q_2 = 56.0 m^2$, và $Q_3 = 80.0 m^2$.
- Ý nghĩa: Nhà ở đô thị phổ biến nhất trong khoảng $40 - 80 m^2$, các căn trên $150 m^2$ thuộc phân khúc diện tích lớn.

## 2.3. Biểu đồ 3: Phân tầng giá theo Vị trí Tỉnh/Thành phố
- Đặc điểm thống kê: Mặt bằng giá tại Hà Nội và TP. Hồ Chí Minh cao hơn so với các tỉnh thành lân cận. Bất động sản có sổ hồng (`Have certificate`) có định giá cao hơn khoảng 15-25% so với hợp đồng mua bán hoặc chưa có sổ.

---

<div style="page-break-after: always;"></div>

# PHẦN 3: XÂY DỰNG 5 MÔ HÌNH HỌC MÁY VÀ PHƯƠNG THỨC FIT()

## 3.1. Phân chia tập dữ liệu và tiền xử lý
- Tập Train (80%): 24,134 mẫu được sử dụng để khớp tham số (fit).
- Tập Test (20%): 6,034 mẫu được giữ nguyên hoàn toàn độc lập để đánh giá năng lực tổng quát hóa (Generalization).
- Pipeline: Tích hợp `SimpleImputer` xử lý khuyết thiếu, `StandardScaler` và `OneHotEncoder` đảm bảo không bị rò rỉ dữ liệu (Data Leakage).

## 3.2. Thiết lập mô hình đối chuẩn Baseline
- Sử dụng `DummyRegressor(strategy='mean')` luôn dự đoán giá trị trung bình $\bar{y}_{train}$.
- Kết quả Baseline trên tập kiểm thử: $R^2 = -0.0004$, sai số tuyệt đối $MAE = 1.8093$ Tỷ VNĐ, $MAPE = 42.61\%$. Baseline đóng vai trò là cột mốc đối chuẩn tối thiểu.

## 3.3. Huấn luyện 5 mô hình học máy truyền thống
1. **Linear Regression:** $\hat{y} = w^T x + b$, tìm nghiệm tối ưu bằng phương pháp bình phương tối thiểu OLS.
2. **Ridge Regression (Chính quy hóa L2):** $\min_w \|y - Xw\|_2^2 + \alpha \|w\|_2^2$ với $\alpha = 1.0$, giúp giảm hiện tượng đa cộng tuyến.
3. **Decision Tree Regressor:** Cây quyết định hồi quy phân tách không gian theo tiêu chí giảm phương sai (MSE Reduction), thiết lập độ sâu `max_depth=12`.
4. **Random Forest Regressor:** Ensemble Bagging gồm 100 cây quyết định độc lập, lấy mẫu bootstrap.
5. **Gradient Boosting Regressor:** Ensemble Boosting tuần tự 150 cây học phần dư với hàm mất mát MSE và `learning_rate=0.08`.

---

<div style="page-break-after: always;"></div>

# PHẦN 4: THỬ NGHIỆM ĐÁNH GIÁ 5 ĐỘ ĐO VÀ SUY NGẪM HỌC THUẬT

## 4.1. Định nghĩa toán học 5 độ đo hồi quy
1. **MAE (Mean Absolute Error):** $\text{MAE} = \frac{1}{N} \sum |y_i - \hat{y}_i|$ (Sai số tuyệt đối trung bình theo Tỷ VNĐ).
2. **MSE (Mean Squared Error):** $\text{MSE} = \frac{1}{N} \sum (y_i - \hat{y}_i)^2$ (Sai số bình phương trung bình).
3. **RMSE (Root Mean Squared Error):** $\text{RMSE} = \sqrt{\text{MSE}}$ (Cùng đơn vị Tỷ VNĐ với giá nhà).
4. **$R^2$ Score (Hệ số xác định):** $R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ (Tỷ lệ phương sai được giải thích bởi mô hình).
5. **MAPE (%) (Mean Absolute Percentage Error):** $\text{MAPE} = \frac{100\%}{N} \sum \left|\frac{y_i - \hat{y}_i}{y_i}\right|$ (Sai số phần trăm tuyệt đối trung bình).

## 4.2. Bảng kết quả thực nghiệm 5 mô hình trên 6,034 mẫu kiểm thử

| Mô Hình | MAE (Tỷ) | MSE | RMSE (Tỷ) | $R^2$ Score | MAPE (%) | Thời Gian Fit (ms) |
|---|---|---|---|---|---|---|
| **Baseline (Mean Dummy)** | 1.8093 | 4.7483 | 2.1791 | -0.0004 | 42.61% | 2.1 ms |
| 1. Linear Regression | 1.4033 | 3.1185 | 1.7659 | 0.3430 | 30.40% | 68.2 ms |
| 2. Ridge Regression (L2) | 1.4034 | 3.1185 | 1.7659 | 0.3430 | 30.40% | 45.4 ms |
| 3. Decision Tree Regressor | 1.2336 | 2.6491 | 1.6276 | 0.4419 | 26.00% | 116.5 ms |
| 4. Random Forest Regressor | 1.1153 | 2.1441 | 1.4643 | 0.5483 | 23.67% | 772.9 ms |
| **5. Gradient Boosting (Triển khai)** | **1.1516** | **2.2131** | **1.4877** | **0.5338** | **24.71%** | **6321.7 ms** |

## 4.3. Ba Thí nghiệm có kiểm soát (Controlled Experiments)
- **Thí nghiệm 1 (So sánh Mô hình):** Random Forest và Gradient Boosting đạt kết quả tốt hơn so với mô hình tuyến tính (tăng $R^2$ từ 0.34 lên 0.54, giảm MAPE từ 30.4% xuống 23.6%).
- **Thí nghiệm 2 (Khảo sát Siêu tham số $n\_estimators$):** Khi tăng số cây từ 20 $\to$ 50 $\to$ 100 $\to$ 150 $\to$ 250, $R^2$ tăng từ 0.3905 lên 0.5448 và ổn định quanh ngưỡng 150 cây.
- **Thí nghiệm 3 (Khảo sát Biểu diễn Đặc trưng):**
  - Mô hình đầy đủ ($X_{all}$): $R^2 = 0.5338$, $MAPE = 24.71\%$.
  - Mô hình không có vị trí địa lý ($X_{no\_location}$): $R^2 = 0.3323$, $MAPE = 31.94\%$.
  - *Nhận xét:* Thiếu thông tin vị trí làm giảm khoảng $20\%$ độ chính xác của mô hình, cho thấy vai trò quan trọng của không gian biểu diễn đặc trưng.

## 4.4. Trả lời phần Suy ngẫm học thuật bắt buộc (Reflection)

### A. 7 Câu hỏi về Bản chất Thông minh của Hệ thống (Section 18 Slide):
1. **Hệ thống nhận thông tin gì?** Các thuộc tính diện tích, mặt tiền, đường vào, số tầng, số phòng ngủ, phòng tắm, vị trí (quận, tỉnh), pháp lý và hướng nhà.
2. **Biểu diễn nội tại là gì?** Vector số học $x \in \mathbb{R}^{38}$ kết hợp chuẩn hóa chuẩn `StandardScaler` và mã hóa `OneHotEncoder`.
3. **Mô hình học được gì từ các ví dụ?** Học được hàm phi tuyến ánh xạ giữa quy mô xây dựng, vị trí địa lý trung tâm và giá trị thị trường thực tế.
4. **Mô hình đưa ra dự đoán gì?** Giá trị ước lượng BĐS (Tỷ VNĐ), khoảng giá hợp lý $\pm 5\%$ và đóng góp của từng nhóm đặc trưng.
5. **Tại sao mô hình xử lý được trường hợp chưa từng thấy (Unseen input)?** Nhờ năng lực tổng quát hóa (Generalization) từ 30,229 mẫu dữ liệu phân bổ đa dạng.
6. **Phần nào của hệ thống được gọi là 'thông minh'?** Khả năng tự động đúc kết hàm định giá từ dữ liệu thực nghiệm thay vì con người phải lập trình luật cứng.
7. **Hạn chế nào ngăn hệ thống trở nên thông minh hơn?** Mô hình phụ thuộc vào vector đặc trưng thiết kế sẵn và chưa tiếp nhận trực quan hình ảnh nội thất hay biến động kinh tế vĩ mô.

### B. 8 Câu hỏi về Biểu diễn Thông tin (Section 19 Slide):
- Biểu diễn dạng bảng là phù hợp nhất cho dữ liệu có cấu trúc.
- Thông tin bị mất đi gồm cảm quan thẩm mỹ, kiến trúc thực tế và mức độ khấu hao của công trình.
- Hướng phát triển biểu diễn trong tương lai: Biểu diễn dạng ảnh (CNN), dạng đồ thị (GNN mô hình hóa tiện ích xung quanh) và vector nhúng đa phương thức.

### C. Vị trí trong Tiến trình Lịch sử Trí tuệ Nhân tạo (Section 20 Slide):
```
Symbolic AI (Hệ chuyên gia dựa trên luật cố định)
       ↓
Statistical Machine Learning (Đặc trưng thiết kế + Mô hình học máy) <--- BÀI TẬP A1 Ở ĐÂY
       ↓
Deep Learning (Tensors + Biểu diễn tự học từ dữ liệu thô)
       ↓
Foundation / Generative Models (Mô hình nền tảng đa phương thức)
       ↓
Interactive / Agentic Systems (Tri giác + Lập luận + Hành động)
```

---

<div style="page-break-after: always;"></div>

# PHẦN 5: TRIỂN KHAI GIAO DIỆN WEB VÀ KIỂM THỬ DỮ LIỆU THỰC TẾ

## 5.1. Lưu trữ Pipeline mô hình tối ưu
Pipeline mô hình `GradientBoostingRegressor` được tuần tự hóa và lưu trữ tại tệp `models/best_model.joblib`. FastAPI backend tải trực tiếp mô hình vào bộ nhớ để phục vụ suy diễn với thời gian phản hồi < 15ms.

## 5.2. Thực nghiệm 3 trường hợp đầu vào thực tế
- **Trường hợp 1 (Hà Nội):** Nhà tại Cầu Giấy, Hà Nội (85.0m², 3PN, 4 tầng, MT 4.5m) $\to$ **Dự đoán: 8.32 Tỷ VNĐ** (~ 97.9 Triệu VNĐ/m²). Khoảng giá hợp lý: $7.91 - 8.74$ Tỷ VNĐ.
- **Trường hợp 2 (TP. Hồ Chí Minh):** Nhà tại Quận 1, TP.HCM (120.0m², 4PN, 5 tầng, MT 6.0m) $\to$ **Dự đoán: 8.79 Tỷ VNĐ** (~ 73.2 Triệu VNĐ/m²). Khoảng giá hợp lý: $8.35 - 9.23$ Tỷ VNĐ.
- **Trường hợp 3 (Hưng Yên):** Liền kề Văn Giang, Hưng Yên (90.0m², 4PN, 4 tầng, MT 6.0m) $\to$ **Dự đoán: 7.80 Tỷ VNĐ** (~ 86.7 Triệu VNĐ/m²). Khoảng giá hợp lý: $7.41 - 8.19$ Tỷ VNĐ.

## 5.3. Giao diện Web Application Dashboard
Giao diện Web Dashboard được xây dựng theo phong cách giao diện sáng hiện đại (Light Theme), định vị là Nền tảng Định giá Bất động sản Việt Nam (Vietnam Real Estate AI) với các chức năng chính:
1. **Kiểm thử dữ liệu mẫu Kaggle:** Hỗ trợ menu chọn 10 mẫu nhà thực tế từ tập dữ liệu 30,229 bản ghi để đối chiếu giá thực tế và giá dự đoán.
2. **Form nhập liệu thủ công:** 10 trường thông số trực quan kèm thanh trượt phản hồi thời gian thực.
3. **Thẻ kết quả định giá:** Giá trị ước tính nổi bật, khoảng tin cậy $\pm 5\%$ và thanh hiển thị mức độ đóng góp của từng nhóm biến (Feature Importance).
4. **Trợ lý Đồ thị Tri thức Neo4j (Graph RAG):** Tích hợp Chatbot truy vấn đồ thị tri thức 30,229 bản ghi bằng ngôn ngữ tự nhiên, tự động chuyển đổi sang câu lệnh Cypher Query, trích xuất dữ liệu phân tích thị trường và thẻ bất động sản phù hợp.
5. **Bảng đối chuẩn 5 mô hình:** Hiển thị 5 độ đo khoa học của các mô hình học máy trên tập kiểm thử độc lập.

## 5.4. Hướng dẫn Cài đặt Môi trường và Khởi chạy bằng Dòng lệnh (Command Line)

### Bước 1: Mở cửa sổ Terminal (PowerShell / Command Prompt / Terminal trong VS Code)
Điều hướng vào thư mục gốc của dự án:
```bash
cd D:\learning\phat_trien_he_thong_thong_minh\predict_house_price
```

### Bước 2: Cài đặt các thư viện phụ thuộc cần thiết (Dependencies)
```bash
pip install -r requirements.txt
```
*(Các thư viện chính bao gồm: `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `joblib`, `fastapi`, `uvicorn`, `notebook`, `ipywidgets`)*

### Bước 3: Tùy chọn 1 - Khởi chạy Sổ tay Thực nghiệm Jupyter Notebook
```bash
python -m notebook notebooks/A1_06_taint_731.ipynb
```
*Trình duyệt sẽ tự động mở notebook. Tại giao diện, chọn **Cell** -> **Run All** để thực thi toàn bộ 7 bước.*

### Bước 4: Tùy chọn 2 - Khởi chạy Giao diện Web Application Dashboard
```bash
python -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload
```
*Sau khi server báo trạng thái `Application startup complete`, mở trình duyệt web và truy cập địa chỉ:*
**http://127.0.0.1:8000/**

### Bước 5: Chạy các bài kiểm thử tự động (Automated Verification)
- Kiểm thử thực thi Notebook 100%:
  ```bash
  python src/test_notebook_execution.py
  ```
- Kiểm thử toàn bộ REST API Endpoints:
  ```bash
  python tests/test_api.py
  ```

## 5.5. Kết luận và Cam kết liêm chính học thuật
- **Kết luận:** Bài tập lớn A1 đã hoàn thành đầy đủ 5 bước theo yêu cầu đề bài trên tập dữ liệu 30,229 mẫu của Kaggle.
- **Cam kết liêm chính học thuật:** Toàn bộ dữ liệu, mã nguồn và kết quả thực nghiệm trong báo cáo này được thực hiện trung thực, minh bạch và có thể tái lập hoàn toàn (Reproducibility).

<br>

<div align="right">

**Sinh viên thực hiện**  
*(Ký và ghi rõ họ tên)*  
<br><br>
**taint (Mã định danh: 731)**

</div>
