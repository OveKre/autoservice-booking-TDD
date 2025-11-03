import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.base import Base
from src.database import SessionLocal


@pytest.fixture(scope="function")
def test_db():
    """Create a test database and session."""
    # Create in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def clean_database():
    """Clean database fixture for integration tests."""
    from src.database import engine
    Base.metadata.create_all(bind=engine)
    
    yield
    
    Base.metadata.drop_all(bind=engine)

