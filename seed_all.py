"""
Drizzle — Complete Demo Data Seeder
=====================================
Seeds Firestore with:
  • 2 admin users (admin + super_admin)
  • 5 workers across different zones
  • 7 policies (mix of active/expired)
  • 8 claims (approved/pending/flagged/rejected)

Run:  python3 seed_all.py
"""

import sys, os, uuid
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.config.firebase import db
from backend.services.policy_service import calculate_premium

now = datetime.now(timezone.utc)
counts = {"users": 0, "workers": 0, "policies": 0, "claims": 0}


def ts(hours_ago=0):
    return (now - timedelta(hours=hours_ago)).isoformat()


print("🌧️  Drizzle — Seeding Complete Demo Data\n")
print("=" * 55)

# ═══════════════════════════════════════════════════════════
# 1. ADMIN & SUPER ADMIN USERS
# ═══════════════════════════════════════════════════════════
print("\n📋 ADMIN USERS")

admins = [
    {
        "uid": "admin_001",
        "email": "admin@drizzle.io",
        "display_name": "Drizzle Admin",
        "role": "admin",
    },
    {
        "uid": "super_admin_001",
        "email": "superadmin@drizzle.io",
        "display_name": "Drizzle Super Admin",
        "role": "super_admin",
    },
]

for a in admins:
    doc = {
        **a,
        "is_active": True,
        "created_at": ts(72),
        "updated_at": ts(),
    }
    db.collection("users").document(a["uid"]).set(doc)
    counts["users"] += 1
    print(f"  ✅ {a['role']}: {a['display_name']} ({a['email']})")


# ═══════════════════════════════════════════════════════════
# 2. WORKERS
# ═══════════════════════════════════════════════════════════
print("\n👷 WORKERS")

workers = [
    {
        "uid": "worker_rahul",
        "email": "rahul.kumar@demo.drizzle.io",
        "display_name": "Rahul Kumar",
        "phone": "+919876543210",
        "zone": "OMR-Chennai",
        "vehicle_type": "bike",
        "gps_lat": 12.9600,
        "gps_lon": 80.2494,
    },
    {
        "uid": "worker_priya",
        "email": "priya.sharma@demo.drizzle.io",
        "display_name": "Priya Sharma",
        "phone": "+919876543211",
        "zone": "Andheri-Mumbai",
        "vehicle_type": "scooter",
        "gps_lat": 19.1136,
        "gps_lon": 72.8697,
    },
    {
        "uid": "worker_amit",
        "email": "amit.patel@demo.drizzle.io",
        "display_name": "Amit Patel",
        "phone": "+919876543212",
        "zone": "Connaught-Delhi",
        "vehicle_type": "bike",
        "gps_lat": 28.6315,
        "gps_lon": 77.2167,
    },
    {
        "uid": "worker_sneha",
        "email": "sneha.reddy@demo.drizzle.io",
        "display_name": "Sneha Reddy",
        "phone": "+919876543213",
        "zone": "Hitech-Hyderabad",
        "vehicle_type": "auto",
        "gps_lat": 17.4435,
        "gps_lon": 78.3772,
    },
    {
        "uid": "worker_vikram",
        "email": "vikram.singh@demo.drizzle.io",
        "display_name": "Vikram Singh",
        "phone": "+919876543214",
        "zone": "Koramangala-Bangalore",
        "vehicle_type": "bicycle",
        "gps_lat": 12.9352,
        "gps_lon": 77.6245,
    },
]

for w in workers:
    # User profile
    user_doc = {
        "uid": w["uid"],
        "email": w["email"],
        "display_name": w["display_name"],
        "role": "worker",
        "is_active": True,
        "created_at": ts(48),
        "updated_at": ts(),
    }
    db.collection("users").document(w["uid"]).set(user_doc)
    counts["users"] += 1

    # Worker profile
    worker_doc = {
        **w,
        "role": "worker",
        "is_active": True,
        "total_claims": 0,
        "total_payouts": 0.0,
        "created_at": ts(48),
        "updated_at": ts(),
    }
    db.collection("workers").document(w["uid"]).set(worker_doc)
    counts["workers"] += 1
    print(f"  ✅ {w['display_name']} — {w['zone']} ({w['vehicle_type']})")


