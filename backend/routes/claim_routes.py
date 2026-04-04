"""
Drizzle — Claim Routes
========================
Endpoints for claim triggering, retrieval, and review.

IMPORTANT: Route order matters in FastAPI.
Static paths (/trigger, /my-claims, /, /worker/{id})
MUST be registered BEFORE parameterized /{claim_id}.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from backend.middleware.auth import get_current_user, require_role
from backend.config.settings import Roles
from backend.models.schemas import (
    ClaimTriggerRequest, ClaimResponse, ClaimReviewRequest,
)
from backend.services import claim_service

log = logging.getLogger("drizzle.routes.claims")

router = APIRouter(prefix="/claims", tags=["Claims"])


# ── Trigger a new claim ────────────────────────────────────────────────────────

@router.post("/trigger", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def trigger_claim(
    req: ClaimTriggerRequest,
    user: dict = Depends(get_current_user),
):
    """
    Trigger a new insurance claim.
    - Workers can trigger claims on their own policies only.
    - Admins/Super Admins can trigger on behalf of any worker.

    Pipeline: policy validation → MCP signals → claim decision → fraud detection → payout estimation → Firestore save
    """
    # Workers can only trigger claims for their own policies
    if user["role"] == Roles.WORKER:
        from backend.services import policy_service
        policy = await policy_service.get_policy(req.policy_id)
        if not policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Policy {req.policy_id} not found",
            )
        if policy["worker_id"] != user["uid"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Workers can only trigger claims on their own policies",
            )

    try:
        claim = await claim_service.trigger_claim(
            data=req.model_dump(),
            triggered_by=user["uid"],
        )
        return ClaimResponse(**claim)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ── Worker: own claims ─────────────────────────────────────────────────────────

@router.get("/my-claims")
async def get_my_claims(
    user: dict = Depends(require_role(Roles.WORKER)),
):
    """
    [WORKER] Get all claims for the authenticated worker.
    """
    claims = await claim_service.get_claims_by_worker(user["uid"])
    return {"claims": claims, "count": len(claims)}


# ── Admin: list all claims ─────────────────────────────────────────────────────

@router.get("/")
async def list_all_claims(
    claim_status: str = None,
    limit: int = 50,
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] List all claims with optional status filter.
    """
    claims = await claim_service.list_claims(status=claim_status, limit=limit)
    return {"claims": claims, "count": len(claims)}


# ── Claims by worker_id ────────────────────────────────────────────────────────

@router.get("/worker/{worker_id}")
async def get_worker_claims(
    worker_id: str,
    user: dict = Depends(get_current_user),
):
    """
    Get all claims for a specific worker.
    Workers can only view their own; admins can view anyone's.
    """
    if user["role"] == Roles.WORKER and user["uid"] != worker_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers can only view their own claims",
        )

    claims = await claim_service.get_claims_by_worker(worker_id)
    return {"claims": claims, "count": len(claims)}


# ── Admin: review a claim ──────────────────────────────────────────────────────

@router.post("/{claim_id}/review")
async def review_claim(
    claim_id: str,
    req: ClaimReviewRequest,
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] Review a pending/flagged claim — approve or reject.
    """
    try:
        claim = await claim_service.review_claim(
            claim_id=claim_id,
            action=req.action,
            reviewer_uid=user["uid"],
            notes=req.notes,
        )
        return {"message": f"Claim {claim_id} {req.action}d successfully", "claim": claim}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ── Single claim by ID — MUST be last (parameterized wildcard) ─────────────────

@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(
    claim_id: str,
    user: dict = Depends(get_current_user),
):
    """
    Get a single claim by ID.
    Workers can only view their own claims.
    """
    claim = await claim_service.get_claim(claim_id)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim {claim_id} not found",
        )

    # RBAC: workers can only see their own claims
    if user["role"] == Roles.WORKER and claim["worker_id"] != user["uid"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return ClaimResponse(**claim)
