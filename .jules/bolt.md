## 2024-03-24 - Optimizing FastAPI static endpoint serialization
**Learning:** Returning a Python dictionary from a FastAPI endpoint forces the framework to do a relatively expensive internal serialization step.
**Action:** For simple static responses, return a `fastapi.responses.JSONResponse` directly to bypass this overhead, but add `response_model=...` to the route decorator to preserve OpenAPI schema documentation. Avoid mutating global `JSONResponse` objects across requests.
