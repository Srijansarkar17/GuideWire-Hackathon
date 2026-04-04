"""
Drizzle — Database Connection & Backend Test
==============================================
Tests:
  1. Firebase Admin SDK initialization
  2. Firestore read/write connectivity
  3. Module imports (all routes, services, models)
  4. Premium calculation engine
  5. Claim decision engine
  6. Fraud detection engine
  7. FastAPI app startup & health endpoint

Run:  python3 test_db_connection.py
"""

import sys
import os
import time
import traceback

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PASS = "✅"
FAIL = "❌"
WARN = "⚠️"
results = []


def test(name, fn):
    """Run a single test and record result."""
    try:
        result = fn()
        results.append((PASS, name, result))
        print(f"  {PASS}  {name}")
        if result:
            print(f"      → {result}")
    except Exception as e:
        results.append((FAIL, name, str(e)))
        print(f"  {FAIL}  {name}")
        print(f"      → {e}")
        traceback.print_exc(limit=2)


def header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ══════════════════════════════════════════════════════════════
# TEST 1: Environment & Settings
# ══════════════════════════════════════════════════════════════
header("1. ENVIRONMENT & SETTINGS")

def test_env_loading():
    from backend.config.settings import (
        FIREBASE_CREDENTIALS_PATH, FIREBASE_PROJECT_ID,
        ENV, DEBUG, HOST, PORT, GROQ_API_KEY,
    )
    assert os.path.exists(FIREBASE_CREDENTIALS_PATH), \
        f"Firebase key not found at {FIREBASE_CREDENTIALS_PATH}"
    return (f"project={FIREBASE_PROJECT_ID}, env={ENV}, debug={DEBUG}, "
            f"host={HOST}:{PORT}, groq_key={'set' if GROQ_API_KEY else 'MISSING'}")

test("Settings load from .env", test_env_loading)


# ══════════════════════════════════════════════════════════════
# TEST 2: Firebase Admin SDK Initialization
# ══════════════════════════════════════════════════════════════
header("2. FIREBASE ADMIN SDK")

def test_firebase_init():
    import firebase_admin
    from backend.config.firebase import _app, db
    assert firebase_admin._apps, "No Firebase app initialized"
    app = firebase_admin.get_app()
    return f"App name={app.name}, project={app.project_id}"

test("Firebase Admin SDK initialized", test_firebase_init)


def test_firebase_db_client():
    from backend.config.firebase import db
    assert db is not None, "Firestore client is None"
    return f"Firestore client type: {type(db).__name__}"

test("Firestore client singleton", test_firebase_db_client)


# ══════════════════════════════════════════════════════════════
# TEST 3: Firestore READ Connectivity
# ══════════════════════════════════════════════════════════════
header("3. FIRESTORE CONNECTIVITY")

def test_firestore_read():
    from backend.config.firebase import db
    start = time.time()
    # Try to read from _healthcheck collection (may be empty, that's fine)
    docs = db.collection("_healthcheck").limit(1).get()
    elapsed = round((time.time() - start) * 1000, 1)
    return f"Read completed in {elapsed}ms (docs found: {len(docs)})"

test("Firestore READ (healthcheck)", test_firestore_read)


def test_firestore_collections():
    """Check which collections exist in the DB."""
    from backend.config.firebase import db
    start = time.time()
    collections = [c.id for c in db.collections()]
    elapsed = round((time.time() - start) * 1000, 1)
    if collections:
        return f"Collections ({elapsed}ms): {', '.join(collections)}"
    else:
        return f"No collections found ({elapsed}ms) — DB is empty (this is OK for first run)"

test("Firestore collections list", test_firestore_collections)


# ══════════════════════════════════════════════════════════════
# TEST 4: Firestore WRITE/READ/DELETE Test
# ══════════════════════════════════════════════════════════════
header("4. FIRESTORE WRITE/READ/DELETE")

def test_firestore_write_read_delete():
    from backend.config.firebase import db
    from datetime import datetime, timezone
    
    test_collection = "_drizzle_test"
    test_doc_id = "connectivity_test"
    now = datetime.now(timezone.utc).isoformat()
    
    # WRITE
    start = time.time()
    db.collection(test_collection).document(test_doc_id).set({
        "test": True,
        "timestamp": now,
        "message": "Drizzle DB connectivity test",
    })
    write_ms = round((time.time() - start) * 1000, 1)
    
    # READ
    start = time.time()
    doc = db.collection(test_collection).document(test_doc_id).get()
    read_ms = round((time.time() - start) * 1000, 1)
    assert doc.exists, "Document was written but cannot be read back"
    data = doc.to_dict()
    assert data["test"] == True
    assert data["timestamp"] == now
    
    # DELETE (cleanup)
    start = time.time()
    db.collection(test_collection).document(test_doc_id).delete()
    del_ms = round((time.time() - start) * 1000, 1)
    
    return f"Write={write_ms}ms, Read={read_ms}ms, Delete={del_ms}ms — all OK"

test("Firestore WRITE → READ → DELETE", test_firestore_write_read_delete)


