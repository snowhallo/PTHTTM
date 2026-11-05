# TÀI LIỆU BÁO CÁO VÀ HƯỚNG DẪN TRẢ LỜI VẤN ĐÁP
## MÔN HỌC: PHÁT TRIỂN HỆ THỐNG THÔNG MINH (INTELLIGENT SYSTEM DEVELOPMENT)
### CHỦ ĐỀ: THỰC HÀNH CHAPTER 12 - TRIỂN KHAI MÔ HÌNH HỌC MÁY (DEPLOYING ML MODELS)
**Tài liệu giáo trình:** *Python Machine Learning - Wei-Meng Lee (Chapter 12, Book 1)*  
**Bộ dữ liệu:** Pima Indians Diabetes Database (`diabet.csv` / `diabetes.csv` từ Kaggle/UCI)

---

## MỤC LỤC
1. [TỔNG QUAN KIẾN TRÚC HỆ THỐNG](#1-tổng-quan-kiến-trúc-hệ-thống)
2. [DANH SÁCH TOÀN BỘ CÁC VIỆC ĐÃ THỰC HIỆN](#2-danh-sách-toàn-bộ-các-việc-đã-thực-hiện)
3. [HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC THỰC HIỆN](#3-hướng-dẫn-chi-tiết-từng-bước-thực-hiện)
4. [BẢNG KẾT QUẢ THỰC NGHIỆM ĐỐI CHIẾU](#4-bảng-kết-quả-thực-nghiệm-đối-chiếu)
5. [BỘ CÂU HỎI & KỊCH BẢN TRẢ LỜI KHI THẦY GIÁO HỎI VẤN ĐÁP](#5-bộ-câu-hỏi--kịch-bản-trả-lời-khi-thầy-giáo-hỏi-vấn-đáp)
6. [HƯỚNG DẪN THAO TÁC DEMO TRỰC TIẾP TRÊN MÁY TÍNH](#6-hướng-dẫn-thao-tác-demo-trực-tiếp-trên-máy-tính)

---

## 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

Theo sơ đồ giảng dạy trên bảng:
$$\text{Database (diabet.csv)} \longrightarrow \text{Data Cleaning} \longrightarrow \text{Feature Selection (3, 5, 7)} \longrightarrow \text{Model Evaluation (10-Fold CV)} \longrightarrow \text{Save Model (.sav)} \longrightarrow \text{REST API (Flask)} \longleftrightarrow \text{Client}$$

- **Input (Dữ liệu đầu vào):** Bảng dữ liệu y tế 768 bệnh nhân nữ Pima Indians gồm 8 chỉ số khám bệnh (`Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, `BMI`, `DiabetesPedigreeFunction`, `Age`).
- **Target (Mục tiêu dự đoán):** `Outcome` (0 = Không mắc bệnh tiểu đường, 1 = Mắc bệnh tiểu đường).
- **Core AI/ML:** Thuật toán phân lớp tối ưu **K-Nearest Neighbors ($k=19$)** trên **Top 3 đặc trưng (`Glucose`, `BMI`, `Age`)**.
- **Deployment (Triển khai):** Đóng gói thành Web Service chuẩn **REST API** với **Flask**, giao tiếp qua giao thức HTTP POST dạng **JSON**.

---

## 2. DANH SÁCH TOÀN BỘ CÁC VIỆC ĐÃ THỰC HIỆN

1. **Bước 1: Nạp & Tiền xử lý dữ liệu (Data Preprocessing & Cleaning)**
   - Nạp file `diabet.csv` vào DataFrame của Pandas.
   - Phát hiện các giá trị bằng `0` phi lý trong y tế (ví dụ: huyết áp 0, đường huyết 0, BMI 0).
   - Thay thế các giá trị 0 này thành `NaN`, sau đó điền bù khuyết thiếu bằng giá trị trung bình (`mean`) của từng cột tương ứng.

2. **Bước 2: Phân tích tương quan & Lựa chọn đặc trưng (Feature Selection)**
   - Tính toán ma trận hệ số tương quan tuyến tính Pearson (`df.corr()`).
   - Trực quan hóa ma trận bằng biểu đồ nhiệt **Heatmap (Seaborn/Matplotlib)**.
   - Sắp xếp và trích chọn các đặc trưng có ảnh hưởng mạnh nhất tới `Outcome`: Top 3 gồm `Glucose` (0.493), `BMI` (0.312), `Age` (0.238).

3. **Bước 3: Đánh giá & So sánh các thuật toán học máy (Model Evaluation)**
   - Sử dụng phương pháp **10-Fold Cross-Validation** để đánh giá độ chính xác khách quan, tránh Overfitting.
   - Thử nghiệm 4 thuật toán:
     1. *Logistic Regression*
     2. *K-Nearest Neighbors (KNN)* (Quét tìm $k$ tối ưu trong khoảng từ 1 đến 50)
     3. *Support Vector Machine (SVM) - Tuyến tính (Linear Kernel)*
     4. *Support Vector Machine (SVM) - Phi tuyến (RBF Kernel)*

4. **Bước 4: Thực nghiệm mở rộng theo yêu cầu trên bảng lớp học**
   - Khảo sát và so sánh hiệu năng của 4 mô hình trên các tập đặc trưng khác nhau:
     - **Top 3 Features** (`Glucose`, `BMI`, `Age`)
     - **Top 5 Features** (`Glucose`, `BMI`, `Age`, `Pregnancies`, `SkinThickness`)
     - **Top 7 Features** (+ `Insulin`, `DiabetesPedigreeFunction`)
     - **All 8 Features** (Tất cả đặc trưng)

5. **Bước 5: Huấn luyện mô hình tối ưu & Lưu trữ (Model Persistence)**
   - Chọn mô hình xuất sắc nhất: **KNN với $k=19$ trên Top 3 đặc trưng** (Độ chính xác $\approx 77.21\%$).
   - Huấn luyện trên toàn bộ tập dữ liệu và lưu vào file nhị phân `diabetes.sav` bằng thư viện `pickle`.
   - Kiểm tra đọc lại mô hình và thử nghiệm hàm `predict()` và `predict_proba()` (tính độ tin cậy %).

6. **Bước 6: Xây dựng dịch vụ Web REST API với Flask (`REST_API.py`)**
   - Tạo endpoint `POST /diabetes/v1/predict`.
   - Tiếp nhận dữ liệu JSON đầu vào (`{"Glucose": ..., "BMI": ..., "Age": ...}`).
   - Trả về kết quả JSON gồm phân lớp `0/1`, nhãn chẩn đoán `Diabetic / Not Diabetic` và `confidence` (%).

7. **Bước 7: Xây dựng ứng dụng Client kiểm thử tương tác (`Predict_Diabetes.py`)**
   - Cho phép người dùng nhập các chỉ số lâm sàng từ bàn phím.
   - Tự động đóng gói JSON và gửi HTTP POST request đến REST API, sau đó in kết quả ra màn hình.

---

## 3. HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC THỰC HIỆN

### Bước 1: Xử lý dữ liệu khuyết thiếu (Missing Data)
Trong tập dữ liệu, nhiều bệnh nhân có chỉ số `Glucose = 0`, `BloodPressure = 0`, `BMI = 0`. Điều này bất khả thi về mặt sinh học (người còn sống không thể có huyết áp hoặc đường huyết bằng 0). Do đó:
```python
cols_to_clean = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
# 1. Gán NaN cho số 0
df[cols_to_clean] = df[cols_to_clean].replace(0, np.nan)
# 2. Điền trung bình
df.fillna(df.mean(), inplace=True)
```

### Bước 2: Ma trận tương quan & Lựa chọn đặc trưng
Hệ số tương quan thể hiện mức độ liên kết giữa từng đặc trưng với khả năng mắc bệnh:
- `Glucose`: **0.4929** (Độ tương quan cao nhất - lượng đường huyết là yếu tố quyết định hàng đầu).
- `BMI`: **0.3119** (Chỉ số thể trọng - người béo phì có nguy cơ mắc tiểu đường cao).
- `Age`: **0.2384** (Tuổi tác - người lớn tuổi có nguy cơ cao hơn).
$\rightarrow$ Lựa chọn 3 đặc trưng này làm đầu vào chính giúp mô hình gọn nhẹ, giảm chi phí xét nghiệm và tránh hiện tượng quá khớp (*Overfitting*).

### Bước 3: Tìm kiếm siêu tham số cho KNN (Hyperparameter Tuning)
Ta quét các giá trị $k$ lẻ từ 1 đến 50:
```python
ks = list(range(1, 51, 2))
cv_scores = []
for k in ks:
    knn = KNeighborsClassifier(n_neighbors=k)
    score = cross_val_score(knn, X_3, y, cv=10, scoring='accuracy').mean()
    cv_scores.append(score)
optimal_k = ks[cv_scores.index(max(cv_scores))]  # Kết quả: k = 19
```

---

## 4. BẢNG KẾT QUẢ THỰC NGHIỆM ĐỐI CHIẾU

*Kết quả 10-Fold Cross-Validation chi tiết:*

| Tập đặc trưng khảo sát | Danh sách đặc trưng | Logistic Regression | KNN (Tối ưu) | SVM Linear | SVM RBF |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Top 3 Features** *(Chuẩn Chapter 12)* | `Glucose`, `BMI`, `Age` | **76.70%** | **77.21% ($k=19$)** ⭐ | **76.57%** | **76.57%** |
| **Top 5 Features** | `Glucose`, `BMI`, `Age`, `Pregnancies`, `SkinThickness` | **76.83%** | **76.31% ($k=15$)** | **76.57%** | **76.70%** |
| **Top 7 Features** | + `Insulin`, `DiabetesPedigreeFunction` | **76.83%** | **75.40% ($k=15$)** | **76.70%** | **76.70%** |
| **All 8 Features** | Toàn bộ 8 cột đặc trưng | **77.22%** | **74.88% ($k=17$)** | **76.96%** | **76.70%** |

### 📌 Nhận xét khoa học rút ra từ thực nghiệm:
1. **Đối với KNN:** Độ chính xác đạt đỉnh ở **Top 3 đặc trưng (77.21%)** và có xu hướng **giảm dần** khi tăng lên 5, 7 và 8 đặc trưng. Nguyên nhân do thuật toán KNN dựa trên khoảng cách hình học (*Euclidean distance*). Khi tăng số chiều dữ liệu, không gian trở nên thưa thớt (*Curse of Dimensionality - Lời nguyền chiều dữ liệu*) và các đặc trưng ít quan trọng tạo ra nhiễu khoảng cách.
2. **Đối với Logistic Regression / SVM:** Khi đưa thêm nhiều đặc trưng, độ chính xác tăng nhẹ nhờ tính chất gán trọng số tuyến tính, nhưng mức cải thiện không đáng kể so với chi phí phải thu thập thêm 5 xét nghiệm y tế khác.
3. **Kết luận lựa chọn:** Mô hình **KNN ($k=19$) với Top 3 đặc trưng** là sự cân bằng hoàn hảo nhất giữa **độ chính xác cao nhất (77.21%)** và **tính thực tiễn khi triển khai ứng dụng** (người dùng chỉ cần nhập 3 chỉ số quen thuộc).

---

## 5. BỘ CÂU HỎI & KỊCH BẢN TRẢ LỜI KHI THẦY GIÁO HỎI VẤN ĐÁP

### ❓ Câu hỏi 1: Tại sao trong tập dữ liệu có các giá trị bằng 0 lại phải thay bằng NaN rồi mới tính Mean?
> **🗣️ Trả lời:**  
> "Thưa thầy, trong y tế, các chỉ số như nồng độ Glucose, huyết áp BloodPressure, độ dày nếp gấp da SkinThickness hay chỉ số khối cơ thể BMI không thể bằng 0 ở người sống. Giá trị 0 ở đây thực chất là do người thu thập dữ liệu điền vào khi bị thiếu (*Missing Data*). Nếu để nguyên số 0 để tính toán, nó sẽ làm sai lệch nghiêm trọng phân phối và giá trị trung bình của toàn bộ cột. Do đó, quy trình chuẩn là gán các giá trị 0 phi lý này thành `np.nan` (Not a Number) rồi dùng phương pháp nội suy trung bình cột (`df.fillna(df.mean())`) để bù đắp dữ liệu khuyết thiếu."

---

### ❓ Câu hỏi 2: Tại sao em lại chọn 3 đặc trưng (Glucose, BMI, Age) thay vì dùng toàn bộ 8 đặc trưng?
> **🗣️ Trả lời:**  
> "Thưa thầy, việc chọn 3 đặc trưng dựa trên hai cơ sở:
> 1. **Phân tích tương quan (Correlation Analysis):** Qua ma trận tương quan với biến mục tiêu `Outcome`, 3 chỉ số `Glucose` (0.49), `BMI` (0.31), `Age` (0.24) có hệ số tương quan Pearson cao vượt trội so với các chỉ số còn lại.
> 2. **Thực nghiệm kiểm chứng:** Khi chạy thực nghiệm so sánh với KNN, mô hình 3 đặc trưng đạt độ chính xác **77.21%**, cao hơn cả mô hình 8 đặc trưng (74.88%). Việc giảm số chiều dữ liệu giúp loại bỏ nhiễu, tránh hiện tượng Overfitting và giúp hệ thống REST API dễ sử dụng hơn cho người dùng thực tế."

---

### ❓ Câu hỏi 3: Phương pháp 10-Fold Cross-Validation hoạt động như thế nào và tại sao lại dùng nó?
> **🗣️ Trả lời:**  
> "Thưa thầy, 10-Fold Cross-Validation chia tập dữ liệu thành 10 phần bằng nhau. Quá trình lặp lại 10 lần: mỗi lần chọn 1 phần làm tập kiểm thử (Test Set) và 9 phần còn lại làm tập huấn luyện (Train Set). Điểm đánh giá cuối cùng là trung bình cộng của 10 lần đo.  
> Em sử dụng phương pháp này thay vì `train_test_split` thông thường vì tập dữ liệu chỉ có 768 mẫu (khá nhỏ). Cross-Validation giúp đảm bảo mọi mẫu dữ liệu đều được kiểm thử 1 lần, loại bỏ hoàn toàn yếu tố may rủi khi chia tập dữ liệu và phản ánh chính xác khả năng tổng quát hóa của mô hình."

---

### ❓ Câu hỏi 4: Tại sao trong bài này em chọn thuật toán KNN thay vì SVM hay Logistic Regression?
> **🗣️ Trả lời:**  
> "Thưa thầy, sau khi đánh giá đồng thời 4 mô hình bằng 10-Fold Cross-Validation trên cùng một tập dữ liệu 3 đặc trưng:
> - KNN ($k=19$): **77.21%** (Cao nhất)
> - Logistic Regression: **76.70%**
> - SVM Linear Kernel: **76.57%**
> - SVM RBF Kernel: **76.57%**  
> Thuật toán KNN với $k=19$ cho kết quả tối ưu nhất. Giá trị $k=19$ là số lẻ (tránh hòa phiếu phân lớp nhị phân) và đủ lớn để làm mượt ranh giới quyết định, hạn chế ảnh hưởng của các điểm dữ liệu nhiễu (outliers)."

---

### ❓ Câu hỏi 5: File `diabetes.sav` là gì? Tại sao phải lưu mô hình ra file này?
> **🗣️ Trả lời:**  
> "Thưa thầy, `diabetes.sav` là tệp nhị phân lưu trữ đối tượng mô hình Machine Learning đã được huấn luyện đầy đủ các tham số bằng thư viện `pickle` (*Model Persistence*).  
> Việc lưu ra file giúp tách biệt quá trình huấn luyện và quá trình triển khai:
> - Quá trình huấn luyện chỉ cần thực hiện 1 lần.
> - Khi máy chủ Web REST API khởi động, nó chỉ cần nạp trực tiếp file `.sav` vào bộ nhớ RAM trong vài mili-giây để dự đoán ngay lập tức cho người dùng mà không cần phải huấn luyện lại từ đầu."

---

### ❓ Câu hỏi 6: Kiến trúc REST API trong bài hoạt động như thế nào?
> **🗣️ Trả lời:**  
> "Thưa thầy, em sử dụng micro-framework **Flask** để xây dựng REST API:
> - **Endpoint:** `POST /diabetes/v1/predict`
> - **Input payload (JSON):** Nhận một chuỗi JSON chứa 3 giá trị `{"Glucose": 100, "BMI": 30, "Age": 29}`.
> - **Xử lý:** Server trích xuất 3 chỉ số, đưa vào hàm `model.predict()` để lấy nhãn phân lớp (0 hoặc 1) và `model.predict_proba()` để lấy xác suất tin cậy lớn nhất.
> - **Output response (JSON):** Trả về mã HTTP 200 kèm JSON: `{"prediction": 0, "label": "Not Diabetic", "confidence": "78.95"}`."

---

## 6. HƯỚNG DẪN THAO TÁC 100% TRÊN ANACONDA (KHÔNG DÙNG VS CODE)

Theo yêu cầu chuẩn của thầy trên bảng (**"① load anaconda"** & **"Code với NOTEBOOK theo từng cell"**):

### BƯỚC 1: KHỞI ĐỘNG MÔI TRƯỜNG ANACONDA & MỞ JUPYTER NOTEBOOK
1. Bấm phím **Windows**, gõ tìm và mở **Anaconda Navigator** (hoặc mở **Anaconda Prompt**).
2. **Cách 1 (Dùng giao diện Anaconda Navigator):**
   - Tại giao diện chính của Navigator, tìm thẻ **Jupyter Notebook** và bấm nút **Launch**.
   - Trình duyệt Web sẽ tự động mở lên giao diện quản lý file của Jupyter.
3. **Cách 2 (Mở nhanh trực tiếp vào thư mục bài học bằng Anaconda Prompt - Khuyên dùng):**
   - Mở **Anaconda Prompt**, gõ lệnh chuyển đến thư mục bài tập và bật notebook:
     ```bash
     cd /d "d:\learning\phat_trien_he_thong_thong_minh\New folder"
     jupyter notebook
     ```
   - Trình duyệt sẽ mở thẳng thư mục chứa file bài tập.

---

### BƯỚC 2: MỞ VÀ CHẠY FILE NOTEBOOK TRÊN TRÌNH DUYỆT
1. Trên giao diện web Jupyter Notebook, click chọn file: **`Chap12_Diabetes_Notebook.ipynb`**.
2. **Cách chạy từng Cell theo yêu cầu của thầy:**
   - Chọn Cell đầu tiên (Cell 1), nhấn tổ hợp phím **`Shift + Enter`** (hoặc nút **Run** trên thanh công cụ) để chạy lần lượt từng Cell xuống dưới.
   - Thầy yêu cầu giải thích Cell nào thì dừng lại tại Cell đó để thuyết minh kết quả:
     - **Cell 1 - 3:** Tiền xử lý dữ liệu và điền Mean vào các giá trị 0.
     - **Cell 4 - 5:** Hiển thị biểu đồ nhiệt Heatmap tương quan.
     - **Cell 6 - 8:** Đánh giá 4 thuật toán với 10-fold CV trên Top 3 đặc trưng.
     - **Cell 9:** Bảng thực nghiệm mở rộng so sánh **3 features, 5 features, 7 features và toàn bộ 8 features**.
     - **Cell 10 - 11:** Huấn luyện mô hình tối ưu KNN ($k=19$) và lưu file `diabetes.sav`.
     - **Cell 12 - 13:** Xuất mã nguồn `REST_API.py` và `Predict_Diabetes.py`.

---

### BƯỚC 3: KHỞI ĐỘNG VÀ DEMO REST API TRÊN ANACONDA PROMPT
Khi thầy yêu cầu demo triển khai API và ứng dụng Client:

1. **Khởi động Server REST API:**
   - Mở một cửa sổ **Anaconda Prompt** thứ nhất.
   - Chuyển vào thư mục bài học và chạy server Flask:
     ```bash
     cd /d "d:\learning\phat_trien_he_thong_thong_minh\New folder"
     python REST_API.py
     ```
   - Màn hình sẽ hiển thị:
     ```
     Starting Diabetes Prediction REST API on http://127.0.0.1:5000/ ...
      * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     ```

2. **Chạy Client kiểm thử dự đoán thời gian thực:**
   - Mở một cửa sổ **Anaconda Prompt** thứ hai (song song với cửa sổ thứ nhất).
   - Chạy ứng dụng Client:
     ```bash
     cd /d "d:\learning\phat_trien_he_thong_thong_minh\New folder"
     python Predict_Diabetes.py
     ```
   - Nhập thông số mẫu kiểm thử để thầy thấy kết quả:
     - **Trường hợp 1 (Bình thường):** `BMI = 30`, `Age = 29`, `Glucose = 100` $\rightarrow$ Kết quả: **Not Diabetic (Độ tin cậy: 78.95%)**.
     - **Trường hợp 2 (Tiểu đường):** `BMI = 65`, `Age = 29`, `Glucose = 150` $\rightarrow$ Kết quả: **Diabetic (Độ tin cậy: 68.42%)**.

---
*Tài liệu được thiết kế tương thích 100% với môi trường chuẩn Anaconda và Jupyter Notebook.*

