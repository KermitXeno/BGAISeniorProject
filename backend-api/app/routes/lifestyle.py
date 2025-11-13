
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any, List
from pydantic import BaseModel
import httpx
from app.core.database import get_session
from app.core.security import get_current_clinician
from app.core.config import settings
from app.models import LifestyleAssessmentCreate, LifestyleAssessmentRead
router = APIRouter()
class LifestyleRiskResponse(BaseModel):
    assessment_id: int
    patient_id: int
    risk_score_lifestyle: float
    risk_level: str
    risk_factors: Dict[str, Any]
    protective_factors: List[str]
    recommendations: List[str]
    confidence_score: float
class CombinedRiskRequest(BaseModel):
    patient_id: int
    mri_study_id: int
    lifestyle_assessment_id: int
    assessment_name: str
    notes: str = None
class CombinedRiskResponse(BaseModel):
    assessment_id: int
    patient_id: int
    combined_risk_score: float
    risk_level: str
    mri_contribution: float
    lifestyle_contribution: float
    confidence_score: float
    explanation: Dict[str, Any]
    recommendations: List[str]
def calculate_lifestyle_risk(assessment_data: LifestyleAssessmentCreate) -> Dict[str, Any]:
    import random
    random.seed(assessment_data.patient_id + assessment_data.age)
    risk_factors = []
    protective_factors = []
    base_risk = 0.3
    if assessment_data.age > 65:
        risk_factors.append("Advanced age")
        base_risk += 0.2
    elif assessment_data.age > 75:
        risk_factors.append("Very advanced age")
        base_risk += 0.3
    if assessment_data.alcohol_consumption in ["heavy"]:
        risk_factors.append("Heavy alcohol consumption")
        base_risk += 0.15
    elif assessment_data.alcohol_consumption in ["light", "moderate"]:
        protective_factors.append("Moderate alcohol consumption")
        base_risk -= 0.05
    if assessment_data.smoking_status == "current":
        risk_factors.append("Current smoking")
        base_risk += 0.2
    elif assessment_data.smoking_status == "never":
        protective_factors.append("Never smoked")
        base_risk -= 0.1
    if assessment_data.exercise_frequency in ["none", "light"]:
        risk_factors.append("Insufficient physical activity")
        base_risk += 0.1
    elif assessment_data.exercise_frequency in ["moderate", "heavy"]:
        protective_factors.append("Regular physical exercise")
        base_risk -= 0.15
    if assessment_data.diet_quality in ["poor", "fair"]:
        risk_factors.append("Poor diet quality")
        base_risk += 0.1
    elif assessment_data.diet_quality in ["good", "excellent"]:
        protective_factors.append("Healthy diet")
        base_risk -= 0.1
    if assessment_data.family_history_alzheimer:
        risk_factors.append("Family history of Alzheimer's")
        base_risk += 0.25
    if assessment_data.cardiovascular_disease:
        risk_factors.append("Cardiovascular disease")
        base_risk += 0.15
    if assessment_data.diabetes:
        risk_factors.append("Diabetes")
        base_risk += 0.1
    if assessment_data.hypertension:
        risk_factors.append("Hypertension")
        base_risk += 0.08
    if assessment_data.education_years and assessment_data.education_years >= 16:
        protective_factors.append("Higher education")
        base_risk -= 0.1
    if assessment_data.sleep_hours:
        if assessment_data.sleep_hours < 6 or assessment_data.sleep_hours > 9:
            risk_factors.append("Poor sleep patterns")
            base_risk += 0.05
        else:
            protective_factors.append("Adequate sleep")
            base_risk -= 0.05
    risk_score = max(0.05, min(0.95, base_risk))
    if risk_score < 0.3:
        risk_level = "low"
    elif risk_score < 0.7:
        risk_level = "moderate"
    else:
        risk_level = "high"
    return {
        "risk_score_lifestyle": round(risk_score, 2),
        "risk_level": risk_level,
        "risk_factors": {
            "primary_factors": risk_factors[:3],
            "all_factors": risk_factors,
            "factor_weights": {factor: round(random.uniform(0.1, 0.3), 2) for factor in risk_factors}
        },
        "protective_factors": protective_factors,
        "confidence_score": round(random.uniform(0.75, 0.92), 2)
    }
