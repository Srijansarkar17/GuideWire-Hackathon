from __future__ import annotations

"""
Drizzle — Claim Service
=========================
Claim triggering, MCP signal collection, fraud detection, payout estimation.
Integrates with Phase 1 MCP servers.
"""

import logging
import uuid
import asyncio
from datetime import datetime, timezone
from typing import Optional

import httpx

from backend.config.firebase import db
from backend.config.settings import (
    MCP_WEATHER_URL, MCP_TRAFFIC_URL, MCP_SOCIAL_URL,
    ZONE_BASE_INCOME,
)

log = logging.getLogger("drizzle.service.claim")


# ═══════════════════════════════════════════════════════════════════
# MCP SIGNAL COLLECTION (reuses Phase 1 servers)
# ═══════════════════════════════════════════════════════════════════

async def _fetch_mcp_server(name: str, url: str, params: dict) -> dict:
    """Fetch risk score from an MCP server."""
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(url, params=params)
            r.raise_for_status()
            data = r.json()
            log.info(f"MCP {name} → level={data.get('risk_level')} score={data.get(f'{name}_risk_score', data.get(f'{name}_disruption_score', 'N/A'))}")
            return {"status": "ok", "data": data}
    except Exception as e:
        log.error(f"MCP {name} server failed: {e}")
        return {"status": "error", "server": name, "error": str(e)}


async def collect_mcp_signals(lat: float, lon: float, worker_id: str = None, zone: str = None) -> dict:
    """Collect risk signals from all 3 MCP servers in parallel."""
    params = {"lat": lat, "lon": lon, "worker_id": worker_id, "zone": zone}

    weather, traffic, social = await asyncio.gather(
        _fetch_mcp_server("weather", MCP_WEATHER_URL, params),
        _fetch_mcp_server("traffic", MCP_TRAFFIC_URL, params),
        _fetch_mcp_server("social",  MCP_SOCIAL_URL,  params),
    )
    return {"weather": weather, "traffic": traffic, "social": social}


def extract_scores(signals: dict) -> tuple[float, float, float]:
    """Extract normalized scores from MCP signal responses."""
    w = (signals["weather"]["data"].get("weather_risk_score", 0.0)
         if signals["weather"]["status"] == "ok" else 0.0)
    t = (signals["traffic"]["data"].get("traffic_risk_score", 0.0)
         if signals["traffic"]["status"] == "ok" else 0.0)
    s = (signals["social"]["data"].get("social_disruption_score", 0.0)
         if signals["social"]["status"] == "ok" else 0.0)
    return float(w), float(t), float(s)


# ═══════════════════════════════════════════════════════════════════
# CLAIM DECISION (formula-based — same as Phase 1 fallback)
# ═══════════════════════════════════════════════════════════════════

def make_claim_decision(w: float, t: float, s: float) -> dict:
    """
    Decision engine — same rule set as Phase 1 LLM system prompt.
    Can be upgraded to call the LLM endpoint in production.
    """
    fused = round(0.35 * w + 0.25 * t + 0.25 * s, 3)

    # Decision rules
    trigger = fused >= 0.6 or w >= 0.7 or t >= 0.7 or s >= 0.7
    if not trigger and fused >= 0.4:
        # Medium signals — trigger if 2+ servers are medium+
        mediums = sum(1 for score in [w, t, s] if score >= 0.3)
        trigger = mediums >= 2

    confidence = "HIGH" if fused >= 0.6 else "MEDIUM" if fused >= 0.3 else "LOW"

    # Primary cause
    scores = {"weather": w, "traffic": t, "social": s}
    primary_cause = max(scores, key=scores.get)
    if max(scores.values()) - min(scores.values()) < 0.15:
        primary_cause = "combined"

    # Explanation
    explanation = (
        f"Fused disruption score: {fused}. "
        f"Weather={w:.2f}, Traffic={t:.2f}, Social={s:.2f}. "
        f"{'Claim triggered due to significant disruption.' if trigger else 'Disruption levels within acceptable range.'}"
    )

    action = "Auto-payout initiated" if trigger and confidence == "HIGH" else \
             "Claim submitted for review" if trigger else "No action needed"

    return {
        "claim_triggered":    trigger,
        "confidence":         confidence,
        "primary_cause":      primary_cause,
        "explanation":        explanation,
        "recommended_action": action,
        "fused_score":        fused,
        "reasoning_source":   "rule_engine",
    }


# ═══════════════════════════════════════════════════════════════════
# PAYOUT ESTIMATION
# ═══════════════════════════════════════════════════════════════════

def _get_base_income(zone: Optional[str]) -> int:
    if not zone:
        return ZONE_BASE_INCOME["default"]
    zone_lower = zone.lower()
    for city, income in ZONE_BASE_INCOME.items():
        if city in zone_lower:
            return income
    return ZONE_BASE_INCOME["default"]


