
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlmodel import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
import os
import uuid
from datetime import datetime
import httpx
from app.core.database import get_session
from app.core.security import get_current_clinician
from app.core.config import settings
from app.models import MRIStudyCreate, MRIStudyRead, PatientRead
router = APIRouter()
class MRIUploadResponse(BaseModel):
    study_id: int
    message: str
    file_info: Dict[str, Any]
    processing_status: str
class MRIFeatureResponse(BaseModel):
    study_id: int
    feature_vector: Dict[str, float]
    risk_score_mri: float
    risk_explanation: Dict[str, Any]
    processing_time_seconds: float
class MRIProcessingRequest(BaseModel):
    study_id: int
    processing_options: Optional[Dict[str, Any]] = None
def get_mock_mri_results(study_id: int) -> Dict[str, Any]:
    import random
    random.seed(study_id)
    return {
        "study_id": study_id,
        "feature_vector": {
            "hippocampal_volume": round(random.uniform(3000, 4500), 2),
            "cortical_thickness": round(random.uniform(2.1, 3.2), 3),
            "white_matter_volume": round(random.uniform(450000, 520000), 2),
            "ventricle_size": round(random.uniform(15000, 35000), 2),
            "amyloid_burden": round(random.uniform(0.1, 0.8), 3),
            "tau_distribution": round(random.uniform(0.05, 0.6), 3),
            "brain_atrophy_rate": round(random.uniform(0.5, 2.1), 3),
            "default_mode_network": round(random.uniform(0.3, 0.9), 3)
        },
        "risk_score_mri": round(random.uniform(0.1, 0.9), 2),
        "risk_explanation": {
            "high_risk_features": [
                "Reduced hippocampal volume",
                "Increased ventricle size"
            ] if random.random() > 0.5 else [
                "Cortical thinning detected",
                "White matter changes"
            ],
            "protective_features": [
                "Preserved default mode network",
                "Normal tau distribution"
            ] if random.random() > 0.5 else [
                "Minimal brain atrophy",
                "Low amyloid burden"
            ],
            "confidence_score": round(random.uniform(0.7, 0.95), 2),
            "recommendations": "Consider follow-up scan in 6-12 months"
        },
        "processing_time_seconds": round(random.uniform(45.5, 120.3), 1)
    }
@router.post("/upload", response_model=MRIUploadResponse)
async def upload_mri_file(
    patient_id: int = Form(...),
    study_name: str = Form(...),
    acquisition_date: Optional[str] = Form(None),
    scanner_type: Optional[str] = Form(None),
    study_description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_clinician),
    session: Session = Depends(get_session)
):
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_MRI_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not allowed. Supported: {settings.ALLOWED_MRI_EXTENSIONS}"
        )
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
        )
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    study_id = 12345
    return MRIUploadResponse(
        study_id=study_id,
        message="MRI file uploaded successfully",
        file_info={
            "original_filename": file.filename,
            "stored_filename": filename,
            "file_size": file.size,
            "file_type": file_ext,
            "upload_timestamp": datetime.utcnow().isoformat()
        },
        processing_status="uploaded"
    )
@router.post("/process", response_model=MRIFeatureResponse)
async def process_mri_study(
    request: MRIProcessingRequest,
    current_user: Dict[str, Any] = Depends(get_current_clinician),
    session: Session = Depends(get_session)
):
    
    try:
        ml_results = get_mock_mri_results(request.study_id)
        return MRIFeatureResponse(**ml_results)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MRI processing failed: {str(e)}"
        )
@router.get("/study/{study_id}/features", response_model=MRIFeatureResponse)
async def get_mri_features(
    study_id: int,
    current_user: Dict[str, Any] = Depends(get_current_clinician),
    session: Session = Depends(get_session)
):
    
    mock_results = get_mock_mri_results(study_id)
    return MRIFeatureResponse(**mock_results)
@router.get("/study/{study_id}", response_model=MRIStudyRead)
async def get_mri_study(
    study_id: int,
    current_user: Dict[str, Any] = Depends(get_current_clinician),
    session: Session = Depends(get_session)
):
    
    return MRIStudyRead(
        id=study_id,
        patient_id=1001,
        study_name=f"MRI Study {study_id}",
        acquisition_date=datetime.utcnow(),
        scanner_type="Siemens Prisma 3T",
        study_description="T1-weighted structural MRI",
        processing_status="completed",
        risk_score_mri=0.65,
        created_at=datetime.utcnow()
    )
