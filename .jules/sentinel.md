## 2026-10-15 - [Add authentication to sensitive endpoint]
**Vulnerability:** The `/api/v1/greeting` endpoint was exposed without any authentication, allowing unauthorized users to access potentially sensitive data.
**Learning:** Adding authentication to a FastAPI endpoint requires a secure token verification process. We used a constant-time comparison `secrets.compare_digest` instead of simple equality `==` to prevent timing attacks.
**Prevention:** Ensure that all sensitive endpoints are protected with proper authentication mechanisms and that token comparisons are resistant to timing attacks.