def estimate_payout(
    zone: str, w: float, t: float, s: float,
    confidence: str, sum_insured: float = None,
) -> dict:
    """Deterministic payout estimation — same algorithm as Phase 1."""
    base_income = _get_base_income(zone)
    disruption_intensity = 0.35 * w + 0.25 * t + 0.25 * s

    confidence_multiplier = {"HIGH": 1.0, "MEDIUM": 0.75, "LOW": 0.5}
    multiplier = confidence_multiplier.get(confidence, 0.75)

    income_loss_ratio = disruption_intensity * multiplier
    actual_income = round(base_income * (1 - income_loss_ratio), 2)
    income_loss = round(base_income - actual_income, 2)
    payout_amount = round(income_loss * 0.80, 2)

    # Cap at sum insured if provided
    if sum_insured and payout_amount > sum_insured:
        payout_amount = sum_insured

    return {
        "base_daily_income":    base_income,
        "disruption_intensity": round(disruption_intensity, 3),
        "income_loss":          income_loss,
        "payout_amount":        payout_amount,
        "coverage_percent":     80,
    }


# ═══════════════════════════════════════════════════════════════════
# FRAUD DETECTION
# ═══════════════════════════════════════════════════════════════════

def run_fraud_checks(
    lat: float, lon: float,
    worker_lat: Optional[float], worker_lon: Optional[float],
    w: float, t: float, s: float,
    signals: dict,
) -> dict:
    """
    Multi-layered fraud detection:
    1. GPS validation — is the worker where they say they are?
    2. Multi-server validation — do all servers agree on disruption?
    3. Anomaly flags — unusual patterns
    """
    flags = []
    fraud_score = 0.0

    # ── 1. GPS Validation ─────────────────────────────────────────
    gps_valid = True
    if worker_lat is not None and worker_lon is not None:
        # Haversine approximation — check if claim location is within 25km of registered location
        import math
        R = 6371  # Earth radius in km
        dlat = math.radians(lat - worker_lat)
        dlon = math.radians(lon - worker_lon)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(worker_lat)) *
             math.cos(math.radians(lat)) *
             math.sin(dlon / 2) ** 2)
        distance = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        if distance > 25:
            gps_valid = False
            fraud_score += 0.35
            flags.append(f"GPS mismatch: claim location {distance:.1f}km from registered zone")
        elif distance > 15:
            fraud_score += 0.10
            flags.append(f"GPS warning: {distance:.1f}km from registered zone")

    # ── 2. Multi-server Validation ────────────────────────────────
    server_statuses = [
        signals["weather"]["status"],
        signals["traffic"]["status"],
        signals["social"]["status"],
    ]
    servers_up = sum(1 for s in server_statuses if s == "ok")
    multi_server_valid = servers_up >= 2

    if servers_up < 2:
        fraud_score += 0.20
        flags.append(f"Only {servers_up}/3 MCP servers responded — insufficient validation")

    # Check if scores wildly contradict each other
    scores = [w, t, s]
    score_range = max(scores) - min(scores)
    if score_range > 0.7 and max(scores) > 0.6:
        fraud_score += 0.15
        flags.append(f"Score divergence: range={score_range:.2f} — potential localized manipulation")

    # ── 3. Anomaly detection ──────────────────────────────────────
    # If all scores are exactly 0 but a claim is triggered
    if all(score == 0.0 for score in [w, t, s]):
        fraud_score += 0.40
        flags.append("All MCP scores are 0.0 — suspicious claim trigger")

    # Cap fraud score
    fraud_score = round(min(1.0, fraud_score), 3)

    # Verdict
    if fraud_score >= 0.5:
        verdict = "fraudulent"
    elif fraud_score >= 0.2:
        verdict = "suspicious"
    else:
        verdict = "clean"

    return {
        "gps_valid":              gps_valid,
        "multi_server_agreement": multi_server_valid,
        "fraud_score":            fraud_score,
        "flags":                  flags,
        "verdict":                verdict,
    }


# ═══════════════════════════════════════════════════════════════════
# CLAIM LIFECYCLE
# ═══════════════════════════════════════════════════════════════════

