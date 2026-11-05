import re
import logging
from typing import Dict, Any, List, Set
from knowledge_graph.graph_engine import graph_engine

logger = logging.getLogger("EntityExtractor")

class MedicalEntityExtractor:
    """
    Extracts medical entities, numbers, clinical parameters, and intents from user prompts.
    """
    KEYWORD_DICT = {
        "type 1": ["D01"],
        "type 2": ["D02"],
        "tuýp 1": ["D01"],
        "tuýp 2": ["D02"],
        "thai kỳ": ["D03"],
        "tiền đái tháo đường": ["D04"],
        "khát nước": ["S01"],
        "tiểu nhiều": ["S02"],
        "tiểu đêm": ["S02"],
        "sụt cân": ["S03"],
        "ăn nhiều": ["S04"],
        "nhìn mờ": ["S05"],
        "mờ mắt": ["S05"],
        "vết thương": ["S06"],
        "lâu lành": ["S06"],
        "tê bì": ["S07"],
        "chân tay": ["S07"],
        "mệt mỏi": ["S08"],
        "thận": ["C01"],
        "mắt": ["C02"],
        "võng mạc": ["C02"],
        "tim mạch": ["C03"],
        "bàn chân": ["C04"],
        "đoạn chi": ["C04"],
        "metformin": ["M01", "M02"],
        "glucophage": ["M01", "M02"],
        "diamicron": ["M03"],
        "gliclazide": ["M03"],
        "januvia": ["M04"],
        "sitagliptin": ["M04"],
        "galvus": ["M05"],
        "forxiga": ["M06"],
        "dapagliflozin": ["M06"],
        "jardiance": ["M07"],
        "empagliflozin": ["M07"],
        "lantus": ["M08"],
        "insulin": ["DC05", "M08", "M09"],
        "mixtard": ["M09"],
        "glucerna": ["M10"],
        "sữa": ["M10"],
        "dây thìa canh": ["M11"],
        "máy đo": ["M12"],
        "onetouch": ["M12"],
        "chế độ ăn": ["DL01", "DL02"],
        "dinh dưỡng": ["DL01", "DL02"],
        "tập thể dục": ["DL03"],
        "vận động": ["DL03"],
        "huyết áp": ["R05"]
    }

    def extract_keywords_and_intent(self, text: str) -> Dict[str, Any]:
        """Extracts medical entities, numbers, and user intents from user prompt."""
        text_lower = text.lower()
        
        # 1. Clinical parameters extraction (8 features flexible matching)
        glucose_match = re.search(r'(?:glucose|đường huyết|đường máu|blood sugar)\s*(?:là|:|=)?\s*(\d+(?:\.\d+)?)', text_lower) or \
                        re.search(r'(\d+(?:\.\d+)?)\s*(?:mg/dl|mmol/l)?\s*(?:glucose|đường huyết)', text_lower)
                        
        bmi_match = re.search(r'(?:bmi|chỉ số bmi|thể trọng)\s*(?:là|:|=)?\s*(\d+(?:\.\d+)?)', text_lower) or \
                    re.search(r'(\d+(?:\.\d+)?)\s*(?:bmi)', text_lower)
                    
        age_match = re.search(r'(?:tuổi|age)\s*(?:là|:|=)?\s*(\d+)', text_lower) or \
                    re.search(r'(\d+)\s*(?:tuổi|yo|years? old)', text_lower)
                    
        bp_match = re.search(r'(?:huyết áp|blood pressure|bp)\s*(?:tâm trương|là|:|=)?\s*(\d+(?:\.\d+)?)', text_lower)
        insulin_match = re.search(r'(?:insulin|nồng độ insulin)\s*(?:là|:|=)?\s*(\d+(?:\.\d+)?)', text_lower)
        preg_match = re.search(r'(?:mang thai|sinh nở|pregnancies)\s*(?:là|:|=)?\s*(\d+)', text_lower)
        dpf_match = re.search(r'(?:phả hệ|di truyền|pedigree|dpf)\s*(?:là|:|=)?\s*(\d+(?:\.\d+)?)', text_lower)
        skin_match = re.search(r'(?:nếp gấp da|độ dày da|skin thickness)\s*(?:là|:|=)?\s*(\d+(?:\.\d+)?)', text_lower)
        
        clinical_data = {}
        if glucose_match:
            clinical_data["Glucose"] = float(glucose_match.group(1))
        if bmi_match:
            clinical_data["BMI"] = float(bmi_match.group(1))
        if age_match:
            clinical_data["Age"] = float(age_match.group(1))
        if bp_match:
            clinical_data["BloodPressure"] = float(bp_match.group(1))
        if insulin_match:
            clinical_data["Insulin"] = float(insulin_match.group(1))
        if preg_match:
            clinical_data["Pregnancies"] = float(preg_match.group(1))
        if dpf_match:
            clinical_data["DiabetesPedigreeFunction"] = float(dpf_match.group(1))
        if skin_match:
            clinical_data["SkinThickness"] = float(skin_match.group(1))

        # 2. Intent classification
        intents = set()
        
        # Criteria / Blood sugar levels intent
        if any(k in text_lower for k in [
            "chỉ số", "tiêu chuẩn", "chẩn đoán", "hba1c", "bao nhiêu là bị", "bao nhiêu mới bị",
            "mức đường", "ngưỡng đường", "đo đường huyết", "khi nào bị", "xét nghiệm", "tiêu chí"
        ]):
            intents.add("DIAGNOSTIC_CRITERIA")
            
        # Symptoms intent
        if any(k in text_lower for k in [
            "triệu chứng", "dấu hiệu", "biểu hiện", "làm sao biết", "nhận biết", "nhận diện",
            "khát nước", "uống nhiều", "tiểu nhiều", "tiểu đêm", "sụt cân", "ăn nhiều", "mờ mắt", "nhìn mờ", "tê bì", "vết thương"
        ]):
            intents.add("SYMPTOMS")
            
        # Complications intent
        if any(k in text_lower for k in [
            "biến chứng", "nguy hiểm", "hậu quả", "tác hại", "suy thận", "mù mắt", "võng mạc",
            "tim mạch", "đột quỵ", "loét chân", "bàn chân", "hoại tử", "đoạn chi"
        ]):
            intents.add("COMPLICATIONS")
            
        # Diet / Nutrition intent
        if any(k in text_lower for k in [
            "ăn gì", "kiêng gì", "thực đơn", "chế độ ăn", "dinh dưỡng", "uống gì", "món ăn",
            "trái cây", "hoa quả", "gạo lứt", "tinh bột", "đồ ngọt", "sữa"
        ]):
            intents.add("DIET_NUTRITION")
            
        # Exercise intent
        if any(k in text_lower for k in [
            "tập thể dục", "thể thao", "vận động", "chạy bộ", "đi bộ", "tập luyện", "rèn luyện"
        ]):
            intents.add("EXERCISE")
            
        # Type Comparison intent
        if any(k in text_lower for k in [
            "phân biệt", "so sánh type 1", "so sánh tuýp 1", "type 1 và type 2", "tuýp 1 và tuýp 2",
            "khác nhau giữa type 1", "khác nhau giữa tuýp 1"
        ]):
            intents.add("TYPE_COMPARISON")
            
        # Medication intent
        if any(k in text_lower for k in [
            "thuốc", "uống thuốc", "biệt dược", "hoạt chất", "tác dụng phụ", "liều dùng",
            "metformin", "glucophage", "diamicron", "gliclazide", "januvia", "sitagliptin",
            "galvus", "vildagliptin", "forxiga", "dapagliflozin", "jardiance", "empagliflozin",
            "insulin", "lantus", "mixtard", "dây thìa canh", "giá bao nhiêu", "mua ở đâu"
        ]):
            intents.add("MEDICATION")

        # 3. Knowledge Graph Entity Mapping
        matched_node_ids = set()
        for kw, n_ids in self.KEYWORD_DICT.items():
            if kw in text_lower:
                matched_node_ids.update(n_ids)
                
        # Dynamic search in graph engine
        dynamic_search = graph_engine.search_entities(text)
        for item in dynamic_search[:3]:
            matched_node_ids.add(item["id"])
            
        return {
            "clinical_data": clinical_data,
            "intents": list(intents),
            "matched_node_ids": list(matched_node_ids),
            "text": text
        }

entity_extractor = MedicalEntityExtractor()
