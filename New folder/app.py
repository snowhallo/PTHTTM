import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.server import app

if __name__ == '__main__':
    print("==================================================================")
    print("🏥 HỆ THỐNG DỰ ĐOÁN TIỂU ĐƯỜNG & KNOWLEDGE GRAPH LONG CHÂU NEOAI")
    print("🌐 Truy cập ứng dụng Web tại: http://127.0.0.1:5000")
    print("📡 REST API Chapter 12 Endpoint: POST http://127.0.0.1:5000/diabetes/v1/predict")
    print("==================================================================")
    app.run(host='0.0.0.0', port=5000, debug=False)
