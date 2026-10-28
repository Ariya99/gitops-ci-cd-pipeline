## 2025-01-20 - Missing Authentication on API Endpoints
**Vulnerability:** The `/api/v1/greeting` API endpoint was entirely unauthenticated, meaning anyone could invoke the endpoint and increase the `REQUEST_COUNT` prometheus metric. It also allowed any user to trigger business logic in the backend.
**Learning:** API authentication was missing. We must use `secrets.compare_digest()` to compare API tokens to prevent timing attacks.
**Prevention:** Next time, ensure we have tests that specifically check for a `401 Unauthorized` status response when API token is not provided.