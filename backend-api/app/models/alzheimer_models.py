from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Union
from enum import Enum

class UserRole(str, Enum):
    CLINICIAN = "clinician"
    ADMIN = "admin"

class BioModelInput(BaseModel):
    """
    BIO Model input matching your ModelAPI.py exactly.
    Test data format: [0, 75, 12, 2.0, 18.0, 1479, 0.657, 1.187]
    Order: [M/F, Age, EDUC, SES, MMSE, eTIV, nWBV, ASF]
    Automatically converts string inputs to proper numeric types
    """
    gender: int = Field(..., ge=0, le=1, description="0=Female, 1=Male")
    age: int = Field(..., gt=0, description="Age in years")
    educ: int = Field(..., ge=0, description="Education level (years)")
    ses: float = Field(..., description="Socioeconomic status")
    mmse: float = Field(..., description="Mini Mental State Examination score")
    etiv: int = Field(..., description="Estimated total intracranial volume")
    nwbv: float = Field(..., description="Normalized whole brain volume")
    asf: float = Field(..., description="Atlas scaling factor")
    
    model_config = {"str_strip_whitespace": True}
    
    @field_validator('gender', 'age', 'educ', 'etiv', mode='before')
    @classmethod
    def coerce_to_int(cls, v):
        """Convert string to int if needed"""
        if isinstance(v, str):
            return int(float(v.strip()))
        return int(v)
    
    @field_validator('ses', 'mmse', 'nwbv', 'asf', mode='before')
    @classmethod
    def coerce_to_float(cls, v):
        """Convert string to float if needed"""
        if isinstance(v, str):
            return float(v.strip())
        return float(v)

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    full_name: str
    role: UserRole = UserRole.CLINICIAN

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"