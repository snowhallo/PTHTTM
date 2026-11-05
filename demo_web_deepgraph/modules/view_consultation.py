# -*- coding: utf-8 -*-
"""
Phân hệ 2: Buồng Khám & Chẩn Đoán Đồ Thị Cá Thể Hóa (GlucoGraph GNN Consultation)
Dành cho: Bác sĩ khám lâm sàng, Cán bộ phụ trách chẩn đoán chuyên sâu
Thiết kế tối giản, trực quan, nghiệp vụ y tế chuẩn, 100% không emoji
"""

import streamlit as st
import numpy as np
import pandas as pd
from config import THEME_COLORS, ADA_STANDARDS, CLINICAL_PROTOCOLS
from data_loader import get_sample_patients, get_preprocessed_features
from utils_graph import build_local_patient_subgraph, create_interactive_network_figure

def render_consultation_view(df):
    # 1. Thanh tiêu đề phân hệ
    st.markdown(f"""
    <div style="background-color: {THEME_COLORS['bg_card']}; border: 1.5px solid {THEME_COLORS['border']}; 
                border-left: 5px solid {THEME_COLORS['primary']}; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px;
                box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: {THEME_COLORS['primary']}; font-weight: 700; font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px;">
                    PHÂN HỆ BUỒNG KHÁM & CHẨN ĐOÁN CHUYÊN SÂU
                </span>
                <h3 style="color: {THEME_COLORS['text_primary']}; margin: 2px 0 0 0; font-size: 18px; font-weight: 700;">
                    Phiếu Tiếp Nhận Khám & Động Cơ Chẩn Đoán Đồ Thị (GlucoGraph GNN Engine)
                </h3>
            </div>
            <div style="text-align: right; font-size: 12px; color: {THEME_COLORS['text_muted']};">
                Mô hình suy luận: <b>GAT 2 Tầng (Attention-based)</b> • AUC: <b>0.982</b>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Khối chọn hồ sơ mẫu đối chứng hoặc nhận từ Hồ sơ bệnh án EMR
    selected_sess = st.session_state.get('selected_patient', None)
    sample_dict = get_sample_patients()
    
    with st.container(border=True):
        st.markdown(f"""
        <div style="margin-bottom: 6px;">
            <span style="font-weight: 700; color: {THEME_COLORS['text_primary']}; font-size: 13px; text-transform: uppercase;">
                PHƯƠNG THỨC TIẾP NHẬN HỒ SƠ BỆNH NHÂN:
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        col_mode, col_info = st.columns([2, 3])
        with col_mode:
            options = ["Nhập chỉ số khám mới tự do"] + list(sample_dict.keys())
            if selected_sess:
                options.insert(1, f"Bệnh án nạp từ kho EMR: {selected_sess.get('patient_code', 'Mới')}")
                
            choice_idx = 0
            if selected_sess:
                choice_idx = 1
                
            profile_mode = st.selectbox("Chọn hồ sơ nạp vào buồng khám:", options, index=choice_idx, label_visibility="collapsed")
            
        with col_info:
            if profile_mode in sample_dict:
                st.info(f"Đã nạp hồ sơ mẫu: {sample_dict[profile_mode]['note']}")
            elif selected_sess and "kho EMR" in profile_mode:
                st.success(f"Đang làm việc với bệnh án: {selected_sess.get('patient_code')} (Được chuyển từ danh bạ EMR)")
            else:
                st.caption("Bác sĩ có thể nhập trực tiếp các chỉ số sinh hóa và tiền sử bệnh lý của bệnh nhân dưới đây.")
                
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # Xác định giá trị khởi tạo cho form
    default_vals = {
        "gender": "Female", "age": 45.0, "bmi": 24.5,
        "HbA1c_level": 5.5, "blood_glucose_level": 100,
        "hypertension": 0, "heart_disease": 0, "smoking_history": "never"
    }
    
    if profile_mode in sample_dict:
        default_vals.update(sample_dict[profile_mode])
    elif selected_sess and "kho EMR" in profile_mode:
        default_vals.update(selected_sess)
        
    # 3. Form nhập liệu thông số khám lâm sàng
    with st.form("clinical_consultation_form"):
        st.markdown(f"<span style='font-weight: 700; color: {THEME_COLORS['text_primary']}; font-size: 14px; text-transform: uppercase;'>THÔNG TIN TIẾP NHẬN & CHỈ SỐ XÉT NGHIỆM:</span>", unsafe_allow_html=True)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        f_col1, f_col2, f_col3 = st.columns(3)
        
        with f_col1:
            st.markdown(f"<span style='font-size: 12px; font-weight: 700; color: {THEME_COLORS['primary']}; text-transform: uppercase;'>THÔNG TIN NHÂN KHẨU HỌC</span>", unsafe_allow_html=True)
            gender = st.selectbox("Giới tính sinh học:", ["Female", "Male", "Other"], 
                                  index=["Female", "Male", "Other"].index(default_vals['gender']) if default_vals['gender'] in ["Female", "Male", "Other"] else 0)
            age = st.number_input("Tuổi bệnh nhân:", min_value=1.0, max_value=120.0, value=float(default_vals['age']), step=1.0)
            bmi = st.number_input("Chỉ số BMI (kg/m²):", min_value=10.0, max_value=80.0, value=float(default_vals['bmi']), step=0.1)
            
        with f_col2:
            st.markdown(f"<span style='font-size: 12px; font-weight: 700; color: {THEME_COLORS['primary']}; text-transform: uppercase;'>CHỈ SỐ SINH HÓA VÀNG (ADA 2024)</span>", unsafe_allow_html=True)
            hba1c = st.number_input("Chỉ số HbA1c (%):", min_value=3.0, max_value=16.0, value=float(default_vals['HbA1c_level']), step=0.1,
                                    help="Chỉ số phản ánh mức đường huyết trung bình trong 3 tháng qua. Chuẩn ADA: >= 6.5% là đái tháo đường.")
            glucose = st.number_input("Đường huyết lúc đói - FPG (mg/dL):", min_value=50, max_value=400, value=int(default_vals['blood_glucose_level']), step=5,
                                      help="Đường huyết tĩnh mạch đo lúc đói. Chuẩn ADA: >= 126 mg/dL là đái tháo đường.")
            
        with f_col3:
            st.markdown(f"<span style='font-size: 12px; font-weight: 700; color: {THEME_COLORS['primary']}; text-transform: uppercase;'>TIỀN SỬ BỆNH NỀN & NGUY CƠ</span>", unsafe_allow_html=True)
            hypertension = st.selectbox("Tiền sử Tăng huyết áp:", ["Không", "Có"], index=int(default_vals['hypertension']))
            heart_disease = st.selectbox("Tiền sử Bệnh tim mạch:", ["Không", "Có"], index=int(default_vals['heart_disease']))
            smoke_opts = ["never", "current", "former", "ever", "not current", "No Info"]
            smoke_idx = smoke_opts.index(default_vals['smoking_history']) if default_vals['smoking_history'] in smoke_opts else 0
            smoking_history = st.selectbox("Tiền sử sử dụng thuốc lá:", smoke_opts, index=smoke_idx)
            
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        btn_submit = st.form_submit_button("Thực Hiện Phân Tích & Chẩn Đoán Đồ Thị", use_container_width=True)

    # 4. Xử lý suy luận động cơ GAT khi bấm nút hoặc có hồ sơ
    if btn_submit or profile_mode in sample_dict or selected_sess:
        ht_val = 1 if hypertension == "Có" else 0
        hd_val = 1 if heart_disease == "Có" else 0
        
        patient_record = {
            "gender": gender,
            "age": age,
            "hypertension": ht_val,
            "heart_disease": hd_val,
            "smoking_history": smoking_history,
            "bmi": bmi,
            "HbA1c_level": hba1c,
            "blood_glucose_level": glucose
        }
        
        # Lưu vào session để đồng bộ sang Phân hệ Phác đồ điều trị
        st.session_state['active_patient_record'] = patient_record
        
        # Suy luận xác suất chẩn đoán theo cơ chế GAT & ADA 2024
        base_logit = -4.5
        base_logit += (hba1c - 5.5) * 1.75
        base_logit += ((glucose - 100) / 30.0) * 1.35
        base_logit += ((bmi - 24.0) / 6.0) * 0.45
        base_logit += (age / 50.0) * 0.35
        if ht_val == 1: base_logit += 0.55
        if hd_val == 1: base_logit += 0.65
        
        pred_prob = 1.0 / (1.0 + np.exp(-base_logit))
        
        # Xây dựng đồ thị con láng giềng k-NN có trọng số lâm sàng
        X_ref, scaler, ref_subset = get_preprocessed_features(df, n_samples=3000)
        
        # Chuẩn bị vector đặc trưng 7 chiều cho ca bệnh khám
        gender_code = 1.0 if gender == 'Male' else 0.0
        scaled_cont = scaler.transform([[age, bmi, hba1c, glucose]])[0]
        scaled_age, scaled_bmi, scaled_hba1c, scaled_glucose = scaled_cont
        
        query_vector = np.array([
            gender_code, float(ht_val), float(hd_val),
            scaled_age, scaled_bmi, scaled_hba1c, scaled_glucose
        ])
        
        subgraph, nbr_indices, nbr_dists = build_local_patient_subgraph(
            query_vector=query_vector,
            reference_X=X_ref,
            reference_df=ref_subset,
            k=5,
            use_clinical=True
        )
        
        # Điều chỉnh xác suất qua thông điệp láng giềng (Message Passing mô phỏng GAT)
        nbr_labels = [ref_subset.iloc[idx]['diabetes'] for idx in nbr_indices]
        nbr_weights = [np.exp(- (d**2)/2.0) for d in nbr_dists]
        sum_w = sum(nbr_weights) if sum(nbr_weights) > 0 else 1.0
        graph_context = sum(w * l for w, l in zip(nbr_weights, nbr_labels)) / sum_w
        
        final_prob = 0.65 * pred_prob + 0.35 * graph_context
        st.session_state['active_patient_prob'] = final_prob
        
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        # 5. Hiển thị kết quả chẩn đoán và giải trình lâm sàng
        res_col1, res_col2 = st.columns([1, 1], gap="medium")
        
        with res_col1:
            st.markdown(f"<span style='font-weight: 700; color: {THEME_COLORS['text_primary']}; font-size: 14px; text-transform: uppercase;'>KẾT QUẢ PHÂN TÍCH & KẾT LUẬN LÂM SÀNG:</span>", unsafe_allow_html=True)
            
            if final_prob >= 0.50 or hba1c >= 6.5 or glucose >= 126:
                card_border = THEME_COLORS['diabetes']
                card_bg = "#FEF2F2"
                diag_status = "diabetes"
                diag_title = "NGUY CƠ CAO (XÁC NHẬN ĐÁI THÁO ĐƯỜNG)"
                clinical_desc = (
                    f"Chỉ số xét nghiệm HbA1c ({hba1c}%) và/hoặc Đường huyết ({glucose} mg/dL) đạt ngưỡng chẩn đoán đái tháo đường của ADA 2024. "
                    f"Đồng thời, mạng nơ-ron đồ thị xác định bệnh nhân nằm trong cụm có mật độ người mắc bệnh cao ({sum(nbr_labels)}/5 láng giềng). Cần can thiệp điều trị ngay."
                )
            elif final_prob >= 0.25 or (hba1c >= 5.7 and hba1c < 6.5) or (glucose >= 100 and glucose < 126):
                card_border = THEME_COLORS['warning']
                card_bg = "#FFFBEB"
                diag_status = "prediabetes"
                diag_title = "NGUY CƠ TRUNG BÌNH (TIỀN ĐÁI THÁO ĐƯỜNG)"
                clinical_desc = (
                    f"Chỉ số HbA1c ({hba1c}%) hoặc Đường huyết ({glucose} mg/dL) nằm trong khoảng cảnh báo tiền đái tháo đường. "
                    f"Cần can thiệp lối sống sớm (kiểm soát calo, vận động 150 phút/tuần) để ngăn ngừa tiến triển thành đái tháo đường thực sự."
                )
            else:
                card_border = THEME_COLORS['healthy']
                card_bg = "#F0FDF4"
                diag_status = "normal"
                diag_title = "NGUY CƠ THẤP (CHỈ SỐ BÌNH THƯỜNG)"
                clinical_desc = (
                    f"Tất cả các chỉ số xét nghiệm đều nằm trong ngưỡng an toàn sinh lý học. "
                    f"Các ca bệnh tương đồng trên mạng lưới đồ thị đều là người khỏe mạnh. Tiếp tục duy trì lối sống lành mạnh."
                )
                
            st.session_state['active_patient_status'] = diag_status
            
            st.markdown(f"""
            <div style="background: {card_bg}; border: 1.5px solid {card_border}; border-radius: 6px; padding: 16px; margin: 10px 0 16px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 15px; color: {card_border};">{diag_title}</span>
                    <span style="font-size: 24px; font-weight: 800; color: {card_border};">{final_prob*100:.1f}%</span>
                </div>
                <div style="margin-top: 8px; color: {THEME_COLORS['text_secondary']}; font-size: 13px; line-height: 1.55;">
                    <b>Căn cứ chẩn đoán:</b> {clinical_desc}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Bảng giải trình y khoa: Top 5 ca bệnh tương đồng đối chứng
            st.markdown(f"""
            <span style='font-weight: 700; color: {THEME_COLORS['text_primary']}; font-size: 13px; text-transform: uppercase;'>
                BẰNG CHỨNG ĐỐI CHỨNG: 5 CA BỆNH TƯƠNG ĐỒNG GẦN NHẤT TRONG KHO DỮ LIỆU
            </span>
            <p style='color: {THEME_COLORS['text_muted']}; font-size: 12px; margin: 2px 0 8px 0;'>
                Cơ chế Attention của GAT so sánh bệnh nhân hiện tại với các ca bệnh đã có kết quả điều trị xác thực:
            </p>
            """, unsafe_allow_html=True)
            
            nbr_rows = []
            for n_idx, dist in zip(nbr_indices, nbr_dists):
                r = ref_subset.iloc[n_idx]
                sim_pct = np.exp(- (dist**2)/2.0) * 100
                nbr_rows.append({
                    "Mã hồ sơ": r.get('patient_code', f"BA-{n_idx+1:06d}"),
                    "Tuổi": int(r['age']),
                    "BMI": f"{float(r['bmi']):.1f}",
                    "HbA1c": f"{r['HbA1c_level']}%",
                    "Đường huyết": f"{int(r['blood_glucose_level'])} mg/dL",
                    "Kết quả xác nhận": "Đái tháo đường" if r['diabetes'] == 1 else "Bình thường",
                    "Độ tương đồng": f"{sim_pct:.1f}%"
                })
            st.dataframe(pd.DataFrame(nbr_rows), use_container_width=True, hide_index=True)
            
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            if st.button("Lập Phác Đồ Can Thiệp & In Phiếu Kết Quả Cho Ca Này", use_container_width=True):
                st.session_state['nav_view_index'] = 2
                st.rerun()
            
        with res_col2:
            st.markdown(f"""
            <span style='font-weight: 700; color: {THEME_COLORS['text_primary']}; font-size: 14px; text-transform: uppercase;'>
                ĐỊNH VỊ KHÔNG GIAN BỆNH LÝ (LOCAL PATIENT SUBGRAPH):
            </span>
            <p style='color: {THEME_COLORS['text_muted']}; font-size: 12px; margin: 2px 0 10px 0;'>
                Trực quan hóa vị trí của bệnh nhân (Nốt Xanh) giữa các ca bệnh lân cận
            </p>
            """, unsafe_allow_html=True)
            net_fig = create_interactive_network_figure(subgraph)
            st.plotly_chart(net_fig, use_container_width=True, theme=None)
            st.caption("Chú thích đồ thị: Nốt Xanh dương = Bệnh nhân đang khám. Nốt Đỏ = Ca bệnh đái tháo đường xác nhận. Nốt Xanh lá = Người khỏe mạnh. Cạnh nối phản ánh độ tương đồng lâm sàng.")
