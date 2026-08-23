import { Routes, Route, Link } from "react-router-dom";
import { useCart } from "./CartContext";
import products from "./data/products";
import Cart from "./pages/Cart";
import "./App.css";
import Checkout from "./pages/Checkout";

function Store() {
  const { addToCart, cartCount } = useCart();

  return (
    <>
      <section className="hero">
        <p className="eyebrow">AI-POWERED COMMERCE</p>

        <h1>
          Shop smarter.
          <br />
          Checkout with confidence.
        </h1>

        <p className="hero-text">
          A smarter shopping experience powered by AI.
        </p>

        <a href="#products">
          <button className="primary-button">
            Explore Products
          </button>
        </a>
      </section>

      <section
        className="products-section"
        id="products"
      >
        <div className="section-heading">
          <p className="eyebrow">
            FEATURED PRODUCTS
          </p>

          <h2>Popular right now</h2>
        </div>

        <div className="product-grid">
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onAddToCart={addToCart}
            />
          ))}
        </div>
      </section>
    </>
  );
}

function ProductCard({
  product,
  onAddToCart,
}) {
  return (
    <article className="product-card">
      <div className="product-image">
        <span>{product.category}</span>
      </div>

      <div className="product-info">
        <p className="product-category">
          {product.category}
        </p>

        <h3>{product.name}</h3>

        <div className="product-bottom">
          <strong>
            ₹{product.price.toLocaleString("en-IN")}
          </strong>

          <button
            className="cart-button"
            onClick={() => onAddToCart(product)}
          >
            Add to Cart
          </button>
        </div>
      </div>
    </article>
  );
}

function App() {
  const { cartCount } = useCart();

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo">
          <Link to="/">
            Second<span>Chance</span>
          </Link>
        </div>

        <nav>
          <Link to="/">Home</Link>

          <Link to="/#products">
            Products
          </Link>

          <Link to="/cart">
            Cart 🛒 ({cartCount})
          </Link>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Store />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/checkout"element={<Checkout />}/>
        </Routes>
      </main>
    </div>
  );
}

export default App;