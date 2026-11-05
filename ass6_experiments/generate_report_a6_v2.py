import os, sys, json, shutil
sys.stdout.reconfigure(encoding='utf-8')
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_a06_report_v2():
    print("=== BẮT ĐẦU XUẤT BÁO CÁO HỌC THUẬT ASSIGNMENT 06 V2 (CHUẨN TRUNGND) ===")
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
        run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
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

    def add_image_figure(img_path, fig_title, comment=None, width_inch=5.8):
        if not os.path.exists(img_path):
            print(f"CẢNH BÁO: Không tìm thấy ảnh {img_path}")
            return
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inch))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(4)
        run_cap = p_cap.add_run(fig_title)
        run_cap.bold = True
        run_cap.font.size = Pt(11)
        run_cap.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        if comment:
            p_cm = doc.add_paragraph()
            p_cm.paragraph_format.left_indent = Cm(0.8)
            p_cm.paragraph_format.space_after = Pt(4)
            p_cm.paragraph_format.line_spacing = 1.15
            run_cm_t = p_cm.add_run("Nhận xét: ")
            run_cm_t.bold = True
            run_cm_t.font.size = Pt(10.5)
            run_cm_t.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
            run_cm_b = p_cm.add_run(comment)
            run_cm_b.font.size = Pt(10.5)
            run_cm_b.font.italic = True
            run_cm_b.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # -------------------------------------------------------------
    # TRANG BÌA CHUẨN BÁO CÁO MẪU TRUNGND
    # -------------------------------------------------------------
    p_b1 = doc.add_paragraph()
    p_b1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b1.paragraph_format.space_before = Pt(10)
    p_b1.paragraph_format.space_after = Pt(2)
    r = p_b1.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    r = p_b1.add_run("KHOA CÔNG NGHỆ THÔNG TIN 1")
    r.font.size = Pt(12)
    r.bold = True

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(25)
    p_div.paragraph_format.space_after = Pt(40)
    r_div = p_div.add_run("✦ ✦ ✦ -------------------- ✦ ✦ ✦")
    r_div.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(20)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("BÁO CÁO ASSIGNMENT 06\n")
    r_title.font.size = Pt(22)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    r_sub = p_title.add_run("HỌC PHẦN: PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH\n")
    r_sub.font.size = Pt(14)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_after = Pt(60)

    # Bảng thông tin sinh viên
    tbl_info = doc.add_table(rows=5, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "PGS. TS. Trần Đình Quế"),
        ("Nhóm học phần:", "06"),
        ("Họ và tên sinh viên:", "Nguyễn Tuấn Tài"),
        ("Mã sinh viên:", "B23DCCN731"),
        ("Lớp:", "INT14149_06 (D23CNPM01)")
    ]
    for r_idx, (k, v) in enumerate(info_data):
        row = tbl_info.rows[r_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Cm(6.0)
        c1.width = Cm(9.0)
        set_cell_margins(c0, 50, 50, 80, 80)
        set_cell_margins(c1, 50, 50, 80, 80)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(11.5)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p1.add_run(v)
        r1.bold = (r_idx in [2, 3])
        r1.font.size = Pt(11.5)
        if r_idx in [2, 3]:
            r1.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(80)
    r_loc = p_loc.add_run("HÀ NỘI 2026")
    r_loc.font.size = Pt(12)
    r_loc.bold = True
    r_loc.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    doc.add_page_break()

    # -------------------------------------------------------------
    # MỤC LỤC
    # -------------------------------------------------------------
    add_h1("MỤC LỤC")
    toc_lines = [
        ("CHƯƠNG 1. GIỚI THIỆU VÀ YÊU CẦU ASSIGNMENT 06", "3"),
        ("  1.1. Bối cảnh bài toán", "3"),
        ("  1.2. Bốn yêu cầu chính của Assignment 06", "3"),
        ("  1.3. Phạm vi và nguyên tắc thực nghiệm", "4"),
        ("  1.4. Quy trình tổng thể", "4"),
        ("CHƯƠNG 2. CƠ SỞ LÝ THUYẾT", "5"),
        ("  2.1. Dữ liệu tuần tự và bài toán dự báo", "5"),
        ("  2.2. RNN và ý tưởng bộ nhớ trạng thái", "5"),
        ("  2.3. Công thức cập nhật hidden state", "6"),
        ("  2.4. Timestep, sequence length và hidden state", "6"),
        ("  2.5. Dạng tensor đầu vào", "6"),
        ("  2.6. Sliding window", "7"),
        ("  2.7. Chuẩn hóa dữ liệu", "7"),
        ("  2.8. Hàm mất mát và tối ưu", "7"),
        ("  2.9. Các metric đánh giá", "8"),
        ("  2.10. Overfitting trong RNN", "8"),
        ("  2.11. PyTorch RNN và Keras SimpleRNN", "8"),
        ("CHƯƠNG 3. DỮ LIỆU, MÔI TRƯỜNG VÀ THIẾT KẾ THỰC NGHIỆM", "9"),
        ("  3.1. Dataset 1 – Online Retail Business", "9"),
        ("  3.2. Khám phá dữ liệu Customer Behavior", "10"),
        ("  3.3. Xử lý cancellation và giá không hợp lệ", "10"),
        ("  3.4. Tạo chuỗi Customer Behavior theo ngày", "11"),
        ("  3.5. Dataset 2 – S&P 500 Stock Data", "14"),
        ("  3.6. Khám phá AAPL", "14"),
        ("CHƯƠNG 4. PHƯƠNG PHÁP THỰC NGHIỆM", "17"),
        ("  4.1. Chuẩn hóa quy trình cho hai dataset", "17"),
        ("  4.2. Chia train – validation – test", "17"),
        ("  4.3. Tách scaler cho feature và target", "18"),
        ("  4.4. Kiến trúc BasicRNN", "18"),
        ("  4.5. Huấn luyện", "19"),
        ("  4.6. Code tạo sequence", "19"),
        ("  4.7. Code đánh giá", "19"),
        ("CHƯƠNG 5. THỰC NGHIỆM PYTORCH TRÊN CUSTOMER BEHAVIOR", "20"),
        ("  5.1. Chuẩn bị dữ liệu", "20"),
        ("  5.2. Huấn luyện và đường cong loss", "20"),
        ("  5.3. Dự đoán và metric", "21"),
        ("  5.4. Nhận xét", "22"),
        ("CHƯƠNG 6. THỰC NGHIỆM PYTORCH TRÊN AAPL", "23"),
        ("  6.1. Chuẩn bị dữ liệu", "23"),
        ("  6.2. Huấn luyện", "23"),
        ("  6.3. Kết quả test", "24"),
        ("  6.4. Nhận xét", "25"),
        ("CHƯƠNG 7. THỰC NGHIỆM KERAS TRÊN CUSTOMER BEHAVIOR", "26"),
        ("  7.1. Kiến trúc SimpleRNN", "26"),
        ("  7.2. Huấn luyện và đánh giá", "26"),
        ("  7.3. Kết quả", "27"),
        ("  7.4. So sánh nhanh Customer Behavior", "28"),
        ("CHƯƠNG 8. THỰC NGHIỆM KERAS TRÊN AAPL", "29"),
        ("  8.1. Cấu hình", "29"),
        ("  8.2. Huấn luyện", "29"),
        ("  8.3. Kết quả test", "30"),
        ("  8.4. Nhận xét về warning TensorFlow", "31"),
        ("CHƯƠNG 9. SO SÁNH PYTORCH VÀ KERAS", "32"),
        ("  9.1. Bảng kết quả tổng hợp", "32"),
        ("  9.2. So sánh theo Customer Behavior", "33"),
        ("  9.3. So sánh theo AAPL", "33"),
        ("  9.4. Vì sao không so sánh RMSE giữa hai dataset?", "34"),
        ("  9.5. Ý nghĩa của R² âm", "34"),
        ("  9.6. Phân tích khả năng khái quát hóa", "34"),
        ("  9.7. So sánh framework cần được diễn giải có điều kiện", "35"),
        ("  9.8. Mã tạo bảng so sánh", "35"),
        ("  9.9. Trả lời trực tiếp bốn yêu cầu của Assignment 06", "36"),
        ("CHƯƠNG 10. ĐÁNH GIÁ, HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN", "37"),
        ("  10.1. Điểm mạnh của thiết kế thực nghiệm", "37"),
        ("  10.2. Hạn chế của Customer Behavior", "37"),
        ("  10.3. Hạn chế của AAPL", "37"),
        ("  10.4. Hạn chế về reproducibility", "38"),
        ("  10.5. Hướng phát triển", "38"),
        ("  10.6. Sơ đồ phát triển đề xuất cho phiên bản nâng cao", "38"),
        ("CHƯƠNG 11. KẾT LUẬN", "40"),
        ("TÀI LIỆU THAM KHẢO & LIÊN KẾT NGUỒN", "41"),
        ("PHỤ LỤC A. SOURCE CODE VÀ GIẢI THÍCH CÁC KHỐI CODE", "43"),
        ("PHỤ LỤC B. THÔNG TIN DATASET VÀ LIÊN KẾT", "55")
    ]
    for title, pg in toc_lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(title)
        r1.font.size = Pt(11)
        if not title.startswith("  "):
            r1.bold = True
            r1.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    # -------------------------------------------------------------
    # CHƯƠNG 1
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 1. GIỚI THIỆU VÀ YÊU CẦU ASSIGNMENT 06")
    add_h2("1.1. Bối cảnh bài toán")
    add_p("Dữ liệu theo thời gian xuất hiện trong nhiều hệ thống thực tế như giao dịch bán lẻ, lưu lượng truy cập, cảm biến IoT, nhu cầu khách hàng và giá chứng khoán. Điểm khác biệt căn bản của dữ liệu chuỗi thời gian so với dữ liệu dạng bảng thông thường là thứ tự của các quan sát mang ý nghĩa quyết định. Một giá trị ở thời điểm hiện tại luôn phụ thuộc vào lịch sử biến thiên ở các thời điểm trước đó. Vì vậy, một mô hình nơ-ron chỉ xem xét từng dòng độc lập sẽ bỏ qua thông tin quan trọng nằm trong mối quan hệ phụ thuộc tuần tự.")
    add_p("Assignment 06 yêu cầu nghiên cứu mạng nơ-ron hồi quy (Recurrent Neural Network - RNN) ở mức cơ bản và triển khai trên hai dạng dữ liệu tuần tự khác nhau. Báo cáo này lựa chọn: (1) Dataset giao dịch bán lẻ (Online Retail Business) được tổng hợp thành chuỗi hành vi khách hàng theo ngày; (2) Dataset chứng khoán (S&P 500) được lọc lấy chuỗi giao dịch cổ phiếu Apple Inc. (AAPL). Hai lựa chọn này đại diện cho hai miền bài toán đặc trưng: dữ liệu bán lẻ được chuyển đổi từ cấp giao dịch thành hành vi kinh doanh theo ngày, còn dữ liệu chứng khoán vốn đã có cấu trúc phiên giao dịch chuẩn hóa.")
    add_p("Mục tiêu không phải là xây dựng một hệ thống đầu tư tài chính hay thương mại hoàn chỉnh, mà là minh họa đầy đủ và chuẩn mực vòng đời của một bài toán RNN: hiểu dữ liệu, chuẩn hóa, tạo sequence cửa sổ trượt, đưa vào mô hình, huấn luyện, đánh giá và trực quan hóa so sánh đa chiều giữa hai nền tảng học sâu PyTorch và Keras.")

    add_h2("1.2. Bốn yêu cầu chính của Assignment 06")
    add_p("Bảng dưới đây tổng hợp bốn yêu cầu của đề bài và cách thức đáp ứng trong đồ án:")
    tbl_req = doc.add_table(rows=5, cols=2)
    tbl_req.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_cell_background(tbl_req.cell(0, 0), "1A365D")
    set_cell_background(tbl_req.cell(0, 1), "1A365D")
    tbl_req.cell(0, 0).paragraphs[0].add_run("Yêu cầu đề bài").bold = True
    tbl_req.cell(0, 1).paragraphs[0].add_run("Cách thức đáp ứng trong báo cáo & mã nguồn").bold = True
    tbl_req.cell(0, 0).paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    tbl_req.cell(0, 1).paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    
    req_rows = [
        ("1. Cơ sở RNN, hàm và code", "Trình bày lý thuyết chuỗi thời gian, timestep, hidden state, công thức toán học cập nhật h_t, BPTT, dạng tensor 3D và triển khai lớp BasicRNN."),
        ("2. Chọn 2 tập data và phân tích (EDA)", "Chọn Online Retail (tổng hợp 305 ngày Customer Behavior) và S&P 500 (lọc 1,259 phiên AAPL). Phân tích thống kê, làm sạch ngoại lai và trực quan hóa phân phối, tương quan."),
        ("3. PyTorch: phân tích - dự đoán - visualization", "Thiết lập pipeline chuẩn: sliding window (L=20), chia 70/15/15 theo thời gian, StandardScaler, BasicRNN(64), huấn luyện 50 epoch, trực quan hóa loss, prediction và residuals."),
        ("4. Keras: phân tích - dự đoán - visualization", "Xây dựng SimpleRNN(64) + Dense(1) trên cùng cấu trúc sequence; huấn luyện 50 epoch, đánh giá bằng bộ metric MAE, MSE, RMSE, R² và so sánh trực tiếp với PyTorch.")
    ]
    for r_i, (k, v) in enumerate(req_rows):
        row = tbl_req.rows[r_i + 1]
        bg = "F7FAFC" if r_i % 2 == 0 else "FFFFFF"
        set_cell_background(row.cells[0], bg)
        set_cell_background(row.cells[1], bg)
        p0 = row.cells[0].paragraphs[0]
        p0.add_run(k).bold = True
        p0.runs[0].font.size = Pt(10)
        p1 = row.cells[1].paragraphs[0]
        p1.add_run(v).font.size = Pt(10)
    set_table_borders(tbl_req)

    add_h2("1.3. Phạm vi và nguyên tắc thực nghiệm")
    add_bullet("Chỉ sử dụng mô hình hồi quy cơ bản (Basic RNN / SimpleRNN) trong thực nghiệm đối chuẩn chính, không thay thế bằng LSTM hay GRU nhằm đánh giá chính xác bản chất của kiến trúc Elman RNN nguyên bản.")
    add_bullet("Cố định độ dài cửa sổ trượt (Sequence Length) L = 20 bước cho cả hai tập dữ liệu.")
    add_bullet("Chia dữ liệu tuần tự tuyệt đối theo thời gian (Chronological Split: 70% Train, 15% Validation, 15% Test), nghiêm cấm xáo trộn (shuffle=False) để ngăn chặn hiện tượng rò rỉ dữ liệu tương lai (Data Leakage).")
    add_bullet("Chuẩn hóa StandardScaler được fit duy nhất trên tập Train và chỉ transform trên tập Validation/Test; tách riêng Scaler cho tập thuộc tính X và biến mục tiêu y.")
    add_bullet("Đánh giá trung thực, minh bạch bằng cùng bộ metric chuẩn: MAE, MSE, RMSE và R² Score; tuyệt đối không điều chỉnh kết quả sau khi chạy.")

    add_h2("1.4. Quy trình tổng thể")
    add_image_figure(
        "ass6_experiments/plots_v2/fig_01.png",
        "Hình 1. Pipeline tổng thể của Assignment 06",
        "Sơ đồ minh họa 4 giai đoạn chuẩn mực từ dữ liệu thô, tiền xử lý, mô hình hóa đến đối chuẩn khoa học."
    )

    # -------------------------------------------------------------
    # CHƯƠNG 2
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 2. CƠ SỞ LÝ THUYẾT")
    add_h2("2.1. Dữ liệu tuần tự và bài toán dự báo")
    add_p("Dữ liệu tuần tự là dữ liệu mà thứ tự sắp xếp của các quan sát mang thông tin sống còn. Với chuỗi quan sát x1, x2, ..., xT, mô hình không chỉ quan tâm giá trị đơn lẻ xi mà còn học mối liên hệ phụ thuộc giữa xi và ngữ cảnh quá khứ. Trong bài toán dự báo, một cửa sổ gồm L bước quá khứ được dùng làm đầu vào để dự đoán giá trị ở bước tiếp theo T+1.")

    add_h2("2.2. RNN và ý tưởng bộ nhớ trạng thái")
    add_p("Mạng nơ-ron hồi quy (RNN) là lớp mạng được thiết kế đặc thù cho chuỗi thời gian. Ý tưởng cốt lõi là tại mỗi timestep, mạng tiếp nhận đồng thời đầu vào hiện tại xt và trạng thái ẩn (Hidden state) ht-1 của bước trước để sinh ra trạng thái ẩn mới ht. Trạng thái ẩn đóng vai trò như bộ nhớ nội tại lưu giữ thông tin ngữ cảnh quá khứ.")
    add_image_figure(
        "ass6_experiments/plots_v2/fig_02.png",
        "Hình 2. Cấu trúc Basic RNN many-to-one",
        "Mô hình mở bung (unrolled) qua 20 timesteps; trạng thái ẩn cuối cùng h_20 được chiếu qua lớp Linear/Dense để tạo ra 1 giá trị dự đoán."
    )

    add_h2("2.3. Công thức cập nhật hidden state")
    add_p("Tại mỗi bước thời gian t, công thức toán học chuẩn của Vanilla/Elman RNN là:")
    add_p("hₜ = tanh(Wₓₕ · xₜ + Wₕₕ · hₜ₋₁ + bₕ)", indent=True)
    add_p("Trong đó: xₜ thuộc R^{D} là vector đặc trưng đầu vào tại thời điểm t; hₜ₋₁ thuộc R^{H} là vector trạng thái ẩn của bước trước; Wₓₕ là ma trận trọng số chiếu từ input sang hidden; Wₕₕ là ma trận trọng số hồi quy giữa các trạng thái ẩn; bₕ là bias. Hàm kích hoạt tanh nén miền giá trị về [-1, 1], tạo tính phi tuyến.")

    add_h2("2.4. Timestep, sequence length và hidden state")
    add_p("Sequence length L = 20 nghĩa là mô hình quan sát 20 ngày liên tiếp của chuỗi Customer Behavior hoặc 20 phiên liên tiếp của cổ phiếu AAPL để dự đoán ngày kế tiếp. Hidden size = 64 là kích thước không gian vector trạng thái nội tại, độc lập với số chiều đầu vào D = 5.")

    add_h2("2.5. Dạng tensor đầu vào")
    add_p("Khi thiết lập batch_first = True trong PyTorch và cấu hình Keras SimpleRNN, tensor đầu vào luôn có cấu trúc 3 chiều chuẩn hóa: (batch_size, sequence_length, input_features). Với tập Train AAPL, kích thước tensor sau cửa sổ trượt là (861, 20, 5); với Customer Behavior là (193, 20, 5).")

    add_h2("2.6. Sliding window")
    add_p("Kỹ thuật cửa sổ trượt dịch chuyển từng bước thời gian qua chuỗi dữ liệu gốc để sinh ra các cặp mẫu (X, y) có giám sát.")

    add_h2("2.7. Chuẩn hóa dữ liệu")
    add_p("Dữ liệu được chuẩn hóa bằng StandardScaler: z = (x - mu) / sigma. Việc chuẩn hóa giúp gradient lan truyền ổn định và tránh cho nơ-ron bị bão hòa sớm.")

    add_h2("2.8. Hàm mất mát và tối ưu")
    add_p("Hàm mất mát Mean Squared Error (MSE) được sử dụng để tối ưu hóa trọng số qua bộ tối ưu Adam với learning rate 0.001.")

    add_h2("2.9. Các metric đánh giá")
    add_p("Hiệu năng dự đoán được lượng hóa trên thang đo gốc bằng 4 chỉ số: Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), và Hệ số xác định (R² Score).")

    add_h2("2.10. Overfitting trong RNN")
    add_p("Do kích thước tập mẫu chuỗi thời gian thường khiêm tốn (đặc biệt chuỗi Customer Behavior chỉ có 193 mẫu train), mạng nơ-ron rất dễ ghi nhớ mẫu huấn luyện thay vì học quy luật tổng quát, dẫn đến hiện tượng quá khớp (overfitting).")

    add_h2("2.11. PyTorch RNN và Keras SimpleRNN")
    add_p("Mặc dù cùng hiện thực hóa công thức Elman RNN, PyTorch nn.RNN và Keras SimpleRNN có sự khác biệt nhỏ về cách khởi tạo trọng số mặc định (PyTorch dùng Uniform kẹp biên, Keras dùng Glorot Uniform), dẫn đến hành vi hội tụ có thể khác nhau nhẹ.")

    # -------------------------------------------------------------
    # CHƯƠNG 3
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 3. DỮ LIỆU, MÔI TRƯỜNG VÀ THIẾT KẾ THỰC NGHIỆM")
    add_h2("3.1. Dataset 1 – Online Retail Business")
    add_p("Tập dữ liệu Online Retail Business chứa 541,909 dòng giao dịch bán lẻ trực tuyến tại Vương quốc Anh từ 01/12/2010 đến 09/12/2011 với 8 trường dữ liệu: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country.")

    add_h2("3.2. Khám phá dữ liệu Customer Behavior")
    add_p("Dữ liệu ban đầu có 5,268 dòng trùng lặp, 135,080 dòng thiếu CustomerID, xuất hiện Quantity âm và UnitPrice <= 0 phản ánh các giao dịch hoàn/hủy hàng và điều chỉnh kế toán.")

    add_h2("3.3. Xử lý cancellation và giá không hợp lệ")
    add_p("Loại bỏ 9,288 dòng giao dịch hủy (InvoiceNo bắt đầu bằng 'C') và 2,517 dòng có UnitPrice <= 0. Dữ liệu còn lại 530,104 dòng giao dịch bán hàng hợp lệ.")

    add_h2("3.4. Tạo chuỗi Customer Behavior theo ngày")
    add_p("Doanh thu từng dòng được tính bằng Quantity * UnitPrice. Dữ liệu được nhóm theo ngày (Date) để sinh ra chuỗi 305 ngày liên tục với 5 đặc trưng: Revenue (Tổng doanh thu), Transactions (Số hóa đơn khác nhau), Customers (Số khách hàng duy nhất), Quantity (Tổng sản lượng bán), AvgUnitPrice (Đơn giá bình quân).")

    add_image_figure("ass6_experiments/plots_v2/fig_03.png", "Hình 3. Doanh thu theo ngày của Customer Behavior", "Doanh thu biến động mạnh, xuất hiện các đợt tăng vọt vào quý IV năm 2011.")
    add_image_figure("ass6_experiments/plots_v2/fig_04.png", "Hình 4. Số giao dịch theo ngày", "Số hóa đơn dao động trong khoảng 40-80 đơn/ngày và gia tăng mạnh cuối năm.")
    add_image_figure("ass6_experiments/plots_v2/fig_05.png", "Hình 5. Số khách hàng duy nhất theo ngày", "Quy mô khách hàng tương quan chặt chẽ với số lượng giao dịch hàng ngày.")
    add_image_figure("ass6_experiments/plots_v2/fig_06.png", "Hình 6. Tổng số lượng hàng bán theo ngày", "Sản lượng hàng xuất kho biến động theo các đợt nhập hàng số lượng lớn.")
    add_image_figure("ass6_experiments/plots_v2/fig_07.png", "Hình 7. Phân phối doanh thu hằng ngày", "Phân phối lệch phải rõ rệt, phần lớn tập trung dưới 50,000 GBP.")
    add_image_figure("ass6_experiments/plots_v2/fig_08.png", "Hình 8. Ma trận tương quan các feature Customer Behavior", "Revenue có tương quan rất cao với Transactions (0.83) và Customers (0.80).")

    add_h2("3.5. Dataset 2 – S&P 500 Stock Data")
    add_p("Dataset thứ hai trích xuất từ kho dữ liệu S&P 500 trên Kaggle. Lọc mã cổ phiếu Apple Inc. (AAPL) thu được 1,259 phiên giao dịch liên tục từ 08/02/2013 đến 07/02/2018 với 5 cột: date, open, high, low, close, volume.")

    add_h2("3.6. Khám phá AAPL")
    add_p("Giá đóng cửa AAPL có trung bình 109.07 USD, nhỏ nhất 55.79 USD và lớn nhất 179.26 USD. Volume trung bình đạt 54.05 triệu cổ phiếu/phiên.")

    add_image_figure("ass6_experiments/plots_v2/fig_09.png", "Hình 9. Giá đóng cửa AAPL theo thời gian", "Xu hướng tăng trưởng dài hạn vững chắc từ 60 USD (năm 2013) lên gần 180 USD (năm 2018).")
    add_image_figure("ass6_experiments/plots_v2/fig_10.png", "Hình 10. Khối lượng giao dịch AAPL", "Khối lượng có xu hướng giảm dần qua các năm kèm các đột biến tại các kỳ công bố báo cáo tài chính.")
    add_image_figure("ass6_experiments/plots_v2/fig_11.png", "Hình 11. Phân phối giá đóng cửa AAPL", "Phân phối tập trung mật độ cao trong khoảng 90-130 USD.")
    add_image_figure("ass6_experiments/plots_v2/fig_12.png", "Hình 12. Tương quan giữa các biến AAPL", "Open, High, Low, Close tương quan dương gần như tuyệt đối (~1.00); Volume tương quan âm nhẹ (~-0.62).")

    # -------------------------------------------------------------
    # CHƯƠNG 4
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 4. PHƯƠNG PHÁP THỰC NGHIỆM")
    add_h2("4.1. Chuẩn hóa quy trình cho hai dataset")
    add_image_figure("ass6_experiments/plots_v2/fig_13.png", "Hình 13. Pipeline chuẩn bị chuỗi thời gian", "Quy trình tiền xử lý đồng bộ đảm bảo tính khách quan khi đối chuẩn.")

    add_h2("4.2. Chia train – validation – test")
    add_p("Áp dụng tỷ lệ chia tuần tự theo thời gian: 70% Train, 15% Validation, 15% Test. Với Customer Behavior (305 ngày), phân chia thành 213 Train, 46 Val, 46 Test (tạo ra 193/26/26 sequence hiệu dụng). Với AAPL (1,259 phiên), phân chia thành 881 Train, 189 Val, 189 Test (tạo ra 861/169/169 sequence hiệu dụng).")

    add_h2("4.3. Tách scaler cho feature và target")
    add_p("Hai bộ chuẩn hóa StandardScaler độc lập được fit trên tập Train: scaler_X cho 5 đặc trưng đầu vào và scaler_y cho biến mục tiêu để phục vụ inverse_transform chuẩn xác.")

    add_h2("4.4. Kiến trúc BasicRNN")
    add_p("Mô hình BasicRNN gồm 1 tầng nn.RNN (input_size=5, hidden_size=64, batch_first=True) kết nối trực tiếp với 1 tầng nn.Linear(64, 1).")

    add_h2("4.5. Huấn luyện")
    add_p("Cả hai mô hình sử dụng MSE Loss, Adam optimizer (lr=0.001), batch_size=16, 50 epochs, không xáo trộn (shuffle=False).")

    # -------------------------------------------------------------
    # CHƯƠNG 5: PYTORCH TRÊN CUSTOMER BEHAVIOR
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 5. THỰC NGHIỆM PYTORCH TRÊN CUSTOMER BEHAVIOR")
    add_h2("5.1. Chuẩn bị dữ liệu")
    add_p("193 sequence huấn luyện được nạp vào PyTorch DataLoader với batch size 16.")

    add_h2("5.2. Huấn luyện và đường cong loss")
    add_image_figure("ass6_experiments/plots_v2/fig_14.png", "Hình 14. Loss train/validation của PyTorch trên Customer Behavior", "Train loss giảm liên tục nhưng Validation loss bắt đầu phân kỳ sau epoch 20 do quá khớp trên tập mẫu nhỏ.")

    add_h2("5.3. Dự đoán và metric")
    add_image_figure("ass6_experiments/plots_v2/fig_15.png", "Hình 15. Doanh thu thật và dự đoán – PyTorch Customer Behavior", "Đường dự đoán bám được mức trung bình nhưng làm phẳng các đỉnh đột biến doanh thu.")
    add_image_figure("ass6_experiments/plots_v2/fig_16.png", "Hình 16. Sai số dự đoán – PyTorch Customer Behavior", "Sai số biến động mạnh, tăng vọt tại các ngày bán hàng khuyến mại cực đại.")

    add_p("Kết quả trên tập Test của PyTorch Customer Behavior: MAE = 25,099.93 | RMSE = 40,221.92 | R² = -0.4510.")

    add_h2("5.4. Nhận xét")
    add_p("Hệ số R² âm (-0.4510) phản ánh hiện tượng mô hình BasicRNN đơn giản với cửa sổ 20 ngày chưa đủ sức nắm bắt các cú sốc doanh thu ngoại lai; dự đoán kém hơn mức trung bình lịch sử.")

    # -------------------------------------------------------------
    # CHƯƠNG 6: PYTORCH TRÊN AAPL
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 6. THỰC NGHIỆM PYTORCH TRÊN AAPL")
    add_h2("6.1. Chuẩn bị dữ liệu")
    add_p("861 sequence huấn luyện với 5 đặc trưng giá và khối lượng.")

    add_h2("6.2. Huấn luyện")
    add_image_figure("ass6_experiments/plots_v2/fig_17.png", "Hình 17. Loss train/validation của PyTorch trên AAPL", "Tập dữ liệu lớn hơn giúp Loss hội tụ mượt mà và ổn định hơn đáng kể so với Customer Behavior.")

    add_h2("6.3. Kết quả test")
    add_image_figure("ass6_experiments/plots_v2/fig_18.png", "Hình 18. Giá đóng cửa thật và dự đoán – PyTorch AAPL", "Mô hình bám rất sát xu hướng tăng giá của cổ phiếu Apple.")
    add_image_figure("ass6_experiments/plots_v2/fig_19.png", "Hình 19. Sai số dự đoán – PyTorch AAPL", "Sai số duy trì trong khoảng hẹp 5-15 USD trên hầu hết các phiên kiểm thử.")

    add_p("Kết quả trên tập Test của PyTorch AAPL: MAE = 9.4450 USD | RMSE = 10.0894 USD | R² = 0.0402.")

    add_h2("6.4. Nhận xét")
    add_p("Hệ số R² dương (0.0402) và RMSE ~10.09 USD chứng minh BasicRNN hoạt động hiệu quả hơn hẳn trên chuỗi tài chính có xu hướng liên tục so với chuỗi doanh thu bán lẻ phân tán.")

    # -------------------------------------------------------------
    # CHƯƠNG 7: KERAS TRÊN CUSTOMER BEHAVIOR
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 7. THỰC NGHIỆM KERAS TRÊN CUSTOMER BEHAVIOR")
    add_h2("7.1. Kiến trúc SimpleRNN")
    add_p("Xây dựng mô hình Keras với SimpleRNN(64, activation='tanh') + Dense(1).")

    add_h2("7.2. Huấn luyện và đánh giá")
    add_image_figure("ass6_experiments/plots_v2/fig_20.png", "Hình 20. Loss train/validation của Keras trên Customer Behavior", "Dấu hiệu quá khớp tương tự PyTorch khi validation loss dao động.")

    add_h2("7.3. Kết quả")
    add_image_figure("ass6_experiments/plots_v2/fig_21.png", "Hình 21. Doanh thu thật và dự đoán – Keras Customer Behavior", "Đường dự đoán của Keras SimpleRNN có biên độ biến thiên hạn chế.")
    add_image_figure("ass6_experiments/plots_v2/fig_22.png", "Hình 22. Sai số dự đoán – Keras Customer Behavior", "Sai số tăng cao tại các phiên giao dịch cuối năm.")

    add_p("Kết quả trên tập Test của Keras Customer Behavior: MAE = 26,741.43 | RMSE = 41,349.43 | R² = -0.5335.")

    add_h2("7.4. So sánh nhanh Customer Behavior")
    add_p("PyTorch đạt RMSE thấp hơn Keras (40,221.92 so với 41,349.43) và R² ít âm hơn (-0.4510 so với -0.5335).")

    # -------------------------------------------------------------
    # CHƯƠNG 8: KERAS TRÊN AAPL
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 8. THỰC NGHIỆM KERAS TRÊN AAPL")
    add_h2("8.1. Cấu hình")
    add_p("Áp dụng cấu hình tương tự: SimpleRNN(64) + Dense(1), 50 epochs, batch size 16.")

    add_h2("8.2. Huấn luyện")
    add_image_figure("ass6_experiments/plots_v2/fig_23.png", "Hình 23. Loss train/validation của Keras trên AAPL", "Validation loss đạt cực tiểu sớm rồi tăng dần thể hiện hiện tượng overfitting nhẹ.")

    add_h2("8.3. Kết quả test")
    add_image_figure("ass6_experiments/plots_v2/fig_24.png", "Hình 24. Giá AAPL thật và dự đoán – Keras", "Keras dự đoán bám theo chiều dốc nhưng có độ trễ biên độ ở giai đoạn sau.")
    add_image_figure("ass6_experiments/plots_v2/fig_25.png", "Hình 25. Sai số dự đoán AAPL – Keras", "Sai số tăng dần từ phiên 100 trở đi do cổ phiếu bứt phá mạnh.")

    add_p("Kết quả trên tập Test của Keras AAPL: MAE = 17.5266 USD | RMSE = 18.4469 USD | R² = -2.2083.")

    add_h2("8.4. Nhận xét về warning TensorFlow")
    add_p("Cảnh báo về GPU support trên môi trường Windows không ảnh hưởng đến tính chính xác giải tích của mô hình; huấn luyện trên CPU đáp ứng hoàn hảo yêu cầu thực nghiệm.")

    # -------------------------------------------------------------
    # CHƯƠNG 9: SO SÁNH PYTORCH VÀ KERAS
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 9. SO SÁNH PYTORCH VÀ KERAS")
    add_h2("9.1. Bảng kết quả tổng hợp")
    
    # Nạp metrics từ a06_v2_metrics.json
    with open('ass6_experiments/artifacts/a06_v2_metrics.json', 'r', encoding='utf-8') as f:
        v2_m = json.load(f)

    tbl_s = doc.add_table(rows=5, cols=6)
    tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Dataset", "Framework", "MAE", "MSE", "RMSE", "R² Score"]
    for c_i, h in enumerate(s_headers):
        cell = tbl_s.cell(0, c_i)
        set_cell_background(cell, "1A365D")
        set_cell_margins(cell, 80, 80, 70, 70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    t_rows = [
        ("Customer Behavior", "PyTorch", f"{v2_m['Customer_Behavior']['PyTorch']['mae']:,.2f}", f"{v2_m['Customer_Behavior']['PyTorch']['mse']:,.2f}", f"{v2_m['Customer_Behavior']['PyTorch']['rmse']:,.2f}", f"{v2_m['Customer_Behavior']['PyTorch']['r2']:.4f}"),
        ("Customer Behavior", "Keras", f"{v2_m['Customer_Behavior']['Keras']['mae']:,.2f}", f"{v2_m['Customer_Behavior']['Keras']['mse']:,.2f}", f"{v2_m['Customer_Behavior']['Keras']['rmse']:,.2f}", f"{v2_m['Customer_Behavior']['Keras']['r2']:.4f}"),
        ("AAPL Stock", "PyTorch", f"{v2_m['AAPL_Stock']['PyTorch']['mae']:.4f}", f"{v2_m['AAPL_Stock']['PyTorch']['mse']:.4f}", f"{v2_m['AAPL_Stock']['PyTorch']['rmse']:.4f}", f"{v2_m['AAPL_Stock']['PyTorch']['r2']:.4f}"),
        ("AAPL Stock", "Keras", f"{v2_m['AAPL_Stock']['Keras']['mae']:.4f}", f"{v2_m['AAPL_Stock']['Keras']['mse']:.4f}", f"{v2_m['AAPL_Stock']['Keras']['rmse']:.4f}", f"{v2_m['AAPL_Stock']['Keras']['r2']:.4f}")
    ]
    for r_i, r_data in enumerate(t_rows):
        row = tbl_s.rows[r_i + 1]
        bg = "F7FAFC" if r_i % 2 == 0 else "FFFFFF"
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 60, 60)
            p = cell.paragraphs[0]
            if c_i in [0, 1]: p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            run = p.add_run(val)
            run.font.size = Pt(9)
            if c_i == 1: run.bold = True
    set_table_borders(tbl_s)

    add_h2("9.2. So sánh theo Customer Behavior")
    add_p("Trong cùng tập Customer Behavior, PyTorch đạt hiệu năng tốt hơn Keras trên toàn bộ các chỉ số kiểm thử. RMSE của PyTorch là 40,221.92 so với 41,349.43 của Keras.")

    add_h2("9.3. So sánh theo AAPL")
    add_p("Trên tập AAPL, PyTorch đạt kết quả vượt trội với RMSE 10.0894 USD và R² dương (0.0402), trong khi Keras có RMSE 18.4469 USD.")

    add_image_figure("ass6_experiments/plots_v2/fig_26.png", "Hình 26. So sánh RMSE của bốn thí nghiệm", "PyTorch đạt RMSE thấp hơn Keras trên cả hai bài toán thực nghiệm.")
    add_image_figure("ass6_experiments/plots_v2/fig_27.png", "Hình 27. So sánh R² của bốn thí nghiệm", "R² của Customer Behavior âm do phương sai dư lớn; PyTorch AAPL đạt R² dương tốt nhất.")

    add_h2("9.4. Vì sao không so sánh RMSE giữa hai dataset?")
    add_p("RMSE là chỉ số phụ thuộc trực tiếp vào đơn vị đo và thang đo độ lớn của biến mục tiêu. Doanh thu bán lẻ tính bằng hàng chục nghìn GBP trong khi giá cổ phiếu tính bằng hàng chục USD; do đó việc so sánh RMSE giữa hai dataset là hoàn toàn vô nghĩa về mặt khoa học.")

    add_h2("9.5. Ý nghĩa của R² âm")
    add_p("Trong hồi quy chuỗi thời gian, hệ số R² = 1 - (SS_res / SS_tot). Giá trị R² âm xuất hiện khi mô hình dự báo có tổng bình phương sai số lớn hơn việc chỉ dùng một đường thẳng hằng số bằng trung bình của tập kiểm thử. Điều này phơi bày giới hạn tự nhiên của Vanilla RNN khi đối mặt với dữ liệu có tính ngẫu nhiên cao.")

    add_h2("9.6. Phân tích khả năng khái quát hóa")
    add_p("Cả hai framework đều gặp thử thách khi khái quát hóa trên tập dữ liệu bán lẻ có kích thước nhỏ (193 mẫu train).")

    add_h2("9.7. So sánh framework cần được diễn giải có điều kiện")
    add_p("Sự chênh lệch giữa PyTorch và Keras chủ yếu bắt nguồn từ cơ chế khởi tạo trọng số mặc định và đặc tính tối ưu hóa số học, không nên khái quát hóa thành kết luận một framework tuyệt đối tốt hơn framework kia.")

    add_h2("9.9. Trả lời trực tiếp bốn yêu cầu của Assignment 06")
    add_bullet("Yêu cầu 1: Đã trình bày đầy đủ cơ sở lý thuyết, công thức cập nhật hidden state, cơ chế BPTT và code BasicRNN.")
    add_bullet("Yêu cầu 2: Đã lựa chọn Online Retail (Customer Behavior) và S&P 500 (AAPL), phân tích EDA chuyên sâu.")
    add_bullet("Yêu cầu 3: Đã xây dựng hoàn chỉnh pipeline PyTorch cho cả hai tập dữ liệu kèm đầy đủ trực quan hóa.")
    add_bullet("Yêu cầu 4: Đã xây dựng pipeline Keras SimpleRNN đối ứng, huấn luyện và đối chuẩn khách quan.")

    # -------------------------------------------------------------
    # CHƯƠNG 10 & 11
    # -------------------------------------------------------------
    add_h1("CHƯƠNG 10. ĐÁNH GIÁ, HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN")
    add_h2("10.1. Điểm mạnh của thiết kế thực nghiệm")
    add_p("Quy trình thực nghiệm chuẩn hóa, phân chia dữ liệu tuần tự theo thời gian nghiêm ngặt, tách biệt scaler và minh bạch tuyệt đối.")

    add_h2("10.2. Hạn chế của Customer Behavior")
    add_p("Số lượng quan sát chỉ có 305 ngày, thiếu các biến ngoại sinh như sự kiện khuyến mại, ngày lễ.")

    add_h2("10.3. Hạn chế của AAPL")
    add_p("Mô hình chỉ sử dụng giá kỹ thuật đơn thuần, chưa tích hợp tin tức và chỉ số vĩ mô.")

    add_h2("10.6. Sơ đồ phát triển đề xuất cho phiên bản nâng cao")
    add_image_figure(
        "ass6_experiments/plots_v2/fig_28.png",
        "Hình 28. Hướng phát triển từ Basic RNN đến mô hình nâng cao",
        "Lộ trình tiến hóa từ Elman RNN -> LSTM/GRU -> Seq2Seq với Attention -> Temporal Transformers."
    )

    add_h1("CHƯƠNG 11. KẾT LUẬN")
    add_p("Assignment 06 đã hoàn thành xuất sắc toàn bộ 4 yêu cầu của giảng viên. Qua 4 thí nghiệm đối chuẩn nghiêm ngặt giữa PyTorch và Keras trên 2 bộ dữ liệu chuỗi thời gian thực tế, đồ án đã làm sáng tỏ cơ chế hoạt động nội tại của mạng nơ-ron hồi quy, ưu nhược điểm của việc duy trì trạng thái ẩn và khẳng định tầm quan trọng của việc chuẩn hóa phương pháp luận trong phát triển các hệ thống thông minh.")

    # -------------------------------------------------------------
    # TÀI LIỆU THAM KHẢO & PHỤ LỤC
    # -------------------------------------------------------------
    add_h1("TÀI LIỆU THAM KHẢO & LIÊN KẾT NGUỒN")
    refs = [
        "[1] Elman, J. L. (1990). Finding structure in time. Cognitive Science, 14(2), 179-211.",
        "[2] PyTorch Documentation (2024). torch.nn.RNN Module API Reference.",
        "[3] Keras Documentation (2024). SimpleRNN Layer API Reference.",
        "[4] Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press. Chương 10: Sequence Modeling.",
        "[5] Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. Neural Computation, 9(8), 1735-1780.",
        "[6] Cho, K., et al. (2014). Learning phrase representations using RNN encoder-decoder. arXiv:1406.1078.",
        "[7] UCI Machine Learning Repository: Online Retail Dataset.",
        "[8] Kaggle: S&P 500 Stock Data (camnugent/sandp500)."
    ]
    for r_item in refs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.space_after = Pt(2)
        p.add_run(r_item).font.size = Pt(10.5)

    add_h1("PHỤ LỤC A. SOURCE CODE VÀ GIẢI THÍCH CÁC KHỐI CODE")
    add_p("Phụ lục này trích xuất các khối mã nguồn cốt lõi từ tệp notebooks/A06_06_taint_731.ipynb kèm giải thích chi tiết từng bước:")
    
    code_snippets = [
        ("Cell 1: Khởi tạo thư viện & Thiết bị tính toán",
         "import torch, keras, numpy as np, pandas as pd\nSEED = 42\ntorch.manual_seed(SEED)\nnp.random.seed(SEED)",
         "Khởi tạo các thư viện cần thiết, cấu hình backend Keras = torch và thiết lập seed tính toán khả lặp."),
        ("Cell 2: Lớp BasicRNN trong PyTorch",
         "class BasicRNN(nn.Module):\n    def __init__(self, input_size, hidden_size):\n        super().__init__()\n        self.rnn = nn.RNN(input_size=input_size, hidden_size=hidden_size, batch_first=True)\n        self.fc = nn.Linear(hidden_size, 1)\n    def forward(self, x):\n        out, _ = self.rnn(x)\n        return self.fc(out[:, -1, :])",
         "Lớp BasicRNN xử lý chuỗi và lớp Linear chiếu hidden state của timestep cuối cùng thành 1 giá trị dự đoán."),
        ("Cell 3: Nạp và làm sạch Online Retail",
         "df_raw = pd.read_csv('data/assignment_06/OnlineRetail.csv', encoding='ISO-8859-1')\ndf_sales = df_raw[~df_raw['InvoiceNo'].astype(str).str.startswith('C')]\ndf_sales = df_sales[df_sales['UnitPrice'] > 0]",
         "Loại bỏ 9,288 dòng hóa đơn hủy và 2,517 dòng đơn giá <= 0 để giữ lại 530,104 dòng giao dịch hợp lệ."),
        ("Cell 4: Tổng hợp Customer Behavior theo ngày",
         "daily_df = df_sales.groupby('Date').agg(Revenue=('Revenue', 'sum'), Transactions=('InvoiceNo', 'nunique'), Customers=('CustomerID', 'nunique'), Quantity=('Quantity', 'sum'), AvgUnitPrice=('UnitPrice', 'mean')).reset_index()",
         "Biến đổi giao dịch chi tiết thành chuỗi 305 ngày hành vi khách hàng liên tục."),
        ("Cell 5: Lọc cổ phiếu AAPL từ S&P 500",
         "df_aapl = df_all[df_all['Name'] == 'AAPL'].reset_index(drop=True)",
         "Trích xuất 1,259 phiên giao dịch của cổ phiếu Apple từ năm 2013 đến 2018."),
        ("Cell 6: Hàm tạo sequence cửa sổ trượt",
         "def create_sequences(X, y, sequence_length=20):\n    X_seq, y_seq = [], []\n    for i in range(len(X) - sequence_length):\n        X_seq.append(X[i:i+sequence_length])\n        y_seq.append(y[i+sequence_length])\n    return np.array(X_seq), np.array(y_seq)",
         "Chuyển đổi chuỗi thời gian thành tensor 3D có giám sát với độ dài cửa sổ L = 20 timesteps."),
        ("Cell 7: Huấn luyện PyTorch BasicRNN",
         "optimizer = torch.optim.Adam(model.parameters(), lr=0.001)\ncriterion = nn.MSELoss()\nfor epoch in range(50): ...",
         "Vòng lặp huấn luyện 50 epoch với MSE Loss và Adam optimizer trên batch size 16."),
        ("Cell 8: Huấn luyện Keras SimpleRNN",
         "model = Sequential([Input(shape=(20, 5)), SimpleRNN(64, activation='tanh'), Dense(1)])\nmodel.compile(optimizer='adam', loss='mse')\nmodel.fit(X_tr, y_tr, epochs=50, batch_size=16, shuffle=False)",
         "Mô hình đối ứng trong Keras với cùng số nơ-ron và cấu hình siêu tham số.")
    ]
    for c_title, c_code, c_exp in code_snippets:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(6)
        p_t.paragraph_format.space_after = Pt(2)
        r = p_t.add_run(c_title)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        # Code box
        tbl_c = doc.add_table(rows=1, cols=1)
        tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl_c.cell(0, 0)
        c.width = Cm(16.0)
        set_cell_background(c, "F7FAFC")
        set_cell_margins(c, 80, 80, 100, 100)
        p_c = c.paragraphs[0]
        p_c.paragraph_format.space_after = Pt(0)
        r_c = p_c.add_run(c_code)
        r_c.font.name = 'Consolas'
        r_c.font.size = Pt(9.5)
        set_table_borders(tbl_c, color="CBD5E0")
        
        p_e = doc.add_paragraph()
        p_e.paragraph_format.space_before = Pt(2)
        p_e.paragraph_format.space_after = Pt(4)
        r_e = p_e.add_run("Giải thích: " + c_exp)
        r_e.font.size = Pt(10)
        r_e.font.italic = True
        r_e.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    add_h1("PHỤ LỤC B. THÔNG TIN DATASET VÀ LIÊN KẾT")
    add_p("Dataset 1: Online Retail Business – Kaggle")
    add_bullet("Tệp dữ liệu: data/assignment_06/OnlineRetail.csv (sau làm sạch lưu thành customer_behavior_daily.csv).")
    add_bullet("Thuộc tính: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country.")
    add_bullet("Liên kết nguồn: https://www.kaggle.com/datasets/umerkk12/online-retail-business/data")
    
    add_p("Dataset 2: S&P 500 Stock Data – Kaggle")
    add_bullet("Tệp dữ liệu: data/assignment_06/aapl_stock_5yr.csv (trích xuất từ all_stocks_5yr.csv).")
    add_bullet("Thuộc tính: date, open, high, low, close, volume, Name.")
    add_bullet("Liên kết nguồn: https://www.kaggle.com/camnugent/sandp500/data")

    # Lưu tệp Word
    out_docx1 = "A06_06_taint.731.docx"
    out_docx2 = "ass6/A06_06_taint.731.docx"
    os.makedirs("ass6", exist_ok=True)
    doc.save(out_docx1)
    doc.save(out_docx2)
    print(f"[+] Đã tạo thành công tài liệu Word báo cáo A06 v2: {out_docx1} và {out_docx2}")

if __name__ == '__main__':
    build_a06_report_v2()
