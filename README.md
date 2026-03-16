# GuideWire-Hackathon
Team Void Main()

## Problem we are solving!!!!
Gig delivery workers in India operate on a week-to-week income cycle, and even a few hours of disruption due to heavy rain, pollution, curfews, or platform outages can significantly reduce their earnings. These external events are unpredictable and beyond their control, yet there is currently no dedicated system that protects them against short-term income loss.

## Solution
Drizzle is an AI-powered, hyperlocal parametric insurance platform that automatically detects real-time disruptions and compensates workers for verified income loss. Using a simple weekly pricing model, smart risk assessment, and instant automated payouts, Drizzle provides a reliable financial safety net without manual claims or paperwork.

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
