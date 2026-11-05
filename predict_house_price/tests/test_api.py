import sys
import os
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Vietnam Real Estate AI" in response.text
    print("[PASS] GET / -> Trả về giao diện Dashboard thành công 200 OK")

def test_predict_endpoint():
    payload = {
        "city": "Hà Nội",
        "district": "Cầu Giấy",
        "area": 85.0,
        "frontage": 4.5,
        "access_road": 6.0,
        "floors": 4.0,
        "bedroom": 3.0,
        "bathroom": 3.0,
        "legal_status": "Have certificate",
        "house_direction": "Đông - Nam"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["predicted_price_billion"] > 0
    assert "confidence_interval" in data
    assert len(data["feature_contributions"]) > 0
    print(f"[PASS] POST /api/predict -> Định giá thành công: {data['predicted_price_billion']} Tỷ VNĐ")

def test_sample_data_endpoint():
    response = client.get("/api/sample-data")
    assert response.status_code == 200
    data = response.json()
    assert len(data["samples"]) >= 10
    print(f"[PASS] GET /api/sample-data -> Lấy được {len(data['samples'])} mẫu thực tế từ tập dữ liệu 30,229 bản ghi")

def test_neo4j_chat_endpoint():
    payload = {
        "message": "Tìm nhà tại Cầu Giấy dưới 8.5 tỷ có sổ đỏ"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "reply" in data and len(data["reply"]) > 0
    assert "cypher_query" in data and "MATCH" in data["cypher_query"]
    assert "graph_nodes_count" in data and data["graph_nodes_count"] > 0
    print(f"[PASS] POST /api/chat -> Chatbot Neo4j phản hồi thành công với câu truy vấn Cypher:\n       {data['cypher_query'].splitlines()[0]}")

def test_metrics_endpoint():
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "Gradient Boosting" in data
    print("[PASS] GET /api/metrics -> Lấy bảng 5 độ đo thành công 200 OK")

if __name__ == "__main__":
    print("=== BẮT ĐẦU KIỂM THỬ TOÀN BỘ CÁC REST API ENDPOINTS ===")
    test_root_endpoint()
    test_predict_endpoint()
    test_sample_data_endpoint()
    test_neo4j_chat_endpoint()
    test_metrics_endpoint()
    print("=" * 60)
    print("XÁC NHẬN: 100% CÁC API ENDPOINTS ĐỀU HOẠT ĐỘNG HOÀN HẢO!")
    print("=" * 60)
