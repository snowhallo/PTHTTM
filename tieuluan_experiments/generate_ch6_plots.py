import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plots_dir = os.path.join(os.path.dirname(__file__), 'plots')
os.makedirs(plots_dir, exist_ok=True)

# Set global styles
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

def generate_fig_6_1():
    # 1. Euclidean vs Non-Euclidean
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5), dpi=300)
    
    # 1D Sequence (Time Series / Text)
    ax1.set_title("a) Miền 1D Euclide (Chuỗi Thời Gian / RNN)", fontsize=11, fontweight='bold', color='#003366')
    ax1.set_xlim(-0.5, 4.5)
    ax1.set_ylim(-1, 1)
    ax1.axis('off')
    for i in range(4):
        rect = patches.FancyBboxPatch((i, -0.3), 0.6, 0.6, boxstyle="round,pad=0.08", ec='#2B6CB0', fc='#EBF8FF', lw=1.5)
        ax1.add_patch(rect)
        ax1.text(i + 0.3, 0, f"$x_{{{i+1}}}$", ha='center', va='center', fontsize=11, fontweight='bold', color='#1A365D')
        if i < 3:
            ax1.annotate("", xy=(i + 0.95, 0), xytext=(i + 0.65, 0),
                         arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=1.5))
    ax1.text(1.8, -0.7, "Khoảng cách cố định, thứ tự tuyến tính chặt chẽ", ha='center', fontsize=9, style='italic', color='#4A5568')

    # 2D Grid (Image / CNN)
    ax2.set_title("b) Miền 2D Euclide (Lưới Ảnh / CNN)", fontsize=11, fontweight='bold', color='#003366')
    ax2.set_xlim(-0.5, 3.5)
    ax2.set_ylim(-0.5, 3.5)
    ax2.axis('off')
    for r in range(3):
        for c in range(3):
            rect = patches.Rectangle((c, 2 - r), 0.8, 0.8, ec='#2B6CB0', fc='#EBF8FF', lw=1.2)
            ax2.add_patch(rect)
            if r == 1 and c == 1:
                rect.set_facecolor('#BEE3F8')
                ax2.text(c + 0.4, 2 - r + 0.4, "$p_{i,j}$", ha='center', va='center', fontweight='bold', color='#C53030')
            else:
                ax2.text(c + 0.4, 2 - r + 0.4, f"$p_{{{r},{c}}}$", ha='center', va='center', fontsize=8, color='#4A5568')
    ax2.text(1.4, -0.35, "Láng giềng cố định (kích thước Kernel vuông $3\\times 3$)", ha='center', fontsize=9, style='italic', color='#4A5568')

    # Non-Euclidean Graph (GNN)
    ax3.set_title("c) Miền Đồ Thị Phi Euclide (Deep Graph / GNN)", fontsize=11, fontweight='bold', color='#003366')
    ax3.set_xlim(-1.2, 1.2)
    ax3.set_ylim(-1.2, 1.2)
    ax3.axis('off')
    
    nodes = {
        'v': (0, 0),
        'u1': (0.8, 0.6),
        'u2': (0.7, -0.7),
        'u3': (-0.6, -0.8),
        'u4': (-0.9, 0.4),
        'w1': (1.1, 0.1),
        'w2': (-0.3, 0.9)
    }
    edges = [('v', 'u1'), ('v', 'u2'), ('v', 'u3'), ('v', 'u4'), ('u1', 'w1'), ('u2', 'w1'), ('u4', 'w2')]
    for n1, n2 in edges:
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        ax3.plot([x1, x2], [y1, y2], color='#A0AEC0', lw=1.5, zorder=1)
        
    for k, (x, y) in nodes.items():
        if k == 'v':
            circle = plt.Circle((x, y), 0.22, ec='#C53030', fc='#FED7D7', lw=2, zorder=2)
            ax3.add_patch(circle)
            ax3.text(x, y, "$v$", ha='center', va='center', fontweight='bold', color='#9B2C2C', fontsize=12)
        elif k.startswith('u'):
            circle = plt.Circle((x, y), 0.18, ec='#2B6CB0', fc='#BEE3F8', lw=1.5, zorder=2)
            ax3.add_patch(circle)
            ax3.text(x, y, f"${k}$", ha='center', va='center', fontweight='bold', color='#2C5282', fontsize=10)
        else:
            circle = plt.Circle((x, y), 0.14, ec='#718096', fc='#EDF2F7', lw=1.2, zorder=2)
            ax3.add_patch(circle)
            ax3.text(x, y, f"${k}$", ha='center', va='center', color='#4A5568', fontsize=8)
    ax3.text(0, -1.15, "Số lượng láng giềng tùy ý, cấu trúc phi tập trung", ha='center', fontsize=9, style='italic', color='#4A5568')

    plt.tight_layout()
    out = os.path.join(plots_dir, 'fig_6_1_euclidean_vs_noneuclidean.png')
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"[✓] Đã tạo: {out}")

