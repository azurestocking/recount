from sqlalchemy import Column, String, Integer, JSON, ForeignKey, DateTime, Float
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


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    status = Column(String, default='active')
    title = Column(String, default='New Conversation')
    created_at = Column(DateTime, default=datetime.now)
    
    messages = relationship("Message", back_populates="conversation")
    events = relationship("TimelineEvent", back_populates="conversation")
    evidences = relationship("Evidence", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    tokens_used = Column(Integer, default=0)
    message_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    
    conversation = relationship("Conversation", back_populates="messages")
    events = relationship("TimelineEvent", back_populates="source_message")

class TimelineEvent(Base):
    __tablename__ = "timeline_events"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    source_message_id = Column(String, ForeignKey("messages.id"))
    event_date = Column(DateTime)
    description = Column(String)
    confidence_score = Column(Float)
    
    conversation = relationship("Conversation", back_populates="events")
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
    type = Column(String)
    file_path = Column(String)
    description = Column(String)
    meta_data = Column('metadata', JSON)
    created_at = Column(DateTime, default=datetime.now)

    conversation = relationship("Conversation", back_populates="evidences")


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
