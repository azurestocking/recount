# app/api/v1/auth.py

from fastapi import APIRouter

router = APIRouter()

# Add your auth endpoints here, for example:
@router.post("/login")
async def login():
    return {"message": "Login endpoint"}

@router.post("/register")
async def register():
    return {"message": "Register endpoint"}
