# -*- coding: utf-8 -*-
"""
Script to create chapters_1_to_4_content.py from build_tieuluan03_from_tl02.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tieuluan_experiments/build_tieuluan03_from_tl02.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def get_block(start_idx, end_idx):
    block = []
    for l in lines[start_idx:end_idx]:
        if l.startswith('    '):
            block.append(l[4:])
        else:
            block.append(l)
    return ''.join(block)

header = '''# -*- coding: utf-8 -*-
"""
Nội dung Phần Mở Đầu và các Chương 1, 2, 3, 4
Trích xuất từ công trình thực nghiệm của sinh viên Nguyễn Tuấn Tài (B23DCCN731)
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

'''

helper_unpack = '''    add_h1 = helpers['add_h1']
    add_h2 = helpers['add_h2']
    add_h3 = helpers['add_h3']
    add_p = helpers['add_p']
    add_bullet = helpers['add_bullet']
    add_formula = helpers['add_formula']
    add_image_figure = helpers['add_image_figure']
    add_code_listing = helpers['add_code_listing']
    format_table_header_data = helpers['format_table_header_data']
    sanitize_text = helpers['sanitize_text']

'''

intro_body = '''    add_h1("PHẦN MỞ ĐẦU")
    
    add_h2("1. Tính Cấp Thiết của Đề Tài")
    add_p("Trong thập kỷ thứ ba của thế kỷ XXI, Trí tuệ Nhân tạo (Artificial Intelligence - AI) và Học sâu (Deep Learning - DL) đã bứt phá mạnh mẽ khỏi phạm vi các phòng thí nghiệm hàn lâm để trở thành động lực công nghệ cốt lõi định hình lại toàn bộ nền kinh tế số toàn cầu. Từ các hệ thống phân loại y sinh học tự động hỗ trợ chẩn đoán sớm bệnh hiểm nghèo, các thuật toán thị giác máy tính nhận dạng vật thể trong xe tự hành, cho đến các mô hình dự báo chuỗi thời gian tài chính phức tạp, AI đang chứng minh năng lực vượt trội trong việc tự động trích xuất các tri thức tiềm ẩn từ dữ liệu lớn (Big Data).")
    add_p("Tuy nhiên, trong quá trình đào tạo và tiếp cận công nghệ thông minh, một rào cản phổ biến mà sinh viên và các kỹ sư phần mềm thường gặp phải là hội chứng 'hộp đen' (Black-box problem) và xu hướng 'vibe coding' – chỉ sử dụng các thư viện cấp cao (như scikit-learn, Keras) mà không nắm vững bản chất toán học giải tích, đạo hàm ma trận và động lực học tối ưu hóa diễn ra bên dưới. Điều này dẫn đến sự bế tắc khi mô hình gặp lỗi quá khớp (Overfitting), triệt tiêu gradient (Vanishing Gradient) hoặc khi cần tối ưu hóa hiệu năng tính toán trên các thiết bị biên hạn chế tài nguyên.")
    add_p("Bên cạnh đó, việc xây dựng một hệ thống thông minh hoàn chỉnh không chỉ dừng lại ở việc huấn luyện mô hình đạt chỉ số đo lường cao trong môi trường Jupyter Notebook tĩnh, mà mục tiêu tối hậu là phải hoàn thiện toàn bộ vòng đời phát triển hệ thống (System Lifecycle): từ khâu hiểu bản chất và biểu diễn dữ liệu (Data Representation), làm sạch và phân tích khám phá (EDA), huấn luyện mô hình toán học giải tích từ đầu (Scratch), đối sánh với các framework công nghiệp (Keras, PyTorch), và cuối cùng là đóng gói, tối ưu hóa suy luận và triển khai (Deployment) thành một dịch vụ Web/API sẵn sàng phục vụ người dùng cuối.")

    add_h2("2. Mục Tiêu Nghiên Cứu và Nhiệm Vụ Trọng Tâm")
    add_p("Tiểu luận này hướng tới các mục tiêu nghiên cứu và nhiệm vụ trọng tâm sau:")
    add_bullet("Mục tiêu 1: Hệ thống hóa toàn diện tiến trình lịch sử phát triển của AI: Làm rõ các cột mốc thăng trầm lịch sử từ thời kỳ phôi thai (1940s), hai Mùa đông AI, thời kỳ phục hưng của Machine Learning thống kê, cuộc cách mạng Deep Learning, cho đến kỷ nguyên Transformer, AI tạo sinh và Hệ đa Tác tử hiện đại.")
    add_bullet("Mục tiêu 2: Làm chủ bản chất toán học và thuật toán qua 3 phương thức cài đặt: Đối với từng lớp bài toán (Machine Learning cơ bản, Mạng nơ-ron tích chập CNN, và Mạng nơ-ron hồi quy RNN), thực hiện cài đặt song song 3 phiên bản mã nguồn: (1) Cài đặt thuần từ đầu (Scratch Implementation bằng NumPy) để hiểu rõ từng phép đạo hàm giải tích; (2) Cài đặt trên TensorFlow/Keras đại diện cho thiết kế trực quan công nghiệp; (3) Cài đặt trên PyTorch đại diện cho kiến trúc động linh hoạt chuẩn nghiên cứu khoa học.")
    add_bullet("Mục tiêu 3: Khảo sát sâu sắc các bộ dữ liệu đa dạng (Multi-domain Datasets): Trong mỗi chương, tiến hành khảo sát từ 2 đến 3 bộ dữ liệu thực tế: cung cấp đường dẫn truy cập chuẩn, thông số kích thước (samples, features, dimensionality), trích xuất mẫu dữ liệu thực tế, phân tích phân bố thống kê (EDA), ma trận tương quan và nhận xét chuyên sâu về tính chất đại số của dữ liệu.")
    add_bullet("Mục tiêu 4: Đánh giá thực nghiệm và phân tích đối sánh đa chiều: Đo lường, so sánh định lượng giữa 3 mô hình trên các tập dữ liệu dựa trên hệ thống chỉ số toàn diện (Accuracy, Precision, Recall, F1-Score, Loss, Training Time, Inference Latency, FLOPs), vẽ biểu đồ đường cong học tập và phân tích nguyên nhân sai số.")
    add_bullet("Mục tiêu 5: Thiết kế kiến trúc triển khai sản phẩm thực tế (Deployment): Hiện thực hóa mô hình thành dịch vụ phần mềm có thể phục vụ trong thực tế thông qua việc đóng gói mô hình (Serialization / ONNX), xây dựng REST API thời gian thực với FastAPI và chuẩn hóa quy trình MLOps.")
    add_bullet("Mục tiêu 6: Khai phá các kiến trúc tiên tiến (KG, GNN, MAS): Xây dựng cơ sở tri thức Đồ thị kết hợp RAG (Chương 5), Mạng nơ-ron Đồ thị sâu Deep Graph (Chương 6) và Hệ đa Tác tử Thông minh Multi-Agent Systems (Chương 7) ứng dụng trong chẩn đoán y tế và phân tích tài chính.")

    add_h2("3. Đối Tượng và Phạm Vi Nghiên Cứu")
    add_p("Đối tượng nghiên cứu của tiểu luận bao gồm: các nguyên lý biểu diễn dữ liệu số học; các mô hình học máy kinh điển (Linear Regression, Logistic Regression, SVM, Random Forest); kiến trúc mạng nơ-ron tích chập (CNN) cùng các khối cải tiến hiện đại (Residual Connection, Squeeze-and-Excitation); kiến trúc mạng nơ-ron hồi quy (Vanilla RNN, LSTM, GRU) cho chuỗi thời gian; cơ sở tri thức đồ hình (Knowledge Graph), RAG & GraphRAG; mạng nơ-ron đồ thị sâu (Deep Graph / GNNs); và hệ đa tác tử thông minh (Multi-Agent Systems).")
    add_p("Phạm vi nghiên cứu bao quát toàn diện toàn bộ 7 chương chuyên sâu theo đề cương học phần Phát triển Hệ thống Thông minh do PGS. TS. Trần Đình Quế trực tiếp giảng dạy tại Học viện Công nghệ Bưu chính Viễn thông (PTIT), kết hợp chặt chẽ giữa nghiên cứu giải tích toán học, lập trình từ đầu (Scratch Implementation), thực nghiệm trên framework (Keras, PyTorch, Neo4j, PyG) và đóng gói triển khai microservices thực tế.")

    add_h2("4. Phương Pháp Luận và Cách Tiếp Cận Nghiên Cứu")
    add_p("Tiểu luận áp dụng phương pháp luận kết hợp chặt chẽ giữa nghiên cứu lý thuyết giải tích và thực nghiệm khoa học dựa trên số liệu thực tế:")
    add_bullet("1. Lý thuyết: Phương pháp giải tích toán học: Thiết lập các bài toán tối ưu dưới dạng hàm mục tiêu (Objective Function), khai triển đạo hàm riêng giải tích theo từng ma trận trọng số và vector độ lệch thông qua quy tắc chuỗi (Chain Rule).")
    add_bullet("2. Thực nghiệm: Phương pháp lập trình thực nghiệm đối chứng: Thiết lập môi trường tính toán đồng nhất (cùng random seed, cùng tỷ lệ chia tập Train/Validation/Test, cùng cấu hình tiền xử lý chuẩn hóa dữ liệu Standard Scaler) để đảm bảo tính tái lập (Reproducibility) và tính công bằng tuyệt đối giữa 3 phương thức cài đặt (Scratch vs Keras vs PyTorch).")
    add_bullet("3. Triển khai: Phương pháp kỹ nghệ phần mềm và MLOps: Áp dụng kiến trúc microservices phân tách giữa tầng tiền xử lý dữ liệu, tầng mô hình tính toán và tầng giao diện lập trình ứng dụng RESTful API.")

    add_h2("5. Ý Nghĩa Khoa Học và Giá Trị Thực Tiễn")
    add_p("Về mặt khoa học: Báo cáo cung cấp một tài liệu tham khảo hệ thống, chuẩn mực và chi tiết, kết nối một cách liền mạch giữa lý thuyết giải tích toán học trừu tượng với các dòng mã nguồn thực thi cụ thể, giúp xóa bỏ hoàn toàn tính chất 'hộp đen' của các mô hình học sâu.")
    add_p("Về mặt thực tiễn: Toàn bộ các bộ dữ liệu khảo sát đều lấy từ các nguồn thực tế uy tín thế giới (chẩn đoán y sinh học, dự báo giá bất động sản, thị giác nhận dạng vật thể, và chuỗi tài chính giao dịch vàng/bạc quốc tế). Các mã nguồn triển khai REST API cung cấp một khuôn mẫu (Template) hoàn chỉnh sẵn sàng cho việc đóng gói vào các giải pháp phần mềm doanh nghiệp.")

    add_h2("6. Bố Cục Báo Cáo Tiểu Luận")
    add_p("Báo cáo tiểu luận được tổ chức gồm 7 chương chuyên sâu toàn diện và phần kết luận:")
    add_bullet("Phần Mở đầu: Đặt vấn đề, tính cấp thiết, mục tiêu và phương pháp nghiên cứu.")
    add_bullet("Chương 1: Lịch sử phát triển Trí tuệ Nhân tạo - Toàn cảnh các giai đoạn thăng trầm, các bước chuyển mình mô thức (Paradigm Shifts) và 3 bộ dữ liệu kinh điển đặt nền móng AI.")
    add_bullet("Chương 2: Các kỹ thuật Machine Learning cơ bản - Cơ sở toán học, khảo sát 3 bộ dữ liệu tabular (Diabetes, Housing, Wine), cài đặt chi tiết 3 phiên bản Scratch-Keras-PyTorch, thực nghiệm so sánh và triển khai REST API.")
    add_bullet("Chương 3: Mạng nơ-ron Tích chập (CNN) - Toán học tích chập, Pooling, ResNet, SE-Block, khảo sát 3 bộ dữ liệu thị giác (MNIST, Fashion-MNIST, CIFAR-10), cài đặt 3 phiên bản, ma trận nhầm lẫn và triển khai ONNX API.")
    add_bullet("Chương 4: Mạng nơ-ron Hồi quy (RNN) - Bản chất chuỗi, Vanilla RNN, BPTT, bài toán triệt tiêu gradient, LSTM, GRU, khảo sát 3 bộ dữ liệu chuỗi (Gold Prices, Jena Climate, IMDb), cài đặt 3 phiên bản, dự báo đa bước và dashboard triển khai.")
    add_bullet("Chương 5: Knowledge Graph và RAG (Retrieval-Augmented Generation) - Bản thể học, Neo4j, Cypher, TransE, Vector RAG, Hybrid Search, GraphRAG, và hai hệ thống thực tế hoàn chỉnh cho Bệnh Tiểu đường (kết nối ML Chương 2) và Tài chính (kết nối LSTM Chương 4).")
    add_bullet("Chương 6: Học sâu trên Đồ thị (Deep Graph & Graph Neural Networks) - Lý thuyết phổ đồ thị, Laplacian, khung truyền tin MPNN, 3 kiến trúc kinh điển GCN, GraphSAGE, GAT, thực nghiệm phân loại nguy cơ bệnh nhân và dự báo rủi ro vĩ mô, cùng dịch vụ Deep Graph Microservice tích hợp GraphRAG.")
    add_bullet("Chương 7: Hệ đa Tác tử Thông minh (Multi-Agent Systems - MAS) - Mô hình PEAS, cơ chế phối hợp và giao tiếp đa tác tử, Q-Learning, Rule-based agent, mô phỏng 10.000 tập huấn luyện, phân tích độ nhạy siêu tham số và đề xuất kiến trúc hệ đa tác tử cho chẩn đoán đái tháo đường.")
    add_bullet("Phần Kết luận: Tổng kết toàn diện Chương 1 đến Chương 7 và Định hướng nghiên cứu phát triển tương lai.")
    add_bullet("Tài liệu tham khảo: Danh mục 25 tài liệu chuẩn học thuật quốc tế IEEE.")
