def select_intervention(
    behavior,
    risk,
    decision
):
    """
    Select the most appropriate intervention
    based on customer behavior and risk.
    """

    decision_type = decision.get(
        "decision",
        "NO_ACTION"
    )

    risk_score = risk.get(
        "risk_score",
        0
    )

    # =========================================
    # NO ACTION
    # =========================================

    if decision_type == "NO_ACTION":

        return {
            "intervention":
                "NONE",

            "message":
                "No intervention is necessary.",

            "priority":
                "LOW",
        }

    # =========================================
    # MONITOR
    # =========================================

    if decision_type == "MONITOR":

        return {
            "intervention":
                "MONITOR",

            "message":
                "Continue monitoring customer behavior.",

            "priority":
                "LOW",
        }

    # =========================================
    # CUSTOMER BEHAVIOR
    # =========================================

    quantity_reduced = behavior.get(
        "quantity_reduced",
        False
    )

    cart_value_reduced = behavior.get(
        "cart_value_reduced",
        False
    )

    # =========================================
    # PRICE SENSITIVITY
    # =========================================

    if (
        quantity_reduced
        and cart_value_reduced
    ):

        return {
            "intervention":
                "OFFER",

            "message":
                "Customer appears price-sensitive. Consider presenting a relevant offer.",

            "priority":
                "HIGH",
        }

    # =========================================
    # VERY HIGH RISK
    # =========================================

    if risk_score >= 81:

        return {
            "intervention":
                "HUMAN_SUPPORT",

            "message":
                "Customer shows critical abandonment risk. Consider human assistance.",

            "priority":
                "CRITICAL",
        }

    # =========================================
    # HIGH RISK
    # =========================================

    if risk_score >= 61:

        return {
            "intervention":
                "ASSIST",

            "message":
                "Customer shows elevated checkout hesitation. Offer assistance.",

            "priority":
                "HIGH",
        }

    # =========================================
    # DEFAULT
    # =========================================

    return {
        "intervention":
            "ASSIST",

        "message":
            "Offer helpful checkout assistance.",

        "priority":
            "MEDIUM",
    }