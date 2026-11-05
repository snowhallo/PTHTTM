"""
build_member3_report_docx.py
============================
Tạo tài liệu Word (.docx) chuyên sâu, toàn diện và chuẩn mực học thuật
cho toàn bộ nhiệm vụ của THÀNH VIÊN 3:
1. Nghiên cứu lý thuyết về bài toán dự đoán tiểu đường, đặc trưng y sinh và tiền xử lý dữ liệu.
2. Nghiên cứu cơ sở lý thuyết về chuyển đổi dữ liệu bảng sang đồ thị và phòng chống Data Leakage.
3. Đề xuất phương án xây dựng đồ thị và bàn giao nội dung cho thực nghiệm & báo cáo.

Tệp đầu ra: task_thanh_vien_3_du_doan_tieu_duong_gnn.docx
"""

import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

def sanitize_text(text):
    if not isinstance(text, str):
        return str(text)
    return ''.join(ch for ch in text if ch in '\n\r\t' or (32 <= ord(ch) <= 0x10FFFF))

def create_member3_document():
    print("[*] Khởi tạo tài liệu nhiệm vụ THÀNH VIÊN 3...")
    doc = docx.Document()

    # 1. Cấu hình lề trang chuẩn học viện (A4)
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)

    # 2. Định dạng Typography cơ bản
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(4)

    # 3. XML Helper functions
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

    # 4. Heading helpers
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        return p

    def add_p(text, indent=True):
        p = doc.add_paragraph()
        if indent:
            p.paragraph_format.first_line_indent = Cm(0.8)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        run = p.add_run(sanitize_text(text))
        run.font.size = Pt(12)
        return p

    def add_bullet(text, prefix="•  "):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.2
        r_b = p.add_run(prefix)
        r_b.bold = True
        r_b.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        r_t = p.add_run(sanitize_text(text))
        r_t.font.size = Pt(11.5)
        return p

    def add_formula(eq_text, eq_num=""):
        tbl = doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, val="none")
        
        c0 = tbl.cell(0, 0)
        c1 = tbl.cell(0, 1)
        
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 70, 70, 120, 80)
        set_cell_margins(c1, 70, 70, 80, 120)
        
        c0.width = Inches(5.3)
        c1.width = Inches(1.0)
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        
        run0 = p0.add_run(sanitize_text(eq_text))
        run0.font.name = 'Cambria Math'
        run0.font.size = Pt(11.5)
        run0.font.italic = True
        run0.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        
        if eq_num:
            run1 = p1.add_run(sanitize_text(eq_num))
            run1.font.name = 'Times New Roman'
            run1.font.size = Pt(11)
            run1.bold = True
            run1.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
            
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(0)
        p_space.paragraph_format.space_after = Pt(2)
        return tbl

    def add_callout(title, text, bg_color="F0F4F8", border_color="003366"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, 120, 120, 180, 180)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(sanitize_text(title + "\n"))
        r_t.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        r_b = p.add_run(sanitize_text(text))
        r_b.font.size = Pt(10.5)
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(2)

    def format_table(headers, data, col_widths=None):
        tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl)
        # Header
        for j, h in enumerate(headers):
            cell = tbl.cell(0, j)
            set_cell_background(cell, "003366")
            set_cell_margins(cell, 120, 120, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(sanitize_text(h))
            r.bold = True
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        # Data
        for i, row in enumerate(data):
            bg = "FFFFFF" if i % 2 == 0 else "F7FAFC"
            for j, val in enumerate(row):
                cell = tbl.cell(i + 1, j)
                set_cell_background(cell, bg)
                set_cell_margins(cell, 80, 80, 100, 100)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                if j == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(sanitize_text(str(val)))
                r.font.size = Pt(9.5)
        if col_widths:
            for i, row in enumerate(tbl.rows):
                for j, w in enumerate(col_widths):
                    if isinstance(w, docx.shared.Length):
                        row.cells[j].width = w
                    else:
                        row.cells[j].width = Inches(float(w))
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(4)
        return tbl

    def add_code_block(code_text, caption=""):
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.paragraph_format.space_before = Pt(4)
            p_cap.paragraph_format.space_after = Pt(2)
            r_c = p_cap.add_run(sanitize_text(caption))
            r_c.bold = True
            r_c.font.size = Pt(10)
            r_c.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
            
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F8F9FA")
        set_cell_margins(cell, 100, 100, 140, 140)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
            f'<w:left w:val="single" w:sz="16" w:space="0" w:color="003366"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(sanitize_text(code_text))
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(2)

    # =========================================================================
    # TIÊU ĐỀ TÀI LIỆU & THÔNG TIN BÀN GIAO
    # =========================================================================
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_top = p_top.add_run("BÁO CÁO KỸ THUẬT & TÀI LIỆU NGHIÊN CỨU LÝ THUYẾT\n")
    r_top.bold = True
    r_top.font.size = Pt(15)
    r_top.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    r_top_sub = p_top.add_run("PHÂN HỆ NHIỆM VỤ THÀNH VIÊN 3:\nBÀI TOÁN DỰ ĐOÁN TIỂU ĐƯỜNG, ĐẶC TRƯNG Y SINH, TIỀN XỬ LÝ VÀ CHUYỂN ĐỔI DỮ LIỆU BẢNG SANG ĐỒ THỊ (GNN)")
    r_top_sub.bold = True
    r_top_sub.font.size = Pt(13)
    r_top_sub.font.color.rgb = RGBColor(0x99, 0x00, 0x00)

    # Info box
    info_headers = ["Thông tin phân công", "Chi tiết nội dung nhiệm vụ"]
    info_data = [
        ["Thành viên thực hiện:", "Thành viên 3 (Phụ trách Lý thuyết Dữ liệu, Y sinh & Phương án Tạo Đồ thị)"],
        ["Đơn vị bàn giao:", "Bàn giao cho Thành viên 1 (Triển khai Thực nghiệm Giai đoạn 3 & Ghép Báo cáo tổng hợp)"],
        ["Phạm vi nhiệm vụ 1:", "Nghiên cứu lý thuyết về bài toán dự đoán tiểu đường, đặc trưng y sinh và tiền xử lý dữ liệu."],
        ["Phạm vi nhiệm vụ 2:", "Nghiên cứu cơ sở lý thuyết về chuyển đổi dữ liệu bảng sang đồ thị và phòng chống Data Leakage."],
        ["Phạm vi nhiệm vụ 3:", "Đề xuất ít nhất 02 phương án xây dựng đồ thị kèm bộ tiêu chí đánh giá và tài liệu bàn giao."]
    ]
    format_table(info_headers, info_data, [1.8, 4.5])

    # =========================================================================
    # PHẦN 1: NGHIÊN CỨU LÝ THUYẾT BÀI TOÁN & TIỀN XỬ LÝ DỮ LIỆU
    # =========================================================================
    add_h1("PHẦN 1: NGHIÊN CỨU LÝ THUYẾT BÀI TOÁN DỰ ĐOÁN TIỂU ĐƯỜNG, ĐẶC TRƯNG Y SINH VÀ QUY TRÌNH TIỀN XỬ LÝ DỮ LIỆU")

    add_h2("1.1. Phát biểu bài toán dưới góc độ Học máy và Quy tắc xác định biến mục tiêu")
    add_p("Dưới lăng kính của Học máy (Machine Learning), bài toán dự đoán bệnh đái tháo đường (Diabetes Prediction) được định nghĩa là một bài toán Phân loại nhị phân (Binary Classification) có giám sát (Supervised Learning). Giả sử ta có tập dữ liệu gồm N bệnh nhân, mỗi bệnh nhân thứ i được biểu diễn bởi một véc-tơ đặc trưng đầu vào xᵢ ∈ ℝᵈ (với d là số chiều thuộc tính nhân khẩu học, bệnh nền và lâm sàng) và một biến mục tiêu nhị phân yᵢ ∈ {0, 1}:")
    add_formula("D = { (xᵢ, yᵢ) }  với  i = 1, 2, ..., N ;   xᵢ ∈ ℝᵈ,   yᵢ ∈ {0, 1}", "(1.1)")
    add_p("Trong đó, biến mục tiêu yᵢ được quy ước:")
    add_bullet("yᵢ = 0: Bệnh nhân âm tính (Không mắc bệnh đái tháo đường - Non-diabetic).")
    add_bullet("yᵢ = 1: Bệnh nhân dương tính (Mắc bệnh đái tháo đường - Diabetic).")
    add_p("Mục tiêu của mô hình học máy là tìm kiếm một hàm ánh xạ f_θ: ℝᵈ → [0, 1] sao cho ŷᵢ = f_θ(xᵢ) ước lượng chuẩn xác xác suất tiên nghiệm mắc bệnh P(yᵢ = 1 | xᵢ), từ đó đưa ra quyết định chẩn đoán thông qua ngưỡng phân loại τ ∈ (0, 1):")
    add_formula("ŷᵢ = P(y = 1 | xᵢ) = f_θ(xᵢ) ;    ŷ_label = 1  khi  ŷᵢ ≥ τ,   ngược lại  ŷ_label = 0", "(1.2)")

    add_callout("Quy chuẩn Y khoa Quốc tế Xác định Biến Mục tiêu Diabetes:",
"""Theo Hiệp hội Đái tháo đường Hoa Kỳ (ADA - American Diabetes Association) và Tổ chức Y tế Thế giới (WHO), biến mục tiêu 'diabetes = 1' được xác lập khi bệnh nhân thỏa mãn ít nhất một trong các tiêu chuẩn vàng lâm sàng sau:
1. HbA1c (Glycated Hemoglobin) ≥ 6.5% (tương đương 48 mmol/mol) được đo bằng phương pháp chuẩn hóa NGSP.
2. Đường huyết lúc đói (Fasting Plasma Glucose - FPG) ≥ 126 mg/dL (7.0 mmol/L) sau ít nhất 8 giờ nhịn ăn.
3. Nghiệm pháp dung nạp glucose đường uống 2 giờ (2-hour 75g OGTT) ≥ 200 mg/dL (11.1 mmol/L).
4. Đường huyết ngẫu nhiên (Random Plasma Glucose) ≥ 200 mg/dL (11.1 mmol/L) đi kèm các triệu chứng kinh điển (tam chứng: đa niệu, đa ẩm, sụt cân không rõ nguyên nhân).""")

    add_h2("1.2. Phân tích Ý nghĩa Y khoa và Vai trò Dự báo của các Nhóm Đặc trưng")
    add_p("Tập dữ liệu chuẩn mực Diabetes Prediction Dataset (từ nguồn Kaggle) bao gồm 9 trường thông tin cốt lõi, được phân chia thành 3 nhóm đặc trưng sinh học mang tính tương hỗ cao:")

    feat_headers = ["Tên đặc trưng", "Nhóm đặc trưng", "Kiểu dữ liệu", "Khoảng giá trị", "Ý nghĩa y sinh và Vai trò dự báo lâm sàng"]
    feat_data = [
        ["age (Tuổi)", "Nhân khẩu học", "Số liên tục", "0.08 - 80.0", "Tuổi tác là yếu tố nguy cơ độc lập hàng đầu. Quá trình lão hóa làm suy thoái chức năng tế bào beta đảo tụy và gia tăng kháng insulin ngoại vi."],
        ["gender (Giới tính)", "Nhân khẩu học", "Phân loại", "Female / Male / Other", "Phản ánh sự khác biệt về hormone sinh dục (Estrogen vs Testosterone) và kiểu tích tụ mỡ (mỡ nội tạng ở nam, mỡ dưới da ở nữ)."],
        ["hypertension", "Bệnh nền", "Nhị phân (0/1)", "0: Không, 1: Có", "Tăng huyết áp là thành tố cốt lõi của Hội chứng chuyển hóa (Metabolic Syndrome), kích hoạt stress oxy hóa và làm tổn thương vi mạch."],
        ["heart_disease", "Bệnh nền", "Nhị phân (0/1)", "0: Không, 1: Có", "Bệnh tim mạch là biến chứng mạch máu lớn (macrovascular) nguy hiểm nhất của đái tháo đường do rối loạn chuyển hóa lipid và xơ vữa."],
        ["smoking_history", "Hành vi - Lối sống", "Phân loại (6 nhóm)", "never, current, former, ever, not current, No Info", "Nicotine kích thích hệ giao cảm, tăng cortisol và đối kháng thụ thể insulin, làm giảm khả năng hấp thu glucose của cơ vân."],
        ["bmi (Chỉ số khối)", "Lâm sàng", "Số liên tục", "10.0 - 95.7 kg/m²", "Chỉ số béo phì. Mô mỡ phì đại giải phóng ồ ạt acid béo tự do (FFA) và các cytokine tiền viêm (TNF-α, IL-6), trực tiếp gây đề kháng insulin."],
        ["HbA1c_level", "Xét nghiệm vàng", "Số liên tục", "3.5 - 9.0 %", "Tiêu chuẩn vàng đo lường mức đường huyết trung bình trong 2-3 tháng. Giá trị ≥ 6.5% là ngưỡng khẳng định đái tháo đường."],
        ["blood_glucose_level", "Xét nghiệm tức thời", "Số nguyên", "80 - 300 mg/dL", "Nồng độ glucose tự do trong máu tại thời điểm kiểm tra. Thể hiện trạng thái đường huyết cấp tính và khả năng điều hòa tức thời của gan."]
    ]
    format_table(feat_headers, feat_data, [1.1, 1.0, 1.0, 1.1, 2.1])

    add_h2("1.3. Cơ sở Lý thuyết cho Quy trình Tiền xử lý Dữ liệu Toàn diện")
    add_p("Để đảm bảo dữ liệu đạt độ tin cậy tối đa trước khi đưa vào mô hình học máy và cấu trúc đồ thị, quy trình tiền xử lý được thiết lập trên 5 trụ cột kỹ thuật:")

    add_p("1. Khám phá Phân phối Dữ liệu (Exploratory Data Analysis - EDA):", indent=True)
    add_bullet("Phân tích đơn biến (Univariate Analysis): Đo lường độ lệch (skewness) và độ nhọn (kurtosis) của các biến liên tục (BMI, Glucose, HbA1c). Nhận diện các phân phối lệch phải (right-skewed).")
    add_bullet("Phân tích hai biến (Bivariate Analysis): Sử dụng hệ số tương quan Pearson cho cặp biến số liên tục, hệ số tương quan Spearman cho dữ liệu phi tuyến, và kiểm định Chi-bình phương (Chi-Square Test) để đánh giá mối liên hệ giữa các biến phân loại (`gender`, `smoking_history`) với nhãn mục tiêu `diabetes`.")

    add_p("2. Phương pháp Xử lý Mất cân bằng Nhãn (Class Imbalance Mitigation):", indent=True)
    add_p("Trong tập dữ liệu thực tế Kaggle (100.000 dòng), số lượng mẫu nhãn 0 chiếm khoảng 91.500 (91.5%) và nhãn 1 chỉ chiếm khoảng 8.500 (8.5%), tạo ra tỷ lệ mất cân bằng nghiêm trọng (~10.8 : 1). Nếu áp dụng hàm mất mát thông thường, mô hình sẽ có xu hướng dự đoán toàn bộ nhãn 0 để đạt Accuracy 91.5% ảo nhưng hoàn toàn thất bại trong việc phát hiện người bệnh.")
    add_bullet("Cấp độ dữ liệu: Áp dụng kỹ thuật sinh mẫu thiểu số tổng hợp SMOTE (Synthetic Minority Over-sampling Technique) hoặc Borderline-SMOTE trên tập Train. Thuật toán tạo ra các mẫu nhân tạo nội suy dọc theo đoạn thẳng nối giữa một điểm thiểu số xᵢ và láng giềng x_zi:")
    add_formula("x_new = xᵢ + λ · (x_zi - xᵢ)  với  λ ~ Uniform(0, 1)", "(1.3)")
    add_bullet("Cấp độ hàm mất mát: Sử dụng Balanced Cross-Entropy hoặc Focal Loss (Lin et al., 2017) với hệ số điều chỉnh trọng số nhãn w₁ = N₀ / N₁:")
    add_formula("L_Focal = - αₜ (1 - pₜ)^γ · log(pₜ)", "(1.4)")
    add_bullet("Quy chuẩn đánh giá: Loại bỏ hoàn toàn Accuracy; bắt buộc sử dụng PR-AUC (Precision-Recall Area Under Curve), F1-Score (Minority class), ROC-AUC và Balanced Accuracy.")

    add_p("3. Kỹ thuật Xử lý Giá trị Thiếu (Missing Value Imputation):", indent=True)
    add_p("Trường `smoking_history` có khoảng 35.8% mẫu mang giá trị `'No Info'`. Trong y tế, việc 'không có thông tin' bản thân nó mang ý nghĩa thông tin (Missing Not At Random - MNAR). Ta thiết lập 2 chiến lược:")
    add_bullet("Chiến lược 1 (Category Preservation): Giữ nguyên `'No Info'` như một phân lớp độc lập khi One-Hot Encoding để mô hình tự học tín hiệu thiếu thông tin của nhóm bệnh nhân này.")
    add_bullet("Chiến lược 2 (Imputation): Sử dụng mô hình KNN Imputer hoặc Iterative Imputer (MICE) dựa trên tương quan của `age`, `bmi` và `heart_disease` để gán nhãn khả dĩ nhất cho thực nghiệm so sánh.")

    add_p("4. Phát hiện và Xử lý Ngoại lệ Lâm sàng (Clinical Outlier Handling):", indent=True)
    add_p("Khác với dữ liệu công nghiệp, ngoại lệ trong y tế đòi hỏi sự cẩn trọng đặc biệt giữa hai khái niệm:")
    add_bullet("Ngoại lệ nhiễu do lỗi nhập liệu (Data Entry Artifacts): Ví dụ BMI = 0, Glucose = 0 (sinh học không thể tồn tại). Các trường hợp này bắt buộc phải loại bỏ hoặc coi là missing value.")
    add_bullet("Ngoại lệ sinh học thực tế (True Biological Extremes): Ví dụ bệnh nhân có BMI = 60 kg/m² (béo phì độ III) hoặc Blood Glucose = 300 mg/dL (hôn mê tăng áp lực thẩm thấu). Đây là các ca bệnh nguy kịch có nguy cơ tiểu đường cao nhất, TUYỆT ĐỐI KHÔNG ĐƯỢC XÓA BỎ vì sẽ làm mất đi tín hiệu của nhóm nguy cơ cao.")

    add_p("5. Kỹ thuật Chuẩn hóa và Mã hóa Đặc trưng (Normalization & Encoding):", indent=True)
    add_bullet("Biến phân loại: Sử dụng One-Hot Encoding cho `gender` (Male, Female, Other) và `smoking_history` (never, current, former, ever, not current, No Info).")
    add_bullet("Biến số liên tục: Sử dụng RobustScaler thay vì StandardScaler. RobustScaler sử dụng trung vị (Median) và khoảng tứ phân vị (IQR = Q₃ - Q₁) nên không bị bóp méo bởi các giá trị ngoại lệ lâm sàng cực trị:")
    add_formula("x_scaled = (x - Median(x)) / (Q₃(x) - Q₁(x))", "(1.5)")

    add_h2("1.4. Phân tích Giới hạn Dữ liệu Tổng hợp từ Nguồn Kaggle và Tính Đại diện Thực tế")
    add_p("Một báo cáo khoa học xuất sắc đòi hỏi phải nhận diện trung thực các hạn chế cố hữu của nguồn dữ liệu:")
    add_bullet("Bản chất Dữ liệu Bán tổng hợp (Semi-Synthetic Nature): Tập dữ liệu Kaggle được xây dựng dựa trên hồ sơ y tế điện tử kết hợp thuật toán tạo mẫu tổng hợp để bảo vệ quyền riêng tư bệnh nhân (HIPAA compliance). Do đó, một số phân phối đặc trưng (như đường huyết) có tính làm tròn cơ học, làm giảm bớt độ nhiễu tự nhiên của môi trường bệnh viện thực tế.")
    add_bullet("Thiếu hụt Chiều thời gian (Absence of Longitudinal Temporal Dynamics): Dữ liệu là dạng cắt ngang (cross-sectional snapshot) tại một lần khám. Mô hình không nắm bắt được tốc độ tăng cân, xu hướng biến thiên HbA1c qua các năm và tiền sử dùng thuốc điều trị (Metformin, Statin).")
    add_bullet("Thiếu biến Chủng tộc và Di truyền (Missing Race & Genetics): Dữ liệu không ghi nhận biến chủng tộc (Ethnicity). Theo nghiên cứu y học, người gốc Á (Asian) có nguy cơ mắc tiểu đường type 2 ở ngưỡng BMI thấp hơn đáng kể so với người da trắng (ngưỡng thừa cân của người châu Á theo WHO là BMI ≥ 23 kg/m² thay vì ≥ 25 kg/m²).")

    # =========================================================================
    # PHẦN 2: CHUYỂN ĐỔI DỮ LIỆU BẢNG SANG ĐỒ THỊ & PHÒNG CHỐNG DATA LEAKAGE
    # =========================================================================
    add_h1("PHẦN 2: NGHIÊN CỨU CƠ SỞ LÝ THUYẾT VỀ CHUYỂN ĐỔI DỮ LIỆU BẢNG SANG ĐỒ THỊ VÀ PHÒNG CHỐNG DATA LEAKAGE")

    add_h2("2.1. Cơ sở Khoa học: Tại sao cần và có thể chuyển đổi Dữ liệu Bảng sang Đồ thị (GNN)?")
    add_p("1. Điểm nghẽn cố hữu của các mô hình học máy truyền thống trên dữ liệu bảng (Tabular ML):", indent=True)
    add_p("Các mô hình truyền thống (Multi-Layer Perceptron - MLP, Random Forest, XGBoost, LightGBM) đều hoạt động dựa trên giả định nền tảng: các hàng dữ liệu (bệnh nhân) là các quan sát độc lập và có cùng phân phối (i.i.d - Independent and Identically Distributed):")
    add_formula("P(D) = ∏ᵢ₌₁ᴺ P(xᵢ, yᵢ)", "(2.1)")
    add_p("Giả định này hoàn toàn bỏ qua tương quan liên bệnh nhân (inter-patient correlation). Trong thực tế y khoa, không một bệnh nhân nào tồn tại độc lập. Một bệnh nhân có triệu chứng không rõ ràng (biên giới - borderline case) có thể được chẩn đoán chính xác hơn rất nhiều nếu bác sĩ liên hệ hồ sơ của họ với một nhóm bệnh nhân có cùng kiểu hình lâm sàng (clinical phenotypes).")

    add_p("2. Cơ sở lý thuyết của cấu trúc Đồ thị Bệnh nhân (Patient Similarity Graph):", indent=True)
    add_p("Ta có thể mô hình hóa toàn bộ quần thể bệnh nhân dưới dạng một đồ thị G = (V, E, X):")
    add_bullet("Tập đỉnh V = {v₁, v₂, ..., v_N}: Mỗi đỉnh vᵢ đại diện cho một bệnh nhân duy nhất.")
    add_bullet("Ma trận đặc trưng đỉnh X ∈ ℝ^{N × d}: Mỗi hàng xᵢ là véc-tơ thuộc tính y sinh của bệnh nhân vᵢ sau tiền xử lý.")
    add_bullet("Tập cạnh E ⊆ V × V và Ma trận kề A ∈ ℝ^{N × N}: Cạnh eᵢⱼ = (vᵢ, vⱼ) thể hiện mối quan hệ tương đồng lâm sàng giữa bệnh nhân vᵢ và vⱼ. Trọng số cạnh Aᵢⱼ đo lường mức độ tương đồng giữa hai hồ sơ bệnh án.")

    add_p("3. Cơ chế Truyền tin (Message Passing) của Graph Neural Networks (GNN):", indent=True)
    add_p("Khi dữ liệu bảng được cấu trúc hóa thành đồ thị, mạng nơ-ron đồ thị (GNN) sử dụng cơ chế truyền tin lặp qua các tầng l = 0, 1, ..., L-1:")
    add_formula("m_v⁽ˡ⁺¹⁾ = AGGREGATE⁽ˡ⁾( { MSG⁽ˡ⁾(h_u⁽ˡ⁾, h_v⁽ˡ⁾, A_uv) : u ∈ 𝒩(v) } )", "(2.2)")
    add_formula("h_v⁽ˡ⁺¹⁾ = UPDATE⁽ˡ⁾( h_v⁽ˡ⁾, m_v⁽ˡ⁺¹⁾ )", "(2.3)")
    add_p("Thông qua cơ chế này, biểu diễn ẩn h_v của mỗi bệnh nhân không chỉ chứa thông tin cá nhân của họ mà còn được làm giàu bởi cấu trúc láng giềng xung quanh. Điều này giúp làm mịn nhiễu (noise smoothing) và tăng độ bền vững phân loại vượt trội so với việc phân tích đơn lẻ từng dòng bảng.")

    add_h2("2.2. Các Phương pháp Khởi tạo Đồ thị từ Dữ liệu Bảng")
    add_p("Do dữ liệu bệnh nhân dạng bảng không có sẵn cấu trúc liên kết topo tự nhiên (như mạng xã hội hay liên kết phân tử), ta phải áp dụng các thuật toán kiến tạo đồ thị (Graph Construction Algorithms):")

    add_p("1. Thuật toán K-Láng giềng gần nhất (K-Nearest Neighbors - KNN Graph):", indent=True)
    add_p("Phương pháp phổ biến nhất là nối mỗi bệnh nhân vᵢ với k bệnh nhân có khoảng cách ngắn nhất trong không gian đặc trưng:")
    add_formula("𝒩_k(i) = top-k_{j ≠ i}( - dist(xᵢ, xⱼ) )", "(2.4)")
    add_bullet("Đồ thị KNN có hướng (Directed KNN): Cạnh (i, j) tồn tại nếu j ∈ 𝒩_k(i). Ma trận kề có thể bất đối xứng.")
    add_bullet("Đồ thị KNN đối xứng (Mutual / Symmetric KNN): Cạnh tồn tại khi cả hai là láng giềng của nhau, hoặc đối xứng hóa A_sym = max(A, Aᵀ). Đảm bảo tính liên thông và phù hợp với GCN chuẩn.")

    add_p("2. Đồ thị Ngưỡng Bán kính (ε-Radius / Threshold Graph):", indent=True)
    add_p("Nối cạnh giữa hai bệnh nhân nếu độ tương đồng vượt qua một ngưỡng cố định θ:")
    add_formula("Aᵢⱼ = 1  khi  Similarity(xᵢ, xⱼ) ≥ θ ;    ngược lại  Aᵢⱼ = 0", "(2.5)")
    add_bullet("Nhận xét: Phương pháp này nhạy cảm cao với mật độ dữ liệu. Vùng dữ liệu thưa thớt dễ tạo ra các đỉnh cô lập (degree = 0), trong khi vùng dữ liệu đậm đặc dễ tạo ra các đỉnh hub siêu kết nối, làm quá tải tính toán.")

    add_p("3. Đồ thị Lưỡng phân Bệnh nhân - Thực thể Y tế (Bipartite Patient-Entity Graph):", indent=True)
    add_p("Tạo đồ thị gồm 2 tập đỉnh khác loại: Tập đỉnh Bệnh nhân V_P và Tập đỉnh Thuộc tính Y tế V_E (ví dụ: nhóm BMI, nhóm Glucose, trạng thái hút thuốc). Cạnh chỉ tồn tại giữa bệnh nhân và thuộc tính họ mang. Mô hình này triệt tiêu chi phí tính khoảng cách cặp O(N²) nhưng đòi hỏi kiến trúc GNN dị thể phức tạp (Heterogeneous GNN như HAN, RGCN).")

    add_h2("2.3. Tiêu chí Lý thuyết Lựa chọn Tham số k, Thước đo Khoảng cách và Trọng số Cạnh")
    add_p("Hiệu năng của GNN phụ thuộc sống còn vào chất lượng đồ thị được khởi tạo. Các tiêu chí toán học và thực nghiệm được xác lập như sau:")

    add_p("1. Tiêu chí lựa chọn số láng giềng k:", indent=True)
    add_bullet("Nếu k quá nhỏ (k = 1, 2, 3): Đồ thị bị rời rạc, tạo ra nhiều thành phần liên thông riêng lẻ. Cơ chế truyền tin bị nghẽn mạch, mô hình nhạy cảm cao với nhiễu ngoại lệ.")
    add_bullet("Nếu k quá lớn (k ≥ 30): Xuất hiện hiện tượng Làm mịn quá mức (Over-smoothing Problem). Khi số tầng GNN tăng, biểu diễn ẩn của tất cả các đỉnh đều hội tụ về một véc-tơ trung bình chung, làm mất hoàn toàn khả năng phân biệt giữa bệnh nhân tiểu đường và người khỏe mạnh.")
    add_bullet("Khuyến nghị lý thuyết: Chọn k trong khoảng [5, 15] (tối ưu thường là k = 8 hoặc k = 10) để cân bằng giữa độ kết nối thông tin và tính phân tách nhãn.")

    add_p("2. Tiêu chí lựa chọn Thước đo Khoảng cách (Distance Metrics):", indent=True)
    add_bullet("Khoảng cách Euclidean (L2): Thích hợp nhất khi tất cả các đặc trưng đã được chuẩn hóa đồng nhất bằng RobustScaler:")
    add_formula("d_Euc(xᵢ, xⱼ) = √[ ∑ₘ₌₁ᵈ (x_im - x_jm)² ]", "(2.6)")
    add_bullet("Khoảng cách Cosine: Đo góc giữa hai véc-tơ, không phụ thuộc vào độ lớn tuyệt đối. Thích hợp cho dữ liệu thưa (sparse) hoặc sau khi mã hóa One-Hot:")
    add_formula("Sim_Cos(xᵢ, xⱼ) = (xᵢ · xⱼ) / ( ||xᵢ|| · ||xⱼ|| )", "(2.7)")
    add_bullet("Khoảng cách Mahalanobis: Tính đến ma trận hiệp phương sai Σ của dữ liệu, loại bỏ tương quan giữa các biến y khoa (ví dụ tương quan giữa BMI và Glucose):")
    add_formula("d_Mah(xᵢ, xⱼ) = √[ (xᵢ - xⱼ)ᵀ · Σ⁻¹ · (xᵢ - xⱼ) ]", "(2.8)")

    add_p("3. Cách thức Gán Trọng số Cạnh (Edge Weighting):", indent=True)
    add_p("Thay vì dùng ma trận nhị phân {0, 1}, áp dụng hàm nhân Gaussian RBF (Radial Basis Function Kernel) để gán trọng số suy giảm trơn theo khoảng cách:")
    add_formula("Wᵢⱼ = exp( - d(xᵢ, xⱼ)² / (2σ²) )    với  j ∈ 𝒩_k(i)", "(2.9)")
    add_p("Tham số σ đóng vai trò kiểm soát độ rộng của vùng láng giềng, thường được gán bằng trung vị khoảng cách của tập train.")

    add_h2("2.4. Phân tích Các Kịch bản Gây Rò rỉ Dữ liệu (Data Leakage) và Quy tắc Phòng ngừa Nghiêm ngặt")
    add_p("Rò rỉ dữ liệu (Data Leakage) là rủi ro nguy hiểm nhất khi áp dụng GNN trên dữ liệu bảng, có thể dẫn đến kết quả đánh giá giả tạo (overoptimistic results) nhưng hoàn toàn thất bại khi triển khai thực tế. Thành viên 3 xác lập 2 kịch bản rò rỉ cốt tử:")

    add_callout("CẢNH BÁO KỸ THUẬT: HAI KỊCH BẢN RÒ RỈ DỮ LIỆU CỐT TỬ KHI TẠO ĐỒ THỊ",
"""1. KỊCH BẢN 1: RÒ RỈ NHÃN MỤC TIÊU (LABEL LEAKAGE)
• Lỗi vi phạm: Sử dụng toàn bộ bảng dữ liệu (bao gồm cả cột nhãn mục tiêu 'diabetes') để tính toán ma trận khoảng cách KNN hoặc gán trọng số cạnh!
• Hậu quả: Đồ thị sẽ vô tình tạo ra các cạnh dày đặc giữa các bệnh nhân có cùng nhãn bệnh. Mô hình GNN chỉ cần học việc 'đếm nhãn láng giềng' là đạt kết quả 99.9% giả tạo.
• QUY TẮC NGĂN CHẶN 1: TUYỆT ĐỐI loại bỏ biến mục tiêu 'diabetes' ra khỏi không gian đặc trưng trước khi thực thi bất kỳ thuật toán tính khoảng cách hoặc tạo đồ thị nào.

2. KỊCH BẢN 2: RÒ RỈ TẬP KIỂM THỬ SANG TẬP HUẤN LUYỆN (TEST-TO-TRAIN TRANSDUCTIVE LEAKAGE)
• Lỗi vi phạm: Dựng một đồ thị chung cho toàn bộ tập dữ liệu (cả Train và Test) trước khi chia tách dữ liệu!
• Hậu quả: Cấu trúc liên kết của tập Test đã thâm nhập vào quá trình huấn luyện của tập Train. Khi GNN truyền tin, thông tin thuộc tính của các bệnh nhân trong tập Test đã được tổng hợp ngược về các đỉnh tập Train.
• QUY TẮC NGĂN CHẶN 2: BẮT BUỘC áp dụng cơ chế Đồ thị Quy nạp (Inductive Graph Setting):
   - Bước 1: Chia tách tập dữ liệu thành Train / Validation / Test trước tiên.
   - Bước 2: Chỉ sử dụng các đỉnh thuộc tập Train để dựng Đồ thị Huấn luyện G_train = (V_train, E_train).
   - Bước 3: Mọi tham số tiền xử lý (Median, IQR, Mean, Std) chỉ được tính toán trên tập Train và fit sang Validation/Test.
   - Bước 4: Khi kiểm thử một bệnh nhân mới trong tập Test, đỉnh Test chỉ được phép kết nối một chiều đến k láng giềng gần nhất trong tập Train, tuyệt đối không được tạo cạnh giữa các đỉnh Test với nhau.""")

    # =========================================================================
    # PHẦN 3: ĐỀ XUẤT PHƯƠNG ÁN XÂY DỰNG ĐỒ THỊ & BÀN GIAO THỰC NGHIỆM
    # =========================================================================
    add_h1("PHẦN 3: ĐỀ XUẤT PHƯƠNG ÁN XÂY DỰNG ĐỒ THỊ VÀ TÀI LIỆU BÀN GIAO CHO THỰC NGHIỆM & BÁO CÁO")

    add_h2("3.1. Đề xuất Chi tiết Hai Phương án Thiết kế Đồ thị Khả thi")
    add_p("Nhằm cung cấp cơ sở vững chắc cho Thành viên 1 triển khai thực nghiệm mô hình ở Giai đoạn 3, Thành viên 3 đề xuất 02 phương án kiến trúc đồ thị đối chứng:")

    add_p("PHƯƠNG ÁN 1: ĐỒ THỊ ĐỒNG THỂ KNN CHUẨN (BASELINE HOMOGENEOUS KNN GRAPH)", indent=False)
    add_bullet("Cấu trúc topo: Đồ thị đồng thể (Homogeneous Graph) bệnh nhân - bệnh nhân.")
    add_bullet("Không gian thuộc tính đỉnh: Véc-tơ đặc trưng 8 chiều sau khi mã hóa One-Hot và chuẩn hóa RobustScaler.")
    add_bullet("Thuật toán sinh cạnh: K-Nearest Neighbors vô hướng đối xứng với k = 10.")
    add_bullet("Thước đo khoảng cách: Khoảng cách Euclidean tiêu chuẩn trên không gian đã chuẩn hóa.")
    add_bullet("Trọng số cạnh: Ma trận nhị phân Aᵢⱼ ∈ {0, 1} có thêm khuyên tự nối (Self-loops Aᵢᵢ = 1) phục vụ chuẩn hóa GCN: Ã = A + I_N.")
    add_bullet("Ưu điểm nổi bật: Cấu trúc toán học tinh gọn, tốc độ khởi tạo nhanh, dễ dàng tương thích với hầu hết các thư viện GNN tiêu chuẩn (PyTorch Geometric, DGL) và các kiến trúc mạng kinh điển (GCN, GraphSAGE).")
    add_bullet("Nhược điểm: Xem xét trọng số của tất cả các đặc trưng như nhau, chưa phản ánh được ưu tiên lâm sàng của các chỉ số sinh hóa chuyên biệt.")

    add_p("PHƯƠNG ÁN 2: ĐỒ THỊ KHOẢNG CÁCH Y SINH CÓ TRỌNG SỐ LÂM SÀNG (CLINICALLY-WEIGHTED FEATURE GRAPH)", indent=False)
    add_p("Trong chẩn đoán đái tháo đường, chỉ số HbA1c và Blood Glucose mang giá trị quyết định cao hơn nhiều so với biến nhân khẩu học. Do đó, Phương án 2 áp dụng khoảng cách Euclidean có trọng số chuyên gia y sinh (Clinically-Weighted Metric):")
    add_formula("d_W(xᵢ, xⱼ) = \\sqrt{\\sum_{m=1}^d w_m · (x_{im} - x_{jm})^2}", "(3.1)")
    add_bullet("Bộ trọng số lâm sàng w_m được xác lập: w_{HbA1c} = 3.0, w_{Glucose} = 3.0, w_{BMI} = 2.0, w_{Hypertension} = 1.5, w_{HeartDisease} = 1.5, w_{Age} = 1.2, w_{Smoking} = 1.0, w_{Gender} = 1.0.")
    add_bullet("Thuật toán sinh cạnh: KNN với k = 8 kết hợp cơ chế lọc cạnh bằng ngưỡng tương đồng tối thiểu θ = 0.40 để ngăn chặn kết nối giữa các ca bệnh quá dị biệt.")
    add_bullet("Trọng số cạnh: Sử dụng Gaussian RBF Kernel Wᵢⱼ = exp(- d_W(xᵢ, xⱼ)² / (2σ²)) để biểu diễn độ tin cậy liên kết liên bệnh nhân.")
    add_bullet("Ưu điểm nổi bật: Phản ánh trung thực bản chất y học, tạo ra các cụm bệnh nhân có độ tương đồng kiểu hình bệnh lý rất cao, hỗ trợ đắc lực cho các kiến trúc Attention như GAT (Graph Attention Networks).")
    add_bullet("Nhược điểm: Tốn thêm chi phí tính toán nhân trọng số và cần tinh chỉnh siêu tham số σ.")

    add_h2("3.2. Bảng Tiêu chí Đánh giá và So sánh Lựa chọn Phương án Đồ thị")
    add_p("Bảng tiêu chí định lượng và định tính bàn giao cho Thành viên 1 để nghiệm thu và lựa chọn phương án tối ưu trong quá trình huấn luyện mô hình:")

    crit_headers = ["Tiêu chí đánh giá", "Phương án 1 (Baseline KNN Graph)", "Phương án 2 (Clinically-Weighted Graph)", "Ý nghĩa kỹ thuật & Khuyến nghị"]
    crit_data = [
        ["Tỷ lệ Đồng thể Nhãn (Homophily Ratio h)", "Dự kiến: 0.72 - 0.78", "Dự kiến: 0.82 - 0.89 (Cao hơn)", "Tỷ lệ h = |(u,v) ∈ E: y_u = y_v| / |E|. h càng cao thì GNN càng phân loại chính xác, tránh nhiễu nhãn."],
        ["Độ cô lập đỉnh (Isolated Node Ratio)", "Rất thấp (< 0.5% số đỉnh)", "Trung bình (~1.5% do có lọc ngưỡng θ)", "Đảm bảo đồ thị có độ phủ kết nối tốt, không bỏ sót bệnh nhân."],
        ["Độ phức tạp tính toán (Computational Cost)", "Thấp O(N · log N) với BallTree/KDTree", "Trung bình O(N · d · log N)", "Phương án 1 phù hợp cho tập dữ liệu lớn; Phương án 2 tối ưu cho bài toán cần độ chính xác cao."],
        ["Khả năng tích hợp kiến trúc GNN", "Tối ưu cho GCN, GraphSAGE", "Tối ưu cho GAT (Graph Attention), Weighted GCN", "Thành viên 1 nên thử nghiệm Phương án 1 làm Baseline và Phương án 2 làm giải pháp cải tiến."],
        ["Khả năng phòng chống Over-smoothing", "Tốt với k = 10", "Rất tốt với k = 8 và lọc ngưỡng θ", "Giúp mô hình có thể xếp chồng 2-3 tầng GNN mà không bị suy thoái biểu diễn."]
    ]
    format_table(crit_headers, crit_data, [1.5, 1.4, 1.6, 1.8])

    add_h2("3.3. Mã nguồn Mẫu Tham khảo Khởi tạo Đồ thị Chuẩn Bàn giao cho Thành viên 1")
    add_p("Đoạn mã nguồn Python chuẩn mực dưới đây được Thành viên 3 đóng gói để bàn giao trực tiếp cho Thành viên 1 sử dụng trong pipeline thực nghiệm Giai đoạn 3:")

    code_pipeline = """# =========================================================================
# PIPELINE KHỞI TẠO ĐỒ THỊ BỆNH NHÂN (PHÒNG CHỐNG DATA LEAKAGE 100%)
# Người phụ trách: Thành viên 3 | Bàn giao cho: Thành viên 1
# =========================================================================
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.neighbors import NearestNeighbors
import torch
from torch_geometric.data import Data

def build_inductive_patient_graph(df, k=10, test_size=0.2, random_state=42):
    # 1. BƯỚC 1: TÁCH BIỆT NHÃN MỤC TIÊU (NGĂN CHẶN LABEL LEAKAGE)
    feature_cols = [c for c in df.columns if c != 'diabetes']
    X = df[feature_cols].copy()
    y = df['diabetes'].values
    
    # 2. BƯỚC 2: PHÂN CHIA TRAIN/TEST TRƯỚC (NGĂN CHẶN TEST-TO-TRAIN LEAKAGE)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    
    # 3. TIỀN XỬ LÝ (FIT DUY NHẤT TRÊN TRAIN, TRANSFORM SANG TEST)
    cat_cols = ['gender', 'smoking_history']
    num_cols = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    
    scaler = RobustScaler()
    X_train_num = scaler.fit_transform(X_train[num_cols])
    X_test_num = scaler.transform(X_test[num_cols])
    
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_train_cat = encoder.fit_transform(X_train[cat_cols])
    X_test_cat = encoder.transform(X_test[cat_cols])
    
    # Ma trận đặc trưng cuối cùng
    X_train_final = np.hstack([X_train_num, X_train_cat])
    X_test_final = np.hstack([X_test_num, X_test_cat])
    
    # 4. XÂY DỰNG ĐỒ THỊ HUẤN LUYỆN (CHỈ DỰA TRÊN ĐỈNH TRAIN)
    nbrs = NearestNeighbors(n_neighbors=k+1, metric='euclidean', n_jobs=-1)
    nbrs.fit(X_train_final)
    distances, indices = nbrs.kneighbors(X_train_final)
    
    # Xây dựng danh sách cạnh (Edge Index) cho PyG
    source_nodes, target_nodes, edge_weights = [], [], []
    sigma = np.median(distances[:, 1:])  # Chuẩn hóa RBF kernel
    
    for i in range(len(X_train_final)):
        for j_idx in range(1, k+1):  # Bỏ qua chính nó ở vị trí 0
            neighbor = indices[i, j_idx]
            dist = distances[i, j_idx]
            weight = np.exp(- (dist ** 2) / (2 * (sigma ** 2)))
            
            source_nodes.append(i)
            target_nodes.append(neighbor)
            edge_weights.append(weight)
            
    edge_index_train = torch.tensor([source_nodes, target_nodes], dtype=torch.long)
    edge_weight_train = torch.tensor(edge_weights, dtype=torch.float)
    x_train_tensor = torch.tensor(X_train_final, dtype=torch.float)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    
    # Đóng gói đối tượng PyTorch Geometric Data
    train_graph_data = Data(
        x=x_train_tensor,
        edge_index=edge_index_train,
        edge_weight=edge_weight_train,
        y=y_train_tensor
    )
    
    print(f"[+] Khởi tạo Đồ thị Train thành công: {train_graph_data.num_nodes} đỉnh, {train_graph_data.num_edges} cạnh.")
    return train_graph_data, X_test_final, y_test, nbrs, sigma"""

    add_code_block(code_pipeline, "Mã nguồn Python: Pipeline Khởi tạo Đồ thị Bệnh nhân Chuẩn PyTorch Geometric (Chống Leakage)")

    # =========================================================================
    # TÀI LIỆU THAM KHẢO
    # =========================================================================
    add_h1("TÀI LIỆU THAM KHẢO HỌC THUẬT (REFERENCES)")
    refs = [
        "[1] American Diabetes Association (ADA), 'Standards of Medical Care in Diabetes - 2024,' Diabetes Care, vol. 47, suppl. 1, pp. S1-S345, 2024.",
        "[2] T. N. Kipf and M. Welling, 'Semi-Supervised Classification with Graph Convolutional Networks,' in Proceedings of ICLR, 2017.",
        "[3] P. Veličković, G. Cucurull, A. Casanova, A. Romero, P. Liò, and Y. Bengio, 'Graph Attention Networks,' in Proceedings of ICLR, 2018.",
        "[4] W. L. Hamilton, R. Ying, and J. Leskovec, 'Inductive Representation Learning on Large Graphs (GraphSAGE),' in Advances in Neural Information Processing Systems (NeurIPS), 2017.",
        "[5] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, 'SMOTE: Synthetic Minority Over-sampling Technique,' Journal of Artificial Intelligence Research, vol. 16, pp. 321-357, 2002.",
        "[6] T. Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollár, 'Focal Loss for Dense Object Detection,' in Proceedings of IEEE ICCV, 2017, pp. 2980-2988.",
        "[7] Kaggle Dataset: Diabetes Clinical Dataset (100k rows) by ziya07, URL: https://www.kaggle.com/datasets/ziya07/diabetes-clinical-dataset100k-rows, 2023."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Cm(0.8)
        p_ref.paragraph_format.first_line_indent = Cm(-0.8)
        p_ref.paragraph_format.space_after = Pt(3)
        run_r = p_ref.add_run(r)
        run_r.font.size = Pt(10)

    # Lưu tệp Word
    output_filename = "task_thanh_vien_3_du_doan_tieu_duong_gnn.docx"
    doc.save(output_filename)
    print(f"[+] Đã tạo thành công tài liệu bàn giao tại: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_member3_document()
