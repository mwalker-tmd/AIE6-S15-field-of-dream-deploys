import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.api import router as api_router
from dotenv import load_dotenv
from starlette.requests import Request

load_dotenv()

app = FastAPI()

# CORS middleware to allow frontend to talk to the backend
allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
if allowed_origins_env:
    try:
        ALLOWED_ORIGINS = json.loads(allowed_origins_env)
        if isinstance(ALLOWED_ORIGINS, str):
            ALLOWED_ORIGINS = [ALLOWED_ORIGINS]
    except json.JSONDecodeError:
        ALLOWED_ORIGINS = [origin.strip() for origin in allowed_origins_env.split(",")]
else:
    ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:7860",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:7860",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware (optional)
@app.middleware("http")
async def log_request_origin(request: Request, call_next):
    origin = request.headers.get("origin")
    print(f"Incoming request from Origin: {origin} | Path: {request.url.path}")
    response = await call_next(request)
    return response

# Include the API endpoints
app.include_router(api_router, prefix="/api")

# Serve frontend in production
if os.getenv("ENVIRONMENT") == "production":
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

# Print available routes on startup
for route in app.routes:
    print(f"🔗 ROUTE: {route.path} → {route.name}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
