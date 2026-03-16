# GuideWire-Hackathon
Team Void Main()

## Problem Statment
### Who?
Food delivery partners working in metro cities.

### How They Earn?
    - Paid per delivery
    - Weekly income cycle
    - Peak-hour dependent (6PM–10PM)

### What Goes Wrong?

| Disruption              | What Happens                              | Income Impact            |
|-------------------------|--------------------------------------------|--------------------------|
| 🌧 Heavy Rain / Flooding | Orders drop or deliveries become unsafe   | Peak earnings lost       |
| 🌫 High AQI              | Outdoor working hours reduce              | Fewer completed orders   |
| 🚫 Curfew                | Restricted movement across zones          | Zero deliveries          |
| 📱 App Outage            | No order allocation from platform         | Immediate income stop    |

### The Real Issue
    - Income drops instantly
    - No compensation mechanism
    - Loss happens in peak earning hours
    - Workers bear full financial risk

## Persona Definition

### Delivery Segment Chosen:
Food delivery partner working with platforms like Swiggy or Zomato in a metro city.

### Typical Weekly Income:
A delivery partner earns approximately ₹3,500–₹6,000 per week depending on hours worked, location, and demand. Their income depends entirely on the number of successful deliveries completed.

### Typical Risk Exposure:
Since they work outdoors for long hours, they are directly affected by heavy rain, waterlogging, extreme heat, high pollution levels, sudden curfews, and platform outages. During such disruptions, orders drop significantly or deliveries become impossible, leading to immediate income loss.

### Real-World Disruption Scenario:
For example, if heavy rainfall causes flooding in certain micro-zones between 6 PM and 10 PM (peak earning hours), delivery orders reduce sharply. The rider may be unable to complete deliveries safely or access pickup locations. As a result, they lose a portion of their daily income without any compensation.


## Weekly Premium Model

### 1)How Risk Score is Calculated
Each micro-zone is assigned a weekly Risk Score (0–100) based on:
    
    - Historical frequency of weather disruptions

    - Waterlogging and flood-prone patterns

    - Pollution severity trends

    - Platform outage history

    - Disruption volatility (how unpredictable the zone is)

Additionally, rider-specific factors are considered:
   
    - Primary Operating Zone (POZ)
    
    - Earning density in that zone

    - Historical working hours

    - Trust score (behavioral consistency)

The final risk score determines the premium category.

### 2)What Affects the Weekly Premium
The weekly premium depends on:

    - Risk level of the rider’s Primary Operating Zone

    - Frequency of disruptions in that zone

    - Expected income exposure during peak hours

    - Coverage limit selected by the rider

    - Higher-risk zones have slightly higher premiums but also offer higher maximum coverage.

### 3)Weekly Pricing Structure (Example)

| Risk Category     | Weekly Premium | Maximum Weekly Coverage |
|-------------------|---------------|--------------------------|
| Low Risk Zone     | ₹15           | ₹800                     |
| Medium Risk Zone  | ₹28           | ₹1500                    |
| High Risk Zone    | ₹45           | ₹2500                    |

This structure ensures:

- Affordable entry pricing  
- Proportional protection based on risk  
- Financial sustainability for the insurer

### Example Scenario
A food delivery rider operating in a flood-prone micro-zone is classified under Medium Risk.

    - Weekly Premium: ₹28
    - If verified disruptions reduce earnings during peak hours, the rider can receive compensation up to ₹1500 for that week.
This ensures workers are protected without overpaying for unnecessary coverage.


## Solution Overview – Drizzle

### What Drizzle Does

| Step | What Happens | Why It Matters |
|------|-------------|----------------|
| 1️⃣ Zone Intelligence | City divided into 500m–1km micro-zones | Enables hyperlocal risk pricing |
| 2️⃣ Risk Scoring | Each zone gets a dynamic weekly risk score | Fair, data-driven premium calculation |
| 3️⃣ Trigger Monitoring | System tracks rainfall, AQI, curfews, and app outages | Automatic disruption detection |
| 4️⃣ Income Validation | Verifies real income drop before payout | Prevents false claims |
| 5️⃣ Instant Payout | Auto-initiated with zero paperwork | Fast financial protection |

### What Makes It Different
    - Unlike simple geo-trigger models:
    - Payout is linked to economic activity
    - Eligibility requires pre-disruption presence
    - Income loss must be data-validated
    - Fraud detection runs automatically

### Business Model
    - Simple weekly subscription
    - Premium based on zone risk
    - Coverage aligned with weekly earnings cycle

## Core Innovation: Income-Linked Presence (Fraud-Resistant Design)
Traditional models work like this:

    - Rain happened in zone → anyone present gets paid.

This creates fraud risk. Riders could travel to a rainy zone just to claim compensation.

Drizzle introduces:
    
    - Income-Linked Presence Model

Instead of location-based payout, eligibility is tied to economic activity before disruption.

A rider qualifies only if:

    - They were active in that micro-zone in the last 7 days
    - The zone contributes significantly to their weekly income
    - They were present before the disruption started

This ensures payouts are linked to genuine working behavior, not opportunistic movement.

Drizzle protects income — not rainfall exploitation.
