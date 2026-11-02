## 2024-11-02 - Missing Authentication on API Endpoints
**Vulnerability:** The main API endpoint `/api/v1/greeting` lacked authentication, allowing unauthorized access.
**Learning:** Unauthenticated access to business endpoints was possible because authentication wasn't enforced by default in the FastAPI application.
**Prevention:** Implement HTTPBearer authentication relying on an API_TOKEN and require it via FastAPI's `Depends()` on all `/api/v1/` routes.
