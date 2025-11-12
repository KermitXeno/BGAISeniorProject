from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    CLINICIAN = "clinician"
    ADMIN = "admin"

class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str
    role: UserRole = Field(default=UserRole.CLINICIAN)
    is_active: bool = Field(default=True)

class User(UserBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

class BioModelInput(BaseModel):
    gender: int = Field(..., ge=0, le=1, description="0=Female, 1=Male")
    age: int = Field(..., gt=0, description="Age in years")
    educ: int = Field(..., ge=0, description="Years of education") 
    ses: float = Field(..., description="Socioeconomic status")
    mmse: float = Field(..., description="Mini Mental State Examination score")
    etiv: int = Field(..., description="Estimated total intracranial volume")
    nwbv: float = Field(..., description="Normalized whole brain volume")
    asf: float = Field(..., description="Atlas scaling factor")