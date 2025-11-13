
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.core.database import get_session
from main import app
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///test.db", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
@pytest.fixture(name="clinician_token")
def clinician_token_fixture(client: TestClient):
    response = client.post(
        "/auth/login",
        json={
            "email": "clinician@example.com",
            "password": "secret"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]
@pytest.fixture(name="auth_headers")
def auth_headers_fixture(clinician_token: str):
    return {"Authorization": f"Bearer {clinician_token}"}
