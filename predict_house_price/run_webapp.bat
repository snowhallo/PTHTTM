@echo off
title Khoi dong Web Application - PropTech 2024 (06 - taint - 731)
cd /d "%~dp0"
echo ============================================================
echo   KHOI DONG WEB APPLICATION DASHBOARD CHO DU AN
echo   Ma lop: 06 ^| Sinh vien: taint ^| Dinh danh: 731
echo ============================================================
echo.
echo Server dang khoi dong tai: http://127.0.0.1:8000/
echo.

python -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload

pause
