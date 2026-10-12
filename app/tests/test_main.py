import os

from fastapi.testclient import TestClient

os.environ["API_TOKEN"] = "secure-token-123"

from src.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_greeting_unauthorized() -> None:
    response = client.get("/api/v1/greeting")
    assert response.status_code == 403 or response.status_code == 401


def test_greeting_invalid_token() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401


def test_greeting_authorized() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer secure-token-123"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_metrics() -> None:
    client.get("/api/v1/greeting", headers={"Authorization": "Bearer secure-token-123"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
