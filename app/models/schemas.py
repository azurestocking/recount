from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MessageRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

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
    formatted_time: Optional[str] = None

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        if self.event_date:
            self.formatted_time = self.event_date.strftime("%H:%M %p")

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['formatted_time'] = self.formatted_time
        return d

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

# Chat history schemas
class ConversationResponse(BaseModel):
    id: str
    title: str
    status: str
    created_at: datetime
    messages: List[MessageResponse]

    class Config:
        from_attributes = True
