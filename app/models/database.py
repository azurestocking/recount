from sqlalchemy import Column, String, Integer, JSON, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import settings

Base = declarative_base()
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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

# class Evidence(Base):
#     __tablename__ = "evidence"
#
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     conversation_id = Column(String, ForeignKey("conversations.id"))
#     type = Column(String)
#     file_path = Column(String)
#     description = Column(String)
#
#     conversation = relationship("Conversation", back_populates="evidences")


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=True)
    
    type = Column(String)
    file_path = Column(String)
    description = Column(Text)
    meta_data = Column('metadata', JSON)
    created_at = Column(DateTime, default=datetime.now)
    conversation = relationship("Conversation", back_populates="evidences")
    incident = relationship("Incident", back_populates="evidences", foreign_keys=[incident_id])

    @property
    def evidence_metadata(self):
        return self.meta_data

    @evidence_metadata.setter
    def evidence_metadata(self, value):
        self.meta_data = value

class Law(Base):
    __tablename__ = "law"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True)  # 有些law可以没有conversation
    type = Column(String)
    file_path = Column(String)
    description = Column(String)
    meta_data = Column('metadata', JSON)
    created_at = Column(DateTime, default=datetime.now)

class FaissIndex(Base):
    __tablename__ = "faiss_indexes"

    id = Column(String, primary_key=True)
    index_data = Column(LargeBinary, nullable=False)  # FAISS binaries
    id_list = Column(JSON, nullable=True)
