"""
Drizzle — Authentication & RBAC Middleware
===========================================
Provides FastAPI dependencies for:
  1. Token verification  (get_firebase_user)  — only verifies Firebase token
  2. Full auth            (get_current_user)  — token + Firestore profile
  3. Role enforcement    (require_role factory)
"""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.config.firebase import verify_id_token, db
from backend.config.settings import Roles

log = logging.getLogger("drizzle.auth")

# ── Bearer token extractor ────────────────────────────────────────
_bearer_scheme = HTTPBearer(auto_error=False)


def _extract_and_verify_token(
    credentials: Optional[HTTPAuthorizationCredentials],
) -> dict:
    """Shared helper: extract Bearer token and verify it with Firebase."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        decoded = verify_id_token(credentials.credentials)
        return decoded
    except Exception as e:
        log.warning(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_firebase_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> dict:
    """
    Lightweight dependency — verifies Firebase ID token ONLY.
    Does NOT require a Firestore profile. Used for /workers/register.

    Returns: {"uid": str, "email": str, "name": str, ...}
    """
    decoded = _extract_and_verify_token(credentials)
    uid = decoded["uid"]
    email = decoded.get("email", "")
    return {"uid": uid, "email": email, "name": decoded.get("name", "")}


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> dict:
    """
    FastAPI dependency — verifies Firebase ID token AND fetches
    the user's Firestore profile (including role).

    Returns dict with uid, email, role, display_name, and all Firestore fields.
    Raises 401 if token missing/invalid, 403 if no Firestore profile found.
    """
    decoded = _extract_and_verify_token(credentials)
    uid = decoded["uid"]
    email = decoded.get("email", "")

    # ── Fetch role from Firestore users collection ─────────────────
    user_ref = db.collection("users").document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        log.warning(f"User {uid} ({email}) has no Firestore profile")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User profile not found. Please call POST /workers/register first.",
        )

    user_data = user_doc.to_dict()
    user_data["uid"] = uid
    user_data["email"] = email

    # Validate role exists
    role = user_data.get("role", "")
    if role not in Roles.ALL:
        log.warning(f"User {uid} has invalid role: {role!r}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid role '{role}' assigned to user.",
        )

    # Attach to request state for downstream access
    request.state.user = user_data
    return user_data


def require_role(*allowed_roles: str):
    """
    Factory that returns a FastAPI dependency restricting access
    to users with one of the specified roles.

    Usage:
        @router.post("/admin-only", dependencies=[Depends(require_role("admin", "super_admin"))])
        async def admin_endpoint(): ...

    Or inject the user dict directly:
        async def my_endpoint(user=Depends(require_role("admin"))):
            ...
    """
    async def _role_checker(
        user: dict = Depends(get_current_user),
    ) -> dict:
        if user["role"] not in allowed_roles:
            log.warning(
                f"Access denied: user={user['uid']} role={user['role']} "
                f"requires one of {allowed_roles}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {', '.join(allowed_roles)}",
            )
        return user

    return _role_checker
