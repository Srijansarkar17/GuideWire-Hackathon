"""
Drizzle — Phase 2 Backend
===========================
Production-grade FastAPI backend with:
  • Firebase Authentication
  • Firestore Database
  • RBAC (Worker / Admin / Super Admin)
  • Multi-role Dashboard APIs
  • Fraud Detection Engine
  • Premium Calculation Engine

Run:
    uvicorn backend.main:app --port 8000 --reload

Swagger UI:
    http://localhost:8000/docs
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config.settings import ENV, DEBUG, HOST, PORT
from backend.middleware.logging import RequestLoggingMiddleware

# ── Logging ───────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s  %(levelname)-8s  [%(name)s]  %(message)s",
)
log = logging.getLogger("drizzle")


# ── Lifespan (startup/shutdown) ───────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("=" * 60)
    log.info("  🌧️  DRIZZLE — Parametric Insurance Platform")
    log.info(f"  Phase 2 Backend | ENV={ENV}")
    log.info("=" * 60)

    # Firebase is initialized on import in config/firebase.py
    from backend.config.firebase import db
    log.info("Firebase Firestore client ready")

    yield

    log.info("Drizzle backend shutting down")


# ── FastAPI App ───────────────────────────────────────────────────
app = FastAPI(
    title="Drizzle — Parametric Insurance API",
    description=(
        "AI-powered parametric insurance for gig workers. "
        "Phase 2: Firebase Auth + Firestore + RBAC + Dashboard APIs."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)


# ── Register Routers ─────────────────────────────────────────────
from backend.routes.auth_routes import router as auth_router
from backend.routes.worker_routes import router as worker_router
from backend.routes.policy_routes import router as policy_router
from backend.routes.claim_routes import router as claim_router
from backend.routes.dashboard_routes import router as dashboard_router

app.include_router(auth_router)
app.include_router(worker_router)
app.include_router(policy_router)
app.include_router(claim_router)
app.include_router(dashboard_router)


# ── Root & Health ─────────────────────────────────────────────────
@app.get("/", tags=["System"])
async def root():
    return {
        "service": "Drizzle — Parametric Insurance API",
        "version": "2.0.0",
        "phase":   "Phase 2 — Firebase + RBAC + Dashboards",
        "docs":    "/docs",
        "endpoints": {
            "POST /workers/register":     "Register a new worker",
            "POST /policies/create":      "Create a policy (Admin)",
            "GET  /policies/{worker_id}": "Get policies for a worker",
            "POST /claims/trigger":       "Trigger an insurance claim",
            "GET  /claims/{claim_id}":    "Get claim details",
            "POST /claims/{id}/review":   "Approve/reject a claim (Admin)",
            "GET  /dashboard/admin":      "Admin dashboard stats",
            "GET  /dashboard/worker":     "Worker personal dashboard",
            "GET  /auth/me":              "Current user profile",
        },
    }


@app.get("/health", tags=["System"])
async def health():
    """Health check — verifies Firebase connectivity."""
    import httpx
    from backend.config.settings import MCP_WEATHER_URL, MCP_TRAFFIC_URL, MCP_SOCIAL_URL

    mcp_status = {}
    async with httpx.AsyncClient(timeout=3) as c:
        for name, url in [
            ("weather", MCP_WEATHER_URL),
            ("traffic", MCP_TRAFFIC_URL),
            ("social",  MCP_SOCIAL_URL),
        ]:
            try:
                r = await c.get(url.replace("/score", "/health"))
                mcp_status[name] = "ok" if r.status_code == 200 else "error"
            except Exception:
                mcp_status[name] = "unreachable"

    # Test Firestore connectivity
    firestore_ok = False
    try:
        from backend.config.firebase import db
        db.collection("_healthcheck").limit(1).get()
        firestore_ok = True
    except Exception:
        pass

    return {
        "status":         "ok",
        "env":            ENV,
        "firestore":      "connected" if firestore_ok else "error",
        "mcp_servers":    mcp_status,
    }