# ═══════════════════════════════════════════════════════════
# 3. POLICIES
# ═══════════════════════════════════════════════════════════
print("\n📄 POLICIES")

policy_configs = [
    # (worker_idx, coverage_type, days, sum_insured, status, hours_ago)
    (0, "comprehensive", 30, 30000, "active",  24),
    (1, "comprehensive", 60, 50000, "active",  36),
    (2, "weather",       30, 25000, "active",  12),
    (3, "traffic",       90, 40000, "active",  48),
    (4, "comprehensive", 30, 35000, "active",  20),
    (0, "weather",       30, 20000, "expired", 720),  # expired (30 days ago)
    (1, "social",        30, 15000, "cancelled", 480),
]

policies = []  # track for claim references

for w_idx, cov_type, days, insured, p_status, hours_ago in policy_configs:
    w = workers[w_idx]
    policy_id = f"pol_{uuid.uuid4().hex[:12]}"
    created = now - timedelta(hours=hours_ago)

    premium_info = calculate_premium(
        zone=w["zone"],
        coverage_type=cov_type,
        coverage_days=days,
        sum_insured=insured,
        vehicle_type=w["vehicle_type"],
    )

    p_doc = {
        "policy_id":      policy_id,
        "worker_id":      w["uid"],
        "zone":           w["zone"],
        "coverage_type":  cov_type,
        "coverage_days":  days,
        "sum_insured":    insured,
        "premium":        premium_info["premium"],
        "risk_score":     premium_info["risk_score"],
        "daily_rate":     premium_info["daily_rate"],
        "zone_multiplier": premium_info["zone_multiplier"],
        "status":         p_status,
        "start_date":     created.isoformat(),
        "end_date":       (created + timedelta(days=days)).isoformat(),
        "created_by":     "admin_001",
        "created_at":     created.isoformat(),
        "updated_at":     ts(),
    }
    db.collection("policies").document(policy_id).set(p_doc)
    policies.append(p_doc)
    counts["policies"] += 1
    status_emoji = {"active": "🟢", "expired": "🔴", "cancelled": "⚪"}.get(p_status, "⚪")
    print(f"  ✅ {policy_id} — {w['display_name']}, {cov_type}/{days}d, ₹{insured:,} → premium ₹{premium_info['premium']:,} {status_emoji} {p_status}")


# ═══════════════════════════════════════════════════════════
# 4. CLAIMS
# ═══════════════════════════════════════════════════════════
print("\n⚡ CLAIMS")

claim_scenarios = [
    # (worker_idx, policy_idx, w, t, s, status, payout, hours_ago, fraud_verdict)
    # Rahul — heavy rain in Chennai, auto-approved
    (0, 0, 0.85, 0.50, 0.35, "approved", 520.0,  6, "clean"),
    # Priya — traffic jam in Mumbai, pending review
    (1, 1, 0.30, 0.78, 0.40, "pending",  480.0,  3, "clean"),
    # Amit — protest in Delhi, approved
    (2, 2, 0.25, 0.40, 0.82, "approved", 410.0,  8, "clean"),
    # Sneha — traffic in Hyderabad, approved
    (3, 3, 0.20, 0.72, 0.30, "approved", 350.0, 12, "clean"),
    # Vikram — weather in Bangalore, flagged (GPS suspicious)
    (4, 4, 0.70, 0.45, 0.25, "flagged",  390.0,  2, "suspicious"),
    # Rahul — second claim, pending
    (0, 0, 0.60, 0.55, 0.45, "pending",  440.0,  1, "clean"),
    # Priya — low disruption, rejected
    (1, 1, 0.15, 0.20, 0.10, "rejected", 0.0,   10, "clean"),
    # Amit — fake GPS from far away, flagged as fraudulent
    (2, 2, 0.80, 0.60, 0.50, "flagged",  0.0,    4, "fraudulent"),
]

total_worker_claims = {}
total_worker_payouts = {}

