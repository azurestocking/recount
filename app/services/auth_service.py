from sqlalchemy.orm import Session
from app.models.user import User
import bcrypt
import uuid
from fastapi import HTTPException

def register_user(db: Session, user_data: dict):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.user_account == user_data['user_account']) |
            (User.email == user_data['email'])
        ).first()
        
        if existing_user:
            if existing_user.user_account == user_data['user_account']:
                raise HTTPException(status_code=400, detail='Username already exists')
            if existing_user.email == user_data['email']:
                raise HTTPException(status_code=400, detail='Email already exists')

        # Hash password
        hashed_password = bcrypt.hashpw(user_data['user_password'].encode('utf-8'), bcrypt.gensalt())
        
        # Create new user
        new_user = User(
            id=str(uuid.uuid4()),
            user_name=user_data['user_name'],
            user_account=user_data['user_account'],
            user_password=hashed_password.decode('utf-8'),
            email=user_data['email']
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Registration failed: {str(e)}')

def login_user(db: Session, user_account: str, user_password: str):
    try:
        user = db.query(User).filter(User.user_account == user_account).first()
        if not user:
            raise HTTPException(status_code=401, detail='Invalid credentials')
            
        if not bcrypt.checkpw(user_password.encode('utf-8'), user.user_password.encode('utf-8')):
            raise HTTPException(status_code=401, detail='Invalid credentials')
            
        return user
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Login failed: {str(e)}') 