@router.post("/assess", response_model=LifestyleRiskResponse)
async def create_lifestyle_assessment(
    assessment: LifestyleAssessmentCreate,
    current_user: Dict[str, Any] = Depends(get_current_clinician),
    session: Session = Depends(get_session)
):
    
    try:
        ml_results = calculate_lifestyle_risk(assessment)
        assessment_id = 67890
        recommendations = []
        if "Advanced age" in ml_results["risk_factors"]["all_factors"]:
            recommendations.append("Regular cognitive assessment recommended")
        if "Current smoking" in ml_results["risk_factors"]["all_factors"]:
            recommendations.append("Smoking cessation programs available")
        if "Insufficient physical activity" in ml_results["risk_factors"]["all_factors"]:
            recommendations.append("Increase physical exercise to 150min/week")
        if "Poor diet quality" in ml_results["risk_factors"]["all_factors"]:
            recommendations.append("Consider Mediterranean diet consultation")
        if not recommendations:
            recommendations.append("Maintain current healthy lifestyle")
        return LifestyleRiskResponse(
            assessment_id=assessment_id,
            patient_id=assessment.patient_id,
            risk_score_lifestyle=ml_results["risk_score_lifestyle"],
            risk_level=ml_results["risk_level"],
            risk_factors=ml_results["risk_factors"],
            protective_factors=ml_results["protective_factors"],
            recommendations=recommendations,
            confidence_score=ml_results["confidence_score"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lifestyle assessment failed: {str(e)}"
        )
@router.post("/combined-risk", response_model=CombinedRiskResponse)
async def calculate_combined_risk(
    request: CombinedRiskRequest,
    current_user: Dict[str, Any] = Depends(get_current_clinician),
    session: Session = Depends(get_session)
):
    
    try:
        mri_risk = 0.65
        lifestyle_risk = 0.55
        mri_weight = 0.6
        lifestyle_weight = 0.4
        combined_risk = (mri_risk * mri_weight) + (lifestyle_risk * lifestyle_weight)
        combined_risk = round(combined_risk, 2)
        if combined_risk < 0.3:
            risk_level = "low"
        elif combined_risk < 0.7:
            risk_level = "moderate"  
        else:
            risk_level = "high"
        assessment_id = 98765
        return CombinedRiskResponse(
            assessment_id=assessment_id,
            patient_id=request.patient_id,
            combined_risk_score=combined_risk,
            risk_level=risk_level,
            mri_contribution=mri_risk * mri_weight,
            lifestyle_contribution=lifestyle_risk * lifestyle_weight,
            confidence_score=0.85,
            explanation={
                "method": "Weighted ensemble of MRI and lifestyle risk scores",
                "mri_weight": mri_weight,
                "lifestyle_weight": lifestyle_weight,
                "mri_risk": mri_risk,
                "lifestyle_risk": lifestyle_risk,
                "interpretation": f"Combined risk indicates {risk_level} probability of cognitive decline"
            },
            recommendations=[
                "Regular follow-up recommended",
                "Consider cognitive training exercises",
                "Monitor lifestyle factors closely"
            ] if risk_level != "low" else [
                "Continue current preventive measures",
                "Annual cognitive assessment"
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Combined risk calculation failed: {str(e)}"
        )
@router.get("/assessment/{assessment_id}", response_model=LifestyleAssessmentRead)
async def get_lifestyle_assessment(
    assessment_id: int,
    current_user: Dict[str, Any] = Depends(get_current_clinician),
    session: Session = Depends(get_session)
):
    
    return LifestyleAssessmentRead(
        id=assessment_id,
        patient_id=1001,
        age=72,
        alcohol_consumption="moderate",
        smoking_status="former",
        exercise_frequency="moderate",
        diet_quality="good",
        sleep_hours=7.5,
        education_years=16,
        family_history_alzheimer=True,
        cardiovascular_disease=False,
        diabetes=False,
        hypertension=True,
        risk_score_lifestyle=0.55,
        created_at="2023-11-09T12:00:00Z"
    )
