import json
import requests

def predict_diabetes(Glucose, BMI, Age):
    url = "http://127.0.0.1:5000/diabetes/v1/predict"
    data = {
        "Glucose": float(Glucose),
        "BMI": float(BMI), 
        "Age": float(Age)
    }
    headers = {"Content-type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()

if __name__ == '__main__':
    print("=== CHƯƠNG TRÌNH KIỂM THỬ DỰ ĐOÁN TIỂU ĐƯỜNG CLIENT ===")
    Glucose = input('Nhập Glucose (mg/dL) [mặc định 100]: ') or '100'
    BMI = input('Nhập BMI [mặc định 30]: ') or '30'
    Age = input('Nhập Age (tuổi) [mặc định 29]: ') or '29'

    try:
        result = predict_diabetes(Glucose, BMI, Age)
        print("\n--- KẾT QUẢ TỪ REST API ---")
        print("Chẩn đoán:", result.get('label'))
        print("Phân lớp (Class 0/1):", result.get('prediction'))
        print("Độ tin cậy:", str(result.get('confidence')) + '%')
        print("Mức độ nguy cơ:", result.get('risk_level'))
    except Exception as e:
        print("Lỗi kết nối tới Server API:", e)
