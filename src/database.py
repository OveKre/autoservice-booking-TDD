import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.base import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./autoservice.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    """Get a database session."""
    return SessionLocal()


def init_db():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all tables."""
    Base.metadata.drop_all(bind=engine)

