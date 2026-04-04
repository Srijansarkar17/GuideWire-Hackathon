"""
╔══════════════════════════════════════════════════════════════════╗
║     🌧️  DRIZZLE — Manual Interactive Feature Walkthrough         ║
║     You type the values. The engine responds. Live. Real.        ║
╚══════════════════════════════════════════════════════════════════╝

Run:  python3 walkthrough_manual.py
"""

import sys, os, uuid, time, json
from datetime import datetime, timezone
import asyncio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

# ── Colors ────────────────────────────────────────────────────────
R   = "\033[91m"
G   = "\033[92m"
Y   = "\033[93m"
B   = "\033[94m"
M   = "\033[95m"
C   = "\033[96m"
W   = "\033[97m"
DIM = "\033[2m"
UL  = "\033[4m"
RST = "\033[0m"

def ok(msg):    print(f"  {G}✅  {RST}{msg}")
def err(msg):   print(f"  {R}❌  {RST}{msg}")
def info(msg):  print(f"  {C}ℹ️   {RST}{msg}")
def warn(msg):  print(f"  {Y}⚠️   {RST}{msg}")
def hint(msg):  print(f"  {DIM}💡  {msg}{RST}")
def show(k, v): print(f"  {DIM}{k}:{RST}  {W}{v}{RST}")
def result(k, v, color=G): print(f"  {color}{k}:{RST}  {W}{v}{RST}")

def header(step, title, subtitle=""):
    print(f"\n{B}{'━'*64}{RST}")
    print(f"{W}  MODULE {step}: {title}{RST}")
    if subtitle:
        print(f"  {DIM}{subtitle}{RST}")
    print(f"{B}{'━'*64}{RST}")

def section(title):
    print(f"\n  {M}▶  {title}{RST}")
    print(f"  {DIM}{'─'*56}{RST}")

def ask(prompt, default=None, valid_options=None):
    """Prompt user for input with optional default and validation."""
    if valid_options:
        options_str = " / ".join([f"{W}{o}{RST}" for o in valid_options])
        print(f"\n  {Y}→  Options:{RST}  {options_str}")
    if default is not None:
        print(f"  {DIM}(Press ENTER for default: {default}){RST}")
    while True:
        val = input(f"  {C}❯  {prompt}: {RST}").strip()
        if val == "" and default is not None:
            return default
        if valid_options and val not in valid_options:
            warn(f"Invalid. Choose from: {', '.join(valid_options)}")
            continue
        if val == "" and default is None:
            warn("This field is required, please enter a value.")
            continue
        return val

def ask_float(prompt, default=None, min_val=0.0, max_val=None):
    """Prompt user for a float with range validation."""
    if default is not None:
        print(f"  {DIM}(Press ENTER for default: {default}){RST}")
    range_hint = f"[{min_val}"
    if max_val is not None:
        range_hint += f" – {max_val}"
    range_hint += "]"
    print(f"  {DIM}Range: {range_hint}{RST}")
    while True:
        val = input(f"  {C}❯  {prompt}: {RST}").strip()
        if val == "" and default is not None:
            return float(default)
        try:
            f = float(val)
            if f < min_val or (max_val is not None and f > max_val):
                warn(f"Value out of range {range_hint}")
                continue
            return f
        except ValueError:
            warn("Please enter a valid number.")

def ask_int(prompt, default=None, min_val=1, max_val=None):
    """Prompt user for an integer."""
    if default is not None:
        print(f"  {DIM}(Press ENTER for default: {default}){RST}")
    while True:
        val = input(f"  {C}❯  {prompt}: {RST}").strip()
        if val == "" and default is not None:
            return int(default)
        try:
            i = int(val)
            if i < min_val or (max_val is not None and i > max_val):
                warn(f"Must be between {min_val} and {max_val or '∞'}")
                continue
            return i
        except ValueError:
            warn("Please enter a whole number.")

def divider():
    print(f"\n{DIM}{'═'*64}{RST}")

def menu(options):
    """Show a numbered menu, return selected key."""
    for i, (key, label) in enumerate(options.items(), 1):
        print(f"  {W}{i}.{RST}  {label}")
    while True:
        val = input(f"\n  {C}❯  Enter number (1–{len(options)}): {RST}").strip()
        try:
            idx = int(val) - 1
            if 0 <= idx < len(options):
                return list(options.keys())[idx]
        except ValueError:
            pass
        warn(f"Enter a number between 1 and {len(options)}")


# ══════════════════════════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════════════════════════
print(f"""
{B}╔══════════════════════════════════════════════════════════════╗{RST}
{B}║{RST}  {W}🌧️  DRIZZLE — Manual Interactive Walkthrough{RST}            {B}║{RST}
{B}║{RST}  {DIM}You control every input. See the engines respond live.{RST}   {B}║{RST}
{B}╚══════════════════════════════════════════════════════════════╝{RST}

  Available Modules:
  {C}1.{RST}  💰  Premium Calculation Engine
  {C}2.{RST}  ⚡  Claim Decision Engine
  {C}3.{RST}  🔍  Fraud Detection Engine
  {C}4.{RST}  💸  Payout Estimation Engine
  {C}5.{RST}  🔗  Full Claim Pipeline (Decision + Fraud + Payout)
  {C}6.{RST}  👷  Worker Registration (Firestore)
  {C}7.{RST}  📊  Live Dashboard Stats (from Firestore)
  {C}8.{RST}  🔄  Run All Modules in Sequence
  {C}9.{RST}  🚪  Exit
""")

# ── Init Firebase ─────────────────────────────────────────────────
print(f"  {DIM}Connecting to Firebase...{RST}", end="", flush=True)
try:
    from backend.config.firebase import db
    from backend.config.settings import Roles, ZONE_BASE_INCOME
    print(f" {G}connected ✓{RST}\n")
