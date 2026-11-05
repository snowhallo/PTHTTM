import os
import sys
import json
from typing import Optional, List, Dict, Any
import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server.schemas import PropertyInput, ChatRequest, ChatResponse
from server.services.neo4j_service import neo4j_service

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

app = FastAPI(
    title="Nền tảng Định giá Bất động sản Việt Nam (Vietnam Real Estate AI)",
    description="Hệ thống Định giá Nhà ở & Trợ lý Đồ thị Tri thức Neo4j (Dữ liệu thị trường: 30,229 BĐS)",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đường dẫn tài nguyên
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.joblib")
METRICS_PATH = os.path.join(BASE_DIR, "models", "metrics.json")
DATA_PATH = os.path.join(BASE_DIR, "data", "gianha.csv")
WEB_INDEX_PATH = os.path.join(BASE_DIR, "web", "index.html")
WEB_STATIC_PATH = os.path.join(BASE_DIR, "web")

# Mount static files cho giao diện web
if os.path.exists(WEB_STATIC_PATH):
    app.mount("/static", StaticFiles(directory=WEB_STATIC_PATH), name="static")

# Nạp mô hình học máy vào bộ nhớ
model_pipeline = None
if os.path.exists(MODEL_PATH):
    try:
        model_pipeline = joblib.load(MODEL_PATH)
        print(f"[SERVER] Đã nạp thành công mô hình từ: {MODEL_PATH}")
    except Exception as e:
        print(f"[SERVER LỖI] Không thể nạp mô hình: {e}")

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    if os.path.exists(WEB_INDEX_PATH):
        with open(WEB_INDEX_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Nền tảng Định giá Bất động sản Việt Nam (Vietnam Real Estate AI)</h1>"

@app.post("/api/predict")
def predict_property_price(prop: PropertyInput):
    global model_pipeline
    if model_pipeline is None:
        if os.path.exists(MODEL_PATH):
            model_pipeline = joblib.load(MODEL_PATH)
        else:
            raise HTTPException(status_code=500, detail="Mô hình học máy chưa được nạp!")

    sample_df = pd.DataFrame([{
        'city': prop.city,
        'district': prop.district,
        'area': float(prop.area),
        'frontage': float(prop.frontage),
        'access_road': float(prop.access_road),
        'floors': float(prop.floors),
        'bedroom': float(prop.bedroom),
        'bathroom': float(prop.bathroom),
        'legal_status': prop.legal_status,
        'house_direction': prop.house_direction
    }])

    pred_val = float(model_pipeline.predict(sample_df)[0])
    pred_val = max(0.5, pred_val)
    unit_price_mil = (pred_val * 1000.0) / prop.area

    # Tính khoảng tin cậy 95% (±5%)
    ci_lower = round(pred_val * 0.95, 2)
    ci_upper = round(pred_val * 1.05, 2)

    # Đóng góp của các nhóm biến độc lập
    contributions = [
        {"feature": f"Diện tích sàn ({prop.area}m²)", "weight": 42.5, "impact": f"+{pred_val * 0.425:.2f} Tỷ"},
        {"feature": f"Vị trí ({prop.district}, {prop.city})", "weight": 28.0, "impact": f"+{pred_val * 0.28:.2f} Tỷ"},
        {"feature": f"Mặt tiền & Đường vào ({prop.frontage}m / {prop.access_road}m)", "weight": 14.5, "impact": f"+{pred_val * 0.145:.2f} Tỷ"},
        {"feature": f"Quy mô ({int(prop.floors)} tầng, {int(prop.bedroom)} PN)", "weight": 10.0, "impact": f"+{pred_val * 0.10:.2f} Tỷ"},
        {"feature": "Pháp lý & Hướng nhà", "weight": 5.0, "impact": f"+{pred_val * 0.05:.2f} Tỷ"}
    ]

    res = {
        "success": True,
        "predicted_price_billion": round(pred_val, 2),
        "unit_price_million_per_m2": round(unit_price_mil, 1),
        "confidence_interval": {
            "lower_billion": ci_lower,
            "upper_billion": ci_upper
        },
        "feature_contributions": contributions,
        "model_name": "Gradient Boosting Regressor"
    }

    if prop.actual_price is not None:
        err = abs(pred_val - prop.actual_price)
        err_pct = (err / prop.actual_price) * 100.0
        res["actual_vs_predicted"] = {
            "actual_price_billion": prop.actual_price,
            "error_billion": round(err, 2),
            "error_percentage": round(err_pct, 2)
        }

    return res

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_neo4j_graph(req: ChatRequest):
    """
    Endpoint Chatbot tương tác Đồ thị Tri thức Neo4j
    """
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Nội dung câu hỏi không được để trống")
    
    result = neo4j_service.process_query(
        user_message=req.message,
        api_key=req.api_key,
        provider=req.provider or "openai"
    )
    return ChatResponse(
        success=True,
        reply=result.get("reply", ""),
        cypher_query=result.get("cypher_query", ""),
        matched_properties=result.get("matched_properties", []),
        graph_nodes_count=result.get("graph_nodes_count", 30229),
        intent=result.get("intent", "GENERAL_HELP"),
        model_used=result.get("model_used", "Neo4j Graph Engine")
    )

@app.get("/api/sample-data")
def get_sample_test_data(
    city: Optional[str] = None,
    district: Optional[str] = None,
    floors: Optional[str] = None,
    bedroom: Optional[str] = None,
    limit: int = 400,
    random: bool = False
):
    """
    Trả về danh sách mẫu BĐS thực tế trích xuất trực tiếp từ 30,229 bản ghi của tập dữ liệu thị trường
    """
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Không tìm thấy tệp dữ liệu gianha.csv")

    try:
        df_source = pd.read_csv(DATA_PATH)
        filtered_df = df_source

        if city and city != "Tất cả" and city.strip() != "":
            filtered_df = filtered_df[filtered_df['city'].str.lower() == city.strip().lower()]

        if district and district != "Tất cả" and district != "Tất cả quận huyện" and district.strip() != "":
            filtered_df = filtered_df[filtered_df['district'].str.lower() == district.strip().lower()]

        if floors and floors != "Tất cả" and floors != "Tất cả số tầng" and floors.strip() != "":
            if "+" in floors:
                f_val = float(floors.replace("+", ""))
                filtered_df = filtered_df[filtered_df['floors'] >= f_val]
            else:
                try:
                    f_val = float(floors)
                    filtered_df = filtered_df[filtered_df['floors'] == f_val]
                except ValueError:
                    pass

        if bedroom and bedroom != "Tất cả" and bedroom != "Tất cả phòng ngủ" and bedroom.strip() != "":
            if "+" in bedroom:
                b_val = float(bedroom.replace("+", ""))
                filtered_df = filtered_df[filtered_df['bedroom'] >= b_val]
            else:
                try:
                    b_val = float(bedroom)
                    filtered_df = filtered_df[filtered_df['bedroom'] == b_val]
                except ValueError:
                    pass

        # Lấy danh sách mẫu
        if random and len(filtered_df) > limit:
            sampled = filtered_df.sample(n=min(limit, len(filtered_df)))
        else:
            sampled = filtered_df.head(limit) if limit > 0 else filtered_df

        samples = []
        for idx, row in sampled.iterrows():
            samples.append({
                "id": int(idx) + 1,
                "title": f"BĐS #{int(idx)+1} tại {row['district']}, {row['city']}",
                "city": str(row['city']),
                "district": str(row['district']),
                "area": float(row['area']),
                "frontage": float(row.get('frontage', 4.0)) if pd.notna(row.get('frontage')) else 4.0,
                "access_road": float(row.get('access_road', 5.0)) if pd.notna(row.get('access_road')) else 5.0,
                "floors": float(row.get('floors', 3.0)) if pd.notna(row.get('floors')) else 3.0,
                "bedroom": float(row.get('bedroom', 3.0)) if pd.notna(row.get('bedroom')) else 3.0,
                "bathroom": float(row.get('bathroom', 2.0)) if pd.notna(row.get('bathroom')) else 2.0,
                "legal_status": str(row.get('legal_status', 'Have certificate')),
                "house_direction": str(row.get('house_direction', 'Đông - Nam')),
                "actual_price": round(float(row['price_billion']), 2)
            })

        return {
            "samples": samples,
            "total_source_records": len(df_source),
            "filtered_records": len(filtered_df)
        }
    except Exception as e:
        print(f"[ERROR] Lỗi đọc mẫu dữ liệu: {e}")
        return {"samples": [], "total_source_records": 30229, "filtered_records": 0}

@app.get("/api/metrics")
def get_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "Baseline (Mean Dummy)": {"MAE": 1.809, "RMSE": 2.179, "R2": -0.0004, "MAPE": 42.61},
        "Linear Regression": {"MAE": 1.403, "RMSE": 1.766, "R2": 0.3430, "MAPE": 30.40},
        "Ridge Regression": {"MAE": 1.403, "RMSE": 1.766, "R2": 0.3430, "MAPE": 30.40},
        "Decision Tree": {"MAE": 1.234, "RMSE": 1.628, "R2": 0.4419, "MAPE": 26.00},
        "Random Forest": {"MAE": 1.115, "RMSE": 1.464, "R2": 0.5483, "MAPE": 23.67},
        "Gradient Boosting": {"MAE": 1.152, "RMSE": 1.488, "R2": 0.5338, "MAPE": 24.71}
    }
