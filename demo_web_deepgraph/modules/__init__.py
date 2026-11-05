# -*- coding: utf-8 -*-
"""
Các phân hệ chức năng lâm sàng thực tế của GlucoGraph CDSS:
- view_dashboard: Giám sát dịch tễ & Tổng quan lâm sàng
- view_consultation: Buồng khám & Chẩn đoán đồ thị GNN
- view_treatment: Kế hoạch điều trị & Phác đồ ADA 2024
- view_records: Quản lý hồ sơ bệnh án điện tử EMR
"""

from .view_dashboard import render_dashboard_view
from .view_consultation import render_consultation_view
from .view_treatment import render_treatment_view
from .view_records import render_records_view
