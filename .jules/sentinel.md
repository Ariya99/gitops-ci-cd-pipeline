## 2023-10-20 - Fix missing authentication on API endpoint
**Vulnerability:** Missing authentication on the sensitive `/api/v1/greeting` API endpoint.
**Learning:** Adding HTTPBearer authentication requires ensuring constant-time string comparison for the `API_TOKEN` secret comparison to prevent timing attacks.
**Prevention:** Implement an API Gateway or ensure robust HTTPBearer token checking utilizing `secrets.compare_digest` across all sensitive API routes.
