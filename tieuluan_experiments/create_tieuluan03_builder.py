import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    src_path = os.path.join(os.path.dirname(__file__), 'build_tieuluan02_docx.py')
    dst_path = os.path.join(os.path.dirname(__file__), 'build_tieuluan03_from_tl02.py')

    with open(src_path, 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Update imports
    old_import = "from chapter5_content import add_chapter_5, add_updated_conclusion, get_extended_references"
    new_import = """from chapter5_content import add_chapter_5
from chapter6_content import add_chapter_6, add_updated_conclusion_ch6, get_extended_references_ch6"""
    assert old_import in src, "old_import not found"
    src = src.replace(old_import, new_import, 1)

    # 2. Update print and function names
    src = src.replace("tieuluan02_06_15_taint.docx", "tieuluan03_06_15_taint.docx")
    src = src.replace("def build_tieuluan02():", "def build_tieuluan03():")
    src = src.replace("build_tieuluan02()", "build_tieuluan03()")
    src = src.replace("BẮT ĐẦU TẠO TIỂU LUẬN 01", "BẮT ĐẦU TẠO TIỂU LUẬN 03")

    # 3. Update cover page
    old_title = 'r_title = p_title.add_run("TIỂU LUẬN MÔN HỌC (BÁO CÁO TOÀN DIỆN MỞ ĐẦU ĐẾN CHƯƠNG 5)\\n")'
    new_title = 'r_title = p_title.add_run("TIỂU LUẬN MÔN HỌC (BÁO CÁO TOÀN DIỆN MỞ ĐẦU ĐẾN CHƯƠNG 6)\\n")'
    assert old_title in src, "old_title not found"
    src = src.replace(old_title, new_title, 1)

    old_topic = 'r_tp = p_topic.add_run("ĐỀ TÀI: NGHIÊN CỨU LÝ THUYẾT, THỰC NGHIỆM ĐỐI SÁNH\\nVÀ TRIỂN KHAI HỆ THỐNG THÔNG MINH\\n(TỪ MACHINE LEARNING, CNN, RNN ĐẾN KNOWLEDGE GRAPH VÀ RAG PIPELINE)")'
    new_topic = 'r_tp = p_topic.add_run("ĐỀ TÀI: NGHIÊN CỨU LÝ THUYẾT, THỰC NGHIỆM ĐỐI SÁNH\\nVÀ TRIỂN KHAI HỆ THỐNG THÔNG MINH\\n(TỪ MACHINE LEARNING, CNN, RNN, KNOWLEDGE GRAPH ĐẾN DEEP GRAPH NEURAL NETWORKS)")'
    assert old_topic in src, "old_topic not found"
    src = src.replace(old_topic, new_topic, 1)

    # 4. Update TOC
    old_toc_tail = """        ("CHƯƠNG 5: KNOWLEDGE GRAPH VÀ RAG (RETRIEVAL-AUGMENTED GENERATION)", "49"),
        ("  5.1 Mở Đầu (KG & RAG: Timeline Lịch sử và Ý nghĩa Sống còn trong AI)", "49"),
        ("  5.2 Knowledge Graph - Cơ Sở Tri Thức Đồ Hình (Knowledge Base)", "51"),
        ("  5.3 Kỹ Thuật Truy Xuất Tăng Cường Sinh Văn Bản (RAG)", "54"),
        ("  5.4 Cơ Sở Tri Thức và RAG Cho Bệnh Tiểu Đường (Diabetes Healthcare)", "58"),
        ("  5.5 Cơ Sở Tri Thức và RAG Cho Phân Tích Tài Chính (Chứng Khoán & Vàng)", "62"),
        ("  5.6 Triển Khai Hệ Thống Thực Tế (Deployment Pipeline)", "65"),
        ("TỔNG KẾT VÀ ĐỊNH HƯỚNG GIAI ĐOẠN TIẾP THEO (GNN & MULTI-AGENT)", "68"),
        ("TÀI LIỆU THAM KHẢO", "70")
    ]"""

    new_toc_tail = """        ("CHƯƠNG 5: KNOWLEDGE GRAPH VÀ RAG (RETRIEVAL-AUGMENTED GENERATION)", "49"),
        ("  5.1 Mở Đầu (KG & RAG: Timeline Lịch sử và Ý nghĩa Sống còn trong AI)", "49"),
        ("  5.2 Knowledge Graph - Cơ Sở Tri Thức Đồ Hình (Knowledge Base)", "51"),
        ("  5.3 Kỹ Thuật Truy Xuất Tăng Cường Sinh Văn Bản (RAG)", "54"),
        ("  5.4 Cơ Sở Tri Thức và RAG Cho Bệnh Tiểu Đường (Diabetes Healthcare)", "58"),
        ("  5.5 Cơ Sở Tri Thức và RAG Cho Phân Tích Tài Chính (Chứng Khoán & Vàng)", "62"),
        ("  5.6 Triển Khai Hệ Thống Thực Tế (Deployment Pipeline)", "65"),
        ("CHƯƠNG 6: HỌC SÂU TRÊN ĐỒ THỊ (DEEP GRAPH & GRAPH NEURAL NETWORKS)", "68"),
        ("  6.1 Tổng Quan và Tính Cấp Thiết của Deep Graph", "68"),
        ("  6.2 Cơ Sở Toán Học của Học Biểu Diễn Đồ Thị", "70"),
        ("  6.3 Khung Truyền Thông Điệp Tổng Quát (MPNN)", "72"),
        ("  6.4 Các Kiến Trúc GNN Tiêu Biểu (GCN, GraphSAGE, GAT)", "74"),
        ("  6.5 Thực Nghiệm Deep Graph Trên Bài Toán Thực Tế", "78"),
        ("  6.6 Đánh Giá Đối Sánh Hiệu Năng Thực Nghiệm", "82"),
        ("  6.7 Triển Khai Dịch Vụ Deep Graph Microservice và Tích Hợp GraphRAG", "84"),
        ("  6.8 Tiểu Kết Chương 6", "86"),
        ("TỔNG KẾT VÀ ĐỊNH HƯỚNG GIAI ĐOẠN TIẾP THEO (CHƯƠNG 7: MULTI-AGENT)", "87"),
        ("TÀI LIỆU THAM KHẢO", "89")
    ]"""
    assert old_toc_tail in src, "old_toc_tail not found"
    src = src.replace(old_toc_tail, new_toc_tail, 1)

    # 5. Update Abbreviations
    old_abbr_tail = """        ("GAT", "Graph Attention Network", "Mạng Chú ý Đồ thị"),
        ("GCN", "Graph Convolutional Network", "Mạng Tích chập Đồ thị")
    ]"""
    new_abbr_tail = """        ("GAT", "Graph Attention Network", "Mạng Chú ý Đồ thị"),
        ("GCN", "Graph Convolutional Network", "Mạng Tích chập Đồ thị"),
        ("GNN", "Graph Neural Network", "Mạng Nơ-ron Đồ thị"),
        ("MPNN", "Message Passing Neural Network", "Mạng Nơ-ron Truyền Thông điệp"),
        ("GraphSAGE", "Sample and Aggregate", "Mạng Lấy mẫu và Tổng hợp Đồ thị"),
        ("PyG", "PyTorch Geometric", "Thư viện Học sâu Đồ thị trên PyTorch"),
        ("Inductive", "Inductive Representation Learning", "Học Biểu diễn Quy nạp trên Đồ thị")
    ]"""
    assert old_abbr_tail in src, "old_abbr_tail not found"
    src = src.replace(old_abbr_tail, new_abbr_tail, 1)

    # 6. Update Introduction text about report organization
    old_intro_org = """    add_h2("6. Bố Cục Báo Cáo Tiểu Luận")
    add_p("Báo cáo tiểu luận được tổ chức gồm 5 chương chuyên sâu toàn diện và phần tổng kết định hướng tương lai:")
    add_bullet("Phần Mở đầu: Đặt vấn đề, tính cấp thiết, mục tiêu và phương pháp nghiên cứu.")
    add_bullet("Chương 1: Lịch sử phát triển Trí tuệ Nhân tạo - Toàn cảnh các giai đoạn thăng trầm, các bước chuyển mình mô thức (Paradigm Shifts) và 3 bộ dữ liệu kinh điển đặt nền móng AI.")
    add_bullet("Chương 2: Các kỹ thuật Machine Learning cơ bản - Cơ sở toán học, khảo sát 3 bộ dữ liệu tabular (Diabetes, Housing, Wine), cài đặt chi tiết 3 phiên bản Scratch-Keras-PyTorch, thực nghiệm so sánh và triển khai REST API.")
    add_bullet("Chương 3: Mạng nơ-ron Tích chập (CNN) - Toán học tích chập, Pooling, ResNet, SE-Block, khảo sát 3 bộ dữ liệu thị giác (MNIST, Fashion-MNIST, CIFAR-10), cài đặt 3 phiên bản, ma trận nhầm lẫn và triển khai ONNX API.")
    add_bullet("Chương 4: Mạng nơ-ron Hồi quy (RNN) - Bản chất chuỗi, Vanilla RNN, BPTT, bài toán triệt tiêu gradient, LSTM, GRU, khảo sát 3 bộ dữ liệu chuỗi (Gold Prices, Jena Climate, IMDb), cài đặt 3 phiên bản, dự báo đa bước và dashboard triển khai.")
    add_bullet("Chương 5: Knowledge Graph và RAG (Retrieval-Augmented Generation) - Bản thể học, Neo4j, Cypher, TransE, Vector RAG, Hybrid Search, GraphRAG, và hai hệ thống thực tế hoàn chỉnh cho Bệnh Tiểu đường (kết nối ML Chương 2) và Tài chính (kết nối LSTM Chương 4).")
    add_bullet("Phần Kết luận: Tổng kết toàn diện Chương 1 đến Chương 5 và Lộ trình mở rộng sang Chương 6 (Deep Graph Neural Networks) và Chương 7 (Intelligent Multi-Agent Systems).")"""

    new_intro_org = """    add_h2("6. Bố Cục Báo Cáo Tiểu Luận")
    add_p("Báo cáo tiểu luận được tổ chức gồm 6 chương chuyên sâu toàn diện và phần tổng kết định hướng tương lai:")
    add_bullet("Phần Mở đầu: Đặt vấn đề, tính cấp thiết, mục tiêu và phương pháp nghiên cứu.")
    add_bullet("Chương 1: Lịch sử phát triển Trí tuệ Nhân tạo - Toàn cảnh các giai đoạn thăng trầm, các bước chuyển mình mô thức (Paradigm Shifts) và 3 bộ dữ liệu kinh điển đặt nền móng AI.")
    add_bullet("Chương 2: Các kỹ thuật Machine Learning cơ bản - Cơ sở toán học, khảo sát 3 bộ dữ liệu tabular (Diabetes, Housing, Wine), cài đặt chi tiết 3 phiên bản Scratch-Keras-PyTorch, thực nghiệm so sánh và triển khai REST API.")
    add_bullet("Chương 3: Mạng nơ-ron Tích chập (CNN) - Toán học tích chập, Pooling, ResNet, SE-Block, khảo sát 3 bộ dữ liệu thị giác (MNIST, Fashion-MNIST, CIFAR-10), cài đặt 3 phiên bản, ma trận nhầm lẫn và triển khai ONNX API.")
    add_bullet("Chương 4: Mạng nơ-ron Hồi quy (RNN) - Bản chất chuỗi, Vanilla RNN, BPTT, bài toán triệt tiêu gradient, LSTM, GRU, khảo sát 3 bộ dữ liệu chuỗi (Gold Prices, Jena Climate, IMDb), cài đặt 3 phiên bản, dự báo đa bước và dashboard triển khai.")
    add_bullet("Chương 5: Knowledge Graph và RAG (Retrieval-Augmented Generation) - Bản thể học, Neo4j, Cypher, TransE, Vector RAG, Hybrid Search, GraphRAG, và hai hệ thống thực tế hoàn chỉnh cho Bệnh Tiểu đường (kết nối ML Chương 2) và Tài chính (kết nối LSTM Chương 4).")
    add_bullet("Chương 6: Học sâu trên Đồ thị (Deep Graph & Graph Neural Networks) - Lý thuyết phổ đồ thị, Laplacian, khung truyền tin MPNN, 3 kiến trúc kinh điển GCN, GraphSAGE, GAT, thực nghiệm phân loại nguy cơ bệnh nhân và dự báo rủi ro vĩ mô, cùng dịch vụ Deep Graph Microservice tích hợp GraphRAG.")
    add_bullet("Phần Kết luận: Tổng kết toàn diện Chương 1 đến Chương 6 và Lộ trình mở rộng sang Chương 7 (Intelligent Multi-Agent Systems).")"""
    assert old_intro_org in src, "old_intro_org not found"
    src = src.replace(old_intro_org, new_intro_org, 1)

    # 7. Update Chapter 5 + 6 invocation in tail
    old_call_ch5 = """    print("[*] Đang ghi nội dung CHƯƠNG 5: Knowledge Graph và RAG...")
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
        r.font.size = Pt(10.5)"""

    new_call_ch5_ch6 = """    print("[*] Đang ghi nội dung CHƯƠNG 5: Knowledge Graph và RAG...")
    add_chapter_5(doc, plots_dir, helpers)

    print("[*] Đang ghi nội dung CHƯƠNG 6: Deep Graph và Graph Neural Networks...")
    add_chapter_6(doc, plots_dir, helpers)
    
    print("[*] Đang ghi phần TỔNG KẾT VÀ ĐỊNH HƯỚNG GIAI ĐOẠN TIẾP THEO (CHƯƠNG 7 MAS)...")
    add_updated_conclusion_ch6(doc, plots_dir, helpers)
    
    print("[*] Đang ghi TÀI LIỆU THAM KHẢO chuẩn IEEE (Bao gồm GNN)...")
    add_h1("TÀI LIỆU THAM KHẢO")
    references = get_extended_references_ch6()
    for ref_title, ref_url in references:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Cm(0.8)
        p_r.paragraph_format.first_line_indent = Cm(-0.8)
        p_r.paragraph_format.space_after = Pt(3)
        p_r.paragraph_format.line_spacing = 1.15
        r = p_r.add_run(sanitize_text(f"{ref_title} Truy cập: {ref_url}"))
        r.font.size = Pt(10.5)"""

    assert old_call_ch5 in src, "old_call_ch5 not found"
    src = src.replace(old_call_ch5, new_call_ch5_ch6, 1)

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(src)

    print(f"[+] Đã tạo thành công {dst_path} với kích thước {len(src)} ký tự!")

if __name__ == '__main__':
    main()