async def trigger_claim(data: dict, triggered_by: str) -> dict:
    """
    Full claim pipeline:
    1. Validate policy exists and is active
    2. Collect MCP signals
    3. Make claim decision
    4. Run fraud checks
    5. Estimate payout
    6. Store in Firestore
    """
    now = datetime.now(timezone.utc)
    claim_id = f"clm_{uuid.uuid4().hex[:12]}"

    # ── 1. Validate policy ────────────────────────────────────────
    policy_doc = db.collection("policies").document(data["policy_id"]).get()
    if not policy_doc.exists:
        raise ValueError(f"Policy {data['policy_id']} not found")

    policy = policy_doc.to_dict()
    if policy["status"] != "active":
        raise ValueError(f"Policy {data['policy_id']} is {policy['status']}, not active")

    worker_id = data.get("worker_id") or policy["worker_id"]
    zone = data.get("zone") or policy["zone"]

    # ── 2. Get worker GPS for fraud check ─────────────────────────
    worker_doc = db.collection("workers").document(worker_id).get()
    worker_lat, worker_lon = None, None
    if worker_doc.exists:
        w = worker_doc.to_dict()
        worker_lat = w.get("gps_lat")
        worker_lon = w.get("gps_lon")

    # ── 3. Collect MCP signals ────────────────────────────────────
    signals = await collect_mcp_signals(
        lat=data["lat"], lon=data["lon"],
        worker_id=worker_id, zone=zone,
    )
    w_score, t_score, s_score = extract_scores(signals)

    # ── 4. Make claim decision ────────────────────────────────────
    decision = make_claim_decision(w_score, t_score, s_score)

    # ── 5. Fraud detection ────────────────────────────────────────
    fraud = run_fraud_checks(
        lat=data["lat"], lon=data["lon"],
        worker_lat=worker_lat, worker_lon=worker_lon,
        w=w_score, t=t_score, s=s_score,
        signals=signals,
    )

    # ── 6. Payout estimation ─────────────────────────────────────
    payout = {}
    if decision["claim_triggered"]:
        payout = estimate_payout(
            zone, w_score, t_score, s_score,
            decision["confidence"],
            sum_insured=policy.get("sum_insured"),
        )

    # ── 7. Determine status ───────────────────────────────────────
    if fraud["verdict"] == "fraudulent":
        status = "flagged"
    elif decision["claim_triggered"] and decision["confidence"] == "HIGH" and fraud["verdict"] == "clean":
        status = "approved"  # Auto-approve high-confidence clean claims
    elif decision["claim_triggered"]:
        status = "pending"   # Needs admin review
    else:
        status = "rejected"

    # ── 8. Build and store claim document ─────────────────────────
    claim_doc = {
        "claim_id":           claim_id,
        "policy_id":          data["policy_id"],
        "worker_id":          worker_id,
        "zone":               zone,
        "lat":                data["lat"],
        "lon":                data["lon"],
        "notes":              data.get("notes", ""),

        # MCP scores
        "weather_score":      w_score,
        "traffic_score":      t_score,
        "social_score":       s_score,

        # Decision
        "claim_triggered":    decision["claim_triggered"],
        "confidence":         decision["confidence"],
        "primary_cause":      decision["primary_cause"],
        "explanation":        decision["explanation"],
        "recommended_action": decision["recommended_action"],
        "reasoning_source":   decision["reasoning_source"],
        "fused_score":        decision["fused_score"],

        # Payout
        "payout_amount":        payout.get("payout_amount"),
        "disruption_intensity": payout.get("disruption_intensity"),
        "base_daily_income":    payout.get("base_daily_income"),

        # Fraud
        "fraud_check":        fraud,

        # Status
        "status":             status,
        "triggered_by":       triggered_by,
        "reviewed_by":        None,
        "review_notes":       None,
        "created_at":         now.isoformat(),
        "updated_at":         now.isoformat(),
    }

    db.collection("claims").document(claim_id).set(claim_doc)
    log.info(
        f"Claim {claim_id}: triggered={decision['claim_triggered']} "
        f"status={status} fraud={fraud['verdict']} "
        f"payout=₹{payout.get('payout_amount', 0)}"
    )

    # ── Update worker stats ───────────────────────────────────────
    if decision["claim_triggered"] and worker_doc.exists:
        from google.cloud.firestore import Increment
        db.collection("workers").document(worker_id).update({
            "total_claims": Increment(1),
            "total_payouts": Increment(payout.get("payout_amount", 0)),
            "updated_at": now.isoformat(),
        })

    return claim_doc


async def get_claim(claim_id: str) -> dict | None:
    """Fetch a single claim."""
    doc = db.collection("claims").document(claim_id).get()
    return doc.to_dict() if doc.exists else None


async def get_claims_by_worker(worker_id: str) -> list[dict]:
    """Fetch all claims for a worker."""
    from google.cloud.firestore_v1 import FieldFilter
    docs = (
        db.collection("claims")
        .where(filter=FieldFilter("worker_id", "==", worker_id))
        .order_by("created_at", direction="DESCENDING")
        .stream()
    )
    return [doc.to_dict() for doc in docs]


async def list_claims(
    status: str | None = None,
    limit: int = 50,
) -> list[dict]:
    """List claims with optional status filter."""
    from google.cloud.firestore_v1 import FieldFilter
    query = db.collection("claims")
    if status:
        query = query.where(filter=FieldFilter("status", "==", status))
    query = query.limit(limit)
    return [doc.to_dict() for doc in query.stream()]


async def review_claim(claim_id: str, action: str, reviewer_uid: str, notes: str = None) -> dict:
    """
    Admin reviews a claim — approve or reject.
    """
    ref = db.collection("claims").document(claim_id)
    doc = ref.get()
    if not doc.exists:
        raise ValueError(f"Claim {claim_id} not found")

    claim = doc.to_dict()
    if claim["status"] not in ("pending", "flagged"):
        raise ValueError(f"Claim {claim_id} is already {claim['status']}")

    new_status = "approved" if action == "approve" else "rejected"
    now = datetime.now(timezone.utc).isoformat()

    ref.update({
        "status":       new_status,
        "reviewed_by":  reviewer_uid,
        "review_notes": notes,
        "updated_at":   now,
    })

    log.info(f"Claim {claim_id} → {new_status} by {reviewer_uid}")
    return ref.get().to_dict()
