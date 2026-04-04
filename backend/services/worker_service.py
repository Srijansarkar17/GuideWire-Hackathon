from __future__ import annotations

"""
Drizzle — Worker Service
==========================
Handles worker registration & retrieval from Firestore.
"""

import logging
from datetime import datetime, timezone

from google.cloud.firestore_v1 import FieldFilter

from backend.config.firebase import db
from backend.config.settings import Roles

log = logging.getLogger("drizzle.service.worker")


async def register_worker(uid: str, email: str, data: dict) -> dict:
    """
    Register a new worker in both `users` and `workers` collections.
    Called after the user has signed up via Firebase Auth on the frontend.

    Args:
        uid:   Firebase Auth UID
        email: User email from the verified token
        data:  WorkerRegisterRequest dict
    """
    now = datetime.now(timezone.utc).isoformat()

    # ── Create user profile ───────────────────────────────────────
    user_doc = {
        "uid":          uid,
        "email":        email,
        "display_name": data["display_name"],
        "role":         Roles.WORKER,
        "is_active":    True,
        "created_at":   now,
        "updated_at":   now,
    }
    db.collection("users").document(uid).set(user_doc)
    log.info(f"Created user profile: {uid} ({email})")

    # ── Create worker profile ─────────────────────────────────────
    worker_doc = {
        "uid":           uid,
        "email":         email,
        "display_name":  data["display_name"],
        "phone":         data["phone"],
        "zone":          data["zone"],
        "vehicle_type":  data.get("vehicle_type", "bike"),
        "gps_lat":       data.get("gps_lat"),
        "gps_lon":       data.get("gps_lon"),
        "role":          Roles.WORKER,
        "is_active":     True,
        "total_claims":  0,
        "total_payouts": 0.0,
        "created_at":    now,
        "updated_at":    now,
    }
    db.collection("workers").document(uid).set(worker_doc)
    log.info(f"Created worker profile: {uid} zone={data['zone']}")

    return worker_doc


async def get_worker(worker_id: str) -> dict | None:
    """Fetch a single worker by UID."""
    doc = db.collection("workers").document(worker_id).get()
    if doc.exists:
        return doc.to_dict()
    return None


async def list_workers(zone: str | None = None, limit: int = 50) -> list[dict]:
    """List workers, optionally filtered by zone."""
    query = db.collection("workers")
    if zone:
        query = query.where(filter=FieldFilter("zone", "==", zone))
    query = query.limit(limit)

    docs = query.stream()
    return [doc.to_dict() for doc in docs]


async def update_worker(worker_id: str, updates: dict) -> dict | None:
    """Partial update on a worker document."""
    ref = db.collection("workers").document(worker_id)
    doc = ref.get()
    if not doc.exists:
        return None

    updates["updated_at"] = datetime.now(timezone.utc).isoformat()
    ref.update(updates)
    log.info(f"Updated worker {worker_id}: {list(updates.keys())}")
    return ref.get().to_dict()
