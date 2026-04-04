"""
Drizzle — Auth Routes
=======================
Minimal auth endpoints for the backend.
Frontend handles Firebase Auth (Google, Email, etc.)
Backend just verifies tokens and manages Firestore user profiles.
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from google.cloud.firestore_v1 import FieldFilter

from backend.middleware.auth import get_current_user, get_firebase_user, require_role
from backend.config.firebase import db
from backend.config.settings import DRIZZLE_BOOTSTRAP_SECRET, Roles
from backend.models.schemas import BootstrapSuperAdminRequest, UserResponse

log = logging.getLogger("drizzle.routes.auth")

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/bootstrap-super-admin", response_model=UserResponse)
async def bootstrap_super_admin(
    body: BootstrapSuperAdminRequest,
    firebase_user: dict = Depends(get_firebase_user),
):
    """
    First-time setup only: creates the **first** `super_admin` Firestore profile for the
    currently signed-in Firebase user (Bearer token). Requires `DRIZZLE_BOOTSTRAP_SECRET`
    in server `.env` to match `body.secret`. Fails if any `super_admin` already exists.

    For additional admins, use `python -m backend.scripts.seed_admin --role admin` or
    `POST /auth/promote` (super_admin only).
    """
    if not (DRIZZLE_BOOTSTRAP_SECRET or "").strip():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Bootstrap is not configured. Set DRIZZLE_BOOTSTRAP_SECRET in the backend "
                ".env and restart the server, or create the user with seed_admin.py."
            ),
        )
    if body.secret != DRIZZLE_BOOTSTRAP_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid bootstrap secret.",
        )

    existing_sa = list(
        db.collection("users")
        .where(filter=FieldFilter("role", "==", Roles.SUPER_ADMIN))
        .limit(1)
        .stream()
    )
    if existing_sa:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "A super admin already exists. Ask them to grant you access, or run: "
                "python -m backend.scripts.seed_admin --uid <UID> --email <E> --role admin"
            ),
        )

    uid = firebase_user["uid"]
    ref = db.collection("users").document(uid)
    if ref.get().exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A Firestore profile already exists for this account. Sign in normally.",
        )

    email = firebase_user.get("email", "") or ""
    display_name = (firebase_user.get("name") or "").strip() or (
        email.split("@")[0] if email else "Admin"
    )
    now = datetime.now(timezone.utc).isoformat()
    user_doc = {
        "uid": uid,
        "email": email,
        "display_name": display_name,
        "role": Roles.SUPER_ADMIN,
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }
    ref.set(user_doc)
    log.info("Bootstrap: created first super_admin uid=%s email=%s", uid, email)

    return UserResponse(
        uid=uid,
        email=email,
        display_name=display_name,
        role=Roles.SUPER_ADMIN,
        created_at=now,
        is_active=True,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user: dict = Depends(get_current_user)):
    """
    Returns the currently authenticated user's profile.
    Used by frontend to verify login state and get role info.
    """
    return UserResponse(
        uid=user["uid"],
        email=user.get("email", ""),
        display_name=user.get("display_name", ""),
        role=user.get("role", ""),
        created_at=user.get("created_at"),
        is_active=user.get("is_active", True),
    )


@router.post("/promote", response_model=UserResponse)
async def promote_user(
    target_uid: str,
    new_role: str,
    user: dict = Depends(require_role(Roles.SUPER_ADMIN)),
):
    """
    [SUPER_ADMIN only] Promote/change a user's role.
    """
    if new_role not in Roles.ALL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {Roles.ALL}",
        )

    user_ref = db.collection("users").document(target_uid)
    user_doc = user_ref.get()
    if not user_doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {target_uid} not found",
        )

    from datetime import datetime, timezone
    user_ref.update({
        "role": new_role,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })

    updated = user_ref.get().to_dict()
    log.info(f"User {target_uid} promoted to {new_role} by {user['uid']}")

    return UserResponse(
        uid=target_uid,
        email=updated.get("email", ""),
        display_name=updated.get("display_name", ""),
        role=updated.get("role", ""),
        created_at=updated.get("created_at"),
        is_active=updated.get("is_active", True),
    )


@router.get("/users")
async def list_users(
    role: str = None,
    limit: int = 50,
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] List all users, optionally filtered by role.
    """
    from google.cloud.firestore_v1 import FieldFilter

    query = db.collection("users")
    if role:
        query = query.where(filter=FieldFilter("role", "==", role))
    query = query.limit(limit)

    users = [doc.to_dict() for doc in query.stream()]
    return {"users": users, "count": len(users)}
