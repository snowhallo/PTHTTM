"""
agent02_experiments/build_agent02_docx.py
=========================================
Generates the comprehensive, rigorous, and exhaustive academic report:
`agent02_06_15_taint.docx` (and copies to root directory).

Author: Nguyễn Tuấn Tài (MSSV: B23DCCN731)
Course: Phát triển Hệ thống Thông minh - GVHD: PGS. TS. Trần Đình Quế
Class: 06 (D23CNPM01) - Group: 15
"""

import os
import sys
import shutil
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

def create_report():
    print("[*] Starting compilation of AGENT_02 Academic Report...")
    doc = docx.Document()

    # 1. Page Margins (PTIT Academic Standard)
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)

    # Base typography
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(4)

    # XML Helper functions
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

    # Heading helpers
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

    def add_image_figure(img_path, fig_title, comment=None, width_inch=5.8):
        if not os.path.exists(img_path):
            print(f"[!] Warning: Image not found at {img_path}")
            return
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inch))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(3)
        run_cap = p_cap.add_run(sanitize_text(fig_title))
        run_cap.bold = True
        run_cap.font.size = Pt(10.5)
        run_cap.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

        if comment:
            p_cm = doc.add_paragraph()
            p_cm.paragraph_format.left_indent = Cm(0.8)
            p_cm.paragraph_format.right_indent = Cm(0.8)
            p_cm.paragraph_format.space_after = Pt(4)
            p_cm.paragraph_format.line_spacing = 1.15
            run_cm_t = p_cm.add_run("Nhận xét phân tích: ")
            run_cm_t.bold = True
            run_cm_t.font.size = Pt(10)
            run_cm_t.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
            run_cm_b = p_cm.add_run(sanitize_text(comment))
            run_cm_b.font.size = Pt(10)
            run_cm_b.font.italic = True
            run_cm_b.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

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

    # =========================================================================
    # TRANG BÌA (COVER PAGE)
    # =========================================================================
    p_b1 = doc.add_paragraph()
    p_b1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_b1 = p_b1.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN 1\n***")
    r_b1.bold = True
    r_b1.font.size = Pt(13)
    r_b1.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    for _ in range(2):
        doc.add_paragraph()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("BÁO CÁO THỰC HÀNH PHÒNG THÍ NGHIỆM\n")
    r_t1.bold = True
    r_t1.font.size = Pt(15)
    r_t1.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    r_t2 = p_title.add_run("LABORATORY EXPERIMENT 02:\nREINFORCEMENT-LEARNING-BASED AGENT\nVS RULE-BASED AGENT\n")
    r_t2.bold = True
    r_t2.font.size = Pt(18)
    r_t2.font.color.rgb = RGBColor(0x99, 0x00, 0x00)

    r_t3 = p_title.add_run("Nghiên cứu Định lượng và So sánh Đối chứng giữa Tác tử Học tăng cường Q-Learning và Tác tử Dựa trên luật trong Thị trường Thương mại Điện tử Cạnh tranh")
    r_t3.font.italic = True
    r_t3.font.size = Pt(12)
    r_t3.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    for _ in range(3):
        doc.add_paragraph()

    # Student metadata table
    tbl_info = doc.add_table(rows=6, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_info, color="CBD5E0", sz="4", val="single")
    info_data = [
        ("Học phần:", "Phát triển Hệ thống Thông minh (Intelligent System Development)"),
        ("Giảng viên hướng dẫn:", "PGS. TS. Trần Đình Quế"),
        ("Sinh viên thực hiện:", "Nguyễn Tuấn Tài"),
        ("Mã số sinh viên (MSSV):", "B23DCCN731"),
        ("Lớp học phần & Nhóm:", "Lớp 06 (D23CNPM01) — Nhóm bài tập 15"),
        ("Thời hạn nộp (Deadline):", "23:30 Ngày 29 Tháng 10 Năm 2026")
    ]
    for idx, (label, val) in enumerate(info_data):
        c0 = tbl_info.cell(idx, 0)
        c1 = tbl_info.cell(idx, 1)
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 80, 80, 120, 120)
        set_cell_margins(c1, 80, 80, 120, 120)
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.size = Pt(11)
        r0.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.size = Pt(11)

    for _ in range(4):
        doc.add_paragraph()

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_loc = p_loc.add_run("HÀ NỘI — 10/2026")
    r_loc.bold = True
    r_loc.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # SECTION 1: INTRODUCTION AND OBJECTIVES
    # =========================================================================
    add_h1("1. INTRODUCTION AND OBJECTIVES (GIỚI THIỆU & MỤC TIÊU NGHIÊN CỨU)")
    
    add_h2("1.1. Bối cảnh nghiên cứu và Đặt vấn đề")
    add_p("Trong kỷ nguyên kinh tế số và bùng nổ của các nền tảng thương mại điện tử (E-Commerce Marketplaces như Amazon, Shopee, Alibaba), bài toán định giá sản phẩm động (Dynamic Pricing) và ra quyết định bán hàng tự chủ đã trở thành yếu tố sống còn quyết định năng lực cạnh tranh và tối đa hóa lợi nhuận của doanh nghiệp. Ở phương thức truyền thống, các quyết định định giá chủ yếu dựa vào hệ thống dựa trên luật (Rule-Based Systems), nơi các chuyên gia phân tích kinh doanh thiết lập sẵn các kịch bản IF/THEN cố định (ví dụ: 'nếu đối thủ giảm giá và thị trường vào mùa cao điểm thì giảm giá theo'). Mặc dù các hệ thống luật mang lại tính minh bạch tuyệt đối, dễ kiểm soát và không đòi hỏi chi phí tính toán huấn luyện, chúng bộc lộ điểm yếu chết người là tính cứng nhắc, không có khả năng tự tích lũy kinh nghiệm và hoàn toàn thất bại khi thị trường xuất hiện những biến động phi tuyến tính chưa từng được lập trình trước.")
    add_p("Ngược lại, sự trỗi dậy của Trí tuệ Nhân tạo hiện đại với phân nhánh Học tăng cường (Reinforcement Learning - RL) đã mở ra một hướng tiếp cận đột phá: tác tử thông minh tự chủ học hỏi thông qua quá trình tương tác thử-sai (trial-and-error) liên tục với môi trường và đối thủ. Tác tử không cần được bảo ban phải làm gì ở từng tình huống cụ thể, mà tự tìm cách tối ưu hóa hàm giá trị kỳ vọng tích lũy thông qua các tín hiệu phản hồi phần thưởng (reward signals). Tuy nhiên, học tăng cường trong môi trường cạnh tranh đối kháng cũng phải đối mặt với những thách thức nghiêm trọng như hiện tượng phi dừng (non-stationarity), bài toán đánh đổi giữa khám phá và khai thác (exploration vs. exploitation), và sự đánh đổi kinh tế phức tạp giữa việc tăng doanh số bán (volume) và sự sụt giảm biên lợi nhuận trên mỗi đơn hàng (margin).")

    add_h2("1.2. Bảy Mục tiêu Cốt lõi của Bài tập Phòng thí nghiệm")
    add_p("Theo đặc tả chuẩn tại Section 2 của tài liệu hướng dẫn thí nghiệm, báo cáo này hướng tới việc hoàn thành toàn diện 7 mục tiêu học tập và nghiên cứu định lượng sau:")
    add_bullet("Mục tiêu 1: Mô hình hóa Hệ thống Đa tác tử (Multi-Agent System - MAS) và Quy trình Quyết định Markov (MDP) trong bài toán định giá cạnh tranh trên sàn thương mại điện tử.")
    add_bullet("Mục tiêu 2: Cài đặt và thực thi chính xác thuật toán Tabular Q-Learning với chiến lược khám phá phân rã ε-greedy theo đúng các công thức toán học Bellman.")
    add_bullet("Mục tiêu 3: Thiết lập tác tử đối chứng dựa trên luật chuyên gia (Rule-Based Agent) với các điều kiện IF/THEN xác định để so sánh định lượng.")
    add_bullet("Mục tiêu 4: Đo lường và phân tích sự suy giảm biên lợi nhuận kinh tế (Margin vs. Volume Trade-off) khi đưa ra quyết định chiết khấu sản phẩm.")
    add_bullet("Mục tiêu 5: Khảo sát độ nhạy tham số (Sensitivity Analysis) đối với Tốc độ học (Learning Rate α) và Lịch trình khám phá (Exploration Schedule ε).")
    add_bullet("Mục tiêu 6: Đánh giá độ tin cậy và phân tán thống kê thông qua giao thức đa hạt giống ngẫu nhiên (Multi-Seed Statistical Robustness).")
    add_bullet("Mục tiêu 7: Nhận diện hiện tượng phi dừng (Non-stationarity) khi hai tác tử cùng học đồng thời và thực hiện mở rộng mã nguồn mô phỏng kiểm chứng các kịch bản đối thủ thích nghi và ràng buộc chi phí lưu kho tồn kho.")

    # =========================================================================
    # SECTION 2: ENVIRONMENT AND AGENTS DESCRIPTION
    # =========================================================================
    add_h1("2. DESCRIPTION OF THE ENVIRONMENT AND BOTH AGENTS (MÔ TẢ MÔI TRƯỜNG & HAI TÁC TỬ)")
    
    add_h2("2.1. Mô hình Toán học Môi trường Thương mại Điện tử (E-Commerce Environment)")
    add_p("Môi trường mô phỏng thị trường bán lẻ trực tuyến cạnh tranh giữa hai tác tử (Agent 1 và Agent 2). Tại mỗi bước thời gian t trong một episode gồm T = 20 bước, hệ thống được xác định bởi các thành phần toán học chặt chẽ:")
    
    add_p("1. Không gian trạng thái (State Space S):", indent=True)
    add_p("Mỗi tác tử i quan sát trạng thái cục bộ s_i(t) tại đầu bước t, được định nghĩa bởi một bộ đôi rời rạc:")
    add_formula("sᵢ(t) = (dₜ, cᵢ(t)) ∈ {0, 1} × {0, 1}", "(2.1)")
    add_bullet("dₜ ∈ {0, 1}: Trạng thái nhu cầu thị trường tổng thể (0: Nhu cầu thấp, 1: Nhu cầu cao). Nhu cầu tiến hóa độc lập theo phân phối đều ngẫu nhiên: P(dₜ = 0) = P(dₜ = 1) = 0.5 tại mỗi bước.")
    add_bullet("cᵢ(t) ∈ {0, 1}: Hành động giảm giá của đối thủ cạnh tranh ở bước thời gian trước đó t-1 (0: Không giảm giá, 1: Có giảm giá 20%). Tại bước khởi đầu t=0, cᵢ(0) = 0.")
    add_p("Do đó, không gian trạng thái của mỗi tác tử có đúng |S| = 2 × 2 = 4 trạng thái rời rạc:")
    add_bullet("Trạng thái (0, 0): Thị trường nhu cầu thấp, đối thủ trước đó không giảm giá.")
    add_bullet("Trạng thái (0, 1): Thị trường nhu cầu thấp, đối thủ trước đó có giảm giá.")
    add_bullet("Trạng thái (1, 0): Thị trường nhu cầu cao, đối thủ trước đó không giảm giá.")
    add_bullet("Trạng thái (1, 1): Thị trường nhu cầu cao, đối thủ trước đó có giảm giá.")

    add_p("2. Không gian hành động (Action Space A):", indent=True)
    add_p("Tại mỗi bước t, cả hai tác tử đưa ra quyết định định giá đồng thời và độc lập (simultaneous decision-making):")
    add_formula("aᵢ(t) ∈ {0, 1}", "(2.2)")
    add_bullet("aᵢ(t) = 0: Giữ nguyên mức giá niêm yết cơ sở P = $10.0 (Không chiết khấu).")
    add_bullet("aᵢ(t) = 1: Áp dụng chương trình chiết khấu giảm giá 20% (δ = 0.20), giá bán thực tế là P(1 - δ) = $8.0.")

    add_p("3. Lượng khách tiềm năng và Xác suất chuyển đổi (Customer Conversion Model):", indent=True)
    add_p("Lượng khách hàng ghé thăm gian hàng Nₜ phụ thuộc vào trạng thái nhu cầu dₜ:")
    add_formula("Nₜ = 10 (khi dₜ = 0: Nhu cầu thấp)    hoặc    Nₜ = 20 (khi dₜ = 1: Nhu cầu cao)", "(2.3)")
    add_p("Xác suất một khách hàng quyết định mua sản phẩm của tác tử i được mô hình hóa theo hàm tương tác cạnh tranh tuyến tính:")
    add_formula("pᵢ(t) = clip( 0.30 + 0.25·dₜ + 0.15·aᵢ(t) - 0.10·a₋ᵢ(t),   0.05,   0.95 )", "(2.4)")
    add_p("Trong đó, a₋ᵢ(t) là hành động của đối thủ tại bước hiện tại t. Hàm clip bảo đảm xác suất nằm trong khoảng hợp lệ [0.05, 0.95]. Số lượng đơn hàng bán được thực tế Sᵢ(t) là một biến ngẫu nhiên tuân theo phân phối nhị thức:")
    add_formula("Sᵢ(t) ~ Binomial(Nₜ,  pᵢ(t))", "(2.5)")

    add_p("4. Hàm phần thưởng kinh tế (Profit Reward Function):", indent=True)
    add_p("Mục tiêu của tác tử là tối đa hóa lợi nhuận ròng tích lũy. Giá bán đơn vị cơ sở là P = $10.0, chi phí sản xuất mỗi đơn vị sản phẩm là chi phí bất biến C = $5.0. Lợi nhuận trên mỗi đơn hàng bán được là:")
    add_formula("Marginᵢ(t) = P·(1 - δ·aᵢ(t)) - C = { 10.0 - 5.0 = $5.0 (khi aᵢ=0) ;   8.0 - 5.0 = $3.0 (khi aᵢ=1) }", "(2.6)")
    add_p("Phần thưởng tại bước t là tổng lợi nhuận thu được từ toàn bộ đơn hàng bán được:")
    add_formula("rᵢ(t) = Sᵢ(t) × Marginᵢ(t)", "(2.7)")

    add_h2("2.2. Kiến trúc Tác tử Học tăng cường (Tabular Q-Learning Agent)")
    add_p("Tác tử Agent 1 sử dụng thuật toán Tabular Q-Learning kinh điển (Watkins & Dayan, 1992). Bảng tra cứu Q-table có kích thước 2 × 2 × 2 = 8 ô nhớ, biểu diễn giá trị kỳ vọng Q(s, a) = Q(demand, competitor_action, own_action).")
    add_p("1. Chiến lược lựa chọn hành động ε-greedy phân rã (Decaying ε-greedy):", indent=True)
    add_p("Tại mỗi bước, tác tử cân bằng giữa Khám phá và Khai thác:")
    add_formula("a₁(t) = { Random(0, 1)  với xác suất εₖ ;    arg maxₐ Q(s₁(t), a)  với xác suất 1 - εₖ }", "(2.8)")
    add_p("Tại cuối mỗi episode k, tham số khám phá được phân rã nhân:")
    add_formula("εₖ₊₁ = max(ε_min,   εₖ × ε_decay)", "(2.9)")
    add_p("2. Quy tắc cập nhật giá trị Q theo phương trình sai phân thời gian (Bellman Equation):", indent=True)
    add_formula("Q(sₜ, aₜ) ← Q(sₜ, aₜ) + α · [ rₜ + γ · maxₐ· Q(sₜ₊₁, a') - Q(sₜ, aₜ) ]", "(2.10)")
    add_p("Trong đó, α là tốc độ học (learning rate), γ là hệ số chiết khấu tương lai (discount factor), và đại lượng trong dấu ngoặc vuông chính là Sai số Sai phân Thời gian (Temporal Difference Error - δ_TD).")

    add_h2("2.3. Kiến trúc Tác tử Dựa trên luật Chuyên gia (Rule-Based Agent)")
    add_p("Tác tử Agent 2 đại diện cho trường phái chuyên gia kinh tế truyền thống, hành động theo một tập 3 luật IF/THEN xác định, cố định và hoàn toàn không học hỏi từ phần thưởng:")
    add_bullet("Luật 1 (Rule 1): Nếu nhu cầu thị trường thấp (d = 0) -> Không giảm giá (a_2 = 0). Lý do: Quy mô thị trường nhỏ (N=10), giảm giá sẽ làm hao hụt lợi nhuận trầm trọng.")
    add_bullet("Luật 2 (Rule 2): Nếu nhu cầu thị trường cao (d = 1) VÀ đối thủ ở bước trước có giảm giá (c = 1) -> Giảm giá (a_2 = 1) để trả đũa và bảo vệ thị phần.")
    add_bullet("Luật 3 (Rule 3): Nếu nhu cầu thị trường cao (d = 1) VÀ đối thủ ở bước trước không giảm giá (c = 0) -> Không giảm giá (a_2 = 0) để duy trì mặt bằng giá cao.")

    # Image 1: System Architecture
    add_image_figure(
        "agent02_experiments/report_figures/fig_1_system_architecture.png",
        "Hình 1: Sơ đồ Kiến trúc Tổng thể Hệ thống Đa tác tử và Luồng Tương tác trong Môi trường Thương mại Điện tử",
        "Mô hình minh họa chu trình tương tác hai chiều: Tác tử RL (Q-learning) và Tác tử Rule-based cùng quan sát trạng thái cục bộ s_i(t) = (d_t, c_i(t)), chọn hành động đồng thời a_i(t), môi trường tính toán tỷ lệ chuyển đổi cạnh tranh p_i, sinh doanh số nhị thức S_i và phản hồi phần thưởng lợi nhuận r_i."
    )

    # =========================================================================
    # SECTION 3: EXPERIMENTAL SETUP AND PARAMETER CONFIGURATIONS
    # =========================================================================
    add_h1("3. EXPERIMENTAL SETUP AND PARAMETER CONFIGURATIONS (THIẾT LẬP THỰC NGHIỆM)")
    
    add_h2("3.1. Cấu hình Tham số Chuẩn (Baseline Setup)")
    add_p("Các thực nghiệm được thực hiện trên môi trường Python 3.13 với hạt giống ngẫu nhiên cơ sở seed = 42. Cấu hình tham số được chuẩn hóa theo đúng tài liệu đặc tả của môn học:")

    setup_table_headers = ["Tham số (Parameter)", "Ký hiệu", "Giá trị Chuẩn", "Ý nghĩa và Vai trò Kỹ thuật"]
    setup_table_data = [
        ["Số episode huấn luyện", "Episodes", "5.000", "Thời gian huấn luyện đủ dài để bảng Q hội tụ."],
        ["Số bước mỗi episode", "T (Steps)", "20", "Độ dài chuỗi tương tác trong một phiên kinh doanh."],
        ["Tốc độ học Q-learning", "α (Alpha)", "0.10", "Tỷ lệ trọng số cập nhật thông tin mới vào Q-table."],
        ["Hệ số chiết khấu tương lai", "γ (Gamma)", "0.90", "Độ quan trọng của phần thưởng kỳ vọng dài hạn."],
        ["Tỷ lệ khám phá khởi đầu", "ε_start", "0.20", "Xác suất hành động ngẫu nhiên ở đầu huấn luyện."],
        ["Tỷ lệ khám phá tối thiểu", "ε_min", "0.02", "Mức khám phá tối thiểu duy trì sự dẻo dai."],
        ["Tỷ lệ phân rã khám phá", "ε_decay", "0.995", "Tốc độ giảm dần khám phá sau mỗi episode."],
        ["Giá niêm yết cơ sở", "P", "$10.0", "Giá bán tiêu chuẩn khi không áp dụng chiết khấu."],
        ["Chi phí sản xuất đơn vị", "C", "$5.0", "Chi phí biên bất biến trên mỗi đơn vị hàng hóa."],
        ["Mức chiết khấu giảm giá", "δ", "0.20 (20%)", "Tỷ lệ giảm giá khi hành động a=1 (Giá bán $8.0)."],
        ["Khách hàng khi cầu thấp", "N_low", "10", "Lượng khách tiềm năng khi d=0."],
        ["Khách hàng khi cầu cao", "N_high", "20", "Lượng khách tiềm năng khi d=1."],
        ["Số episode đánh giá độc lập", "Eval Episodes", "500", "Số episode chạy đánh giá khi đóng băng Q-table."]
    ]
    format_table(setup_table_headers, setup_table_data, [Inches(1.8), Inches(0.8), Inches(1.0), Inches(2.7)])

    add_h2("3.2. Giao thức Đánh giá Độc lập (Evaluation Protocol)")
    add_p("Để đánh giá chính xác năng lực thực sự của chính sách đã học mà không bị làm nhiễu bởi các hành động ngẫu nhiên trong quá trình học:")
    add_bullet("Đóng băng bảng Q-table: Vô hiệu hóa hàm cập nhật learn() (α = 0).")
    add_bullet("Vô hiệu hóa khám phá: Thiết lập ε = 0.0 tuyệt đối. Tác tử RL hoàn toàn hành động theo chiến lược tham lam (Greedy Policy): a_1(t) = argmax_a Q(s, a).")
    add_bullet("Chạy đánh giá trên 500 episodes độc lập (10.000 bước tương tác) để loại bỏ các sai số mẫu ngắn hạn.")

    add_h2("3.3. Các Kịch bản Thực nghiệm Đối sánh (Experimental Scenarios)")
    add_p("Nghiên cứu triển khai 5 kịch bản thực nghiệm quy chuẩn:")
    add_bullet("Thực nghiệm A (Baseline): RL Agent huấn luyện đối đầu với Fixed Rule-Based Opponent qua 5.000 episodes.")
    add_bullet("Thực nghiệm B (Learning Rate Sensitivity): Khảo sát 3 mức α ∈ {0.01, 0.10, 0.50} để kiểm chứng tốc độ hội tụ và độ ổn định dao động.")
    add_bullet("Thực nghiệm C (Exploration Schedules): Khảo sát 3 lịch trình: Low (ε: 0.05 -> 0.01), Baseline (ε: 0.20 -> 0.02), High (ε: 0.50 -> 0.05).")
    add_bullet("Thực nghiệm D (Multi-Seed Statistical Robustness): Thực thi lặp lại trên 5 hạt giống ngẫu nhiên độc lập (Seeds: 11, 22, 33, 44, 55).")
    add_bullet("Thực nghiệm E (Extended Environments - Phục vụ Q8, Q9, Q10): Triển khai thêm 3 môi trường mở rộng: (1) Hai tác tử RL học đồng thời (Simultaneous RL); (2) Đối thủ hung hăng liên tục giảm giá (Aggressive Opponent p=0.8); (3) Môi trường có chi phí lưu kho và phạt thiếu hàng tồn kho (Inventory Constraints).")

    # =========================================================================
    # SECTION 4: EXPERIMENTAL RESULTS, TABLES, AND FIGURES
    # =========================================================================
    add_h1("4. RESULTS, TABLES, AND FIGURES (KẾT QUẢ THỰC NGHIỆM, BẢNG BIỂU & ĐỒ THỊ)")
    
    add_h2("4.1. Bảng Tổng hợp Kết quả Đánh giá Chuẩn (Suggested Results Table)")
    add_p("Dưới đây là bảng tổng hợp số liệu đo lường định lượng thu được từ các thực nghiệm độc lập theo đúng định dạng mẫu yêu cầu tại Section 7 của đề bài:")

    res_headers = ["Kịch bản Thực nghiệm (Experiment)", "Tác tử (Agent)", "Phần thưởng TB/Bước ($)", "Độ lệch chuẩn (Std)", "Tỷ lệ Giảm giá (%)", "Hành vi Chính sách"]
    res_data = [
        ["Baseline (Eval 500 ep)", "RL Agent (Q-Learning)", "35.1275", "10.421", "0.00%", "Tham lam tối ưu: Không giảm giá"],
        ["Baseline (Eval 500 ep)", "Rule-Based Agent", "34.9685", "10.408", "0.00%", "Cố định: Không giảm giá"],
        ["Learning Rate α = 0.01", "RL Agent", "35.2475", "10.450", "0.00%", "Hội tụ chậm, chính sách ổn định"],
        ["Learning Rate α = 0.10", "RL Agent", "35.2475", "10.450", "0.00%", "Cân bằng tối ưu, hiệu năng cao"],
        ["Learning Rate α = 0.50", "RL Agent", "28.5085", "11.832", "40.52%", "Mất ổn định, giảm giá sai lầm"],
        ["Exploration Low (0.05->0.01)", "RL Agent", "35.1090", "10.415", "0.00%", "Thiếu khám phá nhưng vẫn đạt tối ưu"],
        ["Exploration Baseline (0.2->0.02)", "RL Agent", "35.1275", "10.421", "0.00%", "Lịch trình chuẩn tối ưu"],
        ["Exploration High (0.5->0.05)", "RL Agent", "35.1090", "10.415", "0.00%", "Khám phá dư thừa, hội tụ về tối ưu"],
        ["Ext A: Simultaneous RL", "RL Agent 1", "34.9055", "10.380", "0.00%", "Đồng hội tụ không giảm giá"],
        ["Ext A: Simultaneous RL", "RL Agent 2", "34.9865", "10.395", "0.00%", "Đồng hội tụ không giảm giá"],
        ["Ext B: Aggressive Opp (p=0.8)", "RL Agent", "28.7990", "9.620", "0.00%", "Phòng thủ biên lãi, không giảm giá"],
        ["Ext B: Aggressive Opp (p=0.8)", "Aggressive Opponent", "29.1739", "9.850", "80.18%", "Giảm giá liên tục, phá giá"],
        ["Ext C: Inventory Holding Cost", "RL Agent", "25.7797", "8.950", "0.00%", "Chịu phạt lưu kho hàng tồn"],
        ["Ext C: Inventory Holding Cost", "Rule-Based Agent", "25.7828", "8.940", "0.00%", "Chịu phạt lưu kho hàng tồn"]
    ]
    format_table(res_headers, res_data, [Inches(1.8), Inches(1.3), Inches(1.0), Inches(0.8), Inches(0.9), Inches(1.6)])

    add_h2("4.2. Phân tích Đồ thị Đường cong Học tập Baseline")
    add_image_figure(
        "agent02_experiments/report_figures/fig_2_baseline_training.png",
        "Hình 2: Đường cong Hội tụ Huấn luyện Tích lũy Baseline Q-Learning qua 5.000 Episodes",
        "Đồ thị biểu diễn phần thưởng thu được của RL Agent (đường xanh) và Rule-based Agent (đường đỏ nét đứt) cùng dải độ lệch chuẩn ±1σ. Đồ thị dưới biểu diễn đường cong phân rã lũy thừa của tham số khám phá ε từ 0.20 xuống 0.02. Cả hai tác tử cùng duy trì mức thưởng ổn định quanh 700$/episode (tương đương ~35$/bước)."
    )

    add_h2("4.3. Ma trận Q-Table và Chính sách Tối ưu Học được")
    add_p("Giá trị Q-table sau 5.000 episodes huấn luyện của tác tử RL được trích xuất như sau:")
    
    q_headers = ["Trạng thái (State)", "Mô tả Kinh tế", "Q(s, a=0: Không giảm giá)", "Q(s, a=1: Giảm giá 20%)", "Chính sách Tham lam π*(s)"]
    q_table_data = [
        ["(0, 0)", "Nhu cầu thấp (d=0), Đối thủ không giảm giá (c=0)", "228.30", "178.85", "a* = 0 (Không giảm giá) [Chênh lệch +49.45]"],
        ["(0, 1)", "Nhu cầu thấp (d=0), Đối thủ có giảm giá (c=1)", "177.99", "207.21", "a* = 1 (Giảm giá 20%) [Chênh lệch +29.22]"],
        ["(1, 0)", "Nhu cầu cao (d=1), Đối thủ không giảm giá (c=0)", "246.88", "235.23", "a* = 0 (Không giảm giá) [Chênh lệch +11.65]"],
        ["(1, 1)", "Nhu cầu cao (d=1), Đối thủ có giảm giá (c=1)", "211.42", "242.96", "a* = 1 (Giảm giá 20%) [Chênh lệch +31.54]"]
    ]
    format_table(q_headers, q_table_data, [Inches(0.9), Inches(2.2), Inches(1.2), Inches(1.2), Inches(1.9)])

    add_image_figure(
        "agent02_experiments/report_figures/fig_5_qtable_heatmap.png",
        "Hình 5: Heatmap Ma trận Giá trị Hành động Q(s, a) và Chính sách Tối ưu Tham lam",
        "Bản đồ nhiệt trực quan hóa 8 giá trị Q học được. Ở các trạng thái đối thủ không giảm giá (c=0), hành động tối ưu là Không giảm giá (a=0). Khi đối thủ giảm giá (c=1), hành động tối ưu chuyển sang Giảm giá (a=1) để kích cầu bù đắp lượng chuyển đổi bị mất."
    )

    add_h2("4.4. Phân tích Khảo sát Tham số Tốc độ học và Lịch trình Khám phá")
    add_image_figure(
        "agent02_experiments/report_figures/fig_3_learning_rate.png",
        "Hình 3: Phân tích Độ nhạy của Tốc độ học α ∈ {0.01, 0.10, 0.50} đến Phần thưởng và Tỷ lệ Giảm giá",
        "Với α = 0.01 và 0.10, thuật toán đạt hiệu năng xuất sắc ($35.25/bước, 0% giảm giá). Khi α tăng lên 0.50, sự dao động quá mức khiến tác tử giảm giá sai lầm tới 40.52% số bước, kéo phần thưởng tụt giảm nghiêm trọng xuống còn $28.51/bước."
    )

    add_image_figure(
        "agent02_experiments/report_figures/fig_4_exploration.png",
        "Hình 4: Tác động của Lịch trình Khám phá ε đến Hiệu năng Đánh giá Cuối kỳ",
        "Cả ba cấu hình Low, Baseline và High đều giúp tác tử hội tụ về mức thưởng tối ưu xấp xỉ $35.11 - $35.13/bước, khẳng định không gian trạng thái nhỏ (4 trạng thái) giúp Q-learning rất mạnh mẽ trước sự thay đổi của ε."
    )

    add_h2("4.5. Đánh giá Tính Ổn định Thống kê Đa Hạt giống và Thực nghiệm Mở rộng")
    add_image_figure(
        "agent02_experiments/report_figures/fig_6_multi_seed_boxplot.png",
        "Hình 6: Biểu đồ Hộp (Boxplot) Phân bố Phần thưởng Đánh giá qua 5 Hạt giống Ngẫu nhiên Độc lập",
        "Phần thưởng của RL Agent dao động trong khoảng [34.60, 35.33] với trung bình μ = 34.89$/bước, σ = 0.28$/bước, tương đương tuyệt đối với Rule-based Agent (μ = 34.93$/bước, σ = 0.22$/bước)."
    )

    add_image_figure(
        "agent02_experiments/report_figures/fig_7_extension_dynamic.png",
        "Hình 7: Kết quả Thực nghiệm Mở rộng: Multi-Agent Đồng thời, Đối thủ Hung hăng và Chi phí Tồn kho",
        "Minh chứng định lượng cho thấy: trong kịch bản đối thủ hung hăng xả giá 80% (Ext B), việc tác tử RL kiên định giữ nguyên giá gốc giúp bảo vệ biên lợi nhuận hiệu quả, không bị cuốn vào cuộc chiến giá cả tự sát."
    )

    # =========================================================================
    # SECTION 5: ANSWERS TO ALL TEN LABORATORY QUESTIONS
    # =========================================================================
    add_h1("5. ANSWERS TO ALL TEN LABORATORY QUESTIONS (TRẢ LỜI CHI TIẾT 10 CÂU HỎI PHÒNG THÍ NGHIỆM)")
    
    # -------------------------------------------------------------------------
    # QUESTION 1
    # -------------------------------------------------------------------------
    add_h2("Question 1. Agent and Environment Modeling (Mô hình hóa Tác tử và Môi trường)")
    add_callout("Nội dung Câu hỏi 1:", 
                "Identify the agents, environment, state space, action space, reward function, and state-transition process in the e-commerce simulation. Explain why this problem can be modeled as a multi-agent system rather than a single-agent system.")
    
    add_p("1. Nhận diện các thành phần của bài toán mô phỏng:", indent=True)
    add_bullet("Tác tử (Agents): Hệ thống gồm hai tác tử cạnh tranh: Agent 1 (Tác tử Học tăng cường Tabular Q-Learning) và Agent 2 (Tác tử Dựa trên luật chuyên gia cố định). Cả hai tác tử đóng vai trò là các nhà bán lẻ độc lập trên sàn thương mại điện tử.")
    add_bullet("Môi trường (Environment): Là sàn giao dịch thương mại điện tử mô phỏng, bao gồm khách hàng ghé thăm, động học nhu cầu thị trường ngẫu nhiên, cơ chế tính toán xác suất chuyển đổi khách hàng dựa trên tương quan giá, phân phối số lượng đơn hàng nhị thức và thanh toán doanh thu/lợi nhuận.")
    add_bullet("Không gian trạng thái (State Space S): Gồm 4 trạng thái rời rạc s_i(t) = (d_t, c_i(t)) ∈ {0, 1} × {0, 1}. Biến d_t biểu diễn nhu cầu khách hàng (0: thấp - 10 khách, 1: cao - 20 khách). Biến c_i(t) biểu diễn hành động giảm giá của đối thủ cạnh tranh ở bước liền trước (0: không giảm giá, 1: có giảm giá).")
    add_bullet("Không gian hành động (Action Space A): A = {0, 1}. Trong đó a = 0 là bán giá gốc P = $10.0 (không chiết khấu); a = 1 là giảm giá chiết khấu 20% (P_eff = $8.0).")
    add_bullet("Hàm phần thưởng (Reward Function r): Lợi nhuận ròng trên từng bước r_i(t) = S_i(t) × [P(1 - δ a_i(t)) - C], với C = $5.0 là chi phí sản xuất cố định trên mỗi đơn vị sản phẩm và S_i(t) là số đơn hàng bán được.")
    add_bullet("Quy trình chuyển trạng thái (State-Transition Process): Quá trình chuyển trạng thái s_t -> s_{t+1} là một quy trình ngẫu nhiên hỗn hợp: Thành phần nhu cầu d_{t+1} được sinh ngẫu nhiên độc lập theo phân phối đều P(d_{t+1}=0) = P(d_{t+1}=1) = 0.5. Thành phần c_i(t+1) nhận giá trị chính xác là hành động của đối thủ tại bước hiện tại: c_i(t+1) = a_{-i}(t). Do đó, hàm chuyển trạng thái tổng thể là P(s_{t+1} | s_t, a_1(t), a_2(t)) = 0.5.")

    add_p("2. Luận giải vì sao bài toán phải được mô hình hóa dưới dạng Hệ Đa Tác Tử (Multi-Agent System):", indent=True)
    add_p("Bài toán này KHÔNG THỂ mô hình hóa chính xác dưới dạng hệ đơn tác tử (Single-Agent MDP) vì những lý do bản chất sau:")
    add_bullet("Tính phụ thuộc chiến lược tương hỗ (Strategic Interdependence): Phần thưởng r_i(t) của tác tử i không chỉ phụ thuộc vào hành động của chính nó a_i(t), mà phụ thuộc trực tiếp vào hành động đồng thời a_{-i}(t) của tác tử đối thủ thông qua phương trình xác suất chuyển đổi p_i(t) = clip(0.30 + 0.25 d_t + 0.15 a_i(t) - 0.10 a_{-i}(t)). Hành động giảm giá của đối thủ làm suy giảm ngay lập tức 10% xác suất chuyển đổi của tác tử i.")
    add_bullet("Tính động lực của môi trường (Dynamic Non-Stationary Environment): Trong hệ đơn tác tử, môi trường được giả định là dừng (stationary) với hàm chuyển trạng thái P(s'|s, a) cố định. Trong bài toán này, trạng thái tương lai c_i(t+1) bị quyết định bởi hành động của đối thủ a_{-i}(t). Nếu đối thủ thay đổi hành vi hoặc cùng học tập, quy luật phản hồi của môi trường sẽ biến đổi theo thời gian, vi phạm tiên đề Markov của hệ đơn tác tử.")
    add_bullet("Bản chất lý thuyết trò chơi (Game-Theoretic Nature): Kết quả kinh doanh cuối cùng không phải là sự thích nghi thụ động với thiên nhiên mà là điểm cân bằng trò chơi (Nash Equilibrium) giữa các thực thể có mục tiêu cạnh tranh trực tiếp về thị phần và dòng tiền.")

    # -------------------------------------------------------------------------
    # QUESTION 2
    # -------------------------------------------------------------------------
    add_h2("Question 2. Learning-Based vs. Rule-Based Decisions (So sánh Tác tử Học tập và Tác tử Luật)")
    add_callout("Nội dung Câu hỏi 2:", 
                "Compare the RL-based agent and the rule-based agent in terms of decision-making, use of experience, adaptability, and computational requirements. Give one practical situation in which a rule-based agent could be preferable and another in which an RL-based agent could be preferable.")
    
    add_p("1. Bảng so sánh toàn diện giữa hai trường phái thiết kế tác tử:")
    comp_headers = ["Tiêu chí So sánh", "Tác tử Dựa trên luật (Rule-Based Agent)", "Tác tử Học tăng cường (RL-Based Agent)"]
    comp_data = [
        ["Cơ chế Ra quyết định (Decision-Making)", "Xác định (Deterministic), dựa vào cây quyết định IF/THEN lập trình sẵn bởi con người.", "Dựa trên tối ưu hóa hàm giá trị kỳ vọng Q(s, a), có thể kết hợp yếu tố ngẫu nhiên (ε-greedy, Softmax)."],
        ["Sử dụng Kinh nghiệm (Use of Experience)", "Hoàn toàn KHÔNG sử dụng. Quyết định tại bước t=1.000 giống hệt bước t=1, không có bộ nhớ lịch sử.", "Tích lũy kinh nghiệm liên tục thông qua sai số TD (Bellman updates), tinh chỉnh bảng Q sau mỗi bước tương tác."],
        ["Khả năng Thích ứng (Adaptability)", "Rất kém. Hoàn toàn tê liệt nếu môi trường thay đổi phân phối nhu cầu, giá vốn hoặc hành vi đối thủ mới.", "Rất cao. Có khả năng tự động khám phá chiến lược mới và thích ứng với môi trường động mà không cần can thiệp thủ công."],
        ["Tài nguyên Tính toán (Computational Cost)", "Cực kỳ thấp O(1). Chỉ tốn vài phép so sánh logic cơ bản, không cần bộ nhớ lưu trữ giá trị.", "Cao hơn. Cần bộ nhớ duy trì bảng Q (hoặc mạng nơ-ron sâu) và thời gian huấn luyện qua hàng ngàn episodes thử-sai."],
        ["Tính Minh bạch (Explainability)", "Tuyệt đối minh bạch (White-box). Mọi hành động đều giải thích được bằng quy tắc luật cụ thể.", "Độ minh bạch trung bình (Tabular Q-learning) đến rất thấp (Hộp đen trong Deep RL)."]
    ]
    format_table(comp_headers, comp_data, [Inches(1.8), Inches(2.3), Inches(2.5)])

    add_p("2. Hai tình huống thực tiễn điển hình ứng dụng từng loại tác tử:", indent=True)
    add_bullet("Tình huống ưu tiên Rule-Based Agent: Hệ thống xét duyệt tín dụng ngân hàng tự động hoặc hệ thống tuân thủ phòng chống rửa tiền (AML/KYC). Trong lĩnh vực tài chính - ngân hàng, các quy định pháp lý đòi hỏi tính giải trình 100% (Explainability) đối với lý do từ chối hoặc phê duyệt một khoản vay. Việc áp dụng tác tử học tăng cường thử-sai có thể dẫn tới các hành vi phân biệt đối xử bất hợp pháp hoặc đưa ra các quyết định ngẫu nhiên không thể giải trình trước cơ quan thanh tra tài chính.")
    add_bullet("Tình huống ưu tiên RL-Based Agent: Hệ thống đấu thầu quảng cáo tự động theo thời gian thực (Real-Time Bidding - RTB) trên Google Ads hoặc Meta Ads. Trong môi trường này, hàng triệu phiên đấu giá quảng cáo diễn ra mỗi giây với hàng ngàn đối thủ cạnh tranh có chiến lược biến đổi liên tục theo giờ trong ngày. Không một chuyên gia con người nào có thể bao quát và viết tay hàng triệu luật IF/THEN để tối ưu hóa giá thầu (Bid price). Tác tử RL với khả năng tự động học hỏi từ dữ liệu dòng chảy sẽ liên tục tinh chỉnh giá thầu để tối đa hóa tỷ lệ nhấp chuột (CTR) và tỷ suất hoàn vốn quảng cáo (ROAS).")

    # -------------------------------------------------------------------------
    # QUESTION 3
    # -------------------------------------------------------------------------
    add_h2("Question 3. Q-Learning Update Calculation (Tính toán Cập nhật Phương trình Q-Learning)")
    add_callout("Nội dung Câu hỏi 3:", 
                "Explain the mathematical meaning of the Q-learning update equation. Using a hypothetical example, calculate the updated Q-value when Q(s, a) = 4, α = 0.1, r = 6, γ = 0.9, and max_{a'} Q(s', a') = 5. Show each calculation step and interpret the result.")
    
    add_p("1. Ý nghĩa toán học của phương trình cập nhật Q-learning:", indent=True)
    add_p("Phương trình cập nhật cốt lõi của thuật toán Q-learning được viết dưới dạng sai phân thời gian (Temporal Difference):")
    add_formula("Q(s, a) ← Q(s, a) + α · [ r + γ · maxₐ· Q(s', a') - Q(s, a) ]", "(5.1)")
    add_bullet("Q(s, a): Ước lượng hiện tại về tổng phần thưởng chiết khấu tích lũy kỳ vọng khi thực hiện hành động a tại trạng thái s.")
    add_bullet("Mục tiêu TD (TD Target) = r + γ maxₐ· Q(s', a'): Biểu diễn ước lượng mới tốt hơn về giá trị thực sự, kết hợp giữa phần thưởng nhận được ngay lập tức r và giá trị chiết khấu tương lai tốt nhất tại trạng thái kế tiếp s'.")
    add_bullet("Sai số TD (TD Error) = δ_TD = [r + γ maxₐ· Q(s', a')] - Q(s, a): Đo lường sự bất ngờ hay độ lệch giữa ước lượng mới thực tế và ước lượng cũ kỳ vọng.")
    add_bullet("Tốc độ học α: Tỷ lệ điều chỉnh ước lượng cũ tiến gần hơn về phía mục tiêu TD. Phương trình có thể viết lại dưới dạng trung bình có trọng số: Q_new = (1 - α) Q_old + α (TD Target).")

    add_p("2. Tính toán giải tích từng bước cho ví dụ số học giả định:", indent=True)
    add_p("Cho các giá trị đầu vào: Q(s, a) = 4.0, α = 0.1, r = 6.0, γ = 0.9, và maxₐ· Q(s', a') = 5.0.")
    add_bullet("Bước 1: Tính toán Mục tiêu Sai phân Thời gian (TD Target):")
    add_formula("TD Target = r + γ · maxₐ· Q(s', a') = 6.0 + 0.9 × 5.0 = 6.0 + 4.5 = 10.5", "(5.2)")
    add_bullet("Bước 2: Tính toán Sai số Sai phân Thời gian (TD Error):")
    add_formula("δ_TD = TD Target - Q(s, a) = 10.5 - 4.0 = +6.5", "(5.3)")
    add_bullet("Bước 3: Tính toán Giá trị Q mới sau khi cập nhật (Q_new):")
    add_formula("Q_new(s, a) = Q(s, a) + α · δ_TD = 4.0 + 0.1 × 6.5 = 4.0 + 0.65 = 4.65", "(5.4)")

    add_p("3. Luận giải ý nghĩa kết quả tính toán:", indent=True)
    add_p("Giá trị sai số TD là một số dương lớn (δ_TD = +6.5), chỉ ra rằng trải nghiệm thực tế nhận được (phần thưởng tức thời r=6 kèm triển vọng tương lai 4.5, tổng cộng 10.5) vượt trội hơn rất nhiều so với kỳ vọng ban đầu của tác tử (chỉ là 4.0). Do đó, thuật toán đã thực hiện điều chỉnh tích cực: tăng giá trị của cặp (s, a) thêm 0.65 đơn vị (từ 4.00 lên 4.65). Trọng số α = 0.1 đóng vai trò như một bộ lọc thông thấp (low-pass filter), giúp tác tử hấp thụ thông tin mới từng bước một một cách êm thuận, tránh bị sốc giá trị khi gặp các phần thưởng đột biến ngẫu nhiên.")

    # -------------------------------------------------------------------------
    # QUESTION 4
    # -------------------------------------------------------------------------
    add_h2("Question 4. Exploration and Exploitation (Khám phá và Khai thác)")
    add_callout("Nội dung Câu hỏi 4:", 
                "Explain the role of ε-greedy action selection. Compare at least two exploration configurations using your experimental results. What may happen if the agent explores too much or stops exploring too early?")
    
    add_p("1. Vai trò của cơ chế lựa chọn hành động ε-greedy:", indent=True)
    add_p("Trong học tăng cường, tác tử luôn đối mặt với thế tiến thoái lưỡng nan kinh điển: Khám phá (Exploration - thử các hành động mới để tìm hiểu xem chúng có mang lại kết quả tốt hơn không) và Khai thác (Exploitation - tận dụng tri thức đã biết để chọn hành động có giá trị Q cao nhất hiện tại nhằm thu hoạch phần thưởng tối đa). Chiến lược ε-greedy giải quyết hài hòa bài toán này bằng cách dành xác suất (1 - ε) để khai thác và xác suất ε để hành động ngẫu nhiên. Bằng cách cho tham số ε phân rã giảm dần theo thời gian (từ 0.20 xuống 0.02), tác tử khám phá mạnh mẽ ở giai đoạn đầu và chuyển dịch dần sang khai thác sâu ở giai đoạn sau khi các giá trị Q đã tương đối chính xác.")

    add_p("2. Đối chiếu thực nghiệm định lượng giữa 3 cấu hình khám phá:", indent=True)
    add_bullet("Cấu hình Low Exploration (ε_start = 0.05, ε_min = 0.01): Tác tử chỉ dành 5% ban đầu để khám phá. Kết quả đánh giá: Phần thưởng TB = $35.1090/bước, Tỷ lệ giảm giá = 0.00%.")
    add_bullet("Cấu hình Baseline Exploration (ε_start = 0.20, ε_min = 0.02): Lịch trình chuẩn. Kết quả đánh giá: Phần thưởng TB = $35.1275/bước, Tỷ lệ giảm giá = 0.00%.")
    add_bullet("Cấu hình High Exploration (ε_start = 0.50, ε_min = 0.05): Tác tử dành tới 50% ban đầu để khám phá. Kết quả đánh giá: Phần thưởng TB = $35.1090/bước, Tỷ lệ giảm giá = 0.00%.")
    add_p("Nhận xét: Trong bài toán này, do không gian trạng thái rất nhỏ (|S| = 4, |A| = 2, tổng cộng 8 cặp giá trị Q), cả ba cấu hình khám phá đều cho phép tác tử viếng thăm đầy đủ các ô nhớ trong suốt 5.000 episodes và đều hội tụ về cùng một chính sách tối ưu (không giảm giá).")

    add_p("3. Hệ quả tiêu cực khi Khám phá quá mức hoặc Dừng khám phá quá sớm:", indent=True)
    add_bullet("Hệ quả khi Khám phá quá mức (Over-Exploration): Tác tử liên tục thực hiện các hành động ngẫu nhiên dưới mức tối ưu. Trong bối cảnh kinh doanh, điều này tương đương với việc doanh nghiệp liên tục thử nghiệm các mức giảm giá bừa bãi làm thất thoát doanh thu trực tiếp, đồng thời đưa các tín hiệu nhiễu vào quá trình huấn luyện khiến tốc độ hội tụ chậm lại.")
    add_bullet("Hệ quả khi Dừng khám phá quá sớm (Premature Exploitation / Under-Exploration): Nếu ε giảm quá nhanh hoặc đặt ε_start quá bé, tác tử có thể chỉ thử một hành động vài lần trong điều kiện không may gặp nhu cầu thấp (d=0) và lầm tưởng rằng hành động đó tồi tệ. Hậu quả là tác tử bị kẹt vĩnh viễn tại cực trị địa phương (suboptimal local policy) và bỏ lỡ hành động tối ưu toàn cục thực sự.")

    # -------------------------------------------------------------------------
    # QUESTION 5
    # -------------------------------------------------------------------------
    add_h2("Question 5. Reward and Business Objectives (Hàm phần thưởng và Mục tiêu Kinh doanh)")
    add_callout("Nội dung Câu hỏi 5:", 
                "Explain why offering a discount may increase sales but decrease profit per sale. Using the specified price, unit cost, and discount rate, calculate the profit per sale with and without a discount. Discuss how changing the reward function could alter the agent's learned behavior.")
    
    add_p("1. Bản chất kinh tế của sự đánh đổi giữa Lượng bán và Biên lợi nhuận (Volume vs. Margin Trade-off):", indent=True)
    add_p("Giảm giá là con dao hai lưỡi trong quản trị kinh doanh. Khi giảm giá 20%, sản phẩm trở nên hấp dẫn hơn đối với người tiêu dùng, giúp tăng xác suất chuyển đổi mua hàng thêm +0.15 (tương đương 15 điểm phần trăm), từ đó kéo theo số lượng đơn hàng bán được S_i tăng lên. Tuy nhiên, mức giá thực thu trên mỗi đơn vị sản phẩm bị cắt giảm, trong khi chi phí giá vốn hàng bán C không đổi. Điều này dẫn tới sự sụt giảm nghiêm trọng của biên lợi nhuận trên từng đơn hàng.")

    add_p("2. Tính toán giải tích Lợi nhuận trên mỗi đơn hàng (Profit per Sale):", indent=True)
    add_bullet("Trường hợp Không giảm giá (a = 0):")
    add_formula("Price₀ = $10.0 ;    Cost = $5.0 ;    Margin₀ = 10.0 - 5.0 = $5.0", "(5.5)")
    add_bullet("Trường hợp Có giảm giá 20% (a = 1):")
    add_formula("Price₁ = 10.0 × (1 - 0.20) = $8.0 ;    Cost = $5.0 ;    Margin₁ = 8.0 - 5.0 = $3.0", "(5.6)")
    add_bullet("Mức độ sụt giảm biên lợi nhuận đơn vị:")
    add_formula("Δ Margin = (3.0 - 5.0) / 5.0 = -2.0 / 5.0 = -40.0%", "(5.7)")

    add_p("3. Chứng minh toán học vì sao việc giảm giá làm giảm tổng lợi nhuận kỳ vọng:", indent=True)
    add_p("Xét trường hợp thị trường nhu cầu cao (d = 1, N = 20 khách) và đối thủ không giảm giá (a_{-i} = 0):")
    add_bullet("Nếu Tác tử chọn Không giảm giá (a = 0): Xác suất chuyển đổi là p = 0.30 + 0.25(1) + 0 - 0 = 0.55. Doanh số kỳ vọng E[S] = 20 × 0.55 = 11 đơn hàng. Tổng lợi nhuận kỳ vọng = 11 × $5.0 = $55.0.")
    add_bullet("Nếu Tác tử chọn Giảm giá 20% (a = 1): Xác suất chuyển đổi tăng lên p = 0.30 + 0.25(1) + 0.15 - 0 = 0.70. Doanh số kỳ vọng E[S] = 20 × 0.70 = 14 đơn hàng. Tổng lợi nhuận kỳ vọng = 14 × $3.0 = $42.0.")
    add_p("Kết luận: Lợi nhuận kỳ vọng sụt giảm tới $13.0 (tương đương giảm 23.6%)! Mức tăng 3 đơn hàng bán thêm (tạo thêm 3 × $3 = $9 doanh thu thặng dư) hoàn toàn không thể bù đắp được mức hao hụt $2 trên mỗi đơn hàng đối với 11 đơn hàng cơ sở (thất thoát 11 × $2 = $22). Đây chính là lý do toán học giải thích vì sao tác tử RL thông minh đã học được cách từ chối giảm giá!")

    add_p("4. Tác động khi thay đổi hàm phần thưởng (Reward Function Shaping):", indent=True)
    add_bullet("Nếu chuyển sang hàm thưởng Tối đa hóa Doanh thu (Revenue Maximization - r = S × P_eff): Khi a=0, doanh thu kỳ vọng là 11 × $10 = $110. Khi a=1, doanh thu kỳ vọng là 14 × $8 = $112. Doanh thu khi giảm giá cao hơn ($112 > $110)! Tác tử sẽ đảo ngược chính sách và liên tục giảm giá.")
    add_bullet("Nếu chuyển sang hàm thưởng Tối đa hóa Thị phần (Market Share Maximization - r = S_i / (S_1 + S_2)): Tác tử sẽ hoàn toàn phớt lờ chi phí sản xuất, liên tục chiết khấu kịch khung nhằm triệt hạ lượng khách của đối thủ, dẫn tới cuộc chiến giá cả hủy diệt (destructive price war).")

    # -------------------------------------------------------------------------
    # QUESTION 6
    # -------------------------------------------------------------------------
    add_h2("Question 6. Performance Evaluation (Đánh giá Hiệu năng Định lượng)")
    add_callout("Nội dung Câu hỏi 6:", 
                "Calculate the average reward per time step for each agent from your experimental data. Compare their performance using a table or figure. Explain why one training run is insufficient to establish that one approach is generally superior.")
    
    add_p("1. Tính toán Phần thưởng Trung bình trên mỗi bước thời gian từ Dữ liệu Thực nghiệm:", indent=True)
    add_p("Tổng số bước đánh giá độc lập là 500 episodes × 20 steps = 10.000 bước. Từ file baseline_evaluation.csv:")
    add_bullet("RL Agent (Q-Learning): Tổng phần thưởng = $351.275,0. Phần thưởng trung bình trên mỗi bước thời gian: $351.275 / 10.000 = $35,1275 / bước.")
    add_bullet("Rule-Based Agent: Tổng phần thưởng = $349.685,0. Phần thưởng trung bình trên mỗi bước thời gian: $349.685 / 10.000 = $34,9685 / bước.")
    add_bullet("Chênh lệch tuyệt đối: RL Agent thu được nhiều hơn Rule-based Agent là +$1.590,0 trên toàn bộ quá trình đánh giá, tương đương mức chênh lệch nhỏ +$0,1590 / bước (+0.45%).")

    add_p("2. Luận giải vì sao một lần chạy đơn lẻ (Single Run) là hoàn toàn không đủ để kết luận tính vượt trội:", indent=True)
    add_p("Trong một môi trường có tính stochastic cao như mô phỏng thương mại điện tử này, một lần chạy đơn lẻ không thể đại diện cho hiệu năng tổng quát vì hai nguồn nhiễu ngẫu nhiên lớn:")
    add_bullet("Nhiễu ngẫu nhiên từ Nhu cầu thị trường (Demand Shock): Nhu cầu d_t được sinh ngẫu nhiên độc lập 50/50. Nếu trong một lần chạy ngẫu nhiên, một tác tử tình cờ gặp nhiều bước có d_t = 1 hơn (thị trường 20 khách thay vì 10 khách), tác tử đó sẽ có phần thưởng cao hơn hẳn đơn thuần do may mắn thống kê chứ không phải do chính sách thông minh hơn.")
    add_bullet("Nhiễu ngẫu nhiên từ Phân phối Doanh số Nhị thức (Binomial Sales Draw): Ngay cả khi xác suất chuyển đổi p cố định, số đơn hàng thực tế S ~ Binomial(N, p) vẫn có phương sai Var(S) = N p (1 - p). Sự thăng trầm ngẫu nhiên của xúc xắc nhị thức tạo ra độ lệch chuẩn quanh mức ±10.4$/bước.")
    add_p("Chính vì vậy, phương pháp luận nghiên cứu khoa học bắt buộc phải thực hiện kiểm định đa hạt giống ngẫu nhiên (Multi-seed testing) và báo cáo khoảng tin cậy (Confidence Intervals) kèm độ lệch chuẩn.")

    # -------------------------------------------------------------------------
    # QUESTION 7
    # -------------------------------------------------------------------------
    add_h2("Question 7. Learning Rate and Stability (Tốc độ học và Tính Ổn định)")
    add_callout("Nội dung Câu hỏi 7:", 
                "Compare the Q-learning results for at least three learning rates. Describe how the learning rate affects updating, stability, and sensitivity to new observations. Support your discussion with measured results.")
    
    add_p("1. So sánh kết quả định lượng của 3 mức tốc độ học α ∈ {0.01, 0.10, 0.50}:", indent=True)
    lr_headers = ["Tốc độ học α", "Ý nghĩa Động học", "Phần thưởng TB/Bước ($)", "Tỷ lệ Giảm giá (%)", "Nhận định Ổn định & Hội tụ"]
    lr_data = [
        ["α = 0.01", "Cập nhật thận trọng, hấp thu chậm", "35.2475", "0.00%", "Hội tụ mượt mà, loại bỏ nhiễu tốt, giữ nguyên giá tối ưu."],
        ["α = 0.10", "Chuẩn mực, cân bằng tối ưu", "35.2475", "0.00%", "Tốc độ học lý tưởng, ổn định tuyệt đối, đạt phần thưởng cao nhất."],
        ["α = 0.50", "Cập nhật hung hăng, nhạy cảm quá mức", "28.5085", "40.52%", "Mất ổn định nghiêm trọng, Q-table dao động, giảm giá sai lầm 40.5%."]
    ]
    format_table(lr_headers, lr_data, [Inches(1.0), Inches(1.8), Inches(1.2), Inches(1.1), Inches(2.1)])

    add_p("2. Luận giải bản chất tác động của Learning Rate đến cập nhật và độ ổn định:", indent=True)
    add_bullet("Tốc độ học nhỏ (α = 0.01): Đại diện cho sự bảo thủ. Mỗi trải nghiệm mới chỉ đóng góp 1% vào việc điều chỉnh giá trị Q. Tác tử lọc nhiễu nhị thức cực kỳ tốt. Tuy nhiên, nếu không gian trạng thái lớn hoặc môi trường biến động nhanh, α quá bé sẽ khiến tác tử mất hàng triệu bước mới thích nghi được.")
    add_bullet("Tốc độ học tối ưu (α = 0.10): Cung cấp sự cân bằng lý tưởng. Tác tử mất khoảng vài trăm episodes để đưa bảng Q tiệm cận giá trị thực và duy trì ổn định trong suốt phần đời còn lại.")
    add_bullet("Tốc độ học lớn (α = 0.50): Gây ra hiện tượng mất ổn định nghiêm trọng (Catastrophic Instability). Khi α = 0.5, tác tử cho phép phần thưởng ngẫu nhiên của một bước đơn lẻ thay đổi tới 50% giá trị ô nhớ Q. Khi gặp một bước may mắn mà hành động giảm giá (a=1) tình cờ rơi vào ngày cầu cao và xúc xắc nhị thức sinh ra số đơn hàng tối đa, giá trị Q(s, 1) bị đẩy vọt lên giả tạo. Tác tử lập tức tin rằng giảm giá là tối ưu và liên tục giảm giá ở các bước tiếp theo, khiến tỷ lệ giảm giá vọt lên 40.52% và kéo sụt lợi nhuận tới 19.1% (từ 35.25$ xuống 28.51$).")

    # -------------------------------------------------------------------------
    # QUESTION 8
    # -------------------------------------------------------------------------
    add_h2("Question 8. Multi-Agent Interaction and Non-Stationarity (Tương tác Đa tác tử và Tính Phi Dừng)")
    add_callout("Nội dung Câu hỏi 8:", 
                "Explain how the other agent's actions influence an agent's rewards and observations. Why can independent Q-learning become difficult when both agents learn simultaneously? Suggest one experimental change that could help investigate this problem.")
    
    add_p("1. Cơ chế tác động của hành động đối thủ đến phần thưởng và quan sát của tác tử:", indent=True)
    add_bullet("Tác động trực tiếp đến phần thưởng (Reward Channel): Thông qua hàm chuyển đổi p_i(t) = clip(0.30 + 0.25 d_t + 0.15 a_i(t) - 0.10 a_{-i}(t)), nếu đối thủ chọn giảm giá (a_{-i} = 1), xác suất chuyển đổi của tác tử i bị trừ đi 0.10. Doanh số bán kỳ vọng giảm trực tiếp 1 đơn vị (khi cầu thấp) hoặc 2 đơn vị (khi cầu cao), làm suy giảm doanh thu và lợi nhuận ròng.")
    add_bullet("Tác động đến quan sát trạng thái tương lai (State Transition Channel): Trạng thái mà tác tử i quan sát được ở bước kế tiếp s_i(t+1) = (d_{t+1}, c_i(t+1)) có thành phần c_i(t+1) bằng chính hành động a_{-i}(t) của đối thủ. Như vậy, quỹ đạo trạng thái tương lai hoàn toàn bị chi phối bởi quyết định của đối thủ.")

    add_p("2. Vì sao Q-Learning Độc lập (Independent Q-Learning - IQL) gặp khó khăn khi hai tác tử cùng học đồng thời?", indent=True)
    add_p("Nguyên nhân cốt tử nằm ở Hiện tượng Môi trường Phi dừng (The Non-Stationarity Problem):")
    add_bullet("Sự vi phạm Tính chất Markov (Violation of Markov Property): Thuật toán Q-learning kinh điển được chứng minh toán học là sẽ hội tụ về chính sách tối ưu duy nhất với điều kiện môi trường là một MDP dừng (Stationary Markov Decision Process), nghĩa là hàm chuyển trạng thái P(s'|s, a) và hàm thưởng R(s, a) là bất biến theo thời gian.")
    add_bullet("Bài toán Mục tiêu Di động (Moving Target Problem): Khi cả Agent 1 và Agent 2 cùng học và cập nhật chính sách đồng thời, từ góc nhìn của Agent 1, đối thủ Agent 2 là một phần của môi trường. Nhưng vì Agent 2 đang liên tục thay đổi chính sách π_2(a_2|s_2), xác suất chuyển trạng thái và phân phối phần thưởng của Agent 1 cũng liên tục bị bẻ cong theo thời gian. Mục tiêu học TD Target r + γ max Q(s', a') trở thành một mục tiêu di động, khiến các giá trị Q đã học trong quá khứ bị lỗi thời và thuật toán mất hoàn toàn bảo đảm hội tụ.")

    add_p("3. Đề xuất Thực nghiệm Kiểm chứng và Kết quả Đo lường Thực tế:", indent=True)
    add_p("Chúng tôi đã thiết kế và triển khai kịch bản Extension A trong file run_extension_experiments.py: Cho phép cả hai tác tử đều sử dụng Tabular Q-Learning với cùng tham số và cùng học đồng thời qua 5.000 episodes.")
    add_p("Kết quả đo lường thực tế:")
    add_bullet("Trong giai đoạn đầu (1.000 episodes đầu), sự thăm dò hỗn loạn của cả hai tác tử tạo ra sự giao động mạnh về phần thưởng.")
    add_bullet("Tuy nhiên, nhờ không gian trạng thái đối xứng và hình phạt kinh tế quá nặng của việc giảm giá (mất 40% biên lãi), cả hai tác tử cuối cùng đã cùng hội tụ về điểm cân bằng không giảm giá (Mutual Cooperation / Zero-Discount Equilibrium).")
    add_bullet("Tại giai đoạn đánh giá độc lập: Agent 1 đạt $34.9055/bước (0% giảm giá) và Agent 2 đạt $34.9865/bước (0% giảm giá). Điều này chứng minh rằng trong cấu trúc ma trận chi trả này, điểm cân bằng không giảm giá là một điểm hút Pareto rất mạnh.")

    # -------------------------------------------------------------------------
    # QUESTION 9
    # -------------------------------------------------------------------------
    add_h2("Question 9. Limitations and Robustness (Hạn chế Mô phỏng và Cài đặt Mở rộng)")
    add_callout("Nội dung Câu hỏi 9:", 
                "Identify at least three limitations of the reference simulation or its assumptions. Propose and implement one modification, such as changing demand dynamics, discount size, customer conversion, or competitor behavior. Explain how the modification affects the results.")
    
    add_p("1. Nhận diện ba hạn chế cốt tử của mô hình mô phỏng cơ sở:", indent=True)
    add_bullet("Hạn chế 1: Đối thủ cạnh tranh quá thụ động và cứng nhắc (Predictable & Naive Opponent). Tác tử đối chứng chỉ hành động theo 3 luật IF/THEN cố định, không có khả năng học hỏi hay thay đổi mức chiết khấu. Trong thực tế thương mại điện tử, các đối thủ là những thuật toán định giá động tinh vi, có thể chủ động áp dụng chiến lược giá săn mồi (predatory pricing) hoặc định giá thuật toán cấu kết ngầm (algorithmic collusion).")
    add_bullet("Hạn chế 2: Bỏ qua hoàn toàn chi phí tồn kho và giới hạn năng lực cung ứng (Zero Inventory Holding Cost). Mô hình giả định khả năng cung ứng hàng hóa là vô hạn: bán bao nhiêu cũng có sẵn hàng mà không phải chịu chi phí lưu kho cho các đơn vị hàng ế thừa, cũng như không có chi phí phạt khi đứt gãy chuỗi cung ứng.")
    add_bullet("Hạn chế 3: Không gian trạng thái và hành động bị rời rạc hóa thô thiển (Discretization & Rigid Linearity). Thị trường chỉ có 2 mức giá (0% hoặc 20%), không có mức chiết khấu liên tục (ví dụ 5%, 10%, 15%). Hàm chuyển đổi khách hàng p_i là một hàm tuyến tính thô sơ bị chặn bởi hàm clip, chưa phản ánh được độ co giãn của cầu theo giá phi tuyến tính (Price Elasticity of Demand).")

    add_p("2. Đề xuất và Hiện thực hóa Mã nguồn Mở rộng (Implemented Extensions):", indent=True)
    add_p("Để giải quyết triệt để các hạn chế trên, chúng tôi đã lập trình và thực thi thành công 2 mô hình mở rộng trong file run_extension_experiments.py:")
    add_bullet("Mô hình Mở rộng 1: Kịch bản Đối thủ Hung hăng Phá giá (Aggressive Competitor). Đối thủ liên tục tung ra các chương trình chiết khấu giảm giá với xác suất p = 0.80 nhằm cướp đoạt khách hàng, ép tác tử RL vào trạng thái đối đầu liên tục.")
    add_bullet("Mô hình Mở rộng 2: Môi trường có Ràng buộc Tồn kho & Chi phí Lưu kho (Inventory Constrained Environment). Tại mỗi bước, doanh nghiệp chỉ nhập về mức tồn kho trần Stock = 12 đơn vị. Nếu hàng không bán hết, doanh nghiệp phải trả phí lưu kho $1.5 / đơn vị thừa. Nếu nhu cầu khách vượt quá 12 đơn vị, doanh nghiệp bị phạt $0.5 / khách hàng bỏ lỡ do hết hàng.")

    add_p("3. Phân tích Tác động và Ý nghĩa của Kết quả Mở rộng:", indent=True)
    add_bullet("Tác động của Đối thủ Hung hăng: Khi đối thủ liên tục giảm giá (tỷ lệ giảm giá 80.18%), mặt bằng phần thưởng của toàn bộ thị trường bị kéo tụt xuống (từ ~35.1$ xuống còn ~28.8$/bước). Tuy nhiên, tác tử RL đã bộc lộ sự thông minh vượt bậc: thay vì bị cuốn vào cuộc chiến giảm giá để trả đũa (giống như Luật 2 của tác tử luật), bảng Q của RL Agent xác định rằng giá trị của hành động không giảm giá Q(s, 0) luôn cao hơn Q(s, 1) ở mọi trạng thái! Tác tử RL kiên định duy trì 0.00% tỷ lệ giảm giá, chấp nhận bán ít đơn hàng hơn nhưng giữ nguyên biên lãi $5.0 thay vì $3.0, qua đó đạt $28.7990/bước và tránh được sự phá sản của cuộc đua xuống đáy.")
    add_bullet("Tác động của Ràng buộc Tồn kho: Do phải gánh thêm chi phí lưu kho cho các sản phẩm ế thừa khi nhu cầu thấp, phần thưởng trung bình của cả hai tác tử giảm xuống $25.78/bước. Kết quả này phản ánh chân thực áp lực quản trị chuỗi cung ứng trong thương mại điện tử.")

    # -------------------------------------------------------------------------
    # QUESTION 10
    # -------------------------------------------------------------------------
    add_h2("Question 10. Design a Better Intelligent Agent (Đề xuất Thiết kế Tác tử Thông minh Tiên tiến)")
    add_callout("Nội dung Câu hỏi 10:", 
                "Propose an improved agent or experimental framework for the e-commerce problem. Specify its state representation, actions, reward function, learning or decision-making method, and evaluation procedure. Explain how you would test whether your proposed approach is more robust than both the reference RL agent and the reference rule-based agent.")
    
    add_p("1. Đề xuất Kiến trúc Tác tử Toàn diện Nâng cao (Advanced MARL Agent Architecture):", indent=True)
    add_bullet("Không gian trạng thái mở rộng (Enriched Continuous State Representation): Thay vì chỉ có 4 trạng thái thô sơ, véc-tơ trạng thái s_t bao gồm: (1) Dự báo xu hướng nhu cầu thị trường dạng liên tục d_t ∈ [0, 1]; (2) Mức tồn kho khả dụng hiện tại I_t; (3) Lịch sử 5 bước gần nhất của đối thủ để ước lượng xác suất đối thủ giảm giá p_comp(t); (4) Thời gian còn lại của mùa vụ kinh doanh t/T.")
    add_bullet("Không gian hành động mịn/liên tục (Fine-Grained Continuous Action Space): Thay vì nhị phân 0 hoặc 1, cho phép tác tử chọn mức chiết khấu liên tục a_t = δ_t ∈ [0.00, 0.35] (chiết khấu từ 0% đến 35%) hoặc phân rã thành 8 nấc rời rạc {0%, 5%, 10%, 15%, 20%, 25%, 30%, 35%}.")
    add_bullet("Hàm phần thưởng Pareto Đa mục tiêu (Multi-Objective Reward Function): Kết hợp hài hòa giữa lợi nhuận gộp, chi phí lưu kho và thị phần thương hiệu:")
    add_formula("Rₜ = Profitₜ - λ_hold · max(0, Iₜ - Sₜ) - λ_stockout · max(0, Dₜ - Iₜ) + β · [ Sᵢ,ₜ / (S₁,ₜ + S₂,ₜ) ]", "(5.8)")
    add_bullet("Phương pháp Học và Ra quyết định (Learning Algorithm): Sử dụng thuật toán Deep Deterministic Policy Gradient (DDPG) hoặc PPO (Proximal Policy Optimization) kết hợp mạng Nơ-ron Mô hình hóa Đối thủ (Opponent Modeling Network). Mạng đối thủ dự đoán hành động tiếp theo của đối thủ, cho phép tác tử tính toán trước phản ứng tối ưu thay vì chỉ phản ứng bị động.")

    add_p("2. Quy trình Đánh giá Độ bền vững (Robustness Verification Protocol):", indent=True)
    add_p("Để chứng minh tác tử đề xuất vượt trội hơn cả Reference RL và Reference Rule-Based Agent, chúng tôi thiết lập một Giải đấu Đối kháng Đa dạng (Tournament Benchmark) qua 4 vòng thi đấu:")
    add_bullet("Vòng 1 (Đối đầu Đối thủ Ngẫu nhiên): Kiểm tra khả năng khai thác tối đa lợi nhuận trước các đối thủ hành động không có quy luật.")
    add_bullet("Vòng 2 (Đối đầu Đối thủ Săn mồi / Predatory Competitor): Đánh giá năng lực bảo vệ biên lợi nhuận và quản trị rủi ro dòng tiền khi đối thủ liên tục phá giá.")
    add_bullet("Vòng 3 (Đối đầu Tác tử Học sâu Tiên tiến): Kiểm tra khả năng thích ứng trong môi trường phi dừng và khả năng hội tụ về các thế cân bằng cấu kết ngầm cùng có lợi.")
    add_bullet("Vòng 4 (Kiểm thử Độ sốc Thị trường - Stress Testing): Thay đổi đột ngột giá vốn hàng bán C hoặc xuất hiện các cú sốc sụt giảm nhu cầu tiêu dùng N_t.")
    add_p("Chỉ số đánh giá tổng hợp bao gồm: Lợi nhuận tích lũy trung bình (Mean Cumulative Profit), Hệ số Sharpe của dòng tiền (đo lường độ ổn định rủi ro), và Mức sụt giảm tối đa (Max Drawdown).")

    # =========================================================================
    # SECTION 6: DISCUSSION, LIMITATIONS, AND PROPOSED IMPROVEMENTS
    # =========================================================================
    add_h1("6. DISCUSSION, LIMITATIONS, AND PROPOSED IMPROVEMENTS (THẢO LUẬN SÂU, HẠN CHẾ & CẢI TIẾN)")
    
    add_h2("6.1. Phân biệt Bản chất giữa Quan sát Thực nghiệm và Giải thích Nhân quả")
    add_p("Một nguyên tắc tối thượng trong nghiên cứu khoa học được Thầy nhấn mạnh tại Section 9 là: Sinh viên bắt buộc phải phân biệt rạch ròi giữa 'Quan sát thực nghiệm' (Observation) và 'Giải thích nhân quả' (Causal Explanation):")
    add_bullet("Quan sát thực nghiệm (Observation): Tại thực nghiệm Baseline, tác tử RL đạt phần thưởng trung bình $35.1275/bước, cao hơn mức $34.9685/bước của Rule-based Agent; đồng thời cả hai tác tử đều có tỷ lệ giảm giá 0.00% trong suốt 500 episodes đánh giá.")
    add_bullet("Giải thích nhân quả sai lầm (Flawed Explanation): 'Tác tử RL thông minh hơn nên luôn đánh bại tác tử luật nhờ thuật toán học tăng cường tối ưu'.")
    add_bullet("Giải thích nhân quả chính xác (Rigorous Causal Explanation): Cả hai tác tử đều có tỷ lệ giảm giá 0.00% là do cấu trúc ma trận chi trả kinh tế và hàm chuyển đổi nhị thức. Việc giảm giá làm giảm 40% biên lợi nhuận trên mỗi đơn hàng nhưng chỉ làm tăng tối đa 15% xác suất mua hàng. Về mặt kỳ vọng toán học, hành động giảm giá mang lại lợi nhuận kỳ vọng thấp hơn hành động giữ nguyên giá trong mọi kịch bản đối thủ không giảm giá. Tác tử RL sau quá trình thử-sai đã học được ma trận Q với Q(s, 0) > Q(s, 1), trong khi tác tử Rule-based ngay từ đầu đã có Luật 3 quy định không giảm giá khi đối thủ không giảm giá. Sự chênh lệch nhỏ 0.45% hoàn toàn là do sự biến động ngẫu nhiên của các chuỗi ngày nhu cầu và xúc xắc nhị thức giữa các lượt chạy chứ không phải do sự áp đảo về trí thông minh.")

    add_h2("6.2. Khoảng cách giữa Mô hình Hàn lâm và Thị trường Thương mại Điện tử Thực tế")
    add_p("Mặc dù mô phỏng mang lại những hiểu biết lý thuyết sâu sắc, khoảng cách giữa phòng thí nghiệm và thực tiễn thương mại điện tử còn rất lớn:")
    add_bullet("Tính bất đối xứng thông tin (Information Asymmetry): Trong mô hình, tác tử quan sát được chính xác nhu cầu thị trường và hành động giảm giá của đối thủ. Trên thực tế, các sàn thương mại điện tử không bao giờ công khai lưu lượng truy cập thực hay các chương trình khuyến mãi ẩn (như voucher cá nhân hóa cho từng tài khoản người dùng).")
    add_bullet("Vấn đề Cấu kết Thuật toán (Algorithmic Collusion): Nghiên cứu của Calvano et al. (2020) trên tạp chí American Economic Review đã chỉ ra rằng khi các thuật toán Q-learning được triển khai độc lập trên thị trường, chúng có xu hướng tự động 'bắt tay ngầm' neo giá ở mức độc quyền cao mà không cần bất kỳ sự liên lạc trực tiếp nào. Đây là một rủi ro pháp lý và đạo đức lớn mà các cơ quan chống độc quyền đang phải đối mặt.")

    # =========================================================================
    # SECTION 7: CONCLUSION
    # =========================================================================
    add_h1("7. CONCLUSION (KẾT LUẬN)")
    add_p("Báo cáo thực hành Laboratory Experiment 02 đã hoàn thành trọn vẹn toàn bộ các mục tiêu nghiên cứu, cài đặt thực nghiệm, phân tích dữ liệu và giải quyết thấu đáo toàn bộ 10 câu hỏi phòng thí nghiệm chuyên sâu. Các phát hiện cốt lõi có thể được đúc kết như sau:")
    add_bullet("1. Bản chất của sự đánh đổi kinh tế: Giảm giá kích cầu là một chiến lược nguy hiểm nếu không có sự tính toán kỹ lưỡng về độ co giãn giá. Việc mất 40% biên lợi nhuận không thể được bù đắp bởi mức tăng 15% lượng chuyển đổi, dẫn tới việc chính sách giữ nguyên giá gốc là một điểm cân bằng chi phối.")
    add_bullet("2. Sức mạnh và Giới hạn của Q-Learning: Tabular Q-learning thể hiện khả năng khám phá và tìm ra chính sách tối ưu rất ấn tượng trong không gian trạng thái rời rạc nhỏ. Tuy nhiên, thuật toán cực kỳ nhạy cảm với tốc độ học α. Đặt α quá cao (0.50) sẽ phá hủy hoàn toàn sự ổn định của hệ thống trong môi trường có nhiễu ngẫu nhiên.")
    add_bullet("3. Hiện tượng Phi dừng trong MAS: Khi hai tác tử cùng học đồng thời, môi trường không còn tính dừng. Tuy nhiên, trong bài toán định giá này, cấu trúc lợi nhuận khắc nghiệt đã dẫn dắt cả hai tác tử vượt qua sự hỗn loạn ban đầu để cùng hội tụ về điểm cân bằng không giảm giá cùng có lợi.")
    add_bullet("4. Khả năng Phòng thủ Biên lãi: Trong kịch bản đối thủ hung hăng phá giá (Ext B), tác tử RL đã chứng minh tính ưu việt khi kiên định giữ nguyên giá gốc, bảo toàn dòng tiền và tránh được cuộc chiến giá cả tự sát.")

    # =========================================================================
    # SECTION 8: PYTHON SOURCE CODE EXTRACTS
    # =========================================================================
    add_h1("8. PYTHON SOURCE CODE EXTRACTS (TRÍCH DẪN MÃ NGUỒN PYTHON CỐT LÕI)")
    add_p("Dưới đây là các đoạn mã nguồn then chốt được trích xuất từ tệp thực nghiệm `agent02_experiment.py` và `run_extension_experiments.py` minh chứng cho quá trình triển khai:")

    add_h2("8.1. Thuật toán Cập nhật Bellman của Tác tử Q-Learning")
    add_callout("Mã nguồn Cập nhật Q-Learning (QLearningAgent.learn):",
"""def learn(self, state, action, reward, next_state, terminal=False):
    demand, competitor_previous_action = state
    next_demand, next_competitor_action = next_state
    old_value = self.q[demand, competitor_previous_action, action]
    if terminal:
        target = reward
    else:
        best_future_value = np.max(self.q[next_demand, next_competitor_action])
        target = reward + self.gamma * best_future_value
    # Cập nhật Bellman Q-learning
    self.q[demand, competitor_previous_action, action] = old_value + self.alpha * (target - old_value)""")

    add_h2("8.2. Môi trường Mở rộng Ràng buộc Tồn kho và Chi phí Lưu kho (Extension C)")
    add_callout("Mã nguồn Môi trường Tồn kho (InventoryConstrainedEnvironment.step):",
"""# Inventory constraints & holding cost calculation
actual_sales = min(demand_realized, self.stock_level)
unsold_units = max(0, self.stock_level - demand_realized)
unmet_demand = max(0, demand_realized - self.stock_level)

effective_price = self.config.price * (1.0 - self.config.discount_rate * own_action)
gross_profit = actual_sales * (effective_price - self.config.unit_cost)
penalties = unsold_units * self.holding_cost + unmet_demand * self.stockout_penalty
net_profit = gross_profit - penalties
rewards.append(float(net_profit))""")

    # =========================================================================
    # SECTION 9: REFERENCES
    # =========================================================================
    add_h1("9. REFERENCES (TÀI LIỆU THAM KHẢO CHUẨN IEEE)")
    refs = [
        "[1] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction, 2nd ed. Cambridge, MA: The MIT Press, 2018.",
        "[2] C. J. Watkins and P. Dayan, 'Q-learning,' Machine Learning, vol. 8, no. 3-4, pp. 279-292, 1992.",
        "[3] S. Russell and P. Norvig, Artificial Intelligence: A Modern Approach, 4th ed. Hoboken, NJ: Pearson, 2020.",
        "[4] M. L. Littman, 'Markov games as a framework for multi-agent reinforcement learning,' in Machine Learning Proceedings, Elsevier, 1994, pp. 157-163.",
        "[5] E. Calvano, G. Calzolari, V. Denicolò, and S. Pastorello, 'Artificial intelligence, algorithmic pricing, and collusion,' American Economic Review, vol. 110, no. 10, pp. 3267-3297, 2020.",
        "[6] V. Mnih et al., 'Human-level control through deep reinforcement learning,' Nature, vol. 518, no. 7540, pp. 529-533, 2015.",
        "[7] Trần Đình Quế, Bài giảng và Tài liệu Hướng dẫn Thực hành Phát triển Hệ thống Thông minh: Laboratory Experiment 02, Học viện Công nghệ Bưu chính Viễn thông, 2026."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Cm(0.8)
        p_ref.paragraph_format.first_line_indent = Cm(-0.8)
        p_ref.paragraph_format.space_after = Pt(3)
        run_r = p_ref.add_run(r)
        run_r.font.size = Pt(10.5)

    # Save to files
    out_docx_exp = Path("agent02_experiments/agent02_06_15_taint.docx")
    out_docx_root = Path("agent02_06_15_taint.docx")
    
    doc.save(out_docx_exp)
    doc.save(out_docx_root)
    print(f"[+] Successfully generated DOCX at {out_docx_exp.resolve()}")
    print(f"[+] Successfully copied DOCX to {out_docx_root.resolve()}")

if __name__ == "__main__":
    create_report()
