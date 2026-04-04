Firestore (NoSQL)
│
├── 📁 users/              ← Collection
│   ├── 📄 admin_001       ← Document (JSON-like)
│   │     { uid, email, display_name, role: "admin", ... }
│   ├── 📄 worker_rahul
│   │     { uid, email, display_name, role: "worker", ... }
│   └── ...
│
├── 📁 workers/
│   ├── 📄 worker_rahul
│   │     { zone: "OMR-Chennai", vehicle_type: "bike", gps_lat, ... }
│   └── ...
│
├── 📁 policies/
│   ├── 📄 pol_aa3e98e1e5f8
│   │     { worker_id, zone, premium: 1170.0, status: "active", ... }
│   └── ...
│
└── 📁 claims/
    ├── 📄 clm_b205b239350d
    │     { weather_score: 0.85, fraud_check: { verdict: "clean" }, ... }
    └── ...
