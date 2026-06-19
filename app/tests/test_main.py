from fastapi.testclient import TestClient

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


def test_greeting() -> None:
    response = client.get("/api/v1/greeting")
    assert response.status_code == 200
    assert "message" in response.json()


def test_metrics() -> None:
    client.get("/api/v1/greeting")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
