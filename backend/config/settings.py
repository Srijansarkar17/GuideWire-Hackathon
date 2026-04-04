from __future__ import annotations

"""
Drizzle — Centralized Settings
================================
All environment variables and app-wide constants live here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_PROJECT_ROOT / ".env", override=True)


# ── Firebase ──────────────────────────────────────────────────────
FIREBASE_CREDENTIALS_PATH: str = os.getenv(
    "FIREBASE_CREDENTIALS_PATH",
    os.getenv("FIREBASE_KEY_PATH", str(_PROJECT_ROOT / "firebase_key.json")),
)
FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "drizzle-d76ee")

# One-time super_admin bootstrap via POST /auth/bootstrap-super-admin (optional)
DRIZZLE_BOOTSTRAP_SECRET: str = os.getenv("DRIZZLE_BOOTSTRAP_SECRET", "")

# ── API Keys ──────────────────────────────────────────────────────
OPENAI_API_KEY: str  = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY: str    = os.getenv("GROQ_API_KEY", "")

# ── MCP Server URLs ──────────────────────────────────────────────
MCP_WEATHER_URL: str = os.getenv("MCP_WEATHER_URL", "http://127.0.0.1:8001/score")
MCP_TRAFFIC_URL: str = os.getenv("MCP_TRAFFIC_URL", "http://127.0.0.1:8002/score")
MCP_SOCIAL_URL: str  = os.getenv("MCP_SOCIAL_URL",  "http://127.0.0.1:8003/score")

# ── App Settings ──────────────────────────────────────────────────
ENV: str         = os.getenv("ENV", "development")
DEBUG: bool      = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
SECRET_KEY: str  = os.getenv("SECRET_KEY", "supersecretkey123")
HOST: str        = os.getenv("HOST", "0.0.0.0")
PORT: int        = int(os.getenv("PORT", "8000"))

# ── RBAC Roles ────────────────────────────────────────────────────
class Roles:
    WORKER      = "worker"
    ADMIN       = "admin"
    SUPER_ADMIN = "super_admin"

    ALL = {WORKER, ADMIN, SUPER_ADMIN}

# ── Zone Base Income (INR) ────────────────────────────────────────
ZONE_BASE_INCOME: dict[str, int] = {
    "mumbai":    1400,
    "delhi":     1300,
    "bangalore": 1250,
    "hyderabad": 1100,
    "chennai":   1000,
    "noida":     1100,
    "pune":      1050,
    "kolkata":    950,
    "jaipur":     850,
    "default":   1000,
}