for w_idx, p_idx, ws, ts_score, ss, c_status, payout, hours_ago, fraud_v in claim_scenarios:
    w = workers[w_idx]
    p = policies[p_idx]
    claim_id = f"clm_{uuid.uuid4().hex[:12]}"
    created = now - timedelta(hours=hours_ago)

    fused = round(0.35 * ws + 0.25 * ts_score + 0.25 * ss, 3)
    triggered = c_status not in ("rejected",)
    confidence = "HIGH" if fused >= 0.6 else "MEDIUM" if fused >= 0.3 else "LOW"

    # Determine primary cause
    scores = {"weather": ws, "traffic": ts_score, "social": ss}
    primary_cause = max(scores, key=scores.get)

    # Fraud check
    fraud_score = {"clean": 0.05, "suspicious": 0.35, "fraudulent": 0.65}[fraud_v]
    fraud_flags = []
    if fraud_v == "suspicious":
        fraud_flags = ["GPS warning: 18.3km from registered zone"]
    elif fraud_v == "fraudulent":
        fraud_flags = ["GPS mismatch: claim location 1200km from registered zone",
                       "Score divergence: range=0.30 — potential manipulation"]

    c_doc = {
        "claim_id":           claim_id,
        "policy_id":          p["policy_id"],
        "worker_id":          w["uid"],
        "zone":               w["zone"],
        "lat":                w["gps_lat"] + (0.002 if fraud_v == "clean" else 5.0),
        "lon":                w["gps_lon"] + (0.001 if fraud_v == "clean" else 3.0),
        "notes":              f"Demo claim — {primary_cause} disruption",

        "weather_score":      ws,
        "traffic_score":      ts_score,
        "social_score":       ss,

        "claim_triggered":    triggered,
        "confidence":         confidence,
        "primary_cause":      primary_cause,
        "explanation":        f"Fused disruption score: {fused}. Weather={ws:.2f}, Traffic={ts_score:.2f}, Social={ss:.2f}. {'Claim triggered.' if triggered else 'Below threshold.'}",
        "recommended_action": "Auto-payout initiated" if c_status == "approved" and confidence == "HIGH" else "Claim submitted for review" if triggered else "No action needed",
        "reasoning_source":   "rule_engine",
        "fused_score":        fused,

        "payout_amount":      payout if triggered else None,
        "disruption_intensity": fused if triggered else None,
        "base_daily_income":  1000,

        "fraud_check": {
            "gps_valid":              fraud_v == "clean",
            "multi_server_agreement": True,
            "fraud_score":            fraud_score,
            "flags":                  fraud_flags,
            "verdict":                fraud_v,
        },

        "status":        c_status,
        "triggered_by":  w["uid"],
        "reviewed_by":   "admin_001" if c_status in ("approved", "rejected") else None,
        "review_notes":  f"Demo: {c_status}" if c_status in ("approved", "rejected") else None,
        "created_at":    created.isoformat(),
        "updated_at":    ts(),
    }

    db.collection("claims").document(claim_id).set(c_doc)
    counts["claims"] += 1

    # Track worker stats
    if triggered:
        total_worker_claims[w["uid"]] = total_worker_claims.get(w["uid"], 0) + 1
        total_worker_payouts[w["uid"]] = total_worker_payouts.get(w["uid"], 0) + payout

    status_emoji = {
        "approved": "🟢", "pending": "🟡", "flagged": "🔴", "rejected": "⚫"
    }.get(c_status, "⚪")
    print(f"  ✅ {claim_id} — {w['display_name']}, {primary_cause}, ₹{payout:,.0f} {status_emoji} {c_status} (fraud: {fraud_v})")


# ═══════════════════════════════════════════════════════════
# 5. UPDATE WORKER STATS
# ═══════════════════════════════════════════════════════════
print("\n📊 UPDATING WORKER STATS")

for w in workers:
    claims_count = total_worker_claims.get(w["uid"], 0)
    payouts_total = total_worker_payouts.get(w["uid"], 0)
    if claims_count > 0:
        db.collection("workers").document(w["uid"]).update({
            "total_claims": claims_count,
            "total_payouts": payouts_total,
            "updated_at": ts(),
        })
        print(f"  ✅ {w['display_name']}: {claims_count} claims, ₹{payouts_total:,.0f} payouts")


# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print(f"\n{'=' * 55}")
print(f"🎉 Demo data seeded successfully!\n")
print(f"  👤 Users:    {counts['users']}  (2 admins + 5 workers)")
print(f"  👷 Workers:  {counts['workers']}")
print(f"  📄 Policies: {counts['policies']}  (5 active, 1 expired, 1 cancelled)")
print(f"  ⚡ Claims:   {counts['claims']}  (3 approved, 2 pending, 2 flagged, 1 rejected)")
print()
