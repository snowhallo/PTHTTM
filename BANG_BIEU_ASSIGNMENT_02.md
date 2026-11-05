# TỔNG HỢP TOÀN BỘ BẢNG BIỂU BÁO CÁO ASSIGNMENT 02
**Họ và tên:** Nguyễn Tuấn Tài — **MSSV:** B23DCCN731 — **Nhóm:** 06  
**Môn học:** Phát triển các hệ thống thông minh (PGS. TS. Trần Đình Quế)

> [!TIP]
> **Hướng dẫn copy vào Microsoft Word:**
> - Bạn chỉ cần bôi đen toàn bộ bảng bên dưới (từ hàng tiêu đề đến hàng cuối cùng), nhấn `Ctrl + C`.
> - Sang file Word `A02_06_taint.731.docx`, đặt con trỏ tại vị trí cần dán và nhấn `Ctrl + V`. Microsoft Word sẽ tự động nhận diện định dạng bảng hoàn hảo 100%!

---

## BẢNG 1: So sánh hiệu năng 5 mô hình trên bài toán Dự đoán Tiểu đường (Diabetes)
*(Vị trí: Trang 13 - Mục 14. Experiment 1 – Model Comparison)*

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 0.9603 | 0.8757 | 0.6216 | 0.7271 | 0.9642 |
| **Decision Tree** | 0.9695 | 0.9203 | 0.7020 | 0.7964 | 0.9688 |
| **Random Forest (Tối ưu)** | **0.9718** | **0.9942** | **0.6725** | **0.8023** | **0.9617** |
| **SVM** | 0.9617 | 0.9575 | 0.5745 | 0.7181 | 0.9076 |
| **KNN** | 0.9538 | 0.9498 | 0.4824 | 0.6398 | 0.9058 |

---

## BẢNG 2: Đánh giá các sai số dự đoán trên bài toán Giá nhà (House Price Regression)
*(Vị trí: Trang 20 - Mục 21. Experiment 1 – Model Comparison)*

| Model | MAE | MSE | RMSE | R² |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Regression** | 19.824,50 | 1.245.890.120 | 35.297,16 | 0.8124 |
| **Ridge Regression** | 19.812,40 | 1.243.560.890 | 35.264,15 | 0.8130 |
| **Decision Tree** | 24.150,00 | 1.890.120.450 | 43.475,51 | 0.7389 |
| **Random Forest** | **17.773,12** | 762.887.450 | 27.619,71 | 0.9006 |
| **Gradient Boosting (Tối ưu)** | 18.028,04 | **749.562.300** | **27.378,13** | **0.9023** |

---

## BẢNG 3: Đối chuẩn hiệu năng 6 mô hình trên bài toán Khám phá Hành vi Khách hàng E-commerce
*(Vị trí: Trang 26 - Mục 29. Experiment 1 – Model Comparison)*

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 0.9340 | 0.9736 | 0.9454 | 0.9593 | 0.9719 |
| **Decision Tree** | 0.9347 | 0.9832 | 0.9366 | 0.9593 | 0.9629 |
| **Random Forest** | 0.9276 | 0.9588 | 0.9529 | 0.9559 | 0.9557 |
| **SVM (Tabular)** | 0.9364 | 0.9872 | 0.9348 | 0.9602 | 0.9676 |
| **KNN** | 0.9278 | 0.9613 | 0.9506 | 0.9559 | 0.9579 |
| **Text Linear SVM (Tối ưu)** | **0.9419** | 0.9670 | **0.9622** | **0.9646** | **0.9773** |

---

## BẢNG 4: So sánh tổng hợp kiến trúc & hiệu năng 3 Hệ thống thông minh
*(Vị trí: Trang 36 - Mục 38. Bảng so sánh 3 hệ thống)*

| Tiêu chí đối chuẩn | Hệ thống 1: Dự đoán Tiểu đường | Hệ thống 2: Dự đoán Giá nhà | Hệ thống 3: E-commerce Customer Behavior |
| :--- | :--- | :--- | :--- |
| **Loại bài toán** | Phân loại nhị phân (Binary Classification) | Hồi quy giá trị liên tục (Regression) | Phân loại & Khám phá đánh giá (NLP Classification) |
| **Tập dữ liệu (Dataset)** | `diabetes_100k.csv` (100.000 dòng, 15 thuộc tính y tế) | `house_price_vietnam_2024.csv` (Bất động sản thực tế) | `womens_clothing_reviews.csv` (23.486 lượt review khách hàng) |
| **Biểu diễn dữ liệu** | Imputation, StandardScaler, One-Hot Encoding | ColumnTransformer (RobustScaler + OneHotEncoder) | Text Preprocessing, N-grams, TF-IDF Vectorizer (3.000 chiều) |
| **Thuật toán tối ưu** | **Random Forest** (n_estimators=150, max_depth=8) | **Gradient Boosting Regressor** (n_estimators=200, lr=0.05) | **Text Linear SVM** (LinearSVC với TF-IDF features) |
| **Chỉ số kiểm thử tốt nhất**| **Accuracy: 97.18%** \| **F1: 0.8023** \| Precision: 99.42% | **RMSE: 27.378,13** \| **R²: 0.9023** \| MAE: 18.028,04 | **Accuracy: 94.19%** \| **F1: 0.9646** \| ROC-AUC: 0.9773 |
| **Đồ thị tri thức (KG)** | Neo4j `kg_diabet` (Quan hệ Bệnh - Thuốc - Triệu chứng) | Neo4j Bất động sản (Quan hệ Nhà - Khu vực - Tiện ích) | Knowledge Graph phân nhóm sở thích & Hành vi mua hàng |
| **Giao diện Triển khai** | Web Desktop (HTML/CSS/JS) + Mobile Responsive 3 Tabs | Web Thẩm định giá BĐS + Trợ lý hỏi đáp Neo4j + Mobile | Web Phân tích Review khách hàng + Mobile Responsive |
