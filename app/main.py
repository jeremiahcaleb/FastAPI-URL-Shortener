from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

from app.authentication import auth_router
from app.routers import urls, users
from app.database import models
from app.database import engine
from config import Config

# Create all database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="URL Shortener App",
    description="A URL shortener API built with Python and FastAPI",
    version=Config.VERSION
)

# CORS settings (adjust allow_origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix=Config.URL_PREFIX)
app.include_router(users.router, prefix=Config.URL_PREFIX)
app.include_router(urls.router, prefix=Config.URL_PREFIX)

@app.get(f"{Config.URL_PREFIX}/health", tags=["Health"])
async def health_check():
    return {
        "status": "HEALTHY",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "version": Config.VERSION
    }