def generate_fig_6_2():
    # 2. MPNN Framework
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)

    # Box 1: Neighborhood
    b1 = patches.FancyBboxPatch((0.5, 1.2), 2.2, 2.8, boxstyle="round,pad=0.15", ec='#2B6CB0', fc='#EBF8FF', lw=1.5)
    ax.add_patch(b1)
    ax.text(1.6, 3.6, "1. Láng giềng $\\mathcal{N}(v)$", ha='center', fontweight='bold', color='#003366', fontsize=11)
    ax.text(1.6, 2.7, "Đặc trưng các đỉnh lân cận:\n$h_u^{(k-1)}, \\forall u \\in \\mathcal{N}(v)$\nĐặc trưng cạnh: $e_{uv}$", ha='center', color='#2D3748', fontsize=9)

    # Arrow 1
    ax.annotate("", xy=(3.3, 2.6), xytext=(2.8, 2.6), arrowprops=dict(arrowstyle="->", lw=2, color='#2B6CB0'))
    ax.text(3.05, 2.9, "Message", ha='center', fontsize=9, fontweight='bold', color='#2B6CB0')

    # Box 2: Aggregation
    b2 = patches.FancyBboxPatch((3.4, 1.2), 2.8, 2.8, boxstyle="round,pad=0.15", ec='#D69E2E', fc='#FEFCBF', lw=1.5)
    ax.add_patch(b2)
    ax.text(4.8, 3.6, "2. Pha Tổng hợp (AGGREGATE)", ha='center', fontweight='bold', color='#744210', fontsize=11)
    ax.text(4.8, 2.6, "$m_v^{(k)} = \\bigoplus_{u \\in \\mathcal{N}(v)} M_k(h_v, h_u, e_{uv})$\n\nToán tử $\\bigoplus$ bất biến thứ tự:\nMean, Sum, Max, Attention", ha='center', color='#4A5568', fontsize=9)

    # Arrow 2
    ax.annotate("", xy=(6.8, 2.6), xytext=(6.3, 2.6), arrowprops=dict(arrowstyle="->", lw=2, color='#D69E2E'))
    ax.text(6.55, 2.9, "Update", ha='center', fontsize=9, fontweight='bold', color='#D69E2E')

    # Box 3: Update
    b3 = patches.FancyBboxPatch((6.9, 1.2), 2.6, 2.8, boxstyle="round,pad=0.15", ec='#38A169', fc='#F0FFF4', lw=1.5)
    ax.add_patch(b3)
    ax.text(8.2, 3.6, "3. Pha Cập nhật (UPDATE)", ha='center', fontweight='bold', color='#22543D', fontsize=11)
    ax.text(8.2, 2.6, "$h_v^{(k)} = U_k\\left(h_v^{(k-1)}, m_v^{(k)}\\right)$\n\nKết hợp trạng thái cũ\nvới thông điệp tổng hợp\n(MLP / GRU Cell)", ha='center', color='#2D3748', fontsize=9)

    plt.tight_layout()
    out = os.path.join(plots_dir, 'fig_6_2_message_passing_mpnn.png')
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"[✓] Đã tạo: {out}")

