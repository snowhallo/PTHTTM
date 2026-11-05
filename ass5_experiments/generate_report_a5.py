import os, sys, json, shutil
sys.stdout.reconfigure(encoding='utf-8')
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_a05_report():
    print("=== KHỞI TẠO BÁO CÁO HỌC THUẬT ASSIGNMENT 05 ===")
    doc = docx.Document()
    
    # 1. Cấu hình lề trang theo chuẩn luận văn PTIT (Trái 3cm, Phải 2cm, Trên 2cm, Dưới 2cm)
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(4)
    
    # Helper functions
    def set_cell_background(cell, fill_color):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="CBD5E0", sz="4", val="single"):
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
        run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D) # PTIT Navy Blue
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

    def add_note_box(text, title="Nhận xét chuyên sâu:"):
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

    def add_image_with_caption(img_path, fig_title, source, read_guide, obs, explanation, limits, width_inch=5.8):
        if not os.path.exists(img_path):
            print(f"CẢNH BÁO: Không tìm thấy tệp ảnh: {img_path}")
            return
        # Ảnh
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inch))
        
        # Tiêu đề hình
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(2)
        run_cap = p_cap.add_run(fig_title)
        run_cap.bold = True
        run_cap.font.size = Pt(11)
        run_cap.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        # 5 phần chú giải học thuật bắt buộc
        meta_items = [
            ("Nguồn và cell liên quan: ", source),
            ("Cách đọc: ", read_guide),
            ("Quan sát: ", obs),
            ("Giải thích chi tiết: ", explanation),
            ("Giới hạn diễn giải: ", limits)
        ]
        for prefix, content in meta_items:
            p_m = doc.add_paragraph()
            p_m.paragraph_format.left_indent = Cm(0.8)
            p_m.paragraph_format.space_after = Pt(2)
            p_m.paragraph_format.line_spacing = 1.15
            run_p = p_m.add_run(prefix)
            run_p.bold = True
            run_p.font.size = Pt(10)
            run_p.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
            run_c = p_m.add_run(content)
            run_c.font.size = Pt(10)
            run_c.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
            
        p_post = doc.add_paragraph()
        p_post.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # TRANG BÌA CHUẨN HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
    # -------------------------------------------------------------
    p_b1 = doc.add_paragraph()
    p_b1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b1.paragraph_format.space_before = Pt(10)
    p_b1.paragraph_format.space_after = Pt(2)
    r = p_b1.add_run("BỘ KHOA HỌC VÀ CÔNG NGHỆ\n")
    r.font.size = Pt(13)
    r.bold = True
    r = p_b1.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    r = p_b1.add_run("KHOA CÔNG NGHỆ THÔNG TIN 1")
    r.font.size = Pt(12)
    r.bold = True

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(15)
    p_div.paragraph_format.space_after = Pt(25)
    r_div = p_div.add_run("✦ ✦ ✦ -------------------- ✦ ✦ ✦")
    r_div.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(20)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("BÁO CÁO ASSIGNMENT 05\n")
    r_title.font.size = Pt(20)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    r_sub1 = p_title.add_run("PHÁT TRIỂN CÁC KIẾN TRÚC MẠNG NƠ-RON TÍCH CHẬP (CNN)\n")
    r_sub1.font.size = Pt(15)
    r_sub1.bold = True
    r_sub1.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(40)
    r_sub2 = p_sub.add_run("Nghiên Cứu Tiến Hóa Từ Mô Hình Cơ Bản Đến Các Kỹ Thuật Hiện Đại\n(BatchNorm, Residual, Squeeze-and-Excitation Attention)\nVà Các Kiến Trúc Kinh Điển Thích Nghi Trên Đa Dạng Kiểu Dữ Liệu")
    r_sub2.font.size = Pt(12)
    r_sub2.font.italic = True
    r_sub2.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # Khung thông tin sinh viên
    tbl_info = doc.add_table(rows=4, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "PGS. TS. Trần Đình Quế"),
        ("Sinh viên thực hiện:", "Nguyễn Tuấn Tài"),
        ("Mã sinh viên:", "B23DCCN731"),
        ("Lớp học phần & Nhóm:", "INT14149_06 — Nhóm 06")
    ]
    for r_idx, (k, v) in enumerate(info_data):
        row = tbl_info.rows[r_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Cm(5.5)
        c1.width = Cm(9.5)
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(12)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(v)
        r1.font.size = Pt(12)
        if r_idx in [0, 1]:
            r1.bold = True

    set_table_borders(tbl_info, color="A0AEC0", sz="4", val="single")

    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_before = Pt(80)
    p_bot.paragraph_format.space_after = Pt(0)
    r_bot = p_bot.add_run("Hà Nội – Năm 2026")
    r_bot.font.size = Pt(12)
    r_bot.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # MỤC LỤC VÀ DANH MỤC HÌNH VẼ / BẢNG BIỂU
    # -------------------------------------------------------------
    add_h1("MỤC LỤC")
    toc_items = [
        ("1. GIỚI THIỆU VÀ MỤC TIÊU CỦA ASSIGNMENT 05", "3"),
        ("  1.1. Bối cảnh nghiên cứu học máy và mạng tích chập", "3"),
        ("  1.2. Mục tiêu kỹ thuật cốt lõi", "3"),
        ("  1.3. Ba tập dữ liệu thực nghiệm", "4"),
        ("  1.4. Quy trình thực nghiệm tổng thể", "4"),
        ("2. CƠ SỞ LÝ THUYẾT VỀ MẠNG NƠ-RON VÀ CNN", "5"),
        ("  2.1. Bản chất hàm hợp của mạng nơ-ron sâu", "5"),
        ("  2.2. Trích xuất đặc trưng tự động và học biểu diễn", "6"),
        ("  2.3. Cấu trúc một lớp Convolutional", "6"),
        ("  2.4. Phép toán tích chập và bản chất nhân ma trận", "7"),
        ("  2.5. Kích thước Kernel (Kernel Size)", "7"),
        ("  2.6. Bước nhảy trượt (Stride)", "8"),
        ("  2.7. Cơ chế đệm viền (Padding)", "8"),
        ("  2.8. Vùng cảm nhận không gian (Receptive Field)", "9"),
        ("  2.9. Hàm kích hoạt phi tuyến (Activation Functions)", "9"),
        ("  2.10. Tầng gộp giảm chiều (Pooling Layers)", "10"),
        ("  2.11. Tầng kết nối đầy đủ (Fully Connected / Dense Layer)", "10"),
        ("  2.12. Lan truyền ngược và thuật toán cập nhật Adam", "11"),
        ("3. SỰ PHÁT TRIỂN CỦA CÁC KIẾN TRÚC CNN KINH ĐIỂN", "11"),
        ("  3.1. LeNet-5 (1998)", "11"),
        ("  3.2. AlexNet (2012)", "12"),
        ("  3.3. VGG Network (2014)", "12"),
        ("  3.4. ResNet (2015)", "13"),
        ("  3.5. MobileNet và các kiến trúc hiện đại", "14"),
        ("4. CƠ SỞ LÝ THUYẾT VỀ CÁC KỸ THUẬT CẢI TIẾN CNN", "14"),
        ("  4.1. Giới hạn cố hữu của Basic CNN", "14"),
        ("  4.2. Chuẩn hóa theo lô (Batch Normalization)", "15"),
        ("  4.3. Kết nối phần dư (Residual Connection / Skip Connection)", "16"),
        ("  4.4. Cơ chế chú ý kênh (Channel Attention / Squeeze-and-Excitation)", "17"),
        ("  4.5. Phân tích so sánh chuỗi cấu trúc cải tiến M1 – M4", "18"),
        ("  4.6. Mở rộng phép tích chập Conv1D cho dữ liệu dạng bảng", "18"),
        ("  4.7. So sánh các mô hình cổ điển thích nghi", "19"),
        ("5. DỮ LIỆU VÀ BÀI TOÁN THỰC NGHIỆM", "19"),
        ("  5.1. Giới thiệu 3 bài toán nghiên cứu", "19"),
        ("  5.2. Tập dữ liệu MNIST", "20"),
        ("  5.3. Tập dữ liệu Fashion-MNIST", "21"),
        ("  5.4. Tập dữ liệu Bệnh tiểu đường Pima Indians Diabetes", "22"),
        ("  5.5. Chiến lược phân chia dữ liệu Train / Validation / Test", "23"),
        ("  5.6. Tiền xử lý dữ liệu và chuẩn hóa thang đo", "23"),
        ("  5.7. Xây dựng PyTorch DataLoader", "24"),
        ("  5.8. Bảng tổng kết dữ liệu thực nghiệm", "24"),
        ("6. THIẾT KẾ VÀ CÀI ĐẶT CÁC MÔ HÌNH CNN", "25"),
        ("  6.1. Mô hình M1: Basic CNN", "25"),
        ("  6.2. Mô hình M2: BatchNorm CNN", "26"),
        ("  6.3. Mô hình M3: Residual CNN", "27"),
        ("  6.4. Mô hình M4: Attention CNN (Squeeze-and-Excitation)", "28"),
        ("  6.5. Mô hình M5: Adapted LeNet", "29"),
        ("  6.6. Mô hình M6: Adapted AlexNet", "30"),
        ("  6.7. Mô hình M7: Adapted VGG", "31"),
        ("  6.8. Thiết kế các mô hình Conv1D cho dữ liệu bảng Diabetes", "31"),
        ("  6.9. Kiểm tra Output Shape và Thống kê Không gian tham số", "33"),
        ("7. QUY TRÌNH HUẤN LUYỆN VÀ ĐÁNH GIÁ ĐỐI CHUẨN", "34"),
        ("  7.1. Thiết lập siêu tham số và tối ưu hóa", "34"),
        ("  7.2. Cơ chế lưu trữ trạng thái tối ưu (Validation Checkpointing)", "34"),
        ("  7.3. Đánh giá độc lập trên Test Set", "35"),
        ("  7.4. Hệ thống các độ đo đánh giá toàn diện", "35"),
        ("8. KẾT QUẢ THỰC NGHIỆM ĐỐI CHUẨN", "36"),
        ("  8.1. Kết quả thực nghiệm trên tập dữ liệu MNIST", "36"),
        ("  8.2. Kết quả thực nghiệm trên tập dữ liệu Fashion-MNIST", "37"),
        ("  8.3. Kết quả thực nghiệm trên tập dữ liệu Diabetes", "38"),
        ("  8.4. Phân tích chi tiết các độ đo phân loại (Classification Metrics)", "39"),
        ("  8.5. Mức độ cải thiện độ chính xác so với mô hình cơ sở M1", "40"),
        ("  8.6. Phân tích độ phức tạp tính toán và chi phí tham số", "40"),
        ("9. TRỰC QUAN HÓA VÀ PHÂN TÍCH BIỂU ĐỒ KHOA HỌC", "41"),
        ("  9.1. Vai trò của trực quan hóa trong nghiên cứu học sâu", "41"),
        ("  9.2. Phân tích đường cong Loss trên MNIST (Hình 23)", "41"),
        ("  9.3. Phân tích đường cong Loss trên Fashion-MNIST (Hình 24)", "42"),
        ("  9.4. Phân tích đường cong Loss trên Diabetes (Hình 25)", "43"),
        ("  9.5. Phân tích so sánh Test Accuracy trên MNIST (Hình 26)", "44"),
        ("  9.6. Phân tích so sánh Test Accuracy trên Fashion-MNIST (Hình 27)", "45"),
        ("  9.7. Phân tích so sánh Test Accuracy trên Diabetes (Hình 28)", "46"),
        ("  9.8. Phân tích thời gian huấn luyện (Training Time - Hình 29)", "47"),
        ("  9.9. Phân tích số tham số huấn luyện (Trainable Parameters - Hình 30)", "48"),
        ("  9.10. Phân tích Ma trận nhầm lẫn trên MNIST (Hình 31)", "49"),
        ("  9.11. Phân tích Ma trận nhầm lẫn trên Fashion-MNIST (Hình 32)", "50"),
        ("  9.12. Phân tích Ma trận nhầm lẫn trên Diabetes (Hình 33)", "51"),
        ("10. SO SÁNH, THẢO LUẬN VÀ BÀN LUẬN KHOA HỌC", "52"),
        ("  10.1. So sánh chuỗi tiến hóa M1 – M4 trên MNIST", "52"),
        ("  10.2. So sánh chuỗi tiến hóa M1 – M4 trên Fashion-MNIST", "53"),
        ("  10.3. So sánh chuỗi tiến hóa M1 – M4 trên Diabetes", "54"),
        ("  10.4. Classical CNN và các mô hình cải tiến tiến hóa", "55"),
        ("  10.5. Sự khác biệt bản chất giữa Test Loss và Accuracy", "55"),
        ("  10.6. Mối quan hệ giữa Accuracy, Precision, Recall và F1-Score", "56"),
        ("  10.7. Trade-off giữa độ phức tạp mô hình và hiệu quả dự đoán", "57"),
        ("  10.8. Vai trò của tính lặp lại (Reproducibility)", "57"),
        ("  10.9. Ý nghĩa học thuật sâu sắc của Assignment 05", "58"),
        ("11. HẠN CHẾ CỦA THỰC NGHIỆM VÀ HƯỚNG PHÁT TRIỂN", "58"),
        ("  11.1. Giới hạn số lượng epoch huấn luyện", "58"),
        ("  11.2. Kích thước tập dữ liệu Diabetes nhỏ", "59"),
        ("  11.3. Áp dụng Conv1D trên dữ liệu bảng phi cấu trúc không gian", "59"),
        ("  11.4. Bản chất thích nghi của các kiến trúc cổ điển", "60"),
        ("  11.5. Thời gian huấn luyện phụ thuộc tài nguyên phần cứng CPU", "60"),
        ("  11.6. Chưa áp dụng Data Augmentation và Hyperparameter Tuning sâu", "61"),
        ("  11.7. Hướng phát triển và mở rộng trong tương lai", "61"),
        ("12. KẾT LUẬN TỔNG THỂ", "62"),
        ("PHỤ LỤC: NGUỒN DỮ LIỆU KAGGLE VÀ CẤU TRÚC THƯ MỤC DỰ ÁN", "63")
    ]
    for title, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.line_spacing = 1.15
        r_t = p_t.add_run(title)
        if not title.startswith("  "):
            r_t.bold = True
            r_t.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        dots_len = max(3, 85 - len(title))
        r_dots = p_t.add_run(" " + "." * dots_len + " ")
        r_dots.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
        r_pg = p_t.add_run(page)
        r_pg.bold = True

    doc.add_page_break()

    # DANH MỤC HÌNH VẼ
    add_h1("DANH MỤC HÌNH VẼ")
    fig_list = [
        ("Hình 1", "Quy trình thực nghiệm tổng quát của Assignment 05", "4"),
        ("Hình 2", "CNN được nhìn như một hàm hợp của nhiều phép biến đổi", "5"),
        ("Hình 3", "Một số mẫu ảnh MNIST được trực quan hóa trong quá trình chuẩn bị dữ liệu", "20"),
        ("Hình 4", "DataLoader của MNIST và kích thước batch", "21"),
        ("Hình 5", "Một số mẫu Fashion-MNIST được trực quan hóa", "21"),
        ("Hình 6", "Phân chia Training / Validation / Test của Fashion-MNIST", "22"),
        ("Hình 7", "Phân bố hai lớp Outcome của Diabetes", "22"),
        ("Hình 8", "Xử lý giá trị 0 sinh lý bất thường trong Diabetes", "23"),
        ("Hình 9", "Kết quả Dataset summary tổng hợp trong notebook", "25"),
        ("Hình 10", "Định nghĩa kiến trúc cho M1 Basic CNN", "26"),
        ("Hình 11", "Định nghĩa kiến trúc cho M2 BatchNorm CNN", "26"),
        ("Hình 12", "So sánh tham số và kích thước tensor giữa M1 và M2", "27"),
        ("Hình 13", "Định nghĩa khối ResidualBlock2D", "27"),
        ("Hình 14", "Định nghĩa kiến trúc cho M3 Residual CNN", "28"),
        ("Hình 15", "Định nghĩa khối chú ý kênh SEBlock2D", "28"),
        ("Hình 16", "Định nghĩa kiến trúc cho M4 Attention CNN", "29"),
        ("Hình 17", "Định nghĩa kiến trúc M1 Basic Conv1D cho Diabetes", "32"),
        ("Hình 18", "Định nghĩa kiến trúc M2 BatchNorm Conv1D cho Diabetes", "32"),
        ("Hình 19", "Định nghĩa khối ResidualBlock1D", "32"),
        ("Hình 20", "Định nghĩa kiến trúc M3 Residual Conv1D cho Diabetes", "33"),
        ("Hình 21", "Định nghĩa khối SEBlock1D cho Diabetes", "33"),
        ("Hình 22", "Định nghĩa kiến trúc M4 Attention Conv1D cho Diabetes", "33"),
        ("Hình 23", "Đường loss huấn luyện và validation của bảy mô hình trên MNIST", "42"),
        ("Hình 24", "Đường loss huấn luyện và validation của các mô hình trên Fashion-MNIST", "43"),
        ("Hình 25", "Đường loss huấn luyện và validation của bốn mô hình Diabetes", "44"),
        ("Hình 26", "So sánh test accuracy của bảy mô hình trên MNIST", "45"),
        ("Hình 27", "So sánh test accuracy trên Fashion-MNIST", "46"),
        ("Hình 28", "So sánh test accuracy của bốn mô hình Diabetes", "47"),
        ("Hình 29", "Thời gian huấn luyện các mô hình ảnh trên MNIST và Fashion-MNIST", "48"),
        ("Hình 30", "So sánh số tham số trainable của bảy mô hình ảnh", "49"),
        ("Hình 31", "Confusion Matrix của M7 Adapted VGG trên MNIST", "50"),
        ("Hình 32", "Confusion Matrix của M6 Adapted AlexNet trên Fashion-MNIST", "51"),
        ("Hình 33", "Confusion Matrix của M3 Residual trên Diabetes", "52")
    ]
    for f_id, f_desc, f_pg in fig_list:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.space_after = Pt(2)
        p_f.paragraph_format.line_spacing = 1.15
        r_id = p_f.add_run(f"{f_id}. {f_desc}")
        dots_len = max(3, 85 - len(f"{f_id}. {f_desc}"))
        r_dots = p_f.add_run(" " + "." * dots_len + " ")
        r_dots.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
        r_pg = p_f.add_run(f_pg)
        r_pg.bold = True

    add_h1("DANH MỤC BẢNG BIỂU")
    tbl_list = [
        ("Bảng 1", "Tổng kết thông tin 3 tập dữ liệu thực nghiệm", "24"),
        ("Bảng 2", "Đặc tả kiến trúc và không gian tham số 7 mô hình ảnh 2D và 4 mô hình bảng 1D", "34"),
        ("Bảng 3", "Kết quả thực nghiệm trên tập dữ liệu MNIST (7 mô hình)", "36"),
        ("Bảng 4", "Kết quả thực nghiệm trên tập dữ liệu Fashion-MNIST (7 mô hình)", "37"),
        ("Bảng 5", "Kết quả thực nghiệm trên tập dữ liệu Diabetes (4 mô hình Conv1D)", "38"),
        ("Bảng 6", "Chi tiết các độ đo phân loại nâng cao (Accuracy, Precision, Recall, F1)", "39"),
        ("Bảng 7", "Mức cải thiện Accuracy so với mô hình cơ sở M1 Basic CNN", "40")
    ]
    for t_id, t_desc, t_pg in tbl_list:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.line_spacing = 1.15
        r_id = p_t.add_run(f"{t_id}. {t_desc}")
        dots_len = max(3, 85 - len(f"{t_id}. {t_desc}"))
        r_dots = p_t.add_run(" " + "." * dots_len + " ")
        r_dots.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
        r_pg = p_t.add_run(t_pg)
        r_pg.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHƯƠNG 1: GIỚI THIỆU VÀ MỤC TIÊU CỦA ASSIGNMENT 05
    # -------------------------------------------------------------
    add_h1("1. GIỚI THIỆU VÀ MỤC TIÊU CỦA ASSIGNMENT 05")
    
    add_h2("1.1. Bối cảnh nghiên cứu học máy và mạng tích chập")
    add_p("Trong lịch sử phát triển của Trí tuệ Nhân tạo và Thị giác Máy tính, Mạng Nơ-ron Tích chập (Convolutional Neural Network - CNN) đã tạo nên một cuộc cách mạng vượt bậc, thay đổi hoàn toàn cách thức máy tính nhận thức và phân tích dữ liệu không gian. Trước khi CNN trở nên phổ biến, các phương pháp học máy truyền thống (như SVM, Random Forest, hay Mạng Nơ-ron Truyền thẳng Đa tầng MLP) hoàn toàn phụ thuộc vào giai đoạn trích xuất đặc trưng thủ công (hand-crafted features) như SIFT, SURF hay HOG. Quy trình thủ công này không chỉ đòi hỏi sự am hiểu sâu sắc từ chuyên gia miền mà còn gặp phải giới hạn nghiêm trọng: các đặc trưng thủ công không thể tự tối ưu hóa theo hàm mất mát của toàn bộ hệ thống, dẫn đến việc thông tin cấu trúc cục bộ và tính bất biến tịnh tiến (translation invariance) bị suy giảm đáng kể.")
    add_p("Assignment 05 trong học phần Phát triển Hệ thống Thông minh được thiết kế nhằm mục đích đưa người học đi sâu vào bản chất toán học, kiến trúc kỹ thuật và quy trình thực nghiệm đối chuẩn nghiêm ngặt của mạng tích chập. Điểm đặc biệt của bài tập lớn này là việc khảo sát toàn diện quá trình tiến hóa kiến trúc: từ một mạng CNN cơ bản (M1), từng kỹ thuật hiện đại lần lượt được tích hợp và đánh giá độc lập bao gồm Chuẩn hóa theo lô (M2: Batch Normalization), Kết nối phần dư (M3: Residual Skip Connection), và Cơ chế chú ý kênh (M4: Squeeze-and-Excitation Channel Attention). Đồng thời, bài tập đối sánh trực tiếp các kiến trúc cải tiến này với ba cột mốc kinh điển trong lịch sử Deep Learning là LeNet-5 (1998), AlexNet (2012) và VGG (2014) dưới các phiên bản thích nghi chuẩn mực.")

    add_h2("1.2. Mục tiêu kỹ thuật cốt lõi")
    add_p("Báo cáo Assignment 05 được thực hiện nhằm giải quyết các mục tiêu khoa học và kỹ thuật cụ thể sau:")
    add_bullet("Hiểu và biểu diễn mạng CNN dưới lăng kính toán học của Phép hợp các hàm tham số hóa (Function Composition): f(x; θ) = (f_L ∘ f_{L-1} ∘ ... ∘ f_1)(x).")
    add_bullet("Hiện thực hóa chuỗi tiến hóa kiến trúc M1 → M2 → M3 → M4 trên cả miền dữ liệu hình ảnh 2 chiều và miền dữ liệu bảng lâm sàng 1 chiều.")
    add_bullet("Thiết kế và cài đặt ba mô hình cổ điển thích nghi M5 (LeNet), M6 (AlexNet), M7 (VGG) tương thích hoàn hảo với kích thước ảnh 28×28.")
    add_bullet("Triển khai quy trình thực nghiệm đối chuẩn nghiêm ngặt (Controlled Experiments) trên 3 tập dữ liệu độc lập với 18 lượt huấn luyện, áp dụng kỹ thuật lưu trạng thái tối ưu (Validation Checkpointing) nhằm triệt tiêu hoàn toàn hiện tượng overfitting ở epoch cuối.")
    add_bullet("Đánh giá và so sánh đa chiều: không chỉ nhìn vào Accuracy đơn thuần mà phải phân tích toàn diện Test Loss, Precision, Recall, F1-Score, Ma trận nhầm lẫn (Confusion Matrix), cùng với sự đánh đổi về tài nguyên tính toán (Độ phức tạp tham số và Thời gian huấn luyện).")

    add_h2("1.3. Ba tập dữ liệu thực nghiệm")
    add_p("Để kiểm chứng khả năng tổng quát hóa của các kiến trúc, ba tập dữ liệu với đặc tính phân phối hoàn toàn khác biệt được đưa vào thực nghiệm:")
    add_bullet("MNIST: Tập dữ liệu 70,000 ảnh xám kích thước 28×28 chứa chữ số viết tay từ 0 đến 9. Đây là bài toán phân loại chuẩn mực với độ phân tách cao, đóng vai trò là môi trường kiểm tra độ chính xác cơ sở.")
    add_bullet("Fashion-MNIST: Tập dữ liệu 70,000 ảnh xám kích thước 28×28 gồm 10 lớp sản phẩm thời trang của Zalando. Dữ liệu này có độ biến thiên cao về họa tiết, biên dạng và độ bóng, đặt ra thử thách lớn hơn rất nhiều so với MNIST.")
    add_bullet("Pima Indians Diabetes: Tập dữ liệu y tế gồm 768 bệnh nhân với 8 thuộc tính lâm sàng dạng bảng (tuổi, chỉ số BMI, nồng độ glucose máu, huyết áp...). Bài toán yêu cầu phân loại nhị phân nguy cơ mắc tiểu đường, đóng vai trò kiểm chứng tính ứng dụng của phép tích chập 1D (Conv1D) trên dữ liệu bảng.")

    add_h2("1.4. Quy trình thực nghiệm tổng thể")
    add_p("Toàn bộ quy trình thực nghiệm trong Assignment 05 được mô tả trực quan thông qua sơ đồ hệ thống dưới đây:")
    
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_01_overall_workflow.png',
        fig_title='Hình 1. Quy trình thực nghiệm tổng quát của Assignment 05.',
        source='ass5_experiments/plots/fig_01_overall_workflow.png, tương ứng cell pipeline trong notebook.',
        read_guide='Đọc từ trái sang phải theo 3 khối chính: 3 tập dữ liệu đầu vào (MNIST, Fashion-MNIST, Diabetes) -> Các kiến trúc mô hình (7 mô hình 2D và 4 mô hình 1D) -> Quy trình huấn luyện, Validation Checkpoint và đánh giá đối chuẩn.',
        obs='Sơ đồ thể hiện mạch lạc tính thống nhất của đường ống thực nghiệm, liên kết chặt chẽ giữa tiền xử lý dữ liệu, thiết kế mô hình và đánh giá khách quan.',
        explanation='Quy trình đảm bảo mỗi mô hình đều được huấn luyện trong điều kiện kiểm soát (cùng optimizer Adam, cùng learning rate lr=0.001, cùng cơ chế lưu best model state theo validation accuracy). Điều này loại bỏ các yếu tố gây nhiễu bên ngoài khi so sánh.',
        limits='Sơ đồ biểu diễn luồng dữ liệu logic ở mức tổng quát, không phản ánh chi tiết các bước tính toán tensor số học bên trong từng kernel.'
    )

    # -------------------------------------------------------------
    # CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VỀ MẠNG NƠ-RON VÀ CNN
    # -------------------------------------------------------------
    add_h1("2. CƠ SỞ LÝ THUYẾT VỀ MẠNG NƠ-RON VÀ CNN")
    
    add_h2("2.1. Bản chất hàm hợp của mạng nơ-ron sâu")
    add_p("Về mặt bản chất toán học, một mạng nơ-ron sâu không phải là một chiếc hộp đen thần bí, mà là một chuỗi liên tiếp các phép toán ánh xạ phi tuyến được tham số hóa, hay chính là một hàm hợp phức hợp (Function Composition). Cho một véc-tơ hoặc ma trận đầu vào x thuộc không gian R^d, đầu ra dự đoán y_hat của một mạng có L tầng được biểu diễn dưới dạng:")
    add_p("y_hat = f(x; θ) = (f_L ∘ f_{L-1} ∘ ... ∘ f_1)(x) = f_L(f_{L-1}(...f_1(x; W_1, b_1)...; W_{L-1}, b_{L-1}); W_L, b_L)", indent=False)
    add_p("Trong đó, mỗi tầng l thực hiện một phép biến đổi affine kết hợp với một hàm kích hoạt phi tuyến σ: z_l = σ(W_l * z_{l-1} + b_l). Tập hợp tất cả các ma trận trọng số và véc-tơ độ lệch θ = {W_1, b_1, ..., W_L, b_L} tạo nên không gian tham số của mô hình. Quá trình học tập (learning) thực chất là quá trình tìm kiếm một điểm tối ưu θ* trong không gian tham số nhằm cực tiểu hóa một hàm mất mát L(y, y_hat) trên toàn bộ tập dữ liệu huấn luyện.")

    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_02_function_composition.png',
        fig_title='Hình 2. CNN được nhìn như một hàm hợp của nhiều phép biến đổi.',
        source='ass5_experiments/plots/fig_02_function_composition.png, minh họa trực quan khái niệm Function Composition.',
        read_guide='Quan sát dòng chảy thông tin từ trái sang phải: Dữ liệu x ban đầu được truyền qua tầng tích chập f1, phi tuyến f2, giảm chiều f3 và phân lớp f4 để tạo ra logit đầu ra.',
        obs='Mỗi khối chức năng đại diện cho một phép biến đổi hình học trong không gian nhiều chiều, chuyển đổi dần các đặc trưng thô thành các biểu diễn trừu tượng.',
        explanation='Góc nhìn hàm hợp cho thấy rõ tính phân cấp: tầng đầu nắm bắt các chi tiết cục bộ (cạnh, góc, texture), các tầng sâu hơn tổng hợp thành các bộ phận và cấu trúc ngữ nghĩa hoàn chỉnh.',
        limits='Hình vẽ minh họa 4 khối tượng trưng, trên thực tế số tầng của mạng nơ-ron sâu có thể lên tới hàng chục hoặc hàng trăm tầng.'
    )

    add_h2("2.2. Trích xuất đặc trưng tự động và học biểu diễn")
    add_p("Sự khác biệt căn bản giữa Mạng Nơ-ron Truyền thẳng (MLP) và Mạng Nơ-ron Tích chập (CNN) nằm ở hai đặc tính hình học quan trọng: Tính cục bộ không gian (Spatial Locality) và Tính bất biến tịnh tiến (Translation Equivariance / Invariance).")
    add_p("Trong MLP, ma trận trọng số kết nối mọi nơ-ron đầu vào với mọi nơ-ron đầu ra. Khi áp dụng lên ảnh 2D, ta buộc phải kéo phẳng (flatten) ảnh thành véc-tơ 1 chiều, hành động này phá vỡ hoàn toàn mối liên hệ không gian giữa các điểm ảnh lân cận. Ngược lại, lớp tích chập duy trì cấu trúc không gian 2D bằng cách chỉ áp dụng các bộ lọc có kích thước nhỏ (ví dụ 3×3, 5×5) trượt trên toàn bộ ảnh. Điều này mang lại hai lợi ích vô cùng to lớn: Thứ nhất, chia sẻ trọng số (Weight Sharing) giúp giảm hàng nghìn lần số lượng tham số cần học. Thứ hai, tính tương đương tịnh tiến bảo đảm rằng nếu một cạnh hay một đặc trưng xuất hiện ở bất kỳ vị trí nào trên ảnh, bộ lọc đều có thể nhận diện chính xác.")

    add_h2("2.3. Cấu trúc một lớp Convolutional")
    add_p("Một lớp tích chập chuẩn mực nhận đầu vào là một tensor bậc 3 kích thước (C_in, H_in, W_in), trong đó C_in là số kênh (channels), H_in và W_in là chiều cao và chiều rộng của bản đồ đặc trưng (feature map). Lớp này được trang bị C_out bộ lọc, mỗi bộ lọc có kích thước (C_in, K_h, K_w). Khi thực hiện phép tích chập, mỗi bộ lọc sẽ trượt trên toàn bộ không gian của đầu vào để sinh ra một kênh đặc trưng mới trong tensor đầu ra có kích thước (C_out, H_out, W_out).")

    add_h2("2.4. Phép toán tích chập và bản chất nhân ma trận")
    add_p("Về mặt giải tích, phép tích chập rời rạc 2 chiều tại tọa độ (i, j) của kênh đầu ra thứ c được định nghĩa như sau:")
    add_p("Y_{c, i, j} = b_c + ∑_{k=0}^{C_in - 1} ∑_{u=0}^{K_h - 1} ∑_{v=0}^{K_w - 1} X_{k, i*s + u, j*s + v} * W_{c, k, u, v}", indent=False)
    add_p("Trong đó W_{c, k, u, v} là trọng số của bộ lọc thứ c tại vị trí (u, v) trên kênh thứ k, b_c là độ lệch tương ứng, và s là bước nhảy trượt (stride). Trong thực tế tính toán hiệu năng cao (như thư viện cuDNN của PyTorch), phép toán này được chuyển đổi thành phép nhân ma trận tổng quát (GEMM - General Matrix Multiply) thông qua thuật toán im2col, giúp tận dụng tối đa năng lực xử lý song song của GPU/CPU.")

    add_h2("2.5. Kích thước Kernel (Kernel Size)")
    add_p("Kích thước bộ lọc (Kernel Size K) quyết định phạm vi không gian mà mỗi nơ-ron có thể quan sát trong một bước tính toán. Xu hướng thiết kế hiện đại (bắt nguồn từ kiến trúc VGG) ưu tiên sử dụng các bộ lọc nhỏ 3×3 thay vì các bộ lọc lớn 5×5 hay 7×7. Lý do là việc xếp chồng liên tiếp hai lớp tích chập 3×3 có cùng vùng cảm nhận hữu hiệu (effective receptive field) là 5×5 (vì 3 + 3 - 1 = 5), nhưng số lượng tham số chỉ là 2 * (3×3) = 18 trọng số, so với 1 * (5×5) = 25 trọng số (tiết kiệm 28% tham số), đồng thời cho phép tích hợp hai lần hàm kích hoạt phi tuyến giúp mô hình có tính biểu đạt cao hơn.")

    add_h2("2.6. Bước nhảy trượt (Stride)")
    add_p("Bước nhảy trượt s (Stride) là khoảng cách dịch chuyển của bộ lọc sau mỗi lần tính toán tích chập. Khi s = 1, bộ lọc trượt qua từng điểm ảnh liên tiếp, giữ lại chi tiết không gian tối đa. Khi s > 1 (ví dụ s = 2), bộ lọc bỏ qua các điểm ảnh trung gian, làm giảm kích thước bản đồ đặc trưng xuống xấp xỉ một nửa. Kỹ thuật này thường được dùng thay thế cho các tầng gộp pooling trong các kiến trúc CNN hiện đại.")

    add_h2("2.7. Cơ chế đệm viền (Padding)")
    add_p("Khi một bộ lọc trượt qua ảnh, các điểm ảnh ở rìa ảnh được tham gia tính toán ít lần hơn so với các điểm ảnh ở trung tâm, dẫn đến việc kích thước ảnh bị thu hẹp dần sau mỗi lớp tích chập. Cơ chế đệm viền (Padding p) giải quyết vấn đề này bằng cách bổ sung thêm các hàng và cột có giá trị 0 (Zero-padding) xung quanh biên của ảnh. Công thức tổng quát xác định kích thước không gian đầu ra là:")
    add_p("H_out = ⌊ (H_in + 2*p - K_h) / s ⌋ + 1,    W_out = ⌊ (W_in + 2*p - K_w) / s ⌋ + 1", indent=False)
    add_p("Khi chọn K = 3, s = 1 và p = 1 (còn gọi là Same Padding), ta luôn có H_out = H_in và W_out = W_in, bảo toàn trọn vẹn kích thước không gian của bản đồ đặc trưng qua các lớp tích chập.")

    add_h2("2.8. Vùng cảm nhận không gian (Receptive Field)")
    add_p("Vùng cảm nhận (Receptive Field - RF) là phạm vi không gian trên ảnh đầu vào có ảnh hưởng trực tiếp đến giá trị của một nơ-ron cụ thể ở tầng sâu. Qua mỗi tầng tích chập hoặc pooling, vùng cảm nhận tăng dần theo công thức đệ quy:")
    add_p("RF_l = RF_{l-1} + (K_l - 1) * S_{l-1}", indent=False)
    add_p("Trong đó S_{l-1} là tích các bước nhảy trượt của tất cả các tầng trước đó. Một mạng CNN có cấu trúc đủ sâu sẽ có vùng cảm nhận bao trùm toàn bộ bức ảnh, cho phép các tầng phân loại cuối cùng đưa ra quyết định dựa trên mối tương quan toàn cục của mọi chi tiết trong ảnh.")

    add_h2("2.9. Hàm kích hoạt phi tuyến (Activation Functions)")
    add_p("Nếu không có hàm kích hoạt phi tuyến, một mạng nơ-ron sâu dù có bao nhiêu tầng cũng chỉ tương đương với một phép biến đổi affine tuyến tính đơn lẻ. Hàm kích hoạt ReLU (Rectified Linear Unit), được định nghĩa là f(x) = max(0, x), là tiêu chuẩn vàng trong các mạng CNN hiện đại nhờ hai ưu điểm vượt trội: Thứ nhất, đạo hàm của nó bằng 1 cho mọi giá trị x > 0, giúp triệt tiêu hoàn toàn hiện tượng triệt tiêu gradient (Vanishing Gradient) vốn là căn bệnh kinh niên của hàm Sigmoid hay Tanh. Thứ hai, phép tính max(0, x) cực kỳ đơn giản về mặt phần cứng, giúp tăng tốc độ huấn luyện lên nhiều lần.")

    add_h2("2.10. Tầng gộp giảm chiều (Pooling Layers)")
    add_p("Tầng gộp (Pooling) thực hiện phép tổng hợp thống kê không gian cục bộ nhằm giảm độ phân giải của bản đồ đặc trưng, từ đó giảm chi phí tính toán và số lượng tham số cho các tầng phía sau. Phổ biến nhất là Max Pooling (chọn giá trị lớn nhất trong cửa sổ k×k), giúp giữ lại các tín hiệu kích hoạt mạnh nhất và tạo ra tính bất biến nhẹ đối với các phép dịch chuyển nhỏ. Ngoài ra, Average Pooling (lấy trung bình cộng) thường được áp dụng ở tầng cuối dưới dạng Global Average Pooling để làm phẳng đặc trưng mà không cần quá nhiều tham số kết nối.")

    add_h2("2.11. Tầng kết nối đầy đủ (Fully Connected / Dense Layer)")
    add_p("Sau khi bản đồ đặc trưng đã được trích xuất qua chuỗi các tầng tích chập và gộp, tensor nhiều chiều được duỗi thẳng (flatten) thành một véc-tơ một chiều để đưa vào các tầng kết nối đầy đủ (Fully Connected - FC). Tầng FC đóng vai trò như một bộ phân loại phi tuyến tổng hợp các đặc trưng trừu tượng toàn cục và ánh xạ chúng sang số chiều bằng đúng số lớp cần phân loại (logits).")

    add_h2("2.12. Lan truyền ngược và thuật toán cập nhật Adam")
    add_p("Quá trình huấn luyện sử dụng thuật toán lan truyền ngược (Backpropagation) dựa trên quy tắc dây chuyền vi tích phân để tính gradient của hàm mất mát đối với từng trọng số:")
    add_p("∂L / ∂W_l = (∂L / ∂z_l) * (∂z_l / ∂W_l)", indent=False)
    add_p("Thuật toán tối ưu Adam (Adaptive Moment Estimation) được sử dụng trong suốt bài thực hành này. Adam kết hợp ưu điểm của cả Momentum (tính trung bình trượt có trọng số của gradient bậc nhất m_t) và RMSprop (chia cho căn bậc hai của trung bình trượt gradient bậc hai v_t), giúp các bước cập nhật trọng số thích nghi linh hoạt theo từng chiều tham số, tăng tốc hội tụ và hạn chế sa vào các điểm yên ngựa (saddle points).")

    # -------------------------------------------------------------
    # CHƯƠNG 3: SỰ PHÁT TRIỂN CỦA CÁC KIẾN TRÚC CNN KINH ĐIỂN
    # -------------------------------------------------------------
    add_h1("3. SỰ PHÁT TRIỂN CỦA CÁC KIẾN TRÚC CNN KINH ĐIỂN")
    
    add_h2("3.1. LeNet-5 (1998)")
    add_p("Được phát triển bởi Yann LeCun và các cộng sự vào năm 1998, LeNet-5 là kiến trúc CNN tiên phong chứng minh tính khả thi của mạng tích chập trong việc nhận dạng chữ số viết tay trên séc ngân hàng. Cấu trúc kinh điển của LeNet-5 bao gồm hai khối [Conv - AvgPool] xen kẽ với ba tầng Fully Connected. Ở thời điểm đó, do hạn chế về phần cứng và dữ liệu, LeNet-5 sử dụng hàm kích hoạt Sigmoid/Tanh và Average Pooling với số lượng tham số khiêm tốn khoảng 44 nghìn tham số. Trong Assignment 05, LeNet được tái hiện dưới phiên bản thích nghi hiện đại sử dụng ReLU để đối chuẩn trực tiếp.")

    add_h2("3.2. AlexNet (2012)")
    add_p("Chiến thắng áp đảo của Alex Krizhevsky, Ilya Sutskever và Geoffrey Hinton tại cuộc thi ImageNet 2012 với kiến trúc AlexNet đã đánh dấu bước ngoặt lịch sử mở ra kỷ nguyên bùng nổ của Deep Learning. AlexNet đã chứng minh tính hiệu quả vượt bậc của ba yếu tố kỹ thuật then chốt: (1) Sử dụng hàm kích hoạt ReLU thay thế cho Tanh giúp huấn luyện nhanh gấp 6 lần; (2) Kỹ thuật Dropout (tỷ lệ 0.5) ở các tầng FC để ngăn ngừa overfitting; và (3) Khai thác sức mạnh tính toán song song của card đồ họa GPU.")

    add_h2("3.3. VGG Network (2014)")
    add_p("Nhóm Visual Geometry Group (VGG) thuộc Đại học Oxford đã đề xuất một nguyên lý thiết kế mang tính chuẩn mực vào năm 2014: Thay vì sử dụng các bộ lọc có kích thước đa dạng và phức tạp, toàn bộ mạng VGG chỉ sử dụng đồng nhất các bộ lọc kích thước nhỏ 3×3 với stride 1 và padding 1, kết hợp với các tầng MaxPool 2×2 để thu nhỏ kích thước không gian. Kiến trúc VGG (như VGG-16, VGG-19) cho thấy rằng việc gia tăng độ sâu của mạng bằng cách xếp chồng các lớp tích chập nhỏ sẽ mang lại khả năng trích xuất đặc trưng vượt trội hơn hẳn so với việc sử dụng các bộ lọc lớn.")

    add_h2("3.4. ResNet (2015)")
    add_p("Khi các nhà nghiên cứu cố gắng xây dựng các mạng CNN sâu hơn (trên 20 tầng), họ vấp phải một rào cản nghiêm trọng gọi là Vấn đề suy thoái mạng (Degradation Problem): khi mạng càng sâu, độ chính xác không những không tăng mà còn bão hòa và sụt giảm nhanh chóng, nguyên nhân là do gradient bị triệt tiêu hoặc bùng nổ khi lan truyền qua quá nhiều tầng. Kaiming He và các cộng sự đã giải quyết triệt để vấn đề này với kiến trúc ResNet (Residual Network) năm 2015 thông qua kỹ thuật Kết nối tắt (Skip Connection / Residual Connection). Thay vì bắt các tầng nơ-ron học ánh xạ mục tiêu H(x), ResNet tái định nghĩa bài toán để các tầng học phần dư F(x) = H(x) - x, dẫn đến đầu ra H(x) = F(x) + x. Cơ chế này tạo ra một đường cao tốc cho gradient lan truyền thẳng về các tầng đầu mà không bị suy giảm, mở đường cho việc xây dựng các mạng siêu sâu lên tới 152 hay thậm chí 1000 tầng.")

    add_h2("3.5. MobileNet và các kiến trúc hiện đại")
    add_p("Bên cạnh việc chạy đua về độ sâu và độ chính xác, nhu cầu triển khai mô hình học sâu trên các thiết bị di động và thiết bị nhúng với tài nguyên hạn chế đã thúc đẩy sự ra đời của các kiến trúc tối ưu hóa như MobileNet (sử dụng Depthwise Separable Convolution), DenseNet (kết nối mọi tầng với mọi tầng tiếp theo) và EfficientNet (áp dụng Compound Scaling để cân bằng đồng thời độ sâu, độ rộng và độ phân giải ảnh).")

    # -------------------------------------------------------------
    # CHƯƠNG 4: CƠ SỞ LÝ THUYẾT VỀ CÁC KỸ THUẬT CẢI TIẾN CNN
    # -------------------------------------------------------------
    add_h1("4. CƠ SỞ LÝ THUYẾT VỀ CÁC KỸ THUẬT CẢI TIẾN CNN")
    
    add_h2("4.1. Giới hạn cố hữu của Basic CNN")
    add_p("Mô hình Basic CNN (M1) được xây dựng theo lối tiếp cận cổ điển: các tầng Conv2d, ReLU và MaxPool2d được xếp chồng tuần tự. Dù đơn giản và dễ hiểu, mô hình này bộc lộ ba điểm yếu kỹ thuật cơ bản:")
    add_bullet("Hiện tượng dịch chuyển đồng biến nội tại (Internal Covariate Shift): Khi các trọng số ở tầng trước thay đổi qua các bước gradient, phân phối đầu vào của các tầng sau liên tục bị biến động, khiến tốc độ học bị chậm lại đáng kể.")
    add_bullet("Tắc nghẽn thông tin gradient: Khi độ sâu mạng tăng lên, gradient truyền ngược qua các phép nhân ma trận liên tiếp dễ bị suy giảm, cản trở việc tối ưu hóa các tầng phía dưới.")
    add_bullet("Xử lý bình đẳng mọi kênh đặc trưng: Lớp tích chập chuẩn gán trọng số đồng đều cho mọi kênh bản đồ đặc trưng, không có cơ chế tự thích nghi để tăng cường các kênh chứa thông tin quan trọng và ức chế các kênh nhiễu.")

    add_h2("4.2. Chuẩn hóa theo lô (Batch Normalization)")
    add_p("Được đề xuất bởi Sergey Ioffe và Christian Szegedy (2015), Chuẩn hóa theo lô (Batch Normalization - BN) là một trong những cải tiến mang tính đột phá nhất trong lịch sử học sâu. Trong quá trình huấn luyện, BN chuẩn hóa từng kênh đặc trưng của một mini-batch B = {x_1, ..., x_m} về phân phối chuẩn có kỳ vọng bằng 0 và phương sai bằng 1 theo các bước toán học:")
    add_p("μ_B = (1/m) * ∑_{i=1}^m x_i", indent=False)
    add_p("σ_B^2 = (1/m) * ∑_{i=1}^m (x_i - μ_B)^2", indent=False)
    add_p("x_hat_i = (x_i - μ_B) / √(σ_B^2 + ϵ)", indent=False)
    add_p("y_i = γ * x_hat_i + β = BN_{γ, β}(x_i)", indent=False)
    add_p("Trong đó γ (scale) và β (shift) là hai tham số có thể học được (trainable parameters), cho phép mạng tự phục hồi lại biểu diễn ban đầu nếu việc chuẩn hóa làm mất mát thông tin. Lợi ích của BN bao gồm: (1) Ổn định dòng gradient, cho phép sử dụng learning rate lớn hơn; (2) Giảm sự phụ thuộc khắt khe vào việc khởi tạo trọng số ban đầu; và (3) Đóng vai trò như một kỹ thuật điều hòa nhẹ (regularization), giúp giảm bớt nhu cầu sử dụng Dropout.")

    add_h2("4.3. Kết nối phần dư (Residual Connection / Skip Connection)")
    add_p("Kỹ thuật kết nối phần dư (Residual Connection) cho phép tín hiệu đầu vào x của một khối được cộng trực tiếp vào đầu ra biến đổi F(x) thông qua một nhánh tắt (Identity Shortcut):")
    add_p("y = F(x, {W_i}) + x", indent=False)
    add_p("Về mặt đạo hàm, gradient của hàm mất mát L đối với đầu vào x có dạng:")
    add_p("∂L / ∂x = (∂L / ∂y) * (∂F / ∂x + 1) = (∂L / ∂y) * (∂F / ∂x) + (∂L / ∂y)", indent=False)
    add_p("Thành phần '+ 1' chính là điểm mấu chốt toán học: ngay cả khi gradient của nhánh biến đổi (∂F / ∂x) tiến về 0 (triệt tiêu gradient), tín hiệu gradient từ tầng trên (∂L / ∂y) vẫn được truyền nguyên vẹn ngược về các tầng dưới thông qua nhánh identity. Điều này bảo đảm rằng mô hình dư thừa luôn hoạt động tối thiểu bằng một hàm đồng nhất, triệt tiêu hoàn toàn hiện tượng suy thoái mạng.")

    add_h2("4.4. Cơ chế chú ý kênh (Channel Attention / Squeeze-and-Excitation)")
    add_p("Khối Squeeze-and-Excitation (SE-Block), do Jie Hu và các cộng sự giới thiệu (đoạt giải nhất ILSVRC 2017), bổ sung cơ chế chú ý kênh (Channel Attention) cho mạng CNN bằng cách tường minh hóa mối tương quan phụ thuộc giữa các kênh đặc trưng. Khối SE bao gồm hai giai đoạn tính toán:")
    add_bullet("Giai đoạn Ép (Squeeze): Nén toàn bộ thông tin không gian H×W của từng kênh c thành một giá trị vô hướng biểu diễn bối cảnh toàn cục thông qua phép gộp trung bình toàn cục (Global Average Pooling): z_c = (1 / (H*W)) * ∑_{i=1}^H ∑_{j=1}^W u_c(i, j).")
    add_bullet("Giai đoạn Kích thích (Excitation): Sử dụng một mạng nơ-ron nhỏ gồm hai tầng Fully Connected với hệ số co hẹp r (reduction ratio = 4) kết hợp hàm ReLU và Sigmoid để sinh ra trọng số chú ý cho từng kênh: s = σ(W_2 * δ(W_1 * z)).")
    add_bullet("Tái cân chỉnh (Scale): Nhân từng bản đồ đặc trưng u_c với hệ số chú ý s_c tương ứng: x_tilde_c = s_c * u_c. Nhờ đó, mạng tự động tập trung tài nguyên vào các đặc trưng ngữ nghĩa quan trọng và bỏ qua các đặc trưng nhiễu.")

    add_h2("4.5. Phân tích so sánh chuỗi cấu trúc cải tiến M1 – M4")
    add_p("Chuỗi mô hình từ M1 đến M4 thể hiện một quy trình tiến hóa kiến trúc vô cùng chặt chẽ và logic:")
    add_bullet("M1 (Basic CNN): Đường cơ sở tuần tự [Conv - ReLU - MaxPool].")
    add_bullet("M2 (BatchNorm CNN): Tích hợp BatchNorm2d sau mỗi lớp Conv2d, ổn định dòng gradient và tăng tốc độ hội tụ.")
    add_bullet("M3 (Residual CNN): Tích hợp khối ResBlock2D với 2 lớp Conv2d và kết nối tắt Identity, gia cố khả năng bảo toàn thông tin sâu.")
    add_bullet("M4 (Attention CNN): Tích hợp khối SEBlock2D ngay sau ResBlock2D, bổ sung năng lực tự động cân chỉnh trọng số giữa các kênh.")

    add_h2("4.6. Mở rộng phép tích chập Conv1D cho dữ liệu dạng bảng")
    add_p("Một đóng góp học thuật nổi bật của Assignment 05 là việc mở rộng các nguyên lý tích chập sang dữ liệu bảng 1 chiều (1D Tabular Data). Trong bài toán Diabetes với 8 đặc trưng lâm sàng, mỗi mẫu bệnh nhân được biểu diễn dưới dạng tensor 3 chiều kích thước (Batch_Size, 1, 8), trong đó số kênh in_channels = 1 và độ dài chuỗi length = 8. Phép tích chập 1D (Conv1d) với kernel size = 3 và padding = 1 sẽ trượt dọc theo chuỗi 8 đặc trưng để học các mối tương quan cục bộ giữa các biến số lâm sàng liền kề. Toàn bộ các cơ chế BatchNorm1d, ResBlock1D và SEBlock1D đều được ánh xạ tương ứng sang không gian 1 chiều, tạo nên một hệ thống đối sánh hoàn hảo.")

    add_h2("4.7. So sánh các mô hình cổ điển thích nghi")
    add_p("Bên cạnh chuỗi M1 - M4, ba mô hình cổ điển thích nghi được đưa vào đối chuẩn:")
    add_bullet("M5 (Adapted LeNet): 2 lớp Conv (kernel 5×5) + 3 lớp FC. Nhẹ nhất về số lượng tham số nhưng có thể gặp hạn chế về tính biểu đạt trên dữ liệu khó.")
    add_bullet("M6 (Adapted AlexNet): 3 lớp Conv (kernel 3×3, kênh tăng dần 32→64→128) + 2 lớp FC lớn kết hợp Dropout(0.5). Không gian tham số lên tới 1.7 triệu trọng số, đại diện cho mô hình dung lượng lớn (High-Capacity).")
    add_bullet("M7 (Adapted VGG): Áp dụng nguyên lý khối tích chập kép [Conv-Conv-Pool] liên tiếp với 4 lớp Conv2d 3×3 + 2 lớp FC kết hợp Dropout(0.5). Khoảng 467 nghìn tham số, đại diện cho thiết kế cấu trúc sâu và đồng nhất.")

    # -------------------------------------------------------------
    # CHƯƠNG 5: DỮ LIỆU VÀ BÀI TOÁN THỰC NGHIỆM
    # -------------------------------------------------------------
    add_h1("5. DỮ LIỆU VÀ BÀI TOÁN THỰC NGHIỆM")
    
    add_h2("5.1. Giới thiệu 3 bài toán nghiên cứu")
    add_p("Để bảo đảm tính khách quan và khoa học của kết luận, Assignment 05 tiến hành khảo nghiệm trên 3 bài toán phân loại độc lập:")
    add_bullet("Bài toán 1: Nhận dạng chữ số viết tay trên tập dữ liệu MNIST (10 lớp, ảnh xám 28×28).")
    add_bullet("Bài toán 2: Phân loại sản phẩm thời trang trên tập dữ liệu Fashion-MNIST (10 lớp, ảnh xám 28×28).")
    add_bullet("Bài toán 3: Dự đoán nguy cơ mắc bệnh tiểu đường trên tập dữ liệu Pima Indians Diabetes (Nhị phân 0-1, dữ liệu bảng 8 chiều).")

    add_h2("5.2. Tập dữ liệu MNIST")
    add_p("Tập dữ liệu MNIST bao gồm 60,000 ảnh huấn luyện và 10,000 ảnh kiểm thử của các chữ số từ 0 đến 9 do Viện Tiêu chuẩn và Công nghệ Quốc gia Hoa Kỳ (NIST) chuẩn hóa. Các điểm ảnh có giá trị độ sáng từ 0 (nền đen) đến 255 (nét chữ trắng).")

    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_03_mnist_samples.png',
        fig_title='Hình 3. Một số mẫu ảnh MNIST được trực quan hóa trong quá trình chuẩn bị dữ liệu.',
        source='ass5_experiments/plots/fig_03_mnist_samples.png, trích xuất trực tiếp từ DataLoader của MNIST trong notebook.',
        read_guide='Mỗi ô vuông hiển thị một ảnh xám 28x28 tương ứng với một chữ số viết tay từ lớp 0 đến lớp 9 kèm nhãn lớp ở tiêu đề.',
        obs='Các chữ số có nét viết rõ ràng, độ tương phản cao, nền đen đồng nhất và đối tượng nằm trọn vẹn ở vùng trung tâm ảnh.',
        explanation='Đặc điểm phân phối chuẩn mực này giải thích vì sao hầu hết các mô hình CNN đều đạt độ chính xác rất cao (>98.5%) trên MNIST, khiến dư địa cải thiện giữa các kiến trúc tương đối hẹp.',
        limits='Ảnh mẫu chỉ đại diện cho các trường hợp viết chuẩn; trong thực tế chữ số viết tay có thể bị nghiêng, mờ hoặc đứt nét.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_04_mnist_dataloader.png',
        fig_title='Hình 4. DataLoader của MNIST và kích thước batch.',
        source='Cell [3] trong executed notebook A05_06_taint_731.ipynb, phần khởi tạo DataLoader cho MNIST.',
        read_guide='Đọc mã nguồn khởi tạo transforms.Compose, random_split và DataLoader với batch_size=64 cho train và 1000 cho val/test.',
        obs='Mã lệnh thiết lập rõ ràng hạt giống ngẫu nhiên SEED=42 để bảo đảm tính tái lập, phân chia 54,000 mẫu train, 6,000 mẫu validation và 10,000 mẫu test.',
        explanation='Việc chuẩn hóa mean=0.1307 và std=0.3081 đưa dữ liệu về thang đo chuẩn, hỗ trợ thuật toán Adam hội tụ nhanh và ổn định.',
        limits='Ảnh chụp trực tiếp từ môi trường thực thi Jupyter notebook của sinh viên Nguyễn Tuấn Tài.'
    )

    add_h2("5.3. Tập dữ liệu Fashion-MNIST")
    add_p("Fashion-MNIST được tạo ra bởi phòng nghiên cứu của Zalando vào năm 2017 nhằm thay thế trực tiếp cho MNIST vốn đã trở nên quá dễ đối với các thuật toán hiện đại. Tập dữ liệu gồm 70,000 ảnh xám 28×28 thuộc 10 lớp mặt hàng: T-shirt/top, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, Ankle boot.")

    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_05_fashion_mnist_samples.png',
        fig_title='Hình 5. Một số mẫu Fashion-MNIST được trực quan hóa.',
        source='ass5_experiments/plots/fig_05_fashion_mnist_samples.png, sinh từ tập dữ liệu thật của Fashion-MNIST.',
        read_guide='Quan sát 10 sản phẩm thời trang đại diện cho 10 lớp phân loại kèm tên gọi tiếng Anh và chỉ số lớp tương ứng.',
        obs='Các lớp có sự tương đồng hình học rất lớn: ví dụ T-shirt (lớp 0), Pullover (lớp 2), Coat (lớp 4) và Shirt (lớp 6) đều có biên dạng áo dài/ngắn tay rất dễ nhầm lẫn.',
        explanation='Độ phức tạp hình thái và sự đa dạng về hoa văn khiến Fashion-MNIST trở thành thước đo lý tưởng để kiểm chứng sự vượt trội của các kiến trúc CNN cải tiến so với mô hình cơ sở.',
        limits='Kích thước 28x28 giới hạn độ phân giải của các chi tiết nhỏ như cúc áo, cổ áo hoặc khóa kéo.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_06_fashion_mnist_split.png',
        fig_title='Hình 6. Phân chia Training / Validation / Test của Fashion-MNIST.',
        source='Cell [4] trong executed notebook A05_06_taint_731.ipynb, phần chuẩn bị dữ liệu Fashion-MNIST.',
        read_guide='Đọc các dòng lệnh áp dụng transforms với mean=0.2860, std=0.3530 và phân chia tỷ lệ tập dữ liệu tương tự MNIST.',
        obs='Output hiển thị chính xác số lượng mẫu: 54,000 mẫu train, 6,000 mẫu val và 10,000 mẫu test.',
        explanation='Thiết lập đồng nhất về kích thước tập dữ liệu giữa MNIST và Fashion-MNIST giúp việc so sánh thời gian huấn luyện và độ phức tạp đạt tính khách quan khoa học cao nhất.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_h2("5.4. Tập dữ liệu Bệnh tiểu đường Pima Indians Diabetes")
    add_p("Tập dữ liệu Diabetes từ Viện Quốc gia về Bệnh Tiểu đường, Tiêu hóa và Bệnh Thận Hoa Kỳ (NIDDK) bao gồm hồ sơ bệnh án của 768 nữ bệnh nhân người da đỏ Pima từ 21 tuổi trở lên. Mục tiêu là dự đoán biến Outcome (0: Không mắc bệnh, 1: Mắc bệnh tiểu đường). 8 biến đầu vào bao gồm:")
    add_bullet("Pregnancies: Số lần mang thai.")
    add_bullet("Glucose: Nồng độ đường huyết sau 2 giờ làm nghiệm pháp dung nạp glucose.")
    add_bullet("BloodPressure: Huyết áp tâm trương (mm Hg).")
    add_bullet("SkinThickness: Độ dày nếp gấp da cơ tam đầu (mm).")
    add_bullet("Insulin: Nồng độ insulin huyết thanh sau 2 giờ (mu U/ml).")
    add_bullet("BMI: Chỉ số khối cơ thể (cân nặng tính bằng kg / (chiều cao tính bằng m)^2).")
    add_bullet("DiabetesPedigreeFunction: Điểm số tiền sử gia đình mắc bệnh tiểu đường.")
    add_bullet("Age: Tuổi của bệnh nhân (năm).")

    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_07_diabetes_distribution.png',
        fig_title='Hình 7. Phân bố hai lớp Outcome của Diabetes.',
        source='ass5_experiments/plots/fig_07_diabetes_distribution.png, trích xuất từ dữ liệu lâm sàng thật.',
        read_guide='Biểu đồ cột so sánh số lượng và tỷ lệ phần trăm giữa hai lớp Outcome: Không tiểu đường (0) và Mắc tiểu đường (1).',
        obs='Dữ liệu mất cân bằng rõ rệt: Lớp 0 chiếm 500 mẫu (65.1%), trong khi Lớp 1 chỉ có 268 mẫu (34.9%).',
        explanation='Hiện tượng mất cân bằng lớp (Class Imbalance) là đặc trưng cố hữu của dữ liệu y tế. Điều này đòi hỏi mô hình không chỉ quan tâm đến Accuracy mà phải theo dõi sát sao Precision, Recall và F1-Score để tránh báo động giả hoặc bỏ sót ca bệnh nguy hiểm.',
        limits='Quy mô 768 mẫu tương đối khiêm tốn so với chuẩn dữ liệu của học sâu hiện đại.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_08_diabetes_zero_handling.png',
        fig_title='Hình 8. Xử lý giá trị 0 sinh lý bất thường trong Diabetes.',
        source='Cell [5] trong executed notebook A05_06_taint_731.ipynb, phần tiền xử lý dữ liệu bảng lâm sàng.',
        read_guide='Đọc khối mã thay thế các giá trị 0 phi lý sinh học (ở các cột Glucose, BloodPressure, SkinThickness, Insulin, BMI) bằng giá trị trung vị (median) theo từng lớp.',
        obs='Mã lệnh kiểm tra cẩn thận các giá trị bất thường trước khi thực hiện chuẩn hóa StandardScale.',
        explanation='Trong y học, các chỉ số như nồng độ Glucose hay Huyết áp bằng 0 là không thể tồn tại ở người sống; đây là các giá trị bị khuyết (missing values) được mã hóa thành 0 khi nhập liệu. Xử lý bằng median theo từng nhãn giúp bảo toàn tính phân phối sinh học mà không gây rò rỉ dữ liệu (data leakage).',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_h2("5.5. Chiến lược phân chia dữ liệu Train / Validation / Test")
    add_p("Để đảm bảo việc đánh giá không bị sai lệch (data snooping), chiến lược phân chia dữ liệu được thiết lập chặt chẽ:")
    add_bullet("Với MNIST và Fashion-MNIST: Tập huấn luyện ban đầu (60,000 ảnh) được chia thành 54,000 ảnh train (90%) và 6,000 ảnh validation (10%). Tập kiểm thử chuẩn gồm 10,000 ảnh test hoàn toàn độc lập chỉ được dùng một lần duy nhất ở bước đánh giá cuối cùng.")
    add_bullet("Với Diabetes: 768 mẫu được phân chia theo tỷ lệ phân tầng (Stratified Split) thành: 537 mẫu train (70%), 115 mẫu validation (15%), và 116 mẫu test (15%). Việc phân tầng bảo đảm tỷ lệ giữa hai lớp 0 và 1 đồng nhất trên cả ba tập.")

    add_h2("5.6. Tiền xử lý dữ liệu và chuẩn hóa thang đo")
    add_p("Với dữ liệu ảnh, các giá trị điểm ảnh [0, 255] được chuyển sang tensor số thực trong đoạn [0.0, 1.0] và chuẩn hóa Z-score: X_norm = (X - mean) / std. Cụ thể, MNIST sử dụng mean=0.1307, std=0.3081; Fashion-MNIST sử dụng mean=0.2860, std=0.3530. Với Diabetes, các đặc trưng được chuẩn hóa bằng StandardScaler huấn luyện trên tập train để có kỳ vọng 0 và phương sai 1.")

    add_h2("5.7. Xây dựng PyTorch DataLoader")
    add_p("Dữ liệu sau khi tiền xử lý được đóng gói vào các đối tượng TensorDataset và DataLoader của PyTorch với tham số shuffle=True cho tập train nhằm xáo trộn ngẫu nhiên thứ tự các mẫu ở mỗi epoch, triệt tiêu sự phụ thuộc thứ tự. Kích thước batch được cấu hình tối ưu: batch_size=64 cho dữ liệu ảnh và batch_size=32 cho dữ liệu bảng.")

    add_h2("5.8. Bảng tổng kết dữ liệu thực nghiệm")
    add_p("Bảng 1 tổng kết đầy đủ các đặc tính kỹ thuật của ba bộ dữ liệu thực nghiệm:")

    # Bảng 1
    tbl_d = doc.add_table(rows=4, cols=6)
    tbl_d.alignment = WD_TABLE_ALIGNMENT.CENTER
    d_headers = ["Tập dữ liệu", "Loại dữ liệu", "Kích thước đầu vào", "Số lớp", "Phân chia (Train / Val / Test)", "Mục tiêu bài toán"]
    d_rows = [
        ["MNIST", "Hình ảnh xám 2D", "1 × 28 × 28", "10 chữ số", "54,000 / 6,000 / 10,000", "Phân loại chữ số viết tay"],
        ["Fashion-MNIST", "Hình ảnh xám 2D", "1 × 28 × 28", "10 thời trang", "54,000 / 6,000 / 10,000", "Phân loại sản phẩm thời trang"],
        ["Diabetes", "Dữ liệu bảng 1D", "1 × 8 đặc trưng", "2 (Nhị phân)", "537 / 115 / 116", "Dự đoán nguy cơ tiểu đường"]
    ]
    for c_idx, h in enumerate(d_headers):
        cell = tbl_d.cell(0, c_idx)
        set_cell_background(cell, "2B6CB0")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(d_rows):
        for c_idx, val in enumerate(row_data):
            cell = tbl_d.cell(r_idx + 1, c_idx)
            set_cell_margins(cell, 60, 60, 100, 100)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.bold = True

    set_table_borders(tbl_d, color="CBD5E0", sz="4", val="single")

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_09_dataset_summary.png',
        fig_title='Hình 9. Kết quả Dataset summary trong notebook.',
        source='Cell [6] trong executed notebook A05_06_taint_731.ipynb, phần tổng kết kiểm tra tính toàn vẹn của dữ liệu.',
        read_guide='Đọc các dòng in tóm tắt kích thước tensor, số lượng mẫu và hình dạng đầu ra của cả 3 bài toán.',
        obs='Tất cả các DataLoader đều được khởi tạo trơn tru, tensor shape hoàn toàn tương thích với các mô hình 2D và 1D đã thiết kế.',
        explanation='Bước kiểm tra này bảo đảm không xảy ra lỗi lệch chiều (dimension mismatch) hay thiếu hụt dữ liệu trong quá trình huấn luyện tự động.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    # -------------------------------------------------------------
    # CHƯƠNG 6: THIẾT KẾ VÀ CÀI ĐẶT CÁC MÔ HÌNH CNN
    # -------------------------------------------------------------
    add_h1("6. THIẾT KẾ VÀ CÀI ĐẶT CÁC MÔ HÌNH CNN")
    
    add_h2("6.1. Mô hình M1: Basic CNN")
    add_p("Mô hình cơ sở M1 (Basic CNN) được thiết kế với hai tầng tích chập và một tầng Fully Connected. Cấu trúc cụ thể bao gồm:")
    add_bullet("Conv2d(1, 16, kernel_size=3, padding=1) → ReLU → MaxPool2d(2, 2). Kích thước tensor giảm từ 28×28 xuống 14×14 với 16 kênh.")
    add_bullet("Conv2d(16, 32, kernel_size=3, padding=1) → ReLU → MaxPool2d(2, 2). Kích thước tensor giảm từ 14×14 xuống 7×7 với 32 kênh.")
    add_bullet("Flatten → Linear(32 * 7 * 7, 10). Tầng kết nối đầy đủ ánh xạ 1,568 đặc trưng sang 10 logit phân lớp.")
    add_p("Tổng số tham số của M1 là: (1*16*3*3 + 16) + (16*32*3*3 + 32) + (1568*10 + 10) = 160 + 4,640 + 15,690 = 20,490 tham số.")

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_10_m1_basic_def.png',
        fig_title='Hình 10. Định nghĩa hàm cho M1 Basic CNN.',
        source='Cell [7] trong executed notebook A05_06_taint_731.ipynb, định nghĩa lớp BasicCNN kế thừa từ nn.Module.',
        read_guide='Đọc các hàm __init__ và forward thực hiện tuần tự các phép tích chập, phi tuyến ReLU, gộp MaxPool và Linear.',
        obs='Cấu trúc mã nguồn PyTorch chuẩn mực, rõ ràng, dễ bảo trì và theo dõi luồng dữ liệu.',
        explanation='M1 đóng vai trò là cột mốc chuẩn (baseline) để định lượng mức độ cải thiện của các kỹ thuật tiếp theo.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_h2("6.2. Mô hình M2: BatchNorm CNN")
    add_p("Mô hình M2 tích hợp thêm hai tầng nn.BatchNorm2d(16) và nn.BatchNorm2d(32) ngay sau mỗi lớp Conv2d và trước hàm kích hoạt ReLU. Việc bổ sung này thêm vào mỗi tầng BN hai tham số học được (γ, β) cho mỗi kênh:")
    add_bullet("Tầng BN thứ nhất (16 kênh): Thêm 16*2 = 32 tham số (cộng 32 tham số thống kê chạy running mean/var).")
    add_bullet("Tầng BN thứ hai (32 kênh): Thêm 32*2 = 64 tham số.")
    add_p("Tổng số tham số học được của M2 là 20,490 + 32 + 64 = 20,586 tham số (tăng chính xác 96 tham số so với M1).")

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_11_m2_bn_def.png',
        fig_title='Hình 11. Định nghĩa hàm cho M2 BatchNorm CNN.',
        source='Cell [8] trong executed notebook A05_06_taint_731.ipynb, định nghĩa lớp BatchNormCNN.',
        read_guide='Quan sát sự xuất hiện của self.bn1 và self.bn2 trong __init__ và thứ tự gọi F.relu(self.bn1(self.conv1(x))) trong forward.',
        obs='Thứ tự chuẩn Conv -> BN -> ReLU được áp dụng nghiêm ngặt theo khuyến nghị của Ioffe & Szegedy.',
        explanation='Chuẩn hóa đầu ra trước khi qua hàm kích hoạt giúp phân phối giá trị luôn ổn định quanh vùng nhạy của ReLU.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_12_m1_m2_param_comp.png',
        fig_title='Hình 12. So sánh tham số giữa M1 và M2.',
        source='Cell [9] trong executed notebook A05_06_taint_731.ipynb, mã kiểm tra và so sánh số tham số giữa M1 và M2.',
        read_guide='Đọc các dòng in kết quả tham số: M1 có 20,490 tham số, M2 có 20,586 tham số (chênh lệch đúng 96 tham số).',
        obs='Kết quả kiểm tra tham số khớp chính xác 100% với tính toán giải tích lý thuyết.',
        explanation='Minh chứng rõ ràng rằng BatchNorm chỉ gia tăng một lượng tham số cực kỳ nhỏ nhưng mang lại sự ổn định tính toán to lớn.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_h2("6.3. Mô hình M3: Residual CNN")
    add_p("Mô hình M3 kế thừa tầng Conv đầu tiên của M2, sau đó chèn vào một khối phần dư ResBlock2D(16) trước khi đi qua tầng MaxPool. Khối ResBlock2D bao gồm hai lớp Conv2d(16, 16, 3, padding=1) đi kèm BatchNorm2d(16), với kết nối tắt x_out = ReLU(x + BN(Conv(ReLU(BN(Conv(x)))))). Số tham số bổ sung của ResBlock2D là: 2 * (16*16*3*3 + 16 + 16*2) = 2 * (2,304 + 16 + 32) = 4,704 tham số. Tổng số tham số của M3 là 20,586 + 4,704 = 25,290 tham số.")

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_13_resblock_def.png',
        fig_title='Hình 13. Định nghĩa khối ResidualBlock.',
        source='Cell [10] trong executed notebook A05_06_taint_731.ipynb, định nghĩa lớp ResBlock2D.',
        read_guide='Đọc phương thức forward: return F.relu(x + self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x)))))).',
        obs='Phép cộng nhánh tắt "+ x" được thực hiện trước hàm kích hoạt ReLU cuối cùng của khối.',
        explanation='Cấu trúc này cho phép tín hiệu đầu vào đi thẳng qua khối mà không bị suy hao nếu nhánh tích chập chưa học được đặc trưng hữu ích.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_14_m3_resnet_def.png',
        fig_title='Hình 14. Định nghĩa ResidualCNN.',
        source='Cell [11] trong executed notebook A05_06_taint_731.ipynb, định nghĩa lớp ResidualCNN hoàn chỉnh.',
        read_guide='Quan sát sự tích hợp của self.res = ResBlock2D(16) vào kiến trúc tổng thể giữa conv1 và conv2.',
        obs='Mô hình kết hợp nhuần nhuyễn giữa khối tích chập chuẩn, khối phần dư và các tầng gộp không gian.',
        explanation='Thiết kế này bảo đảm tensor kích thước 14x14 được tinh chỉnh đặc trưng sâu trước khi gộp xuống 7x7.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_h2("6.4. Mô hình M4: Attention CNN (Squeeze-and-Excitation)")
    add_p("Mô hình M4 tích hợp khối SEBlock2D(16, r=4) ngay sau khối ResBlock2D của M3. Khối SE thực hiện ép thông tin không gian qua adaptive_avg_pool2d(x, 1), sau đó đưa qua hai tầng Linear(16, 4) và Linear(4, 16) với hàm kích hoạt Sigmoid để nhân lại với tensor đặc trưng ban đầu. Số tham số bổ sung của SEBlock2D là: (16*4 + 4) + (4*16 + 16) = 68 + 80 = 148 tham số. Tổng số tham số của M4 là 25,290 + 148 = 25,438 tham số.")

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_15_seblock_def.png',
        fig_title='Hình 15. Định nghĩa SEBlock.',
        source='Cell [12] trong executed notebook A05_06_taint_731.ipynb, định nghĩa lớp SEBlock2D.',
        read_guide='Đọc các phép toán trong forward: F.adaptive_avg_pool2d(x, 1), qua self.fc1 (ReLU) và self.fc2 (Sigmoid), rồi nhân lại x * w.',
        obs='Cơ chế chú ý kênh được cài đặt cực kỳ tinh gọn, hiệu quả và tối ưu hóa bộ nhớ.',
        explanation='Hệ số co hẹp r=4 cân bằng hoàn hảo giữa khả năng biểu đạt mối tương quan kênh và chi phí tham số bổ sung.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_16_m4_attention_def.png',
        fig_title='Hình 16. Định nghĩa AttentionCNN.',
        source='Cell [13] trong executed notebook A05_06_taint_731.ipynb, định nghĩa lớp AttentionCNN tích hợp cả ResBlock và SEBlock.',
        read_guide='Quan sát dòng mã: x = self.se(self.res(x)) trước khi đưa qua MaxPool.',
        obs='Đỉnh cao tiến hóa của chuỗi mô hình: vừa có khả năng truyền gradient của ResNet vừa có cơ chế lọc đặc trưng của SE-Net.',
        explanation='Mô hình đại diện cho sự kết hợp của hai kỹ thuật đoạt giải cao nhất trong lịch sử các cuộc thi thị giác máy tính quốc tế.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_h2("6.5. Mô hình M5: Adapted LeNet")
    add_p("Phiên bản thích nghi của LeNet-5 bao gồm hai tầng Conv2d (kernel 5×5 không padding): Conv1(1→6, 5×5) giảm kích thước xuống 24×24; AvgPool2d(2) giảm xuống 12×12; Conv2(6→16, 5×5) giảm xuống 8×8; AvgPool2d(2) giảm xuống 4×4. Phần phân loại gồm 3 tầng FC: Linear(256, 120) → Linear(120, 84) → Linear(84, 10). Toàn bộ mô hình có 44,426 tham số.")

    add_h2("6.6. Mô hình M6: Adapted AlexNet")
    add_p("Được thiết kế theo phong cách AlexNet thích nghi với ảnh 28×28: gồm 3 tầng Conv2d (32→64→128, kernel 3×3, padding 1) với hai tầng MaxPool2d(2), tạo ra tensor 128 kênh kích thước 7×7. Tầng phân loại sử dụng Fully Connected lớn: Linear(128*7*7 = 6,272, 256) đi kèm Dropout(0.5) và Linear(256, 10). Do tầng FC đầu tiên có kích thước ma trận trọng số rất lớn (6,272 × 256 = 1,605,632), tổng số tham số của M6 lên tới 1,701,130 tham số, lớn nhất trong toàn bộ các mô hình thực nghiệm.")

    add_h2("6.7. Mô hình M7: Adapted VGG")
    add_p("Thiết kế theo nguyên lý khối tích chập kép của VGG: Khối 1 gồm hai lớp Conv2d(1→32) và Conv2d(32→32) + MaxPool; Khối 2 gồm hai lớp Conv2d(32→64) và Conv2d(64→64) + MaxPool. Tensor đầu ra của feature extractor có kích thước 64 kênh × 7 × 7 = 3,136 đặc trưng. Phần phân loại gồm Linear(3,136, 128) đi kèm Dropout(0.5) và Linear(128, 10). Tổng số tham số của M7 là 467,818 tham số.")

    add_h2("6.8. Thiết kế các mô hình Conv1D cho dữ liệu bảng Diabetes")
    add_p("Với dữ liệu bảng Diabetes (8 thuộc tính lâm sàng), chuỗi 4 mô hình 1D được thiết kế đối xứng hoàn toàn:")
    add_bullet("Diabetes M1 Basic CNN: Conv1d(1, 16, 3, pad=1) → ReLU → MaxPool1d(2) (chiều dài giảm về 4) → Conv1d(16, 32, 3, pad=1) → ReLU → Linear(32*4 = 128, 1). Có 1,761 tham số.")
    add_bullet("Diabetes M2 BatchNorm CNN: Tích hợp BatchNorm1d(16) và BatchNorm1d(32). Có 1,857 tham số (tăng 96 tham số).")
    add_bullet("Diabetes M3 Residual CNN: Tích hợp khối ResBlock1D(16) với hai lớp Conv1d(16, 16, 3, pad=1) và BatchNorm1d(16). Có 3,489 tham số.")
    add_bullet("Diabetes M4 Attention CNN: Tích hợp thêm SEBlock1D(16, r=4) với adaptive_avg_pool1d và hai tầng Linear. Có 3,637 tham số.")

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_17_diab_m1_def.png',
        fig_title='Hình 17. Định nghĩa DiabetesBasicCNN.',
        source='Cell [14] trong executed notebook A05_06_taint_731.ipynb, định nghĩa kiến trúc Conv1D cơ bản cho Diabetes.',
        read_guide='Đọc các hàm __init__ và forward áp dụng Conv1d và MaxPool1d trên tensor 1 chiều.',
        obs='Mô hình nhận đầu vào (B, 1, 8) và trả về logit nhị phân kích thước (B, 1).',
        explanation='Chứng minh tính linh hoạt của phép tích chập khi mở rộng ra ngoài phạm vi thị giác máy tính.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_18_diab_m2_bn_def.png',
        fig_title='Hình 18. Định nghĩa hàm BatchNorm cho Diabete.',
        source='Cell [15] trong executed notebook A05_06_taint_731.ipynb, định nghĩa DiabetesBatchNormCNN.',
        read_guide='Quan sát việc tích hợp BatchNorm1d(16) và BatchNorm1d(32).',
        obs='Cấu trúc chuẩn tắc tương tự mô hình ảnh 2D nhưng hoạt động trên không gian 1D.',
        explanation='Chuẩn hóa theo lô đặc biệt quan trọng với dữ liệu y tế do các chỉ số có thang đo ban đầu rất phân tán.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_19_diab_resblock1d_def.png',
        fig_title='Hình 19. Định nghĩa ResidualBlock1D.',
        source='Cell [16] trong executed notebook A05_06_taint_731.ipynb, định nghĩa lớp ResBlock1D.',
        read_guide='Đọc phương thức forward với kết nối tắt 1D: return F.relu(x + self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x)))))).',
        obs='Bảo toàn hoàn hảo cơ chế phần dư trên miền dữ liệu bảng.',
        explanation='Giúp gradient truyền thông suốt qua các tầng biến đổi đặc trưng lâm sàng.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_20_diab_m3_resnet_def.png',
        fig_title='Hình 20. Định nghĩa DiabetesResidualCNN.',
        source='Cell [17] trong executed notebook A05_06_taint_731.ipynb, định nghĩa DiabetesResidualCNN hoàn chỉnh.',
        read_guide='Quan sát sự tích hợp của ResBlock1D vào chuỗi xử lý Conv1D.',
        obs='Kiến trúc tinh gọn, chỉ với 3,489 tham số nhưng có chiều sâu biểu diễn đặc trưng mạnh mẽ.',
        explanation='Mô hình này sau đó đã chứng minh đạt hiệu năng vượt trội nhất trong toàn bộ nhóm thực nghiệm Diabetes.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_21_diab_seblock1d_def.png',
        fig_title='Hình 21. Định nghĩa SEBlock1D cho Diabetes.',
        source='Cell [18] trong executed notebook A05_06_taint_731.ipynb, định nghĩa lớp SEBlock1D.',
        read_guide='Đọc phép gộp adaptive_avg_pool1d(x, 1) và cơ chế kích thích kênh bằng Sigmoid trong không gian 1D.',
        obs='Kênh đặc trưng 1D được tái cân chỉnh trọng số phụ thuộc vào ngữ cảnh toàn thể mẫu bệnh nhân.',
        explanation='Mở rộng cơ chế Channel Attention sang phân tích dữ liệu bảng y tế.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_image_with_caption(
        img_path='ass5_experiments/rendered_cells/fig_22_diab_m4_attention_def.png',
        fig_title='Hình 22. Định nghĩa DiabetesAttentionCNN.',
        source='Cell [19] trong executed notebook A05_06_taint_731.ipynb, định nghĩa DiabetesAttentionCNN tích hợp cả ResBlock1D và SEBlock1D.',
        read_guide='Quan sát dòng mã: x = self.se(self.res(x)) trong forward pass.',
        obs='Mô hình Conv1D phức tạp nhất dành cho dữ liệu tiểu đường với 3,637 tham số.',
        explanation='Cung cấp đối chứng thực nghiệm sâu sắc về giới hạn của cơ chế attention trên các tập dữ liệu nhỏ.',
        limits='Ảnh thực thi chụp trực tiếp từ Playwright.'
    )

    add_h2("6.9. Kiểm tra Output Shape và Thống kê Không gian tham số")
    add_p("Trước khi bước vào huấn luyện, một dummy tensor kích thước (1, 1, 28, 28) cho ảnh và (1, 1, 8) cho bảng được truyền qua từng mô hình để xác thực output shape và đếm chính xác số lượng tham số học được (trainable parameters).")
    
    # Bảng 2
    tbl_p = doc.add_table(rows=12, cols=5)
    tbl_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_headers = ["Ký hiệu", "Tên kiến trúc mô hình", "Miền dữ liệu", "Output Shape", "Số lượng tham số học được"]
    p_rows = [
        ["M1", "Basic CNN", "Hình ảnh 2D", "torch.Size([1, 10])", "20,490"],
        ["M2", "BatchNorm CNN", "Hình ảnh 2D", "torch.Size([1, 10])", "20,586"],
        ["M3", "Residual CNN", "Hình ảnh 2D", "torch.Size([1, 10])", "25,290"],
        ["M4", "Attention CNN (SE-Net)", "Hình ảnh 2D", "torch.Size([1, 10])", "25,438"],
        ["M5", "Adapted LeNet-5", "Hình ảnh 2D", "torch.Size([1, 10])", "44,426"],
        ["M6", "Adapted AlexNet", "Hình ảnh 2D", "torch.Size([1, 10])", "1,701,130"],
        ["M7", "Adapted VGG", "Hình ảnh 2D", "torch.Size([1, 10])", "467,818"],
        ["M1 (1D)", "Diabetes Basic Conv1D", "Dữ liệu bảng 1D", "torch.Size([1, 1])", "1,761"],
        ["M2 (1D)", "Diabetes BatchNorm Conv1D", "Dữ liệu bảng 1D", "torch.Size([1, 1])", "1,857"],
        ["M3 (1D)", "Diabetes Residual Conv1D", "Dữ liệu bảng 1D", "torch.Size([1, 1])", "3,489"],
        ["M4 (1D)", "Diabetes Attention Conv1D", "Dữ liệu bảng 1D", "torch.Size([1, 1])", "3,637"]
    ]
    for c_idx, h in enumerate(p_headers):
        cell = tbl_p.cell(0, c_idx)
        set_cell_background(cell, "2B6CB0")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(p_rows):
        for c_idx, val in enumerate(row_data):
            cell = tbl_p.cell(r_idx + 1, c_idx)
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx in [0, 4]:
                r.bold = True
            if c_idx == 4:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    set_table_borders(tbl_p, color="CBD5E0", sz="4", val="single")

    # -------------------------------------------------------------
    # CHƯƠNG 7: QUY TRÌNH HUẤN LUYỆN VÀ ĐÁNH GIÁ ĐỐI CHUẨN
    # -------------------------------------------------------------
    add_h1("7. QUY TRÌNH HUẤN LUYỆN VÀ ĐÁNH GIÁ ĐỐI CHUẨN")
    
    add_h2("7.1. Thiết lập siêu tham số và tối ưu hóa")
    add_p("Nhằm bảo đảm nguyên tắc thực nghiệm có kiểm soát (Controlled Experiments), các siêu tham số được cố định chặt chẽ:")
    add_bullet("Thuật toán tối ưu: Adam Optimizer với learning rate khởi tạo lr = 0.001, betas = (0.9, 0.999), eps = 1e-8.")
    add_bullet("Hàm mất mát (Loss Function): nn.CrossEntropyLoss() cho bài toán phân loại đa lớp (MNIST và Fashion-MNIST); nn.BCEWithLogitsLoss() kết hợp hàm Sigmoid số học ổn định cho bài toán nhị phân Diabetes.")
    add_bullet("Số epoch huấn luyện: 5 epochs cho các tập dữ liệu ảnh (đủ để các mô hình CNN hội tụ tới mức ổn định mà không lãng phí tài nguyên); 15 epochs cho tập dữ liệu bảng Diabetes.")
    add_bullet("Kích thước lô (Batch Size): 64 cho ảnh 2D và 32 cho bảng 1D.")

    add_h2("7.2. Cơ chế lưu trữ trạng thái tối ưu (Validation Checkpointing)")
    add_p("Một lỗi phương pháp luận rất phổ biến trong các báo cáo học máy là việc lấy trực tiếp trạng thái mô hình ở epoch cuối cùng để đem đi đánh giá trên test set. Trong thực tế, mô hình ở epoch cuối rất có thể đã bắt đầu rơi vào vùng quá khớp (overfitting) hoặc gặp phải dao động ngẫu nhiên khiến hiệu năng suy giảm.")
    add_p("Trong Assignment 05, một cơ chế Checkpointing chuyên nghiệp được lập trình: sau mỗi epoch, mô hình được chuyển sang chế độ model.eval(), tính toán chính xác Validation Accuracy trên tập validation độc lập. Nếu val_acc > best_val_acc, một bản sao sâu (deepcopy) của toàn bộ state_dict sẽ được ghi nhận. Khi kết thúc toàn bộ chu trình huấn luyện, mô hình tự động tải lại best_state_dict này trước khi thực hiện bất kỳ phép đo nào trên Test Set. Điều này bảo đảm kết quả đánh giá luôn phản ánh năng lực tổng quát hóa cao nhất của kiến trúc.")

    add_h2("7.3. Đánh giá độc lập trên Test Set")
    add_p("Toàn bộ 18 lượt thực nghiệm (7 mô hình MNIST + 7 mô hình Fashion-MNIST + 4 mô hình Diabetes) được đánh giá trên tập Test Set hoàn toàn biệt lập dưới ngữ cảnh torch.no_grad(). Đầu ra logit được chuyển đổi thành nhãn dự đoán:")
    add_bullet("Với ảnh đa lớp: pred = torch.argmax(logits, dim=1).")
    add_bullet("Với nhị phân: pred = (torch.sigmoid(logits) >= 0.5).float().")

    add_h2("7.4. Hệ thống các độ đo đánh giá toàn diện")
    add_p("Để đánh giá đa chiều hành vi phân loại, bốn độ đo chuẩn mực được tính toán:")
    add_bullet("Độ chính xác tổng thể: Accuracy = (TP + TN) / (TP + TN + FP + FN).")
    add_bullet("Độ chuẩn xác (Precision): Tỷ lệ các dự đoán dương tính là thực sự chính xác: Precision = TP / (TP + FP).")
    add_bullet("Độ nhạy (Recall): Tỷ lệ các mẫu thực tế dương tính được mô hình phát hiện: Recall = TP / (TP + FN).")
    add_bullet("Điểm F1-Score: Trung bình điều hòa giữa Precision và Recall: F1 = 2 * (Precision * Recall) / (Precision + Recall). Với các bài toán đa lớp, độ đo được tính theo trọng số phân bố mẫu (Weighted Average).")

    # -------------------------------------------------------------
    # CHƯƠNG 8: KẾT QUẢ THỰC NGHIỆM ĐỐI CHUẨN
    # -------------------------------------------------------------
    add_h1("8. KẾT QUẢ THỰC NGHIỆM ĐỐI CHUẨN")
    
    add_h2("8.1. Kết quả thực nghiệm trên tập dữ liệu MNIST")
    add_p("Bảng 3 trình bày toàn bộ kết quả thực nghiệm của 7 kiến trúc trên tập dữ liệu kiểm thử MNIST sau 5 epochs huấn luyện:")

    # Bảng 3
    tbl_r1 = doc.add_table(rows=8, cols=5)
    tbl_r1.alignment = WD_TABLE_ALIGNMENT.CENTER
    r1_headers = ["Mô hình", "Số tham số", "Thời gian huấn luyện (s)", "Test Loss", "Test Accuracy (%)"]
    r1_data = [
        ["M1 Basic CNN", "20,490", "256.59", "0.039796", "98.72%"],
        ["M2 BatchNorm", "20,586", "289.47", "0.036356", "98.82%"],
        ["M3 Residual", "25,290", "541.19", "0.028206", "99.04%"],
        ["M4 Attention", "25,438", "622.51", "0.031412", "99.00%"],
        ["M5 LeNet", "44,426", "190.04", "0.048912", "98.50%"],
        ["M6 Adapted AlexNet", "1,701,130", "382.06", "0.025842", "99.19%"],
        ["M7 Adapted VGG", "467,818", "343.75", "0.022031", "99.30%"]
    ]
    for c_idx, h in enumerate(r1_headers):
        cell = tbl_r1.cell(0, c_idx)
        set_cell_background(cell, "2B6CB0")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(r1_data):
        for c_idx, val in enumerate(row_data):
            cell = tbl_r1.cell(r_idx + 1, c_idx)
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.bold = True
            if c_idx in [1, 2, 3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if r_idx == 6 and c_idx == 4: # M7 Best
                r.bold = True
                r.font.color.rgb = RGBColor(0x27, 0x67, 0x49)

    set_table_borders(tbl_r1, color="CBD5E0", sz="4", val="single")

    add_p("Nhận xét trên MNIST: Mô hình M7 Adapted VGG đạt độ chính xác cao nhất (99.30%) và Test Loss thấp nhất (0.022031). M6 Adapted AlexNet bám sát phía sau với 99.19%. Trong chuỗi cải tiến tiến hóa M1→M4, M3 Residual đạt 99.04%, vượt qua baseline M1 (98.72%) và M2 BatchNorm (98.82%). M5 LeNet đứng cuối bảng với 98.50%, cho thấy các bộ lọc 5×5 không có đệm của LeNet có phần lép vế so với các kiến trúc sử dụng bộ lọc 3×3 hiện đại.")

    add_h2("8.2. Kết quả thực nghiệm trên tập dữ liệu Fashion-MNIST")
    add_p("Bảng 4 trình bày kết quả thực nghiệm trên tập dữ liệu Fashion-MNIST:")

    # Bảng 4
    tbl_r2 = doc.add_table(rows=8, cols=5)
    tbl_r2.alignment = WD_TABLE_ALIGNMENT.CENTER
    r2_data = [
        ["M1 Basic CNN", "20,490", "88.13", "0.303449", "89.46%"],
        ["M2 BatchNorm", "20,586", "103.22", "0.279555", "90.29%"],
        ["M3 Residual", "25,290", "190.37", "0.253040", "90.78%"],
        ["M4 Attention", "25,438", "203.07", "0.255394", "90.92%"],
        ["M5 LeNet", "44,426", "59.71", "0.385783", "86.02%"],
        ["M6 Adapted AlexNet", "1,701,130", "246.36", "0.242934", "91.20%"],
        ["M7 Adapted VGG", "467,818", "346.91", "0.242247", "90.81%"]
    ]
    for c_idx, h in enumerate(r1_headers):
        cell = tbl_r2.cell(0, c_idx)
        set_cell_background(cell, "2B6CB0")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(r2_data):
        for c_idx, val in enumerate(row_data):
            cell = tbl_r2.cell(r_idx + 1, c_idx)
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.bold = True
            if c_idx in [1, 2, 3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if r_idx == 5 and c_idx == 4: # M6 Best
                r.bold = True
                r.font.color.rgb = RGBColor(0x27, 0x67, 0x49)

    set_table_borders(tbl_r2, color="CBD5E0", sz="4", val="single")

    add_p("Nhận xét trên Fashion-MNIST: Với bài toán thời trang có độ phức tạp cao hơn nhiều, khoảng cách giữa các mô hình bộc lộ rõ rệt. M6 Adapted AlexNet vươn lên dẫn đầu với 91.20% độ chính xác nhờ dung lượng tham số lớn và kỹ thuật Dropout. Đáng chú ý, trong chuỗi M1→M4, sự tiến hóa diễn ra hoàn hảo: M1 (89.46%) → M2 (90.29%, +0.83 pp) → M3 (90.78%, +0.49 pp) → M4 (90.92%, +0.14 pp). Cơ chế chú ý kênh Squeeze-and-Excitation trong M4 đã phát huy tối đa tác dụng khi giúp mô hình phân biệt tốt hơn các chi tiết hoa văn phức tạp. M5 LeNet chỉ đạt 86.02%, sụt giảm nghiêm trọng tới 5.18 điểm phần trăm so với M6.")

    add_h2("8.3. Kết quả thực nghiệm trên tập dữ liệu Diabetes")
    add_p("Bảng 5 trình bày kết quả của 4 mô hình Conv1D trên tập kiểm thử Diabetes (116 mẫu):")

    # Bảng 5
    tbl_r3 = doc.add_table(rows=5, cols=5)
    tbl_r3.alignment = WD_TABLE_ALIGNMENT.CENTER
    r3_data = [
        ["M1 Basic Conv1D", "1,761", "0.75", "0.493523", "75.86%"],
        ["M2 BatchNorm Conv1D", "1,857", "0.95", "0.374922", "82.76%"],
        ["M3 Residual Conv1D", "3,489", "1.43", "0.389033", "86.21%"],
        ["M4 Attention Conv1D", "3,637", "1.97", "0.397135", "81.90%"]
    ]
    for c_idx, h in enumerate(r1_headers):
        cell = tbl_r3.cell(0, c_idx)
        set_cell_background(cell, "2B6CB0")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(r3_data):
        for c_idx, val in enumerate(row_data):
            cell = tbl_r3.cell(r_idx + 1, c_idx)
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.bold = True
            if c_idx in [1, 2, 3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if r_idx == 2 and c_idx == 4: # M3 Best
                r.bold = True
                r.font.color.rgb = RGBColor(0x27, 0x67, 0x49)

    set_table_borders(tbl_r3, color="CBD5E0", sz="4", val="single")

    add_p("Nhận xét trên Diabetes: Mô hình M3 Residual Conv1D xuất sắc đạt độ chính xác cao nhất (86.21%), vượt trội baseline M1 (75.86%) tới 10.34 điểm phần trăm. Một phát hiện khoa học đặc biệt quan trọng: mô hình M4 Attention đạt 81.90%, thấp hơn M3 dù có số tham số nhiều hơn và thời gian huấn luyện lâu hơn. Điều này chỉ ra rằng trên các tập dữ liệu nhỏ (small sample size), việc thêm cơ chế attention có thể gây ra hiện tượng overfitting nhẹ do các tham số phụ của khối SE khó tối ưu hóa chính xác khi không có đủ lượng dữ liệu hỗ trợ.")

    add_h2("8.4. Phân tích chi tiết các độ đo phân loại (Classification Metrics)")
    add_p("Bảng 6 tổng hợp chi tiết các chỉ số phân loại nâng cao của mô hình tiêu biểu nhất trên từng tập dữ liệu:")

    # Bảng 6
    tbl_m = doc.add_table(rows=4, cols=5)
    tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_headers = ["Tập dữ liệu", "Mô hình tiêu biểu", "Accuracy", "Precision", "Recall", "F1-Score"]
    tbl_m._tbl.tblPr.append(parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/><w:insideV w:val="none"/></w:tblBorders>'))
    
    # Header format
    tbl_m_cells = tbl_m.rows[0].cells
    for i, h in enumerate(["Tập dữ liệu", "Mô hình tiêu biểu", "Accuracy", "Precision (Weighted)", "Recall (Weighted)", "F1-Score (Weighted)"]):
        pass
    
    # Re-create table properly
    doc.paragraphs[-1]._p.getparent().remove(tbl_m._tbl)
    tbl_m = doc.add_table(rows=4, cols=6)
    tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_cols = ["Tập dữ liệu", "Mô hình tiêu biểu", "Accuracy", "Precision", "Recall", "F1-Score"]
    m_data = [
        ["MNIST", "M7 Adapted VGG", "99.30%", "99.30%", "99.30%", "99.30%"],
        ["Fashion-MNIST", "M6 Adapted AlexNet", "91.20%", "91.16%", "91.20%", "91.15%"],
        ["Diabetes", "M3 Residual Conv1D", "86.21%", "86.69%", "86.21%", "85.68%"]
    ]
    for c_idx, h in enumerate(m_cols):
        cell = tbl_m.cell(0, c_idx)
        set_cell_background(cell, "2B6CB0")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(m_data):
        for c_idx, val in enumerate(row_data):
            cell = tbl_m.cell(r_idx + 1, c_idx)
            set_cell_margins(cell, 60, 60, 100, 100)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx in [0, 1]:
                r.bold = True
            if c_idx >= 2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    set_table_borders(tbl_m, color="CBD5E0", sz="4", val="single")

    add_p("Đặc biệt với Diabetes, F1-Score đạt 85.68% thấp hơn một chút so với Accuracy 86.21%, phản ánh tính mất cân bằng mẫu giữa hai lớp. Tuy nhiên, Precision đạt tới 86.69% cho thấy mô hình có độ tin cậy rất cao khi đưa ra chẩn đoán dương tính, hạn chế tối đa việc gây hoang mang cho bệnh nhân khỏe mạnh.")

    add_h2("8.5. Mức độ cải thiện độ chính xác so với mô hình cơ sở M1")
    add_p("Bảng 7 tổng hợp mức độ cải thiện độ chính xác tuyệt đối (tính bằng điểm phần trăm - percentage points pp) của mô hình tốt nhất so với Baseline M1:")

    # Bảng 7
    tbl_imp = doc.add_table(rows=4, cols=5)
    tbl_imp.alignment = WD_TABLE_ALIGNMENT.CENTER
    imp_headers = ["Tập dữ liệu", "Mô hình tốt nhất", "Baseline M1 Acc", "Best Acc", "Mức cải thiện (pp)"]
    imp_data = [
        ["MNIST", "M7 Adapted VGG", "98.72%", "99.30%", "+0.58 pp"],
        ["Fashion-MNIST", "M6 Adapted AlexNet", "89.46%", "91.20%", "+1.74 pp"],
        ["Diabetes", "M3 Residual Conv1D", "75.86%", "86.21%", "+10.34 pp"]
    ]
    for c_idx, h in enumerate(imp_headers):
        cell = tbl_imp.cell(0, c_idx)
        set_cell_background(cell, "2B6CB0")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(imp_data):
        for c_idx, val in enumerate(row_data):
            cell = tbl_imp.cell(r_idx + 1, c_idx)
            set_cell_margins(cell, 60, 60, 100, 100)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx in [0, 1]:
                r.bold = True
            if c_idx >= 2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if c_idx == 4:
                r.bold = True
                r.font.color.rgb = RGBColor(0x27, 0x67, 0x49)

    set_table_borders(tbl_imp, color="CBD5E0", sz="4", val="single")

    add_h2("8.6. Phân tích độ phức tạp tính toán và chi phí tham số")
    add_p("Số lượng tham số dao động mạnh mẽ từ 1,761 (Diabetes M1) cho tới 1,701,130 (Adapted AlexNet). Mô hình M4 Attention chỉ tăng thêm 148 tham số so với M3 Residual nhưng thời gian huấn luyện trên MNIST tăng từ 541.19s lên 622.51s (+15.0%). Điều này chứng minh rằng chi phí tính toán không chỉ phụ thuộc vào số lượng tham số lưu trữ mà còn chịu ảnh hưởng sâu sắc bởi cấu trúc luồng tính toán (Forward graph topology), các phép toán pooling thích nghi và các nhánh rẽ tính toán.")

    # -------------------------------------------------------------
    # CHƯƠNG 9: TRỰC QUAN HÓA VÀ PHÂN TÍCH BIỂU ĐỒ KHOA HỌC
    # -------------------------------------------------------------
    add_h1("9. TRỰC QUAN HÓA VÀ PHÂN TÍCH BIỂU ĐỒ KHOA HỌC")
    
    add_h2("9.1. Vai trò của trực quan hóa trong nghiên cứu học sâu")
    add_p("Trực quan hóa đồ họa không chỉ nhằm mục đích trang trí báo cáo, mà là công cụ chẩn đoán khoa học then chốt giúp kỹ sư AI nhìn thấu hành vi hội tụ, phát hiện sớm hiện tượng overfitting, đánh giá sự ổn định của gradient và phân tích chi tiết các cặp nhầm lẫn trong không gian đa chiều.")

    add_h2("9.2. Phân tích đường cong Loss trên MNIST (Hình 23)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_23_loss_mnist.png',
        fig_title='Hình 23. Đường loss huấn luyện và validation của bảy mô hình trên MNIST.',
        source='ass5_experiments/plots/fig_23_loss_mnist.png, ghi nhận từ quá trình huấn luyện 5 epochs của 7 mô hình trên MNIST.',
        read_guide='Đồ thị bên trái là Training Loss, đồ thị bên phải là Validation Loss. Trục hoành là Epoch (1-5), trục tung là CrossEntropy Loss.',
        obs='Tất cả 7 đường loss đều giảm dốc đứng ngay từ epoch 1 và nhanh chóng hội tụ về dưới mức 0.05 ở epoch 5. Đường validation loss của M7 Adapted VGG và M3 Residual nằm ở vị trí thấp nhất.',
        explanation='Tính chất dễ phân tách của MNIST giúp gradient truyền ổn định. Sự chênh lệch giữa train loss và val loss rất hẹp, minh chứng mô hình không hề bị quá khớp.',
        limits='Do chỉ chạy 5 epochs, một số mô hình sâu như M6 và M7 vẫn còn tiềm năng giảm loss nhẹ nếu tiếp tục huấn luyện.'
    )

    add_h2("9.3. Phân tích đường cong Loss trên Fashion-MNIST (Hình 24)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_24_loss_fashion_mnist.png',
        fig_title='Hình 24. Đường loss huấn luyện và validation của các mô hình trên Fashion-MNIST.',
        source='ass5_experiments/plots/fig_24_loss_fashion_mnist.png, theo dõi quá trình huấn luyện trên Fashion-MNIST.',
        read_guide='Đọc tương tự Hình 23. Quan sát độ dốc và khoảng cách giữa train loss và val loss giữa các mô hình.',
        obs='Loss trên Fashion-MNIST hội tụ ở mức cao hơn đáng kể (khoảng 0.20 - 0.35) so với MNIST. M5 LeNet có đường loss nằm tách biệt ở phía trên cùng (val loss ~0.385).',
        explanation='Độ phức tạp hình thái của quần áo khiến mạng mất nhiều bước gradient hơn để học. M6 AlexNet và M7 VGG nhờ có Dropout nên khoảng cách train-val loss được kiểm soát rất tốt.',
        limits='Biểu đồ phản ánh xu hướng trung bình theo batch, không biểu diễn dao động nội bộ giữa từng step.'
    )

    add_h2("9.4. Phân tích đường cong Loss trên Diabetes (Hình 25)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_25_loss_diabetes.png',
        fig_title='Hình 25. Đường loss huấn luyện và validation của bốn mô hình Diabetes.',
        source='ass5_experiments/plots/fig_25_loss_diabetes.png, theo dõi 15 epochs của 4 mô hình Conv1D.',
        read_guide='Trục hoành là 15 Epochs, trục tung là nhị phân BCE Loss. Đường nét liền là Train Loss, nét đứt là Validation Loss.',
        obs='Train loss giảm đều từ 0.65 xuống 0.20-0.40. Tuy nhiên, Validation loss bắt đầu đi ngang từ epoch 7-8 và có xu hướng dao động nhẹ ở các epoch sau.',
        explanation='Tập dữ liệu Diabetes có số lượng mẫu nhỏ (537 mẫu train). Khi mạng học sâu hơn, hiện tượng ghi nhớ mẫu (memorization) xuất hiện, làm val loss không giảm thêm. Đây là minh chứng tuyệt đối cho sự cần thiết của cơ chế Validation Checkpointing.',
        limits='Kích thước validation chỉ 115 mẫu nên đường cong có độ nhạy dao động cao hơn so với tập dữ liệu ảnh.'
    )

    add_h2("9.5. Phân tích so sánh Test Accuracy trên MNIST (Hình 26)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_26_acc_mnist.png',
        fig_title='Hình 26. So sánh test accuracy của bảy mô hình trên MNIST.',
        source='ass5_experiments/plots/fig_26_acc_mnist.png, biểu đồ cột đối chuẩn kết quả kiểm thử trên 10,000 mẫu MNIST.',
        read_guide='Trục tung biểu diễn Test Accuracy trong khoảng [97.0%, 100.0%]. Đọc giá trị phần trăm ghi trên đầu mỗi cột.',
        obs='Cả 7 cột đều vượt mốc 98.5%. M7 Adapted VGG dẫn đầu với 99.30%, tiếp theo là M6 (99.19%), M3 (99.04%) và M4 (99.00%).',
        explanation='Việc giới hạn trục tung từ 97% giúp quan sát rõ sự chênh lệch nhỏ nhưng có ý nghĩa giữa các kiến trúc. M3 và M4 cải thiện rõ rệt so với M1 (98.72%).',
        limits='Thang đo phóng đại có thể tạo cảm giác chênh lệch rất lớn về mặt thị giác, cần đối chiếu với con số thực tế.'
    )

    add_h2("9.6. Phân tích so sánh Test Accuracy trên Fashion-MNIST (Hình 27)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_27_acc_fashion_mnist.png',
        fig_title='Hình 27. So sánh test accuracy trên Fashion-MNIST.',
        source='ass5_experiments/plots/fig_27_acc_fashion_mnist.png, so sánh độ chính xác trên 10,000 mẫu Fashion-MNIST.',
        read_guide='Trục tung biểu diễn khoảng [84.0%, 93.0%]. Đọc giá trị phần trăm và bậc thang độ cao giữa các nhóm mô hình.',
        obs='M6 AlexNet đạt đỉnh 91.20%. Chuỗi M1 (89.46%) -> M2 (90.29%) -> M3 (90.78%) -> M4 (90.92%) tạo thành một bậc thang tăng trưởng hoàn hảo.',
        explanation='Khẳng định giá trị thực tiễn của BatchNorm, Residual và Channel Attention: mỗi kỹ thuật bổ sung đều đóng góp gia tăng độ chính xác một cách nhất quán.',
        limits='Độ chính xác chưa đạt mức >93% do chưa áp dụng kỹ thuật tăng cường dữ liệu (Data Augmentation).'
    )

    add_h2("9.7. Phân tích so sánh Test Accuracy trên Diabetes (Hình 28)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_28_acc_diabetes.png',
        fig_title='Hình 28. So sánh test accuracy của bốn mô hình Diabetes.',
        source='ass5_experiments/plots/fig_28_acc_diabetes.png, đối chuẩn kết quả trên 116 bệnh nhân tập kiểm thử.',
        read_guide='Trục tung biểu diễn khoảng [70.0%, 90.0%]. Bốn cột đại diện cho 4 kiến trúc Conv1D.',
        obs='M3 Residual Conv1D vượt trội hoàn toàn với 86.21%, bỏ xa M1 (75.86%) tới 10.34 điểm phần trăm. M4 Attention (81.90%) thấp hơn M3.',
        explanation='Residual connection giúp mạng 1D khai thác tối đa mối tương quan cục bộ giữa 8 đặc trưng mà không bị nghẽn thông tin.',
        limits='Do tập test có 116 mẫu, mỗi mẫu dự đoán đúng/sai tương ứng với bước nhảy xấp xỉ 0.86% độ chính xác.'
    )

    add_h2("9.8. Phân tích thời gian huấn luyện (Training Time - Hình 29)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_29_training_time.png',
        fig_title='Hình 29. Thời gian huấn luyện các mô hình ảnh trên MNIST và Fashion-MNIST.',
        source='ass5_experiments/plots/fig_29_training_time.png, so sánh thời gian thực thi tính bằng giây trên cùng phần cứng CPU.',
        read_guide='Cột xanh là MNIST, cột cam là Fashion-MNIST. Trục tung là thời gian tính bằng giây cho trọn vẹn 5 epochs.',
        obs='M4 Attention mất thời gian lâu nhất trên MNIST (622.5s), tiếp theo là M3 Residual (541.2s). M5 LeNet nhanh nhất (190.0s trên MNIST và 59.7s trên Fashion-MNIST).',
        explanation='Các phép toán bổ sung trong khối Residual và SEBlock làm tăng chiều dài đồ thị tính toán xuôi và ngược, dẫn đến thời gian thực thi lâu hơn.',
        limits='Thời gian huấn luyện phụ thuộc vào tải hệ thống và việc tối ưu luồng của PyTorch trên CPU đa lõi.'
    )

    add_h2("9.9. Phân tích số tham số huấn luyện (Trainable Parameters - Hình 30)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_30_trainable_parameters.png',
        fig_title='Hình 30. So sánh số tham số trainable của bảy mô hình ảnh.',
        source='ass5_experiments/plots/fig_30_trainable_parameters.png, biểu diễn số tham số trên thang đo Logarithmic.',
        read_guide='Trục tung là thang đo log từ 10^4 đến 5*10^6. Đọc số tham số cụ thể được dán trên từng đỉnh cột.',
        obs='Sự phân hóa cực kỳ sâu sắc: M6 AlexNet sở hữu tới 1,701,130 tham số, cao gấp 83 lần so với M1 (20,490) và gấp 67 lần so với M4 (25,438).',
        explanation='M6 có số tham số khổng lồ do ma trận kết nối đầy đủ Flatten -> Linear(6272, 256). Ngược lại, M3 và M4 duy trì số tham số rất nhỏ gọn (~25k) mà vẫn đạt độ chính xác xấp xỉ M6.',
        limits='Thang đo log giúp biểu diễn các giá trị chênh lệch lớn nhưng có thể làm giảm bớt độ ấn tượng trực quan về độ phình tham số của M6.'
    )

    add_h2("9.10. Phân tích Ma trận nhầm lẫn trên MNIST (Hình 31)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_31_confusion_matrix_mnist.png',
        fig_title='Hình 31. Confusion Matrix của M7 Adapted VGG trên MNIST.',
        source='ass5_experiments/plots/fig_31_confusion_matrix_mnist.png, ma trận nhầm lẫn 10x10 trên 10,000 ảnh test MNIST.',
        read_guide='Trục tung là Nhãn thực tế (True Label), trục hoành là Nhãn dự đoán (Predicted Label). Đường chéo chính biểu diễn số lượng mẫu dự đoán chính xác.',
        obs='Hầu như toàn bộ trọng số tập trung tuyệt đối vào đường chéo chính (màu xanh đậm). Chỉ có rải rác một vài ca nhầm lẫn nhỏ (như chữ số 4 bị nhầm thành 9, hoặc chữ số 7 nhầm thành 1).',
        explanation='Độ chính xác 99.30% tương ứng với 9,930/10,000 mẫu đúng. Các trường hợp nhầm lẫn đều là những chữ số có nét viết biến dạng nghiêm trọng trong thực tế.',
        limits='Ma trận chỉ phản ánh kết quả trên tập kiểm thử tĩnh chuẩn của MNIST.'
    )

    add_h2("9.11. Phân tích Ma trận nhầm lẫn trên Fashion-MNIST (Hình 32)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_32_confusion_matrix_fashion.png',
        fig_title='Hình 32. Confusion Matrix của M6 Adapted AlexNet trên Fashion-MNIST.',
        source='ass5_experiments/plots/fig_32_confusion_matrix_fashion.png, ma trận nhầm lẫn 10x10 trên 10,000 mẫu Fashion-MNIST.',
        read_guide='Quan sát các ô nằm ngoài đường chéo chính có mật độ màu cam đậm để nhận diện các cặp lớp thường xuyên bị nhầm lẫn.',
        obs='Các ô nhầm lẫn tập trung chủ yếu ở hai cụm: Cụm áo (T-shirt lớp 0 và Shirt lớp 6 có tới 90 ca nhầm lẫn lẫn nhau; Pullover lớp 2 và Coat lớp 4 có 80 ca nhầm lẫn); Cụm giày dép (Ankle boot lớp 9 và Sneaker lớp 7 có 40 ca nhầm lẫn). Ngược lại, Trouser (lớp 1) dự đoán đúng tới 980/1000 mẫu.',
        explanation='Biên dạng không gian của T-shirt và Shirt ở độ phân giải 28x28 là cực kỳ giống nhau, ngay cả mắt người cũng gặp khó khăn trong việc phân biệt nếu cổ áo không rõ ràng.',
        limits='Minh họa giới hạn nhận thức của mô hình 2D khi thiếu thông tin màu sắc và độ phân giải cao.'
    )

    add_h2("9.12. Phân tích Ma trận nhầm lẫn trên Diabetes (Hình 33)")
    add_image_with_caption(
        img_path='ass5_experiments/plots/fig_33_confusion_matrix_diabetes.png',
        fig_title='Hình 33. Confusion Matrix của M3 Residual trên Diabetes.',
        source='ass5_experiments/plots/fig_33_confusion_matrix_diabetes.png, ma trận nhầm lẫn 2x2 trên 116 mẫu bệnh nhân kiểm thử.',
        read_guide='Gồm 4 ô: Góc trên-trái là Đúng Âm tính (TN), góc trên-phải là Báo động giả (FP), góc dưới-trái là Bỏ sót ca bệnh (FN), góc dưới-phải là Đúng Dương tính (TP).',
        obs='Mô hình đạt TN = 68 ca (trên tổng số 75 người bình thường), TP = 32 ca (trên tổng số 41 người bệnh). Số ca báo động giả FP = 7 và bỏ sót FN = 9.',
        explanation='Tổng số mẫu dự đoán đúng là 68 + 32 = 100 / 116 mẫu, tương ứng với Accuracy 86.21%. Tỷ lệ phát hiện bệnh nhân thực tế (Recall) đạt 32/41 = 78.05%, là con số rất ấn tượng trên tập dữ liệu bảng lâm sàng nhỏ.',
        limits='Trong ứng dụng y tế lâm sàng thực tế, chi phí của việc bỏ sót bệnh nhân (FN) thường nguy hiểm hơn nhiều so với báo động giả (FP), có thể cần tinh chỉnh threshold phân loại xuống mức 0.35 - 0.40.'
    )

    # -------------------------------------------------------------
    # CHƯƠNG 10: SO SÁNH, THẢO LUẬN VÀ BÀN LUẬN KHOA HỌC
    # -------------------------------------------------------------
    add_h1("10. SO SÁNH, THẢO LUẬN VÀ BÀN LUẬN KHOA HỌC")
    
    add_h2("10.1. So sánh chuỗi tiến hóa M1 – M4 trên MNIST")
    add_p("Trên tập dữ liệu MNIST, việc chuyển từ M1 (98.72%) lên M2 (+0.10 pp) và M3 (+0.22 pp) mang lại sự cải thiện rõ ràng. Tuy nhiên, M4 Attention (99.00%) lại thấp hơn M3 một lượng nhỏ 0.04 pp. Nguyên nhân là do MNIST là bài toán nhận dạng chữ số đơn kênh với cấu trúc quá đơn giản, thông tin giữa các kênh không có sự phân hóa sâu sắc nên việc áp dụng cơ chế Channel Attention không tạo thêm lợi thế phân biệt, ngược lại còn làm tăng nhẹ số lượng tham số cần tối ưu.")

    add_h2("10.2. So sánh chuỗi tiến hóa M1 – M4 trên Fashion-MNIST")
    add_p("Trái ngược hoàn toàn với MNIST, trên Fashion-MNIST chuỗi M1 → M2 → M3 → M4 thể hiện tính ưu việt tuyệt đối ở mọi nấc thang tiến hóa: M1 (89.46%) → M2 (90.29%) → M3 (90.78%) → M4 (90.92%). Điều này chứng minh quy luật khoa học: Các cơ chế nâng cao như Residual Connection và Channel Attention chỉ phát huy tối đa giá trị khi bài toán đầu vào có độ phức tạp cao, không gian đặc trưng phong phú và có nhiều chi tiết ngữ nghĩa tinh vi.")

    add_h2("10.3. So sánh chuỗi tiến hóa M1 – M4 trên Diabetes")
    add_p("Trong bài toán dữ liệu bảng Diabetes, M3 Residual Conv1D tạo nên bước nhảy vọt ngoạn mục nhất với 86.21% (+10.34 pp so với M1). Tuy nhiên, M4 Attention sụt giảm xuống 81.90%. Hiện tượng này mang lại một bài học kinh nghiệm sâu sắc: Attention không phải là 'viên đạn bạc' (silver bullet) luôn đem lại hiệu quả trong mọi hoàn cảnh. Khi dữ liệu quá nhỏ (768 mẫu), các khối Attention dễ làm phức tạp hóa không gian tối ưu, dẫn đến việc mô hình học phải các mối tương quan giả (spurious correlations).")

    add_h2("10.4. Classical CNN và các mô hình cải tiến tiến hóa")
    add_p("So sánh giữa nhóm cổ điển (M5, M6, M7) và nhóm cải tiến (M1 - M4) cho thấy:")
    add_bullet("LeNet (M5): Kiến trúc ra đời sớm nhất với các bộ lọc 5×5 không đệm và Average Pooling bộc lộ giới hạn rõ ràng, luôn xếp cuối bảng trên cả MNIST (98.50%) và Fashion-MNIST (86.02%).")
    add_bullet("Adapted AlexNet (M6): Đạt độ chính xác hàng đầu trên Fashion-MNIST (91.20%) nhờ dung lượng tham số khổng lồ (1.7M) và kỹ thuật Dropout. Tuy nhiên, chi phí bộ nhớ của M6 là quá đắt đỏ.")
    add_bullet("Adapted VGG (M7): Đạt độ chính xác cao nhất trên MNIST (99.30%) và Test Loss thấp nhất trên Fashion-MNIST (0.242247), chứng minh nguyên lý thiết kế các khối tích chập kép 3×3 đồng nhất là cực kỳ mạnh mẽ.")
    add_bullet("M3 & M4 cải tiến: Chỉ với khoảng 25 nghìn tham số (bằng 1.5% kích thước của M6), M3 và M4 đạt hiệu năng xấp xỉ sát sao (~90.9% so với 91.2%), thể hiện hiệu quả sử dụng tham số (Parameter Efficiency) vượt trội gấp hàng chục lần.")

    add_h2("10.5. Sự khác biệt bản chất giữa Test Loss và Accuracy")
    add_p("Một phát hiện tinh tế từ bảng kết quả Fashion-MNIST: Mô hình M7 Adapted VGG có Test Loss thấp nhất (0.242247) nhưng Test Accuracy (90.81%) lại thấp hơn M6 Adapted AlexNet (Accuracy 91.20%, Loss 0.242934). Điều này lý giải bản chất toán học: Cross-Entropy Loss đo lường mức độ tự tin (confidence) của phân phối xác suất dự đoán trên toàn bộ các lớp, trong khi Accuracy chỉ là một hàm bước nhảy rời rạc dựa trên giá trị cực đại argmax. Một mô hình có thể có Accuracy cao hơn nếu đưa ra nhiều quyết định đúng sát nút, nhưng lại có Loss cao hơn nếu nó quá tự tin ở một vài dự đoán sai lầm. Do đó, việc theo dõi đồng thời cả Loss và Accuracy là bắt buộc trong nghiên cứu học thuật.")

    add_h2("10.6. Mối quan hệ giữa Accuracy, Precision, Recall và F1-Score")
    add_p("Trong các bài toán cân bằng như MNIST và Fashion-MNIST, 4 chỉ số này hầu như tiệm cận trùng khít nhau. Tuy nhiên, trên dữ liệu mất cân bằng như Diabetes, sự phân hóa bộc lộ rõ: Accuracy đạt 86.21%, Precision đạt 86.69%, nhưng Recall đạt 78.05% trên lớp bệnh nhân và F1 đạt 85.68%. Điều này khẳng định rằng trong các ứng dụng thực tế có sự chênh lệch chi phí sai lầm (asymmetric error cost), ta không bao giờ được phép chỉ dựa vào Accuracy đơn thuần.")

    add_h2("10.7. Trade-off giữa độ phức tạp mô hình và hiệu quả dự đoán")
    add_p("Thực nghiệm Assignment 05 là minh chứng điển hình cho bài toán đánh đổi kinh điển trong kỹ nghệ hệ thống thông minh: Giữa Năng lực dự đoán (Predictive Performance) và Chi phí tài nguyên (Computational / Memory Cost). M6 AlexNet đạt thêm 0.28 pp độ chính xác so với M4 trên Fashion-MNIST nhưng phải trả giá bằng số tham số gấp 67 lần. Trong các hệ thống nhúng (Edge AI) hoặc vi mạch xử lý thời gian thực, M3 hoặc M4 chắc chắn là sự lựa chọn tối ưu hơn hẳn.")

    add_h2("10.8. Vai trò của tính lặp lại (Reproducibility)")
    add_p("Bằng cách thiết lập cố định hạt giống ngẫu nhiên SEED = 42 cho cả Python random, NumPy và PyTorch, toàn bộ 18 lượt thực nghiệm cùng các biểu đồ trực quan hóa được đảm bảo tính lặp lại 100%. Đây là nền tảng cốt lõi của phương pháp luận nghiên cứu khoa học chuẩn mực.")

    add_h2("10.9. Ý nghĩa học thuật sâu sắc của Assignment 05")
    add_p("Assignment 05 đã hoàn thành xuất sắc sứ mệnh học thuật khi giúp sinh viên không chỉ nắm vững cách lập trình mạng tích chập bằng thư viện PyTorch, mà quan trọng hơn là thấu hiểu tường tận nguyên lý hoạt động nội tại của từng khối kỹ thuật, rèn luyện tư duy thực nghiệm có kiểm soát và năng lực phân tích dữ liệu đa chiều.")

    # -------------------------------------------------------------
    # CHƯƠNG 11: HẠN CHẾ CỦA THỰC NGHIỆM VÀ HƯỚNG PHÁT TRIỂN
    # -------------------------------------------------------------
    add_h1("11. HẠN CHẾ CỦA THỰC NGHIỆM VÀ HƯỚNG PHÁT TRIỂN")
    
    add_h2("11.1. Giới hạn số lượng epoch huấn luyện")
    add_p("Do giới hạn về thời gian thực thi trên phần cứng CPU (mỗi epoch MNIST mất khoảng 15-20 giây cho 54,000 ảnh), thực nghiệm chỉ tiến hành trong 5 epochs cho các tập dữ liệu ảnh. Dù 5 epochs là đủ để quan sát rõ rệt sự phân hóa giữa các kiến trúc, các mô hình dung lượng lớn như M6 và M7 hoàn toàn có thể đạt độ chính xác cao hơn nữa nếu được huấn luyện trong 20 - 30 epochs.")

    add_h2("11.2. Kích thước tập dữ liệu Diabetes nhỏ")
    add_p("Tập dữ liệu Pima Indians Diabetes chỉ có 768 mẫu, khiến tập kiểm thử chỉ vỏn vẹn 116 bệnh nhân. Kích thước mẫu nhỏ này khiến phương sai ước lượng tương đối lớn và làm hạn chế khả năng học của các khối chú ý phức tạp như SEBlock.")

    add_h2("11.3. Áp dụng Conv1D trên dữ liệu bảng phi cấu trúc không gian")
    add_p("Phép tích chập vốn được thiết kế dựa trên giả định về tính tương quan không gian liên tục cục bộ. Trong dữ liệu bảng, thứ tự sắp xếp của 8 cột thuộc tính là nhân tạo và không mang tính liên tục vật lý như các điểm ảnh lân cận. Dù Conv1D đạt kết quả rất khả quan (86.21%), việc áp dụng tích chập trên dữ liệu bảng vẫn đòi hỏi sự cẩn trọng về mặt lý thuyết.")

    add_h2("11.4. Bản chất thích nghi của các kiến trúc cổ điển")
    add_p("Các mô hình LeNet, AlexNet và VGG trong bài thực nghiệm là các phiên bản thu nhỏ (Adapted versions) được tinh chỉnh để nhận đầu vào ảnh xám 28×28, không phải là nguyên bản ImageNet (ảnh màu 224×224). Do đó, sự so sánh mang tính chất đối chuẩn kiến trúc chứ không phản ánh trọn vẹn sức mạnh tuyệt đối của phiên bản gốc.")

    add_h2("11.5. Thời gian huấn luyện phụ thuộc tài nguyên phần cứng CPU")
    add_p("Thời gian huấn luyện đo đạc chịu ảnh hưởng bởi tiến trình nền của hệ điều hành Windows và cơ chế quản lý xung nhịp CPU, không nên xem là một thuộc tính toán học cố định của thuật toán.")

    add_h2("11.6. Chưa áp dụng Data Augmentation và Hyperparameter Tuning sâu")
    add_p("Thực nghiệm chưa tích hợp các kỹ thuật tăng cường dữ liệu ảnh (xoay, dịch chuyển, cắt xén ngẫu nhiên) cũng như chưa thực hiện tìm kiếm siêu tham số tối ưu (Grid Search / Bayesian Optimization) cho learning rate và weight decay.")

    add_h2("11.7. Hướng phát triển và mở rộng trong tương lai")
    add_p("Các hướng phát triển tiếp theo đầy tiềm năng bao gồm: (1) Mở rộng sang các tập dữ liệu ảnh màu thực tế như CIFAR-10 và CIFAR-100; (2) Triển khai mô hình trên hạ tầng GPU với kiến trúc Vision Transformer (ViT); (3) Khảo sát các kỹ thuật nén mô hình như Lượng tử hóa (Quantization) và Cắt tỉa (Pruning) để triển khai trên thiết bị biên.")

    # -------------------------------------------------------------
    # CHƯƠNG 12: KẾT LUẬN TỔNG THỂ
    # -------------------------------------------------------------
    add_h1("12. KẾT LUẬN TỔNG THỂ")
    add_p("Assignment 05 đã cung cấp một bức tranh toàn cảnh, sâu sắc và thuyết phục về sức mạnh của Mạng Nơ-ron Tích chập (CNN). Thông qua 18 lượt thực nghiệm đối chuẩn nghiêm ngặt trên 3 tập dữ liệu đa dạng, báo cáo đã khẳng định vững chắc các kết luận khoa học cốt lõi sau:")
    add_bullet("Sự vượt trội của các kỹ thuật tiến hóa hiện đại: Chuẩn hóa theo lô (BatchNorm) giúp ổn định dòng gradient; Kết nối phần dư (Residual) giải quyết triệt để sự tắc nghẽn thông tin ở các tầng sâu; Cơ chế chú ý kênh (Squeeze-and-Excitation) giúp mạng tự động chọn lọc các kênh thông tin ngữ nghĩa quan trọng.")
    add_bullet("Hiệu quả tham số vượt bậc: Các mô hình cải tiến M3 và M4 chỉ với ~25k tham số đã đạt hiệu năng tiệm cận các mô hình kinh điển khổng lồ như AlexNet (1.7M tham số), tiết kiệm hơn 98% tài nguyên tính toán.")
    add_bullet("Sự cần thiết của phương pháp luận đối chuẩn chuẩn mực: Việc áp dụng Validation Checkpointing, kiểm tra tính toàn vẹn của tensor shape, và đánh giá đa chiều qua Accuracy, Loss, Precision, Recall, F1 và Confusion Matrix là điều kiện tiên quyết để tạo nên một hệ thống thông minh tin cậy và có khả năng ứng dụng thực tiễn cao.")

    # -------------------------------------------------------------
    # PHỤ LỤC
    # -------------------------------------------------------------
    add_h1("PHỤ LỤC: NGUỒN DỮ LIỆU KAGGLE VÀ CẤU TRÚC THƯ MỤC DỰ ÁN")
    add_h2("A. Đường dẫn dữ liệu chuẩn mực trên Kaggle")
    add_bullet("MNIST in CSV - Kaggle: https://www.kaggle.com/datasets/oddrationale/mnist-in-csv")
    add_bullet("Fashion-MNIST - Kaggle: https://www.kaggle.com/datasets/zalando-research/fashionmnist")
    add_bullet("Pima Indians Diabetes Database - Kaggle: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database")

    add_h2("B. Cấu trúc thư mục dự án và tệp mã nguồn thực thi")
    add_p("Toàn bộ mã nguồn, dữ liệu và báo cáo Assignment 05 được tổ chức chuyên nghiệp, khoa học theo đúng yêu cầu giảng viên:")
    add_bullet("notebooks/A05_06_taint_731.ipynb : Tệp Jupyter Notebook chính hoàn chỉnh, chứa toàn bộ mã nguồn thực thi, kiểm tra tensor shapes và hiển thị 11 biểu đồ trực quan hóa khoa học.")
    add_bullet("notebooks/assignment_05/A05_06_taint_731.ipynb : Bản sao lưu đồng bộ trong thư mục con để phục vụ trình chiếu.")
    add_bullet("data/ : Thư mục chứa trọn vẹn dữ liệu gốc đã tải về của MNIST, Fashion-MNIST và Diabetes.")
    add_bullet("ass5_experiments/plots/ : Thư mục chứa toàn bộ 16 tệp biểu đồ, sơ đồ và ma trận nhầm lẫn khoa học xuất ra từ thực nghiệm.")
    add_bullet("ass5_experiments/rendered_cells/ : Thư mục chứa 17 ảnh chụp cell thực thi Jupyter notebook sắc nét, không lỗi font do Playwright Chromium kết xuất.")
    add_bullet("ass5_experiments/artifacts/a05_metrics.json : Tệp lưu trữ toàn bộ số liệu đối chuẩn phục vụ phân tích.")
    add_bullet("A05_06_taint.731.docx : Báo cáo học thuật định dạng Microsoft Word đầy đủ 12 chương, chuẩn luận văn PTIT.")

    # Lưu tài liệu Word
    out_file = 'A05_06_taint.731.docx'
    doc.save(out_file)
    print(f"[OK] Đã xuất bản thành công báo cáo Word: {out_file}")
    
    # Sao lưu sang ass5/
    backup_file = 'ass5/A05_06_taint.731.docx'
    shutil.copyfile(out_file, backup_file)
    print(f"[OK] Đã sao lưu thành công sang: {backup_file}")

if __name__ == '__main__':
    build_a05_report()
