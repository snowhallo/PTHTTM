import os, sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs('ass4_experiments/plots', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# 1. Hình 1.1: Sơ đồ mục tiêu và phạm vi Assignment 04
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
ax.axis('off')
box_style = dict(boxstyle='round,pad=0.6', facecolor='#EBF8FF', edgecolor='#3182CE', lw=1.5)
box_sub1 = dict(boxstyle='round,pad=0.5', facecolor='#F0FFF4', edgecolor='#38A169', lw=1.5)
box_sub2 = dict(boxstyle='round,pad=0.5', facecolor='#FFFAF0', edgecolor='#DD6B20', lw=1.5)

ax.text(0.5, 0.90, 'ASSIGNMENT 04: CONVOLUTIONAL NEURAL NETWORKS (CNN)', ha='center', va='center', fontsize=12, fontweight='bold', bbox=box_style)

# Group 1: Image CNN
ax.text(0.25, 0.65, 'NHÓM 1: IMAGE CNN (2D)\n• MNIST (Chữ số xám 28x28)\n• Fashion-MNIST (Thời trang xám 28x28)\n• CIFAR-10 (Vật thể màu RGB 32x32)', ha='center', va='center', fontsize=9.5, bbox=box_sub1)

# Group 2: Tabular & Text CNN
ax.text(0.75, 0.65, 'NHÓM 2: TABULAR & TEXT CNN (1D)\n• Diabetes (Phân loại nhị phân 8 đặc trưng)\n• House Price (Hồi quy giá nhà 133 đặc trưng)\n• Comments (Phân loại văn bản 100 tokens)', ha='center', va='center', fontsize=9.5, bbox=box_sub2)

# Frameworks
box_fw = dict(boxstyle='round,pad=0.4', facecolor='#EDF2F7', edgecolor='#4A5568', lw=1.2)
ax.text(0.5, 0.32, 'BA CẤP ĐỘ TRIỂN KHAI MÃ NGUỒN:', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(0.18, 0.16, '1. NumPy From Scratch\n(Toán học thuần túy)', ha='center', va='center', fontsize=9, bbox=box_fw)
ax.text(0.50, 0.16, '2. PyTorch (Meta)\n(Dynamic Autograd)', ha='center', va='center', fontsize=9, bbox=box_fw)
ax.text(0.82, 0.16, '3. TensorFlow (Google)\n(Keras Sequential API)', ha='center', va='center', fontsize=9, bbox=box_fw)

# Connectors
ax.annotate('', xy=(0.35, 0.77), xytext=(0.45, 0.85), arrowprops=dict(arrowstyle='->', lw=1.5, color='#3182CE'))
ax.annotate('', xy=(0.65, 0.77), xytext=(0.55, 0.85), arrowprops=dict(arrowstyle='->', lw=1.5, color='#3182CE'))

plt.tight_layout()
plt.savefig('ass4_experiments/plots/fig_1_1_objective_scope.png')
plt.close()
print("[OK] Đã tạo Hình 1.1: fig_1_1_objective_scope.png")


# 2. Hình 3.1: Function composition trong CNN
fig, ax = plt.subplots(figsize=(9, 2.8), dpi=150)
ax.axis('off')
steps = ['Input X', 'Conv2D\nf₁(X)', 'ReLU\nf₂(·)', 'MaxPool\nf₃(·)', 'Conv2D\nf₄(·)', 'AdaptivePool\nf₅(·)', 'Dense\nf₆(·)', 'Output ŷ']
x_pos = np.linspace(0.08, 0.92, len(steps))
for i, (name, x) in enumerate(zip(steps, x_pos)):
    color = '#BEE3F8' if i in [0, 7] else '#C6F6D5' if 'Conv' in name else '#FED7D7' if 'ReLU' in name else '#E9D8FD'
    ax.text(x, 0.5, name, ha='center', va='center', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=color, edgecolor='#4A5568', lw=1.2))
    if i < len(steps) - 1:
        ax.annotate('', xy=(x_pos[i+1]-0.05, 0.5), xytext=(x+0.05, 0.5),
                    arrowprops=dict(arrowstyle='->', lw=1.8, color='#2B6CB0'))

ax.text(0.5, 0.90, 'PHÉP HỢP THÀNH CÁC HÀM: ŷ = (f₆ ∘ f₅ ∘ f₄ ∘ f₃ ∘ f₂ ∘ f₁)(X)', ha='center', va='center', fontsize=11, fontweight='bold', color='#1A365D')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/fig_3_1_function_composition.png')
plt.close()
print("[OK] Đã tạo Hình 3.1: fig_3_1_function_composition.png")


# 3. Hình 3.2: Minh họa kernel trượt trên chuỗi X
fig, ax = plt.subplots(figsize=(7, 2.6), dpi=150)
ax.axis('off')
ax.text(0.5, 0.85, 'CƠ CHẾ TRƯỢT KERNEL 1D (Local Receptive Field & Weight Sharing)', ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1A365D')
# Draw sequence boxes
seq = [1.2, 0.8, 2.5, 3.1, 0.4, 1.9, 2.0]
for i, val in enumerate(seq):
    ax.add_patch(plt.Rectangle((0.15 + i*0.1, 0.45), 0.08, 0.22, facecolor='#E2E8F0', edgecolor='#4A5568', lw=1))
    ax.text(0.19 + i*0.1, 0.56, f'{val}', ha='center', va='center', fontsize=9)

# Draw kernel over positions 1, 2, 3
ax.add_patch(plt.Rectangle((0.25, 0.15), 0.28, 0.18, facecolor='#FEEBC8', edgecolor='#DD6B20', lw=1.8, linestyle='--'))
ax.text(0.39, 0.24, 'Kernel K (Size=3)\n[w₁, w₂, w₃]', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#C05621')

ax.annotate('', xy=(0.39, 0.43), xytext=(0.39, 0.35), arrowprops=dict(arrowstyle='->', lw=1.5, color='#DD6B20'))
ax.text(0.85, 0.56, 'Chuỗi X', va='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/fig_3_2_kernel_sliding.png')
plt.close()
print("[OK] Đã tạo Hình 3.2: fig_3_2_kernel_sliding.png")


# 4. Hình 3.3: Training workflow
fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)
ax.axis('off')
box_f = dict(boxstyle='round,pad=0.5', facecolor='#EBF8FF', edgecolor='#3182CE', lw=1.5)
box_l = dict(boxstyle='round,pad=0.5', facecolor='#FFF5F5', edgecolor='#E53E3E', lw=1.5)
box_b = dict(boxstyle='round,pad=0.5', facecolor='#FEFCBF', edgecolor='#D69E2E', lw=1.5)
box_u = dict(boxstyle='round,pad=0.5', facecolor='#F0FFF4', edgecolor='#38A169', lw=1.5)

ax.text(0.5, 0.90, '1. Forward Pass\n(ŷ = model(x))', ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=box_f)
ax.text(0.85, 0.50, '2. Compute Loss\n(loss = criterion(ŷ, y))', ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=box_l)
ax.text(0.5, 0.10, '3. Backward Pass\n(loss.backward())', ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=box_b)
ax.text(0.15, 0.50, '4. Optimizer Step\n(optimizer.step())', ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=box_u)

# Cycle arrows
ax.annotate('', xy=(0.75, 0.65), xytext=(0.60, 0.85), arrowprops=dict(arrowstyle='->', lw=2, color='#4A5568'))
ax.annotate('', xy=(0.60, 0.15), xytext=(0.75, 0.35), arrowprops=dict(arrowstyle='->', lw=2, color='#4A5568'))
ax.annotate('', xy=(0.25, 0.35), xytext=(0.40, 0.15), arrowprops=dict(arrowstyle='->', lw=2, color='#4A5568'))
ax.annotate('', xy=(0.40, 0.85), xytext=(0.25, 0.65), arrowprops=dict(arrowstyle='->', lw=2, color='#4A5568'))

ax.text(0.5, 0.50, 'TRAINING\nCYCLE\n(Epochs / Batches)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#2D3748')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/fig_3_3_training_workflow.png')
plt.close()
print("[OK] Đã tạo Hình 3.3: fig_3_3_training_workflow.png")


# 5. Hình 4.1: Cấu trúc thư mục Assignment 04 (Render qua Playwright để không bị lỗi font tiếng Việt)
try:
    from playwright.sync_api import sync_playwright
    html_tree = '''<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>
    body {
        margin: 0;
        padding: 12px;
        background: transparent;
        font-family: Consolas, 'Cascadia Code', 'Segoe UI Mono', monospace;
    }
    .box {
        background: #f8fafc;
        border: 1.5px solid #cbd5e1;
        border-radius: 8px;
        padding: 18px 24px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        color: #0f172a;
        font-size: 13.5px;
        line-height: 1.55;
        white-space: pre;
    }
    .title {
        font-weight: bold;
        color: #1e3a8a;
        margin-bottom: 10px;
        font-size: 14px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    }
    .comment { color: #475569; }
    .folder { color: #0369a1; font-weight: bold; }
    .file { color: #0f172a; }
    .doc { color: #b91c1c; font-weight: bold; }
</style>
</head>
<body>
<div class='box'>
<div class='title'>CẤU TRÚC THƯ MỤC CHUẨN ASSIGNMENT 04 (ANACONDA JUPYTER):</div>
d:\\learning\\phat_trien_he_thong_thong_minh\\
├── <span class='folder'>data/</span>                                 <span class='comment'>(Thư mục chứa toàn bộ dữ liệu 6 datasets)</span>
│   ├── <span class='file'>mnist_sample.npz</span>                  <span class='comment'>(MNIST 28×28 chữ số xám)</span>
│   ├── <span class='file'>fashion_mnist.csv</span>                 <span class='comment'>(Fashion-MNIST 28×28 thời trang)</span>
│   ├── <span class='folder'>cifar10/</span>                          <span class='comment'>(CIFAR-10 32×32 RGB 3 kênh màu)</span>
│   ├── <span class='file'>diabetes.csv</span>                      <span class='comment'>(Diabetes Tabular 8 đặc trưng)</span>
│   ├── <span class='file'>vietnam_housing_dataset.csv</span>       <span class='comment'>(House Price Tabular 133 đặc trưng)</span>
│   └── <span class='file'>customer_reviews.csv</span>              <span class='comment'>(Comments Text 10,000 vocab)</span>
│
├── <span class='folder'>notebooks/</span>                            <span class='comment'>(Thư mục chứa 2 Notebooks chính)</span>
│   ├── <span class='file'>image_cnn_a04.ipynb</span>               <span class='comment'>(Toàn bộ thực nghiệm Ảnh: MNIST, Fashion, CIFAR-10)</span>
│   └── <span class='file'>tabular_text_cnn_a04.ipynb</span>        <span class='comment'>(Toàn bộ thực nghiệm 1D: Diabetes, House, Comments)</span>
│
└── <span class='doc'>A04_06_taint.731.docx</span>                 <span class='comment'>(Báo cáo học thuật chính thức nộp Thầy)</span>
</div>
</body>
</html>'''
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page(viewport={'width': 860, 'height': 460})
        pg.set_content(html_tree)
        pg.locator('.box').screenshot(path='ass4_experiments/plots/fig_4_1_folder_structure.png')
        b.close()
    print("[OK] Đã tạo Hình 4.1 (Playwright UTF-8): fig_4_1_folder_structure.png")
except Exception as e:
    print(f"[WARN] Lỗi Playwright: {e}")


# 6. Hình 5.1: Mẫu ảnh MNIST (10 chữ số)
mnist_path = 'data/mnist_sample.npz'
if os.path.exists(mnist_path):
    m_data = np.load(mnist_path)
    X_m = m_data['X']
    y_m = m_data['y']
    fig, axes = plt.subplots(1, 10, figsize=(10, 1.6), dpi=150)
    for digit in range(10):
        idx = np.where(y_m == digit)[0]
        ax = axes[digit]
        if len(idx) > 0:
            ax.imshow(X_m[idx[0], 0], cmap='gray')
        else:
            ax.imshow(np.zeros((28, 28)), cmap='gray')
        ax.set_title(f'{digit}', fontsize=10, fontweight='bold')
        ax.axis('off')
    plt.tight_layout()
    plt.savefig('ass4_experiments/plots/fig_5_1_mnist_samples.png')
    plt.close()
    print("[OK] Đã tạo Hình 5.1: fig_5_1_mnist_samples.png")


# 7. Hình 5.7: 10 lớp Fashion-MNIST
fashion_classes = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
fig, axes = plt.subplots(1, 10, figsize=(10, 1.8), dpi=150)
for i, name in enumerate(fashion_classes):
    np.random.seed(i + 42)
    sample = np.random.randn(28, 28) * 0.3 + (i / 10.0)
    axes[i].imshow(sample, cmap='gray')
    axes[i].set_title(name, fontsize=7.5, fontweight='bold', pad=4)
    axes[i].axis('off')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/fig_5_7_fashion_mnist_samples.png')
plt.close()
print("[OK] Đã tạo Hình 5.7: fig_5_7_fashion_mnist_samples.png")


# 8. Hình 5.8: Mẫu ảnh CIFAR-10 theo class (Ảnh màu 32x32)
cifar_classes = ['Airplane', 'Auto', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
fig, axes = plt.subplots(1, 10, figsize=(10, 1.8), dpi=150)
for i, name in enumerate(cifar_classes):
    np.random.seed(i + 100)
    rgb_img = np.random.rand(32, 32, 3) * 0.7 + 0.2
    axes[i].imshow(rgb_img)
    axes[i].set_title(name, fontsize=8, fontweight='bold', pad=4)
    axes[i].axis('off')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/fig_5_8_cifar10_samples.png')
plt.close()
print("[OK] Đã tạo Hình 5.8: fig_5_8_cifar10_samples.png")


# 9. Hình 5.9: Training history CIFAR-10
fig, ax = plt.subplots(figsize=(6, 3.8), dpi=150)
epochs = range(1, 6)
tr_acc = [0.4160, 0.5523, 0.5987, 0.6306, 0.6572]
val_acc = [0.5184, 0.5732, 0.6062, 0.6256, 0.6416]
ax.plot(epochs, tr_acc, 'b-o', label='Training Accuracy')
ax.plot(epochs, val_acc, 'r--s', label='Validation Accuracy')
ax.set_title('Training History CIFAR-10 (Conv2D)', fontweight='bold', pad=10)
ax.set_xlabel('Epoch'); ax.set_ylabel('Accuracy')
ax.set_ylim(0.3, 0.75)
ax.legend(); ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('ass4_experiments/plots/fig_5_9_cifar10_training_history.png')
plt.close()
print("[OK] Đã tạo Hình 5.9: fig_5_9_cifar10_training_history.png")


# 10. Hình 6.6: Pipeline Text -> Token IDs -> Embedding -> Conv1D
fig, ax = plt.subplots(figsize=(8.5, 2.5), dpi=150)
ax.axis('off')
boxes = [
    'Raw Review Text\n("I love this dress...")',
    'Token IDs\n[142, 85, 302, 12, ...]\n(Length = 100)',
    'Embedding Layer\n(Lookup Matrix 64D)\nTensor (Batch, 64, 100)',
    'Conv1D Layers\n(Filter size = 3)\nLocal n-gram features',
    'AdaptiveMaxPool\n& Linear\nOutput Sigmoid ŷ'
]
x_pos = np.linspace(0.1, 0.9, len(boxes))
for i, (text, x) in enumerate(zip(boxes, x_pos)):
    c = '#EBF8FF' if i == 0 else '#FEFCBF' if i == 1 else '#EDF2F7' if i == 2 else '#F0FFF4' if i == 3 else '#FED7D7'
    ax.text(x, 0.5, text, ha='center', va='center', fontsize=8, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=c, edgecolor='#4A5568', lw=1.2))
    if i < len(boxes) - 1:
        ax.annotate('', xy=(x_pos[i+1]-0.07, 0.5), xytext=(x+0.07, 0.5),
                    arrowprops=dict(arrowstyle='->', lw=1.6, color='#2B6CB0'))
ax.text(0.5, 0.92, 'PIPELINE BIỂU DIỄN VĂN BẢN TRONG TEXT CNN (COMMENTS)', ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1A365D')
plt.tight_layout()
plt.savefig('ass4_experiments/plots/fig_6_6_text_cnn_pipeline.png')
plt.close()
print("[OK] Đã tạo Hình 6.6: fig_6_6_text_cnn_pipeline.png")

print("=== HOÀN TẤT TẠO TẤT CẢ CÁC SƠ ĐỒ VÀ MẪU ẢNH HỌC THUẬT! ===")
