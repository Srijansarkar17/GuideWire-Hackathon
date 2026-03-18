# 🌧️ **Drizzle** – *Income Safety Net for India's Gig Workforce*

<div align="center">
  
  [![Made by Team Void Main()](https://img.shields.io/badge/Team-Void%20Main%20()-blueviolet?style=for-the-badge&logo=python)](https://github.com/your-repo)
  [![GuideWire Hackathon](https://img.shields.io/badge/GuideWire-Hackathon%202024-ff6b35?style=for-the-badge&logo=guidewire)](https://)
  [![Prototype](https://img.shields.io/badge/Status-Prototype-brightgreen?style=for-the-badge)](https://)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)
  
  ### *Because Rain Shouldn't Mean Empty Plates* 🍽️☔
  
  [🎥 Watch Demo](#) • [📊 Live Dashboard](#) • [📄 Pitch Deck](#) • [📱 Download App](#)
  
</div>

---

## 📋 **Table of Contents**
- [The $5B Problem](#-the-5b-problem-nobodys-solving)
- [Our Innovation](#-our-innovation-income-linked-presence)
- [Risk Intelligence](#-hyperlocal-risk-intelligence)
- [Premium Model](#-premium-model-that-makes-sense)
- [System Architecture](#-system-architecture)
- [User Experience](#-user-experience-flow)
- [Tech Stack](#-tech-stack--innovation)
- [Live Demo](#-live-demo-preview)
- [Development Roadmap](#-development-roadmap)
- [Installation](#-installation--setup)
- [API Documentation](#-api-documentation)
- [Impact Metrics](#-impact-metrics)
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
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/c51157d3-569d-4ac5-a35f-135c3fde279f" />


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

# 🏗️ System Architecture

<img width="868" height="990" alt="image" src="https://github.com/user-attachments/assets/b026b71d-5f22-4e50-9e4e-faf192a6ec21" />


## Data Flow Diagram

```mermaid
flowchart TD
    subgraph Input
        A[Rider Activity] --> B[(Historical DB)]
        C[Weather Data] --> D{Disruption Detector}
        E[Platform Outages] --> D
    end
    
    subgraph Processing
        D --> F[Risk Scorer]
        B --> F
        F --> G[Premium Calculator]
        G --> H[Policy Issuance]
        
        D --> I[Trigger Event]
        I --> J[Income Validator]
        J --> K{Legitimate Claim?}
    end
    
    subgraph Output
        K -->|Yes| L[Auto-payout]
        K -->|No| M[Flag for Review]
        L --> N[Bank Transfer]
        M --> O[Fraud Database]
    end
    
    style D fill:#f9d71c
    style K fill:#ff6b6b
    style L fill:#4CAF50
```

# 📱 User Experience Flow

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

# 🏁 Development Roadmap

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



