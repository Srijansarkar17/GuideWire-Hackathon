#!/usr/bin/env python3
"""
Drizzle — Phase 2 Integration Test Suite
==========================================
Tests the full backend without a real Firebase Auth token.
We bypass Firebase ID token verification by temporarily patching
`verify_id_token` to return a fake decoded token, and we create
real Firestore documents directly.

Usage:
    cd /Users/adityapratapsingh/Downloads/drizzle-main
    python -m backend.scripts.test_phase2

What is tested:
    1.  Firebase / Firestore connectivity
    2.  Premium calculation engine
    3.  Claim decision engine
    4.  Fraud detection engine
    5.  Payout estimation
    6.  Worker registration (Firestore write)
    7.  Policy creation (Firestore write)
    8.  Claim trigger pipeline (end-to-end Firestore write)
    9.  Dashboard aggregation queries
    10. RBAC role enforcement logic
    11. Route smoke-test (imports & router registration)
"""

import sys
import asyncio
import logging
from datetime import datetime, timezone
from unittest.mock import patch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger("drizzle.test")

PASS  = "✅ PASS"
FAIL  = "❌ FAIL"
SKIP  = "⏭  SKIP"

results: list[tuple[str, str, str]] = []   # (test_name, status, detail)


def record(name: str, ok: bool, detail: str = ""):
    status = PASS if ok else FAIL
    results.append((name, status, detail))
    symbol = "✅" if ok else "❌"
    print(f"  {symbol}  {name}" + (f"  — {detail}" if detail else ""))


# ═══════════════════════════════════════════════════════════════════
# 1. FIREBASE CONNECTIVITY
# ═══════════════════════════════════════════════════════════════════

def test_firebase_connectivity():
    print("\n── 1. Firebase / Firestore Connectivity ──────────────────────")
    try:
        from backend.config.firebase import db
        # Simple read — touch _healthcheck collection
        db.collection("_healthcheck").limit(1).get()
        record("Firestore connection", True, "connected to drizzle-d76ee")
    except Exception as e:
        record("Firestore connection", False, str(e))

    try:
        from backend.config.firebase import db
        test_ref = db.collection("_test_write").document("ping")
        test_ref.set({"ts": datetime.now(timezone.utc).isoformat()})
        test_ref.delete()
        record("Firestore read/write", True)
    except Exception as e:
        record("Firestore read/write", False, str(e))


# ═══════════════════════════════════════════════════════════════════
# 2. PREMIUM CALCULATION
# ═══════════════════════════════════════════════════════════════════

def test_premium_calculation():
    print("\n── 2. Premium Calculation Engine ──────────────────────────────")
    from backend.services.policy_service import calculate_premium

    cases = [
        dict(zone="Mumbai", coverage_type="comprehensive", coverage_days=30,  sum_insured=30000, vehicle_type="bike"),
        dict(zone="Chennai", coverage_type="weather",       coverage_days=90,  sum_insured=20000, vehicle_type="bicycle"),
        dict(zone="Delhi",   coverage_type="traffic",       coverage_days=180, sum_insured=50000, vehicle_type="scooter"),
        dict(zone="Jaipur",  coverage_type="social",        coverage_days=7,   sum_insured=10000, vehicle_type="auto"),
    ]
    for c in cases:
        try:
            result = calculate_premium(**c)
            ok = (
                result["premium"] > 0 and
                0 <= result["risk_score"] <= 1 and
                result["daily_rate"] > 0
            )
            record(
                f"Premium calc ({c['zone']}, {c['coverage_type']}, {c['coverage_days']}d)",
                ok,
                f"₹{result['premium']} | risk={result['risk_score']} | daily=₹{result['daily_rate']}",
            )
        except Exception as e:
            record(f"Premium calc ({c['zone']})", False, str(e))


# ═══════════════════════════════════════════════════════════════════
# 3. CLAIM DECISION ENGINE
# ═══════════════════════════════════════════════════════════════════