'''

# Get original blocks from build_tieuluan03_from_tl02.py
def indent_code(block_str):
    res = []
    for line in block_str.split('\n'):
        if line.strip():
            res.append('    ' + line)
        else:
            res.append('')
    return '\n'.join(res)

ch1_raw = get_block(526, 613)
ch2_raw = get_block(613, 844)
ch3_raw = get_block(844, 1090)
ch4_raw = get_block(1090, 1307)

with open('tieuluan_experiments/chapters_1_to_4_content.py', 'w', encoding='utf-8') as out:
    out.write(header)
    out.write('def add_intro(doc, helpers):\n' + helper_unpack + intro_body + '\n\n')
    out.write('def add_chapter_1(doc, plots_dir, helpers):\n' + helper_unpack + indent_code(ch1_raw) + '\n\n')
    out.write('def add_chapter_2(doc, plots_dir, helpers):\n' + helper_unpack + indent_code(ch2_raw) + '\n\n')
    out.write('def add_chapter_3(doc, plots_dir, helpers):\n' + helper_unpack + indent_code(ch3_raw) + '\n\n')
    out.write('def add_chapter_4(doc, plots_dir, helpers):\n' + helper_unpack + indent_code(ch4_raw) + '\n\n')

print('Generated tieuluan_experiments/chapters_1_to_4_content.py successfully!')