except Exception as e:
    print(f"\n{R}Cannot connect to Firebase: {e}{RST}")
    sys.exit(1)

# ── Available Zones ───────────────────────────────────────────────
ZONES = [
    "OMR-Chennai",
    "Andheri-Mumbai",
    "Koramangala-Bangalore",
    "Connaught-Delhi",
    "Hitech-Hyderabad",
    "Whitefield-Bangalore",
    "Noida-Delhi",
    "Kolkata-Central",
]
VEHICLES   = ["bike", "scooter", "bicycle", "auto"]
COV_TYPES  = ["comprehensive", "weather", "traffic", "social"]
CONF_LEVELS = ["HIGH", "MEDIUM", "LOW"]


# ══════════════════════════════════════════════════════════════════
# MODULE 1: PREMIUM CALCULATION
# ══════════════════════════════════════════════════════════════════
def module_premium():
    header(1, "PREMIUM CALCULATION ENGINE",
           "Calculate how much a worker pays for their insurance policy")

    print(f"""
  {DIM}The premium engine uses multiple risk factors to price each policy:{RST}
   • Zone risk multiplier   (Mumbai is riskier than Jaipur)
   • Vehicle type factor    (bicycle riders face higher weather risk)
   • Coverage type factor   (comprehensive costs more than single-peril)
   • Duration discount      (longer policies get cheaper daily rates)
   • Claim history surcharge (+5% per past claim)
""")

    section("Enter Policy Parameters")

    hint("Zone examples: OMR-Chennai, Andheri-Mumbai, Koramangala-Bangalore, Connaught-Delhi")
    for i, z in enumerate(ZONES, 1):
        print(f"    {DIM}{i}. {z}{RST}")
    zone_idx = ask_int("Pick a zone (1–8)", default=1, min_val=1, max_val=8)
    zone = ZONES[zone_idx - 1]

    hint("comprehensive = all risks | weather / traffic / social = single peril")
    cov_type = ask("Coverage type", default="comprehensive", valid_options=COV_TYPES)

    hint("Minimum 1 day, maximum 365 days. Discounts apply at 60, 90, 180+ days")
    cov_days = ask_int("Coverage days", default=30, min_val=1, max_val=365)

    hint("The maximum payout you'll receive. Minimum ₹1,000 — Maximum ₹5,00,000")
    sum_insured = ask_float("Sum insured (₹)", default=30000, min_val=1000, max_val=500000)

    hint("Bicycle riders face more weather exposure → higher premium")
    vehicle = ask("Vehicle type", default="bike", valid_options=VEHICLES)

    hint("Every past claim adds 5% surcharge (max 25%)")
    past_claims = ask_int("Past claims (worker history)", default=0, min_val=0, max_val=10)

    # Calculate
    from backend.services.policy_service import calculate_premium
    r = calculate_premium(
        zone=zone, coverage_type=cov_type, coverage_days=cov_days,
        sum_insured=sum_insured, vehicle_type=vehicle, worker_claim_history=past_claims
    )

    section("📊 Premium Calculation Result")
    print()
    result("Zone",              zone)
    result("Coverage Type",     cov_type)
    result("Coverage Days",     f"{cov_days} days")
    result("Sum Insured",       f"₹{sum_insured:,.0f}")
    result("Vehicle",           vehicle)
    result("Past Claims",       past_claims)
    print(f"  {DIM}{'─'*50}{RST}")
    result("Zone Risk Multiplier", f"{r['zone_multiplier']}×")
    result("Vehicle Factor",       f"{r['vehicle_factor']}×")
    result("Coverage Factor",      f"{r['coverage_factor']}×")
    result("Risk Score",           f"{r['risk_score']} / 1.0")
    print(f"  {DIM}{'─'*50}{RST}")
    result("💰 TOTAL PREMIUM",  f"₹{r['premium']:,.2f}", color=G)
    result("📅 Daily Rate",     f"₹{r['daily_rate']:,.2f} / day", color=C)

    # Show how duration affects price
    print(f"\n  {DIM}Duration sensitivity (same zone/vehicle/sum):{RST}")
    print(f"  {DIM}{'Days':>6} {'Premium':>12} {'Daily Rate':>12} {'Discount':>10}{RST}")
    for d in [7, 30, 60, 90, 180]:
        rd = calculate_premium(zone=zone, coverage_type=cov_type, coverage_days=d,
                               sum_insured=sum_insured, vehicle_type=vehicle)
        discount = {7: "0%", 30: "0%", 60: "4%", 90: "8%", 180: "15%"}[d]
        marker = f" {G}← your choice{RST}" if d == cov_days else ""
        print(f"  {DIM}{d:>6}d{RST}  {W}₹{rd['premium']:>10,.2f}{RST}  {DIM}₹{rd['daily_rate']:>10,.2f}/d  {discount:>9}{RST}{marker}")

    ok("Premium calculation complete!")


