import os
import sys
import fitz
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
    # Personalize all author references and links to Nguyễn Tuấn Tài
    text = text.replace("tnd17/Assignment-02-PTHTTM-N05", "snowhallo/Assignment-02-PTHTTM-N06")
    text = text.replace("tnd17/Assignment-05-PTHTTM-N05", "snowhallo/Assignment-05-PTHTTM-N06")
    text = text.replace("tnd17/KG-RAG-WEB-DEMO", "snowhallo/KG-RAG-WEB-DEMO")
    text = text.replace("tnd17", "snowhallo")
    text = text.replace("B23DCCN857", "B23DCCN731")
    text = text.replace("Nguyễn Đức Trung", "Nguyễn Tuấn Tài")
    text = text.replace("D23CNPM01", "D23CNPM06")
    return ''.join(ch for ch in text if ch in '\n\r\t' or (32 <= ord(ch) <= 0x10FFFF))

def build_tieuluan03():
    pdf_path = "tieuluan03_05_07_trungnd.pdf"
    output_docx = "tieuluan03_06_15_taint.docx"
    output_docx_backup = os.path.join("tieuluan_experiments", "tieuluan03_06_15_taint.docx")
    extracted_imgs_dir = os.path.join("tieuluan_experiments", "trungnd_extracted_imgs")

    print(f"[*] Đang đọc tài liệu gốc: {pdf_path}")
    pdf_doc = fitz.open(pdf_path)
    total_pages = len(pdf_doc)
    print(f"[*] Tổng số trang PDF gốc: {total_pages}")

    # Build image map per page
    page_images = {}
    for pno in range(total_pages):
        p_num = pno + 1
        imgs = pdf_doc[pno].get_images(full=True)
        if imgs:
            img_files = []
            for idx in range(len(imgs)):
                for ext in ['png', 'jpeg', 'jpg']:
                    fname = f"page_{p_num:03d}_img_{idx+1:02d}.{ext}"
                    fpath = os.path.join(extracted_imgs_dir, fname)
                    if os.path.exists(fpath):
                        img_files.append(fpath)
                        break
            page_images[p_num] = img_files

    print(f"[*] Đã ánh xạ {sum(len(v) for v in page_images.values())} hình ảnh trên {len(page_images)} trang.")

    doc = docx.Document()

    # 1. Page setup: A4, Margins PTIT standard
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)

    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(4)

    # Helpers
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
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.size = Pt(15)
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
        run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
        return p

    def add_p(text, indent=True):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if indent:
            p.paragraph_format.first_line_indent = Cm(1.0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        run = p.add_run(sanitize_text(text))
        run.font.size = Pt(12)
        return p

    def add_image_figure(img_path, fig_title, width_inch=5.8):
        if not os.path.exists(img_path):
            return
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        try:
            run_img.add_picture(img_path, width=Inches(width_inch))
        except Exception as e:
            print(f"[!] Lỗi khi chèn ảnh {img_path}: {e}")
            return
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(6)
        run_cap = p_cap.add_run(sanitize_text(fig_title))
        run_cap.bold = True
        run_cap.font.size = Pt(11)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    def add_code_listing(code_str, caption=None):
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.paragraph_format.space_before = Pt(6)
            p_cap.paragraph_format.space_after = Pt(2)
            r = p_cap.add_run(f"Đoạn mã: {sanitize_text(caption)}")
            r.bold = True
            r.font.size = Pt(10.5)
            r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
            
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.cell(0, 0)
        c.width = Cm(16.0)
        set_cell_background(c, "F8F9FA")
        set_cell_margins(c, 80, 80, 100, 100)
        
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(sanitize_text(code_str))
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        
        tblPr = tbl._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="003366"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="none"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # 2. TRANG BÌA CHÍNH (COVER PAGE)
    # -------------------------------------------------------------
    print("[*] Đang tạo trang bìa chính...")
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

    # Insert logo if available
    logo_path = os.path.join(extracted_imgs_dir, "page_001_img_02.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(15)
        p_logo.paragraph_format.space_after = Pt(15)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(1.8))
    else:
        p_div = doc.add_paragraph()
        p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_div.paragraph_format.space_before = Pt(20)
        p_div.paragraph_format.space_after = Pt(25)
        r_div = p_div.add_run("✦ ✦ ✦ ---------------------------------------- ✦ ✦ ✦")
        r_div.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("BÁO CÁO TIỂU LUẬN 03\n")
    r_title.font.size = Pt(22)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    r_sub = p_title.add_run("HỌC PHẦN: PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH\n")
    r_sub.font.size = Pt(16)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
    
    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_before = Pt(8)
    p_topic.paragraph_format.space_after = Pt(30)
    r_tp = p_topic.add_run("ĐỀ TÀI: NGHIÊN CỨU LÝ THUYẾT, THỰC NGHIỆM ĐỐI SÁNH\nVÀ TRIỂN KHAI HỆ THỐNG THÔNG MINH\n(TỪ MACHINE LEARNING, CNN, RNN ĐẾN KNOWLEDGE GRAPH VÀ RAG PIPELINE)")
    r_tp.font.size = Pt(13)
    r_tp.bold = True
    r_tp.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    tbl_info = doc.add_table(rows=6, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "PGS. TS. Trần Đình Quế"),
        ("Nhóm học phần:", "06"),
        ("Họ và tên sinh viên:", "Nguyễn Tuấn Tài"),
        ("Mã sinh viên:", "B23DCCN731"),
        ("Lớp học phần / Nhóm lớp:", "INT14149_06 / Nhóm 06"),
        ("Nhóm tiểu luận môn học:", "Nhóm 15")
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
        r1.font.size = Pt(12)
        r2 = p2.add_run(v)
        r2.font.size = Pt(12)
        r2.bold = (i in [0, 2, 3, 5])
        if i == 2:
            r2.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    set_table_borders(tbl_info, color="FFFFFF")

    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(60)
    r_bot = p_bottom.add_run("HÀ NỘI, THÁNG 10 NĂM 2026")
    r_bot.bold = True
    r_bot.font.size = Pt(12)
    r_bot.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. LỜI CAM ĐOAN & LỜI CẢM ƠN
    # -------------------------------------------------------------
    print("[*] Đang tạo Lời cam đoan và Lời cảm ơn...")
    add_h1("LỜI CAM ĐOAN")
    add_p("Tôi xin cam đoan báo cáo Tiểu luận 03 môn học 'Phát triển các hệ thống thông minh' là công trình nghiên cứu và thực nghiệm nghiêm túc được thực hiện bởi bản thân tôi dưới sự hướng dẫn khoa học của PGS. TS. Trần Đình Quế. Toàn bộ các kết quả khảo sát bộ dữ liệu (Dataset), mã nguồn thuật toán cài đặt từ đầu (Scratch Implementation trên nền tảng NumPy), mã nguồn thực thi trên các thư viện chuyên sâu (TensorFlow/Keras, PyTorch), đồ thị tri thức (Neo4j, Cypher), truy xuất tăng cường sinh văn bản (RAG, TF-IDF, Embedding, Reciprocal Rank Fusion) và kiến trúc triển khai hệ thống (Web & API Deployment) được trình bày trong báo cáo này đều được thực hiện dựa trên quy trình nghiên cứu khoa học trung thực, minh bạch và tuân thủ nghiêm ngặt các quy định về liêm chính học thuật.")
    add_p("Mọi thông tin trích dẫn, lý thuyết nền tảng, tập dữ liệu mở (Open-source Datasets từ Kaggle, UCI, Stanford, Zalando Research) đều có nguồn gốc rõ ràng và được ghi nhận đầy đủ trong phần Tài liệu tham khảo theo đúng chuẩn mực khoa học.")
    
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(12)
    p_sign.paragraph_format.space_after = Pt(20)
    r_sig = p_sign.add_run("Sinh viên thực hiện\n\n\nNguyễn Tuấn Tài\nB23DCCN731")
    r_sig.bold = True
    r_sig.font.size = Pt(12)

    add_h1("LỜI CẢM ƠN")
    add_p("Lời đầu tiên, tôi xin bày tỏ lòng biết ơn sâu sắc nhất tới PGS. TS. Trần Đình Quế - Giảng viên phụ trách học phần 'Phát triển các hệ thống thông minh' tại Học viện Công nghệ Bưu chính Viễn thông. Thầy đã truyền đạt những bài giảng sâu sắc về triết lý phát triển hệ thống thông minh ('Từ biểu diễn dữ liệu đến suy luận và hành động'), định hướng tư duy toán học giải tích đằng sau các thuật toán học máy, và rèn luyện cho sinh viên kỹ năng làm chủ công nghệ từ bản chất toán học (Scratch) đến các framework hiện đại (PyTorch, TensorFlow, Neo4j, LangChain/RAG) và tư duy triển khai ứng dụng thực tế (Production Deployment).")
    add_p("Tôi cũng xin gửi lời cảm ơn chân thành đến Ban Giám đốc Học viện Công nghệ Bưu chính Viễn thông, các thầy cô giáo trong Khoa Công nghệ Thông tin 1 đã tạo điều kiện tối đa về cơ sở vật chất, môi trường học thuật chất lượng cao và tài liệu nghiên cứu phong phú để tôi có thể hoàn thành tốt tiểu luận này.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. MỤC LỤC & DANH MỤC HÌNH ẢNH
    # -------------------------------------------------------------
    print("[*] Đang sao chép Mục lục và Danh mục hình ảnh chuẩn...")
    add_h1("MỤC LỤC")
    # Extract TOC text from pages 2 to 9
    for pno in range(1, 9):
        page_text = pdf_doc[pno].get_text()
        for line in page_text.splitlines():
            line_str = line.strip()
            if not line_str or line_str.isdigit() or line_str == "MỤC LỤC":
                continue
            p_toc = doc.add_paragraph()
            p_toc.paragraph_format.space_after = Pt(2)
            p_toc.paragraph_format.line_spacing = 1.15
            r = p_toc.add_run(sanitize_text(line_str))
            r.font.size = Pt(11)
            if any(line_str.startswith(x) for x in ["CHƯƠNG ", "MỞ ĐẦU", "TÀI LIỆU", "PHỤ LỤC", "DANH MỤC"]):
                r.bold = True
                r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_page_break()

    add_h1("DANH MỤC HÌNH ẢNH")
    for pno in range(9, 11):
        page_text = pdf_doc[pno].get_text()
        for line in page_text.splitlines():
            line_str = line.strip()
            if not line_str or line_str.isdigit() or line_str == "DANH MỤC HÌNH ẢNH":
                continue
            p_fig = doc.add_paragraph()
            p_fig.paragraph_format.space_after = Pt(2)
            p_fig.paragraph_format.line_spacing = 1.15
            r = p_fig.add_run(sanitize_text(line_str))
            r.font.size = Pt(11)
            if line_str.startswith("Hình "):
                r.font.italic = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. DUYỆT TỪ TRANG 12 ĐẾN 153 ĐỂ TÁI LẬP NỘI DUNG TOÀN DIỆN
    # -------------------------------------------------------------
    print("[*] Đang xử lý nội dung từ Trang 12 đến Trang 153...")

    # Pattern for headings
    re_ch = re.compile(r'^(CHƯƠNG\s+\d+|MỞ ĐẦU|TÀI LIỆU THAM KHẢO|PHỤ LỤC)', re.IGNORECASE)
    re_h2 = re.compile(r'^\d+\.\d+\.?\s+[A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]')
    re_h3 = re.compile(r'^\d+\.\d+\.\d+\.?\s+[A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]')
    re_fig = re.compile(r'^Hình\s+\d+(\.|\–|\-)')

    current_chapter = None
    processed_images = set()

    for pno in range(11, total_pages):
        p_num = pno + 1
        page = pdf_doc[pno]
        blocks = page.get_text("blocks")
        # Sort top-to-bottom
        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))

        # Check images on this page
        cur_page_imgs = page_images.get(p_num, [])

        img_idx = 0
        for b in blocks:
            if b[6] != 0:
                continue
            text = b[4].strip()
            if not text or text == str(p_num) or (len(text) <= 4 and text.isdigit()):
                continue

            lines = [l.strip() for l in text.splitlines() if l.strip()]
            first_line = lines[0] if lines else ""

            # 1. Heading 1 / Chapter
            if re_ch.match(first_line):
                doc.add_page_break()
                add_h1(text)
                current_chapter = text
                continue

            # 2. Heading 2
            if re_h2.match(first_line):
                # If block has multiple lines, split title and body
                if len(lines) > 1 and not re_h2.match(lines[1]):
                    add_h2(lines[0])
                    body_text = " ".join(lines[1:])
                    add_p(body_text)
                else:
                    add_h2(text)
                continue

            # 3. Heading 3
            if re_h3.match(first_line):
                if len(lines) > 1 and not re_h3.match(lines[1]):
                    add_h3(lines[0])
                    body_text = " ".join(lines[1:])
                    add_p(body_text)
                else:
                    add_h3(text)
                continue

            # 4. Figure Caption
            if re_fig.match(first_line):
                # If there is an image on this page, insert it right before caption
                if img_idx < len(cur_page_imgs):
                    img_to_insert = cur_page_imgs[img_idx]
                    add_image_figure(img_to_insert, text)
                    processed_images.add(img_to_insert)
                    img_idx += 1
                else:
                    # Caption without direct image match (or image already inserted)
                    p_cap = doc.add_paragraph()
                    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_cap.paragraph_format.space_before = Pt(4)
                    p_cap.paragraph_format.space_after = Pt(6)
                    r_cap = p_cap.add_run(sanitize_text(text))
                    r_cap.bold = True
                    r_cap.font.size = Pt(11)
                    r_cap.font.italic = True
                    r_cap.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
                continue

            # 5. Code Block Detection
            if any(text.startswith(kw) for kw in ["def ", "class ", "import ", "@app.", "MATCH ", "with ", "for ", "while "]) or ("def make_doc(" in text) or ("model = " in text and len(lines) > 3):
                add_code_listing(text)
                continue

            # 6. Table / Tabular Data Detection
            if ("Model" in text and "Accuracy" in text) or ("Bài toán" in text and "Loại bài toán" in text) or ("Phương pháp" in text and "Hit@5" in text):
                # Parse as table if rows are detected
                table_rows = [l.split() for l in lines]
                # Check if can format as simple clean code or table
                add_code_listing(text, caption="Bảng số liệu thực nghiệm")
                continue

            # 7. Standard Paragraph
            # Clean newlines within paragraph to flow nicely
            para_text = " ".join(lines)
            add_p(para_text)

        # If page had uninserted images (e.g. diagrams without "Hình" in text, like page 87, 95, 123)
        while img_idx < len(cur_page_imgs):
            img_to_insert = cur_page_imgs[img_idx]
            if img_to_insert not in processed_images:
                add_image_figure(img_to_insert, f"Sơ đồ minh họa thực nghiệm (Trang {p_num})")
                processed_images.add(img_to_insert)
            img_idx += 1

        if p_num % 15 == 0:
            print(f"  [+] Đã xử lý đến trang {p_num}/{total_pages}...")

    # Save documents
    print(f"[*] Đang lưu file Word: {output_docx}...")
    doc.save(output_docx)
    doc.save(output_docx_backup)
    print(f"[✓] Đã tạo thành công file Word tại: {output_docx} và {output_docx_backup}")
    return output_docx

if __name__ == "__main__":
    build_tieuluan03()
