# 🌧️ **Drizzle** – *Income Safety Net for India's Gig Workforce*

<div align="center">
  
  [![Made by Team Void Main()](https://img.shields.io/badge/Team-Void%20Main%20()-blueviolet?style=for-the-badge&logo=python)](https://github.com/your-repo)
  [![GuideWire Hackathon](https://img.shields.io/badge/GuideWire-Hackathon%202024-ff6b35?style=for-the-badge&logo=guidewire)](https://)
  [![Prototype](https://img.shields.io/badge/Status-Prototype-brightgreen?style=for-the-badge)](https://)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)
  
  ### *Because Rain Shouldn't Mean Empty Plates* 🍽️☔
  
  
</div>

---

## 📋 **Table of Contents**
- [The $5B Problem](#-the-5b-problem-nobodys-solving)
- [Our Innovation](#-our-innovation-income-linked-presence)
- [Premium Model](#-premium-model-that-makes-sense)
- [System Architecture](#-system-architecture)
- [User Experience](#-user-experience-flow)
- [Tech Stack](#-tech-stack--innovation)
- [Development Roadmap](#-development-roadmap)
- [Team](#-team-void-main)

---

## 🎯 **The $5B Problem Nobody's Solving**

```mermaid
graph TD
    A[Food Delivery Partner] -->|Works Peak Hours| B[6PM-10PM Daily]
    B --> C{Disruption Hits}
    C -->|Rain/Flood| D[❌ Can't Deliver]
    C -->|High AQI| E[⚠️ Reduced Hours]
    C -->|Curfew| F[🚫 No Movement]
    C -->|App Outage| G[📱 Zero Orders]
    
    D --> H[📉 Immediate Income Loss]
    E --> H
    F --> H
    G --> H
    
    H --> I[💔 No Compensation Today]
    I --> J[🤕 Worker Bears All Risk]
    
    style J fill:#ff4444,stroke:#333,stroke-width:4px,color:white
    style H fill:#ff6b6b,stroke:#333,stroke-width:2px
    style C fill:#f9d71c,stroke:#333,stroke-width:2px
    style A fill:#4CAF50,stroke:#333,stroke-width:2px,color:white
    style B fill:#2196F3,stroke:#333,stroke-width:2px,color:white
```
## The Human Cost 😔

| **Metric**      | **Impact**      | **Emotional Toll**               |
| --------------- | --------------- | -------------------------------- |
| Weekly Income   | ₹3,500–₹6,000   | Feeds a family of 4              |
| Peak Hours Lost | 20 hrs/week     | 60% of weekly earnings           |
| Disruption Days | 15–20 days/year | 1 month of lost income           |
| Safety Net      | ❌ ZERO          | Complete financial vulnerability |


## 🌍 Real Disruption Scenarios

| **Disruption**           | **What Happens**                        | **Income Impact**      | **Frequency** |
| ------------------------ | --------------------------------------- | ---------------------- | ------------- |
| 🌧 Heavy Rain / Flooding | Orders drop or deliveries become unsafe | Peak earnings lost     | 8–10× / year  |
| 🌫 High AQI              | Outdoor working hours reduce            | Fewer completed orders | 15–20× / year |
| 🚫 Curfew                | Restricted movement across zones        | Zero deliveries        | 2–3× / year   |
| 📱 App Outage            | No order allocation from platform       | Immediate income stop  | 4–5× / year   |


---

# 🧠 Our Innovation: Income-Linked Presence™

- Traditional parametric insurance: "It's raining, here's money."

- Drizzle: "You lost income because you couldn't work, here's protection."


## The Fraud-Proof Architecture
```mermaid
sequenceDiagram
    participant Rider
    participant Drizzle
    participant WeatherAPI
    participant IncomeValidator
    participant Bank
    
    Note over Rider,Bank: Pre-Disruption Phase
    Rider->>Drizzle: Works in Micro-zone (7-day history)
    Drizzle->>Drizzle: Builds Income Profile
    
    Note over Rider,Bank: Disruption Event
    WeatherAPI->>Drizzle: Heavy Rain Alert 🌧️
    Drizzle->>Drizzle: Geo-fence affected micro-zones
    
    Note over Rider,Bank: Validation Layer (Critical!)
    Drizzle->>IncomeValidator: Check rider presence BEFORE disruption?
    IncomeValidator-->>Drizzle: ✅ Verified (Active in zone last 7 days)
    
    Drizzle->>IncomeValidator: Verify income drop?
    IncomeValidator-->>Drizzle: ✅ 60% reduction verified
    
    Note over Rider,Bank: Automated Payout
    Drizzle->>Bank: ₹1,500 instant transfer
    Bank-->>Rider: 💰 Funds available immediately
    
    Note over Rider,Bank: Fraud Prevention
    Note right of IncomeValidator: Prevents:<br/>• Zone-hopping<br/>• False claims<br/>• Double dipping
```

## How Traditional Models Fail


```mermaid

graph LR
    subgraph "Traditional Model"
    A[Rain in Zone] --> B[Anyone in Zone Gets Paid]
    B --> C[🚫 Fraud: Riders rush to rainy zone]
    end
    
    subgraph "Drizzle Model"
    D[Rain in Zone] --> E[Check Pre-disruption Presence]
    E --> F[Verify Income Drop]
    F --> G[✅ Legitimate Riders Only]
    end
    
    style C fill:#ff4444,color:white
    style G fill:#4CAF50,color:white

```

## 🗺️ Hyperlocal Risk Intelligence


<img width="1450" height="1062" alt="image" src="https://github.com/user-attachments/assets/931e351d-0fcb-4eeb-a772-7dba9d79d6eb" />



### Micro-zone Grid (500m Resolution)

```mermaid
mindmap
  root((Mumbai<br/>Micro-zones))
    🔥 High Risk
      🏢 BKC
        Risk: 85
        Flood: High
        AQI: 320
        💰 Premium: ₹45
      🏞️ POWAI
        Risk: 65
        Flood: High
        💰 Premium: ₹38
      🚂 KURLA
        Risk: 55
        Waterlog: Yes
        💰 Premium: ₹32
    
    🟡 Medium Risk
      🏘️ ANDHERI
        Risk: 45
        Flood: Medium
        AQI: 180
        💰 Premium: ₹28
      🏪 CHEMBUR
        Risk: 40
        AQI: Poor
        💰 Premium: ₹22
      🏥 WADALA
        Risk: 45
        Hospital: Yes
        💰 Premium: ₹28
      🏖️ JUHU
        Risk: 35
        Coastal: Yes
        💰 Premium: ₹22
    
    🟢 Low Risk
      🌉 BANDRA
        Risk: 25
        Flood: Low
        AQI: 120
        💰 Premium: ₹18
      🏭 LOWER PAREL
        Risk: 15
        Flood: None
        AQI: 90
        💰 Premium: ₹15
      🏘️ GHATKOPAR
        Risk: 30
        Status: Stable
        💰 Premium: ₹18
      🎬 GOREGAON
        Risk: 28
        Studio: Metro
        💰 Premium: ₹18
      🏛️ DADAR
        Risk: 22
        Transit: High
        💰 Premium: ₹18




```
```mermaid
flowchart TD
    subgraph Legend
        L1[🔥 High Risk 70-100] --- L2[🟡 Medium Risk 40-69] --- L3[🟢 Low Risk 0-39]
    end

    subgraph "MUMBAI MICRO-ZONE MAP - 500m Grid"
        direction TB
        
        subgraph Row1
            BKC["🏢 BKC<br/><strong>Risk: 85🔥</strong><br/>Flood: High<br/>AQI: 320<br/>💰 ₹45"]
            ANDHERI["🏘️ ANDHERI<br/><strong>Risk: 45🟡</strong><br/>Flood: Med<br/>AQI: 180<br/>💰 ₹28"]
            BANDRA["🌉 BANDRA<br/><strong>Risk: 25🟢</strong><br/>Flood: Low<br/>AQI: 120<br/>💰 ₹18"]
            LOWER_PAREL["🏭 LOWER PAREL<br/><strong>Risk: 15🟢</strong><br/>Flood: None<br/>AQI: 90<br/>💰 ₹15"]
        end
        
        subgraph Row2
            POWAI["🏞️ POWAI<br/><strong>Risk: 65🔥</strong><br/>Flood: High<br/>💰 ₹38"]
            KURLA["🚂 KURLA<br/><strong>Risk: 55🔥</strong><br/>Waterlog: Y<br/>💰 ₹32"]
            CHEMBUR["🏪 CHEMBUR<br/><strong>Risk: 40🟡</strong><br/>AQI: Poor<br/>💰 ₹22"]
            GHATKOPAR["🏘️ GHATKOPAR<br/><strong>Risk: 30🟢</strong><br/>Stable<br/>💰 ₹18"]
        end
        
        subgraph Row3
            JUHU["🏖️ JUHU<br/><strong>Risk: 35🟡</strong><br/>Coastal: Y<br/>💰 ₹22"]
            GOREGAON["🎬 GOREGAON<br/><strong>Risk: 28🟢</strong><br/>Studio: M<br/>💰 ₹18"]
            WADALA["🏥 WADALA<br/><strong>Risk: 45🟡</strong><br/>Hospital: Y<br/>💰 ₹28"]
            DADAR["🏛️ DADAR<br/><strong>Risk: 22🟢</strong><br/>Transit: H<br/>💰 ₹18"]
        end
    end
    
    BKC --- POWAI --- JUHU
    ANDHERI --- KURLA --- GOREGAON
    BANDRA --- CHEMBUR --- WADALA
    LOWER_PAREL --- GHATKOPAR --- DADAR
    
    style BKC fill:#ff4444,color:white
    style POWAI fill:#ff4444,color:white
    style KURLA fill:#ff4444,color:white
    style ANDHERI fill:#ffaa33,color:black
    style CHEMBUR fill:#ffaa33,color:black
    style JUHU fill:#ffaa33,color:black
    style WADALA fill:#ffaa33,color:black
    style BANDRA fill:#4CAF50,color:white
    style LOWER_PAREL fill:#4CAF50,color:white
    style GHATKOPAR fill:#4CAF50,color:white
    style GOREGAON fill:#4CAF50,color:white
    style DADAR fill:#4CAF50,color:white
```
## 💰 Premium Model That Makes Sense
### Weekly Pricing Structure
| **Risk Level** | **Zone Examples**   | **Weekly Premium** | **Coverage Cap** | **Break-even**        | **Adoption Rate** |
| -------------- | ------------------- | ------------------ | ---------------- | --------------------- | ----------------- |
| 🟢 **Low**     | Bandra, Lower Parel | ₹15                | ₹800             | ~1 disruption / year  | 45%               |
| 🟡 **Medium**  | Andheri, Chembur    | ₹28                | ₹1,500           | ~2 disruptions / year | 35%               |
| 🔥 **High**    | BKC, Powai          | ₹45                | ₹2,500           | ~3 disruptions / year | 20%               |

## Real Scenario: Raj's Story

```mermaid
gantt
    title Raj's Week with Drizzle - ₹28 Premium
    dateFormat HH:mm
    axisFormat %H:%M
    
    section Normal Days (Mon-Wed)
    Peak Earnings (6PM-10PM) :mon, 18:00, 4h
    Peak Earnings :tue, 18:00, 4h
    Peak Earnings :wed, 18:00, 4h
    
    section Disruption Day (Thursday)
    Heavy Rain Alert :crit, alert1, 16:00, 2h
    Peak Hours Lost :crit, loss1, 18:00, 4h
    Income Drop Detected :crit, detect, 22:00, 30m
    Claim Auto-initiated :milestone, claim, 22:30, 1m
    Payout Processed :done, payout, 22:31, 1m
    
    section Post-Disruption (Fri-Sat)
    Normal Operations :fri, 18:00, 4h
    Weekend Peak :sat, 18:00, 4h
    
    section Financial Impact
    Premium Paid (Weekly) :premium, 00:00, 1d
    Payout Received :crit, payout_rec, 22:31, 1m
    Net Gain :milestone, gain, 23:00, 1m
```

## 🏗️ System Architecture

![Untitled Diagram (2)](https://github.com/user-attachments/assets/b2f9cb27-b0fd-490e-b232-0fe4b94c86f3)



## 🚨 Adversarial Defense & Anti-Spoofing Strategy

### Simple GPS is obsolete. Multi-modal intelligence is the new standard. ⚡
### Added: March 20, 2026 • 24-Hour Crisis Response

### ⚠️ The Crisis: What We Discovered


```mermaid
graph TD
    subgraph "THE ATTACK VECTOR"
        A[📱 Telegram Syndicate<br/>500+ Bad Actors] --> B[🔄 GPS Spoofing Apps<br/>Fake Location Data]
        B --> C[🏠 Resting Safely at Home<br/>Claiming to be Stranded]
        C --> D[💣 Beta Platform Drained<br/>Liquidity Pool = ZERO]
    end
    
    subgraph "DRIZZLE DEFENSE"
        E[🚨 24-HOUR PIVOT] --> F[🧠 Multi-Layer Anti-Spoofing]
        F --> G[📊 Behavioral • Network • Temporal]
        G --> H[🛡️ DRIZZLE FORTIFIED<br/>Syndicate Proof]
    end
    
    style D fill:#ff4444,color:white
    style E fill:#ffaa33,color:black
    style H fill:#4CAF50,color:white
```

## 🧠 1. The Differentiation: AI/ML Architecture for Genuine vs. Spoofed Locations
### Enhanced Fraud Detection Module

```mermaid
flowchart TD
    subgraph "EXISTING ARCHITECTURE"
        A[Rider App] --> B[API Gateway]
        B --> C[Risk Scoring Engine]
        C --> D[Premium Calculator]
        D --> E[Policy Manager]
        
        B --> F[Claim Engine]
        F --> G[Income Validation]
        G --> H[Fraud Detection]
        H --> I[Payments]
    end
    
    subgraph "🆕 ENHANCED FRAUD DETECTION LAYER"
        J[Incoming Claim] --> K{LAYER 1<br/>Behavioral Biometrics}
        K --> L[Gyroscope • Accelerometer<br/>Battery Drain • Device Angle]
        
        L --> M{LAYER 2<br/>Network Forensics}
        M --> N[Cell Tower Handoffs<br/>WiFi AP Fingerprints • Bluetooth Density]
        
        N --> O{LAYER 3<br/>Historical Context}
        O --> P[7-Day Zone History<br/>Time Patterns • Earnings Density]
        
        P --> Q{LAYER 4<br/>Temporal Correlation}
        Q --> R[Cluster Analysis<br/>Simultaneous Claims • Same Coordinates]
        
        R --> S{ENSEMBLE ML}
        S --> T[✅ GENUINE]
        S --> U[🚫 SPOOFED]
    end
    
    H -.-> J
    T --> I
    U --> V[🛡️ FLAGGED - Manual Review]
    
    style T fill:#4CAF50,color:white
    style U fill:#ff4444,color:white
    style V fill:#ffaa33,color:black
```


## 🧠 Signal-Based Fraud Detection System

This table outlines how different sensor signals are used to distinguish between a **genuine stranded rider** and a **spoofing bad actor**, along with the corresponding **ML detection techniques**.

---

### 📊 Detection Strategy

| Signal Type        | Genuine Stranded Rider                                      | Spoofing Bad Actor                                   | ML Detection Method                                      |
|-------------------|------------------------------------------------------------|------------------------------------------------------|----------------------------------------------------------|
| 📱 **Gyroscope**   | Micro-movements (handlebar wobble, looking around)         | Perfectly still (phone placed on table)              | Isolation Forest → flags unnatural stillness during storm |
| 📈 **Accelerometer** | Natural vibration from rain/wind                          | Zero vibration                                       | Threshold Anomaly → static behavior = spoofing           |
| 🔋 **Battery Drain** | Faster drain (signal search, high brightness)             | Normal drain (idle device)                           | Regression Model → expected vs actual drain deviation     |
| 📡 **Cell Towers** | Handoffs between 3–5 towers as rider moves                 | Stuck on 1–2 towers                                  | DBSCAN Clustering → detects lack of tower transitions     |
| 📶 **WiFi APs**    | Multiple APs changing every 2–3 minutes                    | Same 2–3 APs consistently                            | Fingerprint Matching → low environment diversity score    |
| 📐 **Device Angle** | Natural tilt variations (70°–110°)                        | Flat (0°–5°) or overly consistent angle              | Statistical Variance → detects artificial consistency     |

---

### ⚡ Key Insight

> A **real rider in distress** exhibits *natural randomness and environmental interaction*,  
> while a **spoofing actor shows unnatural consistency or inactivity*.

---

### 🚀 ML Techniques Used

- 🌲 Isolation Forest → Outlier detection  
- 📉 Regression Models → Behavioral deviation analysis  
- 📊 DBSCAN → Pattern clustering (mobility analysis)  
- 🎯 Threshold-based Anomaly Detection  
- 🧬 Statistical Variance Modeling  
- 🛰️ Environment Fingerprinting  

---


## 📊 2. The Data: Beyond Basic GPS Coordinates
### Data Points to Detect Coordinated Fraud Rings


```mermaid
mindmap
  root((FRAUD DETECTION<br/>DATA ECOSYSTEM))
    📱 Device Sensors
      Gyroscope (rotation)
      Accelerometer (movement)
      Magnetometer (direction)
      Barometer (altitude/pressure)
      Ambient Light
      Battery Temperature
      Battery Drain Rate
    
    📶 Network Layer
      Cell Tower IDs & Handoff Frequency
      WiFi AP MAC Addresses
      Bluetooth Device Density
      Signal Strength Variance
      Network Latency
      IP Geolocation Consistency
    
    🗺️ Behavioral History
      7-Day Zone Presence
      Time-of-Day Patterns
      Earnings Density Map
      Typical Movement Speed
      Resting Spots (home locations)
      Delivery Hotspots
    
    👥 Social Graph
      Co-claimants in Same Zone
      Telegram Group Signals
      Claim Timing Clustering
      Shared Device Fingerprints
      Same Spoofed Coordinates
      Identical Sensor Patterns
```
## 🧩 Specific Data Points for Syndicate Detection

This module analyzes behavioral, environmental, and historical patterns to detect **coordinated fraud and spoofing activities** in real-time.

---

### 📊 Signal Intelligence Breakdown

| Data Category              | Specific Metrics                                              | What It Reveals                                                                 |
|---------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| 🔄 **Movement Fingerprint** | Gyroscope XYZ variance, Accelerometer frequency             | Spoofed apps generate perfectly smooth, unnatural sensor data                   |
| 🌐 **Network Environment** | Visible WiFi networks (MAC), Nearby Bluetooth devices       | Real streets → dozens of signals; controlled environments → very few            |
| ⏱️ **Temporal Clustering** | Claims per minute in same zone, synchronized timestamps     | Fraud syndicates trigger claims simultaneously (e.g., via Telegram coordination) |
| 📍 **Spatial Anomalies**   | Multiple riders at exact same coordinates (±0.000001°)       | GPS spoofing apps often reuse identical latitude/longitude values               |
| 🔋 **Power Behavior**      | Battery drain rate, Charging status                         | Real riders rarely charge devices during extreme conditions (e.g., rain)        |
| 📊 **Historical Deviation**| Deviation from 30-day movement/behavior pattern             | First-time claims in high-risk zones are highly suspicious                      |
| 👥 **Device Fingerprinting** | Device ID, App version, OS build                         | Fraud rings often reuse identical spoofing tools and configurations             |
 

---

## Syndicate Detection Algorithm

```mermaid
flowchart LR
    subgraph "REAL-TIME SYNDICATE DETECTION"
        A[Incoming Claims Stream] --> B[Sliding Window: 15 min]
        B --> C{Cluster by Zone}
        C --> D[Count > Threshold?]
        
        D -->|Yes| E{Analyze Patterns}
        E --> F[Same Coordinates?]
        E --> G[Same Sensor Readings?]
        E --> H[Same Device Fingerprint?]
        E --> I[Same Claim Time?]
        
        F & G & H & I --> J[Correlation Score]
        J -->|>80%| K[🚨 SYNDICATE ALERT]
        J -->|<40%| L[✅ Normal Variance]
    end
    
    K --> M[Freeze All Claims in Zone]
    M --> N[Manual Investigator Assigned]
    N --> O[Blocklist Device IDs]
    O --> P[Update ML Model]
```


## ⚖️ 3. The UX Balance: Handling "Flagged" Claims Fairly

- The Challenge:
> "How do we catch fraudsters without punishing honest riders who lose network in a storm?"

### The Solution: Tiered Trust Workflow

```mermaid
graph TD
    subgraph "CLAIM SUBMISSION"
        A[Rider Files Claim] --> B{Fraud Detection<br/>Layers 1-4}
    end
    
    subgraph "TRUST TIERS"
        B -->|Score > 85%| C[✅ TIER 1: TRUSTED]
        B -->|Score 60-85%| D[🟢 TIER 2: LOW RISK]
        B -->|Score 30-60%| E[🟡 TIER 3: MEDIUM RISK]
        B -->|Score < 30%| F[🔴 TIER 4: HIGH RISK]
    end
    
    subgraph "AUTOMATED ACTIONS"
        C --> G[⚡ Instant Payout<br/>No Review]
        D --> H[⏱️ Fast-track Review<br/>30 min SLA]
        E --> I[🔍 Enhanced Review<br/>2 hour SLA]
        F --> J[🚫 Flagged + Hold<br/>Manual Investigation]
    end
    
    subgraph "HONEST RIDER PROTECTION"
        K[Network Drop<br/>in Bad Weather] --> L{Does rider have<br/>history in zone?}
        L -->|Yes| M[✅ Override Flag<br/>Approve with note]
        L -->|No| N[⚠️ Request<br/>Additional Proof]
        
        N --> O[Upload Screenshot<br/>of Error Message]
        O --> P[Manual Review<br/>Priority Queue]
        P --> Q[✅ Approve if Legit]
    end
    
    style C fill:#4CAF50,color:white
    style D fill:#8BC34A,color:white
    style E fill:#FFC107,color:black
    style F fill:#ff4444,color:white
    style K fill:#2196F3,color:white
```


## 🛡️ Enhanced Architecture: Anti-Spoofing Layer

### Updated System Architecture with Adversarial Defense



```mermaid
flowchart TD
    subgraph "INPUT LAYER"
        A[Rider App] --> B[API Gateway]
        B --> C[Authentication]
        C --> D[Request Validation]
        D --> E[Rate Limiting]
    end
    
    subgraph "CORE SERVICES"
        E --> F[Risk Scoring Engine]
        F --> G[Zone Risk • Weather • Pollution]
        
        E --> H[Claim Engine]
        H --> I[Disruption Monitoring<br/>Rain • AQI • Outage]
    end
    
    subgraph "🆕 ADVERSARIAL DEFENSE LAYER"
        I --> J[Multi-Modal Fraud Detection]
        
        J --> K[LAYER 1: Behavioral Biometrics]
        K --> K1[Gyroscope • Accelerometer<br/>Battery Drain • Device Angle]
        
        J --> L[LAYER 2: Network Forensics]
        L --> L1[Cell Tower Handoffs<br/>WiFi AP Fingerprints<br/>Bluetooth Density]
        
        J --> M[LAYER 3: Historical Context]
        M --> M1[7-Day Zone History<br/>Time Patterns • Earnings Map]
        
        J --> N[LAYER 4: Temporal Correlation]
        N --> N1[Cluster Analysis<br/>Syndicate Detection<br/>Coordinate Clustering]
        
        J --> O[ENSEMBLE ML SCORING]
    end
    
    subgraph "VALIDATION & PAYMENTS"
        O --> P[Income Validation]
        P --> Q{Rider Activity<br/>Earnings Drop?}
        
        Q -->|Yes + High Trust| R[Payments<br/>Razorpay • UPI • Stripe]
        Q -->|Yes + Low Trust| S[🛡️ FLAGGED - Review Queue]
        Q -->|No| T[❌ Claim Rejected]
    end
    
    subgraph "EXTERNAL DATA SOURCES"
        U[Weather API] --> F
        V[Google Traffic API] --> F
        W[Twitter/X API] --> H
        X[Reddit API] --> H
        Y[Delivery Platform API] --> P
        Z[Telegram Monitoring API] --> N
    end
    
    style J fill:#ffaa33,color:black,stroke-width:4px
    style O fill:#4CAF50,color:white,stroke-width:4px
    style S fill:#ff4444,color:white
    style R fill:#4CAF50,color:white
```



## 📱 User Experience Flow

<img width="1574" height="1456" alt="image" src="https://github.com/user-attachments/assets/2a0aa385-66d8-4741-9c14-eddb8543518a" />

## User Journey Map

```mermaid
journey
    title Rider Journey with Drizzle
    section Onboarding
      Download App: 5: Rider
      Complete KYC: 3: Rider
      Select Zone: 4: Rider
      Pay Premium: 5: Rider, System
    section Daily Usage
      View Coverage: 5: Rider
      Work Normally: 5: Rider
      Receive Alerts: 4: System
    section Disruption Event
      Rain Detected: 5: System
      Income Drop Verified: 4: System
      Auto-claim Filed: 5: System
    section Resolution
      Claim Approved: 5: System
      Money Received: 5: Rider, Bank
      Feedback Given: 4: Rider
```

# 🔥 What Makes Drizzle Unbeatable

| **Feature**      | **Traditional Insurance** | **Drizzle**                | **Impact**               |
| ---------------- | ------------------------- | -------------------------- | ------------------------ |
| Pricing          | One-size-fits-all         | 🎯 Hyperlocal micro-zones  | 40% more affordable      |
| Claims           | 7–15 days paperwork       | ⚡ Instant auto-payout      | 100% faster              |
| Fraud Prevention | Reactive investigation    | 🛡️ Income-linked presence | <1% fraud rate           |
| Coverage         | Fixed amount              | 📊 Dynamic to earnings     | Never over/under insured |
| Accessibility    | Complex forms             | 📱 2-minute setup          | 5× adoption rate         |
| Risk Assessment  | Annual review             | 🔄 Real-time updates       | Always accurate          |
| Customer Support | Call center               | 🤖 AI-powered chat         | 24/7 instant help        |

# 🚀 Tech Stack & Innovation
```
const drizzleTech = {
    frontend: {
        framework: '⚛️ React 18',
        styling: '🎨 Tailwind CSS + DaisyUI',
        state: '🔄 Redux Toolkit',
        maps: '🗺️ Mapbox GL + React Map GL',
        pwa: '📱 Workbox + Vite PWA',
        charts: '📊 Recharts + D3.js',
        animations: '✨ Framer Motion'
    },
    backend: {
        api: '⚡ FastAPI + Pydantic',
        database: '🐘 PostgreSQL 15 + TimescaleDB',
        cache: '🚀 Redis 7',
        queue: '📨 Celery + RabbitMQ',
        search: '🔍 Elasticsearch',
        websockets: '🔌 Socket.io'
    },
    ml: {
        forecasting: '📈 Prophet + ARIMA',
        riskScoring: '🤖 scikit-learn + XGBoost',
        anomaly: '🔍 Isolation Forest + Autoencoders',
        deployment: '🚀 MLflow + ONNX'
    },
    devops: {
        container: '🐳 Docker + Docker Compose',
        orchestration: '☸️ Kubernetes + Helm',
        ci/cd: '🔄 GitHub Actions + ArgoCD',
        monitoring: '📈 Prometheus + Grafana',
        logging: '📝 ELK Stack',
        cloud: '☁️ AWS (EKS, RDS, ElastiCache)'
    },
    security: {
        auth: '🔐 JWT + OAuth2',
        encryption: '🔒 AES-256',
        compliance: '📋 GDPR + PCI DSS',
        rate_limit: '⏱️ Redis + Token Bucket'
    }
};

```

## 🏁 Development Roadmap

```mermaid
gantt
    title Drizzle Development Timeline - GuideWire Hackathon 2026
    dateFormat YYYY-MM-DD
    axisFormat %b %d
    
    section Foundation (Week 1-2)
    Persona Research & Problem Validation :done, 2026-06-02, 7d
    Risk Scoring MVP Design :done, 2026-06-09, 7d
    Premium Logic Implementation :done, 2026-06-16, 7d
    
    section Core Features (Week 3-4)
    Trigger Automation System :active, 2026-06-23, 7d
    Fraud Detection Module :2026-06-30, 7d
    Policy Management System :2026-06-23, 14d
    Income Validation Engine :2026-06-30, 10d
    
    section Integration (Week 5)
    Weather API Integration :2026-07-03, 3d
    Payment Gateway (Razorpay) :2026-07-03, 3d
    Platform API Simulation :2026-07-03, 3d
    
    section Polish (Week 6)
    Payout System Integration :2026-07-06, 2d
    Analytics Dashboard :2026-07-06, 2d
    Mobile App Polish :2026-07-06, 2d
    
    section Launch (Final Days)
    Testing & QA :2026-07-07, 1d
    Documentation :2026-07-07, 1d
    Pitch Deck & Demo :2026-07-08, 1d
    Hackathon Submission :milestone, 2026-07-08, 1d
```

## Team

- Devanshi Agrawal
- Nilesh Kanti
- Rishit Vats
- Srijan Sarkar
- Aditya Pratap Singh



