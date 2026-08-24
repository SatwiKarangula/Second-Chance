def calculate_risk_score(behavior):
    """
    Calculate checkout abandonment risk
    using explainable behavioral rules.
    """

    score = 0
    reasons = []

    # =========================================
    # 1. HIGH CART VALUE
    # =========================================

    cart_value = behavior.get(
        "cart_value",
        0
    )

    if cart_value >= 100000:
        score += 20

        reasons.append(
            "High-value cart"
        )

    # =========================================
    # 2. CART CHANGES
    # =========================================

    cart_changes = behavior.get(
        "cart_change_count",
        0
    )

    if cart_changes >= 3:
        score += 20

        reasons.append(
            "Multiple cart changes"
        )

    elif cart_changes >= 2:
        score += 10

        reasons.append(
            "Repeated cart changes"
        )

    elif cart_changes >= 1:
        score += 5

        reasons.append(
            "Cart was changed"
        )

    # =========================================
    # 3. INACTIVITY
    # =========================================

    inactive_seconds = behavior.get(
        "inactive_duration_seconds",
        0
    )

    if inactive_seconds >= 120:
        score += 30

        reasons.append(
            "Long checkout inactivity"
        )

    elif inactive_seconds >= 60:
        score += 20

        reasons.append(
            "Checkout inactivity detected"
        )

    elif inactive_seconds >= 30:
        score += 10

        reasons.append(
            "Short checkout inactivity"
        )

    # =========================================
    # 4. QUANTITY REDUCTION
    # =========================================

    quantity_reduced = behavior.get(
        "quantity_reduced",
        False
    )

    if quantity_reduced:
        score += 15

        reasons.append(
            "Purchase quantity reduced"
        )

    # =========================================
    # 5. CART VALUE REDUCTION
    # =========================================

    initial_cart_value = behavior.get(
        "initial_cart_value",
        0
    )

    cart_value_change = behavior.get(
        "cart_value_change",
        0
    )

    if (
        initial_cart_value > 0
        and cart_value_change < 0
    ):

        reduction_percentage = (
            abs(cart_value_change)
            / initial_cart_value
        ) * 100

        if reduction_percentage >= 50:

            score += 15

            reasons.append(
                "Major spending reduction"
            )

        elif reduction_percentage >= 25:

            score += 10

            reasons.append(
                "Significant spending reduction"
            )

        elif reduction_percentage >= 10:

            score += 5

            reasons.append(
                "Spending reduced"
            )

    # =========================================
    # LIMIT SCORE
    # =========================================

    score = min(
        score,
        100
    )

    # =========================================
    # RISK LEVEL
    # =========================================

    if score >= 81:

        risk_level = "CRITICAL"

    elif score >= 61:

        risk_level = "HIGH"

    elif score >= 31:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    # =========================================
    # RETURN RESULT
    # =========================================

    return {
        "risk_score": score,

        "risk_level": risk_level,

        "reasons": reasons,
    }