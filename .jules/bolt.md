## 2024-05-20 - Fast FastAPI Static Endpoints
**Learning:** Returning a dictionary in FastAPI causes the framework to run its full serialization pipeline (Pydantic, etc.). For static endpoints, returning a new `JSONResponse` directly avoids this serialization overhead while avoiding global response mutation bugs from middlewares.
**Action:** Use `JSONResponse` for static returns and add `response_model` to the route decorator to preserve OpenAPI schema.
