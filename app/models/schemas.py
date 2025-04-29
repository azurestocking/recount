from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MessageRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None

class MessageResponse(BaseModel):
    conversation_id: str
    response: str
    tokens_used: int

class TimelineEvent(BaseModel):
    description: str
    confidence: float
    event_date: datetime

class ChatResponse(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    events: Optional[List[TimelineEvent]] = None
    evidence: Optional[List[dict]] = None

