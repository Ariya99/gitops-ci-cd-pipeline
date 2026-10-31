import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def set_api_token(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "test-token")


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_greeting() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_greeting_unauthorized() -> None:
    response = client.get("/api/v1/greeting")
    assert response.status_code == 401  # auto_error=True with HTTPBearer causes 401 not 403


def test_greeting_invalid_token() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401


def test_greeting_missing_env_var(monkeypatch) -> None:
    monkeypatch.delenv("API_TOKEN", raising=False)
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"


def test_metrics() -> None:
    client.get("/api/v1/greeting", headers={"Authorization": "Bearer test-token"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
