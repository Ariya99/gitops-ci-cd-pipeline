import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_api_token(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "test_secret_token_123")


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_greeting() -> None:
    headers = {"Authorization": "Bearer test_secret_token_123"}
    response = client.get("/api/v1/greeting", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()


def test_greeting_unauthenticated() -> None:
    response = client.get("/api/v1/greeting")
    assert response.status_code == 401

    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/api/v1/greeting", headers=headers)
    assert response.status_code == 401


def test_metrics() -> None:
    headers = {"Authorization": "Bearer test_secret_token_123"}
    client.get("/api/v1/greeting", headers=headers)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
