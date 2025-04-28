from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True)
    user_name = Column(String(255), nullable=False)
    user_account = Column(String(255), unique=True, nullable=False)
    user_password = Column(String(255), nullable=False)
    user_role = Column(String(255), default='user', nullable=False)
    email = Column(String(255), unique=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean, default=False) 