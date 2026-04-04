"""
Drizzle — Dashboard Routes
=============================
Aggregated data endpoints for multi-role dashboards.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException

from backend.middleware.auth import get_current_user, require_role
from backend.config.settings import Roles
from backend.services import dashboard_service

log = logging.getLogger("drizzle.routes.dashboard")

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/admin")
async def admin_dashboard(
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] Full admin dashboard with aggregate stats.
    Includes:
    - Total workers, policies, claims
    - Pending/approved/rejected claims
    - Total payout and loss ratio
    - Zone breakdown
    """
    stats = await dashboard_service.get_dashboard_stats()
    return stats


@router.get("/worker")
async def worker_dashboard(
    user: dict = Depends(require_role(Roles.WORKER)),
):
    """
    [WORKER] Personal dashboard for the authenticated worker.
    Includes:
    - Worker profile
    - Active policies and coverage
    - Recent claims and payouts
    """
    dashboard = await dashboard_service.get_worker_dashboard(user["uid"])
    return dashboard


@router.get("/worker/{worker_id}")
async def worker_dashboard_by_id(
    worker_id: str,
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] View any worker's dashboard.
    """
    dashboard = await dashboard_service.get_worker_dashboard(worker_id)
    if not dashboard.get("worker"):
        raise HTTPException(
            status_code=404,
            detail=f"Worker {worker_id} not found",
        )
    return dashboard


@router.get("/super-admin")
async def super_admin_dashboard(
    user: dict = Depends(require_role(Roles.SUPER_ADMIN)),
):
    """
    [SUPER_ADMIN] Extended dashboard with system-level insights.
    Includes everything from admin dashboard plus:
    - User role distribution
    - System health metrics
    """
    from backend.config.firebase import db

    stats = await dashboard_service.get_dashboard_stats()

    # Add role distribution
    users = list(db.collection("users").stream())
    role_dist = {}
    for u in users:
        role = u.to_dict().get("role", "unknown")
        role_dist[role] = role_dist.get(role, 0) + 1

    stats["role_distribution"] = role_dist
    stats["total_users"] = len(users)

    return stats
