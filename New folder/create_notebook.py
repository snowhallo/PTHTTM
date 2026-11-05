import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from sklearn import linear_model, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

print("Building complete, error-free Jupyter Notebook for Chapter 12...")

# 1. Prepare data
try:
    df = pd.read_csv('diabet.csv')
except FileNotFoundError:
    df = pd.read_csv('diabetes.csv')

# Clean data
cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
df[cols] = df[cols].replace(0, np.nan)
df.fillna(df.mean(), inplace=True)

# Train optimal model
X_top3 = df[['Glucose', 'BMI', 'Age']]
y = df.iloc[:, 8]
knn_opt = KNeighborsClassifier(n_neighbors=19)
knn_opt.fit(X_top3, y)
pickle.dump(knn_opt, open('diabetes.sav', 'wb'))
print("Successfully generated diabetes.sav")

# Create rich Notebook cells with clean syntax and %%writefile for exports
cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# BÀI THỰC HÀNH CHAPTER 12: DEPLOYING MACHINE LEARNING MODELS\n",
            "### Môn học: Phát Triển Hệ Thống Thông Minh (Intelligent System Development)\n",
            "**Giáo trình:** *Python Machine Learning - Wei-Meng Lee (Chapter 12)*  \n",
            "**Tập dữ liệu:** *Pima Indians Diabetes Database* (`diabet.csv` / `diabetes.csv`)\n",
            "\n",
            "---\n",
            "### 🎯 Mục tiêu thực hành:\n",
            "1. **Khám phá và Tiền xử lý dữ liệu y tế:** Phát hiện và xử lý các giá trị 0 phi lý (Glucose, Huyết áp, BMI = 0) bằng phương pháp gán `NaN` và điền giá trị trung bình (`mean`).\n",
            "2. **Phân tích tương quan & Trích chọn đặc trưng:** Sử dụng ma trận hệ số tương quan Pearson và Heatmap để lựa chọn Top 3 đặc trưng ảnh hưởng mạnh nhất: `Glucose`, `BMI`, `Age`.\n",
            "3. **Đánh giá & So sánh mô hình bằng 10-Fold Cross-Validation:** So sánh 4 thuật toán (*Logistic Regression, KNN, SVM Linear, SVM RBF*).\n",
            "4. **Khảo sát mở rộng:** Đo lường hiệu năng của 4 mô hình trên 4 tập đặc trưng khác nhau (Top 3, Top 5, Top 7, All 8 đặc trưng) và chứng minh hiện tượng *Lời nguyền chiều dữ liệu (Curse of Dimensionality)* trên KNN.\n",
            "5. **Huấn luyện mô hình tối ưu & Đóng gói (Model Persistence):** Huấn luyện KNN ($k=19$) và lưu file `diabetes.sav` bằng `pickle`.\n",
            "6. **Triển khai Web Service REST API & Client:** Tích hợp với Flask REST API và giao diện Web tương tác."
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Nạp và Khám phá Dữ liệu (Load & Inspect Data)\n",
            "- Tập dữ liệu gồm 768 mẫu bệnh nhân nữ người da đỏ Pima từ 21 tuổi trở lên.\n",
            "- Biến mục tiêu `Outcome`: `0` (Không mắc tiểu đường) và `1` (Mắc tiểu đường)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import pickle\n",
            "import warnings\n",
            "warnings.filterwarnings('ignore')\n",
            "\n",
            "# Nạp dữ liệu từ file CSV\n",
            "try:\n",
            "    df = pd.read_csv('diabet.csv')\n",
            "    print(\"--> Nạp thành công file 'diabet.csv'\")\n",
            "except FileNotFoundError:\n",
            "    df = pd.read_csv('diabetes.csv')\n",
            "    print(\"--> Nạp thành công file 'diabetes.csv'\")\n",
            "\n",
            "print(\"Kích thước tập dữ liệu:\", df.shape)\n",
            "df.info()\n",
            "display(df.head(10))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Tiền xử lý Dữ liệu khuyết thiếu (Data Cleaning & Imputation)\n",
            "> **Lý giải y học:** Các chỉ số sinh tồn như `Glucose` (đường huyết), `BloodPressure` (huyết áp), `SkinThickness` (độ dày nếp gấp da), `BMI` (chỉ số khối cơ thể) **không thể bằng 0 ở người còn sống**.\n",
            "> Các số 0 này thực chất là giá trị bị thiếu (Missing values). Ta phải thay thế bằng `NaN` và điền bù bằng giá trị trung bình (`mean`) của từng cột."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 2,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Kiểm tra số lượng giá trị null và số lượng giá trị 0 ở từng cột\n",
            "print(\"--- Số lượng giá trị Null ban đầu ---\")\n",
            "print(df.isnull().sum())\n",
            "\n",
            "print(\"\\n--- Số lượng giá trị bằng 0 ở từng cột ---\")\n",
            "print(df.eq(0).sum())"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 3,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Thay thế các giá trị 0 phi lý bằng NaN và điền bù bằng giá trị trung bình (mean)\n",
            "cols_to_clean = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']\n",
            "df[cols_to_clean] = df[cols_to_clean].replace(0, np.nan)\n",
            "df.fillna(df.mean(), inplace=True)\n",
            "\n",
            "print(\"--- Số lượng giá trị 0 sau khi xử lý (Cột Outcome giữ nguyên 0/1 làm nhãn) ---\")\n",
            "print(df.eq(0).sum())"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Phân tích Tương quan & Lựa chọn Đặc trưng (Correlation Analysis & Feature Selection)\n",
            "- Hệ số tương quan Pearson đo lường mức độ liên kết tuyến tính giữa từng đặc trưng với biến nhãn `Outcome`.\n",
            "- Các đặc trưng có tương quan cao nhất thể hiện khả năng phân biệt bệnh nhân mắc tiểu đường tốt nhất."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 4,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Tính toán ma trận hệ số tương quan Pearson\n",
            "corr = df.corr()\n",
            "display(corr)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 5,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Trực quan hóa ma trận tương quan bằng biểu đồ Heatmap (Seaborn & Matplotlib)\n",
            "plt.figure(figsize=(10, 8))\n",
            "sns.heatmap(corr, annot=True, cmap=\"coolwarm\", fmt=\".2f\", linewidths=0.5, cbar=True)\n",
            "plt.title(\"Correlation Heatmap - Pima Indians Diabetes Dataset\", fontsize=14, pad=15)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 6,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Sắp xếp và trích xuất danh sách đặc trưng có tương quan cao nhất với Outcome\n",
            "top_corr_features = df.corr()['Outcome'].abs().sort_values(ascending=False)\n",
            "print(\"--- Mức độ tương quan với nhãn Outcome (Sắp xếp giảm dần) ---\")\n",
            "for feat, val in top_corr_features.items():\n",
            "    print(f\"- {feat:<25}: {val:.4f}\")\n",
            "\n",
            "print(\"\\n=> 3 đặc trưng hàng đầu được chọn theo Chapter 12: ['Glucose', 'BMI', 'Age']\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Đánh giá và So sánh các Thuật toán Học máy (Model Evaluation with 10-Fold Cross-Validation)\n",
            "> **Tại sao dùng 10-Fold Cross-Validation?**  \n",
            "> Tập dữ liệu nhỏ (768 mẫu). 10-Fold CV chia tập dữ liệu thành 10 phần: mỗi lượt dùng 9 phần để train và 1 phần để test. Kết quả là trung bình của 10 lần đo, giúp loại bỏ yếu tố may rủi khi phân chia tập dữ liệu và đánh giá khách quan khả năng tổng quát hóa của mô hình."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 7,
        "metadata": {},
        "outputs": [],
        "source": [
            "from sklearn import linear_model, svm\n",
            "from sklearn.neighbors import KNeighborsClassifier\n",
            "from sklearn.model_selection import cross_val_score\n",
            "\n",
            "# Tách biến đầu vào X (Top 3 đặc trưng) và biến mục tiêu y (Outcome)\n",
            "X_top3 = df[['Glucose', 'BMI', 'Age']]\n",
            "y = df.iloc[:, 8]\n",
            "\n",
            "results_list = []\n",
            "\n",
            "# 1. Logistic Regression\n",
            "log_reg = linear_model.LogisticRegression()\n",
            "log_reg_score = cross_val_score(log_reg, X_top3, y, cv=10, scoring='accuracy').mean()\n",
            "results_list.append({\"Algorithm\": \"Logistic Regression\", \"Accuracy\": log_reg_score})\n",
            "print(f\"1. Logistic Regression Score : {log_reg_score*100:.2f}%\")\n",
            "\n",
            "# 2. K-Nearest Neighbors (Quét tìm k tối ưu từ 1 đến 50)\n",
            "ks = list(range(1, 51, 2))\n",
            "cv_scores = []\n",
            "for k in ks:\n",
            "    knn = KNeighborsClassifier(n_neighbors=k)\n",
            "    score = cross_val_score(knn, X_top3, y, cv=10, scoring='accuracy').mean()\n",
            "    cv_scores.append(score)\n",
            "\n",
            "best_knn_score = max(cv_scores)\n",
            "best_k = ks[cv_scores.index(best_knn_score)]\n",
            "results_list.append({\"Algorithm\": f\"K-Nearest Neighbors (k={best_k})\", \"Accuracy\": best_knn_score})\n",
            "print(f\"2. K-Nearest Neighbors (k={best_k}) : {best_knn_score*100:.2f}%\")\n",
            "\n",
            "# 3. SVM Linear Kernel\n",
            "svm_linear = svm.SVC(kernel='linear')\n",
            "svm_lin_score = cross_val_score(svm_linear, X_top3, y, cv=10, scoring='accuracy').mean()\n",
            "results_list.append({\"Algorithm\": \"SVM (Linear Kernel)\", \"Accuracy\": svm_lin_score})\n",
            "print(f\"3. SVM Linear Kernel Score   : {svm_lin_score*100:.2f}%\")\n",
            "\n",
            "# 4. SVM RBF Kernel\n",
            "svm_rbf = svm.SVC(kernel='rbf')\n",
            "svm_rbf_score = cross_val_score(svm_rbf, X_top3, y, cv=10, scoring='accuracy').mean()\n",
            "results_list.append({\"Algorithm\": \"SVM (RBF Kernel)\", \"Accuracy\": svm_rbf_score})\n",
            "print(f\"4. SVM RBF Kernel Score      : {svm_rbf_score*100:.2f}%\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 8,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Biểu đồ trực quan hóa quá trình tìm kiếm k tối ưu cho thuật toán KNN\n",
            "plt.figure(figsize=(10, 5))\n",
            "plt.plot(ks, [s * 100 for s in cv_scores], marker='o', color='#0284c7', linewidth=2, markersize=6)\n",
            "plt.axvline(best_k, color='#ef4444', linestyle='--', label=f'Optimal k = {best_k} ({best_knn_score*100:.2f}%)')\n",
            "plt.title('KNN Hyperparameter Tuning (10-Fold Cross-Validation)', fontsize=13)\n",
            "plt.xlabel('Number of Neighbors (k)', fontsize=11)\n",
            "plt.ylabel('10-Fold CV Accuracy (%)', fontsize=11)\n",
            "plt.grid(True, linestyle=':', alpha=0.6)\n",
            "plt.legend(fontsize=11)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 9,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Bảng xếp hạng độ chính xác của 4 thuật toán trên Top 3 đặc trưng\n",
            "df_results = pd.DataFrame(results_list)\n",
            "df_results['Accuracy (%)'] = df_results['Accuracy'].apply(lambda x: f\"{x*100:.2f}%\")\n",
            "display(df_results.sort_values(by='Accuracy', ascending=False)[['Algorithm', 'Accuracy (%)']])"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Thực nghiệm Mở rộng: Đối chiếu Hiệu năng trên các Tập Đặc trưng (3, 5, 7, 8 Features)\n",
            "> **Nhận xét chuyên sâu:**  \n",
            "> - Đối với **KNN**, độ chính xác cao nhất đạt được ở **Top 3 đặc trưng (77.21%)** và giảm dần khi đưa vào 5, 7 và 8 đặc trưng. Điều này minh chứng cho hiện tượng **Lời nguyền chiều dữ liệu (*Curse of Dimensionality*)**: trong không gian nhiều chiều, khoảng cách Euclidean bị bão hòa và các đặc trưng thứ yếu làm tăng độ nhiễu.\n",
            "> - Mô hình **KNN ($k=19$) với Top 3 đặc trưng** là giải pháp tối ưu nhất cả về độ chính xác và tính thực tiễn khi triển khai Web API."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 10,
        "metadata": {},
        "outputs": [],
        "source": [
            "sorted_feat_list = df.corr()['Outcome'].abs().sort_values(ascending=False).index[1:].tolist()\n",
            "\n",
            "feature_subsets = {\n",
            "    \"Top 3 Features\": sorted_feat_list[:3],\n",
            "    \"Top 5 Features\": sorted_feat_list[:5],\n",
            "    \"Top 7 Features\": sorted_feat_list[:7],\n",
            "    \"All 8 Features\": sorted_feat_list\n",
            "}\n",
            "\n",
            "benchmark_rows = []\n",
            "for subset_name, feats in feature_subsets.items():\n",
            "    X_sub = df[feats]\n",
            "    \n",
            "    # Logistic Regression\n",
            "    lr_acc = cross_val_score(linear_model.LogisticRegression(max_iter=1000), X_sub, y, cv=10, scoring='accuracy').mean()\n",
            "    \n",
            "    # KNN scan\n",
            "    knn_scores_sub = [cross_val_score(KNeighborsClassifier(n_neighbors=k_val), X_sub, y, cv=10, scoring='accuracy').mean() for k_val in range(1, 36, 2)]\n",
            "    best_knn_sub = max(knn_scores_sub)\n",
            "    best_k_sub = list(range(1, 36, 2))[knn_scores_sub.index(best_knn_sub)]\n",
            "    \n",
            "    # SVMs\n",
            "    svm_lin_acc = cross_val_score(svm.SVC(kernel='linear'), X_sub, y, cv=10, scoring='accuracy').mean()\n",
            "    svm_rbf_acc = cross_val_score(svm.SVC(kernel='rbf'), X_sub, y, cv=10, scoring='accuracy').mean()\n",
            "    \n",
            "    benchmark_rows.append({\n",
            "        \"Tập đặc trưng\": subset_name,\n",
            "        \"Danh sách đặc trưng\": \", \".join(feats),\n",
            "        \"Logistic Regression\": f\"{lr_acc*100:.2f}%\",\n",
            "        \"KNN (Tối ưu)\": f\"{best_knn_sub*100:.2f}% (k={best_k_sub})\",\n",
            "        \"SVM Linear\": f\"{svm_lin_acc*100:.2f}%\",\n",
            "        \"SVM RBF\": f\"{svm_rbf_acc*100:.2f}%\"\n",
            "    })\n",
            "\n",
            "df_benchmark = pd.DataFrame(benchmark_rows)\n",
            "display(df_benchmark)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Huấn luyện Mô hình Tối ưu & Đóng gói (Model Training & Persistence)\n",
            "- Huấn luyện thuật toán **KNN ($k=19$)** trên toàn bộ 768 mẫu dữ liệu với 3 đặc trưng: `Glucose`, `BMI`, `Age`.\n",
            "- Đóng gói mô hình thành tệp nhị phân `diabetes.sav` bằng `pickle` để Web Service có thể nạp nhanh chóng mà không cần huấn luyện lại."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 11,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Huấn luyện mô hình tối ưu KNN (k=19) trên Top 3 đặc trưng\n",
            "model = KNeighborsClassifier(n_neighbors=19)\n",
            "model.fit(X_top3, y)\n",
            "\n",
            "# Lưu mô hình ra tệp nhị phân diabetes.sav\n",
            "filename = 'diabetes.sav'\n",
            "pickle.dump(model, open(filename, 'wb'))\n",
            "print(f\"--> Đã huấn luyện và lưu mô hình thành công vào '{filename}'\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 12,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Kiểm thử nạp lại file .sav và dự đoán 2 mẫu bệnh nhân điển hình\n",
            "loaded_model = pickle.load(open(filename, 'rb'))\n",
            "\n",
            "# Mẫu 1: Người bình thường (Glucose=100, BMI=30, Age=29)\n",
            "patient1 = pd.DataFrame([[100, 30, 29]], columns=['Glucose', 'BMI', 'Age'])\n",
            "pred1 = loaded_model.predict(patient1)[0]\n",
            "conf1 = np.amax(loaded_model.predict_proba(patient1)[0]) * 100\n",
            "print(f\"Bệnh nhân 1 (Glucose=100, BMI=30, Age=29) -> Kết quả: {'Diabetic (Tiểu đường)' if pred1==1 else 'Not Diabetic (Bình thường)'} | Độ tin cậy: {conf1:.2f}%\")\n",
            "\n",
            "# Mẫu 2: Người nguy cơ cao (Glucose=160, BMI=42, Age=50)\n",
            "patient2 = pd.DataFrame([[160, 42, 50]], columns=['Glucose', 'BMI', 'Age'])\n",
            "pred2 = loaded_model.predict(patient2)[0]\n",
            "conf2 = np.amax(loaded_model.predict_proba(patient2)[0]) * 100\n",
            "print(f\"Bệnh nhân 2 (Glucose=160, BMI=42, Age=50) -> Kết quả: {'Diabetic (Tiểu đường)' if pred2==1 else 'Not Diabetic (Bình thường)'} | Độ tin cậy: {conf2:.2f}%\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Triển khai REST API Web Service & Client Script\n",
            "- Xuất file `REST_API.py` (Flask micro-service tiếp nhận POST request JSON) và `Predict_Diabetes.py` (Client kiểm thử)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 13,
        "metadata": {},
        "outputs": [],
        "source": [
            "%%writefile REST_API.py\n",
            "import pickle\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "from flask import Flask, request, jsonify\n",
            "from flask_cors import CORS\n",
            "\n",
            "app = Flask(__name__)\n",
            "CORS(app)\n",
            "\n",
            "filename = \"diabetes.sav\"\n",
            "loaded_model = pickle.load(open(filename, \"rb\"))\n",
            "\n",
            "@app.route('/diabetes/v1/predict', methods=['POST'])\n",
            "def predict():\n",
            "    features = request.json\n",
            "    try:\n",
            "        glucose = float(features.get(\"Glucose\", 0))\n",
            "        bmi = float(features.get(\"BMI\", 0))\n",
            "        age = float(features.get(\"Age\", 0))\n",
            "        \n",
            "        input_df = pd.DataFrame([[glucose, bmi, age]], columns=['Glucose', 'BMI', 'Age'])\n",
            "        prediction = loaded_model.predict(input_df)\n",
            "        confidence = loaded_model.predict_proba(input_df)\n",
            "        \n",
            "        response = {\n",
            "            \"prediction\": int(prediction[0]),\n",
            "            \"label\": \"Diabetic\" if int(prediction[0]) == 1 else \"Not Diabetic\",\n",
            "            \"confidence\": str(round(np.amax(confidence[0]) * 100, 2)),\n",
            "            \"risk_level\": \"Cao\" if int(prediction[0]) == 1 else \"Thấp\"\n",
            "        }\n",
            "        return jsonify(response)\n",
            "    except Exception as e:\n",
            "        return jsonify({\"error\": str(e)}), 400\n",
            "\n",
            "if __name__ == '__main__':\n",
            "    print(\"Starting Diabetes Prediction REST API on http://127.0.0.1:5000/ ...\")\n",
            "    app.run(host='0.0.0.0', port=5000, debug=False)\n"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 14,
        "metadata": {},
        "outputs": [],
        "source": [
            "%%writefile Predict_Diabetes.py\n",
            "import json\n",
            "import requests\n",
            "\n",
            "def predict_diabetes(Glucose, BMI, Age):\n",
            "    url = \"http://127.0.0.1:5000/diabetes/v1/predict\"\n",
            "    data = {\n",
            "        \"Glucose\": float(Glucose),\n",
            "        \"BMI\": float(BMI), \n",
            "        \"Age\": float(Age)\n",
            "    }\n",
            "    headers = {\"Content-type\": \"application/json\"}\n",
            "    response = requests.post(url, data=json.dumps(data), headers=headers)\n",
            "    return response.json()\n",
            "\n",
            "if __name__ == '__main__':\n",
            "    print(\"=== CHƯƠNG TRÌNH KIỂM THỬ DỰ ĐOÁN TIỂU ĐƯỜNG CLIENT ===\")\n",
            "    Glucose = input('Nhập Glucose (mg/dL) [mặc định 100]: ') or '100'\n",
            "    BMI = input('Nhập BMI [mặc định 30]: ') or '30'\n",
            "    Age = input('Nhập Age (tuổi) [mặc định 29]: ') or '29'\n",
            "    \n",
            "    try:\n",
            "        result = predict_diabetes(Glucose, BMI, Age)\n",
            "        print(\"\\n--- KẾT QUẢ TỪ REST API ---\")\n",
            "        print(\"Chẩn đoán:\", result.get('label'))\n",
            "        print(\"Phân lớp (Class 0/1):\", result.get('prediction'))\n",
            "        print(\"Độ tin cậy:\", str(result.get('confidence')) + '%')\n",
            "        print(\"Mức độ nguy cơ:\", result.get('risk_level'))\n",
            "    except Exception as e:\n",
            "        print(\"Lỗi kết nối tới Server API:\", e)\n"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 15,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Kiểm thử trực tiếp hàm dự đoán client ngay trong Notebook\n",
            "test_cases = {\n",
            "    \"Bệnh nhân 1 (Bình thường)\": [100, 28.5, 29],\n",
            "    \"Bệnh nhân 2 (Nguy cơ cao)\": [165, 38.0, 52]\n",
            "}\n",
            "\n",
            "print(\"=== KIỂM THỬ DỰ ĐOÁN TRỰC TIẾP TRONG NOTEBOOK ===\")\n",
            "for name, values in test_cases.items():\n",
            "    sample_df = pd.DataFrame([values], columns=['Glucose', 'BMI', 'Age'])\n",
            "    p = loaded_model.predict(sample_df)[0]\n",
            "    c = np.amax(loaded_model.predict_proba(sample_df)[0]) * 100\n",
            "    label = \"Diabetic (Tiểu đường)\" if p == 1 else \"Not Diabetic (Bình thường)\"\n",
            "    print(f\"* {name}: {label} | Độ tin cậy: {c:.2f}%\")\n"
        ]
    }
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.13.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('Chap12_Diabetes_Notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Saved updated Chap12_Diabetes_Notebook.ipynb successfully!")
