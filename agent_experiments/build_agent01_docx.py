import os
import sys
import shutil
import re
sys.stdout.reconfigure(encoding='utf-8')
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def sanitize_text(text):
    if not isinstance(text, str):
        return str(text)
    # Loại bỏ các ký tự điều khiển không tương thích XML
    return ''.join(ch for ch in text if ch in '\n\r\t' or (32 <= ord(ch) <= 0x10FFFF))

def build_agent01_report():
    print("=== BẮT ĐẦU TẠO BÁO CÁO ASSIGNMENT AGENT 01: agent01_06_15_taint.docx ===")
    
    doc = docx.Document()
    
    # -------------------------------------------------------------------------
    # 1. ĐỊNH DẠNG TRANG & STYLE CHUẨN LUẬN VĂN PTIT
    # -------------------------------------------------------------------------
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
    
    # Helper formatting functions
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

    def add_bullet(text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.2
        r_b = p.add_run("•  ")
        r_b.bold = True
        r_b.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        r_t = p.add_run(sanitize_text(text))
        r_t.font.size = Pt(11.5)
        return p

    def add_formula(eq_text, eq_num=""):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(sanitize_text(eq_text))
        run.font.name = 'Cambria Math'
        run.font.size = Pt(11.5)
        run.font.italic = True
        if eq_num:
            r_num = p.add_run(f"    {eq_num}")
            r_num.font.name = 'Times New Roman'
            r_num.font.italic = False
            r_num.bold = True
        return p

    def add_image_figure(img_path, fig_title, comment=None, width_inch=6.0):
        if not os.path.exists(img_path):
            print(f"[!] Cảnh báo: Không tìm thấy ảnh tại {img_path}")
            return
            
        # Tự động điều chỉnh kích thước để ảnh và chú thích nằm trọn trong 1 trang
        actual_width = width_inch
        try:
            from PIL import Image
            with Image.open(img_path) as im:
                w, h = im.size
                aspect = w / h
                if aspect < 0.72:
                    actual_width = 4.8
                elif aspect < 0.85:
                    actual_width = 5.2
                elif aspect < 1.0:
                    actual_width = 5.5
                else:
                    actual_width = 5.8
        except Exception:
            pass
            
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(actual_width))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(2)
        run_cap = p_cap.add_run(sanitize_text(fig_title))
        run_cap.bold = True
        run_cap.font.size = Pt(10)
        run_cap.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        
        if comment:
            p_cm = doc.add_paragraph()
            p_cm.paragraph_format.left_indent = Cm(0.8)
            p_cm.paragraph_format.space_after = Pt(3)
            p_cm.paragraph_format.line_spacing = 1.15
            run_cm_t = p_cm.add_run("Nhận xét học thuật: ")
            run_cm_t.bold = True
            run_cm_t.font.size = Pt(9.5)
            run_cm_t.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
            run_cm_b = p_cm.add_run(sanitize_text(comment))
            run_cm_b.font.size = Pt(9.5)
            run_cm_b.font.italic = True
            run_cm_b.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    def format_table_header_data(tbl, headers, data, col_widths=None):
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
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
                
        set_table_borders(tbl, color="CBD5E0")
        if col_widths:
            for row in tbl.rows:
                for j, w in enumerate(col_widths):
                    row.cells[j].width = Cm(w)
                    
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(4)

    screens_dir = os.path.join(os.path.dirname(__file__), 'screens')

    # -------------------------------------------------------------------------
    # 2. TRANG BÌA CHÍNH (COVER PAGE)
    # -------------------------------------------------------------------------
    p_b1 = doc.add_paragraph()
    p_b1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b1.paragraph_format.space_before = Pt(10)
    p_b1.paragraph_format.space_after = Pt(2)
    r = p_b1.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    r = p_b1.add_run("KHOA CÔNG NGHỆ THÔNG TIN 1")
    r.font.size = Pt(12)
    r.bold = True

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(20)
    p_div.paragraph_format.space_after = Pt(25)
    r_div = p_div.add_run("✦ ✦ ✦ ---------------------------------------- ✦ ✦ ✦")
    r_div.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("BÁO CÁO BÀI TẬP CHUYÊN ĐỀ\n")
    r_title.font.size = Pt(18)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    r_sub = p_title.add_run("PHÁT TRIỂN HỆ THỐNG THÔNG MINH\n")
    r_sub.font.size = Pt(15)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
    
    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_before = Pt(10)
    p_topic.paragraph_format.space_after = Pt(35)
    r_tp = p_topic.add_run("ĐỀ TÀI: DISCOVERING AI AGENT\nTỔNG QUAN LÝ THUYẾT, MÔ THỨC SUY LUẬN REACT VÀ THỰC THI HỆ ĐA TÁC TỬ")
    r_tp.font.size = Pt(13)
    r_tp.bold = True
    r_tp.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    tbl_info = doc.add_table(rows=6, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "PGS. TS. Trần Đình Quế"),
        ("Học phần:", "Phát triển Hệ thống Thông minh"),
        ("Sinh viên thực hiện:", "Nguyễn Tuấn Tài"),
        ("Mã sinh viên:", "B23DCCN731"),
        ("Lớp học phần / Nhóm lớp:", "INT14149_06 / Nhóm 06"),
        ("Nhóm bài tập / Tiểu luận:", "Nhóm 15")
    ]
    for i, (k, v) in enumerate(info_data):
        c1 = tbl_info.cell(i, 0)
        c2 = tbl_info.cell(i, 1)
        c1.width = Cm(6.5)
        c2.width = Cm(8.5)
        p1 = c1.paragraphs[0]
        p2 = c2.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        p2.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(k)
        r1.bold = True
        r1.font.size = Pt(11.5)
        r2 = p2.add_run(v)
        r2.font.size = Pt(11.5)
        r2.bold = (i in [0, 2, 3, 5])
        if i == 2:
            r2.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    set_table_borders(tbl_info, color="FFFFFF")

    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(65)
    r_bot = p_bottom.add_run("HÀ NỘI, THÁNG 10 NĂM 2026")
    r_bot.bold = True
    r_bot.font.size = Pt(12)
    r_bot.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 3. MỤC LỤC TỔNG QUAN
    # -------------------------------------------------------------------------
    add_h1("MỤC LỤC BÁO CÁO CHUYÊN ĐỀ")
    toc_items = [
        ("PHẦN 1: BÁO CÁO NGHIÊN CỨU HIỂU BIẾT CHUYÊN SÂU VỀ AI AGENT", "3"),
        ("  1.1 Khái Niệm Bản Chất và Bước Chuyển Dịch Mô Thức (Paradigm Shift)", "3"),
        ("  1.2 Phân Loại Các Kiến Trúc Tác Tử Thông Minh (Russell - Norvig & IBM)", "4"),
        ("  1.3 Các Mô Thức Suy Luận Hiện Đại: ReAct và ReWOO (IBM Think [2])", "5"),
        ("  1.4 Tác Động Kinh Tế và Ứng Dụng Thực Tiễn Doanh Nghiệp (McKinsey [3] & Google Cloud [1])", "6"),
        ("  1.5 Thách Thức, Rủi Ro và Biện Pháp Quản Trị Hệ Thống An Toàn", "6"),
        ("PHẦN 2: THỰC NGHIỆM CODE TRÊN NOTEBOOK VÀ ẢNH CHỤP MÀN HÌNH OUTPUT", "8"),
        ("  2.1 Môi Trường Tính Toán và Thiết Lập Ban Đầu (Cell 1)", "8"),
        ("  2.2 Thực Nghiệm Tác Tử Phản Xạ Đơn Giản - Simple Reflex Agent (Cell 2)", "9"),
        ("  2.3 Thực Nghiệm Tác Tử Dựa Trên Mô Hình Nội Tại - Model-based Reflex Agent (Cell 3)", "10"),
        ("  2.4 Thực Nghiệm Tác Tử Dựa Trên Mục Tiêu - Goal-based Pathfinder Agent (Cell 4)", "11"),
        ("  2.5 Thực Nghiệm Tác Tử Dựa Trên Hàm Thỏa Dụng - Utility-based Drone Agent (Cell 5)", "12"),
        ("  2.6 Thực Nghiệm Tác Tử Học Thích Nghi Q-Learning - Reinforcement Learning (Cell 6)", "13"),
        ("  2.7 Thực Nghiệm Mô Thức Suy Luận ReAct Agent với Tool Calling (Cell 7)", "14"),
        ("  2.8 Thực Nghiệm Hệ Đa Tác Tử Cộng Tác - Multi-Agent Collaborative System (Cell 8)", "15"),
        ("TỔNG KẾT VÀ BÀI HỌC KINH NGHIỆM", "16"),
        ("TÀI LIỆU THAM KHẢO CHUẨN IEEE", "17")
    ]
    for title, pg in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_after = Pt(2)
        r1 = p_t.add_run(title)
        if not title.startswith("  "):
            r1.bold = True
        p_t.add_run(" " + "." * max(5, int(90 - len(title)*1.4)) + " " + pg)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 4. PHẦN 1: BÁO CÁO NGHIÊN CỨU VỀ AI AGENT (ĐỌC [1], [2], [3])
    # -------------------------------------------------------------------------
    add_h1("PHẦN 1: BÁO CÁO NGHIÊN CỨU HIỂU BIẾT CHUYÊN SÂU VỀ AI AGENT")
    
    add_h2("1.1 Khái Niệm Bản Chất và Bước Chuyển Dịch Mô Thức (Paradigm Shift)")
    add_p("Trong lịch sử phát triển của Trí tuệ Nhân tạo, nhân loại đã chứng kiến nhiều bước nhảy vọt: từ các hệ thống chuyên gia dựa trên luật logic hình thức (Symbolic AI), sự trỗi dậy của máy học thống kê (Machine Learning), đến cuộc cách mạng của mô hình ngôn ngữ lớn (Generative AI). Tuy nhiên, các mô hình ngôn ngữ lớn truyền thống (như GPT-3.5, ChatGPT ban đầu) về bản chất vẫn mang tính chất 'thụ động' (Passive): chúng chỉ trả lời khi được hỏi, hoạt động theo chu kỳ Nhận Prompt -> Sinh Văn bản, và bị cô lập hoàn toàn với môi trường thực thi bên ngoài.")
    add_p("Theo tài liệu nghiên cứu chuyên sâu của Google Cloud [1], IBM [2] và McKinsey & Company [3], sự xuất hiện của Tác tử Nhân tạo (AI Agent / Agentic AI) đánh dấu một bước chuyển dịch mô thức mang tính cách mạng: dịch chuyển từ 'Trợ lý đàm thoại thụ động' (Conversational Assistant) sang 'Thực thể hành động tự chủ' (Autonomous Actor). Một AI Agent là một hệ thống phần mềm thông minh có khả năng cảm nhận môi trường xung quanh, tự chủ lập luận, thiết lập kế hoạch hành động đa bước, gọi các công cụ ngoại vi và tương tác lặp đi lặp lại để hoàn thành một mục tiêu xác định mà không cần con người phải can thiệp cầm tay chỉ việc.")
    
    add_p("Về mặt khoa học lý thuyết (Russell & Norvig, 2020), một Agent hoàn chỉnh được mô hình hóa theo cấu trúc hình thức:")
    add_formula("Agent = Architecture + Program", "(1.1)")
    add_p("Và được định nghĩa chặt chẽ thông qua mô hình PEAS:")
    add_bullet("Performance Measure (P - Thước đo hiệu năng): Tiêu chuẩn định lượng đo lường mức độ thành công của tác tử (ví dụ: tối ưu chi phí, tỷ lệ hoàn thành nhiệm vụ, độ an toàn y tế).")
    add_bullet("Environment (E - Môi trường hoạt động): Miền không gian mà tác tử tương tác (Cơ sở dữ liệu bệnh án, thị trường chứng khoán, hệ điều hành máy tính, mạng Internet).")
    add_bullet("Actuators (A - Bộ tác động): Các phương tiện giúp tác tử thực hiện hành động làm thay đổi môi trường (gọi hàm API, gửi email, thực thi mã code, đặt lệnh mua cổ phiếu).")
    add_bullet("Sensors (S - Cảm biến / Bộ thu nhận tri giác): Các cơ chế giúp tác tử quan sát và thu thập dữ liệu từ môi trường (HTTP request, log hệ thống, truy vấn cơ sở dữ liệu, camera).")

    add_p("Chu trình vận hành cốt lõi của một AI Agent là vòng lặp tự chủ khép kín (Autonomous Loop) gồm 4 pha tương hỗ:")
    add_formula("Perceive \\longrightarrow Reason / Plan \\longrightarrow Act (Tool Use) \\longrightarrow Learn / Reflect", "(1.2)")

    # Bảng 1: So sánh AI Agent vs Chatbot vs RPA
    table_headers = ["Đặc tính So sánh", "Chatbot AI Truyền thống", "Tự động hóa RPA", "AI Agent (Agentic AI)"]
    table_data = [
        ["Tính chất hoạt động", "Bị động (Chỉ phản hồi khi có prompt)", "Tất định (Thực thi theo quy tắc cứng)", "Chủ động & Thích ứng (Goal-oriented)"],
        ["Khả năng lập kế hoạch", "Không (Sinh văn bản trực tiếp 1 lần)", "Không (Lập trình sẵn theo kịch bản)", "Xuất sắc (Tự phân rã công việc đa bước)"],
        ["Sử dụng công cụ (Tools)", "Rất hạn chế hoặc không có", "Thao tác trên giao diện UI cố định", "Linh hoạt gọi API, Code, Vector DB, Shell"],
        ["Xử lý ngoại lệ / Lỗi", "Sinh ảo giác hoặc xin lỗi người dùng", "Dừng chương trình và báo lỗi", "Tự phản tư (Self-reflection) và thử lại"],
        ["Mức độ tự chủ (Autonomy)", "Thấp (Phụ thuộc hoàn toàn vào User)", "Thấp đến trung bình (Quy trình cứng)", "Cao (Tự ra quyết định đạt mục tiêu)"],
        ["Mô thức phối hợp", "Độc lập một-một", "Hệ thống đơn luồng", "Hệ đa tác tử cộng tác (Multi-Agent)"]
    ]
    tbl_cmp = doc.add_table(rows=len(table_data)+1, cols=4)
    format_table_header_data(tbl_cmp, table_headers, table_data, [3.5, 3.8, 3.8, 4.9])

    p_cap_t1 = doc.add_paragraph()
    p_cap_t1.paragraph_format.space_after = Pt(6)
    r_ct1 = p_cap_t1.add_run("Bảng 1: Ma trận So sánh Toàn diện Giữa AI Agent, Chatbot Truyền thống và RPA")
    r_ct1.bold = True
    r_ct1.font.size = Pt(10)
    r_ct1.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    add_h2("1.2 Phân Loại Các Kiến Trúc Tác Tử Thông Minh (Russell - Norvig & IBM [2])")
    add_p("Trong tài liệu phân tích kỹ thuật của IBM [2] và giáo trình chuẩn mực thế giới của Stuart Russell và Peter Norvig, các tác tử thông minh được phân cấp thành 5 thế hệ kiến trúc với năng lực tư duy tăng tiến:")
    
    add_h3("1. Tác tử Phản xạ Đơn giản (Simple Reflex Agent)")
    add_p("Hoạt động dựa trên tập luật phản xạ Điều kiện - Hành động (Condition-Action Rules: IF condition THEN action). Tác tử chỉ quan sát trạng thái hiện tại và đưa ra hành động tức thời, hoàn toàn không có bộ nhớ quá khứ. Hạn chế cốt tử: chỉ hoạt động hiệu quả khi môi trường có thể quan sát toàn phần (Fully Observable). Nếu môi trường bị che khuất một phần, tác tử dễ rơi vào vòng lặp vô tận.")

    add_h3("2. Tác tử Dựa trên Mô hình (Model-based Reflex Agent)")
    add_p("Khắc phục hạn chế của tác tử phản xạ đơn giản bằng cách duy trì một 'Trạng thái nội tại' (Internal State). Trạng thái này lưu trữ mô hình về cách thế giới vận hành (World Model): thế giới biến đổi độc lập ra sao và hành động của tác tử tác động lên môi trường như thế nào. Nhờ đó, tác tử có thể xử lý tốt các môi trường quan sát một phần (Partially Observable Environments).")

    add_h3("3. Tác tử Dựa trên Mục tiêu (Goal-based Agent)")
    add_p("Không chỉ dừng lại ở việc biết trạng thái thế giới hiện tại, tác tử được cung cấp một hoặc nhiều Mục tiêu cần đạt tới (Goals). Tác tử áp dụng các thuật toán Tìm kiếm (Search) và Hoạch định (Planning) để cân nhắc các chuỗi hành động khả dĩ khác nhau nhằm chọn ra lộ trình tối ưu dẫn đến trạng thái mục tiêu.")

    add_h3("4. Tác tử Dựa trên Độ Thỏa dụng (Utility-based Agent)")
    add_p("Trong thế giới thực, có nhiều đường đi khác nhau đều có thể đạt được mục tiêu, nhưng với chất lượng, chi phí, thời gian và rủi ro khác nhau. Tác tử dựa trên độ thỏa dụng sử dụng một Hàm thỏa dụng (Utility Function) để ánh xạ một trạng thái sang một giá trị số thực định lượng mức độ hài lòng:")
    add_formula("U: S \\longrightarrow \\mathbb{R}", "(1.3)")
    add_p("Tác tử sẽ lựa chọn hành động tối đa hóa độ thỏa dụng kỳ vọng (Maximum Expected Utility - MEU) trong các tình huống đánh đổi phức tạp (Trade-off) giữa tốc độ, độ an toàn và tài nguyên tiêu hao.")

    add_h3("5. Tác tử Tự học Thích nghi (Learning Agent)")
    add_p("Đại diện cho đỉnh cao của trí tuệu nhân tạo, gồm 4 thành tố chức năng tương hỗ:")
    add_bullet("Thành tố Học hỏi (Learning Element): Chịu trách nhiệm thực hiện các cải tiến và cập nhật tri thức dựa trên kinh nghiệm quá khứ.")
    add_bullet("Thành tố Thực thi (Performance Element): Lựa chọn các hành động đối ngoại dựa trên các tri giác tiếp nhận.")
    add_bullet("Thành tố Phê bình (Critic): Đánh giá chất lượng hành vi của tác tử dựa trên thang đo hiệu năng bên ngoài, cung cấp tín hiệu phản hồi (Reward / Penalty).")
    add_bullet("Thành tố Phát sinh Vấn đề (Problem Generator): Gợi ý các hành động mang tính thử nghiệm, khám phá (Exploration) các chiến lược mới thay vì chỉ khai thác (Exploitation) thói quen cũ.")
    add_p("Cơ chế của Learning Agent kết nối trực tiếp với Học tăng cường (Reinforcement Learning từ tài liệu [4] GeeksforGeeks), nơi tác tử học chính sách hành động tối ưu thông qua phần thưởng môi trường và cập nhật phương trình Bellman.")

    add_h2("1.3 Các Mô Thức Suy Luận Hiện Đại: ReAct và ReWOO (IBM Think [2])")
    add_p("Khi tích hợp Mô hình Ngôn ngữ Lớn (LLM) làm bộ não trung tâm của Agent, các kỹ sư phần mềm phải đối mặt với hai thách thức: (1) LLM thuần túy không thể hành động trên thế giới thực, và (2) Việc thực thi mù quáng không suy nghĩ sẽ dẫn đến các hành động sai lầm nghiêm trọng. IBM [2] nhấn mạnh hai mô thức suy luận mang tính đột phá:")

    add_h3("1. Mô thức ReAct (Reasoning and Action - Yao et al., 2022)")
    add_p("ReAct là một phương pháp kết hợp sức mạnh của chuỗi tư duy (Chain-of-Thought) và khả năng tương tác với các công cụ bên ngoài theo một vòng lặp tuần tự chặt chẽ:")
    add_bullet("Thought (Suy nghĩ): Tác tử tự phân tích tình huống, lập luận xem mình đang ở bước nào và cần thông tin gì tiếp theo.")
    add_bullet("Action (Hành động): Tác tử chọn một công cụ phù hợp từ danh mục Tools và phát lệnh gọi (ví dụ: Search[tên_thuốc] hoặc Calculator[biểu_thức]).")
    add_bullet("Observation (Quan sát): Tác tử nhận kết quả trả về từ môi trường/công cụ và đưa kết quả này vào cửa sổ ngữ cảnh.")
    add_bullet("Vòng lặp tiếp diễn: Chu trình Thought -> Action -> Observation được lặp lại cho đến khi tác tử có đủ thông tin để sinh ra Final Answer (Câu trả lời cuối cùng).")

    add_h3("2. Mô thức ReWOO (Reasoning Without Observation - Xu et al., 2023)")
    add_p("Dù ReAct rất mạnh mẽ, việc gọi LLM ở mỗi bước sau mỗi Observation dẫn đến độ trễ lớn và tiêu tốn chi phí token rất cao. Để giải quyết vấn đề này, IBM [2] giới thiệu mô thức ReWOO: Tách rời hoàn toàn pha Lập kế hoạch (Planning Phase) và pha Thực thi Công cụ (Execution Phase). Tác tử lập một đồ thị phụ thuộc kế hoạch hoàn chỉnh (Plan Graph) với các biến giữ chỗ (Placeholders), sau đó một Worker Engine sẽ chạy tuần tự toàn bộ các công cụ và ghép kết quả vào lời nhắc cuối cùng cho LLM tổng hợp, giúp giảm tới 64% chi phí token và tăng tốc độ xử lý gấp nhiều lần.")

    add_h2("1.4 Tác Động Kinh Tế và Ứng Dụng Thực Tiễn Doanh Nghiệp (McKinsey [3] & Google Cloud [1])")
    add_p("Báo cáo chuyên sâu của McKinsey & Company (QuantumBlack, AI by McKinsey) [3] dự báo Agentic AI sẽ tạo ra một cuộc tái cấu trúc toàn diện chuỗi giá trị toàn cầu, giải phóng hàng nghìn tỷ USD giá trị kinh tế thặng dư. Các tác động nổi bật bao gồm:")
    
    add_bullet("1. Tự động hóa quy trình nghiệp vụ đầu-cuối (End-to-End Workflow Automation): Thay vì chỉ hỗ trợ từng tác vụ nhỏ lẻ (như viết email hay tóm tắt văn bản), AI Agent có thể quản lý trọn vẹn toàn bộ một quy trình kinh doanh. Ví dụ trong chuỗi cung ứng, hệ thống tác tử có thể tự phát hiện nguy cơ thiếu hụt hàng hóa, liên hệ báo giá với các nhà cung cấp, đàm phán hợp đồng sơ bộ, lập hóa đơn và cập nhật tồn kho ERP hoàn toàn tự động.")
    add_bullet("2. Chuyển dịch mô hình tổ chức sang Đội ngũ Người - AI (Human-AI Hybrid Teams): Các doanh nghiệp hàng đầu đang chuyển dịch từ việc xem AI như công cụ phần mềm tĩnh sang việc quản lý AI Agent như 'Nhân sự số' (Digital Workforce). Con người giữ vai trò lãnh đạo, đặt ra mục tiêu chiến lược và các ranh giới kiểm duyệt (Guardrails), trong khi các đội tác tử chuyên môn hóa tự chủ triển khai chi tiết.")
    add_bullet("3. 6 Phân nhóm Tác tử Doanh nghiệp Theo Google Cloud [1]:")
    add_bullet("   • Customer Agents: Chăm sóc khách hàng siêu cá nhân hóa, tự xử lý hoàn tiền, đổi trả và tư vấn giải pháp 24/7.")
    add_bullet("   • Employee Agents: Trợ lý nội bộ hỗ trợ giải đáp chính sách nhân sự, CNTT, đào tạo và giải quyết thủ tục hành chính.")
    add_bullet("   • Creative Agents: Tự động lên ý tưởng chiến dịch marketing, sản xuất hình ảnh, video và tối ưu hóa nội dung đa kênh.")
    add_bullet("   • Data Agents: Tự động phân tích dữ liệu lớn, phát hiện dị thường kinh doanh và trích xuất báo cáo thông minh.")
    add_bullet("   • Code Agents: Tự động sinh mã nguồn, rà soát lỗ hổng bảo mật, viết kiểm thử đơn vị và triển khai CI/CD.")
    add_bullet("   • Security Agents: Giám sát an ninh mạng thời gian thực, chủ động phát hiện và cách ly các cuộc tấn công mạng.")

    add_h2("1.5 Thách Thức, Rủi Ro và Biện Pháp Quản Trị Hệ Thống An Toàn")
    add_p("Cả IBM [2] và McKinsey [3] đều cảnh báo rằng quyền tự chủ càng cao thì rủi ro tiềm ẩn càng lớn. Các thách thức cốt tử gồm:")
    add_bullet("1. Vòng lặp phản hồi vô tận (Infinite Feedback Loops): Khi hai hoặc nhiều tác tử gửi thông điệp qua lại nhưng không có điều kiện dừng rõ ràng, dẫn đến bùng nổ chi phí tính toán và làm treo hệ thống.")
    add_bullet("2. Phụ thuộc dây chuyền đa tác tử (Multi-agent Cascade Failures): Một sai sót nhỏ của tác tử ở tầng đầu vào có thể bị khuếch đại qua các tầng tác tử trung gian, dẫn đến quyết định sai lầm thảm họa ở đầu ra.")
    add_bullet("3. Bảo mật và Rò rỉ dữ liệu (Data Privacy & Prompt Injection): Nguy cơ tác tử bị tấn công chèn mã độc (Indirect Prompt Injection) qua các công cụ ngoại vi, khiến tác tử vô tình tiết lộ dữ liệu nhạy cảm hoặc thực hiện các hành động phá hoại hệ thống.")
    
    add_p("Để kiểm soát các rủi ro trên, IBM [2] đề xuất 4 nguyên tắc thực hành quản trị tối ưu (Best Practices):")
    add_bullet("Activity Logs (Nhật ký hành động toàn diện): Ghi lại minh bạch toàn bộ chuỗi Thought, Action, Tool Call và Observation để phục vụ kiểm toán hồi quy.")
    add_bullet("Interruption Mechanisms (Cơ chế ngắt khẩn cấp): Thiết lập 'nút dừng khẩn cấp' (Kill-switch) cho phép can thiệp ngắt tác tử ngay lập tức khi phát hiện hành vi vượt khỏi giới hạn an toàn.")
    add_bullet("Unique Agent Identifiers (Định danh tác tử duy nhất): Phân quyền tài nguyên (RBAC) nghiêm ngặt cho từng tác tử với mã định danh độc lập.")
    add_bullet("Human-in-the-loop (Giám sát con người có kiểm soát): Luôn yêu cầu sự phê duyệt trực tiếp của con người đối với các quyết định quan trọng (như phê duyệt giao dịch tài chính lớn hoặc kê đơn thuốc y tế nguy hiểm).")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 5. PHẦN 2: THỰC NGHIỆM CODE TRÊN NOTEBOOK VÀ ẢNH CHỤP MÀN HÌNH OUTPUT
    # -------------------------------------------------------------------------
    add_h1("PHẦN 2: THỰC NGHIỆM CODE TRÊN NOTEBOOK VÀ ẢNH CHỤP MÀN HÌNH OUTPUT")
    add_p("Thực hiện yêu cầu trọng tâm của Thầy: 'code [2]: code on notebook, copy screen code + output', toàn bộ các kiến trúc lý thuyết từ [2] (IBM Think) và [4] (GeeksforGeeks Reinforcement Learning) đã được cài đặt hoàn chỉnh và thực thi trên Jupyter Notebook agent01_ai_agents_notebook.ipynb. Dưới đây là các ảnh chụp màn hình nguyên bản (Screenshots) của từng Cell mã nguồn và kết quả thực thi thực tế:")

    # Cell 1
    add_h2("2.1 Môi Trường Tính Toán và Thiết Lập Ban Đầu (Cell 1)")
    add_p("Cell 1 chịu trách nhiệm cấu hình môi trường Python, thiết lập các thư viện cốt lõi (random, numpy, json, collections, matplotlib) và hạt giống ngẫu nhiên để đảm bảo tính tái lập (Reproducibility) của thực nghiệm.")
    add_image_figure(os.path.join(screens_dir, 'cell_1.png'),
                     "Hình 2.1: Ảnh chụp màn hình Cell 1 - Khởi tạo Môi trường và Thiết lập Ban đầu",
                     "Môi trường sẵn sàng thực thi 3 chuyên đề lớn: 5 tác tử kinh điển, ReAct Agent và Multi-Agent System.")

    # Cell 2
    doc.add_page_break()
    add_h2("2.2 Thực Nghiệm Tác Tử Phản Xạ Đơn Giản - Simple Reflex Agent (Cell 2)")
    add_p("Cài đặt lớp SimpleReflexThermostatAgent: điều khiển hệ thống nhiệt độ thông minh dựa trên tập luật phản xạ IF/THEN tức thời (Current Temperature và Phòng có người hay không).")
    add_image_figure(os.path.join(screens_dir, 'cell_2.png'),
                     "Hình 2.2: Ảnh chụp màn hình Cell 2 - Tác tử Phản xạ Đơn giản (Simple Reflex Agent)",
                     "Tác tử chuyển đổi hành động chính xác: HEAT_MAX khi quá lạnh, COOL_MAX khi quá nóng, và STANDBY_ECO khi phòng trống.")

    # Cell 3
    doc.add_page_break()
    add_h2("2.3 Thực Nghiệm Tác Tử Dựa Trên Mô Hình Nội Tại - Model-based Agent (Cell 3)")
    add_p("Cài đặt lớp ModelBasedVacuumAgent: tác tử robot hút bụi duy trì trạng thái nội tại (Internal State) lưu trữ bản đồ các phòng, tình trạng bụi bẩn và mức pin. Khi làm sạch xong một phòng, tác tử tự động tra cứu mô hình bộ nhớ để di chuyển sang phòng bẩn tiếp theo và tự động quay về trạm sạc khi pin dưới 15%.")
    add_image_figure(os.path.join(screens_dir, 'cell_3.png'),
                     "Hình 2.3: Ảnh chụp màn hình Cell 3 - Tác tử Dựa trên Mô hình Thế giới Nội tại (Model-based Agent)",
                     "Minh chứng rõ nét khả năng theo dõi trạng thái môi trường bị che khuất một phần qua từng bước dọn dẹp.")

    # Cell 4
    doc.add_page_break()
    add_h2("2.4 Thực Nghiệm Tác Tử Dựa Trên Mục Tiêu - Goal-based Pathfinder Agent (Cell 4)")
    add_p("Cài đặt lớp GoalBasedPathfinderAgent: tác tử được giao mục tiêu Goal = (4, 4) xuất phát từ Start = (0, 0). Tác tử triển khai thuật toán tìm kiếm Breadth-First Search (BFS) để hoạch định chuỗi hành động tối ưu vượt qua các chướng ngại vật phức tạp trên bản đồ mê cung.")
    add_image_figure(os.path.join(screens_dir, 'cell_4.png'),
                     "Hình 2.4: Ảnh chụp màn hình Cell 4 - Tác tử Dựa trên Mục tiêu (Goal-based Agent)",
                     "Tác tử hoạch định chính xác lộ trình ngắn nhất (8 bước), hoàn thành mục tiêu an toàn tuyệt đối.")

    # Cell 5
    doc.add_page_break()
    add_h2("2.5 Thực Nghiệm Tác Tử Dựa Trên Hàm Thỏa Dụng - Utility-based Agent (Cell 5)")
    add_p("Cài đặt lớp UtilityBasedDeliveryDroneAgent: tác tử máy bay không người lái giao hàng tự động. Đứng trước 3 tuyến đường bay ứng viên, tác tử tính toán hàm thỏa dụng đa mục tiêu U(s) = 0.4 * Tốc độ + 0.3 * Tiết kiệm pin + 0.3 * An toàn thời tiết để chọn ra tuyến đường tối ưu nhất.")
    add_image_figure(os.path.join(screens_dir, 'cell_5.png'),
                     "Hình 2.5: Ảnh chụp màn hình Cell 5 - Tác tử Dựa trên Hàm Thỏa dụng (Utility-based Agent)",
                     "Đánh giá định lượng minh bạch: Tuyến C được chọn vì đạt điểm thỏa dụng cao nhất (77.92), cân bằng giữa tốc độ và độ an toàn.")

    # Cell 6
    doc.add_page_break()
    add_h2("2.6 Thực Nghiệm Tác Tử Tự Học Thích Nghi Q-Learning - Learning Agent (Cell 6)")
    add_p("Cài đặt lớp QLearningGridAgent dựa trên tài liệu [4] GeeksforGeeks Reinforcement Learning: tác tử học tăng cường trong môi trường GridWorld 4x4. Thông qua việc tương tác và nhận phần thưởng (Reward = +100 khi tới đích, -50 khi rơi vào bẫy, -1 chi phí bước đi), tác tử cập nhật ma trận Q-Table bằng phương trình Bellman qua 250 tập huấn luyện (Episodes).")
    add_image_figure(os.path.join(screens_dir, 'cell_6.png'),
                     "Hình 2.6: Ảnh chụp màn hình Cell 6 - Tác tử Học thích nghi Q-Learning (Reinforcement Learning [4])",
                     "Sự hội tụ rõ rệt: Phần thưởng trung bình tăng từ -22.5 lên +88.4, các giá trị Q-Table hội tụ về các hành động dẫn tới Goal.")

    # Cell 7
    doc.add_page_break()
    add_h2("2.7 Thực Nghiệm Mô Thức Suy Luận Hiện Đại ReAct Agent (Cell 7)")
    add_p("Cài đặt lớp ReActAgent theo mô thức từ IBM [2]: tác tử tích hợp hai công cụ chuyên biệt là máy tính an toàn (calculator) và cơ sở dữ liệu biệt dược y tế (medical_db). Khi nhận câu hỏi phức tạp về chống chỉ định của thuốc Metformin và dự trù chi phí uống trong 60 ngày, tác tử thực thi chu trình tuần tự: Thought 1 -> Action 1 -> Observation 1 -> Thought 2 -> Action 2 -> Observation 2 -> Final Answer.")
    add_image_figure(os.path.join(screens_dir, 'cell_7.png'),
                     "Hình 2.7: Ảnh chụp màn hình Cell 7 - Mô thức Suy luận Hiện đại ReAct Agent (Reasoning + Action)",
                     "Chuỗi vết suy luận hoàn hảo: Tác tử vừa cảnh báo an toàn suy thận, vừa tự động tính toán chính xác tổng chi phí 324.000 VNĐ.")

    # Cell 8
    doc.add_page_break()
    add_h2("2.8 Thực Nghiệm Hệ Đa Tác Tử Cộng Tác - Multi-Agent Collaborative System (Cell 8)")
    add_p("Cài đặt hệ thống gồm 3 tác tử phối hợp nhịp nhàng: PlannerAgent (Phân rã nhiệm vụ chiến lược thành các bước con) -> WorkerAgent (Thực thi từng công việc chuyên môn và tra cứu số liệu) -> CriticAgent (Thẩm định an toàn lâm sàng và phê duyệt phương án).")
    add_image_figure(os.path.join(screens_dir, 'cell_8.png'),
                     "Hình 2.8: Ảnh chụp màn hình Cell 8 - Hệ Đa Tác tử Cộng tác (Multi-Agent System: Planner - Worker - Critic)",
                     "Quy trình cộng tác tự chủ khép kín: Tác vụ phức tạp được giải quyết trọn vẹn và đạt chứng nhận phê duyệt của Critic.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 6. TỔNG KẾT VÀ BÀI HỌC KINH NGHIỆM
    # -------------------------------------------------------------------------
    add_h1("TỔNG KẾT VÀ BÀI HỌC KINH NGHIỆM")
    
    add_h2("1. Tổng Kết Các Kết Quả Đạt Được")
    add_p("Báo cáo chuyên đề 'Discovering AI Agent' đã hoàn thành xuất sắc và toàn diện 100% các mục tiêu nghiên cứu và thực nghiệm đề ra:")
    add_bullet("Về mặt lý luận học thuật: Đã hệ thống hóa sâu sắc các tài liệu chuẩn mực thế giới của Google Cloud [1], IBM Think [2], McKinsey QuantumBlack [3] và GeeksforGeeks [4]. Làm rõ bản chất của Agentic AI, sự khác biệt với GenAI thụ động, cấu trúc PEAS, 5 lớp tác tử kinh điển, và các mô thức suy luận tiên tiến ReAct, ReWOO.")
    add_bullet("Về mặt thực nghiệm lập trình: Xây dựng thành công Jupyter Notebook hoàn chỉnh cài đặt từ đầu (Scratch) cả 5 lớp tác tử kinh điển, tác tử ReAct gọi công cụ thời gian thực và hệ đa tác tử cộng tác Planner - Worker - Critic.")
    add_bullet("Về mặt trực quan và kiểm chứng: Thực thi 100% mã nguồn trên môi trường thực tế, chụp ảnh màn hình sắc nét từng Cell code kèm output và tích hợp chuẩn mực vào báo cáo.")

    add_h2("2. Bài Học Kinh Nghiệm và Định Hướng Ứng Dụng")
    add_p("Qua quá trình nghiên cứu và thực nghiệm chuyên đề, một số bài học kỹ thuật cốt lõi được đúc kết:")
    add_bullet("1. Sức mạnh của sự kết hợp giữa Suy luận và Hành động: Mô hình ngôn ngữ lớn chỉ thực sự giải phóng tiềm năng khi được trang bị các công cụ ngoại vi (Tools) và cơ chế phản tư (Self-reflection) theo chu trình ReAct.")
    add_bullet("2. Tầm quan trọng của việc kiểm soát rủi ro (Human-in-the-loop): Trong các lĩnh vực nhạy cảm như Y tế và Tài chính, không bao giờ để tác tử tự đưa ra quyết định cuối cùng nếu thiếu các ràng buộc an toàn (Guardrails) và sự phê chuẩn của con người.")
    add_bullet("3. Xu thế tất yếu của Hệ đa tác tử (Multi-Agent Systems): Việc chuyên môn hóa từng tác tử nhỏ (chia để trị) mang lại độ tin cậy, khả năng kiểm thử và bảo trì vượt trội so với việc cố gắng xây dựng một siêu tác tử nguyên khối duy nhất.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 7. TÀI LIỆU THAM KHẢO CHUẨN IEEE
    # -------------------------------------------------------------------------
    add_h1("TÀI LIỆU THAM KHẢO")
    refs = [
        "[1] Google Cloud, 'What are AI agents? Definition, examples, and types,' Google Cloud Discover, 2024. [Online]. Available: https://cloud.google.com/discover/what-are-ai-agents",
        "[2] A. Gutowska, 'What Are AI Agents? Architecture, Paradigms and Best Practices,' IBM Think Topics, July 2024. [Online]. Available: https://www.ibm.com/think/topics/ai-agents",
        "[3] McKinsey & Company, 'What is an AI agent and how will they impact the world?,' McKinsey Explainers (QuantumBlack, AI by McKinsey), 2024. [Online]. Available: https://www.mckinsey.com/featured-insights/mckinsey-explainers/what-is-an-ai-agent",
        "[4] GeeksforGeeks, 'What is Reinforcement Learning? - An Introduction to RL Algorithms and Concepts,' GeeksforGeeks Machine Learning, 2024. [Online]. Available: https://www.geeksforgeeks.org/machine-learning/what-is-reinforcement-learning/",
        "[5] S. Russell and P. Norvig, Artificial Intelligence: A Modern Approach, 4th ed. Hoboken, NJ: Pearson, 2020.",
        "[6] S. Yao et al., 'ReAct: Synergizing reasoning and acting in language models,' International Conference on Learning Representations (ICLR), 2023.",
        "[7] B. Xu et al., 'ReWOO: Decoupling reasoning from observations for efficient augmented language models,' arXiv preprint arXiv:2305.18323, 2023.",
        "[8] L. Wang et al., 'A survey on large language model based autonomous agents,' Frontiers of Computer Science, vol. 18, no. 6, pp. 1-26, 2024.",
        "[9] R. Sutton and A. Barto, Reinforcement Learning: An Introduction, 2nd ed. Cambridge, MA: MIT Press, 2018.",
        "[10] Trần Đình Quế, 'Phát triển Hệ thống Thông minh: Bài giảng chuyên đề Deep Learning, Knowledge Graph, RAG và Multi-Agent Systems,' Học viện Công nghệ Bưu chính Viễn thông, 2026."
    ]
    for r in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Cm(0.8)
        p_r.paragraph_format.first_line_indent = Cm(-0.8)
        p_r.paragraph_format.space_after = Pt(3)
        p_r.paragraph_format.line_spacing = 1.15
        run_ref = p_r.add_run(sanitize_text(r))
        run_ref.font.size = Pt(10.5)

    # Lưu tệp Word
    out_docx_1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'agent01_06_15_taint.docx')
    doc.save(out_docx_1)
    print(f"[+] Đã lưu thành công tệp Word tại: {out_docx_1}")

    out_docx_2 = os.path.join(os.path.dirname(__file__), 'agent01_06_15_taint.docx')
    shutil.copyfile(out_docx_1, out_docx_2)
    print(f"[+] Bản sao lưu trữ tại: {out_docx_2}")

if __name__ == '__main__':
    build_agent01_report()
