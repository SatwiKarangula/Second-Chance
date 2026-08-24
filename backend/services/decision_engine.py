def make_intervention_decision(
    behavior,
    risk
):
    """
    Decide whether Second Chance
    should intervene with a customer.
    """

    risk_score = risk.get(
        "risk_score",
        0
    )

    inactive_seconds = behavior.get(
        "inactive_duration_seconds",
        0
    )

    # =========================================
    # LOW RISK
    # =========================================

    if risk_score < 31:

        return {
            "decision": "NO_ACTION",
            "reason": "Customer behavior appears normal.",
        }

    # =========================================
    # MEDIUM RISK
    # =========================================

    if risk_score < 61:

        return {
            "decision": "MONITOR",
            "reason": "Customer shows some hesitation.",
        }

    # =========================================
    # HIGH RISK
    # =========================================

    if risk_score < 81:

        if inactive_seconds >= 60:

            return {
                "decision":
                    "INTERVENTION_RECOMMENDED",

                "reason":
                    "High risk combined with checkout inactivity.",
            }

        return {
            "decision":
                "CONSIDER_INTERVENTION",

            "reason":
                "Customer behavior indicates elevated risk.",
        }

    # =========================================
    # CRITICAL RISK
    # =========================================

    return {
        "decision":
            "INTERVENTION_RECOMMENDED",

        "reason":
            "Critical abandonment risk detected.",
    }