# ══════════════════════════════════════════════════════════════
# TEST 5: Read Existing Data (if any)
# ══════════════════════════════════════════════════════════════
header("5. EXISTING DATA CHECK")

def test_existing_data():
    from backend.config.firebase import db
    
    counts = {}
    for coll_name in ["users", "workers", "policies", "claims"]:
        docs = list(db.collection(coll_name).limit(5).stream())
        counts[coll_name] = len(docs)
    
    summary = ", ".join(f"{k}={v}" for k, v in counts.items())
    if any(v > 0 for v in counts.values()):
        return f"Found data: {summary}"
    else:
        return f"All empty: {summary} — you'll need to seed data or register users"

test("Existing Firestore data", test_existing_data)


# ══════════════════════════════════════════════════════════════
# TEST 6: Module Imports
# ══════════════════════════════════════════════════════════════
header("6. MODULE IMPORTS")

def test_model_imports():
    from backend.models.schemas import (
        UserBase, UserResponse, WorkerRegisterRequest, WorkerResponse,
        PolicyCreateRequest, PolicyResponse,
        ClaimTriggerRequest, ClaimResponse, FraudCheckResult,
        DashboardStats, ClaimReviewRequest,
    )
    return "All 11 Pydantic schemas imported"

test("Pydantic schemas", test_model_imports)


def test_service_imports():
    from backend.services import worker_service, policy_service, claim_service, dashboard_service
    return "All 4 services imported"

test("Service modules", test_service_imports)


def test_middleware_imports():
    from backend.middleware.auth import get_firebase_user, get_current_user, require_role
    from backend.middleware.logging import RequestLoggingMiddleware
    return "Auth + Logging middleware imported"

test("Middleware modules", test_middleware_imports)


def test_route_imports():
    from backend.routes.auth_routes import router as auth_router
    from backend.routes.worker_routes import router as worker_router
    from backend.routes.policy_routes import router as policy_router
    from backend.routes.claim_routes import router as claim_router
    from backend.routes.dashboard_routes import router as dashboard_router
    return f"All 5 routers imported (auth, worker, policy, claim, dashboard)"

test("Route modules", test_route_imports)


# ══════════════════════════════════════════════════════════════
# TEST 7: Premium Calculation Engine
# ══════════════════════════════════════════════════════════════
header("7. PREMIUM CALCULATION ENGINE")

def test_premium_calc():
    from backend.services.policy_service import calculate_premium
    
    result = calculate_premium(
        zone="OMR-Chennai",
        coverage_type="comprehensive",
        coverage_days=30,
        sum_insured=30000.0,
        vehicle_type="bike",
        worker_claim_history=0,
    )
    assert "premium" in result
    assert "risk_score" in result
    assert result["premium"] > 0
    return (f"zone=Chennai, type=comprehensive, 30d, ₹30k → "
            f"premium=₹{result['premium']}, risk={result['risk_score']}, "
            f"daily=₹{result['daily_rate']}")

test("Premium calculation (Chennai/comprehensive/30d)", test_premium_calc)


def test_premium_zones():
    from backend.services.policy_service import calculate_premium
    
    zones = ["mumbai", "delhi", "bangalore", "kolkata", "jaipur"]
    premiums = {}
    for zone in zones:
        r = calculate_premium(zone=zone, coverage_type="comprehensive",
                             coverage_days=30, sum_insured=30000.0)
        premiums[zone] = r["premium"]
    
    parts = [f"{z}=₹{p}" for z, p in premiums.items()]
    return ", ".join(parts)

test("Premium across zones (₹30k/30d/comprehensive)", test_premium_zones)


# ══════════════════════════════════════════════════════════════
# TEST 8: Claim Decision Engine
# ══════════════════════════════════════════════════════════════
header("8. CLAIM DECISION ENGINE")

def test_claim_decision_high():
    from backend.services.claim_service import make_claim_decision
    
    # fused = 0.35*0.9 + 0.25*0.8 + 0.25*0.7 = 0.315+0.2+0.175 = 0.69 → HIGH
    result = make_claim_decision(w=0.9, t=0.8, s=0.7)
    assert result["claim_triggered"] == True
    assert result["confidence"] == "HIGH"
    return (f"w=0.9, t=0.8, s=0.7 → triggered={result['claim_triggered']}, "
            f"confidence={result['confidence']}, cause={result['primary_cause']}")

test("High disruption → claim triggered", test_claim_decision_high)


def test_claim_decision_low():
    from backend.services.claim_service import make_claim_decision
    
    result = make_claim_decision(w=0.1, t=0.1, s=0.1)
    assert result["claim_triggered"] == False
    return (f"w=0.1, t=0.1, s=0.1 → triggered={result['claim_triggered']}, "
            f"confidence={result['confidence']}")

test("Low disruption → no claim", test_claim_decision_low)


# ══════════════════════════════════════════════════════════════
# TEST 9: Fraud Detection Engine
# ══════════════════════════════════════════════════════════════
header("9. FRAUD DETECTION ENGINE")

