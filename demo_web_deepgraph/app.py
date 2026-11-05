# -*- coding: utf-8 -*-
"""
Điểm vào chính của ứng dụng: GlucoGraph CDSS
Hệ Thống Quản Lý & Hỗ Trợ Ra Quyết Định Lâm Sàng Chẩn Đoán & Quản Lý Đái Tháo Đường
Ứng dụng Mạng nơ-ron Đồ thị (Deep Graph Learning) trên Mạng tương đồng Bệnh nhân (Patient Similarity Network)

Thiết kế tối giản, khoa học, chuẩn phần mềm y tế lâm sàng (Clean Neutral Theme)
Tuyệt đối không lạm dụng emoji, không màu mè AI, 100% hướng tới người dùng thực tế.
"""

import streamlit as st
import os
import sys

# Thiết lập đường dẫn thư mục hiện tại để nạp các mô-đun con
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from config import (
    APP_TITLE,
    APP_SUBTITLE,
    ORGANIZATION_NAME,
    SYSTEM_VERSION,
    THEME_COLORS
)
from data_loader import load_dataset
from modules.view_dashboard import render_dashboard_view
from modules.view_consultation import render_consultation_view
from modules.view_treatment import render_treatment_view
from modules.view_records import render_records_view

# -----------------------------------------------------------------------------
# 1. CẤU HÌNH TRANG STREAMLIT (CHUẨN Y TẾ, KHÔNG EMOJI)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GlucoGraph CDSS - Hệ Thống Hỗ Trợ Chẩn Đoán Lâm Sàng",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. INJECTION CSS: CLEAN NEUTRAL CLINICAL THEME (TỐI GIẢN, CHỐNG LỖI MÀU TUYỆT ĐỐI)
# -----------------------------------------------------------------------------
custom_css = f"""
<style>
    /* 1. Nền ứng dụng Slate dịu mắt, tương phản mạnh với các thẻ màu trắng */
    .stApp {{
        background-color: {THEME_COLORS['bg_main']} !important;
        color: {THEME_COLORS['text_primary']} !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    
    /* 2. Thanh bên (Sidebar) phân định rõ ràng */
    [data-testid="stSidebar"] {{
        background-color: {THEME_COLORS['bg_sidebar']} !important;
        border-right: 1.5px solid {THEME_COLORS['border']} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {THEME_COLORS['text_primary']} !important;
    }}
    
    /* 3. Tiêu đề và văn bản có màu đen than sắc nét */
    h1, h2, h3, h4, h5, h6, p, span, label {{
        color: {THEME_COLORS['text_primary']};
    }}
    
    /* 4. Nhãn trường nhập liệu (Widget Labels) */
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span {{
        color: {THEME_COLORS['text_secondary']} !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }}
    
    /* 5. Khung Container viền rõ, thẻ trắng nổi bật trên nền Slate (White Cards on Slate) */
    div[data-testid="stContainer"],
    [data-testid="stContainer"],
    [data-testid="stForm"],
    div[data-testid="stForm"] {{
        background-color: #FFFFFF !important;
        border: 1.5px solid {THEME_COLORS['border']} !important;
        border-radius: 8px !important;
        padding: 18px !important;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.05) !important;
        margin-bottom: 16px !important;
    }}
    
    /* 6. Form nhập liệu lâm sàng */
    [data-testid="stForm"] {{
        background-color: #FFFFFF !important;
        border: 1.5px solid {THEME_COLORS['border']} !important;
        border-radius: 8px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.05) !important;
    }}
    
    /* 7. Input, Selectbox, NumberInput - Đóng khung viền màu xanh y tế rõ rệt ngay từ mặc định */
    [data-testid="stSelectbox"] div[role="group"],
    [data-testid="stSelectbox"] .react-aria-ComboBox div[role="group"],
    [data-testid="stSelectbox"] [data-rac][role="group"],
    [data-testid="stNumberInputContainer"],
    [data-testid="stNumberInput"] div[data-testid="stNumberInputContainer"],
    [data-testid="stTextInputContainer"],
    [data-testid="stTextInput"] div[data-testid="stTextInputContainer"],
    [data-testid="stTextInputRootElement"],
    [data-testid="stTextInput"] div[data-testid="stTextInputRootElement"],
    [data-testid="stTextInput"] .react-aria-TextField > div,
    [data-testid="stTextInput"] div[role="group"],
    [data-testid="stTextInput"] div[data-rac],
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="select"] > div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        background-color: #F8FAFC !important;
        border: 1.5px solid {THEME_COLORS['primary']} !important;
        border-radius: 8px !important;
        color: {THEME_COLORS['text_primary']} !important;
        box-shadow: 0 1px 2px rgba(37, 99, 235, 0.08) !important;
    }}
    [data-testid="stSelectbox"] div[role="group"]:focus-within,
    [data-testid="stNumberInputContainer"]:focus-within,
    [data-testid="stTextInputContainer"]:focus-within,
    [data-testid="stTextInputRootElement"]:focus-within,
    [data-testid="stTextInput"] .react-aria-TextField > div:focus-within,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {{
        border-color: {THEME_COLORS['primary_hover']} !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.25) !important;
    }}
    [data-testid="stSelectbox"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    div[data-baseweb="input"] input,
    input[type="text"], input[type="number"] {{
        color: {THEME_COLORS['text_primary']} !important;
        background-color: transparent !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSelectbox"] button svg {{
        fill: {THEME_COLORS['primary']} !important;
    }}
    [data-testid="stNumberInput"] button {{
        background-color: #EFF6FF !important;
        border-left: 1px solid #BFDBFE !important;
        color: {THEME_COLORS['primary']} !important;
    }}
    [data-testid="stNumberInput"] button:hover {{
        background-color: #DBEAFE !important;
    }}
    
    /* Popover menu của dropdown selectbox */
    div[data-baseweb="popover"],
    ul[data-testid="stSelectboxVirtualDropdown"],
    ul[role="listbox"],
    [data-rac][role="listbox"],
    .react-aria-ListBox {{
        background-color: #FFFFFF !important;
        border: 1.5px solid {THEME_COLORS['primary']} !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15) !important;
    }}
    li[role="option"],
    div[role="option"] {{
        color: {THEME_COLORS['text_primary']} !important;
        background-color: #FFFFFF !important;
        font-size: 13.5px !important;
    }}
    li[role="option"]:hover,
    div[role="option"]:hover,
    li[aria-selected="true"],
    div[aria-selected="true"] {{
        background-color: #EFF6FF !important;
        color: {THEME_COLORS['primary']} !important;
        font-weight: 700 !important;
    }}
    
    /* 8. Nút bấm tiêu chuẩn lâm sàng và Submit Button trong Form */
    [data-testid="stFormSubmitButton"] button,
    button[kind="secondaryFormSubmit"],
    button[kind="primaryFormSubmit"],
    .stButton > button {{
        background-color: {THEME_COLORS['primary']} !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 14.5px !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 22px !important;
        box-shadow: 0 2px 5px rgba(37, 99, 235, 0.3) !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stFormSubmitButton"] button:hover,
    button[kind="secondaryFormSubmit"]:hover,
    button[kind="primaryFormSubmit"]:hover,
    .stButton > button:hover {{
        background-color: {THEME_COLORS['primary_hover']} !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 10px rgba(29, 78, 216, 0.4) !important;
        transform: translateY(-1px) !important;
    }}
    [data-testid="stFormSubmitButton"] button *,
    button[kind="secondaryFormSubmit"] *,
    button[kind="primaryFormSubmit"] *,
    .stButton > button * {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }}
    
    /* 9. Bảng dữ liệu y khoa (Dataframe) */
    [data-testid="stDataFrame"] {{
        border: 1.5px solid {THEME_COLORS['border']} !important;
        border-radius: 6px !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
    }}
    
    /* 10. Thanh cuộn mảnh, gọn gàng */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: {THEME_COLORS['bg_main']};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {THEME_COLORS['border']};
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {THEME_COLORS['border_focus']};
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. NẠP DỮ LIỆU LÂM SÀNG
# -----------------------------------------------------------------------------
df = load_dataset()

# -----------------------------------------------------------------------------
# 4. THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR LÂM SÀNG)
# -----------------------------------------------------------------------------
menu_keys = [
    "1. Giám sát Dịch tễ (Dashboard)",
    "2. Buồng Khám & Chẩn đoán GNN (Consultation)",
    "3. Phác đồ Điều trị ADA 2024 (Care Plan)",
    "4. Hồ sơ Bệnh án EMR (Records)"
]

# Đảm bảo duy trì trạng thái phân hệ hiện tại khi bấm nút submit trong form
if 'nav_selection' not in st.session_state:
    st.session_state['nav_selection'] = menu_keys[0]

# Kiểm tra nếu có yêu cầu chuyển view từ session_state (ví dụ bấm nút chọn bệnh án từ EMR hoặc Buồng khám)
if 'nav_view_index' in st.session_state:
    target_idx = st.session_state.pop('nav_view_index')
    if 0 <= target_idx < len(menu_keys):
        st.session_state['nav_selection'] = menu_keys[target_idx]

with st.sidebar:
    st.markdown(f"""
    <div style="padding: 10px 0 16px 0; border-bottom: 1px solid {THEME_COLORS['border']}; margin-bottom: 16px;">
        <div style="display: inline-block; background: {THEME_COLORS['primary']}; color: #FFFFFF !important; 
                    font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 4px; margin-bottom: 6px; text-transform: uppercase;">
            CLINICAL DECISION SUPPORT
        </div>
        <h3 style="color: {THEME_COLORS['text_primary']}; margin: 0; font-size: 17px; font-weight: 800; line-height: 1.25;">
            GLUCOGRAPH CDSS
        </h3>
        <p style="color: {THEME_COLORS['text_muted']}; font-size: 12px; margin: 3px 0 0 0;">
            Hệ Thống Chẩn Đoán & Quản Lý Đái Tháo Đường
        </p>
        <p style="color: {THEME_COLORS['text_secondary']}; font-size: 11px; margin: 4px 0 0 0;">
            Đơn vị: <b>{ORGANIZATION_NAME}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<span style='color: {THEME_COLORS['text_muted']}; font-size: 11px; font-weight: 700; text-transform: uppercase;'>QUY TRÌNH NGHIỆP VỤ LÂM SÀNG</span>", unsafe_allow_html=True)
    
    choice = st.radio(
        label="Chọn phân hệ làm việc:",
        options=menu_keys,
        key="nav_selection",
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    # Hộp thông số công nghệ & dữ liệu hệ thống
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid {THEME_COLORS['border']}; padding: 13px; border-radius: 6px; font-size: 11.5px;">
        <span style="font-weight: 700; color: {THEME_COLORS['text_primary']}; text-transform: uppercase; font-size: 10.5px;">
            THÔNG SỐ HỆ THỐNG Y TẾ:
        </span>
        <div style="margin-top: 8px; color: {THEME_COLORS['text_secondary']}; line-height: 1.65;">
            • Cơ sở dữ liệu: <b>100.000 hồ sơ</b><br>
            • Động cơ suy luận: <b>GAT 2 Tầng (Graph Attention)</b><br>
            • Độ chính xác (Accuracy): <b>96.85%</b><br>
            • Độ thuần cụm mạng: <b>94.11%</b><br>
            • Chuẩn can thiệp: <b>ADA Standards 2024</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.caption(f"{SYSTEM_VERSION} • Bản quyền vận hành y tế")

# -----------------------------------------------------------------------------
# 5. KHUNG BANNER CHÍNH CỦA ỨNG DỤNG
# -----------------------------------------------------------------------------
st.markdown(f"""
<div style="background-color: #FFFFFF; border: 1.5px solid {THEME_COLORS['border']}; 
            border-left: 5px solid {THEME_COLORS['primary']};
            border-radius: 8px; padding: 18px 22px; margin-bottom: 22px;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="color: {THEME_COLORS['primary']}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 3px;">
                TRẠM LÀM VIỆC LÂM SÀNG & HỖ TRỢ QUYẾT ĐỊNH Y KHOA (CDSS)
            </div>
            <h2 style="color: {THEME_COLORS['text_primary']}; font-size: 21px; font-weight: 800; margin: 0; line-height: 1.25;">
                {APP_TITLE}
            </h2>
            <p style="color: {THEME_COLORS['text_muted']}; font-size: 12.5px; margin: 4px 0 0 0;">
                {APP_SUBTITLE}
            </p>
        </div>
        <div style="display: flex; gap: 10px;">
            <div style="background: {THEME_COLORS['bg_sidebar']}; border: 1px solid {THEME_COLORS['border']}; padding: 8px 14px; border-radius: 6px; text-align: center;">
                <div style="color: {THEME_COLORS['text_muted']}; font-size: 10.5px; text-transform: uppercase;">Động cơ AI</div>
                <div style="color: {THEME_COLORS['primary']}; font-size: 14px; font-weight: 700;">GAT 2 Tầng</div>
            </div>
            <div style="background: {THEME_COLORS['bg_sidebar']}; border: 1px solid {THEME_COLORS['border']}; padding: 8px 14px; border-radius: 6px; text-align: center;">
                <div style="color: {THEME_COLORS['text_muted']}; font-size: 10.5px; text-transform: uppercase;">Độ chính xác</div>
                <div style="color: {THEME_COLORS['healthy']}; font-size: 14px; font-weight: 700;">96.85%</div>
            </div>
            <div style="background: {THEME_COLORS['bg_sidebar']}; border: 1px solid {THEME_COLORS['border']}; padding: 8px 14px; border-radius: 6px; text-align: center;">
                <div style="color: {THEME_COLORS['text_muted']}; font-size: 10.5px; text-transform: uppercase;">Chuẩn y khoa</div>
                <div style="color: {THEME_COLORS['text_primary']}; font-size: 14px; font-weight: 700;">ADA 2024</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. ĐIỀU HƯỚNG TỚI CÁC PHÂN HỆ NGHIỆP VỤ Y TẾ THỰC TẾ
# -----------------------------------------------------------------------------
if df.empty:
    st.error("Không thể kết nối với cơ sở dữ liệu lâm sàng. Vui lòng kiểm tra lại file data/diabetes_100k.csv.")
else:
    if "1. Giám sát Dịch tễ" in choice:
        render_dashboard_view(df)
    elif "2. Buồng Khám" in choice:
        render_consultation_view(df)
    elif "3. Phác đồ Điều trị" in choice:
        render_treatment_view(df)
    elif "4. Hồ sơ Bệnh án EMR" in choice:
        render_records_view(df)

# -----------------------------------------------------------------------------
# 7. CHÂN TRANG HỆ THỐNG PHẦN MỀM
# -----------------------------------------------------------------------------
st.markdown(f"""
<div style="margin-top: 40px; padding-top: 14px; border-top: 1px solid {THEME_COLORS['border']}; 
            display: flex; justify-content: space-between; align-items: center; color: {THEME_COLORS['text_muted']}; font-size: 11.5px;">
    <div>
        Hệ thống: <b>GlucoGraph CDSS</b> • Hỗ trợ ra quyết định lâm sàng chẩn đoán & quản lý đái tháo đường
    </div>
    <div>
        Công nghệ: <b>Deep Graph Learning (GAT)</b> on Patient Similarity Network
    </div>
    <div>
        {SYSTEM_VERSION}
    </div>
</div>
""", unsafe_allow_html=True)
