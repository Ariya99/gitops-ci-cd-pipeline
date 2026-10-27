## 2024-10-27 - Missing Authentication on API Endpoints
**Vulnerability:** The API endpoint `/api/v1/greeting` lacked any authentication, making it accessible to unauthenticated users.
**Learning:** Endpoints like `/api/v1/...` were exposed without checking for a valid token, potentially allowing unauthorized access to sensitive logic or data, whereas only probes like `/health` should be public.
**Prevention:** Implement an authentication middleware or dependency injection (e.g. `HTTPBearer` in FastAPI) to secure sensitive endpoints and ensure the expected `API_TOKEN` is present and valid using constant-time string comparison.
