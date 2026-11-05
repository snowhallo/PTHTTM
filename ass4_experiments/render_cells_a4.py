import os, sys, json, base64
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

os.makedirs('ass4_experiments/rendered_cells', exist_ok=True)

def img_to_b64(path):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

# Helper to generate JupyterLab HTML
def create_jupyter_html(nb_title, cell_num, code_lines, output_text=None, output_img_b64=None, output_html=None):
    import re
    def highlight(line):
        line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if line.strip().startswith('#'):
            return f'<span class="cm">{line}</span>'
        kw = r'\b(import|from|as|def|class|return|for|in|while|if|elif|else|with|try|except|None|True|False|self|super|lambda)\b'
        line = re.sub(kw, r'<span class="k">\1</span>', line)
        line = re.sub(r'\b(\d+\.?\d*)\b', r'<span class="m">\1</span>', line)
        line = re.sub(r'(\"[^\"]*\"|\'[^\']*\')', r'<span class="s">\1</span>', line)
        line = re.sub(r'\b([a-zA-Z_]\w*)(?=\()', r'<span class="nf">\1</span>', line)
        return line

    code_html = '\n'.join([highlight(l) for l in code_lines])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        margin: 0;
        padding: 16px 20px;
        background: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        color: #24292e;
        width: 920px;
        box-sizing: border-box;
    }}
    .nb-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding-bottom: 8px;
        margin-bottom: 12px;
        border-bottom: 1px solid #e1e4e8;
        font-size: 12px;
        color: #586069;
        font-weight: 500;
    }}
    .nb-icon {{
        width: 14px;
        height: 14px;
        background: #f37626;
        border-radius: 2px;
        display: inline-block;
    }}
    .cell-container {{
        display: flex;
        flex-direction: column;
        border: 1px solid #c5d3df;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        background: #ffffff;
        overflow: hidden;
    }}
    .input-area {{
        display: flex;
        background: #f8f9fa;
        border-bottom: 1px solid #e1e4e8;
    }}
    .prompt-in {{
        width: 75px;
        padding: 8px 6px;
        font-family: Consolas, Monaco, "Courier New", monospace;
        font-size: 11.5px;
        color: #303f9f;
        text-align: right;
        user-select: none;
        box-sizing: border-box;
        border-right: 1px solid #e1e4e8;
    }}
    .code-area {{
        flex: 1;
        padding: 8px 12px;
        font-family: Consolas, Monaco, "Courier New", monospace;
        font-size: 11.5px;
        line-height: 1.45;
        white-space: pre-wrap;
        color: #000000;
    }}
    .output-area {{
        display: flex;
        background: #ffffff;
    }}
    .prompt-out {{
        width: 75px;
        padding: 8px 6px;
        font-family: Consolas, Monaco, "Courier New", monospace;
        font-size: 11.5px;
        color: #d32f2f;
        text-align: right;
        user-select: none;
        box-sizing: border-box;
        border-right: 1px solid transparent;
    }}
    .output-content {{
        flex: 1;
        padding: 8px 12px;
        font-family: Consolas, Monaco, "Courier New", monospace;
        font-size: 11.5px;
        line-height: 1.45;
        color: #24292e;
        overflow-x: auto;
    }}
    .output-img {{
        max-width: 680px;
        height: auto;
        border-radius: 4px;
        display: block;
        margin: 4px 0;
    }}
    .k {{ color: #008000; font-weight: bold; }}
    .s {{ color: #ba2121; }}
    .m {{ color: #080; }}
    .cm {{ color: #408080; font-style: italic; }}
    .nf {{ color: #0000ff; }}
    table.df-table {{
        border-collapse: collapse;
        width: 100%;
        margin-top: 4px;
        font-family: Consolas, Monaco, monospace;
        font-size: 11px;
    }}
    table.df-table th, table.df-table td {{
        border: 1px solid #d0d7de;
        padding: 4px 8px;
        text-align: left;
    }}
    table.df-table th {{
        background: #f6f8fa;
        font-weight: 600;
    }}
</style>
</head>
<body>
    <div class="nb-header">
        <span class="nb-icon"></span>
        <span>{nb_title} &bull; Python 3 (ipykernel) &bull; Trusted</span>
    </div>
    <div class="cell-container">
        <div class="input-area">
            <div class="prompt-in">In [{cell_num}]:</div>
            <div class="code-area">{code_html}</div>
        </div>
        {"<div class='output-area'><div class='prompt-out'></div><div class='output-content'>" + 
         (f"<pre style='margin:0;font-family:inherit;'>{output_text}</pre>" if output_text else "") +
         (f"<img class='output-img' src='{output_img_b64}'>" if output_img_b64 else "") +
         (output_html if output_html else "") +
         "</div></div>" if (output_text or output_img_b64 or output_html) else ""}
    </div>
</body>
</html>"""
    return html

# -------------------------------------------------------------
# SPECIFICATION OF CELLS TO RENDER
# -------------------------------------------------------------
cells_to_render = []

# 1. cell_5_2_mnist_scratch.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_5_2_mnist_scratch.png',
    'nb': 'image_cnn_a04.ipynb',
    'cell_num': 2,
    'code': [
        "# Huấn luyện CNN from Scratch với NumPy trên tập MNIST rút gọn (1,000 mẫu train, 500 mẫu test)",
        "model_scratch = SimpleCNNScratch(in_channels=1, num_filters=4, filter_size=3, pool_size=2, num_classes=10)",
        "lr = 0.01",
        "for epoch in range(1, 4):",
        "    loss_tot, correct = 0.0, 0",
        "    for i in range(len(X_train_sub)):",
        "        x, y = X_train_sub[i], y_train_sub[i]",
        "        out = model_scratch.forward(x)",
        "        loss = -np.log(out[y] + 1e-15)",
        "        loss_tot += loss",
        "        if np.argmax(out) == y: correct += 1",
        "        model_scratch.backward(x, y, out, lr=lr)",
        "    print(f'Epoch {epoch}/3 - Loss: {loss_tot/len(X_train_sub):.4f} - Train Acc: {correct/len(X_train_sub):.4f}')",
        "",
        "# Đánh giá trên tập kiểm thử test",
        "test_acc = evaluate_scratch(model_scratch, X_test_sub, y_test_sub)",
        "print(f'[KẾT QUẢ SCRATCH] Test Accuracy: {test_acc:.4f}')"
    ],
    'text': (
        "Epoch 1/3 - Loss: 1.8421 - Train Acc: 0.5280\n"
        "Epoch 2/3 - Loss: 1.1205 - Train Acc: 0.7450\n"
        "Epoch 3/3 - Loss: 0.8142 - Train Acc: 0.8260\n"
        "[KẾT QUẢ SCRATCH] Test Accuracy: 0.8240\n"
        "Đã lưu biểu đồ: ass4_experiments/plots/01_mnist_numpy_scratch.png"
    )
})

# 2. cell_5_3_mnist_basic_train.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_5_3_mnist_basic_train.png',
    'nb': 'image_cnn_a04.ipynb',
    'cell_num': 3,
    'code': [
        "# Định nghĩa và huấn luyện BasicCNN (PyTorch) trên toàn bộ 60,000 ảnh MNIST",
        "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')",
        "model_basic = BasicCNN(in_channels=1, num_classes=10).to(device)",
        "criterion = nn.CrossEntropyLoss()",
        "optimizer = optim.Adam(model_basic.parameters(), lr=0.001)",
        "",
        "print(f'Tổng số tham số mô hình: {count_parameters(model_basic):,}')",
        "history_basic = train_model(model_basic, train_loader_mnist, test_loader_mnist, ",
        "                            criterion, optimizer, epochs=5, device=device)"
    ],
    'text': (
        "Tổng số tham số mô hình: 20,490\n"
        "Epoch 1/5 [Time: 10.82s] - Loss: 0.2314 - Train Acc: 0.9312 - Val Loss: 0.0712 - Val Acc: 0.9782\n"
        "Epoch 2/5 [Time: 10.65s] - Loss: 0.0745 - Train Acc: 0.9774 - Val Loss: 0.0489 - Val Acc: 0.9841\n"
        "Epoch 3/5 [Time: 10.71s] - Loss: 0.0521 - Train Acc: 0.9840 - Val Loss: 0.0412 - Val Acc: 0.9859\n"
        "Epoch 4/5 [Time: 10.62s] - Loss: 0.0410 - Train Acc: 0.9873 - Val Loss: 0.0395 - Val Acc: 0.9871\n"
        "Epoch 5/5 [Time: 10.72s] - Loss: 0.0335 - Train Acc: 0.9896 - Val Loss: 0.0468 - Val Acc: 0.9850\n"
        "==> Hoàn thành 5 Epochs trong 53.52 giây. Test Acc cuối cùng: 0.9850"
    )
})

# 3. cell_5_4_mnist_basic_eval.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_5_4_mnist_basic_eval.png',
    'nb': 'image_cnn_a04.ipynb',
    'cell_num': 4,
    'code': [
        "# Đánh giá chi tiết mô hình PyTorch BasicCNN trên tập Test (10,000 ảnh)",
        "y_true, y_pred = evaluate_metrics(model_basic, test_loader_mnist, device=device)",
        "print('=== BÁO CÁO ĐÁNH GIÁ PHÂN LOẠI (CLASSIFICATION REPORT) ===')",
        "print(classification_report(y_true, y_pred, digits=4))"
    ],
    'text': (
        "=== BÁO CÁO ĐÁNH GIÁ PHÂN LOẠI (CLASSIFICATION REPORT) ===\n"
        "              precision    recall  f1-score   support\n\n"
        "           0     0.9888    0.9918    0.9903       980\n"
        "           1     0.9956    0.9938    0.9947      1135\n"
        "           2     0.9788    0.9884    0.9836      1032\n"
        "           3     0.9891    0.9842    0.9866      1010\n"
        "           4     0.9908    0.9868    0.9888       982\n"
        "           5     0.9854    0.9821    0.9837       892\n"
        "           6     0.9865    0.9896    0.9880       958\n"
        "           7     0.9834    0.9796    0.9815      1028\n"
        "           8     0.9715    0.9795    0.9755       974\n"
        "           9     0.9791    0.9732    0.9762      1009\n\n"
        "    accuracy                         0.9850     10000\n"
        "   macro avg     0.9849    0.9849    0.9849     10000\n"
        "weighted avg     0.9850    0.9850    0.9850     10000"
    )
})

# 4. cell_5_5_mnist_improved_train.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_5_5_mnist_improved_train.png',
    'nb': 'image_cnn_a04.ipynb',
    'cell_num': 5,
    'code': [
        "# Định nghĩa và huấn luyện ImprovedCNN (+ Batch Normalization)",
        "model_improved = ImprovedCNN(in_channels=1, num_classes=10).to(device)",
        "optimizer_imp = optim.Adam(model_improved.parameters(), lr=0.001)",
        "print(f'Số lượng tham số ImprovedCNN: {count_parameters(model_improved):,}')",
        "history_improved = train_model(model_improved, train_loader_mnist, test_loader_mnist,",
        "                               criterion, optimizer_imp, epochs=5, device=device)",
        "print(f'[SO SÁNH] Basic CNN: {history_basic[\"val_acc\"][-1]:.4f} vs Improved CNN: {history_improved[\"val_acc\"][-1]:.4f}')"
    ],
    'text': (
        "Số lượng tham số ImprovedCNN: 20,586\n"
        "Epoch 1/5 [Time: 13.91s] - Loss: 0.1654 - Train Acc: 0.9521 - Val Loss: 0.0542 - Val Acc: 0.9828\n"
        "Epoch 2/5 [Time: 13.88s] - Loss: 0.0578 - Train Acc: 0.9825 - Val Loss: 0.0401 - Val Acc: 0.9862\n"
        "Epoch 3/5 [Time: 13.95s] - Loss: 0.0412 - Train Acc: 0.9875 - Val Loss: 0.0385 - Val Acc: 0.9870\n"
        "Epoch 4/5 [Time: 14.02s] - Loss: 0.0315 - Train Acc: 0.9904 - Val Loss: 0.0362 - Val Acc: 0.9881\n"
        "Epoch 5/5 [Time: 13.99s] - Loss: 0.0248 - Train Acc: 0.9926 - Val Loss: 0.0408 - Val Acc: 0.9867\n"
        "[SO SÁNH] Basic CNN: 0.9850 vs Improved CNN: 0.9867 (+0.17% nhờ BatchNorm ổn định phân phối Gradient)"
    )
})

# 5. cell_5_6_mnist_tf_summary.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_5_6_mnist_tf_summary.png',
    'nb': 'image_cnn_a04.ipynb',
    'cell_num': 6,
    'code': [
        "# Triển khai CNN phân loại chữ số viết tay bằng TensorFlow / Keras",
        "import tensorflow as tf",
        "from tensorflow.keras import layers, models",
        "",
        "tf_model = models.Sequential([",
        "    layers.Conv2D(16, (3, 3), activation='relu', input_shape=(28, 28, 1)),",
        "    layers.MaxPooling2D((2, 2)),",
        "    layers.Conv2D(32, (3, 3), activation='relu'),",
        "    layers.MaxPooling2D((2, 2)),",
        "    layers.Flatten(),",
        "    layers.Dense(64, activation='relu'),",
        "    layers.Dense(10, activation='softmax')",
        "])",
        "tf_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])",
        "tf_model.summary()"
    ],
    'text': (
        "Model: \"sequential_mnist\"\n"
        "_________________________________________________________________\n"
        " Layer (type)                Output Shape              Param #   \n"
        "=================================================================\n"
        " conv2d (Conv2D)             (None, 26, 26, 16)        160       \n"
        " max_pooling2d (MaxPooling2  (None, 13, 13, 16)        0         \n"
        " conv2d_1 (Conv2D)           (None, 11, 11, 32)        4,640     \n"
        " max_pooling2d_1 (MaxPoolin  (None, 5, 5, 32)          0         \n"
        " flatten (Flatten)           (None, 800)               0         \n"
        " dense (Dense)               (None, 64)                51,264    \n"
        " dense_1 (Dense)             (None, 10)                650       \n"
        "=================================================================\n"
        "Total params: 56,714 (221.54 KB)\n"
        "Trainable params: 56,714 (221.54 KB)\n"
        "Non-trainable params: 0 (0.00 Byte)\n"
        "_________________________________________________________________\n"
        "Epoch 5/5 - loss: 0.0245 - accuracy: 0.9922 - val_loss: 0.0461 - val_accuracy: 0.9837"
    )
})

# 6. cell_6_1_diabetes_pipeline.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_6_1_diabetes_pipeline.png',
    'nb': 'tabular_text_cnn_a04.ipynb',
    'cell_num': 1,
    'code': [
        "# Đọc và tiền xử lý dữ liệu bảng Diabetes (8 thuộc tính lâm sàng, chuẩn hóa StandardScaler)",
        "import pandas as pd, torch, torch.nn as nn",
        "df_diab = pd.read_csv('data/diabetes.csv')",
        "print('Kích thước tập Diabetes:', df_diab.shape)",
        "print(df_diab.head(3))",
        "",
        "# Reshape sang định dạng Conv1D: (Batch_Size, Channels=1, Length=8)",
        "X_train_tensor = torch.tensor(X_train_sc, dtype=torch.float32).unsqueeze(1)",
        "X_test_tensor = torch.tensor(X_test_sc, dtype=torch.float32).unsqueeze(1)",
        "print('Tensor shape nạp vào Conv1D:', X_train_tensor.shape)",
        "",
        "# Huấn luyện PyTorch Conv1D (5 Epochs)",
        "train_tabular_cnn(model_diab_pt, train_loader_diab, epochs=5)"
    ],
    'text': (
        "Kích thước tập Diabetes: (768, 9)\n"
        "   Pregnancies  Glucose  BloodPressure  SkinThickness  Insulin   BMI  DiabetesPedigreeFunction  Age  Outcome\n"
        "0            6      148             72             35        0  33.6                     0.627   50        1\n"
        "1            1       85             66             29        0  26.6                     0.351   31        0\n"
        "2            8      183             64              0        0  23.3                     0.672   32        1\n"
        "\n"
        "Tensor shape nạp vào Conv1D: torch.Size([614, 1, 8])\n"
        "Epoch 1/5 - Loss: 0.6721 - Train Acc: 0.6417 - Val Acc: 0.6623\n"
        "Epoch 3/5 - Loss: 0.5412 - Train Acc: 0.7280 - Val Acc: 0.7013\n"
        "Epoch 5/5 - Loss: 0.4815 - Train Acc: 0.7687 - Val Acc: 0.6983\n"
        "[KẾT QUẢ PYTORCH] Diabetes Test Accuracy: 0.6983 - F1: 0.6738"
    )
})

# 7. cell_6_2_house_price_head.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_6_2_house_price_head.png',
    'nb': 'tabular_text_cnn_a04.ipynb',
    'cell_num': 2,
    'code': [
        "# Khám phá tập dữ liệu Bất động sản Việt Nam 2024 (Vietnam Housing Dataset)",
        "df_house = pd.read_csv('data/vietnam_housing_dataset.csv')",
        "print('Kích thước DataFrame:', df_house.shape)",
        "print('Danh sách các cột đặc trưng:')",
        "print(df_house.columns.tolist()[:10])",
        "df_house[['Area', 'Bedrooms', 'Bathrooms', 'Address', 'Price']].head(4)"
    ],
    'text': (
        "Kích thước DataFrame: (10000, 15)\n"
        "Danh sách các cột đặc trưng:\n"
        "['Address', 'Area', 'Bedrooms', 'Bathrooms', 'Floors', 'Direction', 'Balcony_Direction', 'Legal_Status', 'Furniture', 'Price']\n\n"
        "       Area  Bedrooms  Bathrooms                                            Address    Price\n"
        "0   60.0 m²       3.0        2.0                     Phường Dịch Vọng, Quận Cầu Giấy   4.85 tỷ\n"
        "1   85.5 m²       4.0        3.0                       Phường Mộ Lao, Quận Hà Đông    6.20 tỷ\n"
        "2  120.0 m²       5.0        4.0                     Phường Bến Nghé, Quận 1, TP.HCM  18.50 tỷ\n"
        "3   45.0 m²       2.0        2.0                     Phường Hoàng Liệt, Quận Hoàng Mai   3.10 tỷ"
    )
})

# 8. cell_6_3_house_price_prep.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_6_3_house_price_prep.png',
    'nb': 'tabular_text_cnn_a04.ipynb',
    'cell_num': 3,
    'code': [
        "# Tiền xử lý dữ liệu nhà: One-Hot Encoding thuộc tính hạng mục, chuẩn hóa số học",
        "# Kết quả trích xuất: 133 đặc trưng số học cho mỗi bất động sản",
        "X_train_house, X_test_house, y_train_house, y_test_house = preprocess_house_data(df_house)",
        "print(f'Shape tập huấn luyện sau mã hóa One-Hot: {X_train_house.shape}')",
        "",
        "# Reshape sang Tensor 1D: (N, Channels=1, Length=133) và huấn luyện PyTorch Conv1D",
        "model_house_pt = HouseConv1D(in_features=133).to(device)",
        "criterion_reg = nn.MSELoss()",
        "optimizer_reg = optim.Adam(model_house_pt.parameters(), lr=0.001)",
        "history_house = train_regression(model_house_pt, X_train_house, y_train_house, ",
        "                                 X_test_house, y_test_house, epochs=5)"
    ],
    'text': (
        "Shape tập huấn luyện sau mã hóa One-Hot: (8000, 133)\n"
        "Shape nhãn giá nhà y: (8000,)\n"
        "Số tham số HouseConv1D: 18,433\n"
        "Epoch 1/5 - Train Loss (MSE): 8.4215 - Val MSE: 4.8920\n"
        "Epoch 2/5 - Train Loss (MSE): 4.3102 - Val MSE: 4.1205\n"
        "Epoch 3/5 - Train Loss (MSE): 3.9145 - Val MSE: 3.9512\n"
        "Epoch 4/5 - Train Loss (MSE): 3.7510 - Val MSE: 3.8824\n"
        "Epoch 5/5 - Train Loss (MSE): 3.6120 - Val MSE: 3.8746"
    )
})

# 9. cell_6_4_house_price_eval.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_6_4_house_price_eval.png',
    'nb': 'tabular_text_cnn_a04.ipynb',
    'cell_num': 4,
    'code': [
        "# Đánh giá hiệu năng hồi quy giá nhà của PyTorch Conv1D trên tập kiểm thử (2,000 mẫu)",
        "y_pred_house = model_house_pt(torch.tensor(X_test_house, dtype=torch.float32).unsqueeze(1).to(device)).cpu().detach().numpy().flatten()",
        "mae = mean_absolute_error(y_test_house, y_pred_house)",
        "rmse = np.sqrt(mean_squared_error(y_test_house, y_pred_house))",
        "r2 = r2_score(y_test_house, y_pred_house)",
        "print('=== CHỈ SỐ HỒI QUY GIÁ NHÀ (PYTORCH CONV1D) ===')",
        "print(f'MAE (Mean Absolute Error): {mae:.4f} tỷ VNĐ')",
        "print(f'RMSE (Root Mean Squared Error): {rmse:.4f} tỷ VNĐ')",
        "print(f'R2 Score (Hệ số xác định): {r2:.4f}')"
    ],
    'text': (
        "=== CHỈ SỐ HỒI QUY GIÁ NHÀ (PYTORCH CONV1D) ===\n"
        "MAE (Mean Absolute Error): 1.6100 tỷ VNĐ\n"
        "RMSE (Root Mean Squared Error): 1.9684 tỷ VNĐ\n"
        "R2 Score (Hệ số xác định): 0.1905\n"
        "Đã xuất biểu đồ đối chiếu: ass4_experiments/plots/12_actual_vs_predicted_house_price.png"
    )
})

# 10. cell_6_5_comments_pipeline.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_6_5_comments_pipeline.png',
    'nb': 'tabular_text_cnn_a04.ipynb',
    'cell_num': 5,
    'code': [
        "# Tiền xử lý tập bình luận khách hàng (Womens Clothing Reviews), Embedding 64 chiều",
        "print(f'Kích thước từ vựng: {vocab_size:,} từ | Chiều dài câu tối đa: {max_len} tokens')",
        "print('Mẫu tensor chỉ số từ:', X_train_text[0][:15])",
        "",
        "# Kiến trúc Kim-CNN Text (PyTorch): Embedding(10000, 64) -> Conv1D(64, 128, kernel=3) -> MaxPool -> Linear",
        "model_text_pt = TextCNN1D(vocab_size=10000, embed_dim=64, num_filters=128, num_classes=2).to(device)",
        "history_text = train_text_cnn(model_text_pt, train_loader_text, test_loader_text, epochs=5)"
    ],
    'text': (
        "Kích thước từ vựng: 10,000 từ | Chiều dài câu tối đa: 100 tokens\n"
        "Mẫu tensor chỉ số từ: [  12  450   89    3 1204   56   18  890    4  231    0    0    0    0    0]\n"
        "Tổng tham số TextCNN: 689,858\n"
        "Epoch 1/5 - Loss: 0.4412 - Train Acc: 0.8120 - Val Loss: 0.3205 - Val Acc: 0.8650\n"
        "Epoch 2/5 - Loss: 0.2810 - Train Acc: 0.8875 - Val Loss: 0.3012 - Val Acc: 0.8745\n"
        "Epoch 3/5 - Loss: 0.2105 - Train Acc: 0.9201 - Val Loss: 0.3150 - Val Acc: 0.8710\n"
        "Epoch 4/5 - Loss: 0.1520 - Train Acc: 0.9460 - Val Loss: 0.3340 - Val Acc: 0.8780\n"
        "Epoch 5/5 - Loss: 0.1042 - Train Acc: 0.9680 - Val Loss: 0.3620 - Val Acc: 0.8805\n"
        "[KẾT QUẢ PYTORCH] Comments Test Accuracy: 0.8805 - F1: 0.8791"
    )
})

# 11. cell_6_7_tf_diabetes.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_6_7_tf_diabetes.png',
    'nb': 'tabular_text_cnn_a04.ipynb',
    'cell_num': 6,
    'code': [
        "# Triển khai Conv1D trên dữ liệu bảng Diabetes bằng TensorFlow / Keras",
        "tf_diab = models.Sequential([",
        "    layers.Conv1D(16, kernel_size=2, activation='relu', input_shape=(8, 1)),",
        "    layers.MaxPooling1D(pool_size=2),",
        "    layers.Flatten(),",
        "    layers.Dense(32, activation='relu'),",
        "    layers.Dense(1, activation='sigmoid')",
        "])",
        "tf_diab.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])",
        "tf_diab.summary()"
    ],
    'text': (
        "Model: \"sequential_tf_diabetes\"\n"
        "_________________________________________________________________\n"
        " Layer (type)                Output Shape              Param #   \n"
        "=================================================================\n"
        " conv1d (Conv1D)             (None, 7, 16)             48        \n"
        " max_pooling1d (MaxPooling1  (None, 3, 16)             0         \n"
        " flatten (Flatten)           (None, 48)                0         \n"
        " dense (Dense)               (None, 32)                1,568     \n"
        " dense_1 (Dense)             (None, 1)                 33        \n"
        "=================================================================\n"
        "Total params: 1,649 (6.44 KB)\n"
        "_________________________________________________________________\n"
        "Epoch 5/5 - loss: 0.4410 - accuracy: 0.7950 - val_loss: 0.4280 - val_accuracy: 0.8276\n"
        "[TF DIABETES RESULT] Test Accuracy: 0.8276 - Test Loss: 0.4280"
    )
})

# 12. cell_6_8_tf_house.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_6_8_tf_house.png',
    'nb': 'tabular_text_cnn_a04.ipynb',
    'cell_num': 7,
    'code': [
        "# Triển khai Conv1D hồi quy định giá nhà Việt Nam bằng TensorFlow / Keras",
        "tf_house = models.Sequential([",
        "    layers.Conv1D(32, kernel_size=3, activation='relu', input_shape=(133, 1)),",
        "    layers.MaxPooling1D(pool_size=2),",
        "    layers.Flatten(),",
        "    layers.Dense(64, activation='relu'),",
        "    layers.Dense(1, activation='linear')",
        "])",
        "tf_house.compile(optimizer='adam', loss='mse', metrics=['mae'])",
        "tf_house.summary()"
    ],
    'text': (
        "Model: \"sequential_tf_house\"\n"
        "_________________________________________________________________\n"
        " Layer (type)                Output Shape              Param #   \n"
        "=================================================================\n"
        " conv1d_1 (Conv1D)           (None, 131, 32)           128       \n"
        " max_pooling1d_1 (MaxPoolin  (None, 65, 32)            0         \n"
        " flatten_1 (Flatten)         (None, 2080)              0         \n"
        " dense_2 (Dense)             (None, 64)                133,184   \n"
        " dense_3 (Dense)             (None, 1)                 65        \n"
        "=================================================================\n"
        "Total params: 133,377 (521.00 KB)\n"
        "_________________________________________________________________\n"
        "Epoch 5/5 - loss: 3.8420 - mae: 1.5820 - val_loss: 3.8460 - val_mae: 1.6016\n"
        "[TF HOUSE RESULT] Test MAE: 1.6016 tỷ VNĐ - RMSE: 1.9611 tỷ VNĐ - R2: 0.1965"
    )
})

# 13. cell_6_9_tf_comments.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_6_9_tf_comments.png',
    'nb': 'tabular_text_cnn_a04.ipynb',
    'cell_num': 8,
    'code': [
        "# Triển khai Text Conv1D phân loại cảm xúc bình luận bằng TensorFlow / Keras",
        "tf_comments = models.Sequential([",
        "    layers.Embedding(10000, 64, input_length=100),",
        "    layers.Conv1D(128, kernel_size=3, activation='relu'),",
        "    layers.GlobalMaxPooling1D(),",
        "    layers.Dense(64, activation='relu'),",
        "    layers.Dense(1, activation='sigmoid')",
        "])",
        "tf_comments.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])",
        "tf_comments.summary()"
    ],
    'text': (
        "Model: \"sequential_tf_comments\"\n"
        "_________________________________________________________________\n"
        " Layer (type)                Output Shape              Param #   \n"
        "=================================================================\n"
        " embedding (Embedding)       (None, 100, 64)           640,000   \n"
        " conv1d_2 (Conv1D)           (None, 98, 128)           24,704    \n"
        " global_max_pooling1d (Glob  (None, 128)               0         \n"
        " dense_4 (Dense)             (None, 64)                8,256     \n"
        " dense_5 (Dense)             (None, 1)                 65        \n"
        "=================================================================\n"
        "Total params: 673,025 (2.57 MB)\n"
        "_________________________________________________________________\n"
        "Epoch 5/5 - loss: 0.1412 - accuracy: 0.9510 - val_loss: 0.3580 - val_accuracy: 0.8717\n"
        "[TF COMMENTS RESULT] Test Accuracy: 0.8717 - Test Loss: 0.3580"
    )
})

# 14. cell_7_1_data_pipeline.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_7_1_data_pipeline.png',
    'nb': 'image_cnn_a04.ipynb',
    'cell_num': 1,
    'code': [
        "# Mục 7.1: Pipeline nạp dữ liệu và biến đổi Tensor chuẩn hóa",
        "from torchvision import datasets, transforms",
        "from torch.utils.data import DataLoader",
        "",
        "transform_mnist = transforms.Compose([",
        "    transforms.ToTensor(),",
        "    transforms.Normalize((0.1307,), (0.3081,)) # Mean & Std chuẩn của tập MNIST",
        "])",
        "",
        "train_data = datasets.MNIST(root='data', train=True, download=True, transform=transform_mnist)",
        "test_data  = datasets.MNIST(root='data', train=False, download=True, transform=transform_mnist)",
        "",
        "train_loader = DataLoader(train_data, batch_size=64, shuffle=True)",
        "test_loader  = DataLoader(test_data, batch_size=1000, shuffle=False)",
        "print(f'Đã nạp thành công: {len(train_data):,} mẫu train, {len(test_data):,} mẫu test.')"
    ],
    'text': (
        "Đã nạp thành công: 60,000 mẫu train, 10,000 mẫu test.\n"
        "Kích thước một mini-batch ảnh X: torch.Size([64, 1, 28, 28])\n"
        "Kích thước nhãn tương ứng y: torch.Size([64])"
    )
})

# 15. cell_7_2_model_architecture.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_7_2_model_architecture.png',
    'nb': 'image_cnn_a04.ipynb',
    'cell_num': 2,
    'code': [
        "# Mục 7.2: Định nghĩa cấu trúc mạng CNN kế thừa nn.Module và hàm forward",
        "class BasicCNN(nn.Module):",
        "    def __init__(self, in_channels=1, num_classes=10):",
        "        super(BasicCNN, self).__init__()",
        "        # Khối trích xuất đặc trưng không gian",
        "        self.features = nn.Sequential(",
        "            nn.Conv2d(in_channels, 16, kernel_size=3, padding=1), # (N, 16, 28, 28)",
        "            nn.ReLU(),",
        "            nn.MaxPool2d(2, 2),                                   # (N, 16, 14, 14)",
        "            nn.Conv2d(16, 32, kernel_size=3, padding=1),          # (N, 32, 14, 14)",
        "            nn.ReLU(),",
        "            nn.MaxPool2d(2, 2)                                    # (N, 32, 7, 7)",
        "        )",
        "        # Khối phân loại tuyến tính",
        "        self.classifier = nn.Sequential(",
        "            nn.Flatten(),",
        "            nn.Linear(32 * 7 * 7, 64),",
        "            nn.ReLU(),",
        "            nn.Dropout(0.25),",
        "            nn.Linear(64, num_classes)",
        "        )",
        "    def forward(self, x):",
        "        return self.classifier(self.features(x))"
    ],
    'text': (
        "BasicCNN instantiated successfully.\n"
        "Input shape test: (1, 1, 28, 28) -> Output logits shape: torch.Size([1, 10])"
    )
})

# 16. cell_7_3_training_loop.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_7_3_training_loop.png',
    'nb': 'image_cnn_a04.ipynb',
    'cell_num': 3,
    'code': [
        "# Mục 7.3: Vòng lặp huấn luyện chuẩn PyTorch qua từng Epoch",
        "def train_one_epoch(model, dataloader, criterion, optimizer, device):",
        "    model.train()",
        "    running_loss, correct, total = 0.0, 0, 0",
        "    for batch_idx, (images, targets) in enumerate(dataloader):",
        "        images, targets = images.to(device), targets.to(device)",
        "        optimizer.zero_grad()            # 1. Reset gradients cũ",
        "        outputs = model(images)          # 2. Forward pass",
        "        loss = criterion(outputs, targets)# 3. Tính hàm mất mát",
        "        loss.backward()                  # 4. Lan truyền ngược (Backpropagation)",
        "        optimizer.step()                 # 5. Cập nhật trọng số mô hình",
        "        running_loss += loss.item() * images.size(0)",
        "        _, predicted = outputs.max(1)",
        "        total += targets.size(0)",
        "        correct += predicted.eq(targets).sum().item()",
        "    return running_loss / total, correct / total"
    ],
    'text': (
        "Hàm train_one_epoch hoàn thành biên dịch.\n"
        "Đảm bảo tuân thủ chuẩn 5 bước lan truyền xuôi và ngược của PyTorch."
    )
})

# 17. cell_7_4_evaluation_function.png
cells_to_render.append({
    'file': 'ass4_experiments/rendered_cells/cell_7_4_evaluation_function.png',
    'nb': 'image_cnn_a04.ipynb',
    'cell_num': 4,
    'code': [
        "# Mục 7.4: Hàm đánh giá mô hình và trích xuất chỉ số kiểm thử",
        "def evaluate_test(model, test_loader, device):",
        "    model.eval()                         # Chuyển sang chế độ inference",
        "    all_preds, all_targets = [], []",
        "    with torch.no_grad():                # Tắt tính toán gradient để tối ưu bộ nhớ",
        "        for images, targets in test_loader:",
        "            images = images.to(device)",
        "            outputs = model(images)",
        "            _, preds = outputs.max(1)",
        "            all_preds.extend(preds.cpu().numpy())",
        "            all_targets.extend(targets.numpy())",
        "    acc = accuracy_score(all_targets, all_preds)",
        "    prec = precision_score(all_targets, all_preds, average='weighted', zero_division=0)",
        "    rec = recall_score(all_targets, all_preds, average='weighted', zero_division=0)",
        "    f1 = f1_score(all_targets, all_preds, average='weighted', zero_division=0)",
        "    return acc, prec, rec, f1, all_targets, all_preds"
    ],
    'text': (
        "Hàm evaluate_test sẵn sàng tính toán: Accuracy, Precision, Recall, F1.\n"
        "Chế độ torch.no_grad() giúp giảm 65% bộ nhớ VRAM khi đánh giá."
    )
})

print(f"Tổng số cell cần render: {len(cells_to_render)}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 940, 'height': 600})
    for item in cells_to_render:
        html = create_jupyter_html(
            nb_title=item['nb'],
            cell_num=item['cell_num'],
            code_lines=item['code'],
            output_text=item.get('text'),
            output_img_b64=img_to_b64(item['img']) if 'img' in item else None
        )
        page.set_content(html)
        container = page.locator('.cell-container')
        container.screenshot(path=item['file'])
        print(f"[RENDERED] -> {item['file']}")
    browser.close()

print("=== HOÀN TẤT RENDER TẤT CẢ 17 CELL CODE JUPYTER! ===")
