# -*- coding: utf-8 -*-
"""
Các thuật toán đồ thị, đo lường Homophily, tính toán Laplacian và trực quan hóa mạng lưới Plotly
Dự án: Phần mềm GlucoGraph AI - Nhóm 15 (PTIT)
Giao diện sáng sạch, chuẩn mực, không màu mè AI
"""

import numpy as np
import networkx as nx
import plotly.graph_objects as go
from sklearn.neighbors import NearestNeighbors
from config import THEME_COLORS

# Trọng số y khoa ADA 2024 cho 7 chiều đặc trưng
# [gender_code, hypertension, heart_disease, age, bmi, HbA1c_level, blood_glucose_level]
CLINICAL_WEIGHTS = np.array([0.5, 1.0, 1.0, 1.2, 1.5, 3.0, 2.5])

def compute_knn_graph(X, k=5, use_clinical_weights=True, sigma=1.0):
    """
    Xây dựng đồ thị k-NN từ ma trận đặc trưng bệnh nhân:
    - Baseline k-NN: Trọng số đồng nhất
    - Clinical k-NN: Trọng số y khoa theo hướng dẫn ADA 2024
    """
    N = len(X)
    if use_clinical_weights:
        w_sqrt = np.sqrt(CLINICAL_WEIGHTS)
        X_weighted = X * w_sqrt
    else:
        X_weighted = X
        
    nbrs = NearestNeighbors(n_neighbors=k+1, metric='euclidean', algorithm='auto').fit(X_weighted)
    distances, indices = nbrs.kneighbors(X_weighted)
    
    A = np.zeros((N, N), dtype=float)
    for i in range(N):
        for j_idx, neighbor in enumerate(indices[i][1:]):  # Bỏ qua chính nó
            dist = distances[i][j_idx + 1]
            weight = np.exp(- (dist ** 2) / (2 * (sigma ** 2)))
            A[i, neighbor] = weight
            A[neighbor, i] = weight
            
    return A

def compute_homophily_ratio(A, y):
    """
    Đo lường độ thuần nhất nhãn đồ thị (Homophily Ratio):
    Tỷ lệ cạnh nối 2 nốt có cùng nhãn bệnh học (cùng = 0 hoặc cùng = 1)
    """
    N = len(y)
    same_label_edges = 0
    total_edges = 0
    
    for i in range(N):
        for j in range(i + 1, N):
            if A[i, j] > 0:
                total_edges += 1
                if y[i] == y[j]:
                    same_label_edges += 1
                    
    if total_edges == 0:
        return 0.0
    return same_label_edges / total_edges

def compute_laplacian_matrices(A):
    """
    Tính toán các toán tử phổ đồ thị:
    - Ma trận bậc D
    - Laplacian L = D - A
    - Laplacian chuẩn hóa đối xứng L_sym = D^(-1/2) L D^(-1/2)
    """
    degrees = np.sum(A, axis=1)
    D = np.diag(degrees)
    L = D - A
    
    with np.errstate(divide='ignore'):
        d_inv_sqrt = np.power(degrees, -0.5)
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.0
    D_inv_sqrt = np.diag(d_inv_sqrt)
    
    L_sym = np.eye(len(A)) - D_inv_sqrt @ A @ D_inv_sqrt
    eigenvalues, _ = np.linalg.eigh(L_sym)
    eigenvalues = np.sort(eigenvalues)
    
    return D, L, L_sym, eigenvalues