# ══════════════════════════════════════════════════════════════════
# MODULE 2: CLAIM DECISION ENGINE
# ══════════════════════════════════════════════════════════════════
def module_claim_decision():
    header(2, "CLAIM DECISION ENGINE",
           "Enter disruption scores. The engine decides if a claim is triggered.")

    print(f"""
  {DIM}The decision engine fuses 3 real-time signals into one score:{RST}

      fused_score = 0.35 × weather + 0.25 × traffic + 0.25 × social

  {DIM}Trigger conditions:{RST}
   • fused ≥ 0.6              → {G}TRIGGERED{RST} (HIGH confidence)
   • Any single score ≥ 0.7   → {G}TRIGGERED{RST}
   • fused ≥ 0.4 + 2 signals ≥ 0.3 → {G}TRIGGERED{RST} (MEDIUM confidence)
   • Otherwise                → {R}NO CLAIM{RST}
""")

    section("Enter Signal Scores (0.0 = calm, 1.0 = extreme disruption)")

    print(f"""
  {DIM}Score guide:{RST}
    0.0 – 0.2   → Calm, business as usual
    0.3 – 0.4   → Moderate disruption
    0.5 – 0.6   → Significant disruption
    0.7 – 0.9   → Severe disruption
    1.0         → Extreme / catastrophic
""")

    hint("🌧️  Weather: rain intensity, flooding, storm risk")
    w = ask_float("Weather score", default=0.75, min_val=0.0, max_val=1.0)

    hint("🚗  Traffic: congestion level, road blocks, accidents")
    t = ask_float("Traffic score", default=0.55, min_val=0.0, max_val=1.0)

    hint("📢  Social: bandh, protest, curfew, hartals")
    s = ask_float("Social score", default=0.40, min_val=0.0, max_val=1.0)

    from backend.services.claim_service import make_claim_decision
    r = make_claim_decision(w, t, s)

    section("⚡ Claim Decision Result")
    print()

    fused_color = G if r['fused_score'] >= 0.6 else Y if r['fused_score'] >= 0.4 else R
    trig_str  = f"{G}✅ YES — CLAIM TRIGGERED{RST}" if r['claim_triggered'] else f"{R}❌ NO — No Claim{RST}"
    conf_color = G if r['confidence'] == 'HIGH' else Y if r['confidence'] == 'MEDIUM' else R

    print(f"  {DIM}Input scores:{RST}  {C}W={w:.2f}  T={t:.2f}  S={s:.2f}{RST}")
    result("Fused Score",      f"{r['fused_score']:.3f}", color=fused_color)
    result("Trigger Decision", "", color=W)
    print(f"        {trig_str}")
    result("Confidence",       r['confidence'], color=conf_color)
    result("Primary Cause",    r['primary_cause'])
    result("Action",           r['recommended_action'])
    result("Reasoning Source", r['reasoning_source'])
    print(f"\n  {DIM}Explanation:{RST}")
    print(f"  {W}{r['explanation']}{RST}")

    # Show sensitivity table
    print(f"\n  {DIM}How different score combinations behave:{RST}")
    print(f"  {DIM}{'W':>5} {'T':>5} {'S':>5} → {'Fused':>7} {'Triggered?':>12} {'Conf'}{RST}")
    examples = [
        (0.9, 0.8, 0.7), (0.7, 0.6, 0.5), (0.6, 0.5, 0.4),
        (0.5, 0.4, 0.3), (0.3, 0.3, 0.3), (0.1, 0.1, 0.1),
    ]
    for ew, et, es in examples:
        er = make_claim_decision(ew, et, es)
        tmark = f"{G}✅ YES{RST}" if er['claim_triggered'] else f"{R} NO {RST}"
        cc = G if er['confidence'] == 'HIGH' else Y if er['confidence'] == 'MEDIUM' else R
        marker = f" {Y}← your input{RST}" if (ew, et, es) == (w, t, s) else ""
        print(f"  {DIM}{ew:>5.2f}{et:>6.2f}{es:>6.2f} → {RST}{C}{er['fused_score']:>7.3f}{RST}  {tmark}  {cc}{er['confidence']}{RST}{marker}")

    ok("Decision engine complete!")


