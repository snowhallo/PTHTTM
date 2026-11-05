# -*- coding: utf-8 -*-
"""
Phân hệ 4: Quản Lý Hồ Sơ Bệnh Án Điện Tử (EMR & Patient Directory)
Dành cho: Nhân viên lưu trữ hồ sơ y tế, Bác sĩ tra cứu tiền sử bệnh án
Thiết kế tối giản, sạch sẽ, chuẩn phần mềm EMR bệnh viện, 100% không emoji
"""

import streamlit as st
import pandas as pd
from config import THEME_COLORS

def render_records_view(df):
    # 1. Thanh tiêu đề phân hệ
    st.markdown(f"""
    <div style="background-color: {THEME_COLORS['bg_card']}; border: 1.5px solid {THEME_COLORS['border']}; 
                border-left: 5px solid {THEME_COLORS['primary']}; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px;
                box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: {THEME_COLORS['primary']}; font-weight: 700; font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px;">
                    PHÂN HỆ LƯU TRỮ & QUẢN TRỊ BỆNH ÁN
                </span>
                <h3 style="color: {THEME_COLORS['text_primary']}; margin: 2px 0 0 0; font-size: 18px; font-weight: 700;">
                    Danh Sách Hồ Sơ Bệnh Án Điện Tử (EMR Patient Directory)
                </h3>
            </div>
            <div style="text-align: right; font-size: 12px; color: {THEME_COLORS['text_muted']};">
                Kho dữ liệu tích hợp: <b>100.000 hồ sơ</b> • Chuẩn HL7/EMR
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Bộ lọc tìm kiếm hồ sơ y tế
    with st.container(border=True):
        st.markdown(f"""
        <div style="margin-bottom: 6px;">
            <span style="font-weight: 700; color: {THEME_COLORS['text_primary']}; font-size: 13px; text-transform: uppercase;">
                BỘ LỌC TÌM KIẾM HỒ SƠ Y TẾ:
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            status_filter = st.selectbox(
                "Tình trạng chẩn đoán:",
                ["Tất cả", "Chỉ ca đái tháo đường (1)", "Chỉ người bình thường (0)"]
            )
        with col_f2:
            gender_filter = st.selectbox(
                "Giới tính sinh học:",
                ["Tất cả", "Female", "Male"]
            )
        with col_f3:
            age_range = st.slider("Độ tuổi bệnh nhân:", 0, 100, (20, 80))
        with col_f4:
            search_code = st.text_input("Tìm theo mã bệnh án:", placeholder="Ví dụ: BA-000001")
            
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # Lọc dữ liệu theo điều kiện
    filtered_df = df.copy()
    
    if status_filter == "Chỉ ca đái tháo đường (1)":
        filtered_df = filtered_df[filtered_df['diabetes'] == 1]
    elif status_filter == "Chỉ người bình thường (0)":
        filtered_df = filtered_df[filtered_df['diabetes'] == 0]
        
    if gender_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df['gender'] == gender_filter]
        
    filtered_df = filtered_df[
        (filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])
    ]
    
    if search_code.strip():
        filtered_df = filtered_df[filtered_df['patient_code'].str.contains(search_code.strip(), case=False, na=False)]
        
    # 3. Hiển thị bảng bệnh án
    display_limit = 50
    table_view = filtered_df.head(display_limit).copy()
    
    table_view.rename(columns={
        'patient_code': 'Mã bệnh án',
        'gender': 'Giới tính',
        'age': 'Tuổi',
        'bmi': 'Chỉ số BMI',
        'HbA1c_level': 'HbA1c (%)',
        'blood_glucose_level': 'Đường huyết (mg/dL)',
        'hypertension': 'Tăng huyết áp',
        'heart_disease': 'Bệnh tim mạch',
        'diabetes': 'Trạng thái'
    }, inplace=True)
    
    table_view['Trạng thái'] = table_view['Trạng thái'].apply(lambda x: "Đái tháo đường" if x == 1 else "Bình thường")
    table_view['Tăng huyết áp'] = table_view['Tăng huyết áp'].apply(lambda x: "Có" if x == 1 else "Không")
    table_view['Bệnh tim mạch'] = table_view['Bệnh tim mạch'].apply(lambda x: "Có" if x == 1 else "Không")
    
    st.markdown(f"<span style='font-size: 13px; color: {THEME_COLORS['text_secondary']};'>Hiển thị <b>{len(table_view)}</b> hồ sơ phù hợp (trong tổng số {len(filtered_df):,} hồ sơ theo tiêu chí lọc):</span>", unsafe_allow_html=True)
    st.dataframe(table_view, use_container_width=True, hide_index=True)
    
    # 4. Thao tác tiếp nhận vào buồng khám
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"""
        <div style="margin-bottom: 6px;">
            <span style="font-weight: 700; color: {THEME_COLORS['text_primary']}; font-size: 13px; text-transform: uppercase;">
                TIẾP NHẬN HỒ SƠ VÀO BUỒNG KHÁM CHUYÊN SÂU:
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        sel_col1, sel_col2 = st.columns([3, 1])
        with sel_col1:
            patient_options = table_view['Mã bệnh án'].tolist()
            if patient_options:
                selected_code = st.selectbox("Chọn mã hồ sơ bệnh nhân từ danh sách trên:", patient_options, label_visibility="collapsed")
            else:
                selected_code = None
                
        with sel_col2:
            if selected_code and st.button("Tiếp Nhận Vào Buồng Khám", use_container_width=True):
                raw_row = df[df['patient_code'] == selected_code].iloc[0]
                st.session_state['selected_patient'] = {
                    "patient_code": selected_code,
                    "gender": raw_row['gender'],
                    "age": float(raw_row['age']),
                    "bmi": float(raw_row['bmi']),
                    "HbA1c_level": float(raw_row['HbA1c_level']),
                    "blood_glucose_level": int(raw_row['blood_glucose_level']),
                    "hypertension": int(raw_row['hypertension']),
                    "heart_disease": int(raw_row['heart_disease']),
                    "smoking_history": raw_row['smoking_history']
                }
                # Chuyển ngay sang Phân hệ 2 (Buồng Khám)
                st.session_state['nav_view_index'] = 1
                st.rerun()
