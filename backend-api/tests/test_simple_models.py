import pytest
from fastapi.testclient import TestClient
import io
from PIL import Image

def test_mri_prediction(client: TestClient, auth_headers: dict):
    img = Image.new('RGB', (128, 128), color='gray')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    files = {"file": ("brain_scan.jpg", img_bytes, "image/jpeg")}
    
    response = client.post("/models/predict-mri", files=files, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    
    assert "prediction" in result
    assert "model" in result
    assert result["model"] == "MRI_CNN"

def test_bio_prediction(client: TestClient, auth_headers: dict):
    bio_input = {
        "gender": 0,
        "age": 75,
        "educ": 12, 
        "ses": 2.0,
        "mmse": 18.0,
        "etiv": 1479,
        "nwbv": 0.657,
        "asf": 1.187
    }
    
    response = client.post("/models/predict-bio", json=bio_input, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    
    assert "prediction" in result
    assert "model" in result
    assert result["model"] == "BIO_ML"

def test_model_info(client: TestClient):
    response = client.get("/models/info")
    assert response.status_code == 200
    result = response.json()
    
    assert "mri_model" in result
    assert "bio_model" in result
    assert "eeg_model" in result
    assert result["eeg_model"]["status"] == "under_construction"