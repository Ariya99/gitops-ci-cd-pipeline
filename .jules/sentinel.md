## 2026-10-26 - Add authentication to critical API endpoints
**Vulnerability:** The `/api/v1/greeting` endpoint was exposed without any authentication, allowing unauthorized access.
**Learning:** Sensitive API endpoints should always require authentication by default. Missing authentication can lead to unauthorized data access or abuse.
**Prevention:** Implement an authentication middleware or dependency (like `HTTPBearer` with constant-time token comparison) for all sensitive routes to ensure they are secure by default.
