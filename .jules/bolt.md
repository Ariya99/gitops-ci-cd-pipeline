## 2026-10-24 - Initializing Bolt Journal
**Learning:** Returning JSONResponse directly avoids serialization overhead for static endpoints in FastAPI.
**Action:** Use JSONResponse directly but avoid global instances to prevent mutation bugs from middlewares.
