
import pytest
from fastapi.testclient import TestClient
def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "unhealthy"]
    assert "timestamp" in data
    assert "database" in data
    assert "version" in data
def test_login_valid_credentials(client: TestClient):
    response = client.post(
        "/auth/login",
        json={
            "email": "clinician@example.com",
            "password": "secret"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == "clinician@example.com"
    assert data["user"]["role"] == "clinician"
def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/auth/login",
        json={
            "email": "invalid@example.com",
            "password": "wrong"
        }
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
def test_get_current_user(client: TestClient, auth_headers: dict):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "clinician@example.com"
    assert data["role"] == "clinician"
def test_clinician_access_control(client: TestClient, auth_headers: dict):
    response = client.post("/auth/validate-clinician", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "Access granted for clinician" in data["message"]
    assert data["role"] == "clinician"
def test_unauthorized_access(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 403
def test_invalid_token(client: TestClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code in [401, 403]
