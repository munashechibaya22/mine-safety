from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DetectionResponse(BaseModel):
    id: int
    file_path: str
    file_type: str
    is_safe: bool
    confidence: int
    detected_items: str
    missing_items: str
    reason: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_detections: int
    total_accepted: int
    total_denied: int
    recent_detections: List[DetectionResponse]
