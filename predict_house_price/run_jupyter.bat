@echo off
title Khoi dong Jupyter Notebook - Bai tap A1 (06 - taint - 731)
cd /d "%~dp0"
echo ============================================================
echo   KHOI DONG JUPYTER NOTEBOOK CHO DU AN PREDICT HOUSE PRICE
echo   Ma lop: 06 ^| Sinh vien: taint ^| Dinh danh: 731
echo ============================================================
echo.

if exist "C:\Users\Admin\anaconda3\Scripts\jupyter.exe" (
    echo [OK] Dang khoi dong bang Anaconda Jupyter Notebook...
    "C:\Users\Admin\anaconda3\Scripts\jupyter.exe" notebook "notebooks\A1_06_taint_731.ipynb"
) else (
    echo [INFO] Dang khoi dong bang Python Jupyter...
    python -m notebook "notebooks\A1_06_taint_731.ipynb"
)

pause
