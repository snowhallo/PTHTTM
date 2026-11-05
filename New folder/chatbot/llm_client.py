import os
import json
import logging
import urllib.request
from typing import Dict, Any, Optional

logger = logging.getLogger("LLMClient")

class LLMClient:
    """
    Manages API keys and connects to Google Gemini and OpenAI REST APIs.
    """
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            self.config_path = os.path.join(os.path.dirname(__file__), "llm_config.json")
        else:
            self.config_path = config_path
            
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.load_persisted_keys()

    def load_persisted_keys(self):
        """Loads saved API keys from json file if exists."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    if not self.gemini_api_key:
                        self.gemini_api_key = cfg.get("gemini_api_key", "")
                    if not self.openai_api_key:
                        self.openai_api_key = cfg.get("openai_api_key", "")
            except Exception as e:
                logger.warning(f"Failed to load llm_config.json: {e}")

    def set_api_keys(self, gemini_key: str = "", openai_key: str = ""):
        """Dynamically updates and persists API keys for LLM reasoning."""
        if gemini_key is not None:
            self.gemini_api_key = gemini_key.strip()
        if openai_key is not None:
            self.openai_api_key = openai_key.strip()
            
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({
                    "gemini_api_key": self.gemini_api_key,
                    "openai_api_key": self.openai_api_key
                }, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save llm_config.json: {e}")

    def call_gemini(self, query: str, context: Dict[str, Any], ml_pred: Optional[Dict[str, Any]]) -> Optional[str]:
        """Calls Google Gemini REST API with Knowledge Graph context."""
        if not self.gemini_api_key or len(self.gemini_api_key) < 15 or "AQ." in self.gemini_api_key:
            return None

        system_prompt = (
            "Bạn là Chuyên gia Tư vấn Y khoa & Dược phẩm Bệnh Đái tháo đường, được hỗ trợ bởi Đồ thị tri thức (Knowledge Graph) "
            "từ Nhà thuốc Long Châu và mô hình học máy lâm sàng.\n\n"
            f"--- DỮ LIỆU TỪ KNOWLEDGE GRAPH LONG CHÂU ---\n{context.get('formatted_context', '')}\n\n"
        )
        if ml_pred:
            system_prompt += f"--- KẾT QUẢ PHÂN LOẠI LÂM SÀNG ---\n" \
                             f"Phân loại: {ml_pred.get('label')}, Độ tin cậy: {ml_pred.get('confidence')}%, Mức độ nguy cơ: {ml_pred.get('risk_level')}\n\n"
                             
        system_prompt += (
            "HƯỚNG DẪN TRẢ LỜI:\n"
            "1. Trả lời trực tiếp vào câu hỏi của người dùng bằng tiếng Việt chuẩn mực, khoa học, dễ hiểu và thấu cảm.\n"
            "2. Sử dụng thông tin hoạt chất, liều dùng, giá tham khảo tại Long Châu nếu người dùng hỏi về thuốc.\n"
            "3. Luôn giữ thái độ chuyên môn, kèm lời khuyên khám bác sĩ chuyên khoa nội tiết khi cần thiết."
        )
        
        full_prompt = f"{system_prompt}\n\nCâu hỏi người dùng: {query}"
        payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
        encoded_data = json.dumps(payload).encode('utf-8')
        headers = {'Content-Type': 'application/json'}

        candidate_models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-pro"]
        
        for model_name in candidate_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.gemini_api_key}"
                req = urllib.request.Request(url, data=encoded_data, headers=headers)
                with urllib.request.urlopen(req, timeout=4) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    if "candidates" in res_data and len(res_data["candidates"]) > 0:
                        return res_data['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                logger.debug(f"Model {model_name} failed: {e}")
                continue
                
        return None

    def call_openai(self, query: str, context: Dict[str, Any], ml_pred: Optional[Dict[str, Any]]) -> Optional[str]:
        """Calls OpenAI REST API with Knowledge Graph context."""
        if not self.openai_api_key or len(self.openai_api_key) < 15:
            return None
            
        try:
            url = "https://api.openai.com/v1/chat/completions"
            messages = [
                {"role": "system", "content": f"Bạn là Chuyên gia Tư vấn Đái tháo đường & Dược phẩm Long Châu.\nDữ liệu Knowledge Graph:\n{context.get('formatted_context', '')}"},
                {"role": "user", "content": query}
            ]
            payload = {"model": "gpt-4o-mini", "messages": messages, "temperature": 0.3}
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {self.openai_api_key}'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                return res_data['choices'][0]['message']['content']
        except Exception as e:
            logger.warning(f"OpenAI API call failed: {e}")
            return None

llm_client = LLMClient()
