import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    src_path = os.path.join(os.path.dirname(__file__), 'build_tieuluan01_docx.py')
    dst_path = os.path.join(os.path.dirname(__file__), 'build_tieuluan02_docx.py')

    with open(src_path, 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Update imports
    old_import = "from docx.oxml.ns import nsdecls, qn"
    new_import = """from docx.oxml.ns import nsdecls, qn
from chapter5_content import add_chapter_5, add_updated_conclusion, get_extended_references"""
    assert old_import in src, "old_import not found"
    src = src.replace(old_import, new_import, 1)

    # 2. Update print
    src = src.replace("tieuluan01_06_15_taint.docx", "tieuluan02_06_15_taint.docx")
    src = src.replace("def build_tieuluan01():", "def build_tieuluan02():")
    src = src.replace("build_tieuluan01()", "build_tieuluan02()")

    # 3. Update cover page
    old_title = 'r_title = p_title.add_run("TIỂU LUẬN MÔN HỌC\\n")'
    new_title = 'r_title = p_title.add_run("TIỂU LUẬN MÔN HỌC (BÁO CÁO TOÀN DIỆN MỞ ĐẦU ĐẾN CHƯƠNG 5)\\n")'
    assert old_title in src, "old_title not found"
    src = src.replace(old_title, new_title, 1)

    old_topic = 'r_tp = p_topic.add_run("ĐỀ TÀI: NGHIÊN CỨU LÝ THUYẾT, THỰC NGHIỆM ĐỐI SÁNH\\nVÀ TRIỂN KHAI HỆ THỐNG THÔNG MINH\\n(TỪ MACHINE LEARNING CƠ BẢN, CNN ĐẾN RNN VÀ MLOPS PIPELINE)")'
    new_topic = 'r_tp = p_topic.add_run("ĐỀ TÀI: NGHIÊN CỨU LÝ THUYẾT, THỰC NGHIỆM ĐỐI SÁNH\\nVÀ TRIỂN KHAI HỆ THỐNG THÔNG MINH\\n(TỪ MACHINE LEARNING, CNN, RNN ĐẾN KNOWLEDGE GRAPH VÀ RAG PIPELINE)")'
    assert old_topic in src, "old_topic not found"
    src = src.replace(old_topic, new_topic, 1)

    # 4. Update TOC
    old_toc_tail = """        ("TỔNG KẾT VÀ ĐỊNH HƯỚNG GIAI ĐOẠN TIẾP THEO", "49"),
        ("  1. Tổng Kết Kết Quả Đạt Được Giai Đoạn 1 (Mở đầu -> Chương 4)", "49"),
        ("  2. Lộ Trình Phát Triển Hệ Thống Thông Minh Giai Đoạn 2 (Chương 5, 6, 7)", "50"),
        ("TÀI LIỆU THAM KHẢO", "52")
    ]"""
    new_toc_tail = """        ("CHƯƠNG 5: KNOWLEDGE GRAPH VÀ RAG (RETRIEVAL-AUGMENTED GENERATION)", "49"),
        ("  5.1 Mở Đầu (KG & RAG: Timeline Lịch sử và Ý nghĩa Sống còn trong AI)", "49"),
        ("  5.2 Knowledge Graph - Cơ Sở Tri Thức Đồ Hình (Knowledge Base)", "51"),
        ("  5.3 Kỹ Thuật Truy Xuất Tăng Cường Sinh Văn Bản (RAG)", "54"),
        ("  5.4 Cơ Sở Tri Thức và RAG Cho Bệnh Tiểu Đường (Diabetes Healthcare)", "58"),
        ("  5.5 Cơ Sở Tri Thức và RAG Cho Phân Tích Tài Chính (Chứng Khoán & Vàng)", "62"),
        ("  5.6 Triển Khai Hệ Thống Thực Tế (Deployment Pipeline)", "65"),
        ("TỔNG KẾT VÀ ĐỊNH HƯỚNG GIAI ĐOẠN TIẾP THEO (GNN & MULTI-AGENT)", "68"),
        ("TÀI LIỆU THAM KHẢO", "70")
    ]"""
    assert old_toc_tail in src, "old_toc_tail not found"
    src = src.replace(old_toc_tail, new_toc_tail, 1)

    # 5. Update Abbreviations
    old_abbr_tail = '("MAS", "Multi-Agent System", "Hệ thống Đa Tác tử Thông minh")\n    ]'
    new_abbr_tail = """("MAS", "Multi-Agent System", "Hệ thống Đa Tác tử Thông minh"),
        ("RDF", "Resource Description Framework", "Khuôn khổ Mô tả Tài nguyên W3C"),
        ("OWL", "Web Ontology Language", "Ngôn ngữ Bản thể học Web"),
        ("SPARQL", "SPARQL Protocol and RDF Query Language", "Ngôn ngữ Truy vấn Đồ thị RDF"),
        ("LPG", "Labeled Property Graph", "Đồ thị Thuộc tính có Nhãn"),
        ("KGE", "Knowledge Graph Embedding", "Nhúng Đồ thị Tri thức"),
        ("HNSW", "Hierarchical Navigable Small World", "Thế giới Nhỏ Điều hướng Phân cấp"),
        ("BM25", "Best Matching 25", "Thuật toán Khớp Từ khóa Tốt nhất 25"),
        ("RRF", "Reciprocal Rank Fusion", "Hợp nhất Thứ hạng Đối ứng"),
        ("CoVe", "Chain-of-Verification", "Chuỗi Kiểm chứng Chống Ảo giác"),
        ("GAT", "Graph Attention Network", "Mạng Chú ý Đồ thị"),
        ("GCN", "Graph Convolutional Network", "Mạng Tích chập Đồ thị")
    ]"""
    assert old_abbr_tail in src, "old_abbr_tail not found"
    src = src.replace(old_abbr_tail, new_abbr_tail, 1)

    # 6. Update Introduction text about report organization
    old_intro_org = """    add_h2("6. Bố Cục Báo Cáo Tiểu Luận")
    add_p("Báo cáo tiểu luận được tổ chức gồm 4 chương nội dung cốt lõi và phần tổng kết định hướng tương lai:")
    add_bullet("Phần Mở đầu: Đặt vấn đề, tính cấp thiết, mục tiêu và phương pháp nghiên cứu.")
    add_bullet("Chương 1: Lịch sử phát triển Trí tuệ Nhân tạo - Toàn cảnh các giai đoạn thăng trầm, các bước chuyển mình mô thức (Paradigm Shifts) và 3 bộ dữ liệu kinh điển đặt nền móng AI.")
    add_bullet("Chương 2: Các kỹ thuật Machine Learning cơ bản - Cơ sở toán học, khảo sát 3 bộ dữ liệu tabular (Diabetes, Housing, Wine), cài đặt chi tiết 3 phiên bản Scratch-Keras-PyTorch, thực nghiệm so sánh và triển khai REST API.")
    add_bullet("Chương 3: Mạng nơ-ron Tích chập (CNN) - Toán học tích chập, Pooling, ResNet, SE-Block, khảo sát 3 bộ dữ liệu thị giác (MNIST, Fashion-MNIST, CIFAR-10), cài đặt 3 phiên bản, ma trận nhầm lẫn và triển khai ONNX API.")
    add_bullet("Chương 4: Mạng nơ-ron Hồi quy (RNN) - Bản chất chuỗi, Vanilla RNN, BPTT, bài toán triệt tiêu gradient, LSTM, GRU, khảo sát 3 bộ dữ liệu chuỗi (Gold Prices, Jena Climate, IMDb), cài đặt 3 phiên bản, dự báo đa bước và dashboard triển khai.")
    add_bullet("Phần Kết luận: Tổng kết & Định hướng: Đánh giá kết quả và lộ trình mở rộng sang Chương 5 (Knowledge Graph & RAG), Chương 6 (Deep Graph) và Chương 7 (Multi-Agent Systems).")"""

    new_intro_org = """    add_h2("6. Bố Cục Báo Cáo Tiểu Luận")
    add_p("Báo cáo tiểu luận được tổ chức gồm 5 chương chuyên sâu toàn diện và phần tổng kết định hướng tương lai:")
    add_bullet("Phần Mở đầu: Đặt vấn đề, tính cấp thiết, mục tiêu và phương pháp nghiên cứu.")
    add_bullet("Chương 1: Lịch sử phát triển Trí tuệ Nhân tạo - Toàn cảnh các giai đoạn thăng trầm, các bước chuyển mình mô thức (Paradigm Shifts) và 3 bộ dữ liệu kinh điển đặt nền móng AI.")
    add_bullet("Chương 2: Các kỹ thuật Machine Learning cơ bản - Cơ sở toán học, khảo sát 3 bộ dữ liệu tabular (Diabetes, Housing, Wine), cài đặt chi tiết 3 phiên bản Scratch-Keras-PyTorch, thực nghiệm so sánh và triển khai REST API.")
    add_bullet("Chương 3: Mạng nơ-ron Tích chập (CNN) - Toán học tích chập, Pooling, ResNet, SE-Block, khảo sát 3 bộ dữ liệu thị giác (MNIST, Fashion-MNIST, CIFAR-10), cài đặt 3 phiên bản, ma trận nhầm lẫn và triển khai ONNX API.")
    add_bullet("Chương 4: Mạng nơ-ron Hồi quy (RNN) - Bản chất chuỗi, Vanilla RNN, BPTT, bài toán triệt tiêu gradient, LSTM, GRU, khảo sát 3 bộ dữ liệu chuỗi (Gold Prices, Jena Climate, IMDb), cài đặt 3 phiên bản, dự báo đa bước và dashboard triển khai.")
    add_bullet("Chương 5: Knowledge Graph và RAG (Retrieval-Augmented Generation) - Bản thể học, Neo4j, Cypher, TransE, Vector RAG, Hybrid Search, GraphRAG, và hai hệ thống thực tế hoàn chỉnh cho Bệnh Tiểu đường (kết nối ML Chương 2) và Tài chính (kết nối LSTM Chương 4).")
    add_bullet("Phần Kết luận: Tổng kết toàn diện Chương 1 đến Chương 5 và Lộ trình mở rộng sang Chương 6 (Deep Graph Neural Networks) và Chương 7 (Intelligent Multi-Agent Systems).")"""

    assert old_intro_org in src, "old_intro_org not found"
    src = src.replace(old_intro_org, new_intro_org, 1)

    # 7. Replace old conclusion & references with Chapter 5 + updated conclusion + extended references
    # Let's find the split point right after Hình 4.6
    landmark = 'add_image_figure(os.path.join(plots_dir, \'fig_4_6_autoregressive_api.png\'),'
    assert landmark in src, "landmark fig_4_6 not found"
    
    # We find doc.add_page_break() after fig_4_6
    idx_fig = src.find(landmark)
    idx_pb = src.find("doc.add_page_break()", idx_fig)
    assert idx_pb != -1, "page break after fig_4_6 not found"
    
    body_before_ch5 = src[:idx_pb + len("doc.add_page_break()")]
    
    new_tail = """

    # -------------------------------------------------------------
    # CHƯƠNG 5, TỔNG KẾT VÀ TÀI LIỆU THAM KHẢO MỞ RỘNG
    # -------------------------------------------------------------
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
    
    print("[*] Đang ghi nội dung CHƯƠNG 5: Knowledge Graph và RAG...")
    add_chapter_5(doc, plots_dir, helpers)
    
    print("[*] Đang ghi phần TỔNG KẾT VÀ ĐỊNH HƯỚNG GIAI ĐOẠN TIẾP THEO...")
    add_updated_conclusion(doc, plots_dir, helpers)
    
    print("[*] Đang ghi 30 TÀI LIỆU THAM KHẢO chuẩn IEEE...")
    add_h1("TÀI LIỆU THAM KHẢO")
    references = get_extended_references()
    for ref in references:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Cm(0.8)
        p_r.paragraph_format.first_line_indent = Cm(-0.8)
        p_r.paragraph_format.space_after = Pt(3)
        p_r.paragraph_format.line_spacing = 1.15
        r = p_r.add_run(sanitize_text(ref))
        r.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # LƯU TÀI LIỆU WORD TIEULUAN02
    # -------------------------------------------------------------
    out_docx_1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tieuluan02_06_15_taint.docx')
    doc.save(out_docx_1)
    print(f"[+] Đã lưu thành công tệp Word tại: {out_docx_1}")

    out_docx_2 = os.path.join(os.path.dirname(__file__), 'tieuluan02_06_15_taint.docx')
    shutil.copyfile(out_docx_1, out_docx_2)
    print(f"[+] Bản sao lưu trữ tại: {out_docx_2}")

if __name__ == '__main__':
    build_tieuluan02()
"""

    full_tieuluan02_code = body_before_ch5 + new_tail

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(full_tieuluan02_code)

    print(f"[+] Đã tạo thành công {dst_path} với kích thước {len(full_tieuluan02_code)} ký tự!")

if __name__ == '__main__':
    main()
