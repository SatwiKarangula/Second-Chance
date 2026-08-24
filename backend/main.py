from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from services.behavior_analyzer import analyze_checkout_events
from services.risk_engine import calculate_risk_score
from services.decision_engine import (make_intervention_decision)
from services.intervention_engine import (select_intervention)
from services.ai_reasoning import (generate_ai_recommendation)


app = FastAPI(
    title="Second Chance AI",
    description="AI Checkout Rescue Agent",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# MongoDB Connection
# -------------------------

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["second_chance"]

checkout_events = db["checkout_events"]

ai_decisions = db["ai_decisions"]

checkout_events.create_index(
    "event_key",
    unique=True
)


# -------------------------
# Data Model
# -------------------------

class CheckoutEvent(BaseModel):
    event_type: str
    session_id: str
    cart_value: float
    source: str = "web"
    metadata: dict = {}
    event_key: str


# -------------------------
# Basic Routes
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Second Chance AI is running!"
    }


@app.get("/health")
def health_check():
    try:
        client.admin.command("ping")

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected",
        }


# -------------------------
# Checkout Event API
# -------------------------

@app.post("/api/events")
def create_checkout_event(event: CheckoutEvent):

    event_document = {
        "event_key": event.event_key,
        "event_type": event.event_type,
        "session_id": event.session_id,
        "cart_value": event.cart_value,
        "timestamp": datetime.now(timezone.utc),
        "source": event.source,
        "metadata": event.metadata,
    }

    try:
        result = checkout_events.insert_one(
            event_document
        )

        return {
            "success": True,
            "duplicate": False,
            "event_id": str(result.inserted_id),
            "message": "Checkout event recorded",
        }

    except DuplicateKeyError:
        return {
            "success": True,
            "duplicate": True,
            "message": "Duplicate event ignored",
        }

#-----------------------------
#Create our first behavior API
#-----------------------------

@app.get("/api/behavior/{session_id}")
def get_checkout_behavior(session_id: str):

    events = list(
        checkout_events.find(
            {
                "session_id": session_id
            }
        )
    )

    behavior = analyze_checkout_events(
        events
    )

    return {
        "success": True,
        "session_id": session_id,
        "behavior": behavior,
    }

@app.get("/api/risk/{session_id}")
def get_checkout_risk(session_id: str):

    events = list(
        checkout_events.find(
            {
                "session_id": session_id
            }
        )
    )

    behavior = analyze_checkout_events(
        events
    )

    risk = calculate_risk_score(
        behavior
    )

    decision = make_intervention_decision(
        behavior,
        risk
    )

    intervention = select_intervention(
        behavior,
        risk,
        decision
    )

    ai_recommendation = (
        generate_ai_recommendation(
            behavior,
            risk,
            decision,
            intervention
        )
    )
    ai_decisions.insert_one({
    "session_id": session_id,

    "recommendation":
        ai_recommendation["recommendation"],

    "confidence":
        ai_recommendation["confidence"],

    "reason":
        ai_recommendation["reason"],

    "customer_message":
        ai_recommendation["customer_message"],

    "risk_score":
        risk["risk_score"],

    "risk_level":
        risk["risk_level"],

    "timestamp":
        datetime.now(timezone.utc),
})
    return {
        "success": True,

        "session_id": session_id,

        "behavior": behavior,

        "risk": risk,

        "decision": decision,

        "intervention": intervention,

        "ai_recommendation": ai_recommendation,
    }
