# app/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import register_user, login_user
from app.database.database import get_db
from pydantic import BaseModel
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # Change this to a secure value!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class UserCreate(BaseModel):
    user_name: str
    user_account: str
    user_password: str
    email: str

class UserLogin(BaseModel):
    user_account: str
    user_password: str

router = APIRouter()

@router.post('/register')
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, user_data.model_dump())
        if not user:
            raise HTTPException(status_code=400, detail='User registration failed')
        token = create_access_token({"sub": user.id})
        return {
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'user_name': user.user_name,
                'user_account': user.user_account,
                'email': user.email
            },
            'token': token
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/login')
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    try:
        user = login_user(db, login_data.user_account, login_data.user_password)
        if not user:
            raise HTTPException(status_code=401, detail='Invalid credentials')
        token = create_access_token({"sub": user.id})
        return {
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'user_name': user.user_name,
                'user_account': user.user_account,
                'email': user.email
            },
            'token': token
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
