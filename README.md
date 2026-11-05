# PHÁT TRIỂN HỆ THỐNG THÔNG MINH (PTHTTM)
### Học viện Công nghệ Bưu chính Viễn thông (PTIT)
**Chủ đề:** Deep Graph Learning in AI • Hệ Thống Hỗ Trợ Ra Quyết Định Lâm Sàng Chẩn Đoán & Quản Lý Đái Tháo Đường (**GlucoGraph CDSS**)  
**Mã kho lưu trữ GitHub:** [snowhallo/PTHTTM](https://github.com/snowhallo/PTHTTM)

---

## 1. TỔNG QUAN DỰ ÁN

Dự án nghiên cứu và phát triển phần mềm ứng dụng lâm sàng thực tế dựa trên công nghệ **Mạng nơ-ron Đồ thị (Deep Graph Learning / GNN)** nhằm giải quyết bài toán chẩn đoán sớm và cá thể hóa phác đồ điều trị bệnh Đái tháo đường (Diabetes Type 2):
- **Tập dữ liệu lâm sàng y sinh:** 100.000 hồ sơ bệnh nhân thực tế (`data/diabetes_100k.csv`).
- **Mô hình suy luận cốt lõi:** Graph Attention Network (GAT 2 tầng) trên Mạng lưới tương đồng bệnh nhân (Patient Similarity Network - k-NN có trọng số lâm sàng theo chuẩn ADA 2024).
- **Sản phẩm ứng dụng đầu cuối:** Phần mềm web hỗ trợ quyết định y khoa **GlucoGraph CDSS** phục vụ công tác khám bệnh, chẩn đoán nguy cơ và lập phác đồ can thiệp.

---

## 2. HƯỚNG DẪN CÀI ĐẶT MÔI TRƯỜNG

### 2.1. Yêu cầu hệ thống
- Hệ điều hành: Windows 10/11, macOS, hoặc Linux.
- Phiên bản Python: Python 3.10 trở lên (khuyến nghị Python 3.11 hoặc 3.12).
- Trình duyệt web hiện đại: Chrome, Edge, Brave, hoặc Firefox.

### 2.2. Cài đặt các thư viện phụ thuộc
Mở terminal (PowerShell / Command Prompt / Terminal) tại thư mục gốc của dự án và chạy:

```bash
pip install -r requirements.txt
```

Hoặc cài đặt các gói thư viện chính:
```bash
pip install streamlit plotly pandas numpy scikit-learn networkx torch torch_geometric
```

---

## 3. HƯỚNG DẪN CHẠY PHẦN MỀM DEMO ỨNG DỤNG LÂM SÀNG (GLUCOGRAPH CDSS)

Hệ thống cung cấp giao diện web hiện đại, chuẩn y tế lâm sàng, phân tách độ tương phản cao và trực quan hóa mạng lưới đồ thị thời gian thực.

### Cách 1: Khởi động 1-Click (Dành cho Windows)
Vào thư mục `demo_web_deepgraph/` và nhấp đúp chuột vào tệp:
```text
demo_web_deepgraph/run_demo.bat
```
Tập lệnh sẽ tự động kiểm tra môi trường, nạp cấu hình UTF-8 và khởi chạy ứng dụng trên trình duyệt web tại địa chỉ `http://localhost:8501`.

---

### Cách 2: Khởi động từ Dòng lệnh (Terminal / PowerShell)
1. Mở PowerShell hoặc Terminal tại thư mục dự án:
   ```bash
   cd demo_web_deepgraph
   ```
2. Chạy lệnh:
   ```bash
   streamlit run app.py
   ```
3. Trình duyệt sẽ tự động mở trang chủ `http://localhost:8501`.

---

## 4. QUY TRÌNH NGHIỆP VỤ & TRẢI NGHIỆM TRÊN GIAO DIỆN

Hệ thống được thiết kế theo quy trình vận hành bệnh viện thực tế gồm 4 phân hệ liên kết chặt chẽ:

### Phân hệ 1: Giám Sát Dịch Tễ & Tổng Quan Lâm Sàng (Epidemiology Dashboard)
- **Thẻ KPI:** Giám sát thời gian thực quy mô quần thể 100.000 hồ sơ (tỷ lệ mắc đái tháo đường, tiền đái tháo đường, nhóm cần can thiệp khẩn cấp).
- **Biểu đồ phân tán:** Đối chiếu hai chỉ số sinh hóa cốt lõi (HbA1c & Đường huyết lúc đói) với các ngưỡng chẩn đoán vàng ADA 2024.
- **Biểu đồ cột:** Tỷ lệ phân bố bệnh học theo từng độ tuổi và bảng phân tích hệ số nguy cơ tương đối (RR).

### Phân hệ 2: Buồng Khám & Chẩn Đoán Đồ Thị (GNN Consultation Engine)
- **Phương thức tiếp nhận:**
  - Nhập chỉ số khám tự do của bệnh nhân.
  - Hoặc chọn các hồ sơ ca bệnh mẫu đại diện (Nguy cơ cao, Tiền đái tháo đường, Khỏe mạnh).
  - Hoặc tiếp nhận trực tiếp từ danh bạ bệnh án EMR.
- **Thực hiện phân tích:** Nhấn nút **"Thực Hiện Phân Tích & Chẩn Đoán Đồ Thị"**:
  - Hệ thống tính toán vector đặc trưng 7 chiều lâm sàng.
  - Lan truyền thông điệp (Message Passing) qua các láng giềng gần nhất trên đồ thị.
  - Hiển thị kết luận phân tầng nguy cơ (% xác suất và căn cứ chẩn đoán).
  - Bảng bằng chứng đối chứng 5 ca bệnh tương đồng gần nhất trong cơ sở dữ liệu.
  - Biểu đồ mạng tương tác (Plotly Local Patient Subgraph) định vị nốt bệnh nhân giữa các ca bệnh lân cận.
- **Chuyển tuyến điều trị:** Nhấn nút *"Lập Phác Đồ Can Thiệp & In Phiếu Kết Quả Cho Ca Này"* để chuyển sang Phân hệ 3.

### Phân hệ 3: Phác Đồ Điều Trị & Quản Lý Lâm Sàng (Care Plan & Protocols)
- Tự động đồng bộ hóa hồ sơ bệnh nhân từ Buồng khám.
- Hiển thị phác đồ can thiệp 3 tầng theo chuẩn **ADA Standards of Care in Diabetes 2024**:
  - Mục tiêu kiểm soát HbA1c cá thể hóa.
  - Can thiệp dinh dưỡng & lối sống.
  - Phác đồ dùng thuốc (Metformin đầu tay, phối hợp thuốc SGLT2i / GLP-1 RA khi có biến chứng tim mạch/thận) kèm cảnh báo chống chỉ định.
- **Phiếu kết quả chẩn đoán:** Tạo phiếu kết quả chuẩn bệnh viện có thể in trực tiếp (Ctrl + P).

### Phân hệ 4: Hồ Sơ Bệnh Án Điện Tử (EMR Patient Directory)
- Quản trị kho 100.000 hồ sơ bệnh án điện tử.
- Bộ lọc đa tiêu chí: Tình trạng chẩn đoán, giới tính, khoảng tuổi, tìm kiếm theo Mã bệnh án (`BA-XXXXXX`).
- Nút **"Tiếp Nhận Vào Buồng Khám"** cho phép chọn nhanh bất kỳ bệnh án nào và chuyển ngay sang Buồng khám để phân tích đồ thị.

---

## 5. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
PTHTTM/
│
├── demo_web_deepgraph/              # Ứng dụng Web Lâm Sàng GlucoGraph CDSS
│   ├── app.py                       # File ứng dụng Streamlit chính (UI & Điều hướng)
│   ├── config.py                    # Cấu hình bảng màu y tế, chuẩn ADA 2024, phác đồ
│   ├── data_loader.py               # Mô-đun nạp & xử lý dữ liệu hồ sơ lâm sàng
│   ├── utils_graph.py               # Thuật toán k-NN có trọng số y khoa, vẽ mạng Plotly
│   ├── run_demo.bat                 # Script chạy nhanh 1-click trên Windows
│   ├── requirements.txt             # Danh sách thư viện phụ thuộc của ứng dụng
│   ├── .streamlit/config.toml       # Cấu hình giao diện Streamlit (Light Medical Theme)
│   ├── data/
│   │   └── diabetes_100k.csv        # Dữ liệu 100.000 hồ sơ bệnh nhân đi kèm
│   └── modules/
│       ├── view_dashboard.py        # Phân hệ 1: Giám sát Dịch tễ (Dashboard)
│       ├── view_consultation.py     # Phân hệ 2: Buồng Khám & Động cơ chẩn đoán GAT
│       ├── view_treatment.py        # Phân hệ 3: Phác đồ can thiệp ADA 2024 & Phiếu in
│       └── view_records.py          # Phân hệ 4: Quản lý Hồ sơ Bệnh án EMR 100k
│
├── data/
│   └── diabetes_100k.csv            # Cơ sở dữ liệu 100.000 hồ sơ bệnh nhân (Root)
│
├── requirements.txt                 # File danh sách thư viện toàn bộ dự án
├── .gitignore                       # Cấu hình loại trừ file rác, file tạm
└── README.md                        # Tài liệu hướng dẫn sử dụng & vận hành dự án
```

---

## 6. BẢN QUYỀN & THÔNG TIN HỌC PHẦN
- **Môn học:** Phát triển Hệ thống Thông minh (PTHTTM)
- **Đơn vị:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)
- **Chủ đề nghiên cứu:** Ứng dụng Mạng nơ-ron Đồ thị (Deep Graph Learning) trong Chẩn đoán & Hỗ trợ Quyết định Lâm sàng Đái tháo đường Type 2.

