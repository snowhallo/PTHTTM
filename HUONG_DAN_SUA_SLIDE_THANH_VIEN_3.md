# HƯỚNG DẪN CHI TIẾT SỬA SLIDE THÀNH VIÊN 3 (SLIDE 23 - 32)
**Dự án:** Deep Graph Learning in AI - Dự đoán Bệnh Tiểu đường (Diabetes Prediction)  
**Môn học:** Phát triển Hệ thống Thông minh  
**Link Canva Slide:** [Deep Graph Learning – 44 Slides | Canva](https://www.canva.com/design/DAHZ900uO14/I68j5Pu82YYAFAoV2Z-IIQ/edit)  
**Thư mục chứa ảnh minh họa:** [`d:\learning\phat_trien_he_thong_thong_minh\slide_assets\`](file:///d:/learning/phat_trien_he_thong_thong_minh/slide_assets/)

---

## TỔNG QUAN PHÂN CÔNG THÀNH VIÊN 3
Thành viên 3 phụ trách toàn bộ từ **Slide 23 đến Slide 32** (tổng cộng 10 slide), bao gồm:
1. Phát biểu bài toán y sinh và phân tích tập dữ liệu lâm sàng 100k.
2. Ý nghĩa lâm sàng của các đặc trưng (HbA1c, Glucose, BMI...) theo chuẩn y khoa quốc tế.
3. Khám phá dữ liệu (EDA), phân tích tương quan và xử lý mất cân bằng nhãn ($10.8 : 1$).
4. Quy trình tiền xử lý chuẩn hóa đặc trưng (RobustScaler, OneHotEncoder).
5. Cơ sở khoa học chuyển đổi từ dữ liệu bảng (Tabular) sang cấu trúc đồ thị (Graph).
6. Hai phương án thiết kế đồ thị KNN (Baseline vs Trọng số y sinh) và đo lường độ thuần cụm (Homophily Ratio).
7. Thiết lập phòng thủ chống rò rỉ dữ liệu (Chống Label Leakage & Transductive Test Leakage).

---

## HƯỚNG DẪN SỬA CHI TIẾT TỪNG SLIDE

### SLIDE 23: Trang Tiêu đề Phân đoạn (Divider Slide)
- **Tiêu đề hiện tại:** "Phần 3: Bài toán Dự đoán Bệnh tiểu đường & Khởi tạo Đồ thị" (hoặc tiêu đề tương đương).
- **Hiện trạng:** Đã có bố cục tốt.
- **Việc cần làm:**
  - Kiểm tra lại họ tên, mã sinh viên và vai trò: *"Thành viên 3: Phụ trách Bài toán Y sinh, Tiền xử lý dữ liệu & Thiết kế Đồ thị Bệnh nhân"*.
- **Lời thoại thuyết trình:**
  > *"Kính thưa thầy/cô và các bạn, tiếp nối phần lý thuyết nền tảng về GNN của Thành viên 2, em xin đại diện nhóm trình bày Phần 3: Phân tích bài toán dự đoán bệnh tiểu đường từ dữ liệu y sinh thực tế và cơ chế khoa học để chuyển đổi dữ liệu bảng thành cấu trúc đồ thị cho GNN huấn luyện."*

---

### SLIDE 24: Tổng quan Tập Dữ liệu Lâm sàng (Dataset Overview)
- **Hiện trạng:** Slide hiện tại ghi chung chung *"khoảng 100.000 bản ghi theo report"* và thiếu biểu đồ phân bố thực tế.
- **Việc cần làm:**
  1. Cập nhật các con số chính xác:
     - **Quy mô:** $100,000$ bản ghi bệnh nhân, $9$ cột thuộc tính ($8$ đặc trưng lâm sàng + $1$ nhãn mục tiêu `diabetes`).
     - **Độ hoàn thiện:** $0$ giá trị khuyết thiếu ($0$ missing values).
     - **Mất cân bằng nhãn nghiêm ngặt:** $91,500$ mẫu âm tính ($91.50\%$) vs $8,500$ mẫu dương tính ($8.50\%$) $\to$ Tỷ lệ mất cân bằng **10.76 : 1**.
  2. Tải và chèn hình ảnh: [`fig_1_class_imbalance.png`](file:///d:/learning/phat_trien_he_thong_thong_minh/slide_assets/fig_1_class_imbalance.png) vào khoảng trống bên phải slide.
- **Lời thoại thuyết trình:**
  > *"Nhóm sử dụng tập dữ liệu lâm sàng gồm 100.000 bệnh nhân với 8 biến đặc trưng y sinh. Điểm mấu chốt đầu tiên là hiện tượng mất cân bằng nhãn rất nặng với tỷ lệ 10.76 : 1 (chỉ có 8.5% bệnh nhân mắc bệnh). Do đó, ngay từ khâu tiền xử lý, nhóm bắt buộc phải sử dụng kỹ thuật Stratified Split và tối ưu metric PR-AUC thay vì chỉ nhìn vào Accuracy thông thường."*

---

### SLIDE 25: Ý nghĩa Lâm sàng & Tiêu chuẩn Chẩn đoán Y khoa (Clinical Features)
- **Hiện trạng:** Liệt kê các cột `age, bmi, HbA1c, blood_glucose` nhưng thiếu căn cứ y khoa quốc tế.
- **Việc cần làm:**
  1. Bổ sung trích dẫn tiêu chuẩn chẩn đoán vàng của **Hiệp hội Đái tháo đường Hoa Kỳ (ADA 2024) và WHO**:
     - **Chỉ số HbA1c (Hemoglobin glycated):** Bình thường $< 5.7\%$, Tiền tiểu đường $5.7 - 6.4\%$, **Đái tháo đường $\ge 6.5\%$**. (Thực tế tập dữ liệu: Nhóm bệnh đạt trung bình $6.93\%$, nhóm khỏe $5.40\%$).
     - **Đường huyết (Blood Glucose Level):** Đường huyết đói chuẩn đoán bệnh khi $\ge 126$ mg/dL; ngẫu nhiên $\ge 200$ mg/dL. (Thực tế: Nhóm bệnh đạt trung bình $194.1$ mg/dL so với nhóm khỏe $132.9$ mg/dL).
     - **Chỉ số BMI:** Phân độ béo phì $\ge 25.0$ theo chuẩn châu Á.
  2. Chèn hình ảnh: [`fig_2_clinical_markers.png`](file:///d:/learning/phat_trien_he_thong_thong_minh/slide_assets/fig_2_clinical_markers.png) vào slide.
- **Lời thoại thuyết trình:**
  > *"Để xây dựng đồ thị có ý nghĩa sinh học, nhóm đã đối chiếu với chuẩn y khoa của ADA 2024. Phân tích thực nghiệm trên 100.000 mẫu cho thấy hai chỉ số HbA1c và Glucose phân tách rõ rệt giữa hai nhóm bệnh nhân, hoàn toàn trùng khớp với ngưỡng chẩn đoán lâm sàng của bác sĩ."*

---

### SLIDE 26: Khám phá Dữ liệu (EDA) & Phân tích Tương quan
- **Hiện trạng:** Đang thiếu ma trận tương quan giữa các biến.
- **Việc cần làm:**
  1. Nêu rõ kết quả phân tích tương quan Pearson:
     - **HbA1c ($r = 0.40$)** và **Blood Glucose ($r = 0.42$)** có hệ số tương quan dương mạnh nhất với biến mục tiêu `diabetes`.
     - Nhóm yếu tố nguy cơ nền: **Tuổi tác ($r = 0.26$)**, **BMI ($r = 0.21$)**, **Tăng huyết áp ($r = 0.20$)**.
     - Giới tính và tiền sử hút thuốc có tương quan trực tiếp yếu hơn nhưng cung cấp ngữ cảnh đa chiều quan trọng.
  2. Chèn hình ảnh: [`fig_3_correlation_heatmap.png`](file:///d:/learning/phat_trien_he_thong_thong_minh/slide_assets/fig_3_correlation_heatmap.png).
- **Lời thoại thuyết trình:**
  > *"Biểu đồ nhiệt Pearson chứng minh rằng HbA1c và Glucose là hai biến mang tín hiệu dự báo mạnh nhất. Đây chính là tiền đề toán học để lát nữa nhóm đề xuất Phương án 2: Gán trọng số lâm sàng ưu tiên cho hai biến này khi tính khoảng cách không gian giữa các bệnh nhân."*

---

### SLIDE 27: Phân tích Giới hạn Dữ liệu & Tính Đại diện (Data Limitations)
- **Hiện trạng:** Cần làm sắc sảo hơn góc nhìn phản biện khoa học.
- **Việc cần làm:**
  - Bổ sung 3 luận điểm phản biện chính:
    1. **Tính chất dữ liệu tổng hợp (Synthetic Data):** Dữ liệu được trích xuất từ hồ sơ điện tử y tế kết hợp tổng hợp mô phỏng, do đó phân phối rất mượt và không có ô khuyết thiếu (0 missing value).
    2. **Định dạng dữ liệu cắt ngang (Cross-sectional):** Không có chuỗi thời gian diễn tiến bệnh (longitudinal data) của từng bệnh nhân qua các năm.
    3. **Tính đại diện quần thể:** Tỷ lệ bệnh nhân $8.5\%$ phản ánh sát tỷ lệ dịch tễ học tiểu đường toàn cầu (~10.5% theo IDF Diabetes Atlas 2021).
- **Lời thoại thuyết trình:**
  > *"Dưới góc độ khoa học dữ liệu, nhóm nhận diện rõ giới hạn: Đây là dữ liệu cắt ngang tại một thời điểm khám. Tuy nhiên, tính chất phân phối dịch tễ học 8.5% là hoàn toàn tương đồng với thực tế lâm sàng, tạo môi trường thử nghiệm khách quan cho mô hình."*

---

### SLIDE 28: QUY TRÌNH TIỀN XỬ LÝ & CHUẨN HÓA ĐẶC TRƯNG
- **CẢNH BÁO LỖI:** Slide hiện tại đang chèn hình **mạng nơ-ron đa tầng MLP (`INPUT → LAYER 1 → LAYER 2 → OUTPUT`)**. Đây là hình vẽ sai, không liên quan đến tiền xử lý.
- **Việc cần làm:**
  1. **XÓA BỎ HÌNH MLP HIỆN TẠI.**
  2. Chèn hình ảnh thay thế: [`fig_4_pipeline_architecture.png`](file:///d:/learning/phat_trien_he_thong_thong_minh/slide_assets/fig_4_pipeline_architecture.png).
  3. Cập nhật các luận điểm công nghệ:
     - **Mã hóa One-Hot Encoding:** Xử lý `gender` (Female/Male/Other) và `smoking_history` (never, current, former...).
     - **Chuẩn hóa RobustScaler:** Sử dụng Trung vị (Median) và Khoảng tứ phân vị (IQR) thay vì StandardScaler:
       $$x_{\text{scaled}} = \frac{x - Q_2(x)}{Q_3(x) - Q_1(x)}$$
       *Lý do:* Giữ tính trọn vẹn của các chỉ số xét nghiệm cực đoan (outliers y sinh) mà không làm lệch tâm phân phối.
     - **Quy tắc cách ly:** Fit Scaler và Encoder **DUY NHẤT** trên tập Train, sau đó Transform sang Validation/Test.
- **Lời thoại thuyết trình:**
  > *"Ở khâu chuẩn hóa, nhóm lựa chọn RobustScaler thay vì StandardScaler hay MinMaxScaler. Trong y học, các chỉ số đường huyết hay BMI cao đột biến không phải là lỗi nhập liệu mà là triệu chứng lâm sàng quan trọng. RobustScaler sử dụng trung vị và khoảng tứ phân vị IQR giúp giữ nguyên giá trị thông tin của các ca bệnh nặng mà không bị nhiễu."*

---

### SLIDE 29: Cơ sở Khoa học Chuyển đổi Dữ liệu Bảng sang Đồ thị (Why Graph?)
- **Hiện trạng:** Đã có ý tưởng nhưng cần giải thích chặt chẽ tại sao GNN vượt trội mô hình truyền thống (XGBoost/MLP).
- **Việc cần làm:**
  - Nhấn mạnh sự đối chiếu giữa 2 hệ hình:
    - **Mô hình học máy truyền thống (Tabular ML / i.i.d Assumption):** Giả định các dòng bệnh nhân hoàn toàn độc lập, xét nghiệm của bệnh nhân A không liên quan đến bệnh nhân B.
    - **Hệ hình Đồ thị Y sinh (Graph Learning):** Bệnh nhân tương tự nhau về hồ sơ bệnh lý sẽ có nguy cơ bệnh tương tự nhau. Bằng cách nối cạnh giữa các bệnh nhân tương đồng, GNN cho phép thực hiện **Message Passing** (truyền thông điệp đặc trưng), giúp mô hình học được cấu trúc phân cụm quần thể bệnh lý mà mạng nơ-ron thông thường bỏ sót.
- **Lời thoại thuyết trình:**
  > *"Tại sao dữ liệu bảng lại cần chuyển sang đồ thị? Học máy truyền thống luôn giả định mỗi bệnh nhân là một mẫu i.i.d độc lập. Nhưng trong y học thực tế, các bác sĩ luôn so sánh một ca bệnh mới với các hồ sơ bệnh án có cùng nhóm triệu chứng tương tự. Đồ thị hóa giúp mô hình GNN truyền thông tin qua lại giữa các ca bệnh tương đồng thông qua các vòng Message Passing."*

---

### SLIDE 30 & 31: Thiết kế Đồ thị KNN & Đo lường Độ thuần Đồ thị (Graph Proposals)
- **Hiện trạng:** Thiếu các tham số cụ thể ($k$, metric, trọng số cạnh) và số liệu đo lường.
- **Việc cần làm:**
  1. Trình bày rõ ràng **02 Phương án Thiết kế Đồ thị**:
     - **Phương án 1 (Baseline Homogeneous KNN):**
       - Chọn $k = 10$, khoảng cách Euclidean thông thường.
       - Tổng số cạnh: $80,000$ cạnh (trên mẫu chuẩn 8,000 nút train).
       - Tỷ lệ thuần cụm nhãn (Homophily Ratio): $h = 93.36\%$.
     - **Phương án 2 (Clinically-Weighted KNN - Đề xuất chọn):**
       - Gán trọng số lâm sàng ưu tiên: $\text{HbA1c} \times 3.0$, $\text{Blood Glucose} \times 3.0$, $\text{BMI} \times 2.0$.
       - Chọn $k = 8$, hàm trọng số cạnh Gaussian RBF:
         $$W_{ij} = \exp\left(-\frac{d(i, j)^2}{2\sigma^2}\right)$$
       - Tổng số cạnh: $64,000$ cạnh.
       - Tỷ lệ thuần cụm nhãn: **$h = 94.11\%$** ($+0.75\%$ độ thuần, giảm $20\%$ số cạnh dư thừa).
  2. Chèn hình ảnh minh họa cấu trúc đồ thị: [`fig_6_knn_graph_topology.png`](file:///d:/learning/phat_trien_he_thong_thong_minh/slide_assets/fig_6_knn_graph_topology.png).
- **Lời thoại thuyết trình:**
  > *"Nhóm đã triển khai thực nghiệm cả hai phương án tạo đồ thị. Kết quả chứng minh Phương án 2 với trọng số lâm sàng vượt trội hơn: Tỷ lệ Homophily đạt tới 94.11%, các nút cùng nhãn kết nối chặt chẽ với nhau hơn, đồng thời giảm được 20% số cạnh dư thừa, giúp đồ thị gọn nhẹ và huấn luyện nhanh hơn."*

---

### SLIDE 32: THIẾT LẬP PHÒNG THỦ CHỐNG DATA LEAKAGE (BẢO VỆ ĐỒ THỊ)
- **Hiện trạng:** Nội dung quan trọng nhất để trả lời phản biện của giảng viên nhưng chưa có sơ đồ trực quan.
- **Việc cần làm:**
  1. Nêu rõ hai nguyên tắc bảo vệ nghiêm ngặt:
     - **Nguyên tắc 1 - Chống Label Leakage:** Cột nhãn mục tiêu `diabetes` bị loại bỏ $100\%$ ra khỏi không gian đặc trưng trước khi tính khoảng cách KNN. Khoảng cách giữa hai bệnh nhân chỉ tính dựa trên triệu chứng lâm sàng.
     - **Nguyên tắc 2 - Chống Transductive Leakage (Thiết lập Inductive Graph):**
       + Chia Stratified Split $80/20$ trước khi xây dựng đồ thị.
       + Đồ thị Train $G_{\text{train}}$ chỉ gồm các nút Train.
       + Nút Test khi đánh giá chỉ được tìm $k$ láng giềng trong Train để nhận thông điệp (cạnh có hướng Test $\to$ Train). **Tuyệt đối không tạo cạnh giữa các nút Test với nhau (Test-Test = 0)**.
  2. Chèn hình ảnh: [`fig_5_data_leakage_defense.png`](file:///d:/learning/phat_trien_he_thong_thong_minh/slide_assets/fig_5_data_leakage_defense.png).
- **Lời thoại thuyết trình:**
  > *"Để đảm bảo tính khách quan y khoa, nhóm áp dụng thiết lập Inductive Graph nghiêm ngặt: Không dùng nhãn để tìm hàng xóm và tuyệt đối không tạo cạnh nội bộ giữa các bệnh nhân tập Test. Khi có một bệnh nhân mới đến khám, mô hình chỉ đối chiếu họ với kho bệnh án Train sẵn có mà không để thông tin kiểm thử thẩm thấu ngược lại mô hình."*

---

## BẢNG TỔNG KẾT THAO TÁC CẦN SỬA TRÊN CANVA

| Slide | Thao tác cần làm | Tệp ảnh chèn |
| :---: | :--- | :--- |
| **24** | Điền số liệu $100.000$ mẫu, mất cân bằng $10.76 : 1$, $0$ missing | `fig_1_class_imbalance.png` |
| **25** | Bổ sung chuẩn y khoa ADA $\text{HbA1c} \ge 6.5\%$, Glucose $\ge 126$ | `fig_2_clinical_markers.png` |
| **26** | Điền tương quan Pearson: HbA1c ($0.40$), Glucose ($0.42$) | `fig_3_correlation_heatmap.png` |
| **28** | **XÓA HÌNH MẠNG MLP**, thay bằng sơ đồ Pipeline 4 bước | `fig_4_pipeline_architecture.png` |
| **30-31** | Điền so sánh PA1 ($h=93.36\%$) vs PA2 ($h=94.11\%$, $k=8$) | `fig_6_knn_graph_topology.png` |
| **32** | Trình bày 2 cơ chế chống Label & Transductive Leakage | `fig_5_data_leakage_defense.png` |

