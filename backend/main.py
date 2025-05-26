import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api import router as api_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Serve frontend in production
if os.getenv("ENVIRONMENT") == "production":
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

# Debug mode: print routes
if os.getenv("DEBUG", "false").lower() == "true":
    for route in app.routes:
        print(f"🔗 ROUTE: {route.path} → {route.name}")
