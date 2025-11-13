
import pytest
from fastapi.testclient import TestClient
def test_lifestyle_assessment_creation(client: TestClient, auth_headers: dict):
    payload = {
        "patient_id": 1001,
        "age": 72,
        "alcohol_consumption": "moderate",
        "smoking_status": "former",
        "exercise_frequency": "moderate",
        "diet_quality": "good",
        "sleep_hours": 7.5,
        "education_years": 16,
        "family_history_alzheimer": True,
        "cardiovascular_disease": False,
        "diabetes": False,
        "hypertension": True
    }
    response = client.post("/lifestyle/assess", json=payload, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert "assessment_id" in result
    assert result["patient_id"] == 1001
    assert "risk_score_lifestyle" in result
    assert "risk_level" in result
    assert "recommendations" in result
    assert 0 <= result["risk_score_lifestyle"] <= 1
def test_lifestyle_high_risk_factors(client: TestClient, auth_headers: dict):
    payload = {
        "patient_id": 1002,
        "age": 80,
        "alcohol_consumption": "heavy",
        "smoking_status": "current",
        "exercise_frequency": "none",
        "diet_quality": "poor",
        "sleep_hours": 4.0,
        "education_years": 8,
        "family_history_alzheimer": True,
        "cardiovascular_disease": True,
        "diabetes": True,
        "hypertension": True
    }
    response = client.post("/lifestyle/assess", json=payload, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["risk_level"] in ["moderate", "high"]
    assert len(result["risk_factors"]["all_factors"]) > 3
def test_lifestyle_low_risk_factors(client: TestClient, auth_headers: dict):
    payload = {
        "patient_id": 1003,
        "age": 45,
        "alcohol_consumption": "light",
        "smoking_status": "never",
        "exercise_frequency": "heavy",
        "diet_quality": "excellent",
        "sleep_hours": 8.0,
        "education_years": 20,
        "family_history_alzheimer": False,
        "cardiovascular_disease": False,
        "diabetes": False,
        "hypertension": False
    }
    response = client.post("/lifestyle/assess", json=payload, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["risk_level"] == "low"
    assert len(result["protective_factors"]) > 2
def test_combined_risk_calculation(client: TestClient, auth_headers: dict):
    payload = {
        "patient_id": 1001,
        "mri_study_id": 12345,
        "lifestyle_assessment_id": 67890,
        "assessment_name": "Comprehensive Risk Assessment",
        "notes": "Regular follow-up patient"
    }
    response = client.post("/lifestyle/combined-risk", json=payload, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert "assessment_id" in result
    assert "combined_risk_score" in result
    assert "risk_level" in result
    assert "mri_contribution" in result
    assert "lifestyle_contribution" in result
    assert "explanation" in result
    assert 0 <= result["combined_risk_score"] <= 1
def test_get_lifestyle_assessment(client: TestClient, auth_headers: dict):
    assessment_id = 67890
    response = client.get(f"/lifestyle/assessment/{assessment_id}", headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == assessment_id
    assert "patient_id" in result
    assert "age" in result
def test_lifestyle_assessment_missing_fields(client: TestClient, auth_headers: dict):
    payload = {
        "patient_id": 1004,
        "age": 65
    }
    response = client.post("/lifestyle/assess", json=payload, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert "risk_score_lifestyle" in result
def test_unauthorized_lifestyle_access(client: TestClient):
    payload = {"patient_id": 1001, "age": 65}
    response = client.post("/lifestyle/assess", json=payload)
    assert response.status_code in [401, 403]