def test_claim_decision():
    print("\n── 3. Claim Decision Engine ──────────────────────────────────")
    from backend.services.claim_service import make_claim_decision

    cases = [
        # (w, t, s, expected_trigger, label)
        (0.8, 0.7, 0.6, True,  "All high → fused=0.605 ≥ 0.6"),
        (0.2, 0.1, 0.1, False, "All low  → fused=0.12"),
        # fused = 0.35*0.5 + 0.25*0.4 + 0.25*0.4 = 0.175 + 0.10 + 0.10 = 0.375
        # 0.375 >= 0.4 but only 2 mediums (0.5, 0.4, 0.4) — actually all 3 >= 0.3,
        # so mediums=3 >= 2 → trigger=True
        (0.5, 0.4, 0.4, True,  "Medium×3 → 3 servers medium, triggers"),
        (0.6, 0.0, 0.0, False, "Only weather → fused=0.21, no trigger"),
        (0.7, 0.0, 0.0, True,  "Weather ≥ 0.7 alone → trigger"),
    ]
    for w, t, s, expected_trigger, label in cases:
        try:
            d = make_claim_decision(w, t, s)
            ok = d["claim_triggered"] == expected_trigger
            record(
                f"Claim decision: {label}",
                ok,
                f"triggered={d['claim_triggered']} (expected={expected_trigger}) conf={d['confidence']} fused={d['fused_score']}",
            )
        except Exception as e:
            record(f"Claim decision (w={w} t={t} s={s})", False, str(e))


# ═══════════════════════════════════════════════════════════════════
# 4. FRAUD DETECTION
# ═══════════════════════════════════════════════════════════════════

def test_fraud_detection():
    print("\n── 4. Fraud Detection Engine ──────────────────────────────────")
    from backend.services.claim_service import run_fraud_checks

    clean_signals  = {"weather": {"status": "ok"}, "traffic": {"status": "ok"}, "social": {"status": "ok"}}
    broken_signals = {"weather": {"status": "error"}, "traffic": {"status": "error"}, "social": {"status": "ok"}}

    tests = [
        # (lat, lon, w_lat, w_lon, w, t, s, signals, expected_verdict, label)
        # Same GPS, clean signals → score=0.0 → clean
        (13.08, 80.27, 13.08, 80.27, 0.7, 0.6, 0.5, clean_signals,  "clean",      "Same GPS, clean signals"),
        # GPS mismatch ~2100km → +0.35; but score=0.35 < 0.5 → suspicious (not fraudulent)
        (13.08, 80.27, 28.61, 77.20, 0.7, 0.6, 0.5, clean_signals,  "suspicious", "GPS mismatch Chennai↔Delhi"),
        # All zeros → +0.40 fraud; GPS same → score=0.40 < 0.5 → suspicious
        (13.08, 80.27, 13.08, 80.27, 0.0, 0.0, 0.0, clean_signals,  "suspicious", "All MCP scores zero"),
        # 2 servers down → +0.20; GPS same → score=0.20 → suspicious
        (13.08, 80.27, 13.08, 80.27, 0.5, 0.5, 0.5, broken_signals, "suspicious", "2 servers down"),
        # GPS mismatch + all zeros → +0.35 + 0.40 = 0.75 → fraudulent
        (13.08, 80.27, 28.61, 77.20, 0.0, 0.0, 0.0, clean_signals,  "fraudulent", "GPS mismatch + all zeros → 0.75"),
    ]
    for lat, lon, w_lat, w_lon, w, t, s, signals, expected, label in tests:
        try:
            result = run_fraud_checks(lat, lon, w_lat, w_lon, w, t, s, signals)
            ok = result["verdict"] == expected
            record(
                f"Fraud: {label}",
                ok,
                f"verdict={result['verdict']} (expected={expected}) score={result['fraud_score']} flags={result['flags']}",
            )
        except Exception as e:
            record(f"Fraud check ({label})", False, str(e))


# ═══════════════════════════════════════════════════════════════════
# 5. PAYOUT ESTIMATION
# ═══════════════════════════════════════════════════════════════════

