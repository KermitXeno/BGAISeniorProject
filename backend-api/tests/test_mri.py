
import pytest
from fastapi.testclient import TestClient
import io
def test_mri_upload_success(client: TestClient, auth_headers: dict):
    file_content = b"mock_dicom_file_content"
    files = {
        "file": ("test.dcm", io.BytesIO(file_content), "application/octet-stream")
    }
    data = {
        "patient_id": 1001,
        "study_name": "Test MRI Study",
        "scanner_type": "Siemens Prisma 3T",
        "study_description": "T1-weighted structural MRI"
    }
    response = client.post("/mri/upload", files=files, data=data, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert "study_id" in result
    assert result["processing_status"] == "uploaded"
    assert "file_info" in result
def test_mri_upload_invalid_file_type(client: TestClient, auth_headers: dict):
    file_content = b"invalid_file_content"
    files = {
        "file": ("test.txt", io.BytesIO(file_content), "text/plain")
    }
    data = {
        "patient_id": 1001,
        "study_name": "Test Study"
    }
    response = client.post("/mri/upload", files=files, data=data, headers=auth_headers)
    assert response.status_code == 400
    assert "File type" in response.json()["detail"]
def test_mri_process_study(client: TestClient, auth_headers: dict):
    payload = {
        "study_id": 12345,
        "processing_options": {"preprocessing": True}
    }
    response = client.post("/mri/process", json=payload, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["study_id"] == 12345
    assert "feature_vector" in result
    assert "risk_score_mri" in result
    assert "risk_explanation" in result
    assert 0 <= result["risk_score_mri"] <= 1
def test_get_mri_features(client: TestClient, auth_headers: dict):
    study_id = 12345
    response = client.get(f"/mri/study/{study_id}/features", headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["study_id"] == study_id
    assert "feature_vector" in result
    assert "risk_score_mri" in result
def test_get_mri_study(client: TestClient, auth_headers: dict):
    study_id = 12345
    response = client.get(f"/mri/study/{study_id}", headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == study_id
    assert "patient_id" in result
    assert "processing_status" in result
def test_unauthorized_mri_access(client: TestClient):
    response = client.get("/mri/study/12345")
    assert response.status_code in [401, 403]
