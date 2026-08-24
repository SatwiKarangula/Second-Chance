from datetime import datetime, timezone


def normalize_timestamp(timestamp):
    """
    Make sure every timestamp is timezone-aware
    and treated as UTC.
    """

    if timestamp.tzinfo is None:
        return timestamp.replace(
            tzinfo=timezone.utc
        )

    return timestamp


def analyze_checkout_events(events):
    """
    Analyze raw checkout events and convert them
    into useful customer behavior signals.
    """

    if not events:
        return {
            "event_count": 0,
            "cart_change_count": 0,
            "checkout_duration_seconds": 0,
            "inactive_duration_seconds": 0,
            "cart_value": 0,

            "initial_cart_value": 0,
            "cart_value_change": 0,

            "initial_quantity": 0,
            "current_quantity": 0,
            "quantity_change": 0,

            "quantity_reduced": False,
            "quantity_increased": False,

            "cart_value_reduced": False,
            "cart_value_increased": False,
        }

    # =========================================
    # NORMALIZE TIMESTAMPS
    # =========================================

    for event in events:
        event["timestamp"] = normalize_timestamp(
            event["timestamp"]
        )

    # =========================================
    # SORT EVENTS
    # =========================================

    events = sorted(
        events,
        key=lambda event: event["timestamp"]
    )

    first_event = events[0]
    last_event = events[-1]

    # =========================================
    # EVENT COUNT
    # =========================================

    event_count = len(events)

    # =========================================
    # CART UPDATE COUNT
    # =========================================

    cart_change_count = sum(
        1
        for event in events
        if event.get("event_type") == "CART_UPDATED"
    )

    # =========================================
    # CHECKOUT DURATION
    # =========================================

    checkout_duration = (
        last_event["timestamp"]
        - first_event["timestamp"]
    ).total_seconds()

    # =========================================
    # INACTIVE DURATION
    # =========================================

    now = datetime.now(timezone.utc)

    inactive_duration = (
        now
        - last_event["timestamp"]
    ).total_seconds()

    # =========================================
    # CART VALUES
    # =========================================

    initial_cart_value = first_event.get(
        "cart_value",
        0
    )

    current_cart_value = last_event.get(
        "cart_value",
        0
    )

    cart_value_change = (
        current_cart_value
        - initial_cart_value
    )

    # =========================================
    # QUANTITIES
    # =========================================

    initial_quantity = (
        first_event
        .get("metadata", {})
        .get("total_item_quantity", 0)
    )

    current_quantity = (
        last_event
        .get("metadata", {})
        .get("total_item_quantity", 0)
    )

    quantity_change = (
        current_quantity
        - initial_quantity
    )

    # =========================================
    # BEHAVIOR FLAGS
    # =========================================

    quantity_reduced = (
        quantity_change < 0
    )

    quantity_increased = (
        quantity_change > 0
    )

    cart_value_reduced = (
        cart_value_change < 0
    )

    cart_value_increased = (
        cart_value_change > 0
    )

    # =========================================
    # RETURN BEHAVIOR
    # =========================================

    return {
        "event_count": event_count,

        "cart_change_count":
            cart_change_count,

        "checkout_duration_seconds":
            round(
                checkout_duration,
                2
            ),

        "inactive_duration_seconds":
            round(
                inactive_duration,
                2
            ),

        "cart_value":
            current_cart_value,

        "initial_cart_value":
            initial_cart_value,

        "cart_value_change":
            cart_value_change,

        "initial_quantity":
            initial_quantity,

        "current_quantity":
            current_quantity,

        "quantity_change":
            quantity_change,

        "quantity_reduced":
            quantity_reduced,

        "quantity_increased":
            quantity_increased,

        "cart_value_reduced":
            cart_value_reduced,

        "cart_value_increased":
            cart_value_increased,
    }