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

# Incident schemas
class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None

class IncidentResponse(IncidentBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Timeline event schemas
class TimelineEventCreate(BaseModel):
    event_date: datetime
    description: str
    confidence_score: Optional[float] = None

class TimelineEventResponse(BaseModel):
    id: str
    event_date: datetime
    description: str
    confidence_score: Optional[float] = None
    created_at: datetime

    class Config:
        orm_mode = True

# Evidence schemas
class EvidenceResponse(BaseModel):
    id: str
    type: str
    file_path: str
    description: Optional[str] = None
    created_at: datetime
    metadata: Optional[dict] = None

    class Config:
        orm_mode = True
