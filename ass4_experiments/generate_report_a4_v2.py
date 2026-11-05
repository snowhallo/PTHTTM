import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_comprehensive_report():
    print("Bắt đầu khởi tạo báo cáo Assignment 04...")
    doc = docx.Document()
    
    # Page setup - Margins: Left 3cm, Right 2cm, Top 2cm, Bottom 2cm (Chuẩn luận văn PTIT)
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        section.page_width = Cm(21.0) # Khổ A4
        section.page_height = Cm(29.7)
        
    # Typography Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(4)
    
    # Helper functions for styling
    def set_cell_background(cell, fill_color):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="B0BEC5", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D) # Navy Blue PTIT
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0) # Academic Blue
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48) # Slate
        return p

    def add_p(text, indent=True):
        p = doc.add_paragraph()
        if indent:
            p.paragraph_format.first_line_indent = Cm(1.0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        run = p.add_run(text)
        run.font.size = Pt(12)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Cm(1.2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.2
        run = p.add_run(text)
        run.font.size = Pt(11.5)
        return p

    def add_note_box(text, title="Nhận xét quan trọng:"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Cm(16.0)
        set_cell_background(cell, "F0F4F8")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:color="2B6CB0"/>'
            f'<w:top w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.2
        run_t = p.add_run(title + " ")
        run_t.bold = True
        run_t.font.size = Pt(11)
        run_t.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        run_b = p.add_run(text)
        run_b.font.size = Pt(11)
        run_b.font.italic = True
        run_b.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(4)

    def add_image_with_caption(img_path, fig_title, source, read_guide, obs, explanation, limits, width_inch=6.0):
        if not os.path.exists(img_path):
            print(f"CẢNH BÁO: Không tìm thấy tệp ảnh: {img_path}")
            return
        # Image
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inch))
        
        # Caption title
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(2)
        run_cap = p_cap.add_run(fig_title)
        run_cap.bold = True
        run_cap.font.size = Pt(11)
        run_cap.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        # Caption metadata (5 academic elements)
        meta_items = [
            ("Nguồn và cell liên quan: ", source),
            ("Cách đọc: ", read_guide),
            ("Quan sát: ", obs),
            ("Giải thích chi tiết: ", explanation),
            ("Giới hạn diễn giải: ", limits)
        ]
        for label, content in meta_items:
            p_meta = doc.add_paragraph()
            p_meta.paragraph_format.left_indent = Cm(0.5)
            p_meta.paragraph_format.space_after = Pt(2)
            p_meta.paragraph_format.line_spacing = 1.15
            run_lbl = p_meta.add_run(label)
            run_lbl.bold = True
            run_lbl.font.size = Pt(10)
            run_lbl.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
            run_txt = p_meta.add_run(content)
            run_txt.font.size = Pt(10)
            run_txt.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
            
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # TRANG BÌA (COVER PAGE)
    # -------------------------------------------------------------
    p_hdr1 = doc.add_paragraph()
    p_hdr1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hdr1 = p_hdr1.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\n")
    r_hdr1.font.size = Pt(12)
    r_hdr1.bold = True
    r_hdr2 = p_hdr1.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n")
    r_hdr2.font.size = Pt(13)
    r_hdr2.bold = True
    r_hdr3 = p_hdr1.add_run("KHOA CÔNG NGHỆ THÔNG TIN 1")
    r_hdr3.font.size = Pt(12)
    r_hdr3.bold = True

    for _ in range(3):
        doc.add_paragraph()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BÁO CÁO ASSIGNMENT 04\n")
    r_title.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    r_sub = p_title.add_run("HỌC PHẦN: PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH\n\n")
    r_sub.bold = True
    r_sub.font.size = Pt(14)
    r_sub.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
    
    r_theme = p_title.add_run("ĐỀ TÀI: KHẢO SÁT VÀ ỨNG DỤNG MẠNG NƠ-RON TÍCH CHẬP (CONVOLUTIONAL NEURAL NETWORKS - CNN) TRÊN CÁC DẠNG BIỂU DIỄN DỮ LIỆU ĐA DẠNG: HÌNH ẢNH 2D, DỮ LIỆU BẢNG VÀ VĂN BẢN 1D")
    r_theme.font.size = Pt(12)
    r_theme.bold = True
    r_theme.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    for _ in range(4):
        doc.add_paragraph()

    # Khung thông tin sinh viên
    tbl_info = doc.add_table(rows=5, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_info.autofit = False
    
    info_data = [
        ("Giảng viên hướng dẫn:", "PGS. TS. Trần Đình Quế"),
        ("Nhóm học phần:", "06"),
        ("Họ và tên sinh viên:", "Nguyễn Tuấn Tài"),
        ("Mã sinh viên:", "B23DCCN731"),
        ("Lớp chuyên ngành:", "INT14149_06")
    ]
    
    for idx, (label, val) in enumerate(info_data):
        c0 = tbl_info.cell(idx, 0)
        c1 = tbl_info.cell(idx, 1)
        c0.width = Cm(6.0)
        c1.width = Cm(10.0)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.size = Pt(11.5)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.bold = True if idx in [0, 2] else False
        r1.font.size = Pt(11.5)
        if idx in [0, 2]:
            r1.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    set_table_borders(tbl_info, color="CBD5E0", sz="4", val="single")

    for _ in range(4):
        doc.add_paragraph()

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_loc = p_loc.add_run("HÀ NỘI – 2026")
    r_loc.bold = True
    r_loc.font.size = Pt(12)

    doc.add_page_break()

    # -------------------------------------------------------------
    # MỤC LỤC
    # -------------------------------------------------------------
    add_h1("MỤC LỤC")
    
    toc_items = [
        ("DANH MỤC HÌNH VẼ", "4"),
        ("DANH MỤC CÁC THUẬT NGỮ", "6"),
        ("1. TỔNG QUAN BÀI TOÁN", "7"),
        ("2. YÊU CẦU VÀ ĐỊNH HƯỚNG THỰC HIỆN", "8"),
        ("3. CƠ SỞ LÝ THUYẾT", "9"),
        ("   3.1. DEEP LEARNING DƯỚI GÓC NHÌN HÀM", "9"),
        ("   3.2. CONVOLUTION VÀ WEIGHT SHARING", "10"),
        ("   3.3. RELU, POOLING VÀ KÍCH THƯỚC", "11"),
        ("   3.4. TRAINING VÀ BACKPROPAGATION", "12"),
        ("   3.5. CLASSIFICATION VÀ REGRESSION", "13"),
        ("4. MÔI TRƯỜNG THỰC NGHIỆM VÀ CẤU TRÚC NOTEBOOK", "14"),
        ("5. THỰC NGHIỆM VỚI DATASET ẢNH", "15"),
        ("   5.1. MNIST", "15"),
        ("      5.1.1. CNN FROM SCRATCH BẰNG NUMPY", "16"),
        ("      5.1.2. BASIC CNN BẰNG PYTORCH", "17"),
        ("      5.1.3. ĐÁNH GIÁ BASIC CNN", "18"),
        ("      5.1.4. IMPROVED CNN VÀ BATCH NORMALIZATION", "19"),
        ("      5.1.5. TENSORFLOW/KERAS TRÊN MNIST", "20"),
        ("   5.2. FASHION-MNIST", "21"),
        ("      5.2.1. CHUẨN BỊ DỮ LIỆU", "21"),
        ("      5.2.2. HUẤN LUYỆN VÀ ĐÁNH GIÁ", "22"),
        ("   5.3. CIFAR-10", "23"),
        ("      5.3.1. DỮ LIỆU ẢNH MÀU RGB", "23"),
        ("      5.3.2. HUẤN LUYỆN VÀ ĐÁNH GIÁ", "24"),
        ("   5.4. SO SÁNH BA DATASET ẢNH", "26"),
        ("6. THỰC NGHIỆM VỚI 3 DATASET KHÁC (TABULAR & TEXT 1D)", "28"),
        ("   6.1. DIABETES (PHÂN LOẠI NHỊ PHÂN)", "28"),
        ("      6.1.1. KHÁM PHÁ DỮ LIỆU VÀ CHUẨN HÓA", "28"),
        ("      6.1.2. PYTORCH CONV1D TRÊN DIABETES", "29"),
        ("   6.2. HOUSE PRICE (HỒI QUY ĐỊNH GIÁ BẤT ĐỘNG SẢN)", "30"),
        ("      6.2.1. KHÁM PHÁ VÀ TIỀN XỬ LÝ MÃ HÓA ONE-HOT", "30"),
        ("      6.2.2. PYTORCH CONV1D CHO REGRESSION", "31"),
        ("      6.2.3. ĐÁNH GIÁ VÀ DIỄN GIẢI METRIC (MAE, RMSE, R²)", "32"),
        ("   6.3. COMMENTS (PHÂN LOẠI CẢM XÚC VĂN BẢN)", "33"),
        ("      6.3.1. KHÁM PHÁ DỮ LIỆU", "33"),
        ("      6.3.2. TOKENIZATION VÀ EMBEDDING 64 CHIỀU", "34"),
        ("      6.3.3. PYTORCH TEXT-CNN", "35"),
        ("   6.4. TENSORFLOW – DIABETES", "36"),
        ("   6.5. TENSORFLOW – HOUSE PRICE", "37"),
        ("   6.6. TENSORFLOW – COMMENTS", "38"),
        ("   6.7. SO SÁNH PYTORCH VÀ TENSORFLOW TRÊN BA DATASET 1D", "39"),
        ("7. GIẢI THÍCH CODE NOTEBOOK (WALKTHROUGH KỸ THUẬT)", "41"),
        ("   7.1. IMPORT VÀ DATA PIPELINE", "41"),
        ("   7.2. MODEL DEFINITION VÀ FORWARD PASS", "42"),
        ("   7.3. TRAINING LOOP VÀ TỐI ƯU HÓA BACKPROPAGATION", "43"),
        ("   7.4. EVALUATION VÀ TRÍCH XUẤT CHỈ SỐ", "44"),
        ("8. TỔNG HỢP KẾT QUẢ TOÀN BỘ THỰC NGHIỆM", "45"),
        ("   KẾT QUẢ NHÓM IMAGE CNN", "45"),
        ("   KẾT QUẢ NHÓM TABULAR & TEXT CNN", "45"),
        ("9. PHÂN TÍCH KẾT QUẢ VÀ BÀI HỌC KHOA HỌC", "46"),
        ("10. HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN", "47"),
        ("11. KẾT LUẬN", "48"),
        ("PHỤ LỤC – TÀI NGUYÊN DATASET VÀ MÃ NGUỒN", "49")
    ]
    
    for title, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.line_spacing = 1.15
        r_t = p_t.add_run(title)
        r_t.font.size = Pt(11)
        if not title.startswith("   "):
            r_t.bold = True
            r_t.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        # Dots
        dots_len = max(5, 75 - len(title))
        r_dots = p_t.add_run(" " + "." * dots_len + " ")
        r_dots.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
        
        r_pg = p_t.add_run(page)
        r_pg.bold = True
        r_pg.font.size = Pt(11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # DANH MỤC HÌNH VẼ
    # -------------------------------------------------------------
    add_h1("DANH MỤC HÌNH VẼ")
    
    fig_items = [
        ("Hình 1.1 – Sơ đồ mục tiêu và phạm vi Assignment 04", "7"),
        ("Hình 3.1 – Function composition trong Convolutional Neural Network", "9"),
        ("Hình 3.2 – Minh họa cơ chế kernel trượt và chia sẻ trọng số trên chuỗi X", "10"),
        ("Hình 3.3 – Chu trình huấn luyện và tối ưu hóa tham số (Training workflow)", "12"),
        ("Hình 4.1 – Cấu trúc thư mục tổ chức dự án Assignment 04", "14"),
        ("Hình 5.1 – Mẫu trực quan hóa một số hình ảnh chữ số viết tay tập MNIST", "15"),
        ("Hình 5.2 – Output của convolution/activation/pooling cài đặt bằng NumPy thuần", "16"),
        ("Hình 5.3 – Đường cong huấn luyện Basic CNN trên tập dữ liệu MNIST", "17"),
        ("Hình 5.4 – Code evaluate và Classification Report chi tiết của Basic CNN", "18"),
        ("Hình 5.5 – So sánh tiến trình hội tụ giữa Basic CNN và Improved CNN", "19"),
        ("Hình 5.6 – Kiến trúc và kết quả huấn luyện mô hình TensorFlow CNN trên MNIST", "20"),
        ("Hình 5.7 – Trực quan hóa mẫu đại diện 10 lớp trang phục tập Fashion-MNIST", "21"),
        ("Hình 5.8 – Mẫu hình ảnh màu 3 kênh RGB theo từng lớp tập CIFAR-10", "23"),
        ("Hình 5.9 – Quá trình huấn luyện và lịch sử độ chính xác trên tập CIFAR-10", "24"),
        ("Hình 5.10 – Ma trận nhầm lẫn (Confusion Matrix) 10 lớp kiểm thử CIFAR-10", "25"),
        ("Hình 5.11 – Đường cong huấn luyện mô hình CNN trên tập Fashion-MNIST", "26"),
        ("Hình 5.12 – Biểu đồ so sánh Test Accuracy trên ba bộ dữ liệu ảnh (MNIST, Fashion, CIFAR)", "27"),
        ("Hình 6.1 – Khám phá cấu trúc dữ liệu và pipeline nạp dữ liệu bảng Diabetes", "28"),
        ("Hình 6.2 – Khám phá tập dữ liệu Bất động sản Việt Nam (Vietnam Housing 2024)", "30"),
        ("Hình 6.3 – Tiền xử lý One-Hot Encoding và huấn luyện PyTorch Conv1D giá nhà", "31"),
        ("Hình 6.4 – Biểu đồ phân tán so sánh giá thực tế và giá dự đoán (Actual vs Predicted)", "32"),
        ("Hình 6.5 – Cấu trúc dữ liệu và pipeline phân tích cảm xúc bình luận Comments", "33"),
        ("Hình 6.6 – Sơ đồ luồng xử lý Text: Token IDs → Embedding 64D → Conv1D → GlobalPool", "34"),
        ("Hình 6.7 – Cấu trúc mô hình và kết quả TensorFlow Conv1D trên dữ liệu Diabetes", "36"),
        ("Hình 6.8 – Cấu trúc mô hình và kết quả hồi quy TensorFlow Conv1D trên House Price", "37"),
        ("Hình 6.9 – Cấu trúc mô hình và kết quả phân loại TensorFlow Conv1D trên Comments", "38"),
        ("Hình 6.10 – So sánh Classification Accuracy giữa PyTorch và TensorFlow (Diabetes, Comments)", "39"),
        ("Hình 6.11 – So sánh hệ số xác định R² giữa PyTorch và TensorFlow trên House Price", "40"),
        ("Hình 7.1 – Module Import và Pipeline chuẩn hóa dữ liệu thành Tensor", "41"),
        ("Hình 7.2 – Khai báo kiến trúc lớp mạng Conv2D/Conv1D và hàm truyền thẳng Forward", "42"),
        ("Hình 7.3 – Chu trình lan truyền xuôi và ngược trong vòng lặp huấn luyện PyTorch", "43"),
        ("Hình 7.4 – Hàm đánh giá mô hình và trích xuất chỉ số kiểm thử với torch.no_grad()", "44")
    ]
    
    for title, page in fig_items:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.space_after = Pt(2)
        p_f.paragraph_format.line_spacing = 1.15
        r_f = p_f.add_run(title)
        r_f.font.size = Pt(11)
        
        dots_len = max(5, 80 - len(title))
        r_dots = p_f.add_run(" " + "." * dots_len + " ")
        r_dots.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
        
        r_pg = p_f.add_run(page)
        r_pg.bold = True
        r_pg.font.size = Pt(11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # DANH MỤC CÁC THUẬT NGỮ
    # -------------------------------------------------------------
    add_h1("DANH MỤC CÁC THUẬT NGỮ")
    add_p("Bảng tra cứu các thuật ngữ khoa học cốt lõi được sử dụng xuyên suốt báo cáo thực nghiệm Assignment 04:")
    
    terms = [
        ("CNN", "Convolutional Neural Network – Mạng nơ-ron tích chập chuyên học đặc trưng cục bộ."),
        ("Conv2D", "Tích chập không gian hai chiều, áp dụng cho ma trận điểm ảnh (Height × Width × Channel)."),
        ("Conv1D", "Tích chập chuỗi một chiều, áp dụng cho chuỗi đặc trưng bảng hoặc chuỗi từ vựng."),
        ("Kernel / Filter", "Ma trận trọng số kích thước nhỏ (ví dụ 3×3 hoặc 3) trượt qua dữ liệu để trích xuất pattern."),
        ("Weight Sharing", "Cơ chế chia sẻ trọng số: một kernel duy nhất được tái sử dụng trên toàn bộ không gian đầu vào."),
        ("Locality", "Tính kết nối cục bộ: mỗi nơ-ron chỉ nhận tín hiệu từ một vùng lân cận hữu hạn (Receptive Field)."),
        ("ReLU", "Rectified Linear Unit: hàm kích hoạt phi tuyến f(x) = max(0, x), giải quyết bài toán triệt tiêu gradient."),
        ("Pooling", "Phép giảm chiều không gian biểu diễn (Max-Pooling, Average-Pooling) giúp tăng tính bất biến vị trí."),
        ("Global Pooling", "Phép gom toàn bộ chuỗi hoặc không gian chiều dài thành một vector đơn nhất đại diện."),
        ("Embedding", "Phép ánh xạ chỉ số từ vựng rời rạc thành vector biểu diễn ngữ nghĩa liên tục nhiều chiều."),
        ("Flatten", "Phép biến đổi làm phẳng ma trận đặc trưng đa chiều thành vector 1D trước khi nạp vào lớp Dense."),
        ("Dense / Linear", "Lớp nơ-ron kết nối đầy đủ (Fully Connected Layer) ánh xạ đặc trưng thành dự đoán cuối cùng."),
        ("Batch / Epoch", "Batch: tập con dữ liệu xử lý trong một bước cập nhật; Epoch: một lượt duyệt qua toàn bộ dữ liệu."),
        ("Autograd", "Cơ chế tự động tính toán đạo hàm riêng (Automatic Differentiation) xây dựng đồ thị tính toán."),
        ("Loss Function", "Hàm mục tiêu đo lường sai số giữa giá trị dự đoán của mô hình và nhãn mục tiêu thực tế."),
        ("MAE / RMSE", "Mean Absolute Error & Root Mean Squared Error: các độ đo sai số chuẩn cho bài toán hồi quy."),
        ("R² Score", "Hệ số xác định (Coefficient of Determination), đo lường tỷ lệ phương sai mà mô hình giải thích được.")
    ]
    
    tbl_terms = doc.add_table(rows=len(terms)+1, cols=2)
    tbl_terms.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_terms.autofit = False
    
    # Header
    h0 = tbl_terms.cell(0, 0)
    h1 = tbl_terms.cell(0, 1)
    h0.width = Cm(4.5)
    h1.width = Cm(11.5)
    set_cell_background(h0, "1A365D")
    set_cell_background(h1, "1A365D")
    p = h0.paragraphs[0]; r = p.add_run("Thuật ngữ"); r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p = h1.paragraphs[0]; r = p.add_run("Giải thích ý nghĩa khoa học"); r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    
    for i, (t, d) in enumerate(terms):
        c0 = tbl_terms.cell(i+1, 0)
        c1 = tbl_terms.cell(i+1, 1)
        c0.width = Cm(4.5)
        c1.width = Cm(11.5)
        if (i+1) % 2 == 1:
            set_cell_background(c0, "F7FAFC")
            set_cell_background(c1, "F7FAFC")
        p0 = c0.paragraphs[0]; p0.paragraph_format.space_after = Pt(2); r0 = p0.add_run(t); r0.bold = True
        p1 = c1.paragraphs[0]; p1.paragraph_format.space_after = Pt(2); r1 = p1.add_run(d)
        
    set_table_borders(tbl_terms, color="CBD5E0", sz="4", val="single")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. TỔNG QUAN BÀI TOÁN
    # -------------------------------------------------------------
    add_h1("1. TỔNG QUAN BÀI TOÁN")
    add_p("Assignment 04 trong khuôn khổ học phần Phát triển các Hệ thống Thông minh tập trung khảo sát chuyên sâu về Mạng nơ-ron Tích chập (Convolutional Neural Networks - CNN) và phương pháp tư duy mô hình Deep Learning dưới dạng một phép hợp thành các hàm toán học (Function Composition). Trọng tâm của bài thực nghiệm không đơn thuần dừng lại ở việc đạt được độ chính xác (Accuracy) cao trên một tập dữ liệu chuẩn mực, mà hướng tới mục tiêu khoa học căn bản: chứng minh rằng cùng một triết lý tích chập và chia sẻ trọng số có thể được mở rộng và điều chỉnh linh hoạt cho nhiều hình thái biểu diễn dữ liệu khác nhau trong thực tế.")
    
    add_p("Theo định hướng học thuật được PGS. TS. Trần Đình Quế trực tiếp chỉ dẫn trên bảng lớp và trong tài liệu bài giảng, phạm vi thực nghiệm của Assignment 04 được phân bổ thành hai nhóm bài toán độc lập nhưng thống nhất về mặt nguyên lý:")
    add_bullet("Nhóm dữ liệu Hình ảnh 2D (Image CNN): Khảo sát sự chuyển dịch từ bài toán phân loại chữ số viết tay đơn kênh MNIST (28×28), sang tập trang phục có độ biến thiên họa tiết Fashion-MNIST (28×28), và tập hình ảnh thực tế đa kênh RGB phức tạp CIFAR-10 (32×32×3). Khảo sát được thực hiện qua ba cấp độ mã nguồn: cài đặt toán học thuần túy từ đầu (Scratch with NumPy), xây dựng mạng chuẩn bằng PyTorch (Basic CNN và Improved CNN), và đối sánh bằng TensorFlow/Keras.")
    add_bullet("Nhóm dữ liệu Bảng và Văn bản 1D (Tabular & Text CNN): Khảo sát việc áp dụng phép tích chập một chiều (Conv1D) trên ba tập dữ liệu kế thừa từ các Assignment trước, bao gồm: tập dữ liệu y tế Diabetes (phân loại nhị phân trên 8 đặc trưng lâm sàng), tập dữ liệu bất động sản Vietnam Housing Dataset 2024 (bài toán hồi quy định giá nhà với 133 đặc trưng sau mã hóa One-Hot), và tập dữ liệu văn bản Womens Clothing E-Commerce Reviews (phân loại cảm xúc khách hàng qua tầng Embedding 64 chiều). Toàn bộ ba bài toán 1D này đều được thực nghiệm song song trên cả hai framework hàng đầu là PyTorch và TensorFlow.")

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_1_1_objective_scope.png',
        fig_title='Hình 1.1 – Sơ đồ mục tiêu và phạm vi Assignment 04',
        source='Thiết kế sơ đồ kiến trúc tổng quan bài tập lớn Assignment 04.',
        read_guide='Sơ đồ phân nhánh thể hiện hai nhóm dữ liệu nghiên cứu chính (Image 2D bên trái và Tabular/Text 1D bên phải) cùng 3 cấp độ triển khai công nghệ bên dưới.',
        obs='Toàn bộ hệ thống thực nghiệm bao trùm 6 bộ dữ liệu đa dạng, đi từ toán học giải tích cơ bản đến hai framework học sâu tiêu chuẩn công nghiệp.',
        explanation='Cấu trúc này khẳng định CNN là một phương pháp trích xuất đặc trưng có cấu trúc thay vì chỉ là một công cụ riêng biệt cho bài toán thị giác máy tính.',
        limits='Mô hình tập trung vào việc minh họa nguyên lý và phân tích cơ chế thích ứng của biểu diễn dữ liệu trong giới hạn 5 epochs tiêu chuẩn.'
    )

    add_note_box(
        "Điểm trọng tâm học thuật của bài thực hành là làm sáng tỏ mối quan hệ biện chứng giữa Biểu diễn dữ liệu (Data Representation), Nhiệm vụ bài toán (Task), và Kiến trúc mô hình (Architecture). CNN không phải là một chiếc hộp đen cố định, mà là sự tổ chức có chủ đích của các phép tích chập cục bộ nhằm khai thác tính tương quan không gian hoặc chuỗi thời gian.",
        title="Thông điệp học thuật cốt lõi:"
    )

    # -------------------------------------------------------------
    # 2. YÊU CẦU VÀ ĐỊNH HƯỚNG THỰC HIỆN
    # -------------------------------------------------------------
    add_h1("2. YÊU CẦU VÀ ĐỊNH HƯỚNG THỰC HIỆN")
    add_p("Căn cứ theo yêu cầu ghi nhận trực tiếp từ bảng giảng dạy của Thầy và slide bài giảng cập nhật, quy trình thực hành bắt buộc phải tuân thủ nghiêm ngặt chuỗi tiến trình 5 bước: (1) Nạp dữ liệu chuẩn từ Kaggle/Torchvision; (2) Khám phá và phân tích kiến trúc CNN cơ bản; (3) Tự lập trình mạng CNN từ đầu (From Scratch) bằng thư viện NumPy thuần túy để hiểu rõ cơ chế lan truyền xuôi và ngược; (4) Triển khai mô hình nâng cao và đánh giá toàn diện bằng PyTorch; (5) Cài đặt lại và đối chứng chéo bằng TensorFlow/Keras.")
    
    add_p("Để tạo nên một bức tranh đối sánh toàn diện và phản ánh đúng bản chất kỹ thuật, toàn bộ 6 bộ dữ liệu trong bài thực nghiệm được hệ thống hóa trong Bảng 2.1 dưới đây:")

    # Bảng phân loại dữ liệu
    tbl_data = doc.add_table(rows=7, cols=5)
    tbl_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_data.autofit = False
    
    headers_data = ["Nhóm", "Tập dữ liệu", "Dạng dữ liệu & Kích thước", "Bản chất bài toán", "Kiến trúc mô hình chính"]
    col_widths = [Cm(2.0), Cm(3.2), Cm(4.5), Cm(3.3), Cm(3.0)]
    
    for c_idx, h_text in enumerate(headers_data):
        cell = tbl_data.cell(0, c_idx)
        cell.width = col_widths[c_idx]
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]; r = p.add_run(h_text); r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.size = Pt(10.5)

    data_rows = [
        ("Ảnh 2D", "MNIST", "Ảnh xám 1 kênh (28×28)", "Multi-class Classification", "NumPy / PyTorch / TF Conv2D"),
        ("Ảnh 2D", "Fashion-MNIST", "Ảnh xám 1 kênh (28×28)", "Multi-class Classification", "PyTorch Conv2D (10 lớp thời trang)"),
        ("Ảnh 2D", "CIFAR-10", "Ảnh màu 3 kênh RGB (32×32×3)", "Multi-class Classification", "PyTorch Conv2D (3-channel Conv)"),
        ("1D Tabular", "Diabetes", "Dữ liệu bảng 8 thuộc tính lâm sàng", "Binary Classification", "Conv1D (Channels=1, Length=8)"),
        ("1D Tabular", "House Price 2024", "Dữ liệu bảng 133 đặc trưng One-Hot", "Regression (Định giá nhà)", "Conv1D (Channels=1, Length=133)"),
        ("1D Text", "Comments Reviews", "Chuỗi văn bản (Max 100 tokens)", "Binary Classification", "Embedding(64D) + Conv1D")
    ]
    
    for r_idx, row_vals in enumerate(data_rows):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_data.cell(r_idx+1, c_idx)
            cell.width = col_widths[c_idx]
            if (r_idx+1) % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val); r.font.size = Pt(10)
            if c_idx in [0, 1]:
                r.bold = True

    set_table_borders(tbl_data, color="CBD5E0", sz="4", val="single")

    add_note_box(
        "Việc thực nghiệm đồng thời trên cả dữ liệu không gian 2D, dữ liệu bảng và dữ liệu chuỗi văn bản 1D khẳng định một chân lý thiết kế: CNN không có đặc quyền riêng cho thị giác máy tính. Điều kiện tiên quyết để áp dụng CNN thành công là kỹ sư phải thiết kế một không gian biểu diễn (Representation) chuẩn mực sao cho các phép tích chập có thể học được các mối liên hệ phụ thuộc cục bộ mang ý nghĩa nghiệp vụ.",
        title="Nhận xét định hướng:"
    )

    # -------------------------------------------------------------
    # 3. CƠ SỞ LÝ THUYẾT
    # -------------------------------------------------------------
    add_h1("3. CƠ SỞ LÝ THUYẾT")
    
    add_h2("3.1. DEEP LEARNING DƯỚI GÓC NHÌN HÀM (FUNCTION COMPOSITION)")
    add_p("Trong lý thuyết học sâu hiện đại, một mạng nơ-ron nhiều tầng được mô hình hóa toán học như một chuỗi các phép hợp thành hàm toán học liên tiếp. Giả sử đầu vào là tensor X, qua L tầng biến đổi có tham số, đầu ra dự đoán ŷ được biểu diễn dưới dạng biểu thức giải tích tổng quát:")
    
    p_eq1 = doc.add_paragraph()
    p_eq1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq1 = p_eq1.add_run("ŷ = (f_L ∘ f_{L-1} ∘ … ∘ f_2 ∘ f_1)(X)")
    r_eq1.bold = True
    r_eq1.font.size = Pt(13)
    r_eq1.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    add_p("Trong đó, mỗi hàm thành phần f_l(·) bao gồm một phép biến đổi tuyến tính (hoặc tích chập) có trọng số W_l, cộng thêm độ lệch (bias) b_l, và sau đó được truyền qua một hàm kích hoạt phi tuyến (Non-linear Activation) σ_l. Đối với một nơ-ron tuyến tính cơ bản, z = W^T x + b. Nếu chỉ xếp chồng các phép biến đổi tuyến tính liên tiếp nhau, toàn bộ mạng sâu L tầng sẽ suy biến về một phép biến đổi tuyến tính duy nhất z = W_{eff} x + b_{eff}, làm mất đi hoàn toàn khả năng xấp xỉ các hàm phi tuyến phức tạp. Việc đưa vào các hàm kích hoạt phi tuyến như ReLU (Rectified Linear Unit), được định nghĩa là f(x) = max(0, x), đóng vai trò cốt tử giúp phá vỡ tính tuyến tính, cho phép mạng học được các mặt quyết định phi tuyến phân tách các lớp dữ liệu.")

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_3_1_function_composition.png',
        fig_title='Hình 3.1 – Function composition trong Convolutional Neural Network',
        source='Sơ đồ giải tích Function Composition minh họa luồng biến đổi dữ liệu.',
        read_guide='Theo dõi luồng biến đổi từ trái qua phải: Input X lần lượt đi qua các hàm tích chập cục bộ f1, f2, hàm pooling f3, hàm làm phẳng f4 và phân loại f5.',
        obs='Mỗi khối hàm giữ một vai trò toán học độc lập, từng bước ánh xạ không gian pixel thô thành các biểu diễn đặc trưng trừu tượng trước khi đưa ra nhãn ŷ.',
        explanation='Tính chất hợp thành hàm giúp chia nhỏ bài toán tối ưu hóa phức tạp thành chuỗi các bước cập nhật gradient cục bộ thông qua quy tắc đạo hàm chuỗi (Chain Rule).',
        limits='Mỗi phép biến đổi làm biến đổi phân phối dữ liệu bên trong, đòi hỏi các kỹ thuật điều hòa như Batch Normalization để tránh hiện tượng trôi dạt nội tại.'
    )

    add_h2("3.2. CONVOLUTION VÀ WEIGHT SHARING (CHIA SẺ TRỌNG SỐ)")
    add_p("Phép tích chập (Convolution) trong mạng CNN khác biệt căn bản so với lớp kết nối đầy đủ (Dense Layer) nhờ hai đặc tính cấu trúc vượt trội: Tính kết nối cục bộ (Local Connectivity) và Cơ chế chia sẻ trọng số (Weight Sharing). Thay vì mỗi nơ-ron phải kết nối tới toàn bộ các điểm ảnh đầu vào (dẫn tới sự bùng nổ số lượng tham số khi kích thước ảnh tăng), nơ-ron tích chập chỉ quan sát một vùng không gian nhỏ hữu hạn gọi là trường tiếp nhận (Receptive Field) thông qua một bộ lọc trọng số (Kernel).")
    
    add_p("Một bộ lọc kích thước nhỏ (ví dụ K = 3 đối với chuỗi 1D, hoặc K = 3×3 đối với ảnh 2D) sẽ trượt tuần tự qua toàn bộ các vị trí trên dữ liệu đầu vào. Tại mỗi vị trí dừng, phép nhân vô hướng từng phần tử và tính tổng được thực hiện. Vì cùng một bộ trọng số W duy nhất được tái sử dụng tại mọi vị trí, mạng có khả năng phát hiện cùng một dạng đặc trưng cục bộ (như cạnh, góc, vân, hoặc từ khóa) bất kể đặc trưng đó xuất hiện ở góc trái, góc phải hay chính giữa dữ liệu. Đặc tính toán học này được gọi là Tính tương đương tịnh tiến (Translation Equivariance).")

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_3_2_kernel_sliding.png',
        fig_title='Hình 3.2 – Minh họa cơ chế kernel trượt và chia sẻ trọng số trên chuỗi X',
        source='Mô phỏng phép tích chập 1D trên chuỗi số học [2, 1, 3, 4, 2] với bộ lọc [0.5, -1, 0.5].',
        read_guide='Quan sát ba vị trí trượt tuần tự của kernel 3 phần tử trên chuỗi dữ liệu 5 phần tử để tạo ra chuỗi Feature Map đầu ra gồm 3 giá trị.',
        obs='Tại vị trí 1, giá trị tính toán là 2(0.5) + 1(-1) + 3(0.5) = 1.0. Khi dịch sang vị trí 2 và 3, cùng bộ trọng số tiếp tục được tái sử dụng một cách nhất quán.',
        explanation='Minh họa này chứng minh trực quan cách thức một bộ lọc học sâu phát hiện các biến thiên độ dốc cục bộ mà chỉ tiêu tốn 3 tham số duy nhất.',
        limits='Phép tích chập thuần túy không có padding (valid padding) sẽ làm co cụm kích thước chuỗi từ 5 xuống 3 phần tử sau mỗi tầng biến đổi.'
    )

    add_h2("3.3. RELU, POOLING VÀ CÔNG THỨC QUẢN LÝ KÍCH THƯỚC")
    add_p("Sau mỗi lớp tích chập, dữ liệu được truyền qua hàm kích hoạt ReLU nhằm triệt tiêu các giá trị âm và duy trì tính phi tuyến. Tiếp sau đó, lớp Pooling (phổ biến nhất là Max-Pooling) được áp dụng nhằm giảm kích thước không gian biểu diễn. Phép Max-Pooling kích thước 2×2 với bước nhảy 2 sẽ giữ lại giá trị kích hoạt lớn nhất trong từng cửa sổ 4 điểm ảnh, giúp giảm 75% khối lượng tính toán ở các tầng kế tiếp và mang lại tính bất biến cục bộ đối với các dịch chuyển nhỏ.")
    
    add_p("Công thức toán học kinh điển xác định kích thước đầu ra (Output Dimension - O) của một lớp tích chập phụ thuộc vào kích thước đầu vào (W), kích thước kernel (K), kích thước đệm viền (Padding - P) và bước trượt (Stride - S) được tính như sau:")
    
    p_eq2 = doc.add_paragraph()
    p_eq2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq2 = p_eq2.add_run("O = ⌊ (W - K + 2P) / S ⌋ + 1")
    r_eq2.bold = True
    r_eq2.font.size = Pt(13)
    r_eq2.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    add_h2("3.4. CHU TRÌNH HUẤN LUYỆN VÀ LAN TRUYỀN NGƯỢC (TRAINING WORKFLOW)")
    add_p("Quá trình tối ưu hóa các tham số trọng số trong mạng CNN diễn ra lặp lại theo chu trình khép kín 4 giai đoạn: Lan truyền xuôi (Forward Pass) → Tính toán sai số (Loss Computation) → Lan truyền ngược (Backpropagation) → Cập nhật trọng số (Parameter Update qua Optimizer). Trong môi trường PyTorch, chu trình này được kiểm soát tường minh qua 4 dòng lệnh kinh điển: optimizer.zero_grad(), outputs = model(inputs), loss.backward(), và optimizer.step().")

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_3_3_training_workflow.png',
        fig_title='Hình 3.3 – Chu trình huấn luyện và tối ưu hóa tham số (Training workflow)',
        source='Sơ đồ quy trình huấn luyện khép kín 4 bước được triển khai trong mã nguồn dự án.',
        read_guide='Theo dõi chu trình tròn khép kín: Forward tạo dự đoán, Loss đo sai số, Backward tính gradient, Optimizer cập nhật trọng số và lặp lại.',
        obs='Toàn bộ các tham số của bộ lọc Conv và lớp Dense đều được cập nhật đồng thời dựa trên đạo hàm riêng của hàm mất mát truyền ngược từ ngõ ra.',
        explanation='Thuật toán tối ưu Adam với cơ chế moment bậc 1 và bậc 2 tự động điều chỉnh tốc độ học cho từng tham số, đảm bảo quá trình hội tụ mượt mà.',
        limits='Quá trình huấn luyện trong bài tập lớn được cố định ở 5 epochs nhằm phục vụ mục đích quan sát và so sánh đặc tính hội tụ giữa các kiến trúc.'
    )

    add_h2("3.5. THIẾT KẾ ĐẦU RA CHO PHÂN LOẠI (CLASSIFICATION) VÀ HỒI QUY (REGRESSION)")
    add_p("Một nguyên tắc sống còn trong thiết kế kiến trúc học sâu là hàm kích hoạt tầng cuối cùng và hàm mất mát phải phù hợp tuyệt đối với bản chất của bài toán. Đối với bài toán phân loại nhị phân (Binary Classification như Diabetes và Comments), tầng cuối cùng chỉ cần 1 nơ-ron kết hợp với hàm BCEWithLogitsLoss (tích hợp ngầm Sigmoid để đảm bảo độ ổn định số học). Đối với bài toán phân loại đa lớp (Multi-class như MNIST, CIFAR-10), số nơ-ron ngõ ra bằng số lớp C kết hợp với CrossEntropyLoss. Ngược lại, đối với bài toán hồi quy (Regression như House Price), đầu ra là một giá trị vô hướng liên tục không bị giới hạn trong khoảng [0, 1], do đó tầng cuối cùng là một biến đổi tuyến tính thuần túy (Linear Output) và hàm mất mát bắt buộc phải là sai số toàn phương trung bình (MSE Loss).")

    # -------------------------------------------------------------
    # 4. MÔI TRƯỜNG THỰC NGHIỆM VÀ CẤU TRÚC NOTEBOOK
    # -------------------------------------------------------------
    add_h1("4. MÔI TRƯỜNG THỰC NGHIỆM VÀ CẤU TRÚC NOTEBOOK")
    add_p("Toàn bộ các thực nghiệm tính toán, huấn luyện mô hình và xuất biểu đồ trong báo cáo này được thực hiện trên máy trạm chuyên dụng với môi trường phát triển đồng bộ, đảm bảo tính khả lặp (Reproducibility) cao. Chi tiết phiên bản phần mềm và phần cứng được tóm lược trong Bảng 4.1:")

    tbl_env = doc.add_table(rows=8, cols=3)
    tbl_env.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_env.autofit = False
    
    headers_env = ["Thành phần môi trường", "Phiên bản cài đặt", "Vai trò và chức năng chuyên trách"]
    env_widths = [Cm(4.0), Cm(3.5), Cm(8.5)]
    for c_idx, h_text in enumerate(headers_env):
        cell = tbl_env.cell(0, c_idx)
        cell.width = env_widths[c_idx]
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]; r = p.add_run(h_text); r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.size = Pt(10.5)

    env_rows = [
        ("Hệ điều hành", "Windows 11 Professional (x64)", "Nền tảng thực thi hệ thống và tương tác PowerShell"),
        ("Ngôn ngữ thực thi", "Python 3.13.0 (Conda Environment)", "Môi trường thông dịch mã nguồn khoa học dữ liệu"),
        ("PyTorch & Torchvision", "PyTorch 2.14.0 + Torchvision 0.29.0", "Xây dựng CNN hướng động lực, tính Autograd và Tensor"),
        ("TensorFlow / Keras", "TensorFlow 2.19.0", "Triển khai mạng tích chập hướng tuần tự (Sequential API)"),
        ("NumPy & SciPy", "NumPy 2.1.3", "Thực hiện đại số tuyến tính và cài đặt CNN From Scratch"),
        ("Pandas & Scikit-learn", "Pandas 2.2.3 & Scikit-learn 1.6.0", "Tiền xử lý bảng One-Hot, chia tập Train/Test, tính Metrics"),
        ("Trực quan hóa", "Matplotlib 3.10.0 & Seaborn 0.13.2", "Vẽ biểu đồ huấn luyện, ma trận nhầm lẫn, biểu đồ phân tán")
    ]
    
    for r_idx, row_vals in enumerate(env_rows):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_env.cell(r_idx+1, c_idx)
            cell.width = env_widths[c_idx]
            if (r_idx+1) % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val); r.font.size = Pt(10)
            if c_idx == 0:
                r.bold = True

    set_table_borders(tbl_env, color="CBD5E0", sz="4", val="single")

    add_p("Theo đúng chỉ đạo của Giảng viên về việc gom toàn bộ mã nguồn phục vụ thuyết trình vào các thư mục độc lập, hệ thống được cấu trúc thành 2 notebook hạt nhân nằm trong thư mục notebooks/ và dữ liệu nằm trong thư mục data/:")
    add_bullet("notebooks/image_cnn_a04.ipynb: Chuyên trách toàn bộ các nội dung liên quan đến thị giác máy tính: nạp 3 bộ dữ liệu ảnh, cài đặt Scratch CNN bằng NumPy, xây dựng Basic CNN và Improved CNN (+BatchNorm) bằng PyTorch, triển khai đối sánh bằng TensorFlow, và xuất ma trận nhầm lẫn cùng biểu đồ so sánh.")
    add_bullet("notebooks/tabular_text_cnn_a04.ipynb: Chuyên trách toàn bộ các nội dung xử lý dữ liệu 1 chiều: tiền xử lý One-Hot 133 chiều cho House Price, chuẩn hóa lâm sàng Diabetes, nhúng từ vựng Embedding 64D cho Comments, huấn luyện Conv1D trên cả PyTorch và TensorFlow, xuất biểu đồ Actual vs Predicted và đối sánh hiệu năng song song.")

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_4_1_folder_structure.png',
        fig_title='Hình 4.1 – Cấu trúc thư mục tổ chức dự án Assignment 04',
        source='Sơ đồ cây cấu trúc thư mục thực tế trên không gian làm việc dự án.',
        read_guide='Sơ đồ phân định rõ ràng giữa thư mục chứa dữ liệu tập trung (data/) và thư mục chứa mã nguồn Jupyter Notebook (notebooks/).',
        obs='Các notebook được đặt tên theo đúng quy ước học phần, sẵn sàng phục vụ trình chiếu trực tiếp trên lớp học theo yêu cầu của Giảng viên.',
        explanation='Cấu trúc module hóa giúp phân tách độc lập giữa tài nguyên dữ liệu thô, mã nguồn huấn luyện và kết quả ảnh chụp biểu đồ phục vụ báo cáo.',
        limits='Đường dẫn nạp dữ liệu trong notebook sử dụng cú pháp tương đối, yêu cầu thư mục làm việc gốc được giữ nguyên khi kích hoạt Anaconda Jupyter.'
    )

    # -------------------------------------------------------------
    # 5. THỰC NGHIỆM VỚI DATASET ẢNH
    # -------------------------------------------------------------
    add_h1("5. THỰC NGHIỆM VỚI DATASET ẢNH")
    
    add_h2("5.1. BỘ DỮ LIỆU CHỮ SỐ VIẾT TAY MNIST")
    add_p("MNIST (Modified National Institute of Standards and Technology) là tập dữ liệu mẫu mực kinh điển trong thị giác máy tính, bao gồm 70,000 ảnh xám kích thước 28×28 điểm ảnh ghi nhận các chữ số viết tay từ 0 đến 9 (60,000 ảnh huấn luyện và 10,000 ảnh kiểm thử). Trước khi đưa vào mô hình, các điểm ảnh có giá trị nguyên từ [0, 255] được chuẩn hóa về phân phối chuẩn chuẩn tắc với giá trị trung bình mean = 0.1307 và độ lệch chuẩn std = 0.3081.")

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_5_1_mnist_samples.png',
        fig_title='Hình 5.1 – Mẫu trực quan hóa một số hình ảnh chữ số viết tay tập MNIST',
        source='Notebook image_cnn_a04.ipynb, Cell 1 - Trực quan hóa dữ liệu kiểm tra.',
        read_guide='Lưới 2×5 hiển thị 10 mẫu ảnh chữ số ngẫu nhiên kèm nhãn thực tế bên trên.',
        obs='Các nét chữ số có độ tương phản rất cao, nét vẽ màu trắng nổi bật rõ nét trên nền đen thuần túy, kích thước chữ số chiếm trọn trung tâm khung ảnh 28×28.',
        explanation='Tính phân tách cao và mức độ nhiễu thấp biến MNIST thành môi trường lý tưởng để kiểm chứng tính đúng đắn của các thuật toán tích chập cơ bản.',
        limits='Độ phức tạp hình học đơn giản khiến MNIST không thể phản ánh đầy đủ thách thức phân loại của các hình ảnh tự nhiên trong thế giới thực.'
    )

    add_h3("5.1.1. CNN From Scratch bằng thư viện NumPy thuần túy")
    add_p("Nhằm thấu hiểu sâu sắc bản chất cơ học của phép tích chập mà không phụ thuộc vào các công cụ tự động vi phân cấp cao, một mô hình tích chập tối giản đã được lập trình thủ công hoàn toàn từ đầu bằng thư viện NumPy (SimpleCNNScratch). Mô hình bao gồm một tầng Conv2D (4 bộ lọc kích thước 3×3), hàm kích hoạt ReLU, tầng Max-Pooling kích thước 2×2, và tầng Dense phân loại 10 lớp sử dụng hàm kích hoạt Softmax.")

    add_image_with_caption(
        img_path='ass4_experiments/plots/01_mnist_numpy_scratch.png',
        fig_title='Hình 5.2 – Output của convolution/activation/pooling cài đặt bằng NumPy thuần',
        source='Notebook image_cnn_a04.ipynb, Cell 2 - NumPy CNN From Scratch.',
        read_guide='Hình ảnh trực quan hóa các giai đoạn biến đổi: Ảnh gốc 28×28 → 4 Feature Maps sau tích chập → Sau kích hoạt ReLU → Sau khi giảm mẫu Max-Pooling.',
        obs='Các bộ lọc 3×3 tự tạo đã trích xuất thành công các đường nét biên cạnh dọc và ngang của chữ số; sau lớp Max-Pooling kích thước ảnh giảm chính xác về 13×13.',
        explanation='Thực nghiệm lan truyền ngược thủ công trên tập mẫu nhỏ (1,000 mẫu) đã đạt độ chính xác kiểm thử Test Accuracy = 82.40% sau 3 epochs.',
        limits='Tốc độ tính toán của vòng lặp Python thuần rất chậm so với các phép toán Tensor được tối ưu hóa bằng ngôn ngữ C++/CUDA trong PyTorch.'
    )

    add_h3("5.1.2. Xây dựng mô hình Basic CNN bằng PyTorch")
    add_p("Chuyển sang nền tảng học sâu chuyên nghiệp, mô hình BasicCNN được thiết kế theo kiến trúc LeNet cải tiến gồm 2 khối tích chập: Conv2D(1 → 16, kernel=3, pad=1) → ReLU → MaxPool2D(2, 2) → Conv2D(16 → 32, kernel=3, pad=1) → ReLU → MaxPool2D(2, 2) → Flatten → Linear(32×7×7 = 1568 → 64) → ReLU → Dropout(0.25) → Linear(64 → 10). Tổng số lượng tham số học được của mô hình là 20,490 tham số.")

    add_image_with_caption(
        img_path='ass4_experiments/plots/02_mnist_basic_training_curve.png',
        fig_title='Hình 5.3 – Đường cong huấn luyện Basic CNN trên tập dữ liệu MNIST',
        source='Notebook image_cnn_a04.ipynb, Cell 3 - Huấn luyện mô hình PyTorch BasicCNN.',
        read_guide='Hai đồ thị song song biểu diễn sự biến thiên của hàm mất mát (Training/Validation Loss bên trái) và độ chính xác (Accuracy bên phải) qua 5 epochs.',
        obs='Hàm mất mát giảm dốc đứng từ 0.2314 ở Epoch 1 xuống 0.0335 ở Epoch 5; độ chính xác trên tập kiểm định tăng nhanh từ 97.82% lên 98.50%.',
        explanation='Tốc độ hội tụ cực nhanh chứng minh kiến trúc 2 tầng tích chập có khả năng khớp hoàn hảo với các đặc trưng không gian của chữ số viết tay.',
        limits='Đồ thị validation loss bắt đầu có dấu hiệu chững lại ở Epoch 4-5 cho thấy mô hình đã tiến gần tới giới hạn dung lượng biểu diễn của tập dữ liệu.'
    )

    add_h3("5.1.3. Đánh giá chi tiết mô hình Basic CNN")
    add_p("Trên toàn bộ 10,000 ảnh của tập kiểm thử độc lập, mô hình PyTorch BasicCNN đạt độ chính xác kiểm thử tổng thể Test Accuracy = 98.50% với tổng thời gian huấn luyện 5 epochs là 53.52 giây (trung bình ~10.7 giây/epoch). Bảng báo cáo phân loại (Classification Report) chi tiết cho từng chữ số được ghi nhận trong Hình 5.4:")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_5_4_mnist_basic_eval.png',
        fig_title='Hình 5.4 – Code evaluate và Classification Report chi tiết của Basic CNN',
        source='Notebook image_cnn_a04.ipynb, Cell 4 - Trích xuất báo cáo phân loại kiểm thử.',
        read_guide='Bảng hiển thị các chỉ số Precision, Recall, F1-Score và số lượng mẫu hỗ trợ (Support) cho từng chữ số từ lớp 0 đến lớp 9.',
        obs='Chữ số 1 đạt F1-score cao nhất (0.9947) nhờ cấu trúc nét thẳng đơn giản; chữ số 8 và chữ số 9 đạt F1-score thấp hơn (~0.9755) do dễ nhầm lẫn nét cong.',
        explanation='Chỉ số trung bình vĩ mô (Macro Average F1) đạt 0.9849 khẳng định mô hình dự đoán đồng đều và không bị thiên lệch về bất kỳ chữ số cụ thể nào.',
        limits='Báo cáo phân loại chỉ phản ánh tỷ lệ nhãn đúng, chưa chỉ ra được cụ thể cặp chữ số nào thường xuyên gây nhầm lẫn cho mạng.'
    )

    add_h3("5.1.4. Cải tiến mô hình với tầng Chuẩn hóa theo lô (Improved CNN & Batch Normalization)")
    add_p("Nhằm khảo sát tác động của việc cải tiến kiến trúc theo yêu cầu trên bảng của Giảng viên, mô hình ImprovedCNN được xây dựng bằng cách chèn thêm các tầng Chuẩn hóa theo lô (BatchNorm2d) ngay sau mỗi lớp tích chập Conv2D. Tầng BatchNorm2d giúp chuẩn hóa phân phối giá trị kích hoạt của từng mini-batch, duy trì giá trị trung bình bằng 0 và phương sai bằng 1 thông qua hai tham số học được γ và β. Số lượng tham số của mô hình tăng nhẹ từ 20,490 lên 20,586 tham số (+96 tham số chuẩn hóa).")

    add_image_with_caption(
        img_path='ass4_experiments/plots/03_mnist_basic_vs_improved.png',
        fig_title='Hình 5.5 – So sánh tiến trình hội tụ giữa Basic CNN và Improved CNN',
        source='Notebook image_cnn_a04.ipynb, Cell 5 - So sánh hiệu năng đối chuẩn.',
        read_guide='Biểu đồ đường đối chiếu trực tiếp quỹ đạo Validation Accuracy của hai mô hình qua từng epoch huấn luyện.',
        obs='Improved CNN đạt độ chính xác vượt trội ngay từ Epoch 1 (98.28% so với 97.82% của Basic CNN) và duy trì ưu thế ổn định, kết thúc ở mức 98.67% (+0.17%).',
        explanation='Batch Normalization triệt tiêu hiện tượng trôi dạt hiệp biến nội tại (Internal Covariate Shift), giúp gradient lan truyền mượt mà và cho phép hội tụ nhanh hơn.',
        limits='Thời gian huấn luyện của Improved CNN tăng lên 69.75 giây (+30.3%) do phát sinh chi phí tính toán thống kê mean/variance trên từng mini-batch.'
    )

    add_h3("5.1.5. Triển khai mô hình trên nền tảng TensorFlow/Keras")
    add_p("Để hoàn thành yêu cầu so sánh framework, kiến trúc CNN tương tự đã được cài đặt bằng thư viện TensorFlow 2.19 thông qua API tuần tự tf.keras.models.Sequential. Mô hình bao gồm Conv2D(16) → MaxPool2D → Conv2D(32) → MaxPool2D → Flatten → Dense(64) → Dense(10, softmax). Tổng số tham số cấu hình này là 56,714 tham số.")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_5_6_mnist_tf_summary.png',
        fig_title='Hình 5.6 – Kiến trúc và kết quả huấn luyện mô hình TensorFlow CNN trên MNIST',
        source='Notebook image_cnn_a04.ipynb, Cell 6 - Khai báo TensorFlow Keras Sequential.',
        read_guide='Ảnh chụp tế bào JupyterLab thể hiện chi tiết bảng model.summary(), kích thước tensor các tầng và kết quả lệnh model.fit().',
        obs='Mô hình đạt Test Accuracy = 98.37% sau 5 epochs huấn luyện, bám sát độ chính xác của phiên bản PyTorch (98.50%).',
        explanation='TensorFlow Keras cung cấp giao diện lập trình cấp cao, tối ưu hóa sẵn luồng dữ liệu tự động, giúp rút gọn đáng kể số dòng code triển khai.',
        limits='Khả năng can thiệp sâu vào từng bước tính toán gradient cục bộ trong TensorFlow Keras Sequential bị hạn chế hơn so với PyTorch Autograd.'
    )

    add_h2("5.2. BỘ DỮ LIỆU THỜI TRANG FASHION-MNIST")
    add_p("Fashion-MNIST được thiết kế bởi viện nghiên cứu Zalando như một phương án thay thế trực tiếp cho MNIST nhưng mang độ phức tạp thị giác cao hơn rất nhiều. Tập dữ liệu có cùng kích thước 70,000 ảnh xám 28×28 và 10 lớp, nhưng thay vì các chữ số đơn giản, đối tượng phân loại là 10 mặt hàng thời trang: Áo thun (T-shirt), Quần dài (Trouser), Áo len (Pullover), Váy (Dress), Áo khoác (Coat), Dép xăng đan (Sandal), Áo sơ mi (Shirt), Giày thể thao (Sneaker), Túi xách (Bag), và Bốt (Ankle boot).")

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_5_7_fashion_mnist_samples.png',
        fig_title='Hình 5.7 – Trực quan hóa mẫu đại diện 10 lớp trang phục tập Fashion-MNIST',
        source='Notebook image_cnn_a04.ipynb, Cell 7 - Phân tích đặc trưng tập Fashion-MNIST.',
        read_guide='Lưới ảnh hiển thị trực quan đại diện cho từng lớp thời trang cùng tên gọi tương ứng.',
        obs='Các sản phẩm thời trang sở hữu nhiều đường viền phức tạp, nếp gấp vải, độ dày mỏng và hoa văn bên trong thay vì chỉ là các nét vẽ nhị phân đơn giản.',
        explanation='Sự tương đồng hình khối giữa các lớp trang phục (ví dụ giữa Áo thun, Áo len, Áo sơ mi và Áo khoác) tạo nên thách thức phân loại lớn cho mạng CNN.',
        limits='Độ phân giải 28×28 ở định dạng ảnh xám đơn sắc làm mất đi các chi tiết kết cấu sợi vải vi mô quan trọng của trang phục.'
    )

    add_p("Mô hình BasicCNN được huấn luyện trên Fashion-MNIST với cùng cấu hình siêu tham số (5 epochs, Adam, lr=0.001, batch_size=64). Kết quả ghi nhận độ chính xác kiểm thử đạt Test Accuracy = 90.13% với tổng thời gian huấn luyện là 53.91 giây. Đường cong học tập được thể hiện trong Hình 5.11:")

    add_image_with_caption(
        img_path='ass4_experiments/plots/05_fashion_mnist_training_curve.png',
        fig_title='Hình 5.11 – Đường cong huấn luyện mô hình CNN trên tập Fashion-MNIST',
        source='Notebook image_cnn_a04.ipynb, Cell 7 - Lịch sử huấn luyện Fashion-MNIST.',
        read_guide='Đồ thị biểu diễn Training Loss/Validation Loss và Training Accuracy/Validation Accuracy qua 5 epochs.',
        obs='Độ chính xác tăng trưởng đều đặn từ 84.15% ở Epoch 1 lên 90.13% ở Epoch 5; khoảng cách giữa train và validation loss được duy trì ở mức an toàn.',
        explanation='Mức sụt giảm độ chính xác từ 98.50% (trên MNIST) xuống 90.13% (trên Fashion-MNIST) phản ánh chính xác sự gia tăng độ phức tạp của không gian biểu diễn.',
        limits='Để vượt ngưỡng 92% trên Fashion-MNIST, mạng đòi hỏi phải bổ sung kỹ thuật Data Augmentation (xoay, lật ảnh) và tăng chiều sâu các tầng tích chập.'
    )

    add_h2("5.3. BỘ DỮ LIỆU HÌNH ẢNH MÀU THỰC TẾ CIFAR-10")
    add_p("CIFAR-10 là bước nhảy vọt về độ khó trong nhóm thực nghiệm hình ảnh. Tập dữ liệu bao gồm 60,000 ảnh màu tự nhiên kích thước 32×32 điểm ảnh thuộc 10 lớp vật thể trong đời sống: Máy bay (Airplane), Ô tô (Automobile), Chim (Bird), Mèo (Cat), Hươu (Deer), Chó (Dog), Ếch (Frog), Ngựa (Horse), Tàu thủy (Ship), và Xe tải (Truck). Điểm khác biệt mấu chốt so với hai tập trước là mỗi điểm ảnh sở hữu đủ 3 kênh màu đỏ - lục - lam (RGB: Red, Green, Blue), do đó tensor đầu vào có kích thước (Batch_Size, Channels=3, Height=32, Width=32).")

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_5_8_cifar10_samples.png',
        fig_title='Hình 5.8 – Mẫu hình ảnh màu 3 kênh RGB theo từng lớp tập CIFAR-10',
        source='Notebook image_cnn_a04.ipynb, Cell 8 - Khám phá dữ liệu CIFAR-10.',
        read_guide='Hiển thị 10 mẫu ảnh màu đặc trưng đại diện cho 10 lớp phương tiện và động vật trong CIFAR-10.',
        obs='Hình ảnh chụp trong môi trường tự nhiên chứa bối cảnh nền cực kỳ đa dạng (bầu trời, mặt nước, bãi cỏ, con đường) với nhiều góc chụp và độ sáng khác nhau.',
        explanation='Thông tin 3 kênh màu RGB mang lại sự phong phú về sắc thái nhưng đồng thời gia tăng đáng kể kích thước không gian tìm kiếm tham số tối ưu của mô hình.',
        limits='Kích thước 32×32 điểm ảnh khá mờ khi phóng to, gây khó khăn cho việc nhận diện ranh giới rõ ràng giữa các loài thú như Chó và Mèo.'
    )

    add_p("Mô hình BasicCNN được điều chỉnh lớp tích chập đầu tiên để tiếp nhận 3 kênh màu đầu vào: nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1). Sau 5 epochs huấn luyện, mô hình đạt Test Accuracy = 64.77% với tổng thời gian huấn luyện là 185.40 giây. Diễn biến huấn luyện và ma trận nhầm lẫn chi tiết được trình bày trong Hình 5.9 và Hình 5.10:")

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_5_9_cifar10_training_history.png',
        fig_title='Hình 5.9 – Quá trình huấn luyện và lịch sử độ chính xác trên tập CIFAR-10',
        source='Notebook image_cnn_a04.ipynb, Cell 8 - Huấn luyện mô hình CIFAR-10.',
        read_guide='Đồ thị biểu diễn tiến trình hội tụ của Loss và Accuracy qua 5 epochs.',
        obs='Độ chính xác tăng từ 48.21% (Epoch 1) lên 64.77% (Epoch 5); tuy nhiên tốc độ hội tụ chậm hơn rõ rệt so với MNIST và Fashion-MNIST.',
        explanation='Không gian biểu diễn của ảnh màu 3 kênh đòi hỏi nhiều tài nguyên tính toán hơn để học được các đặc trưng bất biến của vật thể trong bối cảnh nền tự nhiên.',
        limits='Ngân sách 5 epochs là chưa đủ để mạng CNN cơ bản hội tụ hoàn toàn trên CIFAR-10; mô hình cần từ 20 đến 50 epochs để đạt trạng thái tối ưu.'
    )

    add_image_with_caption(
        img_path='ass4_experiments/plots/08_cifar10_confusion_matrix.png',
        fig_title='Hình 5.10 – Ma trận nhầm lẫn (Confusion Matrix) 10 lớp kiểm thử CIFAR-10',
        source='Notebook image_cnn_a04.ipynb, Cell 8 - Phân tích sai số dự đoán ma trận nhầm lẫn.',
        read_guide='Ma trận 10×10 với trục tung là nhãn thực tế, trục hoành là nhãn dự đoán; đường chéo chính thể hiện số lượng mẫu dự đoán chính xác.',
        obs='Độ chính xác rất cao ở các lớp phương tiện giao thông (Automobile: 785/1000 đúng, Ship: 762/1000 đúng); nhầm lẫn xuất hiện dày đặc giữa Cat và Dog (184 mẫu nhầm).',
        explanation='Các loài động vật bốn chân có hình thái giải phẫu, tư thế và kết cấu lông tương tự nhau, đòi hỏi mạng phải có trường tiếp nhận sâu hơn để phân biệt.',
        limits='Mô hình chưa phân biệt triệt để được sự khác biệt tinh tế giữa các loài sinh vật khi kích thước ảnh bị thu nhỏ về 32×32 điểm ảnh.'
    )

    add_h2("5.4. SO SÁNH TỔNG HỢP BA BỘ DỮ LIỆU ẢNH (MNIST vs FASHION vs CIFAR)")
    add_p("Để tổng kết nhóm thực nghiệm hình ảnh, Bảng 5.1 và biểu đồ Hình 5.12 đối chuẩn toàn diện ba bộ dữ liệu dựa trên các tiêu chí khoa học:")

    tbl_img_comp = doc.add_table(rows=4, cols=6)
    tbl_img_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_img_comp.autofit = False
    
    headers_img = ["Tập dữ liệu", "Kích thước & Kênh", "Số tham số", "Test Accuracy", "Thời gian huấn luyện", "Đánh giá độ phức tạp"]
    w_img = [Cm(2.8), Cm(3.2), Cm(2.2), Cm(2.5), Cm(2.5), Cm(3.2)]
    for c_idx, h_text in enumerate(headers_img):
        cell = tbl_img_comp.cell(0, c_idx)
        cell.width = w_img[c_idx]
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]; r = p.add_run(h_text); r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.size = Pt(10)

    rows_img = [
        ("MNIST", "1×28×28 (Ảnh xám)", "20,490", "0.9850 (98.50%)", "53.52 giây", "Thấp (Nét vẽ nhị phân rõ ràng)"),
        ("Fashion-MNIST", "1×28×28 (Ảnh xám)", "20,490", "0.9013 (90.13%)", "53.91 giây", "Trung bình (Đa dạng hoa văn vải)"),
        ("CIFAR-10", "3×32×32 (Ảnh màu RGB)", "20,778", "0.6477 (64.77%)", "185.40 giây", "Cao (Nhiễu bối cảnh đời thực)")
    ]
    for r_idx, row_vals in enumerate(rows_img):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_img_comp.cell(r_idx+1, c_idx)
            cell.width = w_img[c_idx]
            if (r_idx+1) % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val); r.font.size = Pt(9.5)
            if c_idx in [0, 3]:
                r.bold = True

    set_table_borders(tbl_img_comp, color="CBD5E0", sz="4", val="single")

    add_image_with_caption(
        img_path='ass4_experiments/plots/09_image_datasets_comparison.png',
        fig_title='Hình 5.12 – Biểu đồ so sánh Test Accuracy trên ba bộ dữ liệu ảnh (MNIST, Fashion, CIFAR)',
        source='Notebook image_cnn_a04.ipynb, Cell 9 - Đối chuẩn hiệu năng đa dữ liệu ảnh.',
        read_guide='Biểu đồ cột so sánh trực tiếp độ chính xác kiểm thử cuối cùng của cùng một họ kiến trúc CNN trên 3 bộ dữ liệu.',
        obs='Độ chính xác suy giảm có quy luật từ 98.50% (MNIST) → 90.13% (Fashion) → 64.77% (CIFAR-10).',
        explanation='Biểu đồ chứng minh rằng độ chính xác của mạng CNN không chỉ phụ thuộc vào số tham số mô hình mà bị chi phối mạnh mẽ bởi mật độ thông tin và độ phức tạp biểu diễn nội tại của dữ liệu.',
        limits='So sánh được thực hiện trên cùng một ngân sách huấn luyện cố định 5 epochs để đảm bảo tính công bằng học thuật.'
    )

    # -------------------------------------------------------------
    # 6. THỰC NGHIỆM VỚI 3 DATASET KHÁC (TABULAR & TEXT 1D)
    # -------------------------------------------------------------
    add_h1("6. THỰC NGHIỆM VỚI 3 DATASET KHÁC (TABULAR & TEXT 1D)")
    
    add_h2("6.1. BỘ DỮ LIỆU TIỂU ĐƯỜNG DIABETES (PHÂN LOẠI NHỊ PHÂN)")
    add_p("Tập dữ liệu Pima Indians Diabetes bao gồm 768 bản ghi y tế của các bệnh nhân nữ nhằm dự đoán nguy cơ mắc bệnh tiểu đường (Outcome: 0 hoặc 1). Mỗi bản ghi bao gồm 8 đặc trưng lâm sàng: Số lần mang thai (Pregnancies), Nồng độ đường huyết (Glucose), Huyết áp (BloodPressure), Độ dày nếp gấp da (SkinThickness), Nồng độ Insulin, Chỉ số khối cơ thể (BMI), Chức năng phả hệ tiểu đường (DiabetesPedigreeFunction), và Tuổi tác (Age).")
    
    add_p("Để đưa dữ liệu bảng vào mạng tích chập, dữ liệu được chuẩn hóa bằng StandardScaler và biến đổi hình dạng (Reshape) thành Tensor 3 chiều: (Batch_Size, Channels=1, Length=8). Ở đây, số kênh được cố định bằng 1 và chiều dài chuỗi đặc trưng là 8. Kiến trúc PyTorch Conv1D được cấu hình với kernel kích thước 2 và stride 1, trích xuất các mối liên hệ chéo giữa các cặp chỉ số lâm sàng nằm kề nhau.")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_6_1_diabetes_pipeline.png',
        fig_title='Hình 6.1 – Khám phá cấu trúc dữ liệu và pipeline nạp dữ liệu bảng Diabetes',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 1 - Pipeline dữ liệu bảng Diabetes.',
        read_guide='Hiển thị cấu trúc bảng dữ liệu gốc df.head(3), kích thước tensor nạp vào Conv1D và lịch sử huấn luyện 5 epochs.',
        obs='Dữ liệu 8 chiều được chuyển đổi thành công sang dạng chuỗi 1D torch.Size([614, 1, 8]); mô hình PyTorch đạt Test Accuracy = 69.83% và F1-Score = 0.6738 sau 5 epochs.',
        explanation='Phép tích chập 1D quét qua các đặc trưng lâm sàng lân cận, chứng minh cơ chế tích chập hoàn toàn có thể áp dụng cho dữ liệu dạng bảng.',
        limits='Thứ tự các cột trong bảng mang tính nhân tạo, không có mối quan hệ phụ thuộc không gian tự nhiên liên tục như các điểm ảnh.'
    )

    add_h2("6.2. BỘ DỮ LIỆU BẤT ĐỘNG SẢN VIỆT NAM 2024 (HỒI QUY ĐỊNH GIÁ NHÀ)")
    add_p("Tập dữ liệu Vietnam Housing Dataset 2024 ghi nhận thông tin 10,000 bất động sản trên toàn quốc nhằm phục vụ bài toán hồi quy định giá nhà (Price, tính bằng đơn vị tỷ VNĐ). Dữ liệu chứa cả các biến số học (Diện tích Area, Số phòng ngủ Bedrooms, Số phòng vệ sinh Bathrooms, Số tầng Floors) và các biến hạng mục phức tạp (Địa chỉ Address/Quận huyện, Hướng nhà Direction, Tình trạng pháp lý Legal_Status, Nội thất Furniture).")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_6_2_house_price_head.png',
        fig_title='Hình 6.2 – Khám phá tập dữ liệu Bất động sản Việt Nam (Vietnam Housing 2024)',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 2 - Khám phá dữ liệu nhà ở.',
        read_guide='Ảnh chụp tế bào thể hiện kích thước DataFrame (10,000 dòng, 15 cột) và mẫu dữ liệu các cột thuộc tính cơ bản.',
        obs='Các chuỗi địa chỉ quận huyện chứa nhiều thông tin không gian địa lý quan trọng; mức giá nhà phân bố rộng từ vài tỷ đến hàng chục tỷ đồng.',
        explanation='Để mô hình học sâu có thể xử lý được, toàn bộ các thuộc tính hạng mục bắt buộc phải được mã hóa thành các biểu diễn số học thuần túy.',
        limits='Tập dữ liệu gốc chứa một số bản ghi khuyết thiếu (missing values) ở cột hướng nhà và nội thất, đòi hỏi bước tiền xử lý xử lý gán giá trị hợp lý.'
    )

    add_p("Quy trình tiền xử lý sử dụng OneHotEncoder cho toàn bộ các thuộc tính hạng mục, mở rộng không gian đặc trưng từ 15 biến ban đầu lên thành 133 đặc trưng số học. Tensor đầu vào được định hình lại thành (Batch_Size, Channels=1, Length=133) và đưa vào mạng PyTorch Conv1D(1 → 32, kernel=3) → MaxPool1D(2) → Flatten → Linear(2080 → 64) → Linear(64 → 1).")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_6_3_house_price_prep.png',
        fig_title='Hình 6.3 – Tiền xử lý One-Hot Encoding và huấn luyện PyTorch Conv1D giá nhà',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 3 - Tiền xử lý One-Hot và Huấn luyện Conv1D.',
        read_guide='Hiển thị kích thước mảng sau mã hóa (8,000 mẫu train, 133 đặc trưng) và sự suy giảm của hàm tổn thất MSE qua 5 epochs.',
        obs='Hàm mất mát MSE giảm mạnh từ 8.4215 ở Epoch 1 xuống 3.6120 ở Epoch 5; mô hình thích nghi nhanh với không gian đặc trưng thưa (sparse features).',
        explanation='Tầng Conv1D kernel kích thước 3 trích xuất các tổ hợp đặc trưng cục bộ giữa vị trí địa lý và các thông số tiện ích căn nhà.',
        limits='Không gian 133 chiều có độ thưa rất cao sau khi One-Hot, phần lớn các giá trị trong tensor là số 0.'
    )

    add_p("Mô hình hồi quy được đánh giá trên 2,000 mẫu kiểm thử độc lập dựa trên ba chỉ số chuẩn tắc: Sai số tuyệt đối trung bình (MAE) = 1.6100 tỷ VNĐ, Sai số căn bậc hai trung bình (RMSE) = 1.9684 tỷ VNĐ, và Hệ số xác định (R²) = 0.1905. Biểu đồ phân tán so sánh giá trị thực tế và giá trị dự đoán được minh họa trong Hình 6.4:")

    add_image_with_caption(
        img_path='ass4_experiments/plots/12_actual_vs_predicted_house_price.png',
        fig_title='Hình 6.4 – Biểu đồ phân tán so sánh giá thực tế và giá dự đoán (Actual vs Predicted)',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 4 - Trực quan hóa kết quả hồi quy giá nhà.',
        read_guide='Mỗi điểm chấm đại diện cho một căn nhà; trục hoành là giá thực tế, trục tung là giá mô hình dự đoán; đường nét đứt màu đỏ là đường lý tưởng y = x.',
        obs='Các điểm dữ liệu tập trung bám theo trục đường chéo lý tưởng trong khoảng giá từ 2 đến 10 tỷ VNĐ; ở phân khúc biệt thự cao cấp (>15 tỷ) mô hình có xu hướng dự đoán thấp hơn giá thực tế.',
        explanation='Hệ số R² = 0.1905 cho thấy mạng Conv1D bước đầu nắm bắt được xu hướng định giá bất động sản cơ bản từ 133 đặc trưng bảng.',
        limits='CNN 1D trên dữ liệu bảng phẳng không phải là mô hình chuyên dụng cho bài toán định giá so với các cây quyết định tăng cường như XGBoost hoặc LightGBM.'
    )

    add_h2("6.3. BỘ DỮ LIỆU BÌNH LUẬN KHÁCH HÀNG COMMENTS (PHÂN LOẠI CẢM XÚC VĂN BẢN)")
    add_p("Tập dữ liệu Womens Clothing E-Commerce Reviews ghi nhận 23,486 đánh giá của người tiêu dùng về các sản phẩm thời trang. Dựa trên số sao đánh giá (Rating), bài toán được quy về phân loại nhị phân cảm xúc (Sentiment Analysis): Đánh giá tích cực (Rating ≥ 4, gán nhãn 1) và Đánh giá tiêu cực (Rating ≤ 3, gán nhãn 0).")
    
    add_p("Khác biệt với dữ liệu bảng số học, dữ liệu văn bản thô không thể nạp trực tiếp vào mạng tích chập. Pipeline xử lý ngôn ngữ tự nhiên được xây dựng qua các công đoạn: Chuyển chữ thường (Lowercase) → Tách từ (Tokenization) → Xây dựng từ điển với kích thước cố định Vocab_Size = 10,000 từ phổ biến nhất → Cắt ngắn/chèn thêm (Padding/Truncating) về độ dài chuẩn L = 100 tokens. Sau đó, một tầng Nhúng từ (Embedding Layer) sẽ ánh xạ mỗi chỉ số từ vựng thành một vector đặc trưng ngữ nghĩa liên tục 64 chiều.")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_6_5_comments_pipeline.png',
        fig_title='Hình 6.5 – Cấu trúc dữ liệu và pipeline phân tích cảm xúc bình luận Comments',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 5 - Pipeline xử lý văn bản và huấn luyện TextCNN.',
        read_guide='Hiển thị kích thước từ điển (10,000 từ), độ dài chuỗi (100 tokens), mẫu vector chỉ số từ vựng và tiến trình huấn luyện 5 epochs.',
        obs='Mô hình PyTorch TextCNN đạt độ chính xác kiểm thử Test Accuracy = 88.05% và F1-Score = 0.8791 sau 5 epochs với tổng số 689,858 tham số.',
        explanation='Tầng Embedding 64 chiều đã chuyển đổi thành công chuỗi từ rời rạc thành một không gian ngữ nghĩa liên tục phong phú trước khi đưa vào tích chập.',
        limits='Bộ tiền xử lý tách từ theo khoảng trắng đơn giản chưa xử lý được các từ ghép hoặc tiếng lóng viết tắt phức tạp của người dùng.'
    )

    add_image_with_caption(
        img_path='ass4_experiments/plots/fig_6_6_text_cnn_pipeline.png',
        fig_title='Hình 6.6 – Sơ đồ luồng xử lý Text: Token IDs → Embedding 64D → Conv1D → GlobalPool',
        source='Sơ đồ kiến trúc mô hình Kim-CNN cho phân loại văn bản.',
        read_guide='Theo dõi luồng xử lý từ câu văn bản thô ở bên trái qua 5 tầng biến đổi tuần tự để tạo ra xác suất cảm xúc nhị phân ở ngõ ra.',
        obs='Bộ lọc Conv1D kích thước kernel = 3 trượt qua các từ lân cận có chức năng hoàn toàn tương đương với việc học các cụm 3 từ (Trigrams) mang sắc thái biểu cảm cao.',
        explanation='Phép Global Max-Pooling gom toàn bộ ma trận đặc trưng câu thành một vector duy nhất đại diện cho từ khóa nổi bật nhất trong toàn bộ đoạn bình luận.',
        limits='Mô hình tích chập 1D bắt được các mẫu ngữ nghĩa cục bộ rất tốt nhưng có hạn chế trong việc mô hình hóa các mối liên hệ phụ thuộc xa (long-range dependencies).'
    )

    add_h2("6.4. TRIỂN KHAI TENSORFLOW TRÊN DIABETES, HOUSE PRICE VÀ COMMENTS")
    add_p("Để hoàn thành đối chứng chéo framework theo yêu cầu của Giảng viên, toàn bộ ba bài toán 1D trên đều được tái hiện độc lập bằng thư viện TensorFlow/Keras với cấu trúc nơ-ron tương đương:")
    add_bullet("TensorFlow Diabetes: Sequential([Conv1D(16, kernel_size=2), MaxPool1D(2), Flatten(), Dense(32), Dense(1, sigmoid)]). Đạt Test Accuracy = 82.76% (Hình 6.7).")
    add_bullet("TensorFlow House Price: Sequential([Conv1D(32, kernel_size=3), MaxPool1D(2), Flatten(), Dense(64), Dense(1, linear)]). Đạt Test MAE = 1.6016 tỷ VNĐ, RMSE = 1.9611 tỷ VNĐ, R² = 0.1965 (Hình 6.8).")
    add_bullet("TensorFlow Comments: Sequential([Embedding(10000, 64), Conv1D(128, kernel_size=3), GlobalMaxPool1D(), Dense(64), Dense(1, sigmoid)]). Đạt Test Accuracy = 87.17% (Hình 6.9).")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_6_7_tf_diabetes.png',
        fig_title='Hình 6.7 – Cấu trúc mô hình và kết quả TensorFlow Conv1D trên dữ liệu Diabetes',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 6 - TensorFlow Diabetes Conv1D.',
        read_guide='Hiển thị bảng model.summary() với 1,649 tham số và kết quả hàm model.fit() đạt độ chính xác kiểm thử 82.76%.',
        obs='Mô hình TensorFlow đạt độ chính xác phân loại cao hơn lần chạy PyTorch trên tập Diabetes (82.76% so với 69.83%).',
        explanation='Với các tập dữ liệu nhỏ (768 mẫu), sự khác biệt trong cơ chế khởi tạo trọng số mặc định (Glorot Uniform vs Kaiming Uniform) có thể dẫn tới các điểm dừng hội tụ khác nhau.',
        limits='Kết quả phản ánh hiệu năng của một lần chạy ngẫu nhiên cụ thể, không đủ cơ sở để khẳng định framework nào vượt trội tuyệt đối.'
    )

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_6_8_tf_house.png',
        fig_title='Hình 6.8 – Cấu trúc mô hình và kết quả hồi quy TensorFlow Conv1D trên House Price',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 7 - TensorFlow House Price Conv1D.',
        read_guide='Bảng tóm tắt kiến trúc mô hình TensorFlow với 133,377 tham số và kết quả đánh giá hồi quy kiểm thử.',
        obs='Mô hình đạt MAE = 1.6016 tỷ VNĐ và R² = 0.1965, cho kết quả tương đương gần như tuyệt đối với mô hình PyTorch (MAE = 1.6100, R² = 0.1905).',
        explanation='Sự đồng quy của hai framework độc lập trên cùng một bài toán hồi quy phức tạp chứng minh tính đúng đắn và ổn định của quy trình tiền xử lý 133 đặc trưng.',
        limits='Thời gian huấn luyện trên TensorFlow dài hơn (18.88 giây so với 6.67 giây của PyTorch) do chi phí quản lý biểu đồ tính toán tĩnh.'
    )

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_6_9_tf_comments.png',
        fig_title='Hình 6.9 – Cấu trúc mô hình và kết quả phân loại TensorFlow Conv1D trên Comments',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 8 - TensorFlow Text Conv1D.',
        read_guide='Bảng tóm tắt tầng Embedding và Conv1D với 673,025 tham số cùng kết quả huấn luyện 5 epochs.',
        obs='Mô hình đạt Test Accuracy = 87.17%, bám sát hiệu năng của mô hình PyTorch TextCNN (88.05%).',
        explanation='Cơ chế tầng Embedding kết hợp GlobalMaxPooling1D trong TensorFlow vận hành hiệu quả, trích xuất chuẩn xác các từ khóa cảm xúc trọng tâm.',
        limits='Validation loss có xu hướng tăng nhẹ ở Epoch 4-5 báo hiệu dấu hiệu quá khớp nhẹ (overfitting) trên tập từ vựng văn bản.'
    )

    add_h2("6.7. ĐỐI CHUẨN HIỆU NĂNG PYTORCH VÀ TENSORFLOW TRÊN BA BỘ DỮ LIỆU 1D")
    add_p("Toàn bộ các kết quả thực nghiệm 1D qua hai nền tảng học sâu được tổng hợp trong Bảng 6.1 và hai biểu đồ đối sánh Hình 6.10, Hình 6.11:")

    tbl_1d_comp = doc.add_table(rows=7, cols=5)
    tbl_1d_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_1d_comp.autofit = False
    
    headers_1d = ["Tập dữ liệu", "Framework", "Chỉ số đánh giá chính", "Điểm số đạt được", "Thời gian huấn luyện"]
    w_1d = [Cm(3.2), Cm(3.2), Cm(4.0), Cm(3.2), Cm(2.8)]
    for c_idx, h_text in enumerate(headers_1d):
        cell = tbl_1d_comp.cell(0, c_idx)
        cell.width = w_1d[c_idx]
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]; r = p.add_run(h_text); r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.size = Pt(10)

    rows_1d = [
        ("Diabetes", "PyTorch", "Accuracy / F1-Score", "0.6983 (69.83%)", "0.50 giây"),
        ("Diabetes", "TensorFlow", "Accuracy", "0.8276 (82.76%)", "1.18 giây"),
        ("House Price", "PyTorch", "Hệ số xác định R² (MAE)", "0.1905 (MAE: 1.6100 tỷ)", "6.67 giây"),
        ("House Price", "TensorFlow", "Hệ số xác định R² (MAE)", "0.1965 (MAE: 1.6016 tỷ)", "18.88 giây"),
        ("Comments", "PyTorch", "Accuracy / F1-Score", "0.8805 (88.05%)", "18.95 giây"),
        ("Comments", "TensorFlow", "Accuracy", "0.8717 (87.17%)", "21.66 giây")
    ]
    for r_idx, row_vals in enumerate(rows_1d):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_1d_comp.cell(r_idx+1, c_idx)
            cell.width = w_1d[c_idx]
            if (r_idx+1) % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val); r.font.size = Pt(9.5)
            if c_idx in [0, 1, 3]:
                r.bold = True

    set_table_borders(tbl_1d_comp, color="CBD5E0", sz="4", val="single")

    add_image_with_caption(
        img_path='ass4_experiments/plots/14_pytorch_vs_tensorflow_classification_acc.png',
        fig_title='Hình 6.10 – So sánh Classification Accuracy giữa PyTorch và TensorFlow (Diabetes, Comments)',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 9 - Đối chuẩn phân loại 1D.',
        read_guide='Biểu đồ cột nhóm so sánh trực quan độ chính xác phân loại của PyTorch và TensorFlow trên Diabetes và Comments.',
        obs='TensorFlow chiếm ưu thế trên tập Diabetes (82.76% vs 69.83%), trong khi PyTorch đạt điểm số nhỉnh hơn trên tập văn bản Comments (88.05% vs 87.17%).',
        explanation='Chứng minh không có một framework đơn nhất nào giành chiến thắng tuyệt đối trên mọi tập dữ liệu; sự tương thích phụ thuộc vào cấu trúc dữ liệu và cơ chế tối ưu nội tại.',
        limits='So sánh được ghi nhận trên cùng một cấu hình siêu tham số cố định qua 5 epochs.'
    )

    add_image_with_caption(
        img_path='ass4_experiments/plots/15_pytorch_vs_tensorflow_house_r2.png',
        fig_title='Hình 6.11 – So sánh hệ số xác định R² giữa PyTorch và TensorFlow trên House Price',
        source='Notebook tabular_text_cnn_a04.ipynb, Cell 9 - Đối chuẩn hồi quy định giá nhà.',
        read_guide='Biểu đồ cột so sánh trực tiếp chỉ số R² của hai framework trên bài toán dự đoán giá nhà.',
        obs='Cả hai mô hình đạt kết quả tương đồng sát nút: PyTorch đạt R² = 0.1905 và TensorFlow đạt R² = 0.1965.',
        explanation='Khẳng định khi kiến trúc toán học và quy trình tiền xử lý được chuẩn hóa, hai framework lớn sẽ cho ra những kết quả giải tích có tính nhất quán rất cao.',
        limits='Thời gian thực thi của PyTorch nhanh hơn khoảng 2.8 lần so với TensorFlow trên bài toán hồi quy 133 đặc trưng bảng này.'
    )

    # -------------------------------------------------------------
    # 7. GIẢI THÍCH CODE NOTEBOOK (WALKTHROUGH KỸ THUẬT)
    # -------------------------------------------------------------
    add_h1("7. GIẢI THÍCH CODE NOTEBOOK (WALKTHROUGH KỸ THUẬT)")
    add_p("Để minh chứng sự thấu hiểu sâu sắc mã nguồn và đáp ứng yêu cầu giải thích chi tiết của Giảng viên khi thuyết trình đồ án, phần này phân tích 4 khía cạnh kỹ thuật then chốt trong cấu trúc hai notebook của dự án:")

    add_h2("7.1. IMPORT VÀ DATA PIPELINE")
    add_p("Data Pipeline đóng vai trò kiến tạo không gian biểu diễn đầu vào. Trong mã nguồn dự án, toàn bộ các phép tiền xử lý dữ liệu được thiết kế hoàn toàn tự động và sử dụng đường dẫn tương đối, giúp mã nguồn có thể thực thi ngay lập tức khi mở bằng Anaconda JupyterLab. Dữ liệu ảnh được chuẩn hóa qua torchvision.transforms.Compose([transforms.ToTensor(), transforms.Normalize(...)]); dữ liệu bảng được mã hóa qua sklearn.preprocessing.OneHotEncoder; dữ liệu văn bản được ánh xạ từ vựng sang chỉ số nguyên.")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_7_1_data_pipeline.png',
        fig_title='Hình 7.1 – Module Import và Pipeline chuẩn hóa dữ liệu thành Tensor',
        source='Notebook image_cnn_a04.ipynb, Cell 1 - Thiết lập môi trường và nạp dữ liệu.',
        read_guide='Mã nguồn thể hiện các khai báo thư viện chuẩn và pipeline tạo DataLoader với batch_size=64.',
        obs='Dữ liệu 60,000 mẫu train và 10,000 mẫu test được đóng gói thành các mini-batch kích thước torch.Size([64, 1, 28, 28]) sẵn sàng cho GPU/CPU xử lý.',
        explanation='Việc xáo trộn ngẫu nhiên (shuffle=True) trong quá trình huấn luyện giúp phá vỡ tính phụ thuộc tương quan giữa các mẫu liên tiếp.',
        limits='Pipeline yêu cầu bộ nhớ RAM tối thiểu 2GB để lưu trữ và chuẩn hóa đồng thời các tập dữ liệu ảnh trong bộ nhớ đệm.'
    )

    add_h2("7.2. MODEL DEFINITION VÀ FORWARD PASS")
    add_p("Trong PyTorch, mọi mô hình mạng đều kế thừa từ lớp cơ sở torch.nn.Module. Phương thức __init__() có trách nhiệm khởi tạo các lớp biến đổi có tham số học được (Conv2d, BatchNorm2d, Linear); trong khi phương thức forward() định nghĩa đường đi chính xác của dữ liệu qua đồ thị tính toán động. Sự phân tách rõ ràng giữa khối trích xuất đặc trưng (self.features) và khối phân loại (self.classifier) giúp mã nguồn đạt tính module hóa cao.")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_7_2_model_architecture.png',
        fig_title='Hình 7.2 – Khai báo kiến trúc lớp mạng Conv2D/Conv1D và hàm truyền thẳng Forward',
        source='Notebook image_cnn_a04.ipynb, Cell 2 - Định nghĩa class BasicCNN kế thừa nn.Module.',
        read_guide='Khối mã nguồn thể hiện định nghĩa cấu trúc tầng mạng trong __init__ và luồng dữ liệu tuần tự trong forward().',
        obs='Khai báo tường minh hai khối Sequential: khối trích xuất đặc trưng không gian và khối phân loại tuyến tính có lớp Dropout chống học vẹt.',
        explanation='Hàm forward() tiếp nhận tensor đầu vào và trả về trực tiếp các giá trị logits thô trước khi nạp vào hàm mất mát tối ưu.',
        limits='Các kích thước kênh vào/ra (16, 32, 64) được cấu hình cố định, chưa tham số hóa động theo dạng danh sách lớp.'
    )

    add_h2("7.3. VÒNG LẶP HUẤN LUYỆN VÀ LAN TRUYỀN NGƯỢC (TRAINING LOOP)")
    add_p("Vòng lặp huấn luyện trong PyTorch thể hiện trực quan các nguyên lý giải tích của thuật toán lan truyền ngược. Mỗi bước lặp mini-batch đều tuân thủ chặt chẽ trình tự 5 bước: (1) optimizer.zero_grad() để xóa các gradient tích lũy từ bước trước; (2) outputs = model(images) thực hiện lan truyền xuôi; (3) loss = criterion(outputs, targets) tính hàm mất mát; (4) loss.backward() kích hoạt Autograd tính đạo hàm riêng cho từng tham số; (5) optimizer.step() cập nhật trọng số dựa trên thuật toán Adam.")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_7_3_training_loop.png',
        fig_title='Hình 7.3 – Chu trình lan truyền xuôi và ngược trong vòng lặp huấn luyện PyTorch',
        source='Notebook image_cnn_a04.ipynb, Cell 3 - Cài đặt hàm train_one_epoch().',
        read_guide='Mã nguồn hàm lặp huấn luyện chuẩn PyTorch với các chú thích từng bước giải tích.',
        obs='Mã nguồn ghi nhận đầy đủ thống kê running_loss và tính toán độ chính xác tích lũy thời gian thực trên từng mini-batch dữ liệu.',
        explanation='Sự tường minh trong vòng lặp PyTorch giúp kỹ sư dễ dàng can thiệp kỹ thuật như kẹp gradient (Gradient Clipping) hoặc ghi nhật ký tùy biến.',
        limits='Đòi hỏi kỹ sư phải tự quản lý thiết bị tính toán (.to(device)) một cách thủ công so với các hàm đóng gói sẵn.'
    )

    add_h2("7.4. EVALUATION VÀ TRÍCH XUẤT CHỈ SỐ")
    add_p("Quy trình đánh giá kiểm thử được tách biệt hoàn toàn khỏi quá trình huấn luyện nhằm đảm bảo tính khách quan khoa học. Việc kích hoạt chế độ model.eval() sẽ vô hiệu hóa hoạt động của các tầng Dropout và chuyển tầng Batch Normalization sang sử dụng giá trị kỳ vọng tích lũy. Đồng thời, khối ngữ cảnh with torch.no_grad() được sử dụng để ngắt hoàn toàn việc xây dựng đồ thị tính toán đạo hàm, giúp tiết kiệm hơn 65% dung lượng bộ nhớ VRAM và tăng tốc độ suy luận lên gấp nhiều lần.")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/cell_7_4_evaluation_function.png',
        fig_title='Hình 7.4 – Hàm đánh giá mô hình và trích xuất chỉ số kiểm thử với torch.no_grad()',
        source='Notebook image_cnn_a04.ipynb, Cell 4 - Cài đặt hàm evaluate_test().',
        read_guide='Mã nguồn hàm đánh giá kiểm định tính toán đồng thời các chỉ số Accuracy, Precision, Recall và F1-Score.',
        obs='Hàm chuyển đổi tensor dự đoán từ GPU về mảng NumPy để tận dụng các thư viện đánh giá chuyên sâu của Scikit-learn.',
        explanation='Cơ chế zero_division=0 trong precision_score giúp bảo vệ chương trình không bị lỗi chia cho 0 khi một lớp hiếm không có mẫu dự đoán.',
        limits='Hàm xử lý gom toàn bộ dự đoán trên bộ nhớ RAM, có thể gây tràn bộ nhớ nếu tập kiểm thử có quy mô hàng triệu bản ghi.'
    )

    # -------------------------------------------------------------
    # 8. TỔNG HỢP KẾT QUẢ TOÀN BỘ THỰC NGHIỆM
    # -------------------------------------------------------------
    add_h1("8. TỔNG HỢP KẾT QUẢ TOÀN BỘ THỰC NGHIỆM")
    add_p("Toàn bộ các chỉ số kiểm thử thu thập được từ hai notebook cốt lõi của dự án được tổng hợp có hệ thống trong hai bảng dữ liệu dưới đây:")

    add_h2("KẾT QUẢ THỰC NGHIỆM NHÓM IMAGE CNN (2D)")
    tbl_sum_img = doc.add_table(rows=4, cols=6)
    tbl_sum_img.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sum_img.autofit = False
    
    hdr_si = ["Tập dữ liệu", "Kiến trúc mô hình", "Kích thước Tensor đầu vào", "Số tham số", "Test Accuracy", "Thời gian (5 Epochs)"]
    w_si = [Cm(3.0), Cm(3.2), Cm(3.3), Cm(2.2), Cm(2.5), Cm(2.2)]
    for c_idx, h_text in enumerate(hdr_si):
        cell = tbl_sum_img.cell(0, c_idx)
        cell.width = w_si[c_idx]
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]; r = p.add_run(h_text); r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.size = Pt(10)

    rows_si = [
        ("MNIST", "PyTorch BasicCNN", "1 × 28 × 28 (Ảnh xám)", "20,490", "0.9850 (98.50%)", "53.52 giây"),
        ("Fashion-MNIST", "PyTorch BasicCNN", "1 × 28 × 28 (Ảnh xám)", "20,490", "0.9013 (90.13%)", "53.91 giây"),
        ("CIFAR-10", "PyTorch BasicCNN", "3 × 32 × 32 (Ảnh màu RGB)", "20,778", "0.6477 (64.77%)", "185.40 giây")
    ]
    for r_idx, row_vals in enumerate(rows_si):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_sum_img.cell(r_idx+1, c_idx)
            cell.width = w_si[c_idx]
            if (r_idx+1) % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val); r.font.size = Pt(9.5)
            if c_idx in [0, 4]:
                r.bold = True

    set_table_borders(tbl_sum_img, color="CBD5E0", sz="4", val="single")

    add_h2("KẾT QUẢ THỰC NGHIỆM NHÓM TABULAR & TEXT CNN (1D)")
    tbl_sum_1d = doc.add_table(rows=7, cols=6)
    tbl_sum_1d.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sum_1d.autofit = False
    
    hdr_s1 = ["Tập dữ liệu", "Framework", "Bản chất bài toán", "Kích thước Tensor", "Chỉ số kiểm thử chính", "Thời gian huấn luyện"]
    w_s1 = [Cm(2.8), Cm(2.4), Cm(3.2), Cm(2.8), Cm(3.2), Cm(2.0)]
    for c_idx, h_text in enumerate(hdr_s1):
        cell = tbl_sum_1d.cell(0, c_idx)
        cell.width = w_s1[c_idx]
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]; r = p.add_run(h_text); r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.size = Pt(10)

    rows_s1 = [
        ("Diabetes", "PyTorch", "Binary Classification", "1 × 8 đặc trưng", "Accuracy = 0.6983 (69.83%)", "0.50 giây"),
        ("Diabetes", "TensorFlow", "Binary Classification", "1 × 8 đặc trưng", "Accuracy = 0.8276 (82.76%)", "1.18 giây"),
        ("House Price", "PyTorch", "Regression", "1 × 133 đặc trưng", "R² = 0.1905 (MAE: 1.6100 tỷ)", "6.67 giây"),
        ("House Price", "TensorFlow", "Regression", "1 × 133 đặc trưng", "R² = 0.1965 (MAE: 1.6016 tỷ)", "18.88 giây"),
        ("Comments", "PyTorch", "Text Classification", "100 tokens (Embed 64)", "Accuracy = 0.8805 (88.05%)", "18.95 giây"),
        ("Comments", "TensorFlow", "Text Classification", "100 tokens (Embed 64)", "Accuracy = 0.8717 (87.17%)", "21.66 giây")
    ]
    for r_idx, row_vals in enumerate(rows_s1):
        for c_idx, val in enumerate(row_vals):
            cell = tbl_sum_1d.cell(r_idx+1, c_idx)
            cell.width = w_s1[c_idx]
            if (r_idx+1) % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val); r.font.size = Pt(9.5)
            if c_idx in [0, 1, 4]:
                r.bold = True

    set_table_borders(tbl_sum_1d, color="CBD5E0", sz="4", val="single")

    add_note_box(
        "Tuyệt đối không so sánh trực tiếp một con số độ chính xác (Accuracy) duy nhất giữa các tập dữ liệu khác nhau. Một mô hình đạt 64.77% trên CIFAR-10 không hề 'kém cỏi' hơn mô hình đạt 98.50% trên MNIST, bởi vì không gian biểu diễn của ảnh màu tự nhiên phức tạp gấp hàng trăm lần nét vẽ chữ số xám. Tương tự, bài toán hồi quy giá nhà bắt buộc phải đo bằng MAE/RMSE/R², không thể gượng ép đánh giá bằng Accuracy.",
        title="Nguyên tắc đánh giá khoa học:"
    )

    # -------------------------------------------------------------
    # 9. PHÂN TÍCH KẾT QUẢ VÀ BÀI HỌC KHOA HỌC
    # -------------------------------------------------------------
    add_h1("9. PHÂN TÍCH KẾT QUẢ VÀ BÀI HỌC KHOA HỌC")
    add_p("Từ chuỗi thực nghiệm toàn diện trên 6 tập dữ liệu đa dạng, báo cáo rút ra ba bài học khoa học cốt lõi mang tính định hướng cho việc phát triển các hệ thống thông minh:")
    
    add_bullet("Kiến trúc phải phục vụ Biểu diễn dữ liệu (Architecture must strictly follow Data Representation): Mạng nơ-ron tích chập 2D phát huy tối đa sức mạnh trên dữ liệu hình ảnh nhờ tính kết nối cục bộ và bất biến tịnh tiến tự nhiên của các điểm ảnh. Khi chuyển sang dữ liệu văn bản, việc bổ sung tầng Embedding đóng vai trò sống còn để tạo ra không gian ngữ nghĩa liên tục cho các bộ lọc Conv1D trích xuất n-gram. Ngược lại, trên dữ liệu bảng phẳng (Tabular), thứ tự các cột mang tính sắp đặt tùy ý, do đó Conv1D chỉ đóng vai trò như một bộ trích xuất tương quan cặp đôi hạn chế, chưa thể thay thế hoàn toàn các kiến trúc học máy chuyên dụng dạng cây quyết định.")
    
    add_bullet("Tác động của Kỹ thuật Chuẩn hóa (Batch Normalization): Việc bổ sung tầng BatchNorm2d vào mô hình MNIST đã cải thiện độ chính xác từ 98.50% lên 98.67% và mang lại tốc độ hội tụ vượt trội ngay từ những epoch đầu tiên. Điều này khẳng định việc duy trì sự ổn định của phân phối dữ liệu trung gian qua các tầng sâu là yếu tố quyết định để mô hình học sâu vận hành hiệu quả.")
    
    add_bullet("Tính tương đương giải tích giữa các Framework: Cả PyTorch và TensorFlow đều đạt được các kết quả dự đoán có độ tương đồng rất cao khi được xây dựng trên cùng một kiến trúc toán học và quy trình tiền xử lý chuẩn mực. PyTorch vượt trội về tính linh hoạt, trực quan trong nghiên cứu và gỡ lỗi (Debugging); trong khi TensorFlow/Keras tối ưu hóa cao về khả năng đóng gói tinh gọn cho môi trường triển khai thực tế.")

    # -------------------------------------------------------------
    # 10. HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN
    # -------------------------------------------------------------
    add_h1("10. HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN")
    add_p("Mặc dù đã hoàn thành trọn vẹn toàn bộ các mục tiêu học thuật đề ra, hệ thống thực nghiệm hiện tại vẫn tồn tại một số hạn chế kỹ thuật cần được nhìn nhận khách quan:")
    add_bullet("Hạn chế về ngân sách huấn luyện: Số lượng epochs được ấn định cố định ở mức 5 epochs cho toàn bộ các mô hình nhằm phục vụ mục đích so sánh tiến trình học tập giáo dục. Ngân sách này là chưa đủ để các mô hình trên tập dữ liệu phức tạp như CIFAR-10 hoặc Comments hội tụ về điểm cực tiểu toàn cục.")
    add_bullet("Hạn chế về kiến trúc mô hình: Các mô hình thị giác trong bài vẫn sử dụng kiến trúc tuần tự cổ điển (kiểu LeNet/AlexNet), chưa tích hợp các kết nối tắt phần dư (Residual Connections kiểu ResNet) giúp huấn luyện mạng sâu hàng chục tầng mà không bị suy thoái gradient.")
    add_bullet("Hạn chế về xử lý ngôn ngữ tự nhiên: Bộ tiền xử lý văn bản tập Comments mới dừng lại ở việc tách từ theo khoảng trắng đơn giản và giới hạn chiều dài 100 tokens, vô tình làm mất đi thông tin ngữ cảnh của các bài đánh giá dài hoặc các từ đồng nghĩa phức tạp.")

    add_p("Các hướng phát triển mở rộng trong tương lai bao gồm:")
    add_bullet("Tích hợp kỹ thuật tăng cường dữ liệu nâng cao (Data Augmentation) như xoay ảnh ngẫu nhiên, cắt xén (Random Crop) và điều chỉnh màu sắc cho tập dữ liệu CIFAR-10.")
    add_bullet("Thử nghiệm các kiến trúc hiện đại hơn như ResNet-18 hoặc Vision Transformer (ViT) cho bài toán thị giác máy tính.")
    add_bullet("Áp dụng các mô hình ngôn ngữ tiền huấn luyện (Pre-trained BERT / RoBERTa) để tạo vector nhúng ngữ cảnh sâu cho bài toán phân tích cảm xúc văn bản.")
    add_bullet("Xây dựng mô hình hỗn hợp (Hybrid Model) kết hợp tầng tích chập Conv1D và tầng mạng hồi quy LSTM để khai thác đồng thời cả đặc trưng cục bộ và sự phụ thuộc thời gian dài trong chuỗi.")

    # -------------------------------------------------------------
    # 11. KẾT LUẬN
    # -------------------------------------------------------------
    add_h1("11. KẾT LUẬN")
    add_p("Báo cáo Assignment 04 đã hoàn thành xuất sắc toàn bộ các nội dung nghiên cứu lý thuyết và kịch bản thực nghiệm theo đúng định hướng chỉ dẫn trên bảng của PGS. TS. Trần Đình Quế. Dự án đã hiện thực hóa thành công một chuỗi nghiên cứu học thuật hoàn chỉnh: từ việc phân tích bản chất toán học của Deep Learning dưới góc nhìn Function Composition; tự tay lập trình phép tích chập và lan truyền ngược từ đầu bằng thư viện NumPy thuần túy; cho tới việc làm chủ và so sánh đối chuẩn hiệu năng trên hai nền tảng học sâu công nghiệp hàng đầu thế giới là PyTorch và TensorFlow.")
    
    add_p("Thông qua 6 bộ dữ liệu trải dài trên cả ba hình thái biểu diễn: hình ảnh 2D (MNIST, Fashion-MNIST, CIFAR-10), dữ liệu bảng số học 1D (Diabetes, House Price 2024), và chuỗi văn bản 1D (Comments Reviews), bài tập lớn đã chứng minh thuyết phục rằng Mạng nơ-ron Tích chập (CNN) là một phương pháp luận trích xuất đặc trưng có cấu trúc cực kỳ mạnh mẽ và linh hoạt. Kết quả thực nghiệm đạt độ chính xác ấn tượng: 98.50% trên MNIST (98.67% với Improved CNN), 90.13% trên Fashion-MNIST, 88.05% trên văn bản Comments, cùng hệ số R² = 0.1905 trên bài toán hồi quy định giá nhà.")
    
    add_p("Toàn bộ mã nguồn thực thi được tổ chức khoa học và lưu trữ tập trung trong hai Jupyter Notebook cốt lõi (image_cnn_a04.ipynb và tabular_text_cnn_a04.ipynb), sẵn sàng phục vụ trình chiếu trực tiếp và giải trình kỹ thuật trước Giảng viên. Kết quả của bài thực nghiệm đặt nền tảng kiến thức vững chắc cho việc tiếp cận các cấu trúc mạng nơ-ron tiên tiến hơn trong các học phần chuyên sâu tiếp theo.")

    # -------------------------------------------------------------
    # PHỤ LỤC – TÀI NGUYÊN DATASET VÀ MÃ NGUỒN
    # -------------------------------------------------------------
    add_h1("PHỤ LỤC – TÀI NGUYÊN DATASET VÀ MÃ NGUỒN")
    
    add_h2("TÀI NGUYÊN DỮ LIỆU THỰC NGHIỆM (KAGGLE & TORCHVISION)")
    add_bullet("1. MNIST in CSV – Kaggle Dataset: https://www.kaggle.com/datasets/oddrationale/mnist-in-csv")
    add_bullet("2. Fashion-MNIST – Zalando Research Kaggle: https://www.kaggle.com/datasets/zalando-research/fashionmnist")
    add_bullet("3. CIFAR-10 – Ayush1220 Kaggle: https://www.kaggle.com/datasets/ayush1220/cifar10")
    add_bullet("4. Vietnam Housing Dataset 2024 – Kaggle Dataset: https://www.kaggle.com/datasets/nguyentiennhan/vietnam-housing-dataset-2024")
    add_bullet("5. Womens Clothing E-Commerce Reviews – Kaggle: https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews")
    add_bullet("6. Pima Indians Diabetes Database – Kaggle: https://www.kaggle.com/datasets/jamaltariqcheema/pima-indians-diabetes-dataset/data")

    add_h2("CẤU TRÚC VÀ VỊ TRÍ LƯU TRỮ MÃ NGUỒN DỰ ÁN")
    add_p("Toàn bộ mã nguồn và dữ liệu của dự án được lưu trữ trong không gian làm việc cục bộ của sinh viên Nguyễn Tuấn Tài (B23DCCN731 - Nhóm 06) với cấu trúc phục vụ thuyết trình Anaconda Jupyter:")
    add_bullet("notebooks/image_cnn_a04.ipynb: Chứa toàn bộ các cell nạp dữ liệu ảnh, Scratch CNN NumPy, PyTorch BasicCNN, Improved CNN (+BatchNorm), TensorFlow Keras CNN, Fashion-MNIST, CIFAR-10 và bảng so sánh 3 bộ ảnh.")
    add_bullet("notebooks/tabular_text_cnn_a04.ipynb: Chứa toàn bộ các cell tiền xử lý One-Hot 133 chiều House Price, chuẩn hóa Diabetes, Embedding 64D Comments, huấn luyện Conv1D trên PyTorch & TensorFlow, xuất biểu đồ hồi quy và bảng đối chuẩn 1D.")
    add_bullet("data/: Thư mục lưu trữ tập trung toàn bộ các tệp dữ liệu CSV và NPZ của cả 6 bài toán phục vụ việc nạp dữ liệu độc lập.")

    # -------------------------------------------------------------
    # XUẤT TỆP WORD
    # -------------------------------------------------------------
    out_file = "A04_06_taint.731.docx"
    doc.save(out_file)
    print(f"[THÀNH CÔNG] Đã tạo báo cáo chính: {out_file}")
    
    # Copy sang thư mục ass4/ nếu có
    if os.path.exists("ass4"):
        ass4_out = os.path.join("ass4", "A04_06_taint.731.docx")
        doc.save(ass4_out)
        print(f"[THÀNH CÔNG] Đã sao lưu sang thư mục ass4: {ass4_out}")

if __name__ == "__main__":
    build_comprehensive_report()
