from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from .config import settings
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ECHO_SQL,
    pool_pre_ping=True,
    pool_recycle=300,
)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
