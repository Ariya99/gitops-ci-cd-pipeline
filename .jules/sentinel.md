## 2026-10-14 - Add authentication to sensitive endpoints
**Vulnerability:** Missing authentication on the `/api/v1/greeting` endpoint allows unauthenticated users to access potentially sensitive functions and perform unauthorized actions.
**Learning:** The FastAPI application used `HTTPBearer` for authentication but did not apply it to sensitive endpoints, allowing anyone to bypass the authorization check.
**Prevention:** Always verify that sensitive endpoints have authentication applied, using dependency injection correctly as demonstrated with `Depends(verify_token)` applied to the respective endpoints.
