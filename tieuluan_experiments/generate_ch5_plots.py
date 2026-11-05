import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle
import seaborn as sns

# Set academic plotting style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'plots')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("[*] Bắt đầu sinh 8 biểu đồ học thuật cho Chương 5: Knowledge Graph và RAG...")

# ==============================================================================
# HÌNH 5.1: TIẾN TRÌNH LỊCH SỬ KNOWLEDGE GRAPH & RAG (2001 - 2026)
# ==============================================================================
def plot_fig_5_1():
    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    milestones = [
        (2001, "Semantic Web", "Berners-Lee: RDF, OWL,\nWeb ngữ nghĩa dữ liệu liên kết"),
        (2012, "Google KG", "Things not Strings:\nĐồ thị tri thức tìm kiếm"),
        (2013, "TransE & Word2Vec", "Bordes et al.: Nhúng bộ ba\ntri thức vào không gian vector"),
        (2017, "Transformer", "Vaswani et al.: Kiến trúc Attention\nkhai mở kỷ nguyên LLM"),
        (2020, "Vector RAG", "Lewis et al. (Meta AI):\nRetrieval-Augmented Gen."),
        (2022, "LangChain & LlamaIndex", "Framework tích hợp LLM,\nVector Stores & Orchestration"),
        (2023, "Vector DBs Bùng nổ", "Chroma, Milvus, Pinecone:\nLưu trữ & tìm kiếm tương đồng"),
        (2024, "GraphRAG (Microsoft)", "Kết hợp KG và LLM:\nSuy luận toàn cục đa bước"),
        (2026, "Agentic GraphRAG", "Tác tử tự chủ khai thác KG\nvà kiểm chứng chống ảo giác")
    ]
    
    ax.axhline(0, color='#1A365D', lw=3.5, zorder=1)
    
    for i, (yr, title, desc) in enumerate(milestones):
        y_pos = 1.35 if i % 2 == 0 else -1.35
        color = '#2B6CB0' if yr <= 2017 else ('#2C7A7B' if yr <= 2023 else '#D69E2E')
        
        ax.scatter(yr, 0, color=color, s=140, zorder=3, edgecolors='white', lw=2)
        ax.plot([yr, yr], [0, y_pos * 0.75], color='#718096', lw=1.2, ls='--')
        
        box_bg = '#EBF8FF' if yr <= 2017 else ('#E6FFFA' if yr <= 2023 else '#FEFCBF')
        ax.text(yr, y_pos * 0.88, f"{yr}\n{title}\n({desc})", 
                ha='center', va='center',
                fontsize=7.8, weight='bold',
                bbox=dict(boxstyle='round,pad=0.35', facecolor=box_bg, edgecolor=color, lw=1.3))
                
    ax.set_xlim(1999, 2028)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')
    ax.set_title("HÌNH 5.1: TIẾN TRÌNH LỊCH SỬ PHÁT TRIỂN KNOWLEDGE GRAPH VÀ RAG (2001 - 2026)", fontsize=11, pad=18)
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_5_1_kg_rag_timeline.png')
    plt.savefig(out_path)
    plt.close()
    print(f"  [+] Đã tạo: {out_path}")

