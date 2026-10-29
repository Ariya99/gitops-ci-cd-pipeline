## 2023-10-29 - Missing API Authentication
**Vulnerability:** The `/api/v1/greeting` endpoint was exposed without any authentication, allowing unauthorized access.
**Learning:** Sensitive endpoints (e.g., `/api/v1/...`) must always be protected. Here, we implemented `API_TOKEN` validation via HTTPBearer and securely compared the token using `hmac.compare_digest`.
**Prevention:** Ensure all non-health/metric endpoints have a `Depends` clause invoking an authentication verification function. Always use `hmac.compare_digest` for secure token validation.
