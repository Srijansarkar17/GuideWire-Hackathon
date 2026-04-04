"""
Drizzle — Pydantic Schemas
============================
Request/response models for all endpoints.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr


# ═══════════════════════════════════════════════════════════════════
# USER / AUTH
# ═══════════════════════════════════════════════════════════════════

class UserBase(BaseModel):
    email: EmailStr
    display_name: str = Field(..., min_length=2, max_length=100)

class UserResponse(BaseModel):
    uid: str
    email: str
    display_name: str
    role: str
    created_at: Optional[str] = None
    is_active: bool = True


class BootstrapSuperAdminRequest(BaseModel):
    """Shared secret + Firebase ID token (Bearer) creates first super_admin profile."""
    secret: str = Field(..., min_length=1)


# ═══════════════════════════════════════════════════════════════════
# WORKER
# ═══════════════════════════════════════════════════════════════════

class WorkerRegisterRequest(BaseModel):
    """Worker self-registers after Firebase Auth signup."""
    display_name: str = Field(..., min_length=2, max_length=100, examples=["Rahul Kumar"])
    phone: str = Field(..., min_length=10, max_length=15, examples=["+919876543210"])
    zone: str = Field(..., min_length=2, max_length=50, examples=["OMR-Chennai"])
    vehicle_type: Literal["bike", "scooter", "bicycle", "auto"] = Field(
        default="bike", examples=["bike"]
    )
    gps_lat: Optional[float] = Field(None, ge=-90, le=90, examples=[13.0827])
    gps_lon: Optional[float] = Field(None, ge=-180, le=180, examples=[80.2707])


class WorkerResponse(BaseModel):
    uid: str
    display_name: str
    email: str
    phone: str
    zone: str
    vehicle_type: str
    role: str = "worker"
    is_active: bool = True
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    created_at: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════
# POLICY
# ═══════════════════════════════════════════════════════════════════

class PolicyCreateRequest(BaseModel):
    """Admin creates a policy for a worker."""
    worker_id: str = Field(..., examples=["abc123uid"])
    zone: str = Field(..., examples=["OMR-Chennai"])
    coverage_type: Literal["weather", "traffic", "social", "comprehensive"] = Field(
        default="comprehensive", examples=["comprehensive"]
    )
    coverage_days: int = Field(default=30, ge=1, le=365, examples=[30])
    sum_insured: float = Field(default=30000.0, ge=1000, le=500000, examples=[30000])


class PolicyResponse(BaseModel):
    policy_id: str
    worker_id: str
    zone: str
    coverage_type: str
    coverage_days: int
    sum_insured: float
    premium: float
    risk_score: float
    status: Literal["active", "expired", "cancelled"] = "active"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    created_at: Optional[str] = None
    created_by: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════
# CLAIM
# ═══════════════════════════════════════════════════════════════════

class ClaimTriggerRequest(BaseModel):
    """Worker or system triggers a claim."""
    policy_id: str = Field(..., examples=["pol_abc123"])
    lat: float = Field(..., ge=-90, le=90, examples=[13.0827])
    lon: float = Field(..., ge=-180, le=180, examples=[80.2707])
    worker_id: Optional[str] = Field(None, examples=["abc123uid"])
    zone: Optional[str] = Field(None, examples=["OMR-Chennai"])
    notes: Optional[str] = Field(None, max_length=500)


class FraudCheckResult(BaseModel):
    gps_valid: bool = True
    multi_server_agreement: bool = True
    fraud_score: float = Field(default=0.0, ge=0.0, le=1.0)
    flags: list[str] = []
    verdict: Literal["clean", "suspicious", "fraudulent"] = "clean"


class ClaimResponse(BaseModel):
    claim_id: str
    policy_id: str
    worker_id: str
    zone: Optional[str] = None
    lat: float
    lon: float

    # MCP signals
    weather_score: float = 0.0
    traffic_score: float = 0.0
    social_score: float = 0.0

    # LLM decision
    claim_triggered: bool = False
    confidence: str = "LOW"
    primary_cause: str = ""
    explanation: str = ""
    recommended_action: str = ""
    reasoning_source: str = ""

    # Payout
    payout_amount: Optional[float] = None
    disruption_intensity: Optional[float] = None

    # Fraud
    fraud_check: Optional[FraudCheckResult] = None

    # Status
    status: Literal["pending", "approved", "rejected", "paid", "flagged"] = "pending"
    reviewed_by: Optional[str] = None
    created_at: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════
# DASHBOARD AGGREGATES
# ═══════════════════════════════════════════════════════════════════

class DashboardStats(BaseModel):
    total_workers: int = 0
    total_policies: int = 0
    active_policies: int = 0
    total_claims: int = 0
    pending_claims: int = 0
    approved_claims: int = 0
    total_payout: float = 0.0
    avg_fraud_score: float = 0.0


class ClaimReviewRequest(BaseModel):
    """Admin reviews a claim."""
    action: Literal["approve", "reject"] = Field(..., examples=["approve"])
    notes: Optional[str] = Field(None, max_length=500)
