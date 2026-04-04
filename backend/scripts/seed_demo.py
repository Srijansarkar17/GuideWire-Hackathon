"""
Drizzle — Seed Demo Data
===========================
Populates Firestore with demo workers, policies, and claims
for testing and dashboard verification.

Usage:
    python -m backend.scripts.seed_demo
"""

import sys
import os
import uuid
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def seed_demo_data():
    from backend.config.firebase import db
    from backend.services.policy_service import calculate_premium

    now = datetime.now(timezone.utc)
    print("🌧️  Seeding Drizzle demo data...\n")

    # ── Demo Workers ──────────────────────────────────────────────
    workers = [
        {
            "uid": "demo_worker_001",
            "email": "rahul@demo.drizzle.io",
            "display_name": "Rahul Kumar",
            "phone": "+919876543210",
            "zone": "OMR-Chennai",
            "vehicle_type": "bike",
            "gps_lat": 12.9600,
            "gps_lon": 80.2494,
        },
        {
            "uid": "demo_worker_002",
            "email": "priya@demo.drizzle.io",
            "display_name": "Priya Sharma",
            "phone": "+919876543211",
            "zone": "Andheri-Mumbai",
            "vehicle_type": "scooter",
            "gps_lat": 19.1136,
            "gps_lon": 72.8697,
        },
        {
            "uid": "demo_worker_003",
            "email": "amit@demo.drizzle.io",
            "display_name": "Amit Patel",
            "phone": "+919876543212",
            "zone": "Connaught-Delhi",
            "vehicle_type": "bike",
            "gps_lat": 28.6315,
            "gps_lon": 77.2167,
        },
    ]

    for w in workers:
        w_doc = {
            **w,
            "role": "worker",
            "is_active": True,
            "total_claims": 0,
            "total_payouts": 0.0,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        db.collection("users").document(w["uid"]).set({
            "uid": w["uid"],
            "email": w["email"],
            "display_name": w["display_name"],
            "role": "worker",
            "is_active": True,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        })
        db.collection("workers").document(w["uid"]).set(w_doc)
        print(f"  ✅ Worker: {w['display_name']} ({w['zone']})")

    # ── Demo Policies ─────────────────────────────────────────────
    policies = []
    for w in workers:
        policy_id = f"pol_{uuid.uuid4().hex[:12]}"
        premium_info = calculate_premium(
            zone=w["zone"],
            coverage_type="comprehensive",
            coverage_days=30,
            sum_insured=30000,
            vehicle_type=w["vehicle_type"],
        )
        p_doc = {
            "policy_id": policy_id,
            "worker_id": w["uid"],
            "zone": w["zone"],
            "coverage_type": "comprehensive",
            "coverage_days": 30,
            "sum_insured": 30000,
            "premium": premium_info["premium"],
            "risk_score": premium_info["risk_score"],
            "daily_rate": premium_info["daily_rate"],
            "zone_multiplier": premium_info["zone_multiplier"],
            "status": "active",
            "start_date": now.isoformat(),
            "end_date": (now + timedelta(days=30)).isoformat(),
            "created_by": "demo_admin",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        db.collection("policies").document(policy_id).set(p_doc)
        policies.append(p_doc)
        print(f"  ✅ Policy: {policy_id} → ₹{premium_info['premium']}")

    # ── Demo Claims ───────────────────────────────────────────────
    claim_scenarios = [
        {
            "worker_idx": 0,
            "w_score": 0.75, "t_score": 0.45, "s_score": 0.30,
            "status": "approved", "confidence": "HIGH",
            "cause": "weather", "payout": 560.0,
        },
        {
            "worker_idx": 1,
            "w_score": 0.40, "t_score": 0.65, "s_score": 0.50,
            "status": "pending", "confidence": "MEDIUM",
            "cause": "traffic", "payout": 420.0,
        },
        {
            "worker_idx": 2,
            "w_score": 0.20, "t_score": 0.15, "s_score": 0.80,
            "status": "flagged", "confidence": "MEDIUM",
            "cause": "social", "payout": 390.0,
        },
    ]

    for cs in claim_scenarios:
        w = workers[cs["worker_idx"]]
        p = policies[cs["worker_idx"]]
        claim_id = f"clm_{uuid.uuid4().hex[:12]}"

        c_doc = {
            "claim_id": claim_id,
            "policy_id": p["policy_id"],
            "worker_id": w["uid"],
            "zone": w["zone"],
            "lat": w["gps_lat"],
            "lon": w["gps_lon"],
            "weather_score": cs["w_score"],
            "traffic_score": cs["t_score"],
            "social_score": cs["s_score"],
            "claim_triggered": True,
            "confidence": cs["confidence"],
            "primary_cause": cs["cause"],
            "explanation": f"Demo claim: {cs['cause']} disruption detected",
            "recommended_action": "Claim submitted for review",
            "reasoning_source": "demo_seed",
            "fused_score": round(0.35 * cs["w_score"] + 0.25 * cs["t_score"] + 0.25 * cs["s_score"], 3),
            "payout_amount": cs["payout"],
            "disruption_intensity": round(0.35 * cs["w_score"] + 0.25 * cs["t_score"] + 0.25 * cs["s_score"], 3),
            "fraud_check": {
                "gps_valid": True,
                "multi_server_agreement": True,
                "fraud_score": 0.05 if cs["status"] != "flagged" else 0.55,
                "flags": [] if cs["status"] != "flagged" else ["Demo: flagged for review"],
                "verdict": "clean" if cs["status"] != "flagged" else "suspicious",
            },
            "status": cs["status"],
            "triggered_by": w["uid"],
            "reviewed_by": None,
            "created_at": (now - timedelta(hours=2)).isoformat(),
            "updated_at": now.isoformat(),
        }
        db.collection("claims").document(claim_id).set(c_doc)
        print(f"  ✅ Claim: {claim_id} ({cs['status']}) → ₹{cs['payout']}")

    print(f"\n🎉 Demo data seeded successfully!")
    print(f"   Workers:  {len(workers)}")
    print(f"   Policies: {len(policies)}")
    print(f"   Claims:   {len(claim_scenarios)}")


if __name__ == "__main__":
    seed_demo_data()
