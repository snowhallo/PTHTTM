import sys
import os
import json
import pickle
import numpy as np

# Force UTF-8 stdout if possible
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Set project root in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge_graph.graph_engine import graph_engine
from knowledge_graph.neo4j_manager import neo4j_manager
from chatbot.graph_rag import medical_bot
from backend.server import app

def test_ml_model():
    print("\n--- 1. Testing ML Models (diabetes.sav & diabetes_full.sav) ---")
    assert os.path.exists('diabetes.sav'), "diabetes.sav does not exist!"
    with open('diabetes.sav', 'rb') as f:
        model = pickle.load(f)
    
    # Test case 1: Normal patient (Top 3)
    pred1 = model.predict([[100, 28.5, 29]])[0]
    proba1 = model.predict_proba([[100, 28.5, 29]])[0]
    print(f"Sample Normal Top 3 (Glucose=100, BMI=28.5, Age=29): Pred = {pred1}, Prob = {np.amax(proba1)*100:.2f}%")
    assert pred1 == 0, f"Expected 0 for normal, got {pred1}"
    
    # Test case 2: High risk patient (Top 3)
    pred2 = model.predict([[165, 38.0, 52]])[0]
    proba2 = model.predict_proba([[165, 38.0, 52]])[0]
    print(f"Sample High Risk Top 3 (Glucose=165, BMI=38.0, Age=52): Pred = {pred2}, Prob = {np.amax(proba2)*100:.2f}%")
    assert pred2 == 1, f"Expected 1 for diabetic, got {pred2}"

    # Test case 3: Full 8 features model
    from backend.server import get_ml_model
    model_8 = get_ml_model(mode="full")
    sample_8 = [[3, 168, 94, 35, 220, 36.5, 0.88, 50]]
    pred_8 = model_8.predict(sample_8)[0]
    print(f"Sample Full 8 Features (Preg=3, Gluc=168, BP=94, Skin=35, Ins=220, BMI=36.5, DPF=0.88, Age=50): Pred = {pred_8}")
    assert pred_8 == 1, f"Expected 1 for diabetic 8 features, got {pred_8}"
    print("[OK] ML Models (3 & 8 features) test PASSED!")

def test_knowledge_graph():
    print("\n--- 2. Testing Knowledge Graph Engine ---")
    vis_data = graph_engine.get_all_graph_data()
    print(f"Loaded {vis_data['stats']['total_nodes']} nodes and {vis_data['stats']['total_edges']} edges.")
    assert vis_data['stats']['total_nodes'] >= 30, "Knowledge graph should have at least 30 nodes."
    assert vis_data['stats']['total_edges'] >= 40, "Knowledge graph should have at least 40 edges."
    
    # Test search
    search_res = graph_engine.search_entities("Metformin")
    print(f"Search 'Metformin': Found {len(search_res)} entities -> {[r['label'] for r in search_res]}")
    assert len(search_res) > 0, "Should find Metformin in knowledge graph"
    
    # Test node details
    details = graph_engine.get_node_details_and_neighbors("M01")
    assert details is not None, "M01 should exist"
    print(f"Node M01 ({details['node']['label']}): Outgoing relations = {len(details['outgoing'])}")
    print("[OK] Knowledge Graph Engine test PASSED!")

def test_chatbot_graph_rag():
    print("\n--- 3. Testing Medical GraphRAG Chatbot ---")
    # Query 1
    resp1 = medical_bot.generate_response("Tôi bị đường huyết 150, BMI 35 và mắt mờ, có nguy cơ tiểu đường không và mua thuốc gì ở Long Châu?")
    assert len(resp1["answer"]) > 100, "Chatbot answer should be rich and detailed"
    assert len(resp1["extracted_entities"]) > 0, "Should extract medical entities"
    print(f"Chatbot Q1 Extracted Entities: {resp1['extracted_entities']}")
    print("Chatbot Answer Preview (first 200 chars):", resp1["answer"][:200].replace('\n', ' '))
    
    # Query 2 with ML context
    ml_ctx = {"prediction": 1, "label": "Diabetic", "confidence": "78.95", "risk_level": "Cao"}
    resp2 = medical_bot.generate_response("Tôi nên uống thuốc gì và kiêng ăn gì?", ml_prediction=ml_ctx)
    assert len(resp2["answer"]) > 50 and "engine_mode" in resp2, "Should return valid response with engine mode"
    print(f"Chatbot Q2 Engine Mode: {resp2['engine_mode']}")
    print("[OK] Medical GraphRAG Chatbot test PASSED!")

def test_flask_server_endpoints():
    print("\n--- 4. Testing Flask API Endpoints ---")
    client = app.test_client()
    
    # Predict endpoint
    res_pred = client.post('/api/predict', json={"Glucose": 100, "BMI": 28, "Age": 29})
    assert res_pred.status_code == 200, f"Predict API returned {res_pred.status_code}"
    data_pred = json.loads(res_pred.data)
    assert data_pred["prediction"] == 0
    print(f"API /api/predict: {data_pred['label']} ({data_pred['confidence']}%)")

    # Chapter 12 exact REST API path test
    res_ch12 = client.post('/diabetes/v1/predict', json={"Glucose": 160, "BMI": 38, "Age": 50})
    assert res_ch12.status_code == 200, f"Chapter 12 API returned {res_ch12.status_code}"
    data_ch12 = json.loads(res_ch12.data)
    assert data_ch12["prediction"] == 1
    print(f"API /diabetes/v1/predict: {data_ch12['label']} ({data_ch12['confidence']}%)")

    # Graph API
    res_graph = client.get('/api/graph')
    assert res_graph.status_code == 200
    data_graph = json.loads(res_graph.data)
    assert len(data_graph["nodes"]) > 0
    print(f"API /api/graph: Returned {len(data_graph['nodes'])} nodes for Vis.js")

    # Chat API
    res_chat = client.post('/api/chat', json={"message": "Thuốc Glucophage giá bao nhiêu?"})
    assert res_chat.status_code == 200
    data_chat = json.loads(res_chat.data)
    assert "answer" in data_chat
    print(f"API /api/chat: Successfully generated answer")

    # Benchmark API
    res_bench = client.get('/api/benchmark')
    assert res_bench.status_code == 200
    data_bench = json.loads(res_bench.data)
    assert len(data_bench["benchmark"]) == 4
    print(f"API /api/benchmark: Returned 4 benchmark rows")

    print("[OK] All Flask API Endpoints test PASSED!")

if __name__ == '__main__':
    print("==========================================================")
    print("RUNNING FULL SYSTEM VERIFICATION SUITE")
    print("==========================================================")
    test_ml_model()
    test_knowledge_graph()
    test_chatbot_graph_rag()
    test_flask_server_endpoints()
    print("\n==========================================================")
    print("ALL TESTS PASSED SUCCESSFULLY (100% OPERATIONAL)!")
    print("==========================================================")