# ══════════════════════════════════════════════════════════════════
# MODULE 3: FRAUD DETECTION ENGINE
# ══════════════════════════════════════════════════════════════════
def module_fraud():
    header(3, "FRAUD DETECTION ENGINE",
           "Enter GPS coordinates and server status. The engine detects fraud.")

    print(f"""
  {DIM}4-layer fraud detection on every claim:{RST}
   Layer 1 — GPS Validation     → Is the worker where they claim to be?
   Layer 2 — Multi-server       → Did ≥2/3 MCP servers agree?
   Layer 3 — Score Divergence   → Are scores wildly inconsistent?
   Layer 4 — Anomaly            → All zeros = suspicious

  {DIM}Fraud Score → Verdict:{RST}
   0.00 – 0.19  → {G}CLEAN{RST}
   0.20 – 0.49  → {Y}SUSPICIOUS{RST}  (sent to admin review)
   0.50+        → {R}FRAUDULENT{RST}  (claim flagged)
""")

    section("Worker's Registered GPS Location")

    hint("This comes from the worker's registered zone when they signed up.")
    hint("Example — Chennai OMR area: lat=12.960, lon=80.249")
    worker_lat = ask_float("Worker registered latitude", default=12.960, min_val=-90, max_val=90)
    worker_lon = ask_float("Worker registered longitude", default=80.249, min_val=-180, max_val=180)

    section("Claim GPS Location (where they say the disruption happened)")

    print(f"""
  {DIM}Try these scenarios to see different outcomes:{RST}
   ✅ Nearby (clean):     lat=12.962, lon=80.251  →  ~0.3km away
   ⚠️  Warning (16km):    lat=13.105, lon=80.249  →  ~16km away
   🚨 Fraud (18km+):     lat=13.122, lon=80.249  →  ~18km away
   🚨 Different city:    lat=28.631, lon=77.217  →  Delhi (1700km away!)
""")

    claim_lat = ask_float("Claim latitude", default=12.962, min_val=-90, max_val=90)
    claim_lon = ask_float("Claim longitude", default=80.251, min_val=-180, max_val=180)

    section("MCP Server Status")

    hint("Simulates whether our 3 signal servers (Weather/Traffic/Social) responded.")
    hint("Enter how many servers responded: 3 = all OK, 1 = mostly offline")
    servers_ok = ask_int("How many MCP servers responded (0–3)?", default=3, min_val=0, max_val=3)

    section("Disruption Scores (from MCP servers)")

    hint("These are the same 0–1 scores as in the Decision Engine")
    w = ask_float("Weather score", default=0.7, min_val=0.0, max_val=1.0)
    t = ask_float("Traffic score", default=0.5, min_val=0.0, max_val=1.0)
    s = ask_float("Social score",  default=0.4, min_val=0.0, max_val=1.0)

    # Build signal dict
    signals = {
        "weather": {"status": "ok" if servers_ok >= 1 else "error", "data": {}},
        "traffic": {"status": "ok" if servers_ok >= 2 else "error", "data": {}},
        "social":  {"status": "ok" if servers_ok >= 3 else "error", "data": {}},
    }

    from backend.services.claim_service import run_fraud_checks
    result_data = run_fraud_checks(
        lat=claim_lat, lon=claim_lon,
        worker_lat=worker_lat, worker_lon=worker_lon,
        w=w, t=t, s=s,
        signals=signals,
    )

    # Compute actual distance for display
    import math
    R_earth = 6371
    dlat = math.radians(claim_lat - worker_lat)
    dlon = math.radians(claim_lon - worker_lon)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(worker_lat)) *
         math.cos(math.radians(claim_lat)) *
         math.sin(dlon / 2) ** 2)
    distance = R_earth * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    section("🔍 Fraud Detection Result")
    print()

    verdict = result_data['verdict']
    vc = G if verdict == 'clean' else Y if verdict == 'suspicious' else R
    vmark = {"clean": "✅ CLEAN", "suspicious": "⚠️  SUSPICIOUS", "fraudulent": "🚨 FRAUDULENT"}[verdict]

    result("GPS Distance",        f"{distance:.1f} km from registered zone")
    result("GPS Valid",            "✅ Yes" if result_data['gps_valid'] else "❌ No (too far!)")
    result("Servers Up",           f"{servers_ok}/3 MCP servers responded")
    result("Multi-server Valid",   "✅ Yes" if result_data['multi_server_agreement'] else "❌ No")
    print(f"  {DIM}{'─'*50}{RST}")
    result("Fraud Score",          f"{result_data['fraud_score']:.3f} / 1.000", color=vc)
    print(f"  {vc}Verdict:{RST}  {W}{vmark}{RST}")

    if result_data['flags']:
        print(f"\n  {Y}⚠️  Flags raised:{RST}")
        for flag in result_data['flags']:
            warn(flag)
    else:
        ok("No fraud flags — claim passes all checks")

    print(f"\n  {DIM}Fraud score breakdown:{RST}")
    print(f"  {DIM}GPS >25km      → +0.35  |  GPS 15-25km  → +0.10{RST}")
    print(f"  {DIM}<2 servers     → +0.20  |  Score anomaly → +0.40{RST}")
    print(f"  {DIM}Divergence     → +0.15  |  (capped at 1.0){RST}")

    ok("Fraud detection complete!")


# ══════════════════════════════════════════════════════════════════
# MODULE 4: PAYOUT ESTIMATION ENGINE
# ══════════════════════════════════════════════════════════════════
def module_payout():
    header(4, "PAYOUT ESTIMATION ENGINE",
           "Calculate how much a worker gets paid after a successful claim")

    print(f"""
  {DIM}Payout Formula:{RST}
      disruption_intensity = 0.35×W + 0.25×T + 0.25×S
      income_loss_ratio    = disruption × confidence_mult
      income_loss          = base_income × income_loss_ratio
      payout_amount        = income_loss × 80%  (capped at sum_insured)

  {DIM}Base Daily Income by City:{RST}
    Mumbai=₹1,400  Delhi=₹1,300  Bangalore=₹1,250
    Hyderabad=₹1,100  Chennai=₹1,000  Kolkata=₹950
""")

    section("Select Zone")

    for i, z in enumerate(ZONES, 1):
        city = z.split("-")[0]
        income = 1000
        for k, v in ZONE_BASE_INCOME.items():
            if k in z.lower():
                income = v
                break
        print(f"    {DIM}{i}. {z}  (base income ₹{income:,}/day){RST}")

    z_idx = ask_int("Pick zone (1–8)", default=3, min_val=1, max_val=8)
    zone = ZONES[z_idx - 1]

    section("Enter Disruption Scores")

    w = ask_float("Weather score", default=0.75, min_val=0.0, max_val=1.0)
    t = ask_float("Traffic score", default=0.55, min_val=0.0, max_val=1.0)
    s = ask_float("Social score",  default=0.40, min_val=0.0, max_val=1.0)

    hint("Confidence comes from the Decision Engine (HIGH/MEDIUM/LOW)")
    conf = ask("Confidence level", default="HIGH", valid_options=CONF_LEVELS)

    hint("If set, payout is capped (cannot exceed your sum insured). Leave 0 to skip cap.")
    sum_insured_input = ask_float("Sum insured cap (₹, 0 = no cap)", default=0, min_val=0, max_val=500000)
    sum_insured = sum_insured_input if sum_insured_input > 0 else None

    from backend.services.claim_service import estimate_payout
    r = estimate_payout(zone=zone, w=w, t=t, s=s, confidence=conf,
                        sum_insured=sum_insured)

    section("💸 Payout Estimation Result")
    print()

    conf_color = G if conf == "HIGH" else Y if conf == "MEDIUM" else R
    conf_mult  = {"HIGH": 1.0, "MEDIUM": 0.75, "LOW": 0.5}[conf]
    city = zone.split("-")[0]

    result("Zone",                  zone)
    result("City Base Income",      f"₹{r['base_daily_income']:,} / day")
    result("Disruption Intensity",  f"{r['disruption_intensity']:.3f}")
    result("Confidence Level",      conf, color=conf_color)
    result("Confidence Multiplier", f"{conf_mult}×")
    print(f"  {DIM}{'─'*50}{RST}")
    result("Income Without Disruption", f"₹{r['base_daily_income']:,}")
    result("Income Loss",               f"₹{r['income_loss']:,.2f}")
    result("Coverage Rate",             f"80%")
    if sum_insured:
        result("Sum Insured Cap",       f"₹{sum_insured:,.0f}")
    print(f"  {DIM}{'─'*50}{RST}")
    result("💸 PAYOUT AMOUNT", f"₹{r['payout_amount']:,.2f}", color=G)

    # Show effect of confidence
    print(f"\n  {DIM}Effect of confidence on payout (same zone + scores):{RST}")
    print(f"  {DIM}{'Confidence':>12} {'Multiplier':>12} {'Payout':>12}{RST}")
    for cl in ["HIGH", "MEDIUM", "LOW"]:
        rc = estimate_payout(zone=zone, w=w, t=t, s=s, confidence=cl)
        cm_mult = {"HIGH": 1.0, "MEDIUM": 0.75, "LOW": 0.5}[cl]
        cm = {"HIGH": G, "MEDIUM": Y, "LOW": R}[cl]
        marker = f" {Y}← your choice{RST}" if cl == conf else ""
        print(f"  {cm}{cl:>12}{RST}  {DIM}{cm_mult:>11}×{RST}  {W}₹{rc['payout_amount']:>10,.2f}{RST}{marker}")

    ok("Payout estimation complete!")


