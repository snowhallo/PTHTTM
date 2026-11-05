from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PropertyInput(BaseModel):
    city: str = Field(default="Hà Nội", description="Tỉnh / Thành phố")
    district: str = Field(default="Cầu Giấy", description="Quận / Huyện")
    area: float = Field(default=80.0, ge=15.0, le=200.0, description="Diện tích sàn (15 - 200m2)")
    frontage: float = Field(default=4.5, ge=1.0, le=15.0, description="Mặt tiền (1 - 15m)")
    access_road: float = Field(default=5.0, ge=1.0, le=20.0, description="Đường vào (1 - 20m)")
    floors: float = Field(default=3.0, ge=1.0, le=8.0, description="Số tầng (1 - 8)")
    bedroom: float = Field(default=3.0, ge=1.0, le=8.0, description="Số phòng ngủ (1 - 8)")
    bathroom: float = Field(default=2.0, ge=1.0, le=8.0, description="Số phòng vệ sinh (1 - 8)")
    legal_status: str = Field(default="Have certificate", description="Tình trạng pháp lý")
    house_direction: str = Field(default="Đông - Nam", description="Hướng nhà")
    actual_price: Optional[float] = Field(default=None, description="Giá thực tế nếu là mẫu kiểm thử")

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Câu hỏi hoặc yêu cầu tư vấn BĐS từ người dùng")
    api_key: Optional[str] = Field(default=None, description="Khóa API OpenAI hoặc Google Gemini của người dùng")
    provider: Optional[str] = Field(default="openai", description="Nhà cung cấp AI (openai / gemini)")

class PropertyCard(BaseModel):
    id: int
    district: str
    city: str
    area: float
    price_billion: float
    unit_price_million_m2: float
    frontage: float
    floors: int
    bedroom: int
    legal_status: str
    house_direction: str

class ChatResponse(BaseModel):
    success: bool = True
    reply: str
    cypher_query: str
    matched_properties: List[Dict[str, Any]] = []
    graph_nodes_count: int
    intent: str
    model_used: Optional[str] = "Neo4j Graph Engine"
