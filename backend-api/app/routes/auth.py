
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from pydantic import BaseModel, EmailStr
from typing import Dict, Any
from app.core.database import get_session
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_user,
    get_current_clinician
)
from app.core.config import settings
from app.models import User, UserCreate, UserRead
router = APIRouter()
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserRead
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
MOCK_USERS = {
    "clinician@example.com": {
        "id": 1,
        "email": "clinician@example.com",
        "full_name": "Dr. John Smith",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "role": "clinician",
        "is_active": True
    },
    "admin@example.com": {
        "id": 2,
        "email": "admin@example.com",
        "full_name": "Admin User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "role": "admin",
        "is_active": True
    }
}
def authenticate_user(email: str, password: str) -> Dict[str, Any] | None:
    user = MOCK_USERS.get(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user
@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    
    user = authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user["id"]),
            "email": user["email"],
            "role": user["role"],
            "full_name": user["full_name"]
        },
        expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserRead(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            is_active=user["is_active"],
            created_at="2023-01-01T00:00:00Z"
        )
    )
@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    
    return UserRead(
        id=int(current_user["sub"]),
        email=current_user["email"],
        full_name=current_user["full_name"],
        role=current_user["role"],
        is_active=True,
        created_at="2023-01-01T00:00:00Z"
    )
@router.post("/validate-clinician")
async def validate_clinician_access(current_user: Dict[str, Any] = Depends(get_current_clinician)):
    
    return {
        "message": f"Access granted for clinician: {current_user['full_name']}",
        "user_id": current_user["sub"],
        "role": current_user["role"]
    }
