## 2023-10-19 - Missing Security Headers
**Vulnerability:** Fast API application was missing standard security headers (X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security, X-XSS-Protection, Content-Security-Policy).
**Learning:** By default, FastAPI does not automatically include these security headers, leaving endpoints susceptible to risks like clickjacking and XSS.
**Prevention:** Implement a global middleware that automatically injects these headers into every HTTP response.
