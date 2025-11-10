from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from app.core.config import settings
from app.core.database import engine, create_db_and_tables
from app.routes import auth, health, mri, lifestyle
security = HTTPBearer()
def create_application() -> FastAPI:
    app = FastAPI(
        title="Alzheimer's Risk Assessment API",
        description="Backend API for medical software to assess Alzheimer's risks based on MRI scans and lifestyle factors",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router, tags=["health"])
    app.include_router(auth.router, prefix="/auth", tags=["authentication"])
    app.include_router(mri.router, prefix="/mri", tags=["mri-processing"])
    app.include_router(lifestyle.router, prefix="/lifestyle", tags=["lifestyle-assessment"])
    return app
app = create_application()
@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
