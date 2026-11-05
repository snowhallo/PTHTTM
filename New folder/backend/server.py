import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import os
import sys
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add root folder to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from knowledge_graph.graph_engine import graph_engine
from knowledge_graph.neo4j_manager import neo4j_manager
from chatbot.graph_rag import medical_bot

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'frontend'))
CORS(app)

# Load trained ML Models (3 features & 8 features)
MODEL_3_PATH = os.path.join(BASE_DIR, 'diabetes.sav')
MODEL_8_PATH = os.path.join(BASE_DIR, 'diabetes_full.sav')
loaded_model_3 = None
loaded_model_8 = None

def get_clean_dataframe():
    """Loads and cleans diabetes dataset replacing 0s in biological metrics."""
    try:
        df = pd.read_csv(os.path.join(BASE_DIR, 'diabet.csv'))
    except Exception:
        df = pd.read_csv(os.path.join(BASE_DIR, 'diabetes.csv'))
    cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    df[cols] = df[cols].replace(0, np.nan)
    df.fillna(df.mean(), inplace=True)
    return df

def get_ml_model(mode="quick"):
    global loaded_model_3, loaded_model_8
    if mode == "full":
        if loaded_model_8 is None:
            if os.path.exists(MODEL_8_PATH):
                with open(MODEL_8_PATH, 'rb') as f:
                    loaded_model_8 = pickle.load(f)
            else:
                print("Training 8-feature full model (diabetes_full.sav)...")
                df = get_clean_dataframe()
                from sklearn.linear_model import LogisticRegression
                feature_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
                X = df[feature_cols]
                y = df.iloc[:, 8]
                loaded_model_8 = LogisticRegression(max_iter=1000, random_state=42)
                loaded_model_8.fit(X, y)
                with open(MODEL_8_PATH, 'wb') as f:
                    pickle.dump(loaded_model_8, f)
        return loaded_model_8
    else:
        if loaded_model_3 is None:
            if os.path.exists(MODEL_3_PATH):
                with open(MODEL_3_PATH, 'rb') as f:
                    loaded_model_3 = pickle.load(f)
            else:
                print("Training 3-feature Chapter 12 model (diabetes.sav)...")
                df = get_clean_dataframe()
                from sklearn.neighbors import KNeighborsClassifier
                X = df[['Glucose', 'BMI', 'Age']]
                y = df.iloc[:, 8]
                loaded_model_3 = KNeighborsClassifier(n_neighbors=19)
                loaded_model_3.fit(X, y)
                with open(MODEL_3_PATH, 'wb') as f:
                    pickle.dump(loaded_model_3, f)
        return loaded_model_3

