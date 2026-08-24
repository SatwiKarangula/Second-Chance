import os
from typing import Literal

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel


# =========================================
# LOAD ENVIRONMENT VARIABLES
# =========================================

load_dotenv()


# =========================================
# GEMINI CLIENT
# =========================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================================
# AI RESPONSE SCHEMA
# =========================================

class AIRecommendation(BaseModel):

    recommendation: Literal[
        "NONE",
        "MONITOR",
        "ASSIST",
        "OFFER",
        "PAYMENT_HELP",
        "HUMAN_SUPPORT",
    ]

    confidence: float

    reason: str

    customer_message: str


# =========================================
# AI REASONING ENGINE
# =========================================

def generate_ai_recommendation(
    behavior,
    risk,
    decision,
    intervention,
):

    prompt = f"""
You are the AI reasoning engine
for an e-commerce checkout rescue
system called Second Chance.

Your job is to understand customer
checkout behavior and recommend the
most appropriate intervention.

IMPORTANT RULES:

1. Do not invent discounts.
2. Do not invent prices.
3. Do not process payments.
4. Do not modify the customer's cart.
5. Only recommend one of the allowed
   interventions below.

Allowed interventions:

NONE
MONITOR
ASSIST
OFFER
PAYMENT_HELP
HUMAN_SUPPORT

Use the deterministic system signals
as constraints.

The deterministic system calculated:

BEHAVIOR:
{behavior}

RISK:
{risk}

DECISION:
{decision}

INTERVENTION:
{intervention}

Analyze the situation and return:

- recommendation
- confidence from 0 to 1
- short reason
- short customer-friendly message

Keep the reasoning concise.
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": AIRecommendation,
            },
        )

        result = AIRecommendation.model_validate_json(
            response.text
        )

        # =========================================
        # CONFIDENCE GUARDRAIL
        # =========================================

        result.confidence = max(
            0.0,
            min(
                1.0,
                result.confidence
            )
        )

        return result.model_dump()

    except Exception as error:

        print(
            "AI reasoning failed:",
            error
        )

        return {
            "recommendation":
                intervention.get(
                    "intervention",
                    "ASSIST"
                ),

            "confidence": 0.0,

            "reason":
                "AI service unavailable. "
                "Using deterministic intervention.",

            "customer_message":
                intervention.get(
                    "message",
                    "How can we help you complete your purchase?"
                ),
        }