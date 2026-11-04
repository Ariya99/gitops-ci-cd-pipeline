## 2023-11-04 - Missing Authentication on API Endpoints
**Vulnerability:** The `/api/v1/greeting` API endpoint was exposed without any authentication, allowing unauthorized access.
**Learning:** Endpoints mapped under main API routes (e.g. `/api/v1/...`) were intentionally distinct from operational endpoints (`/health`, `/ready`, `/metrics`), but failed to enforce authentication constraints explicitly.
**Prevention:** Always implement authentication on API endpoints unless they are explicitly intended to be public. Use `HTTPBearer` in FastAPI and gracefully handle missing configuration using an HTTP 500 error without exposing internal details.
