"""
Drizzle — Policy Routes
==========================
Endpoints for insurance policy management.

IMPORTANT: Route order matters in FastAPI.
Static paths (/my-policies, /calculate-premium, /detail/{id})
MUST be registered BEFORE the parameterized /{worker_id} route.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from backend.middleware.auth import get_current_user, require_role
from backend.config.settings import Roles
from backend.models.schemas import PolicyCreateRequest, PolicyResponse
from backend.services import policy_service

log = logging.getLogger("drizzle.routes.policies")

router = APIRouter(prefix="/policies", tags=["Policies"])


# ── Admin / Super-Admin: create policy ────────────────────────────────────────

@router.post("/create", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    req: PolicyCreateRequest,
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] Create a new insurance policy for a worker.
    Premium is calculated automatically using rule-based ML engine.
    """
    from backend.services import worker_service
    worker = await worker_service.get_worker(req.worker_id)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker {req.worker_id} not found",
        )

    policy = await policy_service.create_policy(
        data=req.model_dump(),
        created_by=user["uid"],
    )
    return PolicyResponse(**policy)


# ── Admin / Super-Admin: list all policies ────────────────────────────────────

@router.get("/")
async def list_all_policies(
    policy_status: str = None,
    zone: str = None,
    limit: int = 50,
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] List all policies with optional status/zone filter.
    """
    policies = await policy_service.list_policies(
        status=policy_status, zone=zone, limit=limit,
    )
    return {"policies": policies, "count": len(policies)}


# ── Admin / Super-Admin: premium preview ──────────────────────────────────────

@router.post("/calculate-premium")
async def calculate_premium_preview(
    req: PolicyCreateRequest,
    user: dict = Depends(require_role(Roles.ADMIN, Roles.SUPER_ADMIN)),
):
    """
    [ADMIN, SUPER_ADMIN] Preview premium calculation without creating a policy.
    Useful for quoting before committing.
    """
    premium_info = policy_service.calculate_premium(
        zone=req.zone,
        coverage_type=req.coverage_type,
        coverage_days=req.coverage_days,
        sum_insured=req.sum_insured,
    )
    return {
        "worker_id":     req.worker_id,
        "zone":          req.zone,
        "coverage_type": req.coverage_type,
        "coverage_days": req.coverage_days,
        "sum_insured":   req.sum_insured,
        **premium_info,
    }


# ── Worker: own policies ───────────────────────────────────────────────────────

@router.get("/my-policies")
async def get_my_policies(
    user: dict = Depends(require_role(Roles.WORKER)),
):
    """
    [WORKER] Get all policies for the authenticated worker.
    """
    policies = await policy_service.get_policies_by_worker(user["uid"])
    return {"policies": policies, "count": len(policies)}


# ── Single policy by ID ────────────────────────────────────────────────────────

@router.get("/detail/{policy_id}", response_model=PolicyResponse)
async def get_policy_detail(
    policy_id: str,
    user: dict = Depends(get_current_user),
):
    """
    Get a single policy by policy_id.
    Workers can only view their own policies.
    """
    policy = await policy_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found",
        )

    # RBAC: workers can only see their own
    if user["role"] == Roles.WORKER and policy["worker_id"] != user["uid"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return PolicyResponse(**policy)


# ── Policies by worker_id — MUST be last (parameterized wildcard) ─────────────

@router.get("/{worker_id}")
async def get_worker_policies(
    worker_id: str,
    user: dict = Depends(get_current_user),
):
    """
    Get policies for a specific worker.
    Workers can only view their own; admins can view anyone's.
    """
    if user["role"] == Roles.WORKER and user["uid"] != worker_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers can only view their own policies",
        )

    policies = await policy_service.get_policies_by_worker(worker_id)
    return {"policies": policies, "count": len(policies)}
