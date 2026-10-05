import os
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import (
    SystemStatus,
    VisitorInfo,
    WelcomeRequest,
    WelcomeResponse,
)

# App initialization
app = FastAPI(
    title="Welcome Experience API",
    description="A modern FastAPI backend welcoming users with dynamic greetings and visitor tracking.",
    version="1.0.0",
)

# Enable CORS for decoupled frontend or local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start time tracking for uptime
APP_START_TIME = time.time()

# In-memory store for demo visitor history
VISITORS_STORE: List[VisitorInfo] = [
    VisitorInfo(
        id=str(uuid.uuid4())[:8],
        name="Alex Mercer",
        role="Cloud Architect",
        greeting="Welcome to the next generation of cloud experiences, Alex!",
        style="futuristic",
        avatar_color="#6366f1",
        timestamp=datetime.now(),
    ),
    VisitorInfo(
        id=str(uuid.uuid4())[:8],
        name="Sarah Connor",
        role="DevOps Specialist",
        greeting="Delighted to have you with us, Sarah. Systems are primed and ready!",
        style="professional",
        avatar_color="#06b6d4",
        timestamp=datetime.now(),
    ),
]

# Preset avatar accent colors for varied UI presentation
AVATAR_PALETTE = ["#6366f1", "#06b6d4", "#ec4899", "#8b5cf6", "#10b981", "#f59e0b"]


def generate_greeting(name: str, role: str, style: str) -> tuple[str, str]:
    """Generates customized headline and personalized greeting note based on chosen style."""
    clean_name = name.strip()
    clean_role = role.strip() if role else "Special Guest"

    styles_map = {
        "warm": (
            f"Hello, {clean_name}! 🌟",
            f"We are genuinely thrilled to welcome you as a {clean_role}! May your journey ahead be productive and joyful.",
        ),
        "professional": (
            f"Welcome aboard, {clean_name}.",
            f"It is a privilege to collaborate with a skilled {clean_role}. Our platform is configured for your highest efficiency.",
        ),
        "futuristic": (
            f"Initiating Greeting Protocol // {clean_name.upper()} ⚡",
            f"Neural link established for {clean_role}. Next-gen FastAPI engine is synchronized and operating at peak capacity.",
        ),
        "playful": (
            f"Woohoo! Look who just joined: {clean_name}! 🎉",
            f"Grab some coffee and enjoy the ride, {clean_role}! Great things are about to happen.",
        ),
    }

    return styles_map.get(style.lower(), styles_map["warm"])


# Static files setup
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", summary="Serve the frontend welcome dashboard")
async def serve_index():
    """Serves the single-page welcome interface."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "message": "Welcome to the FastAPI Demo API! Frontend template is being configured.",
        "docs_url": "/docs",
    }


@app.get("/api/welcome", summary="Default welcome overview")
async def get_default_welcome():
    """Returns general welcome greeting and quick platform stats."""
    return {
        "title": "Welcome to Cloud & Modern Web Platform",
        "description": "An interactive FastAPI + Python full-stack application built for fast, resilient cloud deployments.",
        "server_time": datetime.utcnow().isoformat() + "Z",
        "total_visitors": len(VISITORS_STORE),
        "status": "operational",
    }


@app.post("/api/welcome", response_model=WelcomeResponse, summary="Personalized user welcome")
async def create_welcome_greeting(payload: WelcomeRequest):
    """Processes visitor information, generates a bespoke welcome greeting, and logs the visit."""
    headline, note = generate_greeting(payload.name, payload.role or "Guest", payload.style or "warm")

    color_index = len(VISITORS_STORE) % len(AVATAR_PALETTE)
    avatar_color = AVATAR_PALETTE[color_index]

    visitor_record = VisitorInfo(
        id=str(uuid.uuid4())[:8],
        name=payload.name.strip(),
        role=(payload.role or "Guest").strip(),
        greeting=f"{headline} - {note}",
        style=payload.style or "warm",
        avatar_color=avatar_color,
        timestamp=datetime.now(),
    )

    # Insert at top of feed
    VISITORS_STORE.insert(0, visitor_record)

    # Keep recent 25 visits
    if len(VISITORS_STORE) > 25:
        VISITORS_STORE.pop()

    return WelcomeResponse(
        message=headline,
        personalized_note=note,
        visitor=visitor_record,
        total_visitors=len(VISITORS_STORE),
    )


@app.get("/api/visitors", response_model=List[VisitorInfo], summary="Get recent visitors feed")
async def get_recent_visitors():
    """Returns a list of recent welcomed users."""
    return VISITORS_STORE


@app.get("/api/health", response_model=SystemStatus, summary="Application health probe")
async def get_health_status():
    """Health probe endpoint suitable for Azure App Service or Container Apps liveness checks."""
    uptime = time.time() - APP_START_TIME
    return SystemStatus(
        status="healthy",
        version="1.0.0",
        uptime_seconds=round(uptime, 2),
        total_visitors_served=len(VISITORS_STORE),
        environment=os.getenv("ENVIRONMENT", "production"),
    )
