## 2023-10-25 - Missing authentication on sensitive endpoints
**Vulnerability:** The main API endpoint `/api/v1/greeting` lacked any authentication, making it publicly accessible and susceptible to unauthorized access or abuse.
**Learning:** Endpoints were initially created without security constraints, likely prioritizing functionality over security during initial development.
**Prevention:** Establish a default-deny pattern for new API endpoints. Ensure that all main API routes require explicit authentication dependencies unless purposefully exposed (like health or metrics endpoints).
