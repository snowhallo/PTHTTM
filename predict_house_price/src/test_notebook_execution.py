import os
import sys
import json
import matplotlib
matplotlib.use('Agg') # Tránh chặn cửa sổ GUI khi test

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

notebook_path = "notebooks/A1_06_taint_731.ipynb"

print(f"=== BẮT ĐẦU KIỂM THỬ THỰC THI JUPYTER NOTEBOOK ({notebook_path}) ===")

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Global namespace
ns = {
    '__name__': '__main__',
    'display': lambda *args: None,
    'HTML': lambda *args: None
}

code_cells = [cell for cell in nb["cells"] if cell["cell_type"] == "code"]
print(f"Tổng số Code Cells: {len(code_cells)}\n")

for i, cell in enumerate(code_cells):
    code = "".join(cell["source"])
    print(f"--- ĐANG CHẠY CELL {i+1} ---")
    try:
        exec(code, ns)
        print(f"[OK] Cell {i+1} chạy thành công 100% không có lỗi!\n")
    except Exception as e:
        print(f"[LỖI Ở CELL {i+1}]: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

print("="*60)
print("TẤT CẢ 7 CODE CELLS CỦA NOTEBOOK ĐỀU CHẠY HOÀN HẢO 100%!")
print("="*60)
