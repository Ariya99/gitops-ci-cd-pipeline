## 2024-05-24 - Missing Authentication on API Endpoint
**Vulnerability:** The `/api/v1/greeting` endpoint was accessible without authentication, exposing internal APIs.
**Learning:** Endpoints mapped under `/api/*` were missing the HTTPBearer security dependency, potentially allowing unauthorized access and unthrottled usage.
**Prevention:** Implement HTTPBearer with constant-time token comparison (`secrets.compare_digest`) for all `/api/*` routes and ensure tests assert 401 Unauthorized for missing tokens.