def generate_fig_6_3():
    # 3. GCN Architecture
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)

    # Input Graph
    p1 = patches.FancyBboxPatch((0.4, 0.8), 2.2, 2.8, boxstyle="round,pad=0.1", ec='#4A5568', fc='#EDF2F7', lw=1.5)
    ax.add_patch(p1)
    ax.text(1.5, 3.2, "Đầu Vào Đồ Thị", ha='center', fontweight='bold', color='#1A202C', fontsize=11)
    ax.text(1.5, 2.2, "Ma trận đặc trưng $X \\in \\mathbb{R}^{N \\times F}$\nMa trận kề $A \\in \\{0, 1\\}^{N \\times N}$\n(Thêm Self-loop $\\tilde{A} = A + I$)", ha='center', fontsize=9, color='#4A5568')

    ax.annotate("", xy=(3.1, 2.2), xytext=(2.7, 2.2), arrowprops=dict(arrowstyle="->", lw=2, color='#003366'))

    # GCN Layer 1
    p2 = patches.FancyBboxPatch((3.2, 0.8), 3.0, 2.8, boxstyle="round,pad=0.1", ec='#003366', fc='#EBF8FF', lw=1.5)
    ax.add_patch(p2)
    ax.text(4.7, 3.2, "Tầng GCN Thứ Nhất", ha='center', fontweight='bold', color='#003366', fontsize=11)
    ax.text(4.7, 2.1, "$H^{(1)} = \\text{ReLU}\\left(\\tilde{D}^{-\\frac{1}{2}} \\tilde{A} \\tilde{D}^{-\\frac{1}{2}} X W^{(0)}\\right)$\n\nTrích xuất nhúng không gian cấp 1\n(1-hop Neighborhood Aggregation)", ha='center', fontsize=8.5, color='#2D3748')

    ax.annotate("", xy=(6.7, 2.2), xytext=(6.3, 2.2), arrowprops=dict(arrowstyle="->", lw=2, color='#003366'))

    # GCN Layer 2
    p3 = patches.FancyBboxPatch((6.8, 0.8), 2.8, 2.8, boxstyle="round,pad=0.1", ec='#2B6CB0', fc='#EBF8FF', lw=1.5)
    ax.add_patch(p3)
    ax.text(8.2, 3.2, "Tầng GCN Thứ Hai & Softmax", ha='center', fontweight='bold', color='#2B6CB0', fontsize=11)
    ax.text(8.2, 2.1, "$Z = \\text{Softmax}\\left(\\hat{A} H^{(1)} W^{(1)}\\right)$\n\nNhúng không gian cấp 2 (2-hop)\nDự đoán phân loại nút (Node Class)", ha='center', fontsize=8.5, color='#2D3748')

    plt.tight_layout()
    out = os.path.join(plots_dir, 'fig_6_3_gcn_architecture.png')
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"[✓] Đã tạo: {out}")

def generate_fig_6_4():
    # 4. GAT Attention
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.0, 2.0)

    center = (0, 0)
    circle_center = plt.Circle(center, 0.4, ec='#C53030', fc='#FED7D7', lw=2, zorder=3)
    ax.add_patch(circle_center)
    ax.text(0, 0, "Đỉnh $i$\n$h_i$", ha='center', va='center', fontweight='bold', color='#9B2C2C', fontsize=11)

    neighbors = [
        ("Đỉnh $j_1$\n$h_{j1}$", (-1.8, 1.2), 0.35, "0.45 (Quan trọng cao)"),
        ("Đỉnh $j_2$\n$h_{j2}$", (1.8, 1.2), 0.25, "0.30 (Trung bình)"),
        ("Đỉnh $j_3$\n$h_{j3}$", (1.6, -1.2), 0.15, "0.15 (Thấp)"),
        ("Đỉnh $j_4$\n$h_{j4}$", (-1.6, -1.2), 0.10, "0.10 (Rất thấp)")
    ]

    for idx, (label, pos, weight, ann) in enumerate(neighbors):
        c = plt.Circle(pos, 0.35, ec='#2B6CB0', fc='#EBF8FF', lw=1.5, zorder=3)
        ax.add_patch(c)
        ax.text(pos[0], pos[1], label, ha='center', va='center', fontweight='bold', color='#1A365D', fontsize=9.5)
        # edge
        lw = weight * 10
        ax.plot([0, pos[0]], [0, pos[1]], color='#2B6CB0', lw=lw, alpha=0.7, zorder=2)
        mid_x = (pos[0]) * 0.55
        mid_y = (pos[1]) * 0.55
        ax.text(mid_x, mid_y + (0.15 if mid_y>0 else -0.15), f"$\\alpha_{{i,j_{idx+1}}} = {weight:.2f}$", 
                ha='center', fontsize=8.5, fontweight='bold', color='#C53030',
                bbox=dict(boxstyle="round,pad=0.2", fc='white', ec='#CBD5E0', lw=0.8))

    ax.set_title("Cơ chế Tự Chú Ý Đồ thị Đa Đầu (Graph Attention Multi-Head Mechanism)", fontsize=11, fontweight='bold', color='#003366', y=1.02)
    plt.tight_layout()
    out = os.path.join(plots_dir, 'fig_6_4_gat_attention_mechanism.png')
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"[✓] Đã tạo: {out}")

