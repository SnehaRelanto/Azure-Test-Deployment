from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class WelcomeRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Name of the visitor")
    role: Optional[str] = Field("Cloud Explorer", max_length=50, description="Visitor title or role")
    style: Optional[str] = Field("warm", description="Greeting style: warm, professional, futuristic, playful")


class VisitorInfo(BaseModel):
    id: str
    name: str
    role: str
    greeting: str
    style: str
    avatar_color: str
    timestamp: datetime


class WelcomeResponse(BaseModel):
    message: str
    personalized_note: str
    visitor: VisitorInfo
    total_visitors: int


class SystemStatus(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    total_visitors_served: int
    environment: str
