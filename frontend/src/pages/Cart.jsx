import { useCart } from "../CartContext";
import { Link } from "react-router-dom";
import axios from "axios";

function Cart() {
  const {
    cart,
    removeFromCart,
    updateQuantity,
    cartTotal,
  } = useCart();

  // -----------------------------------------
  // GET / CREATE CART SESSION ID
  // -----------------------------------------

  const getCartSessionId = () => {
    let sessionId = sessionStorage.getItem(
      "second_chance_session_id"
    );

    if (!sessionId) {
      sessionId = crypto.randomUUID();

      sessionStorage.setItem(
        "second_chance_session_id",
        sessionId
      );
    }

    return sessionId;
  };

  // -----------------------------------------
  // SEND CART_UPDATED EVENT
  // -----------------------------------------

  const sendCartUpdatedEvent = (updatedCart) => {
    if (!updatedCart || updatedCart.length === 0) {
      return;
    }

    const sessionId = getCartSessionId();

    const cartValue = updatedCart.reduce(
      (total, item) =>
        total + item.price * item.quantity,
      0
    );

    const metadata = {
      unique_product_count:
        updatedCart.length,

      total_item_quantity:
        updatedCart.reduce(
          (total, item) =>
            total + item.quantity,
          0
        ),

      items: updatedCart.map((item) => ({
        id: item.id,
        quantity: item.quantity,
        price: item.price,
      })),
    };

    const cartSignature = JSON.stringify(
      updatedCart.map((item) => ({
        id: item.id,
        quantity: item.quantity,
        price: item.price,
      }))
    );

    const eventKey =
      `${sessionId}:CART_UPDATED:${cartSignature}`;

    axios
      .post(
        "http://127.0.0.1:8000/api/events",
        {
          event_type: "CART_UPDATED",
          session_id: sessionId,
          cart_value: cartValue,
          source: "web",
          metadata: metadata,
          event_key: eventKey,
        }
      )
      .then(() => {
        console.log(
          "CART_UPDATED event recorded"
        );
      })
      .catch((error) => {
        console.error(
          "Failed to record CART_UPDATED event:",
          error
        );
      });
  };

  // -----------------------------------------
  // QUANTITY UPDATE
  // -----------------------------------------

  const handleQuantityChange = (
    itemId,
    newQuantity
  ) => {
    if (newQuantity < 1) {
      return;
    }

    const updatedCart = cart.map((item) =>
      item.id === itemId
        ? {
            ...item,
            quantity: newQuantity,
          }
        : item
    );

    updateQuantity(
      itemId,
      newQuantity
    );

    sendCartUpdatedEvent(
      updatedCart
    );
  };

  // -----------------------------------------
  // REMOVE PRODUCT
  // -----------------------------------------

  const handleRemove = (itemId) => {
    const updatedCart = cart.filter(
      (item) => item.id !== itemId
    );

    removeFromCart(itemId);

    if (updatedCart.length > 0) {
      sendCartUpdatedEvent(
        updatedCart
      );
    }
  };

  // -----------------------------------------
  // EMPTY CART
  // -----------------------------------------

  if (cart.length === 0) {
    return (
      <div className="cart-page">
        <h1>Your Cart</h1>

        <p>
          Your cart is currently empty.
        </p>
      </div>
    );
  }

  // -----------------------------------------
  // UI
  // -----------------------------------------

  return (
    <div className="cart-page">
      <h1>Your Cart</h1>

      <div className="cart-items">
        {cart.map((item) => (
          <div
            className="cart-item"
            key={item.id}
          >
            <div>
              <p className="product-category">
                {item.category}
              </p>

              <h3>{item.name}</h3>

              <strong>
                ₹
                {item.price.toLocaleString(
                  "en-IN"
                )}
              </strong>
            </div>

            <div className="quantity-controls">
              <button
                onClick={() =>
                  handleQuantityChange(
                    item.id,
                    item.quantity - 1
                  )
                }
              >
                −
              </button>

              <span>
                {item.quantity}
              </span>

              <button
                onClick={() =>
                  handleQuantityChange(
                    item.id,
                    item.quantity + 1
                  )
                }
              >
                +
              </button>
            </div>

            <button
              className="remove-button"
              onClick={() =>
                handleRemove(
                  item.id
                )
              }
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <h2>Order Summary</h2>

        <div className="cart-total">
          <span>Total</span>

          <strong>
            ₹
            {cartTotal.toLocaleString(
              "en-IN"
            )}
          </strong>
        </div>

        <Link
          to="/checkout"
          className="checkout-button"
        >
          Proceed to Checkout
        </Link>
      </div>
    </div>
  );
}

export default Cart;