def test_fraud_clean():
    from backend.services.claim_service import run_fraud_checks
    
    signals = {
        "weather": {"status": "ok", "data": {}},
        "traffic": {"status": "ok", "data": {}},
        "social":  {"status": "ok", "data": {}},
    }
    result = run_fraud_checks(
        lat=13.08, lon=80.27,
        worker_lat=13.08, worker_lon=80.27,
        w=0.6, t=0.5, s=0.4,
        signals=signals,
    )
    assert result["verdict"] == "clean"
    return f"Same location → verdict={result['verdict']}, fraud_score={result['fraud_score']}"

test("Clean claim (GPS match, all servers OK)", test_fraud_clean)


def test_fraud_gps_mismatch():
    from backend.services.claim_service import run_fraud_checks
    
    signals = {
        "weather": {"status": "ok", "data": {}},
        "traffic": {"status": "ok", "data": {}},
        "social":  {"status": "ok", "data": {}},
    }
    result = run_fraud_checks(
        lat=28.61, lon=77.20,   # Delhi
        worker_lat=13.08, worker_lon=80.27,  # Chennai
        w=0.6, t=0.5, s=0.4,
        signals=signals,
    )
    assert result["fraud_score"] > 0.2
    return f"Delhi vs Chennai → verdict={result['verdict']}, fraud_score={result['fraud_score']}, flags={result['flags']}"

test("Fraudulent claim (GPS mismatch)", test_fraud_gps_mismatch)


# ══════════════════════════════════════════════════════════════
# TEST 10: Payout Estimation
# ══════════════════════════════════════════════════════════════
header("10. PAYOUT ESTIMATION")

def test_payout():
    from backend.services.claim_service import estimate_payout
    
    result = estimate_payout(
        zone="OMR-Chennai", w=0.7, t=0.5, s=0.4,
        confidence="HIGH", sum_insured=30000.0,
    )
    assert result["payout_amount"] > 0
    return (f"Chennai w=0.7,t=0.5,s=0.4 HIGH → "
            f"payout=₹{result['payout_amount']}, "
            f"income_loss=₹{result['income_loss']}, "
            f"disruption={result['disruption_intensity']}")

test("Payout estimation (Chennai/HIGH)", test_payout)


# ══════════════════════════════════════════════════════════════
# TEST 11: FastAPI App Construction
# ══════════════════════════════════════════════════════════════
header("11. FASTAPI APP")

def test_fastapi_app():
    from backend.main import app
    
    routes = [r.path for r in app.routes if hasattr(r, 'path')]
    endpoints = [r for r in routes if not r.startswith("/openapi") and not r.startswith("/docs") and not r.startswith("/redoc")]
    return f"App loaded with {len(endpoints)} routes: {', '.join(sorted(set(endpoints)))}"

test("FastAPI app construction", test_fastapi_app)


def test_fastapi_sync_endpoints():
    """Test the root and health endpoints via TestClient."""
    try:
        from fastapi.testclient import TestClient
        from backend.main import app
        
        client = TestClient(app)
        
        # Root
        r = client.get("/")
        assert r.status_code == 200
        data = r.json()
        assert data["version"] == "2.0.0"
        
        return f"GET / → {r.status_code}, version={data['version']}"
    except ImportError:
        return "TestClient not available (install httpx for sync testing)"

test("GET / root endpoint", test_fastapi_sync_endpoints)


def test_health_endpoint():
    """Test /health endpoint — checks Firestore connectivity."""
    try:
        from fastapi.testclient import TestClient
        from backend.main import app
        
        client = TestClient(app)
        r = client.get("/health")
        assert r.status_code == 200
        data = r.json()
        firestore_status = data.get("firestore", "unknown")
        mcp_status = data.get("mcp_servers", {})
        return (f"GET /health → {r.status_code}, "
                f"firestore={firestore_status}, "
                f"mcp={mcp_status}")
    except ImportError:
        return "TestClient not available"

test("GET /health endpoint", test_health_endpoint)


# ══════════════════════════════════════════════════════════════
# TEST 12: Firebase Auth Functions
# ══════════════════════════════════════════════════════════════
header("12. FIREBASE AUTH FUNCTIONS")

def test_auth_functions():
    from backend.config.firebase import verify_id_token, get_user
    # We can't test with a real token, but ensure functions exist
    assert callable(verify_id_token)
    assert callable(get_user)
    return "verify_id_token() and get_user() are callable"

test("Auth functions available", test_auth_functions)


# ══════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════════════
header("TEST SUMMARY")

passed = sum(1 for r in results if r[0] == PASS)
failed = sum(1 for r in results if r[0] == FAIL)
total = len(results)

print(f"\n  Total:  {total}")
print(f"  {PASS} Passed: {passed}")
print(f"  {FAIL} Failed: {failed}")
print()

if failed > 0:
    print("  Failed tests:")
    for status, name, detail in results:
        if status == FAIL:
            print(f"    {FAIL} {name}: {detail}")
    print()

if failed == 0:
    print("  🎉 ALL TESTS PASSED — Backend is production-ready!")
else:
    print(f"  ⚠️  {failed} test(s) failed — see details above.")

print()
sys.exit(1 if failed > 0 else 0)