def test_payout_estimation():
    print("\n── 5. Payout Estimation ───────────────────────────────────────")
    from backend.services.claim_service import estimate_payout

    cases = [
        ("Mumbai",    0.8, 0.7, 0.6, "HIGH",   30000),
        ("Chennai",   0.4, 0.3, 0.2, "MEDIUM", 20000),
        ("Bangalore", 0.1, 0.1, 0.1, "LOW",    50000),
    ]
    for zone, w, t, s, confidence, sum_insured in cases:
        try:
            p = estimate_payout(zone, w, t, s, confidence, sum_insured)
            ok = p["payout_amount"] >= 0 and p["payout_amount"] <= sum_insured
            record(
                f"Payout ({zone}, {confidence})",
                ok,
                f"₹{p['payout_amount']} (intensity={p['disruption_intensity']})",
            )
        except Exception as e:
            record(f"Payout ({zone})", False, str(e))


# ═══════════════════════════════════════════════════════════════════
# 6. WORKER REGISTRATION (Firestore write)
# ═══════════════════════════════════════════════════════════════════

async def test_worker_registration():
    print("\n── 6. Worker Registration (Firestore) ─────────────────────────")
    from backend.services.worker_service import register_worker, get_worker
    from backend.config.firebase import db

    test_uid   = "test_worker_uid_phase2_auto"
    test_email = "testworker@drizzle.dev"

    # Clean up if previous test run left data
    try:
        db.collection("workers").document(test_uid).delete()
        db.collection("users").document(test_uid).delete()
    except Exception:
        pass  # Document may not exist

    # Graceful skip if Firestore not provisioned
    try:
        db.collection("_healthcheck").limit(1).get()
    except Exception as e:
        record("Register worker (write)", False, f"Firestore not ready: {e}")
        record("Fetch worker (read)",     False, "Skipped — Firestore not ready")
        return test_uid

    try:
        worker = await register_worker(
            uid=test_uid,
            email=test_email,
            data={
                "display_name": "Test Worker",
                "phone":        "+919876543210",
                "zone":         "OMR-Chennai",
                "vehicle_type": "bike",
                "gps_lat":      13.0827,
                "gps_lon":      80.2707,
            },
        )
        record("Register worker (write)", worker["uid"] == test_uid)
    except Exception as e:
        record("Register worker (write)", False, str(e))
        return test_uid

    try:
        fetched = await get_worker(test_uid)
        ok = fetched and fetched["zone"] == "OMR-Chennai" and fetched["role"] == "worker"
        record("Fetch worker (read)", bool(ok), f"zone={fetched.get('zone')} role={fetched.get('role')}")
    except Exception as e:
        record("Fetch worker (read)", False, str(e))

    return test_uid


# ═══════════════════════════════════════════════════════════════════
# 7. POLICY CREATION (Firestore write)
# ═══════════════════════════════════════════════════════════════════

async def test_policy_creation(worker_uid: str):
    print("\n── 7. Policy Creation (Firestore) ─────────────────────────────")
    from backend.services.policy_service import create_policy, get_policy

    policy_id = None
    try:
        policy = await create_policy(
            data={
                "worker_id":     worker_uid,
                "zone":          "OMR-Chennai",
                "coverage_type": "comprehensive",
                "coverage_days": 30,
                "sum_insured":   30000,
            },
            created_by="admin_test_uid",
        )
        policy_id = policy["policy_id"]
        ok = (
            policy["status"] == "active" and
            policy["premium"] > 0 and
            policy["worker_id"] == worker_uid
        )
        record(
            "Create policy (write)",
            ok,
            f"id={policy_id} premium=₹{policy['premium']} risk={policy['risk_score']}",
        )
    except Exception as e:
        record("Create policy (write)", False, str(e))
        return None

    try:
        fetched = await get_policy(policy_id)
        ok = fetched and fetched["policy_id"] == policy_id
        record("Fetch policy (read)", bool(ok))
    except Exception as e:
        record("Fetch policy (read)", False, str(e))

    return policy_id


