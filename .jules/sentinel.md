## 2024-05-16 - Add missing authentication to /api/v1/greeting
**Vulnerability:** The main API endpoint `/api/v1/greeting` lacked any authentication, allowing unauthorized access.
**Learning:** The endpoint was exposed without any security measures, making it vulnerable to unauthorized access and potential misuse. The other endpoints were intentionally left unauthenticated for health/readiness/metrics, but the main API endpoint should have been protected.
**Prevention:** Always ensure that new API endpoints, especially those not related to health/readiness/metrics, implement appropriate authentication (e.g., using `HTTPBearer` with `API_TOKEN`) to prevent unauthorized access.
