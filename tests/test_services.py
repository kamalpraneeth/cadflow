import os
import sys

from fastapi.testclient import TestClient

# Add cadflow-backend to path to import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../cadflow-backend')))
from app.database.models import Base
from app.database.session import get_db
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_homepage():
    """Verify the monolith dashboard loads."""
    response = client.get("/")
    assert response.status_code == 200
