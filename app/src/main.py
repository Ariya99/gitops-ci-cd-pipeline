import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.metrics import REQUEST_COUNT

app = FastAPI(title="GitOps Demo API", version="1.0.0")
security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> str:
    """Verify the API token."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Security: Use environment variable for token, no hardcoded secrets
    # Ensure a secure default that cannot be bypassed easily if the token is missing.
    # In production, it's safer to reject all tokens if not configured.
    expected_token = os.environ.get("API_TOKEN")

    if not expected_token:
        # If API_TOKEN is missing, we want all authentication to fail
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials", # Don't leak exact reason
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Use secrets.compare_digest for constant-time comparison to prevent timing attacks
    if not secrets.compare_digest(credentials.credentials, expected_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials", # Don't leak exact reason
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}

@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}

@app.get("/api/v1/greeting", dependencies=[Depends(verify_token)])
def greeting() -> dict[str, str]:
    REQUEST_COUNT.labels(method="GET", endpoint="/api/v1/greeting").inc()
    return {"message": "Hello from GitOps CI/CD pipeline"}

@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
