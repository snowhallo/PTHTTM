# -*- coding: utf-8 -*-
"""
Trình tạo tài liệu Tiểu Luận Môn Học Final hoàn chỉnh (Chương 1 - Chương 7):
Tập tin xuất: tieuluan_final_06_15_taint.docx
Sinh viên thực hiện: Nguyễn Tuấn Tài (MSV: B23DCCN731)
Lớp học phần: INT14149_06 / Nhóm 06, Nhóm tiểu luận: Nhóm 15
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế (PTIT)
"""
import os
import sys
import shutil
import re

sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from chapters_1_to_4_content import (
    add_intro,
    add_chapter_1,
    add_chapter_2,
    add_chapter_3,
    add_chapter_4
)
from chapter5_content import add_chapter_5
from chapter6_content import add_chapter_6
from chapter7_content import (
    add_chapter_7,
    add_final_conclusion_ch7,
    get_final_references_ch7
)

def sanitize_text(text):
    if not isinstance(text, str):
        return str(text)
    # Loại bỏ các ký tự điều khiển không tương thích XML
    return ''.join(ch for ch in text if ch in '\n\r\t' or (32 <= ord(ch) <= 0x10FFFF))

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is not None:
        tcPr.remove(shd)
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = tcPr.find(qn('w:tcMar'))
    if tcMar is not None:
        tcPr.remove(tcMar)
    tcMar_elm = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar_elm)

