import { useCart } from "../CartContext";
import { Link } from "react-router-dom";

function Cart() {
  const {
    cart,
    removeFromCart,
    updateQuantity,
    cartTotal,
  } = useCart();

  if (cart.length === 0) {
    return (
      <div className="cart-page">
        <h1>Your Cart</h1>
        <p>Your cart is currently empty.</p>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <h1>Your Cart</h1>

      <div className="cart-items">
        {cart.map((item) => (
          <div className="cart-item" key={item.id}>
            <div>
              <p className="product-category">
                {item.category}
              </p>

              <h3>{item.name}</h3>

              <strong>
                ₹{item.price.toLocaleString("en-IN")}
              </strong>
            </div>

            <div className="quantity-controls">
              <button
                onClick={() =>
                  updateQuantity(
                    item.id,
                    item.quantity - 1
                  )
                }
              >
                −
              </button>

              <span>{item.quantity}</span>

              <button
                onClick={() =>
                  updateQuantity(
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
                removeFromCart(item.id)
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
            ₹{cartTotal.toLocaleString("en-IN")}
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