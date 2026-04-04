# 🌧️ Drizzle — Parametric Insurance Platform

> **AI-powered parametric insurance for gig economy workers.**
> Drizzle automatically detects real-world disruptions (rain, traffic jams, social unrest) and triggers insurance payouts — no paperwork, no manual claims.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Overview](#2-architecture-overview)
3. [Directory Structure](#3-directory-structure)
4. [Technology Stack](#4-technology-stack)
5. [Firebase & Firestore Setup](#5-firebase--firestore-setup)
6. [Environment Configuration](#6-environment-configuration)
7. [Installation & Running Locally](#7-installation--running-locally)
8. [RBAC — Role-Based Access Control](#8-rbac--role-based-access-control)
9. [API Endpoints — Complete Reference](#9-api-endpoints--complete-reference)
10. [Core Business Engines](#10-core-business-engines)
11. [Firestore Data Models](#11-firestore-data-models)
12. [MCP Signal Servers (Phase 1)](#12-mcp-signal-servers-phase-1)
13. [Middleware](#13-middleware)
14. [Seeding Demo Data](#14-seeding-demo-data)
15. [Testing — Interactive Walkthrough](#15-testing--interactive-walkthrough)
16. [Known Issues & Limitations](#16-known-issues--limitations)
17. [What Has Been Built (Phase Summary)](#17-what-has-been-built-phase-summary)

---

## 1. Project Overview

Drizzle is a **parametric insurance platform** designed for gig economy workers (delivery riders, cab drivers, auto-rickshaw operators). Unlike traditional insurance that requires manual claim filing and court-like approval processes, Drizzle:

- **Automatically detects disruptions** via 3 real-time MCP (Model Context Protocol) signal servers: Weather, Traffic, and Social.
- **Scores the severity** of disruption using a weighted fused scoring formula.
- **Makes instant claim decisions** using a rule-based engine (with LLM upgrade path).
- **Calculates payouts** based on zone-wise daily income estimates and disruption intensity.
- **Runs multi-layer fraud detection** including GPS validation, multi-server agreement checks, and score anomaly detection.
- **Stores everything in Firestore** — workers, policies, claims — with full audit trails.
- **Enforces Role-Based Access Control (RBAC)** across three roles: Worker, Admin, Super Admin.

### What Makes It "Parametric"

Instead of asking a worker to prove damage happened, Drizzle uses **objective third-party data signals**:
- 🌧️ **Weather server** → real-time rain/storm risk score
- 🚗 **Traffic server** → congestion/gridlock disruption score
- 📢 **Social server** → bandh/protest/curfew disruption score

If the fused score crosses a threshold → claim auto-triggers → payout deposited. No human needed for routine cases.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Mobile/Web)                    │
│         Firebase Auth (Google Sign-In / Email)               │
│         Gets Firebase ID Token → Sends to Backend            │
└────────────────────────────┬────────────────────────────────┘
                             │ Bearer Token
                             ▼
┌─────────────────────────────────────────────────────────────┐
│               FastAPI Backend  (backend.main:app)            │
│                                                              │
│  ┌─────────┐  ┌──────────┐  ┌────────┐  ┌───────────────┐  │
│  │  Auth   │  │ Workers  │  │Policies│  │    Claims     │  │
│  │ Routes  │  │  Routes  │  │ Routes │  │    Routes     │  │
│  └────┬────┘  └────┬─────┘  └───┬────┘  └──────┬────────┘  │
│       │            │            │               │            │
│  ┌────▼────────────▼────────────▼───────────────▼────────┐  │
│  │              Service Layer                             │  │
│  │  worker_service | policy_service | claim_service       │  │
│  │  dashboard_service                                     │  │
│  └─────────────────────┬──────────────────────────────────┘  │
│                        │                                      │
│  ┌─────────────────────▼──────────────────────────────────┐  │
│  │              Firebase Admin SDK                        │  │
│  │  Firestore DB  |  Auth Token Verification             │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
  │ Weather MCP  │  │ Traffic MCP  │  │   Social MCP     │
  │  :8001/score │  │  :8002/score │  │   :8003/score    │
  └──────────────┘  └──────────────┘  └──────────────────┘
```

---

## 3. Directory Structure

```
drizzle-main/
│
├── backend/                         # Main FastAPI application
│   ├── main.py                      # App entry point, router registration, lifespan
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── firebase.py              # Firebase Admin SDK init, Firestore client, token verifier
│   │   ├── settings.py              # All env vars, RBAC roles, zone income table
│   │   └── __init__.py
│   │
│   ├── middleware/
│   │   ├── auth.py                  # Firebase token verification, RBAC dependency injection
│   │   ├── logging.py               # Request timing & structured logging middleware
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── schemas.py               # All Pydantic v2 request/response schemas
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py           # GET /auth/me, POST /auth/promote, GET /auth/users
│   │   ├── worker_routes.py         # POST /workers/register, GET /workers/me, GET /workers/
│   │   ├── policy_routes.py         # POST /policies/create, GET /policies/my-policies
│   │   ├── claim_routes.py          # POST /claims/trigger, POST /claims/{id}/review
│   │   ├── dashboard_routes.py      # GET /dashboard/admin, /dashboard/worker, /dashboard/super-admin
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── worker_service.py        # register_worker, get_worker, list_workers, update_worker
│   │   ├── policy_service.py        # create_policy, calculate_premium, list_policies
│   │   ├── claim_service.py         # trigger_claim, make_claim_decision, run_fraud_checks, estimate_payout
│   │   ├── dashboard_service.py     # get_dashboard_stats, get_worker_dashboard
│   │   └── __init__.py
│   │
│   ├── scripts/
│   │   ├── seed_demo.py             # Seeds 5 demo workers + policies + claims
│   │   └── seed_admin.py            # Seeds admin/super_admin accounts
│   │
│   └── readme.md                    # (legacy placeholder)
│
├── testing1.py                      # Interactive end-to-end feature walkthrough (17 steps)
├── test_db_connection.py            # Firebase/Firestore connectivity sanity check
├── seed_all.py                      # Root-level seed script (runs all seed scripts)
│
├── weather_server.py                # MCP Weather Signal Server (FastAPI, port 8001)
├── traffic_server.py                # MCP Traffic Signal Server (FastAPI, port 8002)
├── social_server.py                 # MCP Social Disruption Server (FastAPI, port 8003)
├── mcp_client.py                    # MCP client used in Phase 1 LLM agent
│
├── firebase_key.json                # Firebase service account credentials (⚠️ do NOT commit)
├── .env                             # Environment variables (⚠️ do NOT commit)
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## 4. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Web Framework** | FastAPI 0.110+ | Async REST API, auto-generated OpenAPI docs |
| **ASGI Server** | Uvicorn | Production-grade ASGI server |
| **Data Validation** | Pydantic v2 | Request/response schemas, field validation |
| **Auth** | Firebase Auth (Admin SDK) | JWT token verification, user management |
| **Database** | Firestore (NoSQL) | Workers, policies, claims, users — all document-based |
| **HTTP Client** | httpx | Async calls to MCP signal servers |
| **Config** | python-dotenv | Environment variable management |
| **LLM (Phase 1)** | OpenAI / Groq | Used in Phase 1 MCP agent; rule engine used in Phase 2 |
| **Middleware** | Starlette BaseHTTPMiddleware | Request logging, timing, auth injection |
| **Language** | Python 3.9+ | (3.12 recommended for best asyncio support) |

---

## 5. Firebase & Firestore Setup

### Firebase Project
- **Project ID:** `drizzle-d76ee`
- **Console:** https://console.firebase.google.com/project/drizzle-d76ee

### Collections in Firestore

| Collection | Document ID | Purpose |
|------------|-------------|---------|
| `users` | Firebase UID | Auth profile + role |
| `workers` | Firebase UID | Full worker profile with GPS, vehicle, zone |
| `policies` | `pol_{uuid12}` | Insurance policies per worker |
| `claims` | `clm_{uuid12}` | Claim records with full pipeline data |

### Authentication Flow

```
1. User opens app (iOS/Android/Web)
2. Firebase Auth handles sign-in (Google, Email/Password)
3. App receives Firebase ID Token (JWT)
4. App sends token as:  Authorization: Bearer <id_token>
5. Backend verifies token via Firebase Admin SDK
6. Backend looks up user's role in Firestore `users` collection
7. RBAC middleware grants/denies access to the endpoint
```

### Firestore Indexes Required

One **composite index** is needed for the worker policy listing query:
- **Collection:** `policies`
- **Fields:** `worker_id ASC`, `created_at DESC`
- **Create at:** https://console.firebase.google.com/project/drizzle-d76ee/firestore/indexes

> ⚠️ Without this index, the worker "my-policies" endpoint falls back to an unordered query. The server handles this gracefully but order is not guaranteed.

---

## 6. Environment Configuration

Create a `.env` file in the project root:

```env
# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase_key.json
FIREBASE_PROJECT_ID=drizzle-d76ee

# API Keys (Phase 1 LLM)
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# MCP Server URLs (defaults shown)
MCP_WEATHER_URL=http://127.0.0.1:8001/score
MCP_TRAFFIC_URL=http://127.0.0.1:8002/score
MCP_SOCIAL_URL=http://127.0.0.1:8003/score

# App Settings
ENV=development
DEBUG=True
SECRET_KEY=supersecretkey123
HOST=0.0.0.0
PORT=8000
```

---

## 7. Installation & Running Locally

### Prerequisites
- Python 3.9+ (3.12 recommended)
- Firebase project with service account key (`firebase_key.json`)
- `.env` file configured

### Setup

```bash
# Clone the repository
cd drizzle-main

# Install dependencies
pip install -r requirements.txt

# Seed demo data (optional but recommended)
python3 seed_all.py

# Start the backend
uvicorn backend.main:app --port 8000 --reload

# Start MCP signal servers (separate terminals)
python3 weather_server.py    # port 8001
python3 traffic_server.py    # port 8002
python3 social_server.py     # port 8003
```

### Access Points

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Root — lists all endpoints |
| `http://localhost:8000/docs` | Swagger UI (interactive API explorer) |
| `http://localhost:8000/redoc` | ReDoc documentation |
| `http://localhost:8000/health` | Health check (Firestore + MCP servers) |

---

## 8. RBAC — Role-Based Access Control

Three roles are defined, each with different permissions:

### 👷 Worker (`role = "worker"`)
- Register their own profile
- View their own worker profile (`GET /workers/me`)
- View their own policies (`GET /policies/my-policies`)
- Trigger claims on their own policies (`POST /claims/trigger`)
- View their own claims (`GET /claims/my-claims`)
- Access personal dashboard (`GET /dashboard/worker`)

### 🛡️ Admin (`role = "admin"`)
- All Worker permissions (on any worker)
- **Create policies** for any worker (`POST /policies/create`)
- **List all workers** (`GET /workers/`)
- **List all policies** (`GET /policies/`)
- **List all claims** (`GET /claims/`)
- **Review claims** — approve or reject (`POST /claims/{id}/review`)
- Access admin dashboard (`GET /dashboard/admin`)
- View any worker's dashboard (`GET /dashboard/worker/{worker_id}`)
- List users by role (`GET /auth/users`)

### 👑 Super Admin (`role = "super_admin"`)
- All Admin permissions
- **Promote users** to any role (`POST /auth/promote`)
- Access super admin dashboard with role distribution (`GET /dashboard/super-admin`)

### Implementation

Roles are stored in `users/{uid}.role` in Firestore — **not** in the JWT token. This means role changes take effect immediately without token re-issue.

The auth middleware (`backend/middleware/auth.py`) provides two FastAPI dependencies:
- `get_firebase_user` — verifies the JWT token only (used for registration where no Firestore profile exists yet)
- `get_current_user` — verifies JWT + fetches Firestore user profile + role
- `require_role(*roles)` — factory that returns a dependency enforcing one of the specified roles

---

## 9. API Endpoints — Complete Reference

### System

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/` | None | Root — service info & endpoint list |
| `GET` | `/health` | None | Health check — Firestore + MCP servers |

### Authentication

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| `GET` | `/auth/me` | Any logged-in user | Get current user profile + role |
| `POST` | `/auth/promote` | Super Admin | Promote a user to a different role |
| `GET` | `/auth/users` | Admin, Super Admin | List all users (filterable by role) |

### Workers

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| `POST` | `/workers/register` | Firebase Token (new user) | Register a new worker profile |
| `GET` | `/workers/me` | Worker | Get own worker profile |
| `GET` | `/workers/` | Admin, Super Admin | List all workers (filter by zone) |
| `GET` | `/workers/{worker_id}` | Admin, Super Admin | Get any worker by UID |

### Policies

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| `POST` | `/policies/create` | Admin, Super Admin | Create a policy (premium auto-calculated) |
| `POST` | `/policies/calculate-premium` | Admin, Super Admin | Preview premium without creating policy |
| `GET` | `/policies/` | Admin, Super Admin | List all policies (filter by status/zone) |
| `GET` | `/policies/my-policies` | Worker | Get own policies |
| `GET` | `/policies/detail/{policy_id}` | Any (own data) | Get single policy by ID |
| `GET` | `/policies/{worker_id}` | Any (own data) | Get all policies for a worker |

### Claims

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| `POST` | `/claims/trigger` | Any (own policy) | Trigger a claim — full pipeline |
| `GET` | `/claims/my-claims` | Worker | Get own claims |
| `GET` | `/claims/` | Admin, Super Admin | List all claims (filter by status) |
| `GET` | `/claims/worker/{worker_id}` | Any (own data) | Get claims for a specific worker |
| `POST` | `/claims/{claim_id}/review` | Admin, Super Admin | Approve or reject a claim |
| `GET` | `/claims/{claim_id}` | Any (own data) | Get single claim by ID |

### Dashboards

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| `GET` | `/dashboard/worker` | Worker | Personal stats — policies, claims, payouts |
| `GET` | `/dashboard/admin` | Admin, Super Admin | Platform-wide aggregations |
| `GET` | `/dashboard/worker/{worker_id}` | Admin, Super Admin | Any worker's dashboard |
| `GET` | `/dashboard/super-admin` | Super Admin | Full platform + role distribution |

---

## 10. Core Business Engines

### 10.1 Premium Calculation Engine

**File:** `backend/services/policy_service.py → calculate_premium()`

The premium is calculated using a multi-factor rule-based model:

```
base_rate     = 2.5% of sum_insured per 30 days
monthly_prem  = sum_insured × base_rate × coverage_factor × zone_multiplier × vehicle_factor × history_surcharge
total_premium = monthly_prem × (coverage_days / 30) × duration_discount
```

**Zone Risk Multipliers:**

| City | Multiplier | Reason |
|------|-----------|--------|
| Mumbai | 1.35× | Monsoon flooding, heavy traffic |
| Chennai | 1.30× | Cyclone-prone, waterlogging |
| Kolkata | 1.25× | Monsoon + frequent bandhs |
| Delhi | 1.20× | AQI + traffic + protests |
| Bangalore | 1.15× | Traffic congestion |
| Hyderabad | 1.10× | Moderate risk |
| Pune | 1.05× | Lower risk |
| Jaipur | 1.00× | Baseline |

**Coverage Type Factors:**

| Coverage | Factor | What it covers |
|----------|--------|----------------|
| Comprehensive | 1.00× | All three disruption types |
| Weather only | 0.70× | Rain, storms, floods |
| Traffic only | 0.60× | Congestion, accidents |
| Social only | 0.50× | Bandhs, protests, curfew |

**Vehicle Type Factors:**

| Vehicle | Factor | Reason |
|---------|--------|--------|
| Bicycle | 1.30× | Most exposed to weather |
| Bike | 1.20× | High exposure |
| Scooter | 1.15× | Moderate exposure |
| Auto | 1.00× | Enclosed, lower risk |

**Duration Discounts:**

| Duration | Discount |
|----------|----------|
| < 60 days | 0% |
| 60–89 days | 4% (×0.96) |
| 90–179 days | 8% (×0.92) |
| 180+ days | 15% (×0.85) |

**Claim History Surcharge:** +5% per past claim, capped at +25%.

---

### 10.2 Claim Decision Engine

**File:** `backend/services/claim_service.py → make_claim_decision()`

Inputs: `weather_score (w)`, `traffic_score (t)`, `social_score (s)`

```
fused_score = 0.35×w + 0.25×t + 0.25×s
```

**Trigger Logic:**

| Condition | Decision | Confidence |
|-----------|----------|------------|
| `fused ≥ 0.6` | Triggered | HIGH |
| Any single score `≥ 0.7` | Triggered | HIGH or MEDIUM |
| `fused ≥ 0.4` AND 2+ scores `≥ 0.3` | Triggered | MEDIUM |
| None of above | No claim | LOW |

**Auto-approval:** If `triggered = True`, `confidence = HIGH`, and `fraud_verdict = clean` → status set to `approved` automatically. Otherwise it goes to `pending` for admin review.

**Primary Cause:** Determined by highest single score. If the range between max and min score is < 0.15, cause is set to `"combined"`.

---

### 10.3 Fraud Detection Engine

**File:** `backend/services/claim_service.py → run_fraud_checks()`

Four layers of fraud detection run on every claim:

**Layer 1 — GPS Validation (Haversine distance)**
- Calculates distance between claim GPS coordinates and worker's registered zone
- `> 25km` → GPS invalid, `+0.35` fraud score, flag added
- `15–25km` → GPS warning, `+0.10` fraud score, flag added

**Layer 2 — Multi-Server Agreement**
- At least 2 out of 3 MCP servers must be reachable and return scores
- `< 2 servers up` → `+0.20` fraud score, flag added
- This prevents gaming the system when servers are artificially taken offline

**Layer 3 — Score Divergence**
- If max score − min score > 0.7 AND max > 0.6 → suspicious localized manipulation
- `+0.15` fraud score

**Layer 4 — Anomaly Detection**
- If all three scores are exactly 0.0 → impossible if a real disruption triggered the claim
- `+0.40` fraud score (near-certain fraud)

**Verdict Thresholds:**

| Fraud Score | Verdict | Claim Status |
|-------------|---------|--------------|
| 0.0 – 0.19 | `clean` | Normal processing |
| 0.20 – 0.49 | `suspicious` | Sent to `pending` for admin review |
| 0.50+ | `fraudulent` | Status set to `flagged` |

---

### 10.4 Payout Estimation Engine

**File:** `backend/services/claim_service.py → estimate_payout()`

**Zone Base Daily Income (INR):**

| City | Daily Income |
|------|-------------|
| Mumbai | ₹1,400 |
| Delhi | ₹1,300 |
| Bangalore | ₹1,250 |
| Hyderabad | ₹1,100 |
| Noida | ₹1,100 |
| Chennai | ₹1,000 |
| Pune | ₹1,050 |
| Kolkata | ₹950 |
| Jaipur | ₹850 |
| Default | ₹1,000 |

**Formula:**

```
disruption_intensity = 0.35×w + 0.25×t + 0.25×s
confidence_mult      = { HIGH: 1.0, MEDIUM: 0.75, LOW: 0.5 }
income_loss_ratio    = disruption_intensity × confidence_mult
actual_income        = base_income × (1 − income_loss_ratio)
income_loss          = base_income − actual_income
payout_amount        = income_loss × 80%   (capped at sum_insured)
```

The 80% coverage ratio reflects the standard parametric insurance structure: workers absorb 20% of the loss as a self-retention.

---

## 11. Firestore Data Models

### `users/{uid}`
```json
{
  "uid": "firebase_uid",
  "email": "worker@example.com",
  "display_name": "Rahul Kumar",
  "role": "worker",              // "worker" | "admin" | "super_admin"
  "is_active": true,
  "created_at": "2024-01-01T00:00:00+00:00",
  "updated_at": "2024-01-01T00:00:00+00:00"
}
```

### `workers/{uid}`
```json
{
  "uid": "firebase_uid",
  "email": "worker@example.com",
  "display_name": "Rahul Kumar",
  "phone": "+919876543210",
  "zone": "OMR-Chennai",
  "vehicle_type": "bike",        // "bike" | "scooter" | "bicycle" | "auto"
  "gps_lat": 12.9352,
  "gps_lon": 77.6245,
  "role": "worker",
  "is_active": true,
  "total_claims": 2,
  "total_payouts": 875.50,
  "created_at": "2024-01-01T00:00:00+00:00",
  "updated_at": "2024-01-01T00:00:00+00:00"
}
```

### `policies/{pol_id}`
```json
{
  "policy_id": "pol_abc123def456",
  "worker_id": "firebase_uid",
  "zone": "OMR-Chennai",
  "coverage_type": "comprehensive",
  "coverage_days": 30,
  "sum_insured": 35000.0,
  "premium": 1207.50,
  "risk_score": 0.325,
  "daily_rate": 40.25,
  "zone_multiplier": 1.30,
  "status": "active",            // "active" | "expired" | "cancelled"
  "start_date": "2024-01-01T00:00:00+00:00",
  "end_date": "2024-01-31T00:00:00+00:00",
  "created_by": "admin_uid",
  "created_at": "2024-01-01T00:00:00+00:00",
  "updated_at": "2024-01-01T00:00:00+00:00"
}
```

### `claims/{clm_id}`
```json
{
  "claim_id": "clm_bde88a07a568",
  "policy_id": "pol_abc123def456",
  "worker_id": "firebase_uid",
  "zone": "OMR-Chennai",
  "lat": 12.9352,
  "lon": 77.6245,
  "notes": "Heavy rain, couldn't work today",

  "weather_score": 0.75,
  "traffic_score": 0.55,
  "social_score": 0.40,

  "claim_triggered": true,
  "confidence": "HIGH",
  "primary_cause": "weather",
  "explanation": "Fused disruption score: 0.528. Weather=0.75...",
  "recommended_action": "Auto-payout initiated",
  "reasoning_source": "rule_engine",
  "fused_score": 0.528,

  "payout_amount": 375.00,
  "disruption_intensity": 0.469,
  "base_daily_income": 1000,

  "fraud_check": {
    "gps_valid": true,
    "multi_server_agreement": true,
    "fraud_score": 0.0,
    "flags": [],
    "verdict": "clean"
  },

  "status": "approved",          // "pending" | "approved" | "rejected" | "flagged" | "paid"
  "triggered_by": "worker_uid",
  "reviewed_by": "admin_uid",
  "review_notes": "Manually approved after walkthrough review",
  "created_at": "2024-01-01T00:00:00+00:00",
  "updated_at": "2024-01-01T00:00:00+00:00"
}
```

---

## 12. MCP Signal Servers (Phase 1)

Three independent FastAPI microservices provide real-time disruption signals. These were built in Phase 1 and are reused in Phase 2 via HTTP calls.

| Server | File | Port | Endpoint | Returns |
|--------|------|------|----------|---------|
| Weather | `weather_server.py` | 8001 | `GET /score` | `weather_risk_score`, `risk_level`, details |
| Traffic | `traffic_server.py` | 8002 | `GET /score` | `traffic_risk_score`, `congestion_level` |
| Social | `social_server.py` | 8003 | `GET /score` | `social_disruption_score`, `event_type` |

### Signal Collection Flow

When `POST /claims/trigger` is called, the backend simultaneously calls all 3 MCP servers via `asyncio.gather()` (parallel async requests with 10-second timeout). If a server is unreachable, its score defaults to `0.0` and is flagged in fraud detection.

```python
# From claim_service.py
weather, traffic, social = await asyncio.gather(
    _fetch_mcp_server("weather", MCP_WEATHER_URL, params),
    _fetch_mcp_server("traffic", MCP_TRAFFIC_URL, params),
    _fetch_mcp_server("social",  MCP_SOCIAL_URL,  params),
)
```

### Fallback Strategy

If MCP servers are offline:
- Scores default to `0.0`
- Fraud detection flags "Only X/3 servers responded"
- Claim can still be triggered manually with direct scores (for testing purposes)
- Health endpoint (`/health`) reports MCP server reachability

---

## 13. Middleware

### Auth Middleware (`backend/middleware/auth.py`)

Three dependency-injection helpers:

```python
# Verifies JWT token only — no Firestore lookup
# Used for /workers/register (user has no profile yet)
get_firebase_user(authorization: str) -> dict

# Verifies JWT + fetches user role from Firestore
# Used for all protected endpoints
get_current_user(authorization: str) -> dict

# Factory — enforces one of the specified roles
# Raises 403 if role doesn't match
require_role(*roles) -> Depends(...)
```

### Request Logging Middleware (`backend/middleware/logging.py`)

Logs every HTTP request with:
- Method and path
- Response status code
- Request duration in milliseconds
- Authenticated user UID and role (if available)

Example log output:
```
2024-01-01 10:00:00  INFO      [drizzle.request]  POST /claims/trigger → 201 (234.5ms) user=worker_uid role=worker
```

---

## 14. Seeding Demo Data

### Seeded Users

| Name | Email | Role | Zone | Vehicle |
|------|-------|------|------|---------|
| Rahul Kumar | rahul.kumar@demo.drizzle.io | worker | OMR-Chennai | bike |
| Priya Sharma | priya.sharma@demo.drizzle.io | worker | Andheri-Mumbai | scooter |
| Amit Patel | amit.patel@demo.drizzle.io | worker | Koramangala-Bangalore | bike |
| Sneha Reddy | sneha.reddy@demo.drizzle.io | worker | Hitech-Hyderabad | auto |
| Vikram Singh | vikram.singh@demo.drizzle.io | worker | Connaught-Delhi | bicycle |
| Drizzle Admin | admin@drizzle.io | admin | — | — |
| Drizzle Super Admin | superadmin@drizzle.io | super_admin | — | — |

Each demo worker has:
- A seeded insurance policy in Firestore
- 1–2 sample claims with various statuses (approved, pending, flagged)

### Running Seeds

```bash
# Seed everything at once
python3 seed_all.py

# Or individually
python3 backend/scripts/seed_demo.py
python3 backend/scripts/seed_admin.py
```

---

## 15. Testing — Interactive Walkthrough

`testing1.py` is a comprehensive, interactive 17-step end-to-end test that runs directly against live Firestore. It tests every feature of the platform and prints color-coded results.

### Running the Walkthrough

```bash
# Interactive mode (manual ENTER between steps)
python3 testing1.py

# Automated mode (non-interactive)
printf '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n' | python3 testing1.py
```

### Steps Covered

| Step | Feature | What It Tests |
|------|---------|---------------|
| 1 | Firebase Auth + RBAC | Lists all seeded users from Firestore, explains roles |
| 2 | Worker Registration | Creates `users/{uid}` + `workers/{uid}` in Firestore |
| 3 | Worker Profile Fetch | Calls `get_worker(uid)` from worker_service |
| 4 | List All Workers | Admin view of all workers |
| 5 | Premium Calculation | 5 zone/vehicle/coverage combinations |
| 6 | Policy Creation | Full policy doc written to Firestore |
| 7 | List Policies | Admin all-policies + worker own-policies |
| 8 | Claim Decision Engine | 5 score combinations — trigger/no-trigger decisions |
| 9 | Fraud Detection | 4 scenarios: clean, GPS warning, GPS fraud, server fraud |
| 10 | Payout Estimation | 5 zone/confidence combinations |
| 11 | Trigger Full Claim | Complete pipeline → claim saved in Firestore |
| 12 | Fetch Claim | Read claim back by ID |
| 13 | Admin Claim Review | Approve a pending claim |
| 14 | Worker Dashboard | Personal stats aggregation |
| 15 | Admin Dashboard | Platform-wide stats + zone breakdown |
| 16 | Super Admin View | Role distribution + claim status breakdown |
| 17 | Cleanup | Deletes all test documents, preserves seed data |

### Latest Test Results (verified ✅)

```
✅  Step  1:  Firebase Auth + RBAC roles            → 8 users found
✅  Step  2:  Worker Registration                   → Firestore write confirmed
✅  Step  3:  Worker Profile Fetch                  → Profile returned
✅  Step  4:  List All Workers                      → 7 workers listed
✅  Step  5:  Premium Calculation                   → 5 scenarios computed
✅  Step  6:  Policy Creation                       → Policy ID generated
✅  Step  7:  Policy Listing                        → Admin + worker views
✅  Step  8:  Claim Decision Engine                 → 5/5 decisions correct
✅  Step  9:  Fraud Detection                       → 4 scenarios flagged correctly
✅  Step 10:  Payout Estimation                     → Zone-based payouts computed
✅  Step 11:  Trigger Claim                         → Full pipeline → Firestore
✅  Step 12:  Fetch Claim                           → Claim retrieved
✅  Step 13:  Admin Claim Review                    → Approved status confirmed
✅  Step 14:  Worker Dashboard                      → Stats aggregated
✅  Step 15:  Admin Dashboard                       → Platform stats + zone breakdown
✅  Step 16:  Super Admin View                      → Role distribution rendered
✅  Step 17:  Cleanup                               → Test data removed
```

---

## 16. Known Issues & Limitations

### Firestore Composite Index (Minor — handled)
- **Issue:** `GET /policies/my-policies` uses `worker_id + order_by created_at` which requires a Firestore composite index.
- **Impact:** Without the index, the query falls back to unordered results (still correct, just not sorted).
- **Fix:** Create the index at https://console.firebase.google.com/project/drizzle-d76ee/firestore/indexes

### Python Version Warning
- The `google-api-core` package shows a `FutureWarning` on Python 3.9.
- **Fix:** Upgrade to Python 3.10+ for full compatibility.

### MCP Servers Not Auto-Started
- The 3 MCP signal servers (`weather_server.py`, `traffic_server.py`, `social_server.py`) must be started separately.
- When they are offline, claim scores default to `0.0` and fraud detection flags this.

### Auth Token for Testing
- Real Firebase ID tokens are required for API endpoints.
- For Swagger UI testing, use the Firebase REST API to get a token, then paste it into the `Authorization: Bearer <token>` header.

### CORS
- Currently set to `allow_origins=["*"]`. Tighten to specific frontend origins before production deployment.

---

## 17. What Has Been Built (Phase Summary)

### Phase 1 — MCP Signal Intelligence (complete ✅)
- Built 3 MCP signal servers: Weather, Traffic, Social
- Built MCP client (`mcp_client.py`) with LLM reasoning pipeline using OpenAI/Groq
- Implemented fused scoring with weighted formula
- Claim decision engine with confidence levels
- Payout estimation with zone-based income model

### Phase 2 — Production Backend (complete ✅)
- Migrated from single-script prototype to full modular FastAPI application
- Firebase Admin SDK integration — token verification + Firestore CRUD
- Implemented 3-role RBAC system (Worker / Admin / Super Admin)
- 5 route modules with 20+ endpoints
- 4 service modules with all business logic
- Pydantic v2 schemas for all request/response models
- Multi-layer fraud detection engine (GPS + multi-server + anomaly)
- Worker, Admin, and Super Admin dashboard aggregations
- Request logging middleware with timing
- Comprehensive seeding scripts for demo data
- 17-step interactive end-to-end test walkthrough (all passing ✅)

### Next Steps (Phase 3 — Roadmap)
- [ ] Firebase Hosting / Cloud Run deployment
- [ ] Firestore Security Rules (replace open rules)
- [ ] Push notification on claim approval
- [ ] iOS/Android frontend integration
- [ ] LLM reasoning re-integration for edge-case claim decisions
- [ ] Policy expiry cron job (auto-expire after `end_date`)
- [ ] Payout disbursement integration (UPI/bank transfer)

---

## Quick Command Reference

```bash
# Start backend
uvicorn backend.main:app --port 8000 --reload

# Start all MCP servers
python3 weather_server.py &
python3 traffic_server.py &
python3 social_server.py &

# Seed demo data
python3 seed_all.py

# Run full test walkthrough (automated)
printf '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n' | python3 testing1.py

# View Swagger docs
open http://localhost:8000/docs

# View Firestore
open https://console.firebase.google.com/project/drizzle-d76ee/firestore
```

---

*Built with ❤️ for gig economy workers — because disruptions shouldn't derail their livelihood.*
