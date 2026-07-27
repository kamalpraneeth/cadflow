import os

import httpx

VALIDATOR_URL = os.getenv("VALIDATOR_URL", "http://localhost:8001")
CONVERTER_URL = os.getenv("CONVERTER_URL", "http://localhost:8002")
METADATA_URL = os.getenv("METADATA_URL", "http://localhost:8003")
AI_AGENT_URL = os.getenv("AI_AGENT_URL", "http://localhost:8004")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

def test_services_health():
    """Verify all microservices are up and healthy."""
    services = [VALIDATOR_URL, CONVERTER_URL, METADATA_URL, AI_AGENT_URL, API_GATEWAY_URL]
    for url in services:
        response = httpx.get(f"{url}/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

def test_webhook_endpoint():
    """Test the API Gateway webhook receiver."""
    payload = {
        "action": "opened",
        "number": 1,
        "pull_request": {"head": {"sha": "abcdef"}},
        "filename": "sample.dxf"
    }
    response = httpx.post(
        f"{API_GATEWAY_URL}/webhook/github",
        json=payload,
        headers={"X-GitHub-Event": "pull_request"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
