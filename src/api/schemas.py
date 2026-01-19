from pydantic import BaseModel
from typing import List, Optional
from datetime import date


# ---------- Image Detection Schemas ----------

class ImageDetection(BaseModel):
    message_id: int
    channel_username: str
    object_class: str
    confidence: float
    image_path: str

    class Config:
        orm_mode = True


# ---------- Search ----------

class SearchQuery(BaseModel):
    keyword: str
    channel: Optional[str] = None


# ---------- Channel Activity ----------

class ChannelActivity(BaseModel):
    channel_username: str
    total_messages: int
    total_images: int
    avg_confidence: float


# ---------- Visual Content Report ----------

class VisualContentReport(BaseModel):
    object_class: str
    detection_count: int
    avg_confidence: float
