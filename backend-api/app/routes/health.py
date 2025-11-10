from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_session
from sqlmodel import Session, text
router = APIRouter()
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database: str
    version: str
@router.get("/health", response_model=HealthResponse)
async def health_check(session: Session = Depends(get_session)):
    try:
        session.exec(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        timestamp=datetime.utcnow(),
        database=db_status,
        version="1.0.0"
    )
