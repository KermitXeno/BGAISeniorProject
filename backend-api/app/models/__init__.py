import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB  # works great on Postgres
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
class UserRole(str, Enum):
    CLINICIAN = "clinician"
    ADMIN = "admin"
class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
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
    assessments: List["Assessment"] = Relationship(back_populates="clinician")
class UserCreate(UserBase):
    password: str
class UserRead(UserBase):
    id: int
    created_at: datetime
class PatientBase(SQLModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    medical_record_number: Optional[str] = Field(default=None, unique=True)
class Patient(PatientBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mri_studies: List["MRIStudy"] = Relationship(back_populates="patient")
    lifestyle_assessments: List["LifestyleAssessment"] = Relationship(back_populates="patient")
    assessments: List["Assessment"] = Relationship(back_populates="patient")
class PatientCreate(PatientBase):
    pass
class PatientRead(PatientBase):
    id: int
    created_at: datetime
class MRIStudyBase(SQLModel):
    study_name: str
    acquisition_date: Optional[datetime] = None
    scanner_type: Optional[str] = None
    study_description: Optional[str] = None
class MRIStudy(MRIStudyBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    file_path: str
    file_size: Optional[int] = None
    processing_status: str = Field(default="pending")

    # JSON fields (dict type + real JSONB column)
    feature_vector: Optional[dict] = Field(default=None, sa_column=sa.Column(JSONB))
    risk_explanation: Optional[dict] = Field(default=None, sa_column=sa.Column(JSONB))

    risk_score_mri: Optional[float] = None
    patient: "Patient" = Relationship(back_populates="mri_studies")
    assessments: List["Assessment"] = Relationship(back_populates="mri_study")

class MRIStudyCreate(MRIStudyBase):
    patient_id: int
class MRIStudyRead(MRIStudyBase):
    id: int
    patient_id: int
    processing_status: str
    risk_score_mri: Optional[float] = None
    created_at: datetime
class LifestyleAssessmentBase(SQLModel):
    age: int
    alcohol_consumption: Optional[str] = None
    smoking_status: Optional[str] = None
    exercise_frequency: Optional[str] = None
    diet_quality: Optional[str] = None
    sleep_hours: Optional[float] = None
    education_years: Optional[int] = None
    family_history_alzheimer: Optional[bool] = None
    cardiovascular_disease: Optional[bool] = None
    diabetes: Optional[bool] = None
    hypertension: Optional[bool] = None
class LifestyleAssessment(LifestyleAssessmentBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    risk_score_lifestyle: Optional[float] = None

    # JSON field
    risk_factors: Optional[dict] = Field(default=None, sa_column=sa.Column(JSONB))

    patient: "Patient" = Relationship(back_populates="lifestyle_assessments")
    assessments: List["Assessment"] = Relationship(back_populates="lifestyle_assessment")

class LifestyleAssessmentCreate(LifestyleAssessmentBase):
    patient_id: int
class LifestyleAssessmentRead(LifestyleAssessmentBase):
    id: int
    patient_id: int
    risk_score_lifestyle: Optional[float] = None
    created_at: datetime
class AssessmentBase(SQLModel):
    assessment_name: str
    notes: Optional[str] = None

class Assessment(AssessmentBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    clinician_id: int = Field(foreign_key="user.id")
    mri_study_id: Optional[int] = Field(foreign_key="mristudy.id")
    lifestyle_assessment_id: Optional[int] = Field(foreign_key="lifestyleassessment.id")
    combined_risk_score: Optional[float] = None
    risk_level: Optional[RiskLevel] = None
    recommendation: Optional[str] = None
    patient: Patient = Relationship(back_populates="assessments")
    clinician: User = Relationship(back_populates="assessments")
    mri_study: Optional[MRIStudy] = Relationship(back_populates="assessments")
    lifestyle_assessment: Optional[LifestyleAssessment] = Relationship(back_populates="assessments")
class AssessmentCreate(AssessmentBase):
    patient_id: int
    mri_study_id: Optional[int] = None
    lifestyle_assessment_id: Optional[int] = None
class AssessmentRead(AssessmentBase):
    id: int
    patient_id: int
    clinician_id: int
    combined_risk_score: Optional[float] = None
    risk_level: Optional[RiskLevel] = None
    created_at: datetime
