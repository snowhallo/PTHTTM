@echo off
chcp 65001 > nul
title GLUCOGRAPH CDSS - HE THONG HO TRO QUYET DINH LAM SANG
echo ======================================================================
echo    KHOI CHAY HE THONG GLUCOGRAPH CDSS (ENTERPRISE CLINICAL EDITION)
echo    HO TRO RA QUYET DINH LAM SANG CHUAN DOAN & QUAN LY DAI THAO DUONG
echo ======================================================================
echo.

cd /d "%~dp0"

echo [*] Dang khoi dong Tram lam viec Lam sang GlucoGraph CDSS...
echo [*] Trinh duyet web se tu dong mo tai: http://localhost:8501
echo.

python -m streamlit run app.py

pause
