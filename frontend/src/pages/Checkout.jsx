import {
  useEffect,
  useRef,
  useState,
} from "react";

import { useCart } from "../CartContext";
import { sendEvent } from "../services/api";

function Checkout() {
  const {
    cart,
    cartTotal,
  } = useCart();

  // =========================================
  // CHECKOUT SESSION
  // =========================================

  const [sessionId] = useState(() => {
    let existingSessionId =
      sessionStorage.getItem(
        "second_chance_session_id"
      );

    if (!existingSessionId) {
      existingSessionId =
        crypto.randomUUID();

      sessionStorage.setItem(
        "second_chance_session_id",
        existingSessionId
      );
    }

    return existingSessionId;
  });

  // Prevent duplicate CHECKOUT_STARTED
  // requests during the same checkout session.
  const checkoutStartedRef = useRef(false);

  // =========================================
  // CUSTOMER INFORMATION
  // =========================================

  const [customer, setCustomer] = useState({
    name: "",
    email: "",
    phone: "",
    address: "",
  });

  // =========================================
  // CHECKOUT_STARTED EVENT
  // =========================================

  useEffect(() => {
    if (
      cart.length === 0 ||
      checkoutStartedRef.current
    ) {
      return;
    }

    checkoutStartedRef.current = true;

    const startCheckout = async () => {
      try {
        await sendEvent({
          event_type: "CHECKOUT_STARTED",

          session_id: sessionId,

          cart_value: cartTotal,

          // Unique logical identity for
          // this checkout-start event.
          event_key:
            `${sessionId}:CHECKOUT_STARTED`,

          source: "web",

          metadata: {
            unique_product_count:
              cart.length,

            total_item_quantity:
              cart.reduce(
                (total, item) =>
                  total + item.quantity,
                0
              ),
          },
        });

        console.log(
          "CHECKOUT_STARTED recorded:",
          sessionId
        );
      } catch (error) {
        // Allow retry if request fails.
        checkoutStartedRef.current = false;

        console.error(
          "Failed to record checkout event:",
          error
        );
      }
    };

    startCheckout();
  }, [
    cart.length,
    cartTotal,
    sessionId,
  ]);

  // =========================================
  // CUSTOMER FORM
  // =========================================

  const handleChange = (event) => {
    const {
      name,
      value,
    } = event.target;

    setCustomer((current) => ({
      ...current,
      [name]: value,
    }));
  };

  // =========================================
  // CHECKOUT SUBMISSION
  // =========================================

  const handleSubmit = (event) => {
    event.preventDefault();

    console.log(
      "Checkout initiated:",
      {
        sessionId,
        customer,
        cart,
        cartTotal,
      }
    );

    alert(
      "Checkout initiated!"
    );
  };

  // =========================================
  // EMPTY CART
  // =========================================

  if (cart.length === 0) {
    return (
      <div className="checkout-page">
        <h1>
          Your cart is empty
        </h1>

        <p>
          Add a product before
          starting checkout.
        </p>
      </div>
    );
  }

  // =========================================
  // CHECKOUT UI
  // =========================================

  return (
    <div className="checkout-page">

      <div className="checkout-content">

        {/* ================================= */}
        {/* CHECKOUT FORM */}
        {/* ================================= */}

        <div className="checkout-form-section">

          <p className="eyebrow">
            CHECKOUT
          </p>

          <h1>
            Complete your purchase
          </h1>

          <p className="checkout-description">
            Enter your details to
            continue to payment.
          </p>

          <form
            onSubmit={handleSubmit}
          >

            {/* FULL NAME */}

            <label>
              Full Name

              <input
                type="text"
                name="name"
                value={customer.name}
                onChange={handleChange}
                placeholder="Enter your name"
                required
              />
            </label>

            {/* EMAIL */}

            <label>
              Email

              <input
                type="email"
                name="email"
                value={customer.email}
                onChange={handleChange}
                placeholder="you@example.com"
                required
              />
            </label>

            {/* PHONE */}

            <label>
              Phone

              <input
                type="tel"
                name="phone"
                value={customer.phone}
                onChange={handleChange}
                placeholder="Enter your phone number"
                required
              />
            </label>

            {/* ADDRESS */}

            <label>
              Address

              <textarea
                name="address"
                value={customer.address}
                onChange={handleChange}
                placeholder="Enter your delivery address"
                rows="4"
                required
              />
            </label>

            {/* PAYMENT BUTTON */}

            <button
              type="submit"
              className="checkout-button"
            >
              Continue to Payment
            </button>

          </form>

        </div>

        {/* ================================= */}
        {/* ORDER SUMMARY */}
        {/* ================================= */}

        <aside className="checkout-summary">

          <h2>
            Order Summary
          </h2>

          {cart.map((item) => (

            <div
              className="summary-item"
              key={item.id}
            >

              <span>
                {item.name} ×{" "}
                {item.quantity}
              </span>

              <strong>
                ₹
                {(
                  item.price *
                  item.quantity
                ).toLocaleString(
                  "en-IN"
                )}
              </strong>

            </div>

          ))}

          <div className="summary-total">

            <span>
              Total
            </span>

            <strong>
              ₹
              {cartTotal.toLocaleString(
                "en-IN"
              )}
            </strong>

          </div>

        </aside>

      </div>

    </div>
  );
}

export default Checkout;