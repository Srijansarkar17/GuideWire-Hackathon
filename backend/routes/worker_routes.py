"""
Drizzle — Worker Routes
=========================
Endpoints for worker registration and management.

Route order matters in FastAPI — static paths must come BEFORE parameterized ones.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from backend.middleware.auth import get_firebase_user, get_current_user, require_role
from backend.config.settings import Roles
from backend.models.schemas import WorkerRegisterRequest, WorkerResponse
from backend.services import worker_service

log = logging.getLogger("drizzle.routes.workers")

router = APIRouter(prefix="/workers", tags=["Workers"])


@router.post("/register", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
async def register_worker(
    req: WorkerRegisterRequest,
    firebase_user: dict = Depends(get_firebase_user),   # ← lightweight: no Firestore profile needed yet
):
    """
    Register a new worker.

    The user authenticates via Firebase Auth on the frontend and sends their
    ID token here. This creates their Firestore `users` + `workers` profiles
    with role=worker.

    Note: Uses `get_firebase_user` (not `get_current_user`) because the user
    has no Firestore profile yet — that's exactly what we're creating here.
    """
    from backend.config.firebase import db

    uid = firebase_user["uid"]

    # Check if already registered
    existing_worker = db.collection("workers").document(uid).get()
    existing_user   = db.collection("users").document(uid).get()

    if existing_worker.exists or existing_user.exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Worker already registered. Use /workers/me to view your profile.",
        )

    worker = await worker_service.register_worker(
        uid=uid,
        email=firebase_user.get("email", ""),
        data=req.model_dump(),
    )
    return WorkerResponse(**worker)


@router.get("/me", response_model=WorkerResponse)
async def get_my_profile(
    user: dict = Depends(require_role(Roles.WORKER)),
):
    """
    [WORKER] Get own worker profile.
    """
    worker = await worker_service.get_worker(user["uid"])
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Worker profile not found",
        )
    return WorkerResponse(**worker)


@router.get("/")
async def list_workers(
    zone: str = None,
    limit: int = 50,
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] List all workers with optional zone filter.
    """
    workers = await worker_service.list_workers(zone=zone, limit=limit)
    return {"workers": workers, "count": len(workers)}


@router.get("/{worker_id}", response_model=WorkerResponse)
async def get_worker(
    worker_id: str,
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] Get any worker's profile by UID.
    """
    worker = await worker_service.get_worker(worker_id)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker {worker_id} not found",
        )
    return WorkerResponse(**worker)