# ══════════════════════════════════════════════════════════════════
# MODULE 5: FULL CLAIM PIPELINE
# ══════════════════════════════════════════════════════════════════
def module_full_pipeline():
    header(5, "FULL CLAIM PIPELINE",
           "Decision + Fraud + Payout — all combined, result saved to Firestore")

    print(f"""
  {DIM}This simulates the complete /claims/trigger pipeline:{RST}
    1. Policy validation         → is the policy active?
    2. Signal collection         → weather/traffic/social scores
    3. Claim decision engine     → triggered? confidence?
    4. Fraud detection           → GPS + multi-server + anomaly
    5. Payout estimation         → zone-based income × disruption
    6. Status determination      → approved / pending / flagged / rejected
    7. Write to Firestore        → claim document stored
""")

    section("Worker Identity (using seeded demo workers)")

    print(f"""
  {DIM}Seeded demo workers in the system:{RST}
   1. worker_rahul     Zone: OMR-Chennai         GPS: 12.9602, 80.2495
   2. worker_priya     Zone: Andheri-Mumbai      GPS: 19.1176, 72.8462
   3. worker_amit      Zone: Koramangala-Bangalore GPS: 12.9352, 77.6245
   4. worker_sneha     Zone: Hitech-Hyderabad    GPS: 17.4435, 78.3772
   5. worker_vikram    Zone: Connaught-Delhi      GPS: 28.6315, 77.2167
   6. Custom UID       (type your own)
""")

    worker_map = {
        "1": ("worker_rahul",  "OMR-Chennai",            12.9602, 80.2495),
        "2": ("worker_priya",  "Andheri-Mumbai",          19.1176, 72.8462),
        "3": ("worker_amit",   "Koramangala-Bangalore",   12.9352, 77.6245),
        "4": ("worker_sneha",  "Hitech-Hyderabad",        17.4435, 78.3772),
        "5": ("worker_vikram", "Connaught-Delhi",         28.6315, 77.2167),
    }

    w_choice = ask("Choose worker (1–5, or type UID)", default="3",
                   valid_options=["1","2","3","4","5","6"])

    if w_choice in worker_map:
        worker_uid, zone, wlat, wlon = worker_map[w_choice]
        show("Worker UID", worker_uid)
        show("Zone",       zone)
    else:
        worker_uid = ask("Enter worker UID", default="worker_amit")
        zone_idx = ask_int("Pick zone (1–8)", default=3, min_val=1, max_val=8)
        zone = ZONES[zone_idx - 1]
        wlat = ask_float("Worker GPS latitude", default=12.9352, min_val=-90, max_val=90)
        wlon = ask_float("Worker GPS longitude", default=77.6245, min_val=-180, max_val=180)

    section("Claim Location GPS")

    hint("Enter where the disruption happened.")
    hint(f"Worker is registered at lat={wlat}, lon={wlon}")
    hint("To simulate GPS fraud, enter coords far from the above location.")
    claim_lat = ask_float("Claim latitude", default=round(wlat + 0.002, 4), min_val=-90, max_val=90)
    claim_lon = ask_float("Claim longitude", default=round(wlon + 0.002, 4), min_val=-180, max_val=180)

    section("Disruption Scores")

    hint("In production, these come from the 3 MCP servers automatically.")
    hint("Try high values (0.7–0.9) to trigger a claim, low (0.1–0.2) to reject.")
    w_score = ask_float("Weather score (0–1)", default=0.75, min_val=0.0, max_val=1.0)
    t_score = ask_float("Traffic score (0–1)", default=0.55, min_val=0.0, max_val=1.0)
    s_score = ask_float("Social score  (0–1)", default=0.40, min_val=0.0, max_val=1.0)

    servers_ok = ask_int("MCP servers responded (0–3)", default=3, min_val=0, max_val=3)

    hint("Sum insured affects the payout cap")
    sum_insured = ask_float("Policy sum insured (₹)", default=35000, min_val=1000, max_val=500000)

    print(f"\n  {DIM}Running full pipeline...{RST}")

    # Run pipeline
    from backend.services.claim_service import (
        make_claim_decision, run_fraud_checks, estimate_payout
    )

    signals_sim = {
        "weather": {"status": "ok" if servers_ok >= 1 else "error", "data": {}},
        "traffic": {"status": "ok" if servers_ok >= 2 else "error", "data": {}},
        "social":  {"status": "ok" if servers_ok >= 3 else "error", "data": {}},
    }

    decision  = make_claim_decision(w_score, t_score, s_score)
    fraud     = run_fraud_checks(
        lat=claim_lat, lon=claim_lon,
        worker_lat=wlat, worker_lon=wlon,
        w=w_score, t=t_score, s=s_score,
        signals=signals_sim,
    )
    payout_info = {}
    if decision["claim_triggered"]:
        payout_info = estimate_payout(
            zone=zone, w=w_score, t=t_score, s=s_score,
            confidence=decision["confidence"],
            sum_insured=sum_insured,
        )

    # Determine status
    if fraud["verdict"] == "fraudulent":
        final_status = "flagged"
    elif decision["claim_triggered"] and decision["confidence"] == "HIGH" and fraud["verdict"] == "clean":
        final_status = "approved"
    elif decision["claim_triggered"]:
        final_status = "pending"
    else:
        final_status = "rejected"

    # Build claim doc
    claim_id = f"clm_manual_{uuid.uuid4().hex[:8]}"
    now_ts   = datetime.now(timezone.utc)

    claim_doc = {
        "claim_id":            claim_id,
        "worker_id":           worker_uid,
        "zone":                zone,
        "lat":                 claim_lat, "lon": claim_lon,
        "notes":               "Manual walkthrough test claim",
        "weather_score":       w_score,
        "traffic_score":       t_score,
        "social_score":        s_score,
        "claim_triggered":     decision["claim_triggered"],
        "confidence":          decision["confidence"],
        "primary_cause":       decision["primary_cause"],
        "explanation":         decision["explanation"],
        "recommended_action":  decision["recommended_action"],
        "reasoning_source":    decision["reasoning_source"],
        "fused_score":         decision["fused_score"],
        "payout_amount":       payout_info.get("payout_amount"),
        "disruption_intensity":payout_info.get("disruption_intensity"),
        "base_daily_income":   payout_info.get("base_daily_income"),
        "fraud_check":         fraud,
        "status":              final_status,
        "triggered_by":        worker_uid,
        "reviewed_by":         None,
        "policy_id":           "manual_test",
        "created_at":          now_ts.isoformat(),
        "updated_at":          now_ts.isoformat(),
    }

    # Save to Firestore
    db.collection("claims").document(claim_id).set(claim_doc)

    section("🔗 Full Pipeline Result")
    print()

    status_colors = {
        "approved": G, "pending": Y, "rejected": R, "flagged": R
    }
    status_marks = {
        "approved": "✅ AUTO-APPROVED",
        "pending":  "🕐 PENDING REVIEW",
        "rejected": "❌ REJECTED",
        "flagged":  "🚨 FLAGGED (Fraud)"
    }

    sc = status_colors.get(final_status, W)
    sm = status_marks.get(final_status, final_status)

    result("Claim ID",      claim_id)
    result("Worker",        worker_uid)
    result("Zone",          zone)
    print(f"  {DIM}Scores:{RST}  {C}W={w_score:.2f}  T={t_score:.2f}  S={s_score:.2f}  Fused={decision['fused_score']:.3f}{RST}")
    print(f"  {DIM}{'─'*54}{RST}")

    trig = G if decision['claim_triggered'] else R
    cc   = G if decision['confidence'] == 'HIGH' else Y if decision['confidence'] == 'MEDIUM' else R
    vc   = G if fraud['verdict'] == 'clean' else Y if fraud['verdict'] == 'suspicious' else R

    result("Claim Triggered",  f"{'YES' if decision['claim_triggered'] else 'NO'}", color=trig)
    result("Confidence",       decision['confidence'], color=cc)
    result("Primary Cause",    decision['primary_cause'])
    result("Fraud Verdict",    fraud['verdict'].upper(), color=vc)
    result("Fraud Score",      f"{fraud['fraud_score']:.3f}")

    if payout_info:
        result("Payout Amount", f"₹{payout_info.get('payout_amount', 0):,.2f}", color=G)
    else:
        result("Payout Amount", "₹0  (claim not triggered)", color=R)

    print(f"  {DIM}{'─'*54}{RST}")
    print(f"\n  {sc}🏷️  FINAL STATUS:  {sm}{RST}")
    print(f"\n  {DIM}Explanation:{RST}")
    print(f"  {W}{decision['explanation']}{RST}")

    if fraud['flags']:
        print(f"\n  {Y}⚠️  Fraud Flags:{RST}")
        for flag in fraud['flags']:
            warn(flag)

    print(f"\n  {DIM}Claim saved to Firestore → claims/{claim_id}{RST}")
    ok("Full pipeline complete! Claim saved.")

    # Offer to delete
    print(f"\n  {Y}Delete this test claim from Firestore?{RST}")
    del_choice = ask("Delete claim? (y/n)", default="y", valid_options=["y", "n"])
    if del_choice == "y":
        db.collection("claims").document(claim_id).delete()
        ok("Test claim deleted from Firestore.")
    else:
        info(f"Claim preserved: claims/{claim_id}")


