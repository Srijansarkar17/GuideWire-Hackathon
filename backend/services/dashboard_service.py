from __future__ import annotations

"""
Drizzle — Dashboard Service
==============================
Aggregation queries for admin and super-admin dashboards.
"""

import logging
from datetime import datetime, timezone

from google.cloud.firestore_v1 import FieldFilter

from backend.config.firebase import db

log = logging.getLogger("drizzle.service.dashboard")


async def get_dashboard_stats() -> dict:
    """
    Aggregate stats across all collections for the admin dashboard.
    """
    # Workers
    workers = list(db.collection("workers").stream())
    total_workers = len(workers)
    active_workers = sum(1 for w in workers if w.to_dict().get("is_active", True))

    # Policies
    policies = list(db.collection("policies").stream())
    total_policies = len(policies)
    active_policies = sum(
        1 for p in policies if p.to_dict().get("status") == "active"
    )
    total_premium_collected = sum(
        p.to_dict().get("premium", 0) for p in policies
    )

    # Claims
    claims = list(db.collection("claims").stream())
    total_claims = len(claims)
    claims_data = [c.to_dict() for c in claims]

    pending_claims = sum(1 for c in claims_data if c.get("status") == "pending")
    approved_claims = sum(1 for c in claims_data if c.get("status") == "approved")
    rejected_claims = sum(1 for c in claims_data if c.get("status") == "rejected")
    flagged_claims = sum(1 for c in claims_data if c.get("status") == "flagged")
    paid_claims = sum(1 for c in claims_data if c.get("status") == "paid")

    total_payout = sum(
        c.get("payout_amount", 0) or 0
        for c in claims_data
        if c.get("status") in ("approved", "paid")
    )

    fraud_scores = [
        c.get("fraud_check", {}).get("fraud_score", 0)
        for c in claims_data
        if c.get("fraud_check")
    ]
    avg_fraud_score = round(
        sum(fraud_scores) / len(fraud_scores), 3
    ) if fraud_scores else 0.0

    # Zone breakdown
    zone_stats = {}
    for p in policies:
        pd = p.to_dict()
        zone = pd.get("zone", "unknown")
        if zone not in zone_stats:
            zone_stats[zone] = {"policies": 0, "premium": 0}
        zone_stats[zone]["policies"] += 1
        zone_stats[zone]["premium"] += pd.get("premium", 0)

    return {
        "overview": {
            "total_workers":          total_workers,
            "active_workers":         active_workers,
            "total_policies":         total_policies,
            "active_policies":        active_policies,
            "total_premium_collected": round(total_premium_collected, 2),
            "total_claims":           total_claims,
            "pending_claims":         pending_claims,
            "approved_claims":        approved_claims,
            "rejected_claims":        rejected_claims,
            "flagged_claims":         flagged_claims,
            "paid_claims":            paid_claims,
            "total_payout":           round(total_payout, 2),
            "avg_fraud_score":        avg_fraud_score,
            "loss_ratio":             round(total_payout / total_premium_collected, 3) if total_premium_collected > 0 else 0,
        },
        "zone_breakdown": zone_stats,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


async def get_worker_dashboard(worker_id: str) -> dict:
    """
    Dashboard data for a specific worker.
    """
    # Worker profile
    worker_doc = db.collection("workers").document(worker_id).get()
    worker = worker_doc.to_dict() if worker_doc.exists else {}

    # Worker's policies
    policies = list(
        db.collection("policies")
        .where(filter=FieldFilter("worker_id", "==", worker_id))
        .stream()
    )
    policies_data = [p.to_dict() for p in policies]

    # Worker's claims
    claims = list(
        db.collection("claims")
        .where(filter=FieldFilter("worker_id", "==", worker_id))
        .stream()
    )
    claims_data = [c.to_dict() for c in claims]

    active_policies = [p for p in policies_data if p.get("status") == "active"]
    total_coverage = sum(p.get("sum_insured", 0) for p in active_policies)
    total_premium = sum(p.get("premium", 0) for p in policies_data)

    return {
        "worker": worker,
        "policies": {
            "total":    len(policies_data),
            "active":   len(active_policies),
            "coverage": round(total_coverage, 2),
            "premium":  round(total_premium, 2),
            "list":     policies_data,
        },
        "claims": {
            "total":    len(claims_data),
            "pending":  sum(1 for c in claims_data if c.get("status") == "pending"),
            "approved": sum(1 for c in claims_data if c.get("status") == "approved"),
            "total_payout": sum(c.get("payout_amount", 0) or 0 for c in claims_data if c.get("status") in ("approved", "paid")),
            "list":     claims_data[:10],  # Last 10 claims
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
