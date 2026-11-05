# -*- coding: utf-8 -*-
"""
Cấu hình hệ thống phần mềm hỗ trợ ra quyết định lâm sàng: GlucoGraph CDSS
Bảng màu trung tính tương phản cao, chuẩn y tế, tiêu chuẩn chẩn đoán và phác đồ ADA 2024
Tuyệt đối không dùng emoji bừa bãi, không màu mè AI
"""

APP_TITLE = "HỆ THỐNG HỖ TRỢ RA QUYẾT ĐỊNH LÂM SÀNG CHẨN ĐOÁN & QUẢN LÝ ĐÁI THÁO ĐƯỜNG"
APP_SUBTITLE = "GlucoGraph CDSS • Ứng dụng Mạng nơ-ron Đồ thị (Deep Graph Learning) trên Mạng tương đồng Bệnh nhân"
ORGANIZATION_NAME = "KHOA NỘI TIẾT & CHUYỂN HÓA - HỆ THỐNG BỆNH VIỆN THỰC HÀNH"
SYSTEM_VERSION = "GlucoGraph CDSS v2.4 (Enterprise Edition)"

# Bảng màu chuẩn phần mềm y tế lâm sàng (Tương phản cao - Thẻ trắng nổi bật trên nền Slate xám)
THEME_COLORS = {
    "bg_main": "#E2E8F0",          # Nền trang xám Slate rõ nét (Slate 200)
    "bg_card": "#FFFFFF",          # Thẻ chức năng trắng sạch nổi bật
    "bg_sidebar": "#CBD5E1",       # Thanh bên xám đậm hơn một bậc (Slate 300)
    "border": "#94A3B8",           # Viền phân cách xám đậm rõ nét (Slate 400)
    "border_focus": "#2563EB",     # Viền khi focus (Medical Blue)
    "text_primary": "#0F172A",     # Chữ đen than dễ đọc (Slate 900)
    "text_secondary": "#334155",   # Chữ phụ vừa phải (Slate 700)
    "text_muted": "#475569",       # Chữ mờ / nhãn trường đậm hơn (Slate 600)
    "primary": "#2563EB",          # Xanh dương y tế chuẩn (Blue 600)
    "primary_hover": "#1D4ED8",    # Xanh dương đậm khi hover
    "healthy": "#16A34A",          # Xanh lá y tế (Âm tính / Bình thường)
    "diabetes": "#DC2626",         # Đỏ lâm sàng (Dương tính / Nguy cơ cao)
    "warning": "#D97706"           # Vàng cam (Tiền đái tháo đường)
}

# Tiêu chuẩn chẩn đoán y khoa ADA 2024 (American Diabetes Association)
ADA_STANDARDS = {
    "hba1c": {
        "normal": (0.0, 5.7),
        "prediabetes": (5.7, 6.4),
        "diabetes": 6.5,
        "unit": "%",
        "label": "Chỉ số xét nghiệm HbA1c"
    },
    "glucose": {
        "normal": (0, 100),
        "prediabetes": (100, 125),
        "diabetes": 126,
        "unit": "mg/dL",
        "label": "Đường huyết lúc đói (FPG)"
    },
    "bmi": {
        "normal": (18.5, 24.9),
        "overweight": (25.0, 29.9),
        "obese": 30.0,
        "unit": "kg/m²",
        "label": "Chỉ số khối cơ thể (BMI)"
    }
}

