# -*- coding: utf-8 -*-
"""
Phân hệ 3: Kế Hoạch Điều Trị & Phác Đồ Can Thiệp Lâm Sàng (ADA 2024 Protocols)
Dành cho: Bác sĩ điều trị, Cán bộ tư vấn quản lý bệnh mãn tính
Thiết kế tối giản, chuẩn y khoa, hỗ trợ in phiếu chỉ định lâm sàng, 100% không emoji
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from config import THEME_COLORS, ADA_STANDARDS, CLINICAL_PROTOCOLS, APP_TITLE

def render_treatment_view(df):
    # 1. Thanh tiêu đề phân hệ
    st.markdown(f"""
    <div style="background-color: {THEME_COLORS['bg_card']}; border: 1.5px solid {THEME_COLORS['border']}; 
                border-left: 5px solid {THEME_COLORS['primary']}; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px;
                box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: {THEME_COLORS['primary']}; font-weight: 700; font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px;">
                    PHÂN HỆ KẾ HOẠCH ĐIỀU TRỊ & QUẢN LÝ LÂM SÀNG
                </span>
                <h3 style="color: {THEME_COLORS['text_primary']}; margin: 2px 0 0 0; font-size: 18px; font-weight: 700;">
                    Phác Đồ Can Thiệp Cá Thể Hóa Chuẩn Hóa Theo ADA 2024
                </h3>
            </div>
            <div style="text-align: right; font-size: 12px; color: {THEME_COLORS['text_muted']};">
                Hướng dẫn thực hành y khoa: <b>ADA Standards of Care in Diabetes 2024</b>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Lấy thông tin bệnh nhân đang hoạt động từ Phân hệ 2 hoặc khởi tạo mặc định
    patient_record = st.session_state.get('active_patient_record', None)
    patient_prob = st.session_state.get('active_patient_prob', 0.942)
    patient_status = st.session_state.get('active_patient_status', 'diabetes')
    
    if not patient_record:
        patient_record = {
            "gender": "Female", "age": 62.0, "bmi": 31.2,
            "HbA1c_level": 8.4, "blood_glucose_level": 215,
            "hypertension": 1, "heart_disease": 1, "smoking_history": "former"
        }
        patient_prob = 0.965
        patient_status = "diabetes"
        st.info("Chưa có hồ sơ từ buồng khám. Hệ thống đang hiển thị phác đồ mẫu cho một ca bệnh đái tháo đường nguy cơ cao.")
        
    protocol = CLINICAL_PROTOCOLS[patient_status]
    
    # 3. Thẻ tóm tắt trạng thái bệnh nhân hiện tại
    st.markdown(f"""
    <div style="background: {protocol['bg_color']}; border: 1.5px solid {protocol['color']}; border-radius: 6px; padding: 14px 18px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 11px; font-weight: 700; color: {protocol['color']}; text-transform: uppercase;">
                    CHẨN ĐOÁN XÁC ĐỊNH TỪ HỆ THỐNG GLUCOGRAPH CDSS:
                </span>
                <h4 style="color: {protocol['color']}; margin: 4px 0 0 0; font-size: 17px; font-weight: 800;">
                    {protocol['title']}
                </h4>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 11.5px; color: {THEME_COLORS['text_muted']};">Xác suất nguy cơ GNN:</span><br>
                <b style="font-size: 22px; color: {protocol['color']}; font-weight: 800;">{patient_prob*100:.1f}%</b>
            </div>
        </div>
        <div style="margin-top: 10px; font-size: 12.5px; color: {THEME_COLORS['text_secondary']}; border-top: 1px solid rgba(0,0,0,0.06); padding-top: 8px;">
            <b>Thông số lâm sàng:</b> Tuổi: {int(patient_record['age'])} | Giới tính: {patient_record['gender']} | BMI: {patient_record['bmi']:.1f} kg/m² | 
            HbA1c: <b>{patient_record['HbA1c_level']}%</b> | Đường huyết đói: <b>{patient_record['blood_glucose_level']} mg/dL</b> | 
            Tăng huyết áp: {'Có' if patient_record['hypertension'] == 1 else 'Không'} | Tim mạch: {'Có' if patient_record['heart_disease'] == 1 else 'Không'}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. Chi tiết phác đồ can thiệp 3 tầng theo chuẩn ADA 2024
    col_p1, col_p2 = st.columns([1, 1], gap="medium")
    
    with col_p1:
        with st.container(border=True):
            st.markdown(f"""<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<span style="font-weight: 700; color: {THEME_COLORS['primary']}; font-size: 14px; text-transform: uppercase;">1. MỤC TIÊU ĐIỀU TRỊ KIỂM SOÁT</span>
<span style="background: #E2E8F0; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 12px; color: {THEME_COLORS['primary']};">Mục tiêu HbA1c: {protocol['target_hba1c']}</span>
</div>
<p style="color: {THEME_COLORS['text_secondary']}; font-size: 13px; line-height: 1.5; margin: 6px 0 14px 0;">
Mục tiêu kiểm soát đường huyết cá thể hóa nhằm giảm thiểu tối đa nguy cơ biến chứng vi mạch (mắt, thận, thần kinh) và biến chứng mạch máu lớn.
</p>
<div style="font-weight: 700; color: {THEME_COLORS['text_primary']}; font-size: 13px; text-transform: uppercase; margin-bottom: 8px;">
2. CAN THIỆP LỐI SỐNG & DINH DƯỠNG:
</div>""", unsafe_allow_html=True)
            for item in protocol['lifestyle']:
                st.markdown(f"• {item}")
        
    with col_p2:
        with st.container(border=True):
            st.markdown(f"""<div style="font-weight: 700; color: {THEME_COLORS['primary']}; font-size: 14px; text-transform: uppercase; margin-bottom: 8px;">
3. PHÁC ĐỒ DÙNG THUỐC (PHARMACOTHERAPY)
</div>""", unsafe_allow_html=True)
            for med in protocol['medication']:
                st.markdown(f"• {med}")
            
            contra_items = "".join([f"<div style='color: #991B1B; font-size: 12px; margin-bottom: 4px;'>• {c}</div>" for c in protocol['contraindications']])
            st.markdown(f"""<div style="margin-top: 14px; background: #FEF2F2; border-left: 4px solid #DC2626; border: 1px solid #FECACA; padding: 12px 14px; border-radius: 6px;">
<div style="font-weight: 700; color: #DC2626; font-size: 12px; text-transform: uppercase; margin-bottom: 6px;">CẢNH BÁO AN TOÀN & CHỐNG CHỈ ĐỊNH:</div>
{contra_items}
</div>""", unsafe_allow_html=True)
        
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    
    # 5. Phiếu Tóm Tắt Kết Luận Lâm Sàng & Chỉ Định Y Khoa (Printable Clinical Summary)
    with st.container(border=True):
        st.markdown(f"""
        <div style="border-bottom: 2px solid {THEME_COLORS['primary']}; padding-bottom: 10px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <span style="font-size: 11px; font-weight: 700; color: {THEME_COLORS['text_muted']}; text-transform: uppercase;">BỆNH VIỆN THỰC HÀNH Y DƯỢC • KHOA NỘI TIẾT</span>
                <h3 style="color: {THEME_COLORS['text_primary']}; margin: 2px 0 0 0; font-size: 18px; font-weight: 800;">
                    PHIẾU KẾT QUẢ CHẨN ĐOÁN & CHỈ ĐỊNH CAN THIỆP LÂM SÀNG
                </h3>
            </div>
            <div style="text-align: right; font-size: 11.5px; color: {THEME_COLORS['text_muted']};">
                Mã phiếu: <b>GLUCO-{datetime.now().strftime('%Y%m%d%H%M')}</b><br>
                Ngày khám: <b>{datetime.now().strftime('%d/%m/%Y')}</b>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 12.5px; margin-bottom: 14px;">
            <div>• <b>Họ tên bệnh nhân:</b> Bệnh nhân khám lâm sàng</div>
            <div>• <b>Tuổi:</b> {int(patient_record['age'])} tuổi &nbsp;&nbsp;&nbsp;• <b>Giới tính:</b> {patient_record['gender']}</div>
            <div>• <b>Chỉ số khối cơ thể (BMI):</b> {patient_record['bmi']:.1f} kg/m²</div>
            <div>• <b>Chỉ số HbA1c:</b> {patient_record['HbA1c_level']}% (Chuẩn ADA: &lt; 5.7%)</div>
            <div>• <b>Đường huyết đói (FPG):</b> {patient_record['blood_glucose_level']} mg/dL (Chuẩn: &lt; 100 mg/dL)</div>
            <div>• <b>Bệnh lý nền:</b> {'Tăng huyết áp' if patient_record['hypertension']==1 else 'Không THA'}, {'Tim mạch' if patient_record['heart_disease']==1 else 'Không tim mạch'}</div>
        </div>
        
        <div style="background: {THEME_COLORS['bg_main']}; border: 1px solid {THEME_COLORS['border']}; padding: 12px 14px; border-radius: 6px; font-size: 12.5px; margin-bottom: 14px;">
            <b>KẾT LUẬN TỔNG QUÁT TỪ HỆ THỐNG GLUCOGRAPH CDSS:</b><br>
            <span style="color: {protocol['color']}; font-weight: 700;">{protocol['title']}</span> (Xác suất nguy cơ đồ thị: <b>{patient_prob*100:.1f}%</b>).<br>
            <i>{protocol['follow_up']}</i>
        </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns([4, 1])
        with btn_c1:
            st.caption("Hệ thống xác thực: GlucoGraph CDSS v2.4 (Deep Graph Learning on Patient Similarity Network)")
        with btn_c2:
            if st.button("In Phiếu Kết Quả", use_container_width=True):
                st.success("Lệnh in đã được chuẩn bị. Bạn có thể sử dụng phím tắt Ctrl + P trên trình duyệt để in phiếu này.")
