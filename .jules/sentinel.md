## 2024-10-12 - Missing API Authentication
**Vulnerability:** The `/api/v1/greeting` endpoint was exposed without any authentication, allowing unauthorized access.
**Learning:** Even simple endpoints need authentication if they perform actions or return data that shouldn't be fully public.
**Prevention:** Implement a standard authentication mechanism like API tokens via headers (`HTTPBearer`) using secure token comparison (`secrets.compare_digest`) for all non-public endpoints.
