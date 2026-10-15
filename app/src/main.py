import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.metrics import REQUEST_COUNT

app = FastAPI(title="GitOps Demo API", version="1.0.0")
security = HTTPBearer(auto_error=False)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify the API token using constant-time comparison."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    expected_token = os.getenv("API_TOKEN")
    if not expected_token:
        # If API_TOKEN is not configured, we should fail securely.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication not configured",
        )

    # Use secrets.compare_digest to prevent timing attacks
    if not secrets.compare_digest(credentials.credentials, expected_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/api/v1/greeting")
def greeting(token: str = Depends(verify_token)) -> dict[str, str]:
    REQUEST_COUNT.labels(method="GET", endpoint="/api/v1/greeting").inc()
    return {"message": "Hello from GitOps CI/CD pipeline"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
