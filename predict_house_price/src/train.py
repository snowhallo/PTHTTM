import os
import sys
import json
import time
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
import joblib

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def load_and_preprocess_kaggle_data(filepath: str = "data/vietnam_housing_dataset.csv"):
    print(f"[1/4] Đang nạp dữ liệu Kaggle từ: {filepath}...")
    df = pd.read_csv(filepath)
    print(f"  -> Tổng số dòng: {df.shape[0]}, Tổng số cột: {df.shape[1]}")
    
    # 1. Trích xuất City và District từ trường Address
    def extract_location(addr):
        if not isinstance(addr, str):
            return "Khác", "Khác"
        parts = [p.strip() for p in addr.split(',') if p.strip()]
        if len(parts) >= 2:
            city = parts[-1]
            district = parts[-2]
        elif len(parts) == 1:
            city = parts[0]
            district = "Khác"
        else:
            city, district = "Khác", "Khác"
            
        # Chuẩn hóa tên thành phố phổ biến
        if any(c in city for c in ['Hồ Chí Minh', 'TP.HCM', 'TP HCM', 'Sài Gòn']):
            city = 'TP. Hồ Chí Minh'
        elif 'Hà Nội' in city:
            city = 'Hà Nội'
        elif 'Đà Nẵng' in city:
            city = 'Đà Nẵng'
        elif 'Hưng Yên' in city:
            city = 'Hưng Yên'
        elif 'Bình Dương' in city:
            city = 'Bình Dương'
        elif 'Hải Phòng' in city:
            city = 'Hải Phòng'
            
        return city, district

    locs = df['Address'].apply(extract_location)
    df['City'] = [l[0] for l in locs]
    df['District'] = [l[1] for l in locs]
    
    # Lấy top các thành phố lớn và toàn bộ các quận huyện thực tế (>= 15 mẫu)
    top_cities = df['City'].value_counts().nlargest(8).index.tolist()
    df['City'] = df['City'].apply(lambda x: x if x in top_cities else 'Tỉnh thành khác')
    
    district_counts = df['District'].value_counts()
    top_districts = district_counts[district_counts >= 15].index.tolist()
    df['District'] = df['District'].apply(lambda x: x if x in top_districts else 'Quận huyện khác')
    
    # Chuẩn hóa tên cột
    df['area'] = df['Area']
    df['frontage'] = df['Frontage']
    df['access_road'] = df['Access Road']
    df['floors'] = df['Floors']
    df['bedroom'] = df['Bedrooms']
    df['bathroom'] = df['Bathrooms']
    df['legal_status'] = df['Legal status'].fillna('Chưa xác định')
    df['house_direction'] = df['House direction'].fillna('Chưa xác định')
    df['city'] = df['City']
    df['district'] = df['District']
    df['price_billion'] = df['Price']
    
    # Lọc bỏ giá trị ngoại lai cực đoan nếu có
    df = df[(df['area'] >= 15.0) & (df['area'] <= 800.0)]
    df = df[(df['price_billion'] >= 0.5) & (df['price_billion'] <= 150.0)]
    
    # Lưu một bản clean copy phục vụ app và notebook
    os.makedirs('data', exist_ok=True)
    clean_cols = ['area', 'frontage', 'access_road', 'floors', 'bedroom', 'bathroom', 'legal_status', 'house_direction', 'city', 'district', 'price_billion']
    clean_df = df[clean_cols]
    clean_df.to_csv('data/gianha.csv', index=False, encoding='utf-8')
    print(f"  -> Đã làm sạch và lưu tập dữ liệu chuẩn: {clean_df.shape[0]} mẫu tại data/gianha.csv")
    
    return clean_df

def build_and_train_models():
    df = load_and_preprocess_kaggle_data()
    
    num_cols = ['area', 'frontage', 'access_road', 'floors', 'bedroom', 'bathroom']
    cat_cols = ['city', 'district', 'legal_status', 'house_direction']
    
    X = df[num_cols + cat_cols]
    y = df['price_billion']
    
    print("\n[2/4] Phân chia 80% Train, 20% Test (random_state=731)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=731)
    
    # Pipeline Tiền xử lý với SimpleImputer + StandardScaler + OneHotEncoder
    num_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='Chưa xác định')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer([
        ('num', num_pipe, num_cols),
        ('cat', cat_pipe, cat_cols)
    ])
    
    print("\n[3/4] Huấn luyện Baseline + 5 Mô hình ML bằng hàm fit()...")
    
    # Baseline
    base_pipe = Pipeline([('prep', preprocessor), ('reg', DummyRegressor(strategy='mean'))])
    base_pipe.fit(X_train, y_train)
    p_base = base_pipe.predict(X_test)
    
    # 5 Models
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0, random_state=731),
        'Decision Tree': DecisionTreeRegressor(max_depth=12, random_state=731),
        'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=15, random_state=731, n_jobs=-1),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=150, learning_rate=0.08, max_depth=5, random_state=731)
    }
    
    metrics = {
        'Baseline (Mean Dummy)': {
            'MAE': float(mean_absolute_error(y_test, p_base)),
            'MSE': float(mean_squared_error(y_test, p_base)),
            'RMSE': float(np.sqrt(mean_squared_error(y_test, p_base))),
            'R2': float(r2_score(y_test, p_base)),
            'MAPE': float(mean_absolute_percentage_error(y_test, p_base) * 100.0)
        }
    }
    
    fitted_pipes = {}
    for name, model in models.items():
        t0 = time.time()
        pipe = Pipeline([('prep', preprocessor), ('reg', model)])
        pipe.fit(X_train, y_train)
        t_el = time.time() - t0
        
        preds = pipe.predict(X_test)
        fitted_pipes[name] = pipe
        metrics[name] = {
            'MAE': float(mean_absolute_error(y_test, preds)),
            'MSE': float(mean_squared_error(y_test, preds)),
            'RMSE': float(np.sqrt(mean_squared_error(y_test, preds))),
            'R2': float(r2_score(y_test, preds)),
            'MAPE': float(mean_absolute_percentage_error(y_test, preds) * 100.0),
            'train_time_ms': round(t_el * 1000.0, 1)
        }
        print(f"  [OK] {name:<22} -> R2: {metrics[name]['R2']:.4f} | MAPE: {metrics[name]['MAPE']:.2f}% | Time: {t_el*1000:.1f}ms")
        
    print("\n[4/4] Lưu trữ mô hình tối ưu Gradient Boosting và metrics...")
    os.makedirs('models', exist_ok=True)
    best_pipe = fitted_pipes['Gradient Boosting']
    joblib.dump(best_pipe, 'models/best_model.joblib')
    
    with open('models/metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
        
    print("  [OK] Đã lưu models/best_model.joblib và models/metrics.json thành công!")
    return metrics

if __name__ == '__main__':
    build_and_train_models()
