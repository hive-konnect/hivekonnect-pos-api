from fastapi.testclient import TestClient

from main import app


def test_health_returns_status_key() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code in {200, 503}
    assert "status" in response.json()
