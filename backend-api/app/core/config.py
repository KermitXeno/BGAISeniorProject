from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from functools import lru_cache
class Settings(BaseSettings):
    APP_NAME: str = "Alzheimer's Risk Assessment API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql://user:password@localhost/alzheimer_db"
    ECHO_SQL: bool = False
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    MAX_FILE_SIZE: int = 500 * 1024 * 1024
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_MRI_EXTENSIONS: List[str] = [".dcm", ".zip", ".nii", ".nii.gz"]
    MRI_PROCESSING_SERVICE_URL: str = "http://localhost:8001"
    LIFESTYLE_MODEL_SERVICE_URL: str = "http://localhost:8002"
    REDIS_URL: str = "redis://localhost:6379"
    class Config:
        env_file = ".env"
        case_sensitive = True
@lru_cache()
def get_settings() -> Settings:
    return Settings()
settings = get_settings()
