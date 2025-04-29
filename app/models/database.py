from sqlalchemy import Column, String, Integer, JSON, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_name = Column(String, nullable=False)
    user_account = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    user_role = Column(String, nullable=False, default='user')
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False)

    incidents = relationship("Incident", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False, default='in_progress')
    location = Column(String)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship("User", back_populates="incidents")
    conversations = relationship("Conversation", back_populates="incident")
    timeline_events = relationship("TimelineEvent", back_populates="incident")
    evidences = relationship("Evidence", back_populates="incident")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    incident_id = Column(String, ForeignKey("incidents.id"))
    status = Column(String, nullable=False)
    title = Column(String, default='New Conversation')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    conversation_metadata = Column(JSON)
    
    user = relationship("User", back_populates="conversations")
    incident = relationship("Incident", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    events = relationship("TimelineEvent", back_populates="conversation")
    evidences = relationship("Evidence", back_populates="conversation")
    affidavits = relationship("Affidavit", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    message_metadata = Column(JSON)
    tokens_used = Column(Integer)
    
    conversation = relationship("Conversation", back_populates="messages")
    events = relationship("TimelineEvent", back_populates="source_message")

class Affidavit(Base):
    __tablename__ = "affidavits"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    content = Column(Text, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    approved_by = Column(String, ForeignKey("users.id"))
    approved_at = Column(DateTime)
    
    conversation = relationship("Conversation", back_populates="affidavits")
    approver = relationship("User")

class TimelineEvent(Base):
    __tablename__ = "timeline_events"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    incident_id = Column(String, ForeignKey("incidents.id"))
    source_message_id = Column(String, ForeignKey("messages.id"))
    event_date = Column(DateTime)
    description = Column(Text, nullable=False)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    conversation = relationship("Conversation", back_populates="events")
    incident = relationship("Incident", back_populates="timeline_events")
    source_message = relationship("Message", back_populates="events")

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    incident_id = Column(String, ForeignKey("incidents.id"))
    type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    evidence_metadata = Column(JSON)
    
    conversation = relationship("Conversation", back_populates="evidences")
    incident = relationship("Incident", back_populates="evidences")