# ══════════════════════════════════════════════════════════════════
# MODULE 6: WORKER REGISTRATION
# ══════════════════════════════════════════════════════════════════
def module_register_worker():
    header(6, "WORKER REGISTRATION",
           "Create a new worker profile in Firestore (simulating POST /workers/register)")

    print(f"""
  {DIM}When a worker registers, TWO documents are created in Firestore:{RST}
    • users/{{uid}}    → auth profile (email, role, name)
    • workers/{{uid}}  → worker profile (zone, vehicle, GPS, stats)

  {DIM}In production, the Firebase UID comes from the ID token.{RST}
  {DIM}Here we let you specify all values directly.{RST}
""")

    section("Enter Worker Details")

    hint("UID will be auto-generated as 'manual_{random}' — you can customize it")
    uid_suffix = uuid.uuid4().hex[:8]
    uid = ask("Worker UID", default=f"manual_{uid_suffix}")

    hint("Use a realistic name to make the demo clear")
    name = ask("Display name", default="Arjun Mehta")

    hint("Format: +91XXXXXXXXXX")
    phone = ask("Phone number", default="+919876543210")

    hint("Which city/area does this worker operate in?")
    for i, z in enumerate(ZONES, 1):
        print(f"    {DIM}{i}. {z}{RST}")
    z_idx = ask_int("Pick zone (1–8)", default=1, min_val=1, max_val=8)
    zone = ZONES[z_idx - 1]

    hint("What vehicle does the worker use for deliveries?")
    vehicle = ask("Vehicle type", default="bike", valid_options=VEHICLES)

    hint("Worker's current/home GPS coordinates")
    hint("Example for Chennai OMR: lat=12.962, lon=80.251")
    gps_lat = ask_float("GPS latitude", default=12.962, min_val=-90, max_val=90)
    gps_lon = ask_float("GPS longitude", default=80.251, min_val=-180, max_val=180)

    now = datetime.now(timezone.utc).isoformat()

    # Build and write docs
    user_doc = {
        "uid": uid, "email": f"{uid}@demo.drizzle.io",
        "display_name": name, "role": "worker",
        "is_active": True, "created_at": now, "updated_at": now,
    }
    worker_doc = {
        "uid": uid, "email": f"{uid}@demo.drizzle.io",
        "display_name": name, "phone": phone,
        "zone": zone, "vehicle_type": vehicle,
        "gps_lat": gps_lat, "gps_lon": gps_lon,
        "role": "worker", "is_active": True,
        "total_claims": 0, "total_payouts": 0.0,
        "created_at": now, "updated_at": now,
    }

    db.collection("users").document(uid).set(user_doc)
    db.collection("workers").document(uid).set(worker_doc)

    section("👷 Registration Result")
    print()
    ok(f"Worker registered! UID = {uid}")
    show("Display Name", name)
    show("Email",        f"{uid}@demo.drizzle.io")
    show("Phone",        phone)
    show("Zone",         zone)
    show("Vehicle",      vehicle)
    show("GPS",          f"{gps_lat}, {gps_lon}")
    show("Role",         "worker")
    show("Status",       "active")
    show("Firestore",    f"users/{uid} + workers/{uid}")

    print(f"\n  {Y}Delete this test worker?{RST}")
    del_choice = ask("Delete? (y/n)", default="y", valid_options=["y", "n"])
    if del_choice == "y":
        db.collection("users").document(uid).delete()
        db.collection("workers").document(uid).delete()
        ok("Test worker deleted.")
    else:
        info(f"Worker preserved: workers/{uid}")