# ----------------- STATIC FRONTEND ROUTES -----------------
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# ----------------- ML PREDICTION API (QUICK 3 & FULL 8 FEATURES) -----------------
@app.route('/diabetes/v1/predict', methods=['POST'])
@app.route('/api/predict', methods=['POST'])
def predict_endpoint():
    """Predicts diabetes outcome based on Quick 3 features or Full 8 clinical parameters."""
    try:
        data = request.json or {}
        mode = data.get("mode", "quick")
        
        # Check if full mode requested or 8 parameters supplied
        is_full = (mode == "full") or ("BloodPressure" in data and "Insulin" in data and "Pregnancies" in data)
        
        glucose = float(data.get("Glucose", 100))
        bmi = float(data.get("BMI", 30))
        age = float(data.get("Age", 29))
        
        if is_full:
            model = get_ml_model(mode="full")
            pregnancies = float(data.get("Pregnancies", 1))
            bp = float(data.get("BloodPressure", 72))
            skin = float(data.get("SkinThickness", 23))
            insulin = float(data.get("Insulin", 80))
            dpf = float(data.get("DiabetesPedigreeFunction", 0.47))
            
            feature_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
            input_df = pd.DataFrame([[pregnancies, glucose, bp, skin, insulin, bmi, dpf, age]], columns=feature_cols)
            inputs_dict = {
                "Glucose": glucose, "BMI": bmi, "Age": age,
                "Pregnancies": pregnancies, "BloodPressure": bp,
                "SkinThickness": skin, "Insulin": insulin,
                "DiabetesPedigreeFunction": dpf
            }
        else:
            model = get_ml_model(mode="quick")
            input_df = pd.DataFrame([[glucose, bmi, age]], columns=['Glucose', 'BMI', 'Age'])
            inputs_dict = {"Glucose": glucose, "BMI": bmi, "Age": age}

        pred = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0]
        confidence = round(float(np.amax(proba)) * 100, 2)
        diabetic_prob = round(float(proba[1]) * 100, 2)
        
        risk_level = "Thấp"
        risk_color = "#10b981"
        if pred == 1:
            risk_level = "Rất cao" if diabetic_prob > 75 else "Cao"
            risk_color = "#ef4444"
        elif diabetic_prob >= 35:
            risk_level = "Trung bình (Tiền tiểu đường)"
            risk_color = "#f59e0b"

        recommendations = []
        if pred == 1 or diabetic_prob >= 35:
            recommendations.append("Đến cơ sở y tế để xét nghiệm máu tĩnh mạch và định lượng HbA1c.")
            recommendations.append("Hạn chế tinh bột nhanh, đường tinh luyện, nước ngọt có ga.")
            recommendations.append("Tăng cường rau xanh, chất xơ hòa tan (>= 25g/ngày).")
            recommendations.append("Duy trì tập thể dục nhịp điệu (đi bộ, bơi lội) >= 150 phút/tuần.")
            recommendations.append("Tham khảo các dòng sản phẩm hỗ trợ và máy đo đường huyết tại Nhà thuốc Long Châu.")
        else:
            recommendations.append("Chỉ số hiện tại ở mức an toàn. Tiếp tục duy trì lối sống lành mạnh.")
            recommendations.append("Khám sức khỏe và đo đường huyết định kỳ 6-12 tháng/lần.")
            recommendations.append("Duy trì chế độ ăn đa dạng dinh dưỡng, đủ chất xơ và kiểm soát cân nặng.")

        # Additional specific clinical alerts in Full 8 Mode
        if is_full:
            if inputs_dict.get("BloodPressure", 0) >= 90:
                recommendations.append(f"⚠️ Huyết áp tâm trương cao ({inputs_dict['BloodPressure']} mmHg) cần được theo dõi hội chứng chuyển hóa và phòng biến chứng mạch máu.")
            if inputs_dict.get("Insulin", 0) >= 160:
                recommendations.append(f"⚠️ Nồng độ Insulin huyết thanh cao ({inputs_dict['Insulin']} μU/ml) là dấu hiệu điển hình của tình trạng đề kháng insulin mô đích.")
            if inputs_dict.get("DiabetesPedigreeFunction", 0) >= 0.7:
                recommendations.append(f"⚠️ Yếu tố di truyền gia đình cao (DPF = {inputs_dict['DiabetesPedigreeFunction']}), cần chủ động phòng ngừa sớm.")

        response = {
            "prediction": int(pred),
            "label": "Diabetic" if int(pred) == 1 else "Not Diabetic",
            "confidence": str(confidence),
            "diabetic_probability": diabetic_prob,
            "non_diabetic_probability": round(100 - diabetic_prob, 2),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "inputs": inputs_dict,
            "mode": "full" if is_full else "quick",
            "model_used": "Full 8 Features Logistic Regression" if is_full else "Top 3 Features KNN (k=19)",
            "recommendations": recommendations
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ----------------- KNOWLEDGE GRAPH APIS -----------------
@app.route('/api/graph', methods=['GET'])
def get_graph_data():
    """Returns complete graph dataset formatted for Vis.js."""
    try:
        data = neo4j_manager.get_vis_graph()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/graph/search', methods=['GET'])
def search_graph():
    """Search graph nodes by query string."""
    q = request.args.get('q', '')
    results = graph_engine.search_entities(q)
    return jsonify({"query": q, "results": results})

@app.route('/api/graph/node/<node_id>', methods=['GET'])
def get_node_details(node_id):
    """Get node details and its direct neighbors."""
    details = graph_engine.get_node_details_and_neighbors(node_id)
    if not details:
        return jsonify({"error": "Node not found"}), 404
    return jsonify(details)

@app.route('/api/neo4j/status', methods=['GET'])
def get_neo4j_status():
    """Get Neo4j connection status and counts."""
    status = neo4j_manager.get_status()
    return jsonify(status)

@app.route('/api/neo4j/config', methods=['POST'])
def configure_neo4j():
    """Update Neo4j credentials and test connection / sync."""
    data = request.json or {}
    uri = data.get("uri", "bolt://localhost:7687")
    user = data.get("user", "neo4j")
    password = data.get("password", "")
    
    res = neo4j_manager.update_credentials(uri, user, password)
    return jsonify(res)

@app.route('/api/neo4j/sync', methods=['POST'])
def sync_neo4j():
    """Trigger synchronization to Neo4j instance."""
    res = neo4j_manager.sync_data()
    return jsonify(res)

# ----------------- CHATBOT GRAPHRAG API -----------------
@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """GraphRAG Chatbot assistant endpoint."""
    try:
        data = request.json or {}
        message = data.get("message", "").strip()
        ml_prediction = data.get("ml_context", None)
        
        if not message:
            return jsonify({"error": "Tin nhắn không được để trống"}), 400
            
        bot_response = medical_bot.generate_response(message, ml_prediction)
        return jsonify(bot_response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/config', methods=['GET', 'POST', 'OPTIONS'])
def configure_chat():
    """Configure Gemini or OpenAI API Key for Chatbot."""
    if request.method == 'GET':
        return jsonify({
            "has_gemini": bool(medical_bot.gemini_api_key),
            "has_openai": bool(medical_bot.openai_api_key),
            "engine_mode": "Generative LLM (Gemini/OpenAI)" if (medical_bot.gemini_api_key or medical_bot.openai_api_key) else "Local Knowledge Graph"
        })
        
    data = request.json or {}
    gemini_key = data.get("gemini_api_key", "")
    openai_key = data.get("openai_api_key", "")
    medical_bot.set_api_keys(gemini_key=gemini_key, openai_key=openai_key)
    return jsonify({
        "success": True,
        "message": "Đã cập nhật cấu hình Generative LLM thành công!",
        "has_gemini": bool(medical_bot.gemini_api_key),
        "has_openai": bool(medical_bot.openai_api_key),
        "engine_mode": "Generative LLM (Gemini/OpenAI)" if (medical_bot.gemini_api_key or medical_bot.openai_api_key) else "Local Knowledge Graph"
    })

# ----------------- BENCHMARK / CHAPTER 12 DATA API -----------------
@app.route('/api/benchmark', methods=['GET'])
def get_benchmark():
    """Returns the Chapter 12 benchmark table data."""
    table = [
        {
            "subset": "Top 3 Features (Chuẩn Chapter 12)",
            "features": ["Glucose", "BMI", "Age"],
            "logistic_regression": "76.70%",
            "knn": "77.21% (k=19)",
            "svm_linear": "76.57%",
            "svm_rbf": "76.57%",
            "is_best": True
        },
        {
            "subset": "Top 5 Features",
            "features": ["Glucose", "BMI", "Age", "Pregnancies", "SkinThickness"],
            "logistic_regression": "76.83%",
            "knn": "76.31% (k=15)",
            "svm_linear": "76.57%",
            "svm_rbf": "76.70%",
            "is_best": False
        },
        {
            "subset": "Top 7 Features",
            "features": ["Glucose", "BMI", "Age", "Pregnancies", "SkinThickness", "Insulin", "DiabetesPedigreeFunction"],
            "logistic_regression": "76.83%",
            "knn": "75.40% (k=15)",
            "svm_linear": "76.70%",
            "svm_rbf": "76.70%",
            "is_best": False
        },
        {
            "subset": "All 8 Features",
            "features": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
            "logistic_regression": "77.22%",
            "knn": "74.88% (k=17)",
            "svm_linear": "76.96%",
            "svm_rbf": "76.70%",
            "is_best": False
        }
    ]
    return jsonify({"benchmark": table})

if __name__ == '__main__':
    print("==================================================================")
    print("🚀 DIABETES AI & LONG CHAU KNOWLEDGE GRAPH WEB APP STARTING...")
    print("📍 URL: http://127.0.0.1:5000")
    print("==================================================================")
    app.run(host='0.0.0.0', port=5000, debug=False)
