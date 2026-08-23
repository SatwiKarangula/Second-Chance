# Second Chance — System Architecture

## 1. Project Overview

Second Chance is an AI-powered checkout recovery system designed
to identify customers who are likely to abandon a purchase,
understand the reason for hesitation, and select an appropriate
intervention to improve checkout conversion.

## 2. Core Objective

The system aims to:

- Detect checkout abandonment risk
- Understand the likely reason behind the risk
- Select an appropriate intervention
- Track the intervention outcome
- Measure recovered conversions and revenue

## 3. High-Level Architecture

Customer
    ↓
React Storefront
    ↓
Checkout
    ↓
Behavior/Event Collection
    ↓
FastAPI Backend
    ↓
Risk Detection
    ↓
AI Diagnosis Agent
    ↓
AI Action Agent
    ↓
Customer Intervention
    ↓
Razorpay Payment
    ↓
Payment Outcome
    ↓
MongoDB
    ↓
Merchant Analytics Dashboard

## 4. Technology Stack

### Frontend
- React
- JavaScript / TypeScript

### Backend
- Python
- FastAPI
- REST APIs

### Database
- MongoDB
- MongoDB Compass

### AI
- Large Language Model
- AI Diagnosis Agent
- AI Action Agent
- Structured outputs
- Tool calling

### Payments
- Razorpay Test Mode

### Development
- VS Code
- Git
- GitHub

## 5. AI Agents

### Diagnosis Agent

Purpose:
Determine why a customer may abandon checkout.

Inputs may include:

- Cart value
- Checkout duration
- Payment attempts
- Product information
- Customer interaction events
- EMI page visits
- Previous checkout activity

Output:

- Risk reason
- Confidence score
- Supporting evidence

### Action Agent

Purpose:
Select the most appropriate recovery intervention.

Possible actions:

- Show EMI information
- Offer a relevant incentive
- Provide payment assistance
- Suggest an alternative payment method
- Provide reassurance
- Do nothing when intervention is unnecessary

## 6. Payment Flow

The system uses Razorpay as the payment infrastructure.

Razorpay is not the AI system.

It provides the payment execution and payment outcome signals
that allow Second Chance to measure whether an intervention
actually resulted in a successful transaction.

## 7. Data Flow

Customer behavior
    ↓
Event generated
    ↓
Backend receives event
    ↓
Risk assessment
    ↓
AI diagnosis
    ↓
AI action selection
    ↓
Intervention
    ↓
Payment attempt
    ↓
Payment result
    ↓
Outcome stored in MongoDB

## 8. Initial MongoDB Collections

Planned collections:

- users
- products
- carts
- checkout_events
- interventions
- payments
- analytics

## 9. Merchant Dashboard

The merchant dashboard will provide:

- Total checkout sessions
- At-risk customers
- Abandoned checkouts
- Successful recoveries
- Recovery rate
- Recovered revenue
- Top abandonment reasons
- Intervention performance

## 10. MVP Principle

The first version will prioritize:

1. Working checkout flow
2. Reliable event collection
3. AI-powered diagnosis
4. AI-powered intervention selection
5. Razorpay test payment
6. Outcome tracking
7. Merchant analytics

The system should demonstrate measurable business value rather
than simply demonstrating an AI chatbot.

## 11. Future Architecture

Future versions may include:

- Machine learning-based risk prediction
- Real-time personalization
- RAG
- Advanced agent workflows
- Experimentation / A-B testing
- Cloud deployment
- Observability
- Automated evaluation
- Production-scale infrastructure