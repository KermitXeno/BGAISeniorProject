from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any
import httpx
from app.core.config import settings
from app.models import BioModelInput

router = APIRouter()

@router.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify API is working"""
    return {"message": "Models API is working", "ml_service_url": settings.ML_SERVICE_URL}

@router.post("/predict-mri")
async def predict_mri(file: UploadFile = File(...)):
    """
    MRI Model prediction - sends image file to your ModelAPI.py
    Expects: image file
    Returns: {"prediction": "class_name"}
    """
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Forward directly to your ModelAPI.py
        async with httpx.AsyncClient() as client:
            files = {"file": (file.filename, await file.read(), file.content_type)}
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/predictMRI",
                files=files,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"ML service error: {response.status_code}")
                
            result = response.json()
            
        return {
            "prediction": result.get("prediction"),
            "model_type": "MRI_CNN",
            "status": "success",
            "service_url": settings.ML_SERVICE_URL
        }
        
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Cannot connect to ML service at {settings.ML_SERVICE_URL}: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@router.post("/predict-bio")
async def predict_bio(bio_data: BioModelInput):
    """
    BIO Model prediction - sends 8 numeric values to your ModelAPI.py
    Input: BioModelInput with 8 fields (gender, age, educ, ses, mmse, etiv, nwbv, asf)
    Output: {"prediction": "class_name"}
    """
    try:
        # Create exact array format your ModelAPI.py expects: [M/F, Age, EDUC, SES, MMSE, eTIV, nWBV, ASF]
        data_array = [
            bio_data.gender,    # 0=Female, 1=Male
            bio_data.age,       # Age in years
            bio_data.educ,      # Education years
            bio_data.ses,       # Socioeconomic status
            bio_data.mmse,      # Mini Mental State Examination
            bio_data.etiv,      # Estimated total intracranial volume
            bio_data.nwbv,      # Normalized whole brain volume
            bio_data.asf        # Atlas scaling factor
        ]
        
        # Forward to your ModelAPI.py
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/predictBIO",
                json={"data": data_array},
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"ML service error: {response.status_code}")
                
            result = response.json()
            
        return {
            "prediction": result.get("prediction"),
            "input_data": data_array,
            "model_type": "BIO_ML",
            "status": "success",
            "service_url": settings.ML_SERVICE_URL
        }
        
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Cannot connect to ML service at {settings.ML_SERVICE_URL}: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@router.post("/test-bio")
async def test_bio_with_sample_data():
    """Test BIO model with your exact test data: [0, 75, 12, 2.0, 18.0, 1479, 0.657, 1.187]"""
    sample_data = [0, 75, 12, 2.0, 18.0, 1479, 0.657, 1.187]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/predictBIO",
                json={"data": sample_data},
                timeout=30.0
            )
            result = response.json()
            
        return {
            "prediction": result.get("prediction"),
            "test_data": sample_data,
            "model_type": "BIO_ML_TEST",
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "test_data": sample_data,
            "status": "failed"
        }

@router.get("/info")
async def model_info():
    return {
        "available_models": ["MRI", "BIO", "EEG"],
        "mri_model": {
            "input": "Brain MRI image (JPG/PNG)",
            "output": "Classification: Mild/Moderate/No/Severe Impairment",
            "status": "active"
        },
        "bio_model": {
            "input": "8 biomarker fields",
            "fields": ["gender(0/1)", "age", "education", "SES", "MMSE", "eTIV", "nWBV", "ASF"],
            "output": "Classification: No/Very Mild/Mild/Moderate Impairment", 
            "status": "active"
        },
        "eeg_model": {
            "status": "under_construction"
        }
    }