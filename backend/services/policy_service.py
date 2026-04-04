from __future__ import annotations

"""
Drizzle — Policy Service
===========================
Policy creation, premium calculation, and lifecycle management.
"""

import logging
import uuid
from datetime import datetime, timezone, timedelta

from google.cloud.firestore_v1 import FieldFilter

from backend.config.firebase import db
from backend.config.settings import ZONE_BASE_INCOME

log = logging.getLogger("drizzle.service.policy")


# ═══════════════════════════════════════════════════════════════════
# PREMIUM CALCULATION (rule-based ML)
# ═══════════════════════════════════════════════════════════════════

def _get_zone_risk_multiplier(zone: str) -> float:
    """
    Zone-specific risk multiplier based on historical disruption data.
    Higher multiplier = higher premium.
    """
    zone_lower = zone.lower()
    risk_map = {
        "mumbai":    1.35,   # Monsoon flooding, high traffic
        "chennai":   1.30,   # Cyclone-prone, waterlogging
        "kolkata":   1.25,   # Monsoon + frequent bandhs
        "delhi":     1.20,   # AQI + traffic + protests
        "bangalore": 1.15,   # Traffic congestion
        "hyderabad": 1.10,   # Moderate risk
        "pune":      1.05,   # Lower risk
        "noida":     1.15,   # Traffic + AQI
        "jaipur":    1.00,   # Baseline
    }
    for city, multiplier in risk_map.items():
        if city in zone_lower:
            return multiplier
    return 1.10  # default


def _get_vehicle_factor(vehicle_type: str) -> float:
    """Vehicle-type risk factor — bikes are more exposed to weather."""
    return {
        "bicycle": 1.30,
        "bike":    1.20,
        "scooter": 1.15,
        "auto":    1.00,
    }.get(vehicle_type, 1.15)


def calculate_premium(
    zone: str,
    coverage_type: str,
    coverage_days: int,
    sum_insured: float,
    vehicle_type: str = "bike",
    worker_claim_history: int = 0,
) -> dict:
    """
    Rule-based premium calculation.

    Base rate = 2.5% of sum_insured per 30 days
    Adjusted by:
      - Zone risk multiplier
      - Coverage type factor
      - Vehicle type factor
      - Claim history surcharge
      - Duration discount for longer policies
    """
    # Base rate: 2.5% per month
    base_rate = 0.025

    # Coverage type factor
    coverage_factor = {
        "weather":       0.70,
        "traffic":       0.60,
        "social":        0.50,
        "comprehensive": 1.00,
    }.get(coverage_type, 1.00)

    zone_multiplier = _get_zone_risk_multiplier(zone)
    vehicle_factor = _get_vehicle_factor(vehicle_type)

    # Claim history surcharge: +5% per past claim, max +25%
    history_surcharge = 1.0 + min(0.25, worker_claim_history * 0.05)

    # Duration discount: longer policies get a discount
    if coverage_days >= 180:
        duration_discount = 0.85
    elif coverage_days >= 90:
        duration_discount = 0.92
    elif coverage_days >= 60:
        duration_discount = 0.96
    else:
        duration_discount = 1.00

    # Calculate
    monthly_premium = sum_insured * base_rate * coverage_factor
    monthly_premium *= zone_multiplier * vehicle_factor * history_surcharge

    total_premium = monthly_premium * (coverage_days / 30.0) * duration_discount
    total_premium = round(total_premium, 2)

    # Risk score (0-1) — reflects combined risk profile
    risk_score = round(
        min(1.0, (zone_multiplier - 0.9) * 2 + (vehicle_factor - 0.9) * 1.5) / 2,
        3,
    )

    return {
        "premium":          total_premium,
        "risk_score":       risk_score,
        "zone_multiplier":  zone_multiplier,
        "vehicle_factor":   vehicle_factor,
        "coverage_factor":  coverage_factor,
        "daily_rate":       round(total_premium / coverage_days, 2),
    }


# ═══════════════════════════════════════════════════════════════════
# FIRESTORE OPERATIONS
# ═══════════════════════════════════════════════════════════════════

async def create_policy(data: dict, created_by: str) -> dict:
    """
    Create a new insurance policy.

    Args:
        data: PolicyCreateRequest dict
        created_by: UID of the admin creating the policy
    """
    now = datetime.now(timezone.utc)
    policy_id = f"pol_{uuid.uuid4().hex[:12]}"

    # Fetch worker for vehicle type
    worker_doc = db.collection("workers").document(data["worker_id"]).get()
    vehicle_type = "bike"
    worker_claims = 0
    if worker_doc.exists:
        w = worker_doc.to_dict()
        vehicle_type = w.get("vehicle_type", "bike")
        worker_claims = w.get("total_claims", 0)

    # Calculate premium
    premium_info = calculate_premium(
        zone=data["zone"],
        coverage_type=data["coverage_type"],
        coverage_days=data["coverage_days"],
        sum_insured=data["sum_insured"],
        vehicle_type=vehicle_type,
        worker_claim_history=worker_claims,
    )

    end_date = now + timedelta(days=data["coverage_days"])

    policy_doc = {
        "policy_id":      policy_id,
        "worker_id":      data["worker_id"],
        "zone":           data["zone"],
        "coverage_type":  data["coverage_type"],
        "coverage_days":  data["coverage_days"],
        "sum_insured":    data["sum_insured"],
        "premium":        premium_info["premium"],
        "risk_score":     premium_info["risk_score"],
        "daily_rate":     premium_info["daily_rate"],
        "zone_multiplier": premium_info["zone_multiplier"],
        "status":         "active",
        "start_date":     now.isoformat(),
        "end_date":       end_date.isoformat(),
        "created_by":     created_by,
        "created_at":     now.isoformat(),
        "updated_at":     now.isoformat(),
    }

    db.collection("policies").document(policy_id).set(policy_doc)
    log.info(
        f"Policy created: {policy_id} for worker={data['worker_id']} "
        f"premium=₹{premium_info['premium']}"
    )
    return policy_doc


async def get_policy(policy_id: str) -> dict | None:
    """Fetch a single policy."""
    doc = db.collection("policies").document(policy_id).get()
    return doc.to_dict() if doc.exists else None


async def get_policies_by_worker(worker_id: str) -> list[dict]:
    """Fetch all policies for a specific worker."""
    docs = (
        db.collection("policies")
        .where(filter=FieldFilter("worker_id", "==", worker_id))
        .order_by("created_at", direction="DESCENDING")
        .stream()
    )
    return [doc.to_dict() for doc in docs]


async def list_policies(
    status: str | None = None,
    zone: str | None = None,
    limit: int = 50,
) -> list[dict]:
    """List policies with optional filters."""
    query = db.collection("policies")
    if status:
        query = query.where(filter=FieldFilter("status", "==", status))
    if zone:
        query = query.where(filter=FieldFilter("zone", "==", zone))
    query = query.limit(limit)
    return [doc.to_dict() for doc in query.stream()]