def set_cell_bottom_border(cell, sz="8", color="000000"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is not None:
        tcPr.remove(tcBorders)
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

def set_table_borders_grid(table):
    """Thiết lập đường viền bảng đầy đủ (Full Grid Lines theo đúng Hình 2)"""
    tblPr = table._tbl.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_tieuluan_final():
    print("=" * 70)
    print("KHỞI TẠO TẠO TIỂU LUẬN FINAL MÔN HỌC: tieuluan_final_06_15_taint.docx")
    print("=" * 70)

    doc = docx.Document()

    # -------------------------------------------------------------------------
    # 1. ĐỊNH DẠNG TRANG & STYLE CHUẨN VĂN BẢN QUY ĐỊNH
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
    normal_font.size = Pt(13)
    normal_font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(4)

    # Thư mục chứa hình ảnh thực nghiệm
    plots_dir = os.path.join(os.path.dirname(__file__), 'plots')
    figures_dir_ch7 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'agent02_experiments', 'report_figures')
    if not os.path.exists(figures_dir_ch7):
        figures_dir_ch7 = plots_dir

    # -------------------------------------------------------------------------
    # 2. BỘ HÀM TIỆN ÍCH CHUẨN VĂN PHONG VÀ ĐỊNH DẠNG
    # -------------------------------------------------------------------------
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13.5)
        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        return p

    def add_p(text, indent=True):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if indent:
            p.paragraph_format.first_line_indent = Cm(1.27)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        run = p.add_run(sanitize_text(text))
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Cm(1.27)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.25
        run = p.add_run(sanitize_text(text))
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        return p

    def add_formula(eq_text, eq_num=""):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(5)
        run = p.add_run(sanitize_text(eq_text))
        run.font.name = 'Cambria Math'
        run.font.size = Pt(12)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if eq_num:
            eq_clean = str(eq_num).strip().strip('()')
            r_num = p.add_run(f"    ({eq_clean})")
            r_num.font.name = 'Times New Roman'
            r_num.font.size = Pt(12)
            r_num.font.italic = False
            r_num.bold = False
            r_num.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        return p

    def add_image_figure(img_path, fig_title, comment=None, width_inch=5.8):
        if not os.path.exists(img_path):
            alt_path = os.path.join(plots_dir, os.path.basename(img_path))
            if os.path.exists(alt_path):
                img_path = alt_path
            else:
                print(f"[!] CẢNH BÁO: Không tìm thấy ảnh: {img_path}")
                return

        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inch))

        # Chuẩn hóa tag hình ảnh: Dưới mỗi ảnh là chữ in nghiêng, căn giữa, bắt đầu bằng chữ "Hình", số La Mã theo chương:
        # Ví dụ: Hình I.1. <nội dung>, Hình V.1. <nội dung>, Hình VII.1. <nội dung>
        title_clean = fig_title.strip()
        roman_map = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'}
        clean_t = re.sub(r'^(?:Hình|Figure)\s*', '', title_clean, flags=re.IGNORECASE).strip()

        m_roman = re.match(r'^([I|V|X]+)\.(\d+)[\.:]?\s*(.*)$', clean_t)
        if m_roman:
            r_num = m_roman.group(1)
            f_idx = m_roman.group(2)
            rest = m_roman.group(3).strip()
            formatted_caption = f"Hình {r_num}.{f_idx}. {rest}"
        else:
            m_arabic = re.match(r'^([1-7])\.(\d+)[\.:]?\s*(.*)$', clean_t)
            if m_arabic:
                ch_idx = int(m_arabic.group(1))
                f_idx = m_arabic.group(2)
                rest = m_arabic.group(3).strip()
                formatted_caption = f"Hình {roman_map[ch_idx]}.{f_idx}. {rest}"
            else:
                formatted_caption = f"Hình {clean_t}"

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(4)
        run_cap = p_cap.add_run(sanitize_text(formatted_caption))
        run_cap.font.name = 'Times New Roman'
        run_cap.font.size = Pt(12)
        run_cap.font.italic = True
        run_cap.bold = False
        run_cap.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    def add_code_listing(code_str, caption=None, lang="Python"):
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.paragraph_format.space_before = Pt(6)
            p_cap.paragraph_format.space_after = Pt(2)
            p_cap.paragraph_format.keep_with_next = True
            r = p_cap.add_run(f"Đoạn mã ({lang}): {sanitize_text(caption)}")
            r.bold = True
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.cell(0, 0)
        c.width = Cm(16.0)
        set_cell_background(c, "F8F9FA")
        set_cell_margins(c, top=80, bottom=80, left=120, right=120)

        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(sanitize_text(code_str))
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        tblPr = tbl._tbl.tblPr
        tblBorders = tblPr.find(qn('w:tblBorders'))
        if tblBorders is not None:
            tblPr.remove(tblBorders)
        box_borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="000000"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="none"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(box_borders)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(4)

    def format_table_header_data(tbl, headers, data, col_widths=None):
        """Định dạng bảng đầy đủ đường viền (Full Grid Lines theo đúng Hình 2)"""
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Hàng tiêu đề (Header row 0)
        for j, h in enumerate(headers):
            cell = tbl.cell(0, j)
            set_cell_background(cell, "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(sanitize_text(h))
            r.bold = True
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        # Các hàng dữ liệu
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                cell = tbl.cell(i + 1, j)
                set_cell_background(cell, "FFFFFF")
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing = 1.15
                if j == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(sanitize_text(str(val)))
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        set_table_borders_grid(tbl)

        if col_widths:
            for row in tbl.rows:
                for j, w in enumerate(col_widths):
                    if j < len(row.cells):
                        row.cells[j].width = Cm(w)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(4)

    # Từ điển helper truyền cho tất cả các mô-đun chương
    helpers = {
        'add_h1': add_h1,
        'add_h2': add_h2,
        'add_h3': add_h3,
        'add_p': add_p,
        'add_bullet': add_bullet,
        'add_formula': add_formula,
        'add_image_figure': add_image_figure,
        'add_code_listing': add_code_listing,
        'format_table_header_data': format_table_header_data,
        'sanitize_text': sanitize_text
    }

    helpers_ch7 = dict(helpers)
    helpers_ch7['figures_dir'] = figures_dir_ch7

    # -------------------------------------------------------------------------
    # 3. TIẾN TRÌNH XÂY DỰNG TỪ PHẦN MỞ ĐẦU ĐẾN HẾT CHƯƠNG 7
    # -------------------------------------------------------------------------
    print("[*] Đang ghi: PHẦN MỞ ĐẦU...")
    add_intro(doc, helpers)
    doc.add_page_break()

    print("[*] Đang ghi: CHƯƠNG 1: Lịch sử phát triển Trí tuệ Nhân tạo (AI)...")
    add_chapter_1(doc, plots_dir, helpers)
    doc.add_page_break()

    print("[*] Đang ghi: CHƯƠNG 2: Các kỹ thuật Machine Learning cơ bản...")
    add_chapter_2(doc, plots_dir, helpers)
    doc.add_page_break()

    print("[*] Đang ghi: CHƯƠNG 3: Mạng nơ-ron Tích chập (CNN)...")
    add_chapter_3(doc, plots_dir, helpers)
    doc.add_page_break()

    print("[*] Đang ghi: CHƯƠNG 4: Mạng nơ-ron Hồi quy (RNN)...")
    add_chapter_4(doc, plots_dir, helpers)
    doc.add_page_break()

    print("[*] Đang ghi: CHƯƠNG 5: Knowledge Graph và RAG (GraphRAG)...")
    add_chapter_5(doc, plots_dir, helpers)
    doc.add_page_break()

    print("[*] Đang ghi: CHƯƠNG 6: Học sâu trên Đồ thị (Deep Graph & GNN)...")
    add_chapter_6(doc, plots_dir, helpers)
    doc.add_page_break()

    print("[*] Đang ghi: CHƯƠNG 7: Hệ đa Tác tử Thông minh (Multi-Agent Systems)...")
    add_chapter_7(doc, helpers_ch7)
    doc.add_page_break()

    print("[*] Đang ghi: KẾT LUẬN TOÀN DIỆN VÀ HƯỚNG PHÁT TRIỂN...")
    add_final_conclusion_ch7(doc, helpers_ch7)
    doc.add_page_break()

    print("[*] Đang ghi: TÀI LIỆU THAM KHẢO chuẩn IEEE...")
    add_h1("TÀI LIỆU THAM KHẢO")
    references = get_final_references_ch7()
    for ref_item in references:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Cm(1.27)
        p_r.paragraph_format.first_line_indent = Cm(-1.27)
        p_r.paragraph_format.space_after = Pt(3)
        p_r.paragraph_format.line_spacing = 1.15
        p_r.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p_r.add_run(sanitize_text(ref_item))
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # -------------------------------------------------------------------------
    # 4. HẬU KIỂM VÀ ĐẢM BẢO 100% FONT CHỮ ĐEN, CĂN LỀ TRÁI & TIMES NEW ROMAN
    # -------------------------------------------------------------------------
    print("[*] Đang thực hiện rà soát hậu kiểm (Post-processing)...")
    black_color = RGBColor(0x00, 0x00, 0x00)
    for p in doc.paragraphs:
        if p.alignment != WD_ALIGN_PARAGRAPH.CENTER:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.color.rgb = black_color
            if r.font.name not in ['Consolas', 'Cambria Math']:
                r.font.name = 'Times New Roman'

    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.color.rgb = black_color
                        if r.font.name not in ['Consolas', 'Cambria Math']:
                            r.font.name = 'Times New Roman'

    # -------------------------------------------------------------------------
    # 5. LƯU TÀI LIỆU CUỐI CÙNG
    # -------------------------------------------------------------------------
    out_dir_experiments = os.path.dirname(__file__)
    out_path_experiments = os.path.join(out_dir_experiments, 'tieuluan_final_06_15_taint.docx')
    doc.save(out_path_experiments)
    print(f"[+] Đã lưu thành công tại thư mục experiments: {out_path_experiments}")

    out_path_root = os.path.join(os.path.dirname(out_dir_experiments), 'tieuluan_final_06_15_taint.docx')
    try:
        shutil.copyfile(out_path_experiments, out_path_root)
        print(f"[+] Đã sao chép thành công ra thư mục gốc dự án: {out_path_root}")
    except PermissionError:
        print(f"[!] Chú ý: Tệp '{out_path_root}' đang được mở trong Word.")
        backup_root = os.path.join(os.path.dirname(out_dir_experiments), 'tieuluan_final_06_15_taint_updated.docx')
        shutil.copyfile(out_path_experiments, backup_root)
        print(f"[+] Đã lưu bản sao cập nhật tại thư mục gốc: {backup_root}")
        print(f"[+] Bản cập nhật chuẩn luôn sẵn sàng tại: {out_path_experiments}")

    print("=" * 70)
    print("HOÀN TẤT TẠO TIỂU LUẬN FINAL MÔN HỌC THÀNH CÔNG!")
    print("=" * 70)

if __name__ == '__main__':
    build_tieuluan_final()

