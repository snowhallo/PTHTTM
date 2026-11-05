# HƯỚNG DẪN CHẠY VÀ THUYẾT TRÌNH CODE DEMO (THÀNH VIÊN 3)
**Dự án:** Deep Graph Learning in AI - Dự đoán Bệnh Tiểu đường  
**Môn học:** Phát triển Hệ thống Thông minh  
**Phần việc phụ trách:** Thành viên 3 (Dữ liệu y sinh, Tiền xử lý, Xây dựng đồ thị & Đóng gói PyG Data)  
**Tập dữ liệu:** [`data/diabetes_100k.csv`](file:///d:/learning/phat_trien_he_thong_thong_minh/data/diabetes_100k.csv) (100.000 bản ghi lâm sàng)

---

## 1. MỤC ĐÍCH CỦA BÀI CODE DEMO
Mã nguồn demo này chứng minh toàn bộ quy trình khoa học của Thành viên 3 đã được lập trình thực tế và chạy ra kết quả định lượng:
1. **Nạp & Phân tích dữ liệu lâm sàng 100k bản ghi (EDA):** Chứng minh mất cân bằng nhãn $10.76 : 1$ và đối chiếu ngưỡng chuẩn ADA 2024.
2. **Quy trình Tiền xử lý chuẩn & Chống Data Leakage:** Stratified Split $80/20$, chuẩn hóa `RobustScaler` (Median & IQR) và One-Hot Encoding chỉ fit trên Train.
3. **Thực thi Xây dựng Đồ thị Bệnh nhân:** Chạy đồng thời Phương án 1 (Baseline $k=10$) và Phương án 2 (Trọng số y sinh $k=8$, Gaussian RBF Kernel).
4. **Đo lường Định lượng:** Tính toán tỷ lệ đồng nhất nhãn (Homophily Ratio $h$) chứng minh PA2 đạt $94.11\%$.
5. **Đóng gói Chuẩn PyTorch Geometric:** Xuất ra đối tượng `torch_geometric.data.Data` và lưu tệp nhị phân `.pt` để bàn giao cho Thành viên 1 và 4 huấn luyện mô hình GCN / GraphSAGE / GAT.

---

## 2. CÁC TỆP NGUỒN CÓ SẴN TRONG THƯ MỤC
- [`demo_tv3_diabetes_graph.py`](file:///d:/learning/phat_trien_he_thong_thong_minh/demo_tv3_diabetes_graph.py): File mã nguồn Python hoàn chỉnh, chạy độc lập từ terminal.
- [`demo_tv3_diabetes_graph.ipynb`](file:///d:/learning/phat_trien_he_thong_thong_minh/demo_tv3_diabetes_graph.ipynb): File Jupyter Notebook trực quan, **đã được chạy sẵn toàn bộ cell kèm output**, bảng biểu và mô tả lý thuyết.
- [`data/patient_graph_tv3_demo.pt`](file:///d:/learning/phat_trien_he_thong_thong_minh/data/patient_graph_tv3_demo.pt): File đồ thị PyTorch Geometric đã được xuất sẵn để bàn giao.
- [`tv3_empirical_metrics.json`](file:///d:/learning/phat_trien_he_thong_thong_minh/tv3_empirical_metrics.json): File JSON lưu trữ đầy đủ các chỉ số thực nghiệm đồ thị.

---

## 3. CÁCH CHẠY DEMO

### CÁCH 1: Chạy trực tiếp từ Terminal / PowerShell (Nhanh & Ấn tượng)
1. Mở PowerShell hoặc Command Prompt tại thư mục dự án `d:\learning\phat_trien_he_thong_thong_minh`.
2. Chạy lệnh:
   ```powershell
   python demo_tv3_diabetes_graph.py
   ```
3. **Kết quả in ra màn hình:**
   ```text
   ================================================================================
   DEMO THÀNH VIÊN 3: KHÁM PHÁ DỮ LIỆU & XÂY DỰNG ĐỒ THỊ BỆNH NHÂN CHO GNN
   ================================================================================

   [1/5] Đang nạp tập dữ liệu từ: ...\data\diabetes_100k.csv...
     -> Kích thước tập dữ liệu: 100,000 dòng x 9 cột
     -> Danh sách các cột: ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'diabetes']
     -> Số lượng giá trị thiếu (Missing values): 0 ô

     [*] Phân tích độ mất cân bằng nhãn (Class Imbalance):
         - Lớp 0 (Âm tính / Không mắc bệnh): 91,500 mẫu (91.50%)
         - Lớp 1 (Dương tính / Mắc tiểu đường): 8,500 mẫu (8.50%)
         - Tỷ lệ mất cân bằng nghiêm ngặt: 10.76 : 1

     [*] Đối chiếu Chuẩn đoán Y khoa Vàng (ADA & WHO Standards):
         - HbA1c (Trung bình): Nhóm Bệnh = 6.93% (≥ 6.5% ngưỡng bệnh) vs Nhóm Khỏe = 5.40%
         - Đường huyết Glucose (Trung bình): Nhóm Bệnh = 194.1 mg/dL vs Nhóm Khỏe = 132.9 mg/dL

   [2/5] Thực hiện Tiền xử lý & Thiết lập Phòng thủ Rò rỉ Dữ liệu...
     -> Lấy mẫu chuẩn đại diện phân tầng: 10,000 bệnh nhân
     -> Phân tách phân tầng: Train = 8,000 nút, Test = 2,000 nút
     -> [CHỐNG LABEL LEAKAGE]: Biến mục tiêu 'diabetes' đã được tách riêng vào vector y.
     -> Kích thước vector đặc trưng nút (Node feature dimension): d = 14
     -> [CHỐNG STATISTICAL LEAKAGE]: Fit RobustScaler & OneHotEncoder DUY NHẤT trên Train!

   [3/5] Khởi tạo Đồ thị Bệnh nhân (So sánh 02 Phương án Thiết kế)...

     [*] Triển khai Phương án 1 (Baseline Homogeneous KNN, k=10):
         - Tổng số cạnh tạo lập (Train Graph): 80,000 cạnh
         - Tỷ lệ đồng nhất nhãn (Homophily Ratio h): 93.36%

     [*] Triển khai Phương án 2 (Clinically-Weighted KNN, k=8) - ĐỀ XUẤT:
         - Trọng số lâm sàng áp dụng: HbA1c=3.0, Glucose=3.0, BMI=2.0
         - Tổng số cạnh tạo lập (Train Graph): 64,000 cạnh
         - Tỷ lệ đồng nhất nhãn (Homophily Ratio h): 94.11%
         -> KẾT QUẢ: PA2 tăng độ thuần cụm +0.75%, giảm 20% số cạnh dư thừa!

   [4/5] Thiết lập Đồ thị Quy nạp (Inductive Graph Setting) cho tập Test...
     -> Số cạnh kết nối Inductive từ Train sang Test: 16,000 cạnh
     -> [CHỐNG TRANSDUCTIVE LEAKAGE]: Không có bất kỳ cạnh nội bộ nào giữa các nút Test (Test-Test = 0)!

   [5/5] Đóng gói thành đối tượng chuẩn PyTorch Geometric (torch_geometric.data.Data)...

     === ĐỐI TƯỢNG ĐỒ THỊ PYTORCH GEOMETRIC HOÀN CHỈNH ===
     Data(x=[8000, 14], edge_index=[2, 64000], edge_attr=[64000, 1], y=[8000])
     - Số lượng nút (Number of Nodes |V|): 8,000
     - Số lượng cạnh (Number of Edges |E|): 64,000
     - Số chiều đặc trưng mỗi nút (Feature dimension): 14
     - Kích thước ma trận cạnh (edge_index shape): [2, 64000]
     - Có nút cô lập không (Has isolated nodes): False
     - Có tự khuyên không (Has self loops): True

   [+] ĐÃ LƯU FILE ĐỒ THỊ BÀN GIAO CHO THÀNH VIÊN 1 & 4 TẠI: ...\data\patient_graph_tv3_demo.pt
   ================================================================================
   DEMO HOÀN THÀNH XUẤT SẮC - SẴN SÀNG BÁO CÁO VÀ THỰC HIỆN LIVE DEMO!
   ================================================================================
   ```

---

### CÁCH 2: Trình diễn qua Jupyter Notebook (Giao diện trực quan cho hội đồng)
1. Mở file [`demo_tv3_diabetes_graph.ipynb`](file:///d:/learning/phat_trien_he_thong_thong_minh/demo_tv3_diabetes_graph.ipynb) bằng **VS Code** (đã có tiện ích Jupyter) hoặc chạy lệnh `jupyter lab` / `jupyter notebook`.
2. Toàn bộ notebook đã được chạy sẵn và lưu output, bạn có thể cuộn qua từng phần để giải thích:
   - **Cell 1:** Nạp các thư viện `torch`, `torch_geometric`, `sklearn`, `pandas`.
   - **Cell 2 & 3:** Hiển thị 5 dòng đầu của tập 100k, in ra bảng phân bố nhãn mất cân bằng và so sánh chỉ số vàng ADA.
   - **Cell 4:** Code tiền xử lý chia Train/Test 80/20, One-Hot Encoder và `RobustScaler` độc lập.
   - **Cell 5:** Code thuật toán KNN so sánh trực tiếp Homophily giữa PA1 ($93.36\%$) và PA2 ($94.11\%$).
   - **Cell 6:** Khối code minh chứng thiết lập Inductive (không có cạnh nội bộ Test-Test).
   - **Cell 7:** Đóng gói đối tượng `torch_geometric.data.Data` và lệnh `torch.save()`.

---

## 4. KỊCH BẢN THUYẾT TRÌNH LIVE DEMO TRONG 2 PHÚT (MẪU)

Khi giảng viên yêu cầu: *"Em hãy demo phần việc của Thành viên 3"*, bạn thao tác như sau:

1. **Mở terminal và gõ `python demo_tv3_diabetes_graph.py`:**
   > *"Thưa thầy/cô, đây là pipeline tự động hóa toàn bộ khâu chuẩn bị dữ liệu và tạo đồ thị của Thành viên 3."*
2. **Chỉ vào kết quả Phần 1 & 2 (EDA & Preprocessing):**
   > *"Ở bước đầu tiên, hệ thống nạp tập dữ liệu lâm sàng 100.000 bệnh nhân. Chúng em phát hiện dữ liệu mất cân bằng 10.76 : 1 và hai chỉ số HbA1c cùng Glucose vượt ngưỡng bệnh chuẩn ADA. Nhóm đã thực hiện Stratified Split 80/20 và chuẩn hóa RobustScaler độc lập trên tập Train để bảo toàn các ca bệnh ngoại lệ."*
3. **Chỉ vào kết quả Phần 3 & 4 (Graph Construction & Metrics):**
   > *"Tiếp theo là khâu tạo đồ thị bệnh nhân: Nhóm đã thực nghiệm so sánh hai phương án. Phương án 1 dùng KNN thuần đạt độ thuần cụm 93.36%. Phương án 2 tích hợp trọng số y sinh ưu tiên HbA1c và Glucose giúp độ thuần Homophily tăng lên 94.11%, đồng thời tiết kiệm 20% bộ nhớ cạnh."*
4. **Chỉ vào kết quả Phần 5 (PyG Data & Bàn giao):**
   > *"Cuối cùng, đồ thị được đóng gói chuẩn thành đối tượng `Data` của PyTorch Geometric với 8.000 nút, 14 đặc trưng và 64.000 cạnh kèm trọng số Gaussian RBF. Nhóm xuất ra file `patient_graph_tv3_demo.pt` để Thành viên 1 và Thành viên 4 trực tiếp nạp vào huấn luyện các mô hình GCN, GraphSAGE và GAT."*

---

## 5. GIẢI THÍCH CÁC THÔNG SỐ TRONG ĐỐI TƯỢNG ĐỒ THỊ `Data(...)`

Nếu thầy cô hỏi từng trường dữ liệu trong đối tượng `Data` nghĩa là gì:
- **`x=[8000, 14]`:** Ma trận đặc trưng của 8.000 bệnh nhân trong tập Train. Mỗi bệnh nhân được biểu diễn bằng vector 14 chiều (6 thuộc tính số học sau khi qua RobustScaler + 8 thuộc tính nhị phân sau One-Hot Encoding giới tính và hút thuốc).
- **`edge_index=[2, 64000]`:** Ma trận kết nối cạnh dạng COO (Coordinate format). Dòng 0 là chỉ số nút nguồn (Source node $i$), dòng 1 là chỉ số nút đích (Target node $j$). Có 64.000 cạnh tương ứng với mỗi bệnh nhân kết nối với $k=8$ bệnh nhân tương đồng nhất ($8.000 \times 8 = 64.000$).
- **`edge_attr=[64000, 1]`:** Trọng số thực của 64.000 cạnh, tính theo hàm hạt nhân Gauss (Gaussian RBF Kernel), thể hiện mức độ tương đồng y sinh giữa 2 bệnh nhân (giá trị nằm trong khoảng $(0, 1]$).
- **`y=[8000]`:** Nhãn chẩn đoán thực tế của 8.000 bệnh nhân ($0$: Không mắc bệnh, $1$: Mắc đái tháo đường).