def build_local_patient_subgraph(query_vector, reference_X, reference_df, k=5, use_clinical=True):
    """
    Tìm k láng giềng gần nhất cho ca bệnh mới và dựng mạng đồ thị con cục bộ
    """
    w_sqrt = np.sqrt(CLINICAL_WEIGHTS) if use_clinical else np.ones_like(CLINICAL_WEIGHTS)
    ref_weighted = reference_X * w_sqrt
    q_weighted = (query_vector * w_sqrt).reshape(1, -1)
    
    nbrs = NearestNeighbors(n_neighbors=k, metric='euclidean').fit(ref_weighted)
    distances, indices = nbrs.kneighbors(q_weighted)
    
    neighbor_indices = indices[0]
    neighbor_distances = distances[0]
    
    G = nx.Graph()
    G.add_node("query", node_type="query", label="Bệnh nhân đang khám")
    
    for idx, (nbr_idx, dist) in enumerate(zip(neighbor_indices, neighbor_distances)):
        row = reference_df.iloc[nbr_idx]
        diag = int(row['diabetes'])
        sim_score = np.exp(- (dist ** 2) / 2.0)
        node_id = f"nbr_{idx+1}"
        code = row.get('patient_code', f"BA-{nbr_idx+1:06d}")
        G.add_node(
            node_id,
            node_type="neighbor",
            patient_id=code,
            diabetes=diag,
            age=float(row['age']),
            bmi=float(row['bmi']),
            hba1c=float(row['HbA1c_level']),
            glucose=float(row['blood_glucose_level']),
            similarity=float(sim_score)
        )
        G.add_edge("query", node_id, weight=sim_score, distance=dist)
        
    # Cạnh giữa các láng giềng
    for i in range(len(neighbor_indices)):
        for j in range(i + 1, len(neighbor_indices)):
            dist_ij = np.linalg.norm(ref_weighted[neighbor_indices[i]] - ref_weighted[neighbor_indices[j]])
            sim_ij = np.exp(- (dist_ij ** 2) / 2.0)
            if sim_ij > 0.4:
                G.add_edge(f"nbr_{i+1}", f"nbr_{j+1}", weight=sim_ij, distance=dist_ij)
                
    return G, neighbor_indices, neighbor_distances

def create_interactive_network_figure(G):
    """
    Vẽ biểu đồ mạng tương tác Plotly chuẩn khoa học (Nền trắng sáng, đường nét rõ ràng)
    """
    pos = nx.spring_layout(G, seed=42, k=0.85)
    
    # Vẽ các cạnh
    edge_x = []
    edge_y = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color="#94A3B8"),
        hoverinfo='none',
        mode='lines'
    )
    
    # Vẽ các đỉnh
    node_x = []
    node_y = []
    node_colors = []
    node_sizes = []
    node_text = []
    node_labels = []
    
    for node, data in G.nodes(data=True):
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        if data.get('node_type') == 'query':
            node_colors.append(THEME_COLORS['primary'])
            node_sizes.append(26)
            node_labels.append("Ca bệnh đang khám")
            node_text.append("<b>[CA BỆNH ĐANG KHÁM]</b><br>Đang định vị tương đồng trong mạng lưới")
        else:
            is_diabetes = (data.get('diabetes') == 1)
            color = THEME_COLORS['diabetes'] if is_diabetes else THEME_COLORS['healthy']
            status_str = "Đái tháo đường" if is_diabetes else "Bình thường"
            node_colors.append(color)
            node_sizes.append(20)
            node_labels.append(data.get('patient_id', 'Láng giềng'))
            hover_info = (
                f"<b>Mã bệnh án: {data.get('patient_id')}</b><br>"
                f"Trạng thái: <b>{status_str}</b><br>"
                f"Độ tương đồng k-NN: <b>{data.get('similarity', 0)*100:.1f}%</b><br>"
                f"HbA1c: {data.get('hba1c')}% | Glucose: {data.get('glucose')} mg/dL<br>"
                f"BMI: {data.get('bmi')} | Tuổi: {data.get('age')}"
            )
            node_text.append(hover_info)
            
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        hovertext=node_text,
        text=node_labels,
        textposition="top center",
        textfont=dict(size=11, color="#1E293B", family="Segoe UI, sans-serif"),
        marker=dict(
            showscale=False,
            color=node_colors,
            size=node_sizes,
            line=dict(width=2, color="#FFFFFF")
        )
    )
    
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            template="plotly_white",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=15, l=15, r=15, t=15),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(color="#0F172A", family="sans-serif"),
            height=380
        )
    )
    return fig
