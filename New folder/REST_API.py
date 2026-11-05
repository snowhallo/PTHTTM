import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

filename = "diabetes.sav"
loaded_model = pickle.load(open(filename, "rb"))

@app.route('/diabetes/v1/predict', methods=['POST'])
def predict():
    features = request.json
    try:
        glucose = float(features.get("Glucose", 0))
        bmi = float(features.get("BMI", 0))
        age = float(features.get("Age", 0))

        input_df = pd.DataFrame([[glucose, bmi, age]], columns=['Glucose', 'BMI', 'Age'])
        prediction = loaded_model.predict(input_df)
        confidence = loaded_model.predict_proba(input_df)

        response = {
            "prediction": int(prediction[0]),
            "label": "Diabetic" if int(prediction[0]) == 1 else "Not Diabetic",
            "confidence": str(round(np.amax(confidence[0]) * 100, 2)),
            "risk_level": "Cao" if int(prediction[0]) == 1 else "Thấp"
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("Starting Diabetes Prediction REST API on http://127.0.0.1:5000/ ...")
    app.run(host='0.0.0.0', port=5000, debug=False)