def generate_fig_6_5():
    # 5. Experimental Evaluation Bar Chart
    models = ['Baseline MLP', 'GCN (Kipf 2017)', 'GraphSAGE (2017)', 'GAT (Veličković 2018)']
    acc = [74.20, 83.65, 85.90, 87.45]
    f1 = [72.80, 82.90, 85.15, 86.80]
    auc = [76.50, 88.40, 90.75, 92.10]

    x = np.arange(len(models))
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    r1 = ax.bar(x - width, acc, width, label='Accuracy (%)', color='#003366')
    r2 = ax.bar(x, f1, width, label='Macro F1-Score (%)', color='#2B6CB0')
    r3 = ax.bar(x + width, auc, width, label='ROC-AUC (%)', color='#319795')

    ax.set_ylabel('Hiệu năng (%)', fontweight='bold', fontsize=10)
    ax.set_title('Đối sánh Hiệu năng Học sâu Đồ thị trên Đồ thị Tri thức Đái tháo đường & Tài chính', fontweight='bold', fontsize=11, color='#003366')
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.legend(frameon=True, facecolor='#F7FAFC')
    ax.set_ylim(60, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for rects in [r1, r2, r3]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    out = os.path.join(plots_dir, 'fig_6_5_gnn_node_classification_results.png')
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"[✓] Đã tạo: {out}")

def generate_fig_6_6():
    # 6. Deep Graph Pipeline Architecture
    fig, ax = plt.subplots(figsize=(11, 4.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5)

    # Component 1: Knowledge Graph Storage
    p1 = patches.FancyBboxPatch((0.5, 1.2), 2.2, 2.8, boxstyle="round,pad=0.12", ec='#4A5568', fc='#EDF2F7', lw=1.5)
    ax.add_patch(p1)
    ax.text(1.6, 3.6, "1. Cơ sở Đồ thị Neo4j", ha='center', fontweight='bold', color='#1A202C', fontsize=11)
    ax.text(1.6, 2.4, "Đồ thị tri thức Long Châu\n& S&P 500 Vĩ mô\n\nNút: Thuốc, Bệnh, Mã CK\nCạnh: Điều trị, Tương tác", ha='center', fontsize=8.5, color='#4A5568')

    ax.annotate("", xy=(3.2, 2.6), xytext=(2.8, 2.6), arrowprops=dict(arrowstyle="->", lw=2, color='#003366'))

    # Component 2: PyTorch Geometric Engine
    p2 = patches.FancyBboxPatch((3.3, 1.2), 2.8, 2.8, boxstyle="round,pad=0.12", ec='#003366', fc='#EBF8FF', lw=1.5)
    ax.add_patch(p2)
    ax.text(4.7, 3.6, "2. GNN Inference Engine", ha='center', fontweight='bold', color='#003366', fontsize=11)
    ax.text(4.7, 2.4, "PyG GAT/GraphSAGE\n\n- Học nhúng nút 128-dim\n- Phân loại nguy cơ bệnh\n- Dự báo liên kết rủi ro vĩ mô", ha='center', fontsize=8.5, color='#2B6CB0')

    ax.annotate("", xy=(6.6, 2.6), xytext=(6.2, 2.6), arrowprops=dict(arrowstyle="->", lw=2, color='#003366'))

    # Component 3: GraphRAG Reranker
    p3 = patches.FancyBboxPatch((6.7, 1.2), 2.0, 2.8, boxstyle="round,pad=0.12", ec='#D69E2E', fc='#FEFCBF', lw=1.5)
    ax.add_patch(p3)
    ax.text(7.7, 3.6, "3. GraphRAG Rerank", ha='center', fontweight='bold', color='#744210', fontsize=11)
    ax.text(7.7, 2.4, "Tái xếp hạng văn bản\ndựa trên khoảng cách\nnhúng GNN & RRF", ha='center', fontsize=8.5, color='#4A5568')

    ax.annotate("", xy=(9.2, 2.6), xytext=(8.8, 2.6), arrowprops=dict(arrowstyle="->", lw=2, color='#D69E2E'))

    # Component 4: FastAPI & Client
    p4 = patches.FancyBboxPatch((9.3, 1.2), 1.5, 2.8, boxstyle="round,pad=0.12", ec='#38A169', fc='#F0FFF4', lw=1.5)
    ax.add_patch(p4)
    ax.text(10.05, 3.6, "4. FastAPI", ha='center', fontweight='bold', color='#22543D', fontsize=11)
    ax.text(10.05, 2.4, "REST API\n\n/predict-node\n/predict-link\n/consult-rag", ha='center', fontsize=8, color='#2D3748')

    plt.tight_layout()
    out = os.path.join(plots_dir, 'fig_6_6_deep_graph_pipeline.png')
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"[✓] Đã tạo: {out}")

if __name__ == "__main__":
    generate_fig_6_1()
    generate_fig_6_2()
    generate_fig_6_3()
    generate_fig_6_4()
    generate_fig_6_5()
    generate_fig_6_6()
    print("[+] Hoàn tất sinh toàn bộ 6 hình ảnh cho Chương 6!")