# ==============================================================================
# HÌNH 5.2: BỘ BA TRI THỨC VÀ LƯỢC ĐỒ PROPERTY GRAPH NEO4J
# ==============================================================================
def plot_fig_5_2():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))
    
    # Subplot 1: Mô hình Bộ ba Tri thức RDF (Subject - Predicate - Object)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title("(a) Mô hình Bộ ba Tri thức RDF: (s, p, o)", fontsize=11, weight='bold', pad=10)
    
    # Subject Node
    sub_box = FancyBboxPatch((0.5, 6.0), 3.0, 2.2, boxstyle="round,pad=0.2", fc="#BEE3F8", ec="#2B6CB0", lw=2)
    ax1.add_patch(sub_box)
    ax1.text(2.0, 7.5, "Chủ thể (Subject)\n:Disease\n'Đái tháo đường T2'", ha='center', va='center', fontsize=9, weight='bold')
    
    # Object Node
    obj_box = FancyBboxPatch((6.5, 6.0), 3.0, 2.2, boxstyle="round,pad=0.2", fc="#C6F6D5", ec="#276749", lw=2)
    ax1.add_patch(obj_box)
    ax1.text(8.0, 7.5, "Khách thể (Object)\n:Medicine\n'Metformin 500mg'", ha='center', va='center', fontsize=9, weight='bold')
    
    # Predicate Arrow
    ax1.annotate('', xy=(6.5, 7.1), xytext=(3.5, 7.1),
                 arrowprops=dict(arrowstyle="simple,tail_width=2,head_width=8,head_length=8",
                                 facecolor='#E53E3E', edgecolor='#9B2C2C', lw=1))
    ax1.text(5.0, 7.6, "Vị từ (Predicate)\n[TREATED_BY]", ha='center', va='center', fontsize=9.5, weight='bold', color='#9B2C2C')
    
    # Explanation
    formula_text = "Phát biểu hình thức:\n(Đái_tháo_đường_T2, TREATED_BY, Metformin)\nVector dịch chuyển TransE:  h + r ≈ t\nHàm tính điểm năng lượng:  f(h, r, t) = -||h + r - t||"
    ax1.text(5.0, 2.5, formula_text, ha='center', va='center', fontsize=9,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.5))
    
    # Subplot 2: Lược đồ Labeled Property Graph (LPG) trong Neo4j
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title("(b) Lược đồ Labeled Property Graph (LPG) Neo4j", fontsize=11, weight='bold', pad=10)
    
    # Node 1
    node1 = FancyBboxPatch((0.5, 5.0), 3.4, 3.6, boxstyle="round,pad=0.2", fc="#EBF8FF", ec="#3182CE", lw=2)
    ax2.add_patch(node1)
    ax2.text(2.2, 7.8, "Node Label: :Disease", ha='center', va='center', fontsize=9.5, weight='bold', color='#2B6CB0')
    ax2.text(2.2, 6.2, "id: 'dia_01'\nname: 'Đái tháo đường'\nicd_10: 'E11'\nchronic: true",
             ha='center', va='center', fontsize=8.5, family='monospace', bbox=dict(boxstyle='square', fc='white', ec='#CBD5E0'))
    
    # Node 2
    node2 = FancyBboxPatch((6.1, 5.0), 3.4, 3.6, boxstyle="round,pad=0.2", fc="#F0FFF4", ec="#38A169", lw=2)
    ax2.add_patch(node2)
    ax2.text(7.8, 7.8, "Node Label: :Medicine", ha='center', va='center', fontsize=9.5, weight='bold', color='#276749')
    ax2.text(7.8, 6.2, "id: 'med_01'\nname: 'Glucophage'\ningredient: 'Metformin'\nprice: 135000",
             ha='center', va='center', fontsize=8.5, family='monospace', bbox=dict(boxstyle='square', fc='white', ec='#CBD5E0'))
             
    # Relationship with properties
    ax2.annotate('', xy=(6.1, 6.8), xytext=(3.9, 6.8),
                 arrowprops=dict(arrowstyle="simple,tail_width=2,head_width=7,head_length=7",
                                 facecolor='#DD6B20', edgecolor='#C05621', lw=1))
    ax2.text(5.0, 7.2, "[:PRESCRIBED]", ha='center', va='center', fontsize=8.5, weight='bold', color='#C05621')
    ax2.text(5.0, 6.0, "{first_line: true,\ndosage: '500mg'}", ha='center', va='center', fontsize=7.5,
             family='monospace', bbox=dict(boxstyle='round,pad=0.2', fc='#FFFAF0', ec='#DD6B20'))

    # Cypher query illustration
    cypher_code = "Cypher Query:\nMATCH (d:Disease)-[r:PRESCRIBED]->(m:Medicine)\nWHERE d.icd_10 = 'E11'\nRETURN m.name, r.dosage, m.price"
    ax2.text(5.0, 2.0, cypher_code, ha='center', va='center', fontsize=8.5, family='monospace',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#2D3748', edgecolor='#1A202C', lw=1.5), color='#63B3ED')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_5_2_triple_property_graph.png')
    plt.savefig(out_path)
    plt.close()
    print(f"  [+] Đã tạo: {out_path}")

# ==============================================================================
# HÌNH 5.3: KIẾN TRÚC QUY TRÌNH VECTOR RAG TIÊU CHUẨN
# ==============================================================================
def plot_fig_5_3():
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Giai đoạn 1: Ingestion & Vector Storage (Trục trên)
    ax.text(0.5, 5.5, "PHẦN 1: INGESTION PIPELINE (OFFLINE BATCH)", fontsize=9.5, weight='bold', color='#2B6CB0')
    
    # Raw Docs
    b1 = FancyBboxPatch((0.5, 3.8), 1.8, 1.4, boxstyle="round,pad=0.15", fc="#EDF2F7", ec="#4A5568", lw=1.5)
    ax.add_patch(b1)
    ax.text(1.4, 4.5, "Tài liệu Y tế / Báo cáo\n(PDF, JSON, HTML)", ha='center', va='center', fontsize=8, weight='bold')
    
    # Chunking
    b2 = FancyBboxPatch((2.8, 3.8), 1.8, 1.4, boxstyle="round,pad=0.15", fc="#EBF8FF", ec="#3182CE", lw=1.5)
    ax.add_patch(b2)
    ax.text(3.7, 4.5, "Phân tách đoạn\nChunking\n(512 tok, 64 ovlp)", ha='center', va='center', fontsize=8, weight='bold')
    
    # Embedding
    b3 = FancyBboxPatch((5.1, 3.8), 2.0, 1.4, boxstyle="round,pad=0.15", fc="#FEFCBF", ec="#D69E2E", lw=1.5)
    ax.add_patch(b3)
    ax.text(6.1, 4.5, "Mô hình Nhúng\n(text-embedding-3\n/ PhoBERT-base)", ha='center', va='center', fontsize=8, weight='bold')

    # Vector DB
    b4 = FancyBboxPatch((7.6, 3.8), 2.0, 1.4, boxstyle="round,pad=0.15", fc="#C6F6D5", ec="#276749", lw=1.5)
    ax.add_patch(b4)
    ax.text(8.6, 4.5, "Vector Database\nChroma / Milvus\n(HNSW Index)", ha='center', va='center', fontsize=8, weight='bold')

    # Arrows for ingestion
    ax.annotate('', xy=(2.8, 4.5), xytext=(2.3, 4.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4A5568'))
    ax.annotate('', xy=(5.1, 4.5), xytext=(4.6, 4.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4A5568'))
    ax.annotate('', xy=(7.6, 4.5), xytext=(7.1, 4.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4A5568'))

    # Giai đoạn 2: Retrieval & Generation (Trục dưới)
    ax.text(0.5, 2.8, "PHẦN 2: RETRIEVAL & GENERATION PIPELINE (ONLINE QUERY)", fontsize=9.5, weight='bold', color='#C53030')
    
    # User Query
    q1 = FancyBboxPatch((0.5, 0.8), 1.8, 1.4, boxstyle="round,pad=0.15", fc="#FED7D7", ec="#E53E3E", lw=1.5)
    ax.add_patch(q1)
    ax.text(1.4, 1.5, "Câu hỏi người dùng\n(User Query)", ha='center', va='center', fontsize=8, weight='bold')
    
    # Query Embedding
    q2 = FancyBboxPatch((2.8, 0.8), 1.8, 1.4, boxstyle="round,pad=0.15", fc="#FEFCBF", ec="#D69E2E", lw=1.5)
    ax.add_patch(q2)
    ax.text(3.7, 1.5, "Query Vector\nq = embed(query)", ha='center', va='center', fontsize=8, weight='bold')

    # Similarity Search
    q3 = FancyBboxPatch((5.1, 0.8), 2.0, 1.4, boxstyle="round,pad=0.15", fc="#E9D8FD", ec="#805AD5", lw=1.5)
    ax.add_patch(q3)
    ax.text(6.1, 1.5, "Cosine Similarity\nTop-k Chunks\ncos(q, d_i) >= theta", ha='center', va='center', fontsize=8, weight='bold')

    # LLM Generator
    q4 = FancyBboxPatch((7.6, 0.8), 2.0, 1.4, boxstyle="round,pad=0.15", fc="#BEE3F8", ec="#2B6CB0", lw=1.5)
    ax.add_patch(q4)
    ax.text(8.6, 1.5, "Generative LLM\n(Gemini 2.5 / GPT-4o)\nAugmented Prompt", ha='center', va='center', fontsize=8, weight='bold')

    # Final Answer
    q5 = FancyBboxPatch((10.0, 0.8), 1.6, 1.4, boxstyle="round,pad=0.15", fc="#C6F6D5", ec="#22543D", lw=1.5)
    ax.add_patch(q5)
    ax.text(10.8, 1.5, "Câu trả lời\nChính xác\n(Grounded)", ha='center', va='center', fontsize=8, weight='bold')

    # Online arrows
    ax.annotate('', xy=(2.8, 1.5), xytext=(2.3, 1.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#E53E3E'))
    ax.annotate('', xy=(5.1, 1.5), xytext=(4.6, 1.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#E53E3E'))
    ax.annotate('', xy=(6.1, 2.2), xytext=(8.6, 3.8), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#805AD5', ls='--'))
    ax.annotate('', xy=(7.6, 1.5), xytext=(7.1, 1.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#E53E3E'))
    ax.annotate('', xy=(10.0, 1.5), xytext=(9.6, 1.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#E53E3E'))

    ax.set_title("HÌNH 5.3: KIẾN TRÚC TOÀN DIỆN HỆ THỐNG VECTOR RAG (OFFLINE INGESTION & ONLINE SERVING)", fontsize=11, pad=12)
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_5_3_vector_rag_pipeline.png')
    plt.savefig(out_path)
    plt.close()
    print(f"  [+] Đã tạo: {out_path}")

# ==============================================================================
# HÌNH 5.4: ĐỐI SÁNH VECTOR RAG VÀ GRAPHRAG (MULTI-HOP REASONING)
# ==============================================================================
def plot_fig_5_4():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))
    
    # Subplot 1: Vector RAG (Giới hạn phân mảnh văn bản)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title("(a) Vector RAG: Truy xuất theo Phân mảnh Đoạn rời rạc", fontsize=10.5, weight='bold')
    
    ax1.text(5, 9.0, "Câu hỏi: 'Bệnh nhân suy thận độ 3 bị tiểu đường có dùng được thuốc A?'",
             ha='center', va='center', fontsize=8.5, weight='bold', bbox=dict(boxstyle='round,pad=0.3', fc='#FFF5F5', ec='#E53E3E'))
             
    # Chunk 1
    c1 = FancyBboxPatch((1, 5.5), 3.5, 2.2, boxstyle="round,pad=0.2", fc="#EDF2F7", ec="#CBD5E0")
    ax1.add_patch(c1)
    ax1.text(2.75, 6.6, "Chunk #104 (Độ tương đồng: 0.84):\n'Thuốc A (Metformin) giúp hạ đường\nhuyết bằng cách ức chế tạo glucose ở gan.'", fontsize=7.5, ha='center', va='center')
    
    # Chunk 2
    c2 = FancyBboxPatch((5.5, 5.5), 3.5, 2.2, boxstyle="round,pad=0.2", fc="#EDF2F7", ec="#CBD5E0")
    ax1.add_patch(c2)
    ax1.text(7.25, 6.6, "Chunk #412 (Độ tương đồng: 0.62 - BỊ BỎ RƠI):\n'Chống chỉ định Metformin với bệnh nhân\nsuy thận có eGFR < 30 mL/phút/1.73m2.'", fontsize=7.5, ha='center', va='center')

    ax1.text(5, 3.5, "Nhược điểm Vector RAG:\n• Đứt gãy liên kết ngữ nghĩa giữa các chunk độc lập.\n• Bỏ lỡ thông tin chống chỉ định vì độ tương đồng thấp hơn ngưỡng top-k.\n• Kết quả LLM dễ sinh Ảo giác (Hallucination) nguy hiểm!",
             ha='center', va='center', fontsize=8.5, color='#9B2C2C', bbox=dict(boxstyle='round,pad=0.4', fc='#FED7D7', ec='#E53E3E'))

    # Subplot 2: GraphRAG (Suy luận đa bước qua đồ thị)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title("(b) Graph RAG: Suy luận Đa bước (Multi-hop) theo Đồ thị", fontsize=10.5, weight='bold')
    
    # Entities
    n_pat = FancyBboxPatch((0.5, 6.5), 2.2, 1.4, boxstyle="round,pad=0.15", fc="#BEE3F8", ec="#2B6CB0", lw=1.5)
    ax2.add_patch(n_pat)
    ax2.text(1.6, 7.2, "Bệnh nhân\n(eGFR=25)", ha='center', va='center', fontsize=8, weight='bold')

    n_dis = FancyBboxPatch((3.8, 6.5), 2.4, 1.4, boxstyle="round,pad=0.15", fc="#EBF8FF", ec="#3182CE", lw=1.5)
    ax2.add_patch(n_dis)
    ax2.text(5.0, 7.2, "Bệnh lý: ĐTĐ T2\nvà Suy thận độ 3", ha='center', va='center', fontsize=8, weight='bold')

    n_med = FancyBboxPatch((7.2, 6.5), 2.3, 1.4, boxstyle="round,pad=0.15", fc="#C6F6D5", ec="#276749", lw=1.5)
    ax2.add_patch(n_med)
    ax2.text(8.35, 7.2, "Thuốc A\n(Metformin)", ha='center', va='center', fontsize=8, weight='bold')

    # Path arrows
    ax2.annotate('', xy=(3.8, 7.2), xytext=(2.7, 7.2), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2B6CB0'))
    ax2.text(3.25, 7.6, "mắc", ha='center', va='center', fontsize=7.5, weight='bold')

    ax2.annotate('', xy=(7.2, 7.2), xytext=(6.2, 7.2), arrowprops=dict(arrowstyle="->", lw=1.5, color='#E53E3E'))
    ax2.text(6.7, 7.6, "CHỐNG CHỈ ĐỊNH", ha='center', va='center', fontsize=7.5, weight='bold', color='#E53E3E')

    # Hop 3: Alternative
    n_alt = FancyBboxPatch((5.0, 4.0), 2.6, 1.4, boxstyle="round,pad=0.15", fc="#FEFCBF", ec="#D69E2E", lw=1.5)
    ax2.add_patch(n_alt)
    ax2.text(6.3, 4.7, "Thuốc thay thế an toàn:\nDPP-4 (Linagliptin)", ha='center', va='center', fontsize=8, weight='bold')

    ax2.annotate('', xy=(6.3, 5.4), xytext=(5.0, 6.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#D69E2E', ls='--'))
    ax2.text(5.1, 5.8, "gợi ý", ha='center', va='center', fontsize=7.5, weight='bold')

    ax2.text(5, 1.8, "Ưu thế vượt trội của GraphRAG:\n• Duyệt đồ thị k-hop tìm thấy toàn bộ mắt xích chống chỉ định ẩn.\n• Kết hợp Vector Search + Graph Traversal cho độ chính xác 100%.\n• Trả lời có bằng chứng cấu trúc minh bạch, tin cậy y khoa.",
             ha='center', va='center', fontsize=8.5, color='#22543D', bbox=dict(boxstyle='round,pad=0.4', fc='#F0FFF4', ec='#38A169'))

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_5_4_graphrag_vs_vectorrag.png')
    plt.savefig(out_path)
    plt.close()
    print(f"  [+] Đã tạo: {out_path}")

# ==============================================================================
# HÌNH 5.5: LƯỢC ĐỒ ĐỒ THỊ TRI THỨC BỆNH TIỂU ĐƯỜNG LONG CHÂU
# ==============================================================================
def plot_fig_5_5():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # Trung tâm: Disease
    d_box = FancyBboxPatch((4.2, 3.0), 2.6, 1.5, boxstyle="round,pad=0.2", fc="#BEE3F8", ec="#2B6CB0", lw=2.5)
    ax.add_patch(d_box)
    ax.text(5.5, 3.75, "Entity: :Disease\n'Đái tháo đường Tuýp 2'\n(ICD-10: E11)", ha='center', va='center', fontsize=9, weight='bold')
    
    # 1. Symptom
    s_box = FancyBboxPatch((0.5, 4.8), 2.5, 1.4, boxstyle="round,pad=0.2", fc="#FED7D7", ec="#E53E3E", lw=2)
    ax.add_patch(s_box)
    ax.text(1.75, 5.5, "Entity: :Symptom\nKhát nước, tiểu nhiều,\nsút cân, mệt mỏi", ha='center', va='center', fontsize=8, weight='bold')
    ax.annotate('', xy=(4.2, 4.0), xytext=(3.0, 5.2), arrowprops=dict(arrowstyle="<-", lw=1.8, color='#E53E3E'))
    ax.text(3.3, 4.8, "HAS_SYMPTOM", fontsize=7.5, weight='bold', color='#E53E3E')

    # 2. Medicine (Long Châu)
    m_box = FancyBboxPatch((8.0, 4.8), 2.5, 1.6, boxstyle="round,pad=0.2", fc="#C6F6D5", ec="#276749", lw=2)
    ax.add_patch(m_box)
    ax.text(9.25, 5.6, "Entity: :Medicine (Long Châu)\nGlucophage 500mg\nDiamicron MR 30mg\nGiá: 110.000 - 220.000 đ", ha='center', va='center', fontsize=8, weight='bold')
    ax.annotate('', xy=(8.0, 5.2), xytext=(6.8, 4.0), arrowprops=dict(arrowstyle="->", lw=1.8, color='#276749'))
    ax.text(7.6, 4.4, "TREATED_BY", fontsize=7.5, weight='bold', color='#276749')

    # 3. Active Ingredient
    ai_box = FancyBboxPatch((8.0, 1.2), 2.5, 1.4, boxstyle="round,pad=0.2", fc="#FEFCBF", ec="#D69E2E", lw=2)
    ax.add_patch(ai_box)
    ax.text(9.25, 1.9, "Entity: :ActiveIngredient\nMetformin HCl\nGliclazide", ha='center', va='center', fontsize=8, weight='bold')
    ax.annotate('', xy=(9.25, 2.6), xytext=(9.25, 4.8), arrowprops=dict(arrowstyle="<-", lw=1.8, color='#D69E2E'))
    ax.text(9.35, 3.6, "CONTAINS", fontsize=7.5, weight='bold', color='#D69E2E')

    # 4. Complication
    comp_box = FancyBboxPatch((0.5, 1.2), 2.5, 1.4, boxstyle="round,pad=0.2", fc="#E9D8FD", ec="#805AD5", lw=2)
    ax.add_patch(comp_box)
    ax.text(1.75, 1.9, "Entity: :Complication\nBệnh võng mạc, suy thận,\nbàn chân đái tháo đường", ha='center', va='center', fontsize=8, weight='bold')
    ax.annotate('', xy=(1.75, 2.6), xytext=(4.2, 3.4), arrowprops=dict(arrowstyle="->", lw=1.8, color='#805AD5'))
    ax.text(2.6, 3.2, "LEADS_TO", fontsize=7.5, weight='bold', color='#805AD5')

    # 5. Diet & Lifestyle
    diet_box = FancyBboxPatch((4.2, 0.5), 2.6, 1.4, boxstyle="round,pad=0.2", fc="#EDF2F7", ec="#4A5568", lw=2)
    ax.add_patch(diet_box)
    ax.text(5.5, 1.2, "Entity: :DietLifestyle\nGiảm tinh bột, tăng chất xơ,\nđi bộ 30p mỗi ngày", ha='center', va='center', fontsize=8, weight='bold')
    ax.annotate('', xy=(5.5, 1.9), xytext=(5.5, 3.0), arrowprops=dict(arrowstyle="<-", lw=1.8, color='#4A5568'))
    ax.text(5.6, 2.4, "RECOMMENDED", fontsize=7.5, weight='bold', color='#4A5568')

    ax.set_title("HÌNH 5.5: LƯỢC ĐỒ BẢN THỂ HỌC (ONTOLOGY) ĐỒ THỊ TRI THỨC BỆNH TIỂU ĐƯỜNG LONG CHÂU", fontsize=11, pad=12)
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_5_5_diabetes_kg_schema.png')
    plt.savefig(out_path)
    plt.close()
    print(f"  [+] Đã tạo: {out_path}")

# ==============================================================================
# HÌNH 5.6: TÍCH HỢP MÔ HÌNH ML TIỂU ĐƯỜNG VỚI GRAPHRAG
# ==============================================================================
def plot_fig_5_6():
    fig, ax = plt.subplots(figsize=(11.5, 5.0))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    
    # 1. Bệnh nhân nhập chỉ số
    p1 = FancyBboxPatch((0.5, 3.2), 2.2, 1.6, boxstyle="round,pad=0.15", fc="#EDF2F7", ec="#4A5568", lw=1.5)
    ax.add_patch(p1)
    ax.text(1.6, 4.0, "Bệnh nhân & Chỉ số lâm sàng\n(Glucose=168, BMI=33.6,\nAge=50, Insulin=0)", ha='center', va='center', fontsize=8, weight='bold')

    # 2. ML Model (Chương 2)
    p2 = FancyBboxPatch((3.4, 3.2), 2.2, 1.6, boxstyle="round,pad=0.15", fc="#FEFCBF", ec="#D69E2E", lw=2)
    ax.add_patch(p2)
    ax.text(4.5, 4.0, "Mô hình ML (Chương 2)\nLogistic / Random Forest\n(F1 = 0.81, ROC = 0.84)", ha='center', va='center', fontsize=8, weight='bold')

    # 3. Kết quả ML
    p3 = FancyBboxPatch((6.3, 3.2), 2.0, 1.6, boxstyle="round,pad=0.15", fc="#FED7D7", ec="#E53E3E", lw=2)
    ax.add_patch(p3)
    ax.text(7.3, 4.0, "Dự báo Nguy cơ:\nRisk = 84.7%\n(DƯƠNG TÍNH CAO)", ha='center', va='center', fontsize=8.5, weight='bold', color='#9B2C2C')

    # Mũi tên trục trên
    ax.annotate('', xy=(3.4, 4.0), xytext=(2.7, 4.0), arrowprops=dict(arrowstyle="->", lw=2, color='#2B6CB0'))
    ax.annotate('', xy=(6.3, 4.0), xytext=(5.6, 4.0), arrowprops=dict(arrowstyle="->", lw=2, color='#D69E2E'))

    # Trục dưới: GraphRAG Orchestration
    p4 = FancyBboxPatch((3.4, 0.6), 2.2, 1.6, boxstyle="round,pad=0.15", fc="#BEE3F8", ec="#2B6CB0", lw=2)
    ax.add_patch(p4)
    ax.text(4.5, 1.4, "Knowledge Graph\n(Neo4j + Long Châu)\nTruy vấn phác đồ & thuốc", ha='center', va='center', fontsize=8, weight='bold')

    p5 = FancyBboxPatch((6.3, 0.6), 2.0, 1.6, boxstyle="round,pad=0.15", fc="#C6F6D5", ec="#276749", lw=2)
    ax.add_patch(p5)
    ax.text(7.3, 1.4, "Medical GraphRAG\n(Gemini 2.5 / GPT-4o)\nLập phác đồ tối ưu", ha='center', va='center', fontsize=8, weight='bold')

    p6 = FancyBboxPatch((9.0, 0.6), 2.1, 4.2, boxstyle="round,pad=0.2", fc="#F0FFF4", ec="#38A169", lw=2)
    ax.add_patch(p6)
    rec_text = "Khuyến nghị Bác sĩ AI:\n\n1. Kết quả: Nguy cơ cao (84.7%)\n2. Thuốc đề xuất:\n   • Metformin 500mg\n   • Giá: 110.000 đ/hộp\n3. Biến chứng cảnh báo:\n   • Theo dõi đáy mắt & thận\n4. Chế độ dinh dưỡng:\n   • Giảm GI < 55, tập thể dục"
    ax.text(10.05, 2.7, rec_text, ha='center', va='center', fontsize=7.5, weight='bold', color='#22543D')

    # Mũi tên tích hợp
    ax.annotate('', xy=(4.5, 2.2), xytext=(4.5, 3.2), arrowprops=dict(arrowstyle="->", lw=2, color='#2B6CB0'))
    ax.text(4.7, 2.7, "Kích hoạt", fontsize=7.5, weight='bold')

    ax.annotate('', xy=(6.3, 1.4), xytext=(5.6, 1.4), arrowprops=dict(arrowstyle="->", lw=2, color='#2B6CB0'))
    ax.annotate('', xy=(7.3, 2.2), xytext=(7.3, 3.2), arrowprops=dict(arrowstyle="->", lw=2, color='#E53E3E'))
    ax.text(7.5, 2.7, "Risk Context", fontsize=7.5, weight='bold', color='#E53E3E')

    ax.annotate('', xy=(9.0, 2.7), xytext=(8.3, 1.4), arrowprops=dict(arrowstyle="->", lw=2, color='#276749'))

    ax.set_title("HÌNH 5.6: SƠ ĐỒ TÍCH HỢP MÔ HÌNH HỌC MÁY TIỂU ĐƯỜNG VỚI HỆ THỐNG GRAPHRAG Y TẾ", fontsize=11, pad=12)
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_5_6_ml_graphrag_integration.png')
    plt.savefig(out_path)
    plt.close()
    print(f"  [+] Đã tạo: {out_path}")

# ==============================================================================
# HÌNH 5.7: ĐỒ THỊ TÀI CHÍNH VĨ MÔ VÀ DỰ BÁO CHUỖI THỜI GIAN LSTM
# ==============================================================================
def plot_fig_5_7():
    fig, ax = plt.subplots(figsize=(11.5, 5.5))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.0)
    ax.axis('off')
    
    # Macro Indicators
    f1 = FancyBboxPatch((0.5, 3.8), 2.2, 1.6, boxstyle="round,pad=0.15", fc="#FED7D7", ec="#E53E3E", lw=1.8)
    ax.add_patch(f1)
    ax.text(1.6, 4.6, "Lãi suất FED (Fed Funds)\nLạm phát Mỹ (CPI)\nChỉ số USD Index (DXY)", ha='center', va='center', fontsize=8, weight='bold')

    f2 = FancyBboxPatch((0.5, 1.0), 2.2, 1.6, boxstyle="round,pad=0.15", fc="#EBF8FF", ec="#3182CE", lw=1.8)
    ax.add_patch(f2)
    ax.text(1.6, 1.8, "Tỷ giá USD/VND\nLãi suất liên ngân hàng\nChính sách Ngân hàng Nhà nước", ha='center', va='center', fontsize=7.8, weight='bold')

    # Central Asset Nodes
    gold_box = FancyBboxPatch((4.5, 3.8), 2.5, 1.6, boxstyle="round,pad=0.2", fc="#FEFCBF", ec="#D69E2E", lw=2.5)
    ax.add_patch(gold_box)
    ax.text(5.75, 4.6, "Thị trường Vàng (XAU/USD)\n(Chương 4 LSTM: Tăng 2.4%)\nKênh trú ẩn an toàn", ha='center', va='center', fontsize=8.2, weight='bold')

    stock_box = FancyBboxPatch((4.5, 1.0), 2.5, 1.6, boxstyle="round,pad=0.2", fc="#C6F6D5", ec="#276749", lw=2.5)
    ax.add_patch(stock_box)
    ax.text(5.75, 1.8, "Thị trường Chứng khoán\n(VN-INDEX / Cổ phiếu)\nNhạy cảm với lãi suất", ha='center', va='center', fontsize=8.2, weight='bold')

    # Arrows macro to assets
    ax.annotate('', xy=(4.5, 4.6), xytext=(2.7, 4.6), arrowprops=dict(arrowstyle="->", lw=1.8, color='#E53E3E'))
    ax.text(3.5, 4.9, "Nghịch biến\n(DXY tăng -> Vàng giảm)", ha='center', fontsize=7.2, weight='bold')

    ax.annotate('', xy=(4.5, 1.8), xytext=(2.7, 1.8), arrowprops=dict(arrowstyle="->", lw=1.8, color='#3182CE'))
    ax.text(3.5, 2.1, "Tác động chi phí vốn", ha='center', fontsize=7.2, weight='bold')

    # GraphRAG & Forecasting Synthesizer
    synth_box = FancyBboxPatch((8.3, 1.5), 2.8, 3.2, boxstyle="round,pad=0.2", fc="#F0FFF4", ec="#38A169", lw=2)
    ax.add_patch(synth_box)
    synth_text = "Hệ thống GraphRAG Tài chính:\n\n1. Đầu vào Quantitative:\n   • Dự báo LSTM vàng t+1 -> t+30\n   • RMSE = 18.42 USD\n2. Đầu vào Qualitative:\n   • Đồ thị quan hệ vĩ mô Neo4j\n   • Tin tức địa chính trị RAG\n3. Khuyến nghị Quản trị Rủi ro:\n   • Tăng tỷ trọng Vàng: 20%\n   • Tích lũy Cổ phiếu phòng thủ\n   • Chiến lược Hedging tỷ giá"
    ax.text(9.7, 3.1, synth_text, ha='center', va='center', fontsize=7.8, weight='bold', color='#22543D')

    ax.annotate('', xy=(8.3, 4.6), xytext=(7.0, 4.6), arrowprops=dict(arrowstyle="->", lw=1.8, color='#D69E2E'))
    ax.annotate('', xy=(8.3, 1.8), xytext=(7.0, 1.8), arrowprops=dict(arrowstyle="->", lw=1.8, color='#276749'))

    ax.set_title("HÌNH 5.7: ĐỒ THỊ TRI THỨC VĨ MÔ KẾT HỢP DỰ BÁO CHUỖI THỜI GIAN LSTM TRONG TÀI CHÍNH", fontsize=11, pad=12)
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_5_7_finance_kg_lstm.png')
    plt.savefig(out_path)
    plt.close()
    print(f"  [+] Đã tạo: {out_path}")

# ==============================================================================
# HÌNH 5.8: KIẾN TRÚC TRIỂN KHAI STREAMLIT UI & FASTAPI GATEWAY
# ==============================================================================
def plot_fig_5_8():
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    
    # 1. Frontend UI
    ui_box = FancyBboxPatch((0.5, 1.2), 2.5, 3.2, boxstyle="round,pad=0.2", fc="#EBF8FF", ec="#3182CE", lw=2)
    ax.add_patch(ui_box)
    ui_text = "Giao diện Tương tác Streamlit\n(Frontend Web Client)\n\n• Chatbot Y tế / Tài chính\n• Trực quan hóa Đồ thị mạng\n• Form nhập chỉ số xét nghiệm\n• Biểu đồ dự báo thời gian thực"
    ax.text(1.75, 2.8, ui_text, ha='center', va='center', fontsize=8, weight='bold', color='#2B6CB0')

    # 2. FastAPI Gateway
    api_box = FancyBboxPatch((4.2, 1.2), 2.8, 3.2, boxstyle="round,pad=0.2", fc="#FEFCBF", ec="#D69E2E", lw=2)
    ax.add_patch(api_box)
    api_text = "FastAPI Backend Gateway\n(Asynchronous REST API)\n\n• POST /api/chat/graphrag\n• POST /api/predict/diabetes\n• POST /api/forecast/gold\n• Pydantic Schema Validation\n• Tokenizer & Intent Router"
    ax.text(5.6, 2.8, api_text, ha='center', va='center', fontsize=8, weight='bold', color='#744210')

    # 3. Data & Reasoning Engines
    eng_box = FancyBboxPatch((8.2, 1.2), 2.8, 3.2, boxstyle="round,pad=0.2", fc="#C6F6D5", ec="#276749", lw=2)
    ax.add_patch(eng_box)
    eng_text = "Hệ thống Lưu trữ & Suy luận\n\n• Neo4j Graph DB (Cypher)\n• ChromaDB (Dense Vectors)\n• Model Registry (PyTorch/ONNX)\n• LLM Engine (Gemini / GPT-4o)\n• Grounding Fact-checker"
    ax.text(9.6, 2.8, eng_text, ha='center', va='center', fontsize=8, weight='bold', color='#22543D')

    # Mũi tên kết nối
    ax.annotate('', xy=(4.2, 3.2), xytext=(3.0, 3.2),
                 arrowprops=dict(arrowstyle="simple,tail_width=2,head_width=7,head_length=7",
                                 facecolor='#3182CE', edgecolor='#2B6CB0'))
    ax.text(3.6, 3.6, "HTTP JSON\nRequest", ha='center', fontsize=7.5, weight='bold')

    ax.annotate('', xy=(3.0, 2.2), xytext=(4.2, 2.2),
                 arrowprops=dict(arrowstyle="simple,tail_width=2,head_width=7,head_length=7",
                                 facecolor='#48BB78', edgecolor='#276749'))
    ax.text(3.6, 1.8, "JSON Stream\nResponse", ha='center', fontsize=7.5, weight='bold')

    ax.annotate('', xy=(8.2, 3.2), xytext=(7.0, 3.2),
                 arrowprops=dict(arrowstyle="simple,tail_width=2,head_width=7,head_length=7",
                                 facecolor='#D69E2E', edgecolor='#B7791F'))
    ax.text(7.6, 3.6, "Query &\nEmbed", ha='center', fontsize=7.5, weight='bold')

    ax.annotate('', xy=(7.0, 2.2), xytext=(8.2, 2.2),
                 arrowprops=dict(arrowstyle="simple,tail_width=2,head_width=7,head_length=7",
                                 facecolor='#48BB78', edgecolor='#276749'))
    ax.text(7.6, 1.8, "Context &\nInference", ha='center', fontsize=7.5, weight='bold')

    ax.set_title("HÌNH 5.8: KIẾN TRÚC TRIỂN KHAI TOÀN DIỆN CỦA HỆ THỐNG GRAPHRAG (STREAMLIT + FASTAPI + NEO4J)", fontsize=11, pad=12)
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_5_8_chatbot_deployment_ui.png')
    plt.savefig(out_path)
    plt.close()
    print(f"  [+] Đã tạo: {out_path}")

if __name__ == '__main__':
    plot_fig_5_1()
    plot_fig_5_2()
    plot_fig_5_3()
    plot_fig_5_4()
    plot_fig_5_5()
    plot_fig_5_6()
    plot_fig_5_7()
    plot_fig_5_8()
    print("[*] Hoàn tất thành công 100% việc tạo 8 hình ảnh cho Chương 5!")