# ══════════════════════════════════════════════════════════════════
# MODULE 7: LIVE DASHBOARD
# ══════════════════════════════════════════════════════════════════
def module_dashboard():
    header(7, "LIVE DASHBOARD STATS",
           "Pulls real data from Firestore — exactly what each role sees")

    print(f"""
  {DIM}Three dashboard levels:{RST}
   👷 Worker Dashboard    → Personal stats only (policies, claims, payouts)
   🛡️  Admin Dashboard    → Platform-wide aggregations + zone breakdown
   👑 Super Admin        → Everything + user role distribution
""")

    dash_choice = menu({
        "worker":      "👷  Worker Dashboard   — personal stats",
        "admin":       "🛡️   Admin Dashboard    — platform-wide stats",
        "superadmin":  "👑  Super Admin        — role distribution + system health",
    })

    if dash_choice == "worker":
        section("Select Worker to View")

        workers_docs = list(db.collection("workers").limit(10).stream())
        print(f"\n  {DIM}Available workers in Firestore:{RST}")
        uid_list = []
        for i, wd in enumerate(workers_docs, 1):
            d = wd.to_dict()
            print(f"    {DIM}{i}. {d.get('display_name','?'):25} zone={d.get('zone','?')}{RST}")
            uid_list.append(wd.id)

        w_idx = ask_int(f"Pick worker (1–{len(uid_list)})", default=1, min_val=1, max_val=len(uid_list))
        selected_uid = uid_list[w_idx - 1]

        from backend.services.dashboard_service import get_worker_dashboard
        dash = run(get_worker_dashboard(selected_uid))

        wi = dash.get("worker", {})
        pi = dash.get("policies", {})
        ci = dash.get("claims", {})

        print()
        print(f"  {W}👷 WORKER PROFILE{RST}")
        show("  Name",    wi.get("display_name", "N/A"))
        show("  Zone",    wi.get("zone", "N/A"))
        show("  Vehicle", wi.get("vehicle_type", "N/A"))
        show("  Phone",   wi.get("phone", "N/A"))

        print(f"\n  {W}📄 POLICIES{RST}")
        show("  Total Policies",  pi.get("total", 0))
        show("  Active",          pi.get("active", 0))
        show("  Total Coverage",  f"₹{pi.get('coverage', 0):,.0f}")
        show("  Premium Paid",    f"₹{pi.get('premium', 0):,.2f}")

        print(f"\n  {W}⚡ CLAIMS{RST}")
        show("  Total Claims",   ci.get("total", 0))
        show("  Pending",        ci.get("pending", 0))
        show("  Approved",       ci.get("approved", 0))
        show("  Total Payout",   f"₹{ci.get('total_payout', 0):,.2f}")

    elif dash_choice == "admin":
        from backend.services.dashboard_service import get_dashboard_stats
        stats = run(get_dashboard_stats())
        ov = stats.get("overview", {})

        print(f"\n  {W}👥 USERS & WORKERS{RST}")
        show("  Total Workers",  ov.get("total_workers", 0))
        show("  Active Workers", ov.get("active_workers", 0))

        print(f"\n  {W}📄 POLICIES{RST}")
        show("  Total",              ov.get("total_policies", 0))
        show("  Active",             ov.get("active_policies", 0))
        show("  Premium Collected",  f"₹{ov.get('total_premium_collected', 0):,.2f}")

        print(f"\n  {W}⚡ CLAIMS{RST}")
        show("  Total",       ov.get("total_claims", 0))
        show("  Pending",     ov.get("pending_claims", 0))
        show("  Approved",    ov.get("approved_claims", 0))
        show("  Rejected",    ov.get("rejected_claims", 0))
        show("  Flagged",     ov.get("flagged_claims", 0))
        show("  Payout",      f"₹{ov.get('total_payout', 0):,.2f}")
        show("  Avg Fraud",   ov.get("avg_fraud_score", 0))
        show("  Loss Ratio",  f"{ov.get('loss_ratio', 0):.1%}")

        print(f"\n  {W}🌍 ZONE BREAKDOWN{RST}")
        for zone, zs in stats.get("zone_breakdown", {}).items():
            print(f"  {C}●{RST}  {zone:<32} {DIM}policies={zs['policies']}  premium=₹{zs['premium']:,.0f}{RST}")

    else:
        from backend.services.dashboard_service import get_dashboard_stats
        stats = run(get_dashboard_stats())
        ov    = stats.get("overview", {})

        print(f"\n  {W}📊 PLATFORM SUMMARY{RST}")
        show("  Workers",   ov.get("total_workers", 0))
        show("  Policies",  ov.get("total_policies", 0))
        show("  Claims",    ov.get("total_claims", 0))
        show("  Payout",    f"₹{ov.get('total_payout', 0):,.2f}")
        show("  Loss Ratio",f"{ov.get('loss_ratio', 0):.1%}")

        all_users = list(db.collection("users").stream())
        role_dist = {}
        for u in all_users:
            r = u.to_dict().get("role", "unknown")
            role_dist[r] = role_dist.get(r, 0) + 1

        print(f"\n  {W}👑 USER ROLE DISTRIBUTION (Total: {len(all_users)}){RST}")
        for role, count in sorted(role_dist.items()):
            emoji  = {"worker":"👷","admin":"🛡️","super_admin":"👑"}.get(role, "❓")
            bar    = "█" * count
            color  = {"worker":C,"admin":Y,"super_admin":M}.get(role, W)
            print(f"  {emoji}  {color}{role:15}{RST}  {W}{bar}{RST} {DIM}({count}){RST}")

        all_claims = list(db.collection("claims").stream())
        status_dist = {}
        for c in all_claims:
            st = c.to_dict().get("status","?")
            status_dist[st] = status_dist.get(st, 0) + 1

        print(f"\n  {W}📋 CLAIM STATUS DISTRIBUTION{RST}")
        emojis = {"approved":"🟢","pending":"🟡","flagged":"🔴","rejected":"⚫"}
        for st, count in sorted(status_dist.items()):
            print(f"  {emojis.get(st,'⚪')}  {st:12}  {W}{'█'*count}{RST} {DIM}({count}){RST}")

    ok("Dashboard loaded from live Firestore!")