# Hướng dẫn can thiệp lâm sàng theo ADA 2024
CLINICAL_PROTOCOLS = {
    "diabetes": {
        "title": "ĐÁI THÁO ĐƯỜNG TYPE 2 (XÁC NHẬN NGUY CƠ CAO)",
        "color": THEME_COLORS["diabetes"],
        "bg_color": "#FEF2F2",
        "target_hba1c": "< 7.0% (Cá thể hóa < 6.5% nếu còn trẻ, không bệnh kèm)",
        "lifestyle": [
            "Kiểm soát calo khẩu phần ăn: Giảm lượng carbohydrate tinh chế, tăng chất xơ hòa tan (rau xanh, yến mạch).",
            "Vận động thể lực: Tối thiểu 150 phút/tuần bài tập aerobic cường độ trung bình (đi bộ nhanh, bơi, đạp xe).",
            "Theo dõi đường huyết: Đo đường huyết đói và sau ăn 2 giờ theo hướng dẫn của bác sĩ điều trị."
        ],
        "medication": [
            "Thuốc đầu tay: Metformin 500mg, uống 1 viên/ngày sau bữa ăn, chỉnh liều tăng dần sau 1-2 tuần lên 1000mg x 2 lần/ngày.",
            "Phối hợp thuốc: Nếu có bệnh lý tim mạch xơ vữa hoặc suy tim/bệnh thận mạn kèm theo, chỉ định phối hợp sớm thuốc ức chế SGLT2 (Empagliflozin/Dapagliflozin) hoặc đồng vận GLP-1 RA."
        ],
        "contraindications": [
            "Chống chỉ định Metformin khi suy thận nặng (độ lọc cầu thận ước tính eGFR < 30 mL/phút/1.73m²).",
            "Thận trọng ngưng thuốc tạm thời trước khi can thiệp chụp phim có tiêm thuốc cản quang hoặc phẫu thuật lớn."
        ],
        "follow_up": "Tái khám kiểm tra chỉ số HbA1c và chức năng thận định kỳ mỗi 3 tháng một lần."
    },
    "prediabetes": {
        "title": "TIỀN ĐÁI THÁO ĐƯỜNG (NGUY CƠ TRUNG BÌNH)",
        "color": THEME_COLORS["warning"],
        "bg_color": "#FFFBEB",
        "target_hba1c": "< 5.7% (Đưa về ngưỡng bình thường)",
        "lifestyle": [
            "Chương trình can thiệp lối sống tích cực (DPP - Diabetes Prevention Program): Mục tiêu giảm 5% - 7% cân nặng ban đầu nếu thừa cân/béo phì.",
            "Tập thể dục cường độ vừa phải 150 phút/tuần chia đều ít nhất 3-5 ngày, không nghỉ quá 2 ngày liên tiếp.",
            "Hạn chế đồ uống có đường, nước ngọt có ga và bánh kẹo ngọt."
        ],
        "medication": [
            "Xem xét điều trị Metformin dự phòng ở bệnh nhân có BMI >= 35, tuổi < 60, hoặc phụ nữ có tiền sử đái tháo đường thai kỳ."
        ],
        "contraindications": [
            "Theo dõi tác dụng phụ tiêu hóa (đầy hơi, buồn nôn) nếu có sử dụng Metformin dự phòng."
        ],
        "follow_up": "Xét nghiệm lại HbA1c và đường huyết lúc đói mỗi 6 tháng đến 12 tháng để đánh giá tiến triển."
    },
    "normal": {
        "title": "BÌNH THƯỜNG (NGUY CƠ THẤP)",
        "color": THEME_COLORS["healthy"],
        "bg_color": "#F0FDF4",
        "target_hba1c": "< 5.7%",
        "lifestyle": [
            "Duy trì chế độ ăn uống cân bằng sinh học: Đủ chất đạm, chất xơ, vitamin và khoáng chất.",
            "Duy trì thể trạng BMI lý tưởng trong khoảng 18.5 - 22.9 kg/m² (chuẩn châu Á).",
            "Duy trì thói quen vận động thể thao đều đặn và ngủ đủ giấc 7-8 giờ mỗi ngày."
        ],
        "medication": [
            "Không có chỉ định sử dụng thuốc hạ đường huyết."
        ],
        "contraindications": [
            "Không áp dụng các chế độ ăn kiêng cực đoan không có chỉ định y khoa."
        ],
        "follow_up": "Khám sức khỏe tổng quát và tầm soát đường huyết định kỳ 1 năm/lần."
    }
}