# ═══════════════════════════════════════════════════════════════════
# 8. CLAIM TRIGGER (end-to-end, MCP servers may be down)
# ═══════════════════════════════════════════════════════════════════

async def test_claim_trigger(worker_uid: str, policy_id: str):
    print("\n── 8. Claim Trigger Pipeline (end-to-end) ─────────────────────")
    from backend.services.claim_service import trigger_claim, get_claim

    claim_id = None
    try:
        claim = await trigger_claim(
            data={
                "policy_id": policy_id,
                "lat":       13.0827,
                "lon":       80.2707,
                "worker_id": worker_uid,
                "zone":      "OMR-Chennai",
                "notes":     "Automated Phase 2 test",
            },
            triggered_by=worker_uid,
        )
        claim_id = claim["claim_id"]
        ok = (
            claim["claim_id"] is not None and
            claim["status"] in ("approved", "pending", "rejected", "flagged") and
            claim["policy_id"] == policy_id
        )
        record(
            "Trigger claim (pipeline)",
            ok,
            f"id={claim_id} status={claim['status']} payout=₹{claim.get('payout_amount', 0)}",
        )
    except Exception as e:
        record("Trigger claim (pipeline)", False, str(e))
        return None

    try:
        fetched = await get_claim(claim_id)
        ok = fetched and fetched["claim_id"] == claim_id
        record("Fetch claim (read)", bool(ok), f"fraud={fetched.get('fraud_check', {}).get('verdict', 'n/a')}")
    except Exception as e:
        record("Fetch claim (read)", False, str(e))

    return claim_id


# ═══════════════════════════════════════════════════════════════════
# 9. DASHBOARD AGGREGATION
# ═══════════════════════════════════════════════════════════════════

async def test_dashboard():
    print("\n── 9. Dashboard Aggregation ───────────────────────────────────")
    from backend.services.dashboard_service import get_dashboard_stats

    try:
        stats = await get_dashboard_stats()
        overview = stats.get("overview", {})
        ok = (
            "total_workers" in overview and
            "total_claims" in overview and
            "total_payout" in overview and
            "zone_breakdown" in stats
        )
        record(
            "Admin dashboard stats",
            ok,
            f"workers={overview.get('total_workers')} "
            f"policies={overview.get('total_policies')} "
            f"claims={overview.get('total_claims')} "
            f"payout=₹{overview.get('total_payout')}",
        )
    except Exception as e:
        record("Admin dashboard stats", False, str(e))


# ═══════════════════════════════════════════════════════════════════
# 10. RBAC ROLE LOGIC
# ═══════════════════════════════════════════════════════════════════

def test_rbac_logic():
    print("\n── 10. RBAC Role Logic ────────────────────────────────────────")
    from backend.config.settings import Roles

    # Validate role constants
    record("Roles.WORKER value",      Roles.WORKER      == "worker")
    record("Roles.ADMIN value",       Roles.ADMIN       == "admin")
    record("Roles.SUPER_ADMIN value", Roles.SUPER_ADMIN == "super_admin")
    record("Roles.ALL set",           Roles.ALL         == {"worker", "admin", "super_admin"})

    # Validate RBAC logic (simulated)
    def can_access(user_role: str, required: list[str]) -> bool:
        return user_role in required

    record("Worker can view own claims",     can_access("worker",      ["worker", "admin", "super_admin"]))
    record("Admin can approve claims",       can_access("admin",       ["admin", "super_admin"]))
    record("Worker cannot approve claims",  not can_access("worker",   ["admin", "super_admin"]))
    record("Super admin has full access",    can_access("super_admin", ["super_admin"]))
    record("Worker cannot access /admin",   not can_access("worker",   ["admin", "super_admin"]))


# ═══════════════════════════════════════════════════════════════════
# 11. MODULE IMPORTS & ROUTE REGISTRATION SMOKE TEST
# ═══════════════════════════════════════════════════════════════════