# ══════════════════════════════════════════════════════════════════
# MAIN LOOP
# ══════════════════════════════════════════════════════════════════

MODULES = {
    "1": ("💰  Premium Calculation Engine", module_premium),
    "2": ("⚡  Claim Decision Engine",       module_claim_decision),
    "3": ("🔍  Fraud Detection Engine",      module_fraud),
    "4": ("💸  Payout Estimation Engine",    module_payout),
    "5": ("🔗  Full Claim Pipeline",         module_full_pipeline),
    "6": ("👷  Worker Registration",         module_register_worker),
    "7": ("📊  Live Dashboard Stats",        module_dashboard),
}

while True:
    divider()
    print(f"\n{W}  SELECT A MODULE TO EXPLORE:{RST}\n")
    for k, (label, _) in MODULES.items():
        print(f"  {C}{k}.{RST}  {label}")
    print(f"  {C}8.{RST}  🔄  Run All Modules in Sequence")
    print(f"  {C}9.{RST}  🚪  Exit\n")

    choice = input(f"  {C}❯  Enter module number: {RST}").strip()

    if choice == "9":
        divider()
        print(f"\n{G}  Thanks for exploring Drizzle! 🌧️{RST}\n")
        break
    elif choice == "8":
        for k, (label, fn) in MODULES.items():
            try:
                fn()
                input(f"\n  {Y}⏎  Press ENTER to continue to next module...{RST}")
            except (KeyboardInterrupt, EOFError):
                break
    elif choice in MODULES:
        label, fn = MODULES[choice]
        try:
            fn()
        except KeyboardInterrupt:
            warn("Module interrupted. Returning to menu.")
        except Exception as e:
            err(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
    else:
        warn("Enter a number from 1 to 9.")
