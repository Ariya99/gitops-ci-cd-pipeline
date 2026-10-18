## 2024-05-24 - Add authentication to unauthenticated API endpoint
**Vulnerability:** The API endpoint `/api/v1/greeting` was accessible without any authentication, exposing internal functionality or potential sensitive info unnecessarily.
**Learning:** Endpoints mapped to APIs should consistently employ authentication decorators by default unless explicitly meant to be public, such as health checks.
**Prevention:** Always use FastAPI dependencies (e.g. `Depends(verify_token)`) leveraging built-in security features like `HTTPBearer` with a secure, constant-time comparison against expected secrets. Tests should enforce valid token paths and failure modes via mocked configurations.
