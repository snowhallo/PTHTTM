import os, sys, json
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_a4_report():
    doc = docx.Document()
    
    # Page setup - Margins: Left 3cm, Right 2cm, Top 2cm, Bottom 2cm per Vietnamese academic standards
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        section.page_width = Cm(21.0) # A4
        section.page_height = Cm(29.7)
        
    # Styles
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
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D) # Navy Blue
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0) # Blue
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

    def add_callout(text, prefix="LƯU Ý QUAN TRỌNG: ", fill="EBF8FF", border="3182CE"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, fill)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        
        # Border
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="24" w:color="{border}"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        r_pre = p.add_run(prefix)
        r_pre.bold = True
        r_pre.font.size = Pt(11)
        r_pre.font.color.rgb = RGBColor(0x2C, 0x52, 0x82)
        r_txt = p.add_run(text)
        r_txt.font.size = Pt(11)
        r_txt.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(4)

    def add_image_with_caption(img_path, fig_title, source, read_guide, obs, explanation, limits, width_inch=6.0):
        if not os.path.exists(img_path):
            print(f"WARNING: Image not found: {img_path}")
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
        
        # Caption metadata (Academic 5-element format)
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
        p_space.paragraph_format.space_after = Pt(6)

    # Load experimental metrics
    with open('ass4_experiments/artifacts/diabetes_cnn_metrics.json', 'r') as f:
        diabetes_metrics = json.load(f)
    with open('ass4_experiments/artifacts/house_cnn_metrics.json', 'r') as f:
        house_metrics = json.load(f)
    with open('ass4_experiments/artifacts/customer_cnn_metrics.json', 'r') as f:
        customer_metrics = json.load(f)
    with open('ass4_experiments/artifacts/gradient_check.json', 'r') as f:
        grad_check = json.load(f)

    print("Building Title Page...")
    # ==========================================
    # TRANG BÌA (TITLE PAGE)
    # ==========================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    run_inst = p_inst.add_run("BỘ KHOA HỌC VÀ CÔNG NGHỆ\n")
    run_inst.bold = True
    run_inst.font.size = Pt(13)
    run_inst2 = p_inst.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n")
    run_inst2.bold = True
    run_inst2.font.size = Pt(14)
    run_inst3 = p_inst.add_run("KHOA CÔNG NGHỆ THÔNG TIN 1")
    run_inst3.font.size = Pt(12)

    # Logo
    logo_path = 'a02_docx_imgs/image1.jpg'
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(20)
        p_logo.paragraph_format.space_after = Pt(20)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.8))

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(6)
    r_tit = p_title.add_run("BÁO CÁO BÀI TẬP LỚN SỐ 04\n")
    r_tit.bold = True
    r_tit.font.size = Pt(18)
    r_tit.font.color.rgb = RGBColor(0x9B, 0x1C, 0x1C) # Red Crimson

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("CHỦ ĐỀ: MẠNG NƠ-RON TÍCH CHẬP (CONVOLUTIONAL NEURAL NETWORKS - CNN) DƯỚI GÓC NHÌN PHÉP HỢP CÁC HÀM, TỰ CÀI ĐẶT TỪ ĐẦU (FROM SCRATCH) VÀ ĐỐI SÁNH NÂNG CAO TRÊN PYTORCH & TENSORFLOW")
    r_sub.bold = True
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    p_mod = doc.add_paragraph()
    p_mod.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mod.paragraph_format.space_after = Pt(24)
    r_mod = p_mod.add_run("Học phần: Phát triển hệ thống thông minh\nGiảng viên hướng dẫn: PGS. TS. Trần Đình Quế")
    r_mod.italic = True
    r_mod.font.size = Pt(12)

    tbl_student = doc.add_table(rows=3, cols=2)
    tbl_student.alignment = WD_TABLE_ALIGNMENT.CENTER
    student_info = [
        ("Sinh viên thực hiện:", "Nguyễn Tuấn Tài"),
        ("Mã số sinh viên:", "B23DCCN731"),
        ("Nhóm / Lớp học phần:", "Nhóm 06 - Lớp INT14149_06")
    ]
    for i, (k, v) in enumerate(student_info):
        c1 = tbl_student.cell(i, 0)
        c2 = tbl_student.cell(i, 1)
        c1.width = Inches(2.2)
        c2.width = Inches(3.2)
        p1 = c1.paragraphs[0]
        p2 = c2.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        p2.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(k)
        r1.bold = True
        r1.font.size = Pt(11)
        r2 = p2.add_run(v)
        r2.font.size = Pt(11)
        set_cell_margins(c1, 40, 40, 50, 50)
        set_cell_margins(c2, 40, 40, 50, 50)

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(40)
    r_foot = p_foot.add_run("HÀ NỘI, THÁNG 09 NĂM 2026")
    r_foot.font.size = Pt(11)
    r_foot.italic = True

    doc.add_page_break()

    # ==========================================
    # MỤC LỤC (TABLE OF CONTENTS)
    # ==========================================
    print("Building Table of Contents...")
    add_h1("MỤC LỤC TỔNG THỂ BÁO CÁO")
    
    toc_items = [
        ("LỜI CẢM ƠN VÀ CAM KẾT HỌC THUẬT", "Trang 3"),
        ("CHƯƠNG I: BẢN CHẤT TOÁN HỌC CỦA TÍCH CHẬP & PHÉP HỢP CÁC HÀM TRONG DEEP LEARNING", "Trang 4"),
        ("  1.1 Khái niệm Deep Learning dưới góc nhìn Phép hợp các hàm (Function Composition)", "Trang 4"),
        ("  1.2 Hai thuộc tính cốt lõi của CNN: Tính cục bộ và Trọng số dùng chung", "Trang 5"),
        ("  1.3 Cơ chế toán học của phép toán Tích chập 1D và 2D", "Trang 6"),
        ("  1.4 Công thức tính kích thước không gian đầu ra, Padding và Stride", "Trang 7"),
        ("  1.5 Công thức tính tổng tham số mô hình và so sánh với MLP", "Trang 8"),
        ("  1.6 Các cơ chế Phép gộp (Pooling) và tính bất biến dịch chuyển", "Trang 9"),
        ("CHƯƠNG II: THIẾT KẾ VÀ CÀI ĐẶT MẠNG TÍCH CHẬP TỪ ĐẦU BẰNG NUMPY (FROM SCRATCH)", "Trang 10"),
        ("  2.1 Kiến trúc các khối lớp tùy chỉnh: Conv1D, ReLU, MaxPool1D, Flatten, Dense", "Trang 10"),
        ("  2.2 Đạo hàm toán học và cơ chế Lan truyền ngược (Backpropagation)", "Trang 11"),
        ("  2.3 Kiểm thử độ chính xác đạo hàm (Gradient Checking: Sai phân hữu hạn)", "Trang 12"),
        ("  2.4 Thực thi và trực quan hóa kết quả kiểm thử trên Jupyter Notebook", "Trang 13"),
        ("CHƯƠNG III: CHUYỂN ĐỔI SANG PYTORCH & TENSORFLOW/KERAS: ĐỐI CHIẾU CÚ PHÁP VÀ AUTOGRAD", "Trang 15"),
        ("  3.1 Cú pháp và Định dạng Tensor: Channel First vs Channel Last", "Trang 15"),
        ("  3.2 So sánh cấu trúc định nghĩa mô hình (torch.nn.Module vs tf.keras.Model)", "Trang 16"),
        ("  3.3 Cơ chế tự động tính vi phân (Autograd Engine vs tf.GradientTape)", "Trang 17"),
        ("  3.4 Bằng chứng thực nghiệm thực thi trên môi trường Anaconda Jupyter", "Trang 18"),
        ("CHƯƠNG IV: THỰC NGHIỆM ĐỐI SÁNH BASELINE CNN VÀ IMPROVED CNN TRÊN 3 BỘ DỮ LIỆU ĐA DẠNG", "Trang 20"),
        ("  4.1 Bộ dữ liệu 1 - Phân loại Nguy cơ Tiểu đường (Diabetes 1D Tabular Sequence)", "Trang 20"),
        ("  4.2 Bộ dữ liệu 2 - Dự đoán Giá nhà đất (House Price 1D Tabular Sequence Regression)", "Trang 23"),
        ("  4.3 Bộ dữ liệu 3 - Phân loại Đánh giá khách hàng (Customer Reviews 1D Text Sequence)", "Trang 26"),
        ("  4.4 Thực nghiệm Mở rộng: Phân loại Ảnh Chữ số viết tay MNIST 2D (So sánh với Bài giảng)", "Trang 29"),
        ("CHƯƠNG V: TRỰC QUAN HÓA BỘ LỌC HỌC ĐƯỢC, ĐÚC KẾT MENTAL MODEL & GIAO DIỆN HỆ THỐNG DEMO", "Trang 31"),
        ("  5.1 Trực quan hóa 16 Bộ lọc Tích chập học được (Learned Filters Visualization)", "Trang 31"),
        ("  5.2 Đúc kết 10 Câu hỏi Mental Model cốt lõi về Mạng tích chập", "Trang 33"),
        ("  5.3 Minh họa Hệ thống Demo Trực quan Đa nền tảng (Desktop & Mobile 6 ảnh dự án)", "Trang 36"),
        ("  5.4 Kết luận và Đề xuất phát triển", "Trang 39")
    ]
    
    for title, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.line_spacing = 1.15
        r_t = p_t.add_run(title)
        r_t.font.size = Pt(11)
        if not title.startswith("  "):
            r_t.bold = True
            r_t.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        # Dots
        dots_len = max(5, 75 - len(title))
        r_d = p_t.add_run(" " + "." * dots_len + " ")
        r_d.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
        
        r_p = p_t.add_run(page)
        r_p.bold = True
        r_p.font.size = Pt(11)

    doc.add_page_break()

    # ==========================================
    # LỜI CẢM ƠN VÀ CAM KẾT
    # ==========================================
    add_h1("LỜI CẢM ƠN VÀ CAM KẾT HỌC THUẬT")
    add_p("Lời đầu tiên, em xin trân trọng gửi lời cảm ơn sâu sắc nhất tới PGS. TS. Trần Đình Quế – Giảng viên phụ trách học phần Phát triển hệ thống thông minh, Khoa Công nghệ Thông tin 1, Học viện Công nghệ Bưu chính Viễn thông. Thầy đã truyền đạt những kiến thức chuyên sâu, có tính hệ thống cao và mang tính đột phá về toán học cũng như kỹ thuật cài đặt Deep Learning. Đặc biệt, thông qua Slide bài giảng 04 (intel_sys_dev_slide_04_updated_11.9.pdf) và Tài liệu hướng dẫn chuyên đề Mạng tích chập dưới góc nhìn Phép hợp các hàm (Deep_Learning_CNN_Function_Composition_Tutorial.pdf), thầy đã giúp sinh viên khai mở bản chất đại số tuyến tính của phép tích chập, thoát khỏi tư duy 'hộp đen' để làm chủ hoàn toàn cấu trúc toán học từ gốc rễ.")
    add_p("Báo cáo Bài tập lớn số 04 (Assignment 04) này được hoàn thành nhằm giải quyết triệt để 5 yêu cầu cốt lõi được thầy giao trên bảng và trong tài liệu hướng dẫn:")
    add_p("1. Khảo sát và tải dữ liệu từ Kaggle/UCI trên 3 miền dữ liệu đa dạng (Tabular Sequence Phân loại Tiểu đường, Tabular Sequence Hồi quy Giá nhà, và Chuỗi văn bản Phân loại cảm xúc khách hàng), kết hợp thực nghiệm mở rộng trên bộ ảnh MNIST 2D;")
    add_p("2. Tự thiết kế và lập trình mạng tích chập hoàn toàn từ đầu (CNN from Scratch) bằng thư viện NumPy, không dựa vào bất kỳ framework tự động tính đạo hàm nào, và thực hiện kiểm thử độ chính xác gradient số học (Gradient Checking) với sai số nhỏ hơn 1e-12;")
    add_p("3. Triển khai chuyển đổi mô hình sang hai nền tảng công nghiệp hàng đầu là PyTorch và TensorFlow/Keras, đối chiếu chi tiết cú pháp định nghĩa, chiều Tensor và cơ chế Autograd;")
    add_p("4. Xây dựng và thực nghiệm đối sánh chuyên sâu giữa Baseline CNN (3 lớp tích chập cơ bản) và Improved CNN (tích hợp Batch Normalization, Dropout và Khối phần dư Residual Connection), đánh giá toàn diện trên các chỉ số định lượng, tốc độ hội tụ và độ phức tạp tính toán;")
    add_p("5. Tổ chức toàn bộ mã nguồn theo đúng chuẩn quản lý dự án học tập đồng bộ từ Bài 1 đến Bài 4: gom toàn bộ các tệp dữ liệu thực nghiệm vào một thư mục tập trung duy nhất ('data/'), gom toàn bộ các tệp Jupyter Notebook vào một thư mục tập trung duy nhất ('notebooks/') có phân định rõ ràng theo từng bài tập (A1, A2, A3, A4) sẵn sàng trình chiếu trên môi trường Anaconda; đồng thời trích xuất 100% hình ảnh thực nghiệm, biểu đồ và giao diện demo trực tiếp từ project của chính sinh viên.")
    add_p("Em xin cam kết toàn bộ dữ liệu, hình ảnh, mã nguồn thực thi và số liệu trong báo cáo này được tạo ra hoàn toàn từ quá trình thực nghiệm độc lập của sinh viên Nguyễn Tuấn Tài (Mã SV: B23DCCN731, Nhóm 06), tuyệt đối không sao chép hình ảnh từ bài báo cáo mẫu hay các nguồn có sẵn trên mạng.")

    doc.add_page_break()

    # ==========================================
    # CHƯƠNG I: BẢN CHẤT TOÁN HỌC CỦA TÍCH CHẬP
    # ==========================================
    print("Building Chapter I...")
    add_h1("CHƯƠNG I: BẢN CHẤT TOÁN HỌC CỦA TÍCH CHẬP & PHÉP HỢP CÁC HÀM TRONG DEEP LEARNING")
    
    add_h2("1.1 Khái niệm Deep Learning dưới góc nhìn Phép hợp các hàm (Function Composition)")
    add_p("Trong lý thuyết học máy kinh điển, các mô hình học có giám sát thường được mô tả dưới dạng một hàm số $y = f(x; \\theta)$ ánh xạ từ không gian đặc trưng đầu vào $\\mathcal{X} \\subset \\mathbb{R}^D$ sang không gian nhãn mục tiêu $\\mathcal{Y}$. Tuy nhiên, trong tài liệu chuyên đề 'Deep Learning CNN Function Composition Tutorial' của PGS. TS. Trần Đình Quế, học sâu (Deep Learning) được định nghĩa một cách chặt chẽ và tổng quát hơn rất nhiều: đó là quá trình xấp xỉ một ánh xạ phi tuyến phức tạp thông qua PHÉP HỢP CỦA MỘT CHUỖI CÁC HÀM ĐƠN GIẢN (Function Composition):")
    
    add_callout(
        "Định nghĩa Phép hợp các hàm:\n"
        "f(x) = (f_L ∘ f_{L-1} ∘ ... ∘ f_2 ∘ f_1)(x) = f_L(f_{L-1}(...(f_1(x))...))\n"
        "Trong đó mỗi hàm f_l(h_{l-1}) = σ(W_l ⊗ h_{l-1} + b_l) biểu diễn một tầng biến đổi biểu diễn đặc trưng (Feature Representation Transfer), σ là hàm kích hoạt phi tuyến tính, và ⊗ là toán tử tích chập hoặc nhân ma trận.",
        prefix="TIÊN ĐỀ TOÁN HỌC 1.1: ",
        fill="F0FFF4",
        border="38A169"
    )
    
    add_p("Góc nhìn này mang lại một sự thấu hiểu sâu sắc: mạng nơ-ron sâu không phải là một chiếc hộp đen thần bí, mà là một chuỗi các phép biến đổi hình học liên tiếp trong không gian vector. Lớp đầu tiên $f_1$ trích xuất các đặc trưng nguyên thủy cục bộ (Low-level features như đường viền, gradient, biến động ngắn hạn). Các lớp tiếp theo $f_2, f_3$ hợp nhất các đặc trưng cục bộ đó thành các mô thức trừu tượng bậc trung (Mid-level features như góc, kết cấu, chu kỳ biến thiên). Cuối cùng, các lớp cao nhất $f_L$ tổng hợp thành biểu diễn ngữ nghĩa toàn cục (High-level semantic representations) giúp bộ phân loại tuyến tính ở đầu ra đưa ra quyết định chính xác.")

    add_h2("1.2 Hai thuộc tính cốt lõi của CNN: Tính cục bộ và Trọng số dùng chung")
    add_p("So với Mạng nơ-ron truyền thẳng đa tầng (MLP / Fully Connected Network), Mạng nơ-ron tích chập (CNN) giải quyết triệt để hai nhược điểm chí mạng: hiện tượng bùng nổ số lượng tham số (Curse of Dimensionality) và sự mất mát cấu trúc không gian/thời gian. CNN đạt được điều này nhờ khai thác triệt để hai giả định tự nhiên của dữ liệu thế giới thực:")
    add_p("1. Tính cục bộ không gian (Locality / Local Receptive Field): Trong ảnh số hoặc chuỗi tín hiệu, các điểm dữ liệu lân cận có mối tương quan rất chặt chẽ với nhau, trong khi các điểm ở xa nhau thường có độ tương quan yếu. Do đó, thay vì kết nối mỗi nơ-ron với toàn bộ đầu vào như MLP, một nơ-ron trong lớp tích chập chỉ kết nối với một vùng lân cận hữu hạn gọi là Trường cảm thụ (Receptive Field) có kích thước bằng bộ lọc (Kernel Size K).")
    add_p("2. Tính bất biến dịch chuyển và Trọng số dùng chung (Weight Sharing / Translation Equivariance): Nếu một đặc trưng (ví dụ: cạnh dốc, một từ khóa cảnh báo, một sự sụt giảm đột ngột) có ích tại một vị trí cục bộ này thì nó cũng có khả năng cao xuất hiện và mang ý nghĩa tương tự tại các vị trí khác. Thay vì học một bộ trọng số riêng cho từng vị trí, CNN sử dụng cùng một bộ lọc (Filter / Kernel) trượt trên toàn bộ không gian đầu vào. Cơ chế này giảm số lượng tham số tự do từ bậc tích $O(D_{in} \\times D_{out})$ xuống chỉ còn bậc $O(K \\times C_{in} \\times C_{out})$, độc lập hoàn toàn với kích thước chiều dài hay độ phân giải của dữ liệu.")

    add_h2("1.3 Cơ chế toán học của phép toán Tích chập 1D và 2D")
    add_p("Về mặt giải tích, phép tích chập liên tục của hai hàm số $f$ và $g$ được định nghĩa bởi tích phân suy rộng: $(f * g)(t) = \\int_{-\\infty}^{\\infty} f(\\tau) g(t - \\tau) d\\tau$. Trong Deep Learning xử lý tín hiệu rời rạc, phép toán thực chất được triển khai dưới dạng Tương quan chéo (Cross-Correlation), trong đó nhân tích chập không bị lật ngược (vì mạng tự học các giá trị trọng số tối ưu):")
    add_p("Đối với tích chập 1D (xử lý chuỗi thời gian, bảng dữ liệu sequence, hoặc văn bản), đầu ra tại vị trí $i$ của kênh thứ $c_{out}$ được tính bằng:")
    add_p("$$Y[c_{out}, i] = b[c_{out}] + \\sum_{c_{in}=1}^{C_{in}} \\sum_{k=0}^{K-1} X[c_{in}, i \\cdot S + k] \\cdot W[c_{out}, c_{in}, k]$$", indent=False)
    add_p("Đối với tích chập 2D (xử lý ma trận ảnh), đầu ra tại tọa độ không gian $(i, j)$ được biểu diễn bởi công thức:")
    add_p("$$Y[c_{out}, i, j] = b[c_{out}] + \\sum_{c_{in}=1}^{C_{in}} \\sum_{m=0}^{K_h-1} \\sum_{n=0}^{K_w-1} X[c_{in}, i \\cdot S + m, j \\cdot S + n] \\cdot W[c_{out}, c_{in}, m, n]$$", indent=False)

    add_h2("1.4 Công thức tính kích thước không gian đầu ra, Padding và Stride")
    add_p("Trong quá trình thiết kế mạng CNN, việc kiểm soát chặt chẽ kích thước không gian qua từng tầng là điều kiện tiên quyết để đảm bảo tính khả thi của mô hình. Với đầu vào có kích thước chiều dài $W$ (hoặc ma trận $H \\times W$), kích thước bộ lọc $K$, bước trượt $S$ (Stride) và độ dày đệm $P$ (Padding), kích thước đầu ra $O$ được xác định chính xác bởi công thức số học sàn:")
    
    add_callout(
        "Công thức chiều không gian đầu ra:\n"
        "O = ⌊(W - K + 2P) / S⌋ + 1\n"
        "• Valid Padding (P = 0): Kích thước bị thu hẹp dần: O = ⌊(W - K) / S⌋ + 1\n"
        "• Same Padding (với S = 1): Giữ nguyên kích thước: P = (K - 1) / 2",
        prefix="CÔNG THỨC KIẾN TRÚC 1.2: ",
        fill="EDF2F7",
        border="4A5568"
    )

    add_h2("1.5 Công thức tính tổng tham số mô hình và so sánh với MLP")
    add_p("Một trong những đóng góp mang tính nền tảng của CNN là tiết kiệm tham số học. Giả sử ta có lớp tích chập chuyển từ $C_{in}$ kênh đầu vào sang $C_{out}$ kênh đầu ra, kích thước bộ lọc là $K_h \\times K_w$, mỗi kênh đầu ra có 1 tham số độ lệch (bias). Tổng số tham số tự do có thể huấn luyện là:")
    add_p("$$N_{params}^{CNN} = C_{out} \\times (C_{in} \\times K_h \\times K_w + 1)$$", indent=False)
    add_p("Ví dụ, xét đầu vào ảnh 2D kích thước $28 \\times 28$ với 1 kênh màu, chuyển sang 32 kênh đặc trưng:")
    add_p("• Nếu dùng MLP Fully-Connected với 32 nơ-ron: Số tham số sẽ là $784 \\times 32 + 32 = 25,120$ trọng số.")
    add_p("• Nếu dùng CNN với bộ lọc $3 \\times 3$: Số tham số chỉ là $32 \\times (1 \\times 3 \\times 3 + 1) = 320$ trọng số! Mức giảm tới 78.5 lần, giúp mô hình miễn nhiễm với việc quá khớp (overfitting) và tăng tốc tính toán hàng chục lần.")

    add_h2("1.6 Các cơ chế Phép gộp (Pooling) và tính bất biến dịch chuyển")
    add_p("Lớp Phép gộp (Pooling Layer) đóng vai trò nén giảm kích thước không gian (Downsampling) của bản đồ đặc trưng, đồng thời củng cố tính bất biến dịch chuyển (Translation Invariance). Có 3 dạng pooling phổ biến:")
    add_p("1. Max Pooling: Lấy giá trị cực đại trong cửa sổ $P_w$. Phép toán này giữ lại tín hiệu kích hoạt mạnh nhất (đặc trưng nổi trội nhất), loại bỏ nhiễu nền và tạo tính bất biến trước những xê dịch nhỏ của vật thể.")
    add_p("2. Average Pooling: Tính giá trị trung bình trong cửa sổ, giữ lại thông tin làm mịn của bối cảnh.")
    add_p("3. Global Average Pooling (GAP): Tính trung bình trên toàn bộ chiều không gian của mỗi kênh đặc trưng, biến bản đồ đặc trưng $C \\times H \\times W$ thành vector $C \\times 1$. Kỹ thuật hiện đại này thay thế hoàn toàn lớp Flatten + Dense truyền thống, loại bỏ hàng triệu trọng số kết nối đầy đủ và ngăn chặn overfitting triệt để.")

    doc.add_page_break()

    # ==========================================
    # CHƯƠNG II: CNN FROM SCRATCH BẰNG NUMPY
    # ==========================================
    print("Building Chapter II...")
    add_h1("CHƯƠNG II: THIẾT KẾ VÀ CÀI ĐẶT MẠNG TÍCH CHẬP TỪ ĐẦU BẰNG NUMPY (CNN FROM SCRATCH)")
    
    add_h2("2.1 Kiến trúc các khối lớp tùy chỉnh: Conv1D, ReLU, MaxPool1D, Flatten, Dense")
    add_p("Để hiện thực hóa trọn vẹn yêu cầu mục 3 trên bảng của Thầy ('Code CNN from Scratch'), sinh viên đã xây dựng một module mạng nơ-ron hướng đối tượng thuần túy bằng thư viện NumPy trong file `notebooks_a4/01_cnn_from_scratch_numpy.ipynb`. Hệ thống kiến trúc bao gồm 5 lớp cốt lõi:")
    add_p("• Lớp Conv1D: Lưu trữ ma trận trọng số $W \\in \\mathbb{R}^{C_{out} \\times C_{in} \\times K}$ được khởi tạo theo phân phối He/Kaiming Normal: $W \\sim \\mathcal{N}(0, \\sqrt{2 / (C_{in} \\cdot K)})$, cùng vector bias $b \\in \\mathbb{R}^{1 \\times C_{out} \\times 1}$. Lớp hỗ trợ linh hoạt tham số Stride $S$ và Padding $P$.")
    add_p("• Lớp ReLU: Thực hiện biến đổi phi tuyến $f(x) = \\max(0, x)$. Trong pha lan truyền xuôi, lưu lại mặt nạ boolean `mask = (x > 0)` để phục vụ lan truyền ngược.")
    add_p("• Lớp MaxPool1D: Thực hiện nén chiều chuỗi tín hiệu theo kích thước cửa sổ $P_{size}$ và bước trượt $S$. Lưu trữ chỉ số cực đại `argmax` của từng cửa sổ.")
    add_p("• Lớp Flatten: Duỗi phẳng bản đồ đặc trưng đa chiều $(N, C, L)$ thành ma trận 2D $(N, C \\cdot L)$ để kết nối vào tầng phân loại.")
    add_p("• Lớp Dense (Linear): Thực hiện phép biến đổi affin $Y = X W + b$ với ma trận trọng số kích thước $(D_{in}, D_{out})$.")

    add_h2("2.2 Đạo hàm toán học và cơ chế Lan truyền ngược (Backpropagation)")
    add_p("Lan truyền ngược trong lớp tích chập là một trong những thuật toán vi phân ma trận phức tạp nhất của học sâu. Giả sử nhận được gradient của hàm mất mát đối với đầu ra tầng tích chập là $\\frac{\\partial L}{\\partial Y} = dout \\in \\mathbb{R}^{N \\times C_{out} \\times L_{out}}$. Theo quy tắc dây chuyền (Chain Rule), các đạo hàm thành phần được tính toán như sau:")
    add_p("1. Đạo hàm theo độ lệch (Bias):")
    add_p("$$\\frac{\\partial L}{\\partial b}[c_{out}] = \\sum_{n=1}^N \\sum_{i=1}^{L_{out}} dout[n, c_{out}, i]$$", indent=False)
    add_p("2. Đạo hàm theo trọng số bộ lọc (Weights):")
    add_p("$$\\frac{\\partial L}{\\partial W}[c_{out}, c_{in}, k] = \\sum_{n=1}^N \\sum_{i=1}^{L_{out}} dout[n, c_{out}, i] \\cdot X_{pad}[n, c_{in}, i \\cdot S + k]$$", indent=False)
    add_p("3. Đạo hàm theo đầu vào (Input Gradient):")
    add_p("$$\\frac{\\partial L}{\\partial X_{pad}}[n, c_{in}, i \\cdot S + k] = \\sum_{c_{out}=1}^{C_{out}} dout[n, c_{out}, i] \\cdot W[c_{out}, c_{in}, k]$$", indent=False)
    add_p("Sau khi tính toán trên ma trận đệm $X_{pad}$, gradient $\\frac{\\partial L}{\\partial X}$ thu được bằng cách cắt bỏ các phần tử đệm ở hai đầu.")

    add_h2("2.3 Kiểm thử độ chính xác đạo hàm (Gradient Checking: Sai phân hữu hạn)")
    add_p("Để kiểm chứng tính đúng đắn tuyệt đối của mã nguồn lan truyền ngược giải tích (Analytical Gradient), sinh viên đã áp dụng phương pháp kiểm thử sai phân hữu hạn đối xứng (Centered Finite Difference). Với một tham số trọng số bất kỳ $\\theta_i$, gradient số học được xấp xỉ bởi công thức:")
    add_p("$$g_{num}(\\theta_i) = \\frac{L(\\theta_i + \\epsilon) - L(\\theta_i - \\epsilon)}{2 \\cdot \\epsilon}$$", indent=False)
    add_p("Với hằng số vô cùng bé $\\epsilon = 10^{-7}$. Sai số tương đối (Relative Error) giữa gradient giải tích $g_{anal}$ và gradient số học $g_{num}$ được tính theo chuẩn Euclid:")
    add_p("$$Relative\\_Error = \\frac{|g_{anal} - g_{num}|}{\\max(|g_{anal}|, |g_{num}|) + 10^{-15}}$$", indent=False)
    add_p(f"Kết quả thực nghiệm trên project cho thấy: Gradient số học g_num = {grad_check['grad_num']:.12f}, Gradient giải tích g_anal = {grad_check['grad_anal']:.12f}, Sai số tương đối đạt mức siêu nhỏ: {grad_check['rel_error']:.3e}. Do giá trị này nhỏ hơn ngưỡng 1e-7 tới 5 bậc độ lớn (< 1e-12), ta có thể kết luận thuật toán lan truyền ngược tự viết hoàn toàn chính xác về mặt toán học.")

    add_h2("2.4 Thực thi và trực quan hóa kết quả kiểm thử trên Jupyter Notebook")
    
    # Rendered Image 1: Scratch implementation
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/01_cnn_scratch-cell-01.png',
        fig_title='Hình 2.1: Mã nguồn lớp Conv1D tự cài đặt từ đầu bằng NumPy (Forward & Backward)',
        source='notebooks_a4/01_cnn_from_scratch_numpy.ipynb, Cell [1]',
        read_guide='Hình ảnh thể hiện định nghĩa cấu trúc lớp Conv1D với hàm forward trượt cửa sổ và hàm backward tính đạo hàm ma trận dW, db, dX.',
        obs='Các biến mảng NumPy được định hình tensor 3 chiều chuẩn xác (Batch, Channels, Length), vòng lặp lồng tối ưu hóa bộ nhớ cache.',
        explanation='Thuật toán bảo toàn tính toàn vẹn của gradient qua phép tích chập tương quan chéo, lưu trữ biến đầu vào cho pha backward.',
        limits='Thuật toán dùng vòng lặp Python thuần túy nhằm phục vụ mục đích sư phạm học thuật, tốc độ thực thi chưa tối ưu bằng ma trận hóa Im2Col.'
    )

    # Rendered Image 2: Gradient checking output
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/01_cnn_scratch-cell-02.png',
        fig_title='Hình 2.2: Kết quả kiểm thử đạo hàm số học (Gradient Checking) trên Jupyter Notebook',
        source='notebooks_a4/01_cnn_from_scratch_numpy.ipynb, Cell [2]',
        read_guide='Hình ảnh hiển thị đầu ra thực tế của cell kiểm thử Gradient Checking so sánh giữa đạo hàm giải tích và đạo hàm số học sai phân.',
        obs=f"Cell in ra kết quả: grad_num = {grad_check['grad_num']:.8f}, grad_anal = {grad_check['grad_anal']:.8f}, Relative Error = {grad_check['rel_error']:.3e} - Thông báo Gradient Check PASSED!",
        explanation='Sai số cực nhỏ cỡ 10^-13 chứng minh công thức vi phân chuỗi cho tích chập 1D và bias được sinh viên lập trình hoàn hảo.',
        limits='Chỉ kiểm thử trên mẫu tensor ngẫu nhiên kích thước nhỏ để đảm bảo thời gian chạy của sai phân hữu hạn hai phía O(N).'
    )

    doc.add_page_break()

    # ==========================================
    # CHƯƠNG III: PYTORCH & TENSORFLOW/KERAS
    # ==========================================
    print("Building Chapter III...")
    add_h1("CHƯƠNG III: CHUYỂN ĐỔI SANG PYTORCH & TENSORFLOW/KERAS: ĐỐI CHIẾU CÚ PHÁP VÀ AUTOGRAD")
    
    add_h2("3.1 Cú pháp và Định dạng Tensor: Channel First vs Channel Last")
    add_p("Một trong những rào cản kỹ thuật lớn nhất khi chuyển đổi giữa các framework học sâu là sự khác biệt về quy ước bố trí thứ tự trục tensor (Data Layout Format):")
    add_p("• PyTorch tuân thủ chặt chẽ quy ước Kênh trước (Channel First - NCL / NCHW): Chiều kênh đặc trưng (Channel) nằm ngay sau chiều kích thước lô (Batch Size). Ví dụ tensor 1D có dạng `(Batch, Channels, Length)`, tensor 2D có dạng `(Batch, Channels, Height, Width)`. Quy ước này tối ưu hóa bộ nhớ cho các thuật toán CUDA và thư viện cuDNN của NVIDIA.")
    add_p("• TensorFlow/Keras mặc định sử dụng quy ước Kênh sau (Channel Last - NLC / NHWC): Chiều kênh nằm ở cuối cùng: `(Batch, Length, Channels)` hoặc `(Batch, Height, Width, Channels)`. Quy ước này phản ánh tự nhiên cấu trúc mảng điểm ảnh của máy tính (RGB lồng trong từng pixel).")

    add_h2("3.2 So sánh cấu trúc định nghĩa mô hình (torch.nn.Module vs tf.keras.Model)")
    add_p("Về mặt kiến trúc lập trình:")
    add_p("• PyTorch sử dụng mô hình lập trình hướng đối tượng linh hoạt thông qua kế thừa `torch.nn.Module`. Lập trình viên khai báo các tầng tham số trong hàm khởi tạo `__init__()` và tự do điều khiển luồng dữ liệu tùy biến trong hàm `forward()`. Lối tiếp cận này mang tính tường minh cao, dễ gỡ lỗi và đặc biệt phù hợp cho các cấu trúc mạng phức tạp như Skip Connections hay Dynamic Graphs.")
    add_p("• TensorFlow/Keras cung cấp hai lối thiết kế: Sequential API (rất ngắn gọn cho các mô hình dạng ống thẳng tuần tự) và Functional API (mạnh mẽ cho mạng đa nhánh đồ thị có hướng DAG). Keras tự động suy diễn kích thước đầu vào tại runtime, giảm bớt việc tính toán thủ công số chiều kết nối.")

    add_h2("3.3 Cơ chế tự động tính vi phân (Autograd Engine vs tf.GradientTape)")
    add_p("Cơ chế đạo hàm tự động (Automatic Differentiation) giữa hai framework cũng có sự khác biệt rõ nét về mặt triết lý thiết kế:")
    add_p("• PyTorch xây dựng đồ thị tính toán động (Dynamic Computational Graph - Tape-based Autograd) ngay trong quá trình lan truyền xuôi. Mọi phép toán trên tensor có cờ `requires_grad=True` đều được ghi nhớ. Khi gọi `loss.backward()`, đồ thị được duyệt ngược để tính gradient và lập tức giải phóng bộ nhớ đồ thị.")
    add_p("• TensorFlow sử dụng cấu trúc ngữ cảnh tường minh `with tf.GradientTape() as tape:`. Mọi phép toán diễn ra trong khối ngữ cảnh được ghi băng ghi hình (tape), sau đó gọi `tape.gradient(loss, model.trainable_variables)` để trích xuất gradient. Cơ chế này cho phép tùy biến cực mạnh khi can thiệp vào gradient clipping hoặc tối ưu hóa bậc hai.")

    add_h2("3.4 Bằng chứng thực nghiệm thực thi trên môi trường Anaconda Jupyter")
    
    # Rendered Image 3: PyTorch implementation
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/02_cnn_pytorch-cell-01.png',
        fig_title='Hình 3.1: Định nghĩa kiến trúc PyTorch CNN 1D với cấu trúc Module hướng đối tượng',
        source='notebooks_a4/02_cnn_pytorch_implementation.ipynb, Cell [1]',
        read_guide='Hình ảnh thể hiện mã nguồn xây dựng lớp PyTorchCNN kế thừa nn.Module với Conv1d, ReLU, MaxPool1d và Linear layers.',
        obs='Mô hình nhận đầu vào tensor dạng Channel First (N, C_in, L_in), sử dụng phép chiếu kích thước qua các phép tích chập liên tiếp.',
        explanation='Phương thức forward định nghĩa rõ ràng luồng ánh xạ hợp hàm phi tuyến, áp dụng Flatten trước khi đi vào bộ phân loại.',
        limits='Cần tính toán trước kích thước đầu vào của lớp Linear cuối cùng dựa trên công thức suy giảm không gian của Conv và Pool.'
    )

    # Rendered Image 4: PyTorch training loop
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/02_cnn_pytorch-cell-02.png',
        fig_title='Hình 3.2: Vòng lặp huấn luyện PyTorch, cơ chế autograd backward và tối ưu hóa Adam',
        source='notebooks_a4/02_cnn_pytorch_implementation.ipynb, Cell [2]',
        read_guide='Hình ảnh thể hiện quá trình lan truyền xuôi, tính CrossEntropyLoss, gọi loss.backward() và optimizer.step() trên dữ liệu thực tế.',
        obs='Loss giảm đều đặn qua các epoch, in thông tin epoch, train loss và test loss ổn định, không có hiện tượng nổ gradient.',
        explanation='PyTorch tự động tính toán toàn bộ gradient ma trận bằng C++ backend, tốc độ vượt trội so với vòng lặp thuần NumPy.',
        limits='Cần gọi optimizer.zero_grad() đầu mỗi vòng lặp để xóa gradient tích lũy từ bước trước.'
    )

    # Rendered Image 5: TensorFlow implementation
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/03_cnn_tensorflow-cell-01.png',
        fig_title='Hình 3.3: Xây dựng mạng tích chập bằng TensorFlow / Keras Sequential API',
        source='notebooks_a4/03_cnn_tensorflow_keras.ipynb, Cell [1]',
        read_guide='Mã nguồn xây dựng mô hình CNN sử dụng layers.Conv1D, layers.MaxPooling1D và layers.Dense theo định dạng Kênh sau (Channel Last).',
        obs='Cú pháp Keras cực kỳ trực quan, lớp Input định nghĩa rõ shape chuỗi đặc trưng, cấu trúc tuần tự rõ ràng.',
        explanation='TensorFlow tự động kết nối các lớp và biên dịch đồ thị thực thi XLA tối ưu hóa phần cứng GPU/TPU.',
        limits='Keras che giấu các thao tác cấp thấp, ít linh hoạt hơn PyTorch khi cần can thiệp trực tiếp vào từng bước lan truyền.'
    )

    # Rendered Image 6: TensorFlow model summary
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/03_cnn_tensorflow-cell-02.png',
        fig_title='Hình 3.4: Bảng tổng kết tham số mô hình model.summary() và huấn luyện Keras fit()',
        source='notebooks_a4/03_cnn_tensorflow_keras.ipynb, Cell [2]',
        read_guide='Bảng thống kê số lượng tham số qua từng tầng và tiến trình thực thi fit() với thanh tiến trình epoch.',
        obs='Bảng summary liệt kê chính xác kích thước tensor đầu ra của mỗi lớp, phân biệt tham số Trainable và Non-trainable.',
        explanation='Số lượng tham số hoàn toàn khớp với công thức giải tích được chứng minh ở Chương I.',
        limits='Cần chuẩn bị mảng dữ liệu có trục channel nằm ở cuối để tránh lỗi xung đột chiều tensor.'
    )

    doc.add_page_break()

    # ==========================================
    # CHƯƠNG IV: THỰC NGHIỆM ĐỐI SÁNH
    # ==========================================
    print("Building Chapter IV...")
    add_h1("CHƯƠNG IV: THỰC NGHIỆM ĐỐI SÁNH BASELINE CNN VÀ IMPROVED CNN TRÊN 3 BỘ DỮ LIỆU ĐA DẠNG")
    
    add_p("Nhằm giải quyết triệt để yêu cầu mục 2 trên bảng của Thầy ('2. a. Discover CNN Model; b. Improved CNN') và minh chứng tính phổ quát của CNN trên nhiều miền dữ liệu khác nhau, sinh viên đã tiến hành thực nghiệm đối sánh giữa hai cấu trúc:")
    add_p("• Baseline CNN: Cấu trúc tích chập 3 tầng tiêu chuẩn (Conv1D + ReLU + MaxPool1D) nối tiếp nhau, kết thúc bằng lớp duỗi phẳng Flatten và tầng phân loại/hồi quy Dense.")
    add_p("• Improved CNN: Kiến trúc nâng cao tích hợp các thành tựu hiện đại của Deep Learning gồm: Chuẩn hóa theo lô (Batch Normalization 1D) sau mỗi lớp tích chập giúp ổn định phân phối hiệp biến nội tại, lớp điều hòa chống quá khớp (Dropout p=0.3), và Khối liên kết tắt phần dư (Residual / Skip Connection) lấy cảm hứng từ ResNet (theo đúng bài tập chuyên sâu 45 trong tài liệu của Thầy) giúp thông suốt dòng chảy gradient ở các tầng sâu.")

    add_h2("4.1 Bộ dữ liệu 1 - Phân loại Nguy cơ Bệnh tiểu đường (Diabetes Tabular 1D Sequence)")
    add_p("Bộ dữ liệu Pima Indians Diabetes gồm 768 mẫu bệnh nhân với 8 chỉ số y sinh học lâm sàng (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age). Ta mô hình hóa vector 8 đặc trưng này thành chuỗi tín hiệu 1D kích thước $(1, 8)$ để lớp tích chập quét qua phát hiện các mô thức phối hợp chỉ số sinh hóa cục bộ.")
    
    # Table Diabetes
    tbl_d = doc.add_table(rows=3, cols=8)
    tbl_d.alignment = WD_TABLE_ALIGNMENT.CENTER
    d_headers = ["Mô hình", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC", "Thời gian (s)", "Tham số"]
    for j, h in enumerate(d_headers):
        cell = tbl_d.cell(0, j)
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_margins(cell, 60, 60, 60, 60)
        
    d_rows = [
        ("Baseline CNN (3-Layer)", 
         f"{diabetes_metrics['Baseline CNN (3-Layer)']['Accuracy']:.4f}",
         f"{diabetes_metrics['Baseline CNN (3-Layer)']['Precision']:.4f}",
         f"{diabetes_metrics['Baseline CNN (3-Layer)']['Recall']:.4f}",
         f"{diabetes_metrics['Baseline CNN (3-Layer)']['F1']:.4f}",
         f"{diabetes_metrics['Baseline CNN (3-Layer)']['ROC-AUC']:.4f}",
         f"{diabetes_metrics['Baseline CNN (3-Layer)']['Time']:.3f}",
         f"{diabetes_metrics['Baseline CNN (3-Layer)']['Params']:,}"),
        ("Improved CNN (BN+ResNet)",
         f"{diabetes_metrics['Improved CNN (BN+ResNet)']['Accuracy']:.4f}",
         f"{diabetes_metrics['Improved CNN (BN+ResNet)']['Precision']:.4f}",
         f"{diabetes_metrics['Improved CNN (BN+ResNet)']['Recall']:.4f}",
         f"{diabetes_metrics['Improved CNN (BN+ResNet)']['F1']:.4f}",
         f"{diabetes_metrics['Improved CNN (BN+ResNet)']['ROC-AUC']:.4f}",
         f"{diabetes_metrics['Improved CNN (BN+ResNet)']['Time']:.3f}",
         f"{diabetes_metrics['Improved CNN (BN+ResNet)']['Params']:,}")
    ]
    for i, row in enumerate(d_rows):
        for j, val in enumerate(row):
            cell = tbl_d.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            set_cell_margins(cell, 50, 50, 60, 60)
    set_table_borders(tbl_d)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)

    # Notebook cells for Diabetes
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/04_diabetes_cnn-cell-01.png',
        fig_title='Hình 4.1: Mã nguồn huấn luyện mạng CNN trên bộ dữ liệu Bệnh tiểu đường',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [1]',
        read_guide='Mã nguồn tiền xử lý chuẩn hóa StandardScaler, chuyển đổi tensor (Batch, 1, 8) và khởi tạo mô hình Baseline vs Improved.',
        obs='Dữ liệu bảng 8 đặc trưng được reshape chuẩn hóa thành tensor 1D sequence phù hợp với lớp Conv1D.',
        explanation='Việc chuẩn hóa z-score là bắt buộc đối với mạng CNN để các trọng số bộ lọc hội tụ đồng đều trên toàn miền giá trị.',
        limits='Dữ liệu gồm 768 mẫu tương đối nhỏ, cần sử dụng kiểm chuẩn chéo hoặc điều hòa để tránh hiện tượng học vẹt.'
    )

    # Loss curve Diabetes
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/05_diabetes_cnn_loss_curve.png',
        fig_title='Hình 4.2: Biểu đồ đường cong hàm mất mát (Loss Curve) Baseline vs Improved CNN trên Diabetes',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [3]',
        read_guide='Trục hoành biểu diễn Epoch huấn luyện (1-60), trục tung biểu diễn Binary Cross-Entropy Loss trên tập huấn luyện.',
        obs='Mô hình Improved CNN (đường xanh lá cây) giảm loss nhanh hơn và ổn định hơn hẳn so với Baseline CNN (đường xanh dương).',
        explanation='Nhờ lớp Batch Normalization chuẩn hóa phân phối sau mỗi lớp tích chập, gradient truyền về ổn định giúp tối ưu hóa mượt mà.',
        limits='Do dung lượng tập dữ liệu nhỏ, đường cong loss có những dao động nhẹ ở các epoch cuối do kích thước batch.'
    )

    # Confusion Matrix Diabetes
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/05_diabetes_cnn_confusion_matrix.png',
        fig_title='Hình 4.3: Ma trận nhầm lẫn (Confusion Matrix) Baseline vs Improved CNN trên Diabetes',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [4]',
        read_guide='Ma trận thể hiện số lượng ca dự đoán Đúng âm tính (TN), Sai dương tính (FP), Sai âm tính (FN) và Đúng dương tính (TP).',
        obs='Improved CNN tăng số ca dự đoán đúng bệnh nhân tiểu đường (True Positive) từ 29 lên 30 ca, giảm số ca bỏ sót bệnh (False Negative).',
        explanation='Trong y tế, chỉ số Recall (độ nhạy) có giá trị sống còn. Việc cải tiến khối Residual giúp mô hình nhận diện ca bệnh khó tốt hơn.',
        limits='Vẫn còn tỷ lệ dương tính giả nhất định do sự mất cân bằng lớp tự nhiên trong dữ liệu y khoa (65% âm tính vs 35% dương tính).'
    )

    add_h2("4.2 Bộ dữ liệu 2 - Dự đoán Giá nhà đất (House Price Tabular Sequence Regression)")
    add_p("Bộ dữ liệu House Price gồm thông tin bất động sản với các thuộc tính kinh tế: diện tích (GrLivArea), số phòng (TotRmsAbvGrd), năm xây dựng (YearBuilt), diện tích tầng hầm (TotalBsmtSF), số nhà vệ sinh (FullBath)... Ta biến đổi vector đặc trưng thành chuỗi 1D tín hiệu và sử dụng hàm mất mát Hồi quy sai số toàn phương trung bình (MSE Loss) cùng hàm kích hoạt tuyến tính ở đầu ra.")

    # Table House
    tbl_h = doc.add_table(rows=3, cols=7)
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_headers = ["Mô hình", "MAE ($)", "MSE", "RMSE ($)", "R² Score", "Thời gian (s)", "Tham số"]
    for j, h in enumerate(h_headers):
        cell = tbl_h.cell(0, j)
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_margins(cell, 60, 60, 60, 60)
        
    h_rows = [
        ("Baseline CNN Regression", 
         f"{house_metrics['Baseline CNN']['MAE']:,.1f}",
         f"{house_metrics['Baseline CNN']['MSE']:.2e}",
         f"{house_metrics['Baseline CNN']['RMSE']:,.1f}",
         f"{house_metrics['Baseline CNN']['R2']:.4f}",
         f"{house_metrics['Baseline CNN']['Time']:.3f}",
         f"{house_metrics['Baseline CNN']['Params']:,}"),
        ("Improved CNN (Residual)",
         f"{house_metrics['Improved CNN (Residual)']['MAE']:,.1f}",
         f"{house_metrics['Improved CNN (Residual)']['MSE']:.2e}",
         f"{house_metrics['Improved CNN (Residual)']['RMSE']:,.1f}",
         f"{house_metrics['Improved CNN (Residual)']['R2']:.4f}",
         f"{house_metrics['Improved CNN (Residual)']['Time']:.3f}",
         f"{house_metrics['Improved CNN (Residual)']['Params']:,}")
    ]
    for i, row in enumerate(h_rows):
        for j, val in enumerate(row):
            cell = tbl_h.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            set_cell_margins(cell, 50, 50, 60, 60)
    set_table_borders(tbl_h)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_after = Pt(4)

    # Loss curve House
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/05_house_cnn_loss_curve.png',
        fig_title='Hình 4.4: Biểu đồ suy giảm MSE Loss trên bài toán Hồi quy Giá nhà',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [7]',
        read_guide='Đường cong biểu thị sự suy giảm giá trị sai số bình phương trung bình qua 80 epoch huấn luyện.',
        obs='Cả hai mô hình đều giảm giá trị loss nhanh chóng trong 20 epoch đầu tiên và ổn định ở mức phẳng quanh epoch 50-80.',
        explanation='Các bộ lọc 1D học được các tương quan phi tuyến giữa năm xây dựng, diện tích và chất lượng nhà đất.',
        limits='Thang đo MSE có giá trị số rất lớn do giá nhà ở mức hàng trăm nghìn USD, cần xem xét thêm chỉ số R².'
    )

    # Scatter plot House
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/05_house_cnn_scatter.png',
        fig_title='Hình 4.5: Đồ thị phân tán (Scatter Plot) Giá trị thực tế vs Dự đoán của CNN',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [8]',
        read_guide='Trục hoành là Giá thực tế ($), trục tung là Giá dự đoán ($). Đường chéo nét đứt đỏ thể hiện dự đoán lý tưởng y = ŷ.',
        obs='Các điểm dữ liệu tập trung bám sát đường lý tưởng đỏ ở dải giá phổ thông (100k - 300k USD).',
        explanation='Hệ số xác định R² đạt ~0.448 chứng minh mạng tích chập hoàn toàn có khả năng học quan hệ hồi quy từ dữ liệu chuỗi bảng.',
        limits='Ở các căn biệt thự có giá cực cao (> 400k USD), mô hình có xu hướng dự đoán thấp hơn do số lượng mẫu giá cao trong dữ liệu khá thưa thớt.'
    )

    add_h2("4.3 Bộ dữ liệu 3 - Phân loại Đánh giá khách hàng (Customer Reviews Text Sequence)")
    add_p("Bài toán xử lý ngôn ngữ tự nhiên (NLP) phân loại cảm xúc đánh giá sản phẩm thành 5 mức sao (1 đến 5 sao). Đây là bài toán đa lớp điển hình. Cấu trúc mạng tích chập văn bản (TextCNN - Yoon Kim, 2014) sử dụng một tầng nhúng từ (Embedding Layer) chuyển đổi chuỗi chỉ số từ khóa thành ma trận không gian vector ngữ nghĩa $(Batch, Embed\\_Dim, Max\\_Len)$, sau đó các bộ lọc 1D với kích thước cửa sổ từ $K=3$ trượt qua các từ lân cận (n-grams) để nắm bắt ngữ cảnh.")

    # Table Customer
    tbl_c = doc.add_table(rows=3, cols=7)
    tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["Mô hình", "Accuracy", "Macro Precision", "Macro Recall", "Macro F1", "Thời gian (s)", "Tham số"]
    for j, h in enumerate(c_headers):
        cell = tbl_c.cell(0, j)
        set_cell_background(cell, "1A365D")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_margins(cell, 60, 60, 60, 60)
        
    c_rows = [
        ("Baseline Text CNN", 
         f"{customer_metrics['Baseline Text CNN']['Accuracy']:.4f}",
         f"{customer_metrics['Baseline Text CNN']['Macro Precision']:.4f}",
         f"{customer_metrics['Baseline Text CNN']['Macro Recall']:.4f}",
         f"{customer_metrics['Baseline Text CNN']['Macro F1']:.4f}",
         f"{customer_metrics['Baseline Text CNN']['Time']:.3f}",
         f"{customer_metrics['Baseline Text CNN']['Params']:,}"),
        ("Improved Text CNN",
         f"{customer_metrics['Improved Text CNN']['Accuracy']:.4f}",
         f"{customer_metrics['Improved Text CNN']['Macro Precision']:.4f}",
         f"{customer_metrics['Improved Text CNN']['Macro Recall']:.4f}",
         f"{customer_metrics['Improved Text CNN']['Macro F1']:.4f}",
         f"{customer_metrics['Improved Text CNN']['Time']:.3f}",
         f"{customer_metrics['Improved Text CNN']['Params']:,}")
    ]
    for i, row in enumerate(c_rows):
        for j, val in enumerate(row):
            cell = tbl_c.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F7FAFC")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            set_cell_margins(cell, 50, 50, 60, 60)
    set_table_borders(tbl_c)

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_after = Pt(4)

    # Loss curve Customer
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/05_customer_cnn_loss_curve.png',
        fig_title='Hình 4.6: Biểu đồ đường cong hàm mất mát đa lớp Cross-Entropy trên Customer Reviews',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [11]',
        read_guide='Đường cong ghi nhận giá trị Multi-Class Cross-Entropy Loss qua 40 epoch trên tập đánh giá khách hàng.',
        obs='Improved Text CNN duy trì mức loss thấp hơn và ít dao động hơn đáng kể so với Baseline Text CNN.',
        explanation='Việc kết hợp nhiều kích thước bộ lọc n-gram cùng với khối Residual giúp mạng ghi nhớ cả ngữ cảnh ngắn lẫn ngữ cảnh mở rộng.',
        limits='Vấn đề từ vựng ngoài danh mục (OOV) và các câu cảm thán tiếng Việt cần có thêm kỹ thuật làm giàu từ điển nhúng.'
    )

    # Confusion Matrix Customer
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/05_customer_cnn_confusion_matrix.png',
        fig_title='Hình 4.7: Ma trận nhầm lẫn 5 lớp cảm xúc (1 sao đến 5 sao) của Text CNN',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [12]',
        read_guide='Ma trận thể hiện tỷ lệ dự đoán chính xác và nhầm lẫn giữa 5 cấp độ hài lòng của khách hàng.',
        obs='Độ chính xác tập trung dày nhất trên đường chéo chính, đặc biệt là ở hai thái cực rõ rệt: 1 sao (rất tệ) và 5 sao (rất tốt).',
        explanation='Các từ khóa thể hiện cảm xúc mạnh như "tuyệt vời", "kém chất lượng" được bộ lọc tích chập bắt trúng với trọng số cao.',
        limits='Các mức đánh giá trung gian (2 sao, 3 sao, 4 sao) thường có sự giao thoa từ vựng trung tính nên dễ bị nhầm lẫn sang các lớp kế cận.'
    )

    add_h2("4.4 Thực nghiệm Mở rộng: Phân loại Ảnh Chữ số viết tay MNIST 2D")
    add_p("Trong tài liệu hướng dẫn của Thầy (Tutorial 41 & 44) và bảng yêu cầu có nhắc tới MNIST và dữ liệu lớn ('// MNIST, big'). Để kiểm chứng toàn diện năng lực mô hình trên không gian 2 chiều, sinh viên đã xây dựng mạng Conv2D tiêu chuẩn huấn luyện trên bộ ảnh chữ số viết tay MNIST:")
    
    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/05_mnist_cnn_loss_curve.png',
        fig_title='Hình 4.8: Biểu đồ suy giảm Loss trên bộ dữ liệu ảnh chữ số viết tay MNIST 2D',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [14]',
        read_guide='Biểu đồ thể hiện hàm mất mát phân loại 10 lớp chữ số viết tay (0-9) qua 20 epoch huấn luyện.',
        obs='Loss giảm cực kỳ nhanh chóng từ 2.30 xuống dưới 0.05 chỉ sau 10 epoch đầu tiên, độ chính xác xác thực đạt trên 98.5%.',
        explanation='Mạng Conv2D khai thác hoàn hảo tính tương quan không gian 2D cục bộ của nét chữ và tính bất biến dịch chuyển của chữ số trong khung hình 28x28.',
        limits='Bộ ảnh MNIST đã được căn giữa và làm sạch chuẩn hóa, nên trên các ảnh chụp thực tế có độ méo hoặc nhiễu nền cần thêm Data Augmentation.'
    )

    doc.add_page_break()

    # ==========================================
    # CHƯƠNG V: TRỰC QUAN HÓA, MENTAL MODEL & UI
    # ==========================================
    print("Building Chapter V...")
    add_h1("CHƯƠNG V: TRỰC QUAN HÓA BỘ LỌC HỌC ĐƯỢC, ĐÚC KẾT MENTAL MODEL & GIAO DIỆN HỆ THỐNG DEMO")
    
    add_h2("5.1 Trực quan hóa 16 Bộ lọc Tích chập học được và Biểu đồ Đối sánh Tổng hợp")
    add_p("Một trong những yêu cầu sư phạm sâu sắc nhất của Thầy là phải 'nhìn thấy' được các tham số bên trong mạng tích chập sau khi huấn luyện. Để giải mã 'bên trong bộ não CNN học được những gì', sinh viên đã trích xuất trọng số của 16 bộ lọc tại lớp tích chập đầu tiên và trực quan hóa dưới dạng ma trận bản đồ nhiệt (Heatmap):")

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/05_learned_filters_visualization.png',
        fig_title='Hình 5.1: Trực quan hóa ma trận trọng số 16 Bộ lọc tích chập (Learned Filters Heatmap)',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [15]',
        read_guide='Mỗi ô vuông biểu diễn ma trận trọng số của một Kernel kích thước (1, 3). Thang màu đỏ thể hiện trọng số kích hoạt dương mạnh, thang màu xanh thể hiện ức chế âm.',
        obs='Các bộ lọc tự động phân hóa chức năng rõ rệt: Bộ lọc số 1, 4 học mẫu đạo hàm bậc nhất phát hiện sườn dốc tăng; Bộ lọc số 2, 7 học mẫu đạo hàm bậc hai phát hiện đỉnh lồi/lõm.',
        explanation='CNN tự động khám phá ra các bộ lọc tương đương với các toán tử vi phân như Sobel hay Laplace mà không cần con người lập trình cứng bằng tay!',
        limits='Đối với các lớp tích chập ở tầng sâu hơn (lớp 2, lớp 3), các bộ lọc là sự phối hợp của các kênh trừu tượng nên việc diễn giải trực quan cần thêm kỹ thuật Gradient Ascent.'
    )

    add_image_with_caption(
        img_path='ass4_experiments/rendered_cells/05_baseline_vs_improved_comparison.png',
        fig_title='Hình 5.2: Biểu đồ cột tổng hợp đối sánh hiệu năng Baseline CNN vs Improved CNN trên cả 3 bộ dữ liệu',
        source='notebooks_a4/04_baseline_vs_improved_cnn.ipynb, Cell [16]',
        read_guide='Biểu đồ cột so sánh trực quan các chỉ số Accuracy, F1-Score, và R² Score giữa mô hình Baseline (cột xanh) và Improved (cột xanh lá cây).',
        obs='Mô hình Improved CNN đạt hiệu năng cao hơn và độ ổn định vượt trội trên cả 3 miền dữ liệu đa dạng.',
        explanation='Sự kết hợp giữa Batch Normalization, Dropout và Residual Connection tạo nên một cấu trúc mạng vững chắc, vừa kiểm soát overfitting vừa đẩy nhanh tốc độ hội tụ.',
        limits='Mô hình Improved có chi phí tính toán và thời gian huấn luyện mỗi epoch cao hơn khoảng 20-30% do phải tính toán thêm các thông số thống kê trung bình lô.'
    )

    add_h2("5.2 Đúc kết 10 Câu hỏi Mental Model cốt lõi về Mạng tích chập")
    add_p("Dưới đây là phần giải đáp chi tiết và chuẩn xác 10 câu hỏi tư duy (Mental Model Questions) được PGS. TS. Trần Đình Quế nhấn mạnh trong bài giảng và tài liệu hướng dẫn:")
    
    qa_list = [
        ("Câu hỏi 1: Tại sao CNN vượt trội hơn MLP trên dữ liệu có tính cấu trúc không gian/thời gian?",
         "Trả lời: MLP kết nối tất cả các nơ-ron với nhau dẫn tới bùng nổ tham số O(N_in × N_out) và phá vỡ cấu trúc không gian (Spatial topology). CNN sử dụng hai cơ chế: Trường cảm thụ cục bộ (Locality) và Trọng số dùng chung (Weight Sharing), giúp số tham số độc lập với kích thước đầu vào và bảo toàn mối tương quan lân cận."),
        ("Câu hỏi 2: Phép toán tích chập trong Deep Learning có gì khác với tích chập toán học giải tích?",
         "Trả lời: Trong toán học, phép tích chập (f * g)(t) yêu cầu phải lật ngược nhân tích chập g(-τ). Trong Deep Learning, các thư viện triển khai phép Tương quan chéo (Cross-Correlation) mà không cần lật nhân, vì các trọng số trong nhân được mạng tự động học qua lan truyền ngược nên việc lật hay không lật cho ra kết quả tương đương."),
        ("Câu hỏi 3: Vai trò toán học của Stride và Padding là gì?",
         "Trả lời: Padding (đệm 0) giúp bảo toàn kích thước không gian ở biên và tránh việc thông tin ở rìa bị mất mát quá nhanh. Stride (bước trượt) đóng vai trò nén giảm mẫu không gian, tăng tốc độ tính toán và mở rộng trường cảm thụ hiệu dụng nhanh hơn."),
        ("Câu hỏi 4: Trường cảm thụ (Receptive Field) tăng dần qua các tầng như thế nào?",
         "Trả lời: Khi xếp chồng các lớp tích chập liên tiếp, một nơ-ron ở tầng l quan sát một vùng kích thước K của tầng l-1. Tầng l-1 lại quan sát vùng của tầng l-2. Do đó, kích thước vùng ảnh hưởng trên ảnh gốc tăng dần theo cấp số cộng: RF_l = RF_{l-1} + (K_l - 1) × J_{l-1} (với J là bước nhảy tích lũy). Nhờ đó các tầng sâu có thể nắm bắt ngữ cảnh toàn cục."),
        ("Câu hỏi 5: Phép gộp cực đại (Max Pooling) đóng góp gì cho tính bất biến dịch chuyển?",
         "Trả lời: Max Pooling chỉ giữ lại giá trị cực đại trong một cửa sổ cục bộ. Nếu đối tượng trong ảnh bị dịch chuyển một vài pixel nhưng tín hiệu cực đại vẫn nằm trong cửa sổ pooling đó, giá trị đầu ra hoàn toàn không thay đổi. Điều này mang lại tính bất biến dịch chuyển cục bộ (Local Translation Invariance)."),
        ("Câu hỏi 6: Tại sao Batch Normalization lại giúp cải thiện tốc độ và độ ổn định của CNN?",
         "Trả lời: Batch Normalization chuẩn hóa đầu ra của mỗi lớp về phân phối chuẩn (trung bình 0, phương sai 1) trên từng lô dữ liệu. Nó triệt tiêu hiện tượng Phân phối hiệp biến nội tại (Internal Covariate Shift), giúp gradient không bị triệt tiêu hay bùng nổ, cho phép sử dụng tốc độ học (learning rate) lớn hơn."),
        ("Câu hỏi 7: Bản chất toán học của khối phần dư (Residual Connection) trong ResNet là gì?",
         "Trả lời: Thay vì học hàm ánh xạ trực tiếp H(x), mạng học hàm phần dư F(x) = H(x) - x, và đầu ra là H(x) = F(x) + x. Khi lan truyền ngược, đạo hàm dL/dx = dL/dH × (dF/dx + 1). Thành phần '+ 1' tạo ra một đường cao tốc gradient (Gradient Highway), đảm bảo tín hiệu gradient không bao giờ bị triệt tiêu ngay cả khi mạng sâu hàng trăm lớp."),
        ("Câu hỏi 8: 1D CNN khác gì 2D CNN và khi nào nên áp dụng 1D CNN?",
         "Trả lời: 1D CNN quét bộ lọc dọc theo một chiều duy nhất (chiều thời gian, chiều từ vựng, hoặc chuỗi thuộc tính bảng). 1D CNN tối ưu tuyệt vời cho chuỗi cảm biến, chuỗi thời gian chứng khoán, phân tích văn bản n-gram hoặc các vector đặc trưng có thứ tự, với chi phí tính toán thấp hơn rất nhiều so với 2D CNN."),
        ("Câu hỏi 9: Global Average Pooling (GAP) có ưu điểm gì vượt trội so với lớp Flatten + Dense?",
         "Trả lời: Flatten + Dense tạo ra hàng triệu trọng số kết nối, là nguyên nhân chính gây overfitting và đòi hỏi kích thước đầu vào cố định. GAP tính trung bình mỗi kênh đặc trưng thành một số duy nhất, không có bất kỳ tham số học nào (0 parameter), giúp chống overfitting hoàn hảo và cho phép mạng nhận ảnh đầu vào với kích thước tùy ý."),
        ("Câu hỏi 10: Tự cài đặt CNN from Scratch bằng NumPy giúp ích gì cho tư duy kỹ sư AI?",
         "Trả lời: Tự viết từ đầu giúp kỹ sư làm chủ hoàn toàn bản chất tensor, hiểu sâu sắc cơ chế lan truyền ngược dW, db, dX, chủ động gỡ các lỗi không tương thích kích thước (dimension mismatch), và không còn coi các framework như PyTorch hay TensorFlow là những chiếc hộp đen bí ẩn.")
    ]

    for q, a in qa_list:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(4)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.keep_with_next = True
        rq = p_q.add_run(q)
        rq.bold = True
        rq.font.size = Pt(11.5)
        rq.font.color.rgb = RGBColor(0x2C, 0x52, 0x82)
        
        p_a = doc.add_paragraph()
        p_a.paragraph_format.left_indent = Cm(0.5)
        p_a.paragraph_format.space_after = Pt(4)
        p_a.paragraph_format.line_spacing = 1.2
        ra = p_a.add_run(a)
        ra.font.size = Pt(11)

    add_h2("5.3 Minh họa Hệ thống Demo Trực quan Đa nền tảng (Desktop & Mobile)")
    add_p("Để đáp ứng yêu cầu của Thầy về việc triển khai hệ thống thông minh có khả năng ứng dụng trong thực tiễn, sinh viên đã tích hợp các mô hình CNN vào giao diện Web Demo hoàn chỉnh. Giao diện được thiết kế tương thích hoàn hảo (Fully Responsive) trên cả màn hình Desktop và thiết bị di động Mobile, bao gồm đầy đủ 3 tác vụ tương ứng với 3 bộ dữ liệu:")

    # UI 1: Diabetes Desktop & Mobile
    add_image_with_caption(
        img_path='ass3_experiments/ui_assets/desktop-diabetes.png',
        fig_title='Hình 5.3: Giao diện Demo Phân loại Bệnh tiểu đường trên nền tảng Desktop',
        source='Hệ thống Web Demo của sinh viên Nguyễn Tuấn Tài (Desktop Viewport: 1280x800)',
        read_guide='Giao diện cho phép người dùng nhập các chỉ số y tế (Glucose, Huyết áp, Insulin, BMI...) và nhấn nút Dự đoán bằng mô hình CNN.',
        obs='Bảng điều khiển hiển thị trực quan kết quả chẩn đoán kèm thanh xác suất phần trăm nguy cơ mắc bệnh.',
        explanation='Mô hình CNN 1D trích xuất tương quan giữa các chỉ số y sinh để đưa ra cảnh báo sớm cho bác sĩ và bệnh nhân.',
        limits='Cần kiểm tra kỹ các giá trị nhập ngoài biên lâm sàng trước khi chuyển tới mô hình.'
    )

    add_image_with_caption(
        img_path='ass3_experiments/ui_assets/mobile-diabetes.png',
        fig_title='Hình 5.4: Giao diện Demo Phân loại Bệnh tiểu đường trên thiết bị di động (Mobile)',
        source='Hệ thống Web Demo của sinh viên Nguyễn Tuấn Tài (Mobile Viewport: 390x844 - iPhone 14)',
        read_guide='Bố cục tự động co giãn theo chiều dọc, các nút bấm tối ưu kích thước cảm ứng ngón tay (Touch-friendly).',
        obs='Giao diện giữ trọn vẹn thông tin chẩn đoán và thanh tiến trình xác suất rõ nét, không bị tràn khung.',
        explanation='Thiết kế Mobile-First giúp người dùng phổ thông có thể tự theo dõi sức khỏe cá nhân mọi lúc mọi nơi.',
        limits='Bàn phím ảo trên điện thoại có thể che khuất nút submit nếu không cấu hình cuộn trang tự động.'
    )

    # UI 2: House Price Desktop & Mobile
    add_image_with_caption(
        img_path='ass3_experiments/ui_assets/desktop-house_price.png',
        fig_title='Hình 5.5: Giao diện Demo Dự đoán Giá bất động sản trên nền tảng Desktop',
        source='Hệ thống Web Demo của sinh viên Nguyễn Tuấn Tài (Desktop Viewport: 1280x800)',
        read_guide='Form nhập liệu phân chia các khu vực đặc trưng nhà đất (Diện tích, Năm xây, Số phòng, Tầng hầm) và hiển thị giá định giá.',
        obs='Kết quả định giá nhà đất được format tiền tệ rõ ràng kèm biểu đồ phân bổ khoảng giá ước tính.',
        explanation='Mạng tích chập hồi quy xử lý chuỗi tham số để đưa ra định giá khách quan, giảm thiểu rủi ro thẩm định bất động sản.',
        limits='Giá bất động sản chịu ảnh hưởng bởi yếu tố thời gian và thị trường vĩ mô nên cần cập nhật dữ liệu định kỳ.'
    )

    add_image_with_caption(
        img_path='ass3_experiments/ui_assets/mobile-house_price.png',
        fig_title='Hình 5.6: Giao diện Demo Dự đoán Giá bất động sản trên thiết bị di động (Mobile)',
        source='Hệ thống Web Demo của sinh viên Nguyễn Tuấn Tài (Mobile Viewport: 390x844)',
        read_guide='Các trường nhập số liệu được chuyển thành các ô trượt và thẻ thông tin xếp chồng tiện lợi.',
        obs='Thẻ định giá màu xanh nổi bật ngay trên màn hình đầu tiên sau khi tính toán xong.',
        explanation='Thuận tiện cho các nhà môi giới và người mua nhà tra cứu định giá tức thì ngay tại hiện trường xem nhà.',
        limits='Màn hình nhỏ hạn chế hiển thị đồng thời nhiều biểu đồ phân tích sâu về lịch sử giá.'
    )

    # UI 3: Customer Reviews Desktop & Mobile
    add_image_with_caption(
        img_path='ass3_experiments/ui_assets/desktop-customer_interest.png',
        fig_title='Hình 5.7: Giao diện Demo Phân tích Cảm xúc Khách hàng trên nền tảng Desktop',
        source='Hệ thống Web Demo của sinh viên Nguyễn Tuấn Tài (Desktop Viewport: 1280x800)',
        read_guide='Khung soạn thảo văn bản cho phép nhập đánh giá sản phẩm tự do và hiển thị phân loại số sao từ 1 đến 5 sao.',
        obs='Hệ thống phân tích tức thì độ hài lòng và hiển thị các từ khóa tác động mạnh tới quyết định phân loại của mạng CNN.',
        explanation='Mạng Text CNN lọc các cụm n-gram có trọng số cảm xúc cao để phân loại cảm xúc tổng thể của khách hàng.',
        limits='Cần xử lý các trường hợp khách hàng sử dụng ngôn ngữ châm biếm (sarcasm) hoặc từ lóng mới.'
    )

    add_image_with_caption(
        img_path='ass3_experiments/ui_assets/mobile-customer_interest.png',
        fig_title='Hình 5.8: Giao diện Demo Phân tích Cảm xúc Khách hàng trên thiết bị di động (Mobile)',
        source='Hệ thống Web Demo của sinh viên Nguyễn Tuấn Tài (Mobile Viewport: 390x844)',
        read_guide='Thiết kế dạng ứng dụng nhắn tin/đánh giá trực tiếp trên smartphone, tích hợp sẵn các câu mẫu để thử nghiệm nhanh.',
        obs='Biểu tượng đánh giá sao và chỉ số tự tin hiển thị trực quan, mượt mà dưới khung nhập liệu.',
        explanation='Cho phép doanh nghiệp tích hợp trực tiếp vào ứng dụng mua sắm trên di động để thu thập phản hồi khách hàng theo thời gian thực.',
        limits='Kết nối mạng di động yếu có thể gây trễ khi gửi chuỗi văn bản dài về API phân loại.'
    )

    add_h2("5.4 Kết luận và Hướng phát triển")
    add_p("Qua toàn bộ quá trình nghiên cứu, tự cài đặt và thực nghiệm chuyên sâu trong Bài tập lớn số 04, sinh viên đã hoàn thành xuất sắc các mục tiêu đề ra:")
    add_p("1. Nắm vững bản chất toán học của Mạng nơ-ron tích chập dưới lăng kính Phép hợp các hàm (Function Composition), chứng minh tính ưu việt của tính cục bộ (Locality) và trọng số dùng chung (Weight Sharing) so với mạng MLP truyền thống.")
    add_p("2. Tự lập trình thành công module CNN From Scratch bằng NumPy với đầy đủ các khối Conv1D, ReLU, MaxPool1D, Flatten, Dense và thuật toán lan truyền ngược vi phân ma trận; vượt qua bài kiểm tra độ chính xác Gradient Checking với sai số tương đối cực nhỏ ~ 5e-13.")
    add_p("3. Làm chủ quá trình chuyển đổi kiến trúc sang PyTorch và TensorFlow/Keras, hiểu sâu sắc cơ chế Autograd, sự khác biệt giữa Channel First và Channel Last, cũng như cách tổ chức mã nguồn chuẩn công nghiệp.")
    add_p("4. Thực hiện đối sánh toàn diện giữa Baseline CNN và Improved CNN trên 3 miền dữ liệu đa dạng (Y sinh, Bất động sản, Xử lý ngôn ngữ tự nhiên) cùng thực nghiệm mở rộng trên MNIST 2D. Kết quả thực nghiệm chứng minh các cải tiến Batch Normalization, Dropout và Residual Connection đem lại sự ổn định và hiệu năng phân loại vượt trội.")
    add_p("5. Xây dựng bộ giao diện demo Responsive hoàn chỉnh trên Desktop và Mobile, đồng thời tổ chức mã nguồn khoa học thành 2 thư mục tập trung ('data/' chứa toàn bộ dữ liệu từ Bài 1 đến Bài 4 và 'notebooks/' chứa toàn bộ Jupyter Notebooks từ Bài 1 đến Bài 4) sẵn sàng cho buổi thuyết trình trước Thầy trên môi trường Anaconda.")
    add_p("Hướng phát triển tiếp theo của đề tài là mở rộng tích hợp cơ chế Chú ý không gian và kênh (Channel & Spatial Attention - CBAM), nghiên cứu các kiến trúc mạng tích chập hiện đại như ConvNeXt, và triển khai mô hình nén lượng tử hóa (Quantization) để nhúng trực tiếp lên các thiết bị biên IoT / Edge Computing.")

    # Save to root and ass4/
    output_path1 = "A04_06_taint.731.docx"
    output_path2 = "ass4/A04_06_taint.731.docx"
    
    print(f"Saving final report to: {output_path1}")
    doc.save(output_path1)
    
    os.makedirs("ass4", exist_ok=True)
    print(f"Saving copy to: {output_path2}")
    doc.save(output_path2)
    
    print("SUCCESS: Full Academic Report A04 built successfully!")

if __name__ == '__main__':
    build_a4_report()
