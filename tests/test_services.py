import os
import sys
from fastapi.testclient import TestClient

# Add cadflow-backend to path to import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../cadflow-backend')))
from app.main import app

client = TestClient(app)

def test_homepage():
    """Verify the monolith dashboard loads."""
    response = client.get("/")
    assert response.status_code == 200
