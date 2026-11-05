# -*- coding: utf-8 -*-
"""
Mô-đun nạp và chuẩn bị dữ liệu hồ sơ bệnh nhân 100k
Dự án: Phần mềm GlucoGraph AI - Nhóm 15 (PTIT)
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import RobustScaler

def find_data_file(filename):
    """Tìm đường dẫn tệp dữ liệu linh hoạt dù chạy từ thư mục gốc hay thư mục con"""
    candidates = [
        os.path.join("data", filename),
        os.path.join("..", "data", filename),
        os.path.join(os.path.dirname(__file__), "..", "data", filename),
        os.path.join(os.path.dirname(__file__), "data", filename)
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)
    return None

@st.cache_data(show_spinner="Đang nạp cơ sở dữ liệu 100.000 hồ sơ bệnh nhân...")
def load_dataset():
    """Nạp tập dữ liệu hồ sơ bệnh nhân lâm sàng"""
    csv_path = find_data_file("diabetes_100k.csv")
    if not csv_path or not os.path.exists(csv_path):
        st.error("Không tìm thấy tệp dữ liệu diabetes_100k.csv.")
        return pd.DataFrame()
    
    df = pd.read_csv(csv_path)
    # Thêm mã định danh bệnh nhân hiển thị (Mã bệnh án)
    if 'patient_code' not in df.columns:
        df['patient_code'] = [f"BA-{i+1:06d}" for i in range(len(df))]
    return df

@st.cache_data
def get_sample_patients():
    """Các ca bệnh mẫu đại diện cho 3 nhóm trạng thái lâm sàng điển hình"""
    return {
        "Ca bệnh 1: Bệnh nhân Nguy cơ Cao (Chỉ số vượt ngưỡng rõ rệt)": {
            "gender": "Male",
            "age": 58.0,
            "hypertension": 1,
            "heart_disease": 1,
            "smoking_history": "former",
            "bmi": 32.4,
            "HbA1c_level": 8.5,
            "blood_glucose_level": 195,
            "diagnosis": "ĐÁI THÁO ĐƯỜNG (NGUY CƠ CAO)",
            "note": "HbA1c 8.5% và Glucose 195 mg/dL đều vượt ngưỡng ADA 2024. Tiền sử tăng huyết áp và bệnh tim mạch."
        },
        "Ca bệnh 2: Bệnh nhân Tiền đái tháo đường (Ngưỡng cận biên)": {
            "gender": "Female",
            "age": 49.0,
            "hypertension": 1,
            "heart_disease": 0,
            "smoking_history": "never",
            "bmi": 27.8,
            "HbA1c_level": 6.1,
            "blood_glucose_level": 118,
            "diagnosis": "TIỀN ĐÁI THÁO ĐƯỜNG",
            "note": "HbA1c nằm trong khoảng 5.7 - 6.4%, Glucose đói 100 - 125 mg/dL. Cần can thiệp lối sống sớm."
        },
        "Ca bệnh 3: Bệnh nhân Bình thường (Chỉ số khỏe mạnh)": {
            "gender": "Female",
            "age": 26.0,
            "hypertension": 0,
            "heart_disease": 0,
            "smoking_history": "never",
            "bmi": 21.3,
            "HbA1c_level": 5.1,
            "blood_glucose_level": 88,
            "diagnosis": "BÌNH THƯỜNG (NGUY CƠ THẤP)",
            "note": "Các chỉ số xét nghiệm huyết học và thể trạng đều nằm hoàn toàn trong ngưỡng an toàn sinh lý."
        }
    }

@st.cache_data
def get_preprocessed_features(df, n_samples=3000):
    """Chuẩn hóa các biến số liên tục bằng RobustScaler chống ngoại lệ lâm sàng"""
    if len(df) > n_samples:
        ref_subset = df.sample(n=n_samples, random_state=42).copy()
    else:
        ref_subset = df.copy()
        
    df_clean = ref_subset.copy()
    
    # Mã hóa nhị phân giới tính
    gender_map = {'Male': 1, 'Female': 0, 'Other': 0}
    df_clean['gender_code'] = df_clean['gender'].map(gender_map).fillna(0)
    
    # Chuẩn hóa các biến liên tục bằng RobustScaler
    scaler = RobustScaler()
    cont_cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    df_clean[cont_cols] = scaler.fit_transform(df_clean[cont_cols])
    
    all_feature_cols = ['gender_code', 'hypertension', 'heart_disease', 'age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    X = df_clean[all_feature_cols].values
    
    return X, scaler, ref_subset
