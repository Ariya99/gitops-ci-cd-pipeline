## 2025-02-14 - [Sentinel: Missing Authentication on Greeting Endpoint]
**Vulnerability:** The `/api/v1/greeting` API endpoint was completely unauthenticated and accessible by anyone, which was identified when examining the endpoints within the FastAPI `main.py` application file.
**Learning:** Endpoints which may act as sensitive boundaries or perform specific data collection or integrations are currently open by default.
**Prevention:** Implement endpoint authorization by default (such as HTTPBearer or JWT token checking middleware) and verify expected behaviors via automated Pytest cases. Added `HTTPBearer` auth token checking using python's constant time `secrets.compare_digest` to prevent timing attacks.