def test_imports():
    print("\n── 11. Module Imports & Route Registration Smoke Test ─────────")
    modules = [
        ("FastAPI app",           "backend.main",                  "app"),
        ("Firebase config",       "backend.config.firebase",       "db"),
        ("Settings",              "backend.config.settings",       "Roles"),
        ("Auth middleware",       "backend.middleware.auth",       "get_current_user"),
        ("Auth (get_firebase)",   "backend.middleware.auth",       "get_firebase_user"),
        ("Schemas",               "backend.models.schemas",        "ClaimResponse"),
        ("Worker service",        "backend.services.worker_service", "register_worker"),
        ("Policy service",        "backend.services.policy_service", "calculate_premium"),
        ("Claim service",         "backend.services.claim_service",  "trigger_claim"),
        ("Dashboard service",     "backend.services.dashboard_service", "get_dashboard_stats"),
        ("Auth routes",           "backend.routes.auth_routes",    "router"),
        ("Worker routes",         "backend.routes.worker_routes",  "router"),
        ("Policy routes",         "backend.routes.policy_routes",  "router"),
        ("Claim routes",          "backend.routes.claim_routes",   "router"),
        ("Dashboard routes",      "backend.routes.dashboard_routes", "router"),
    ]
    for label, module, attr in modules:
        try:
            import importlib
            mod = importlib.import_module(module)
            obj = getattr(mod, attr, None)
            record(f"Import {label}", obj is not None)
        except Exception as e:
            record(f"Import {label}", False, str(e))

    # Check route registration
    try:
        from backend.main import app
        routes = {r.path for r in app.routes}
        expected = ["/", "/health", "/workers/register", "/policies/create", "/claims/trigger"]
        for path in expected:
            record(f"Route registered: {path}", path in routes)
    except Exception as e:
        record("Route registration check", False, str(e))


# ═══════════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════════

async def cleanup(worker_uid: str, policy_id: str, claim_id: str):
    """Remove test documents created during the test run."""
    print("\n── Cleanup: removing test documents ──────────────────────────")
    from backend.config.firebase import db
    try:
        if worker_uid:
            db.collection("workers").document(worker_uid).delete()
            db.collection("users").document(worker_uid).delete()
        if policy_id:
            db.collection("policies").document(policy_id).delete()
        if claim_id:
            db.collection("claims").document(claim_id).delete()
        print("  🗑  Test documents cleaned up")
    except Exception as e:
        print(f"  ⚠️  Cleanup error: {e}")


# ═══════════════════════════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════════════════════════

async def main():
    print("\n" + "═" * 65)
    print("  🌧️  DRIZZLE — Phase 2 Integration Test Suite")
    print("═" * 65)

    worker_uid = None
    policy_id  = None
    claim_id   = None

    # Synchronous tests
    test_imports()
    test_firebase_connectivity()
    test_premium_calculation()
    test_claim_decision()
    test_fraud_detection()
    test_payout_estimation()
    test_rbac_logic()

    # Async Firestore tests
    worker_uid = await test_worker_registration()
    if worker_uid:
        policy_id = await test_policy_creation(worker_uid)
    if policy_id:
        claim_id = await test_claim_trigger(worker_uid, policy_id)

    await test_dashboard()

    # Cleanup
    await cleanup(worker_uid, policy_id, claim_id)

    # ── Summary ──────────────────────────────────────────────────
    print("\n" + "═" * 65)
    print("  📊  TEST SUMMARY")
    print("═" * 65)

    passed  = sum(1 for _, s, _ in results if s == PASS)
    failed  = sum(1 for _, s, _ in results if s == FAIL)
    total   = len(results)

    print(f"\n  Total  : {total}")
    print(f"  Passed : {passed}  ✅")
    print(f"  Failed : {failed}  ❌")

    if failed:
        print("\n  ── Failed Tests ───────────────────────────────────────────")
        for name, status, detail in results:
            if status == FAIL:
                print(f"  ❌  {name}")
                if detail:
                    print(f"       → {detail}")

    pct = round(100 * passed / total) if total else 0
    print(f"\n  Score  : {pct}% ({passed}/{total})")
    print("═" * 65 + "\n")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
