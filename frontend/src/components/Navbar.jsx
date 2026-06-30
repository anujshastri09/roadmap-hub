import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useTheme } from "../context/ThemeContext.jsx";

export default function Navbar() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  return (
    <header
      style={{
        position: "sticky",
        top: 0,
        zIndex: 50,
        backdropFilter: "blur(16px)",
        background: "rgba(8, 7, 11, 0.72)",
        borderBottom: "1px solid var(--border-hairline)",
      }}
    >
      <div
        className="container"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          height: 74,
        }}
      >
        <Link to="/" style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span
            style={{
              width: 34,
              height: 34,
              borderRadius: 10,
              background: "var(--gold-grad)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 16,
              boxShadow: "0 6px 18px rgba(255,216,107,0.25)",
            }}
          >
            ✦
          </span>
          <span
            style={{
              fontFamily: "var(--font-display)",
              fontSize: "1.45rem",
              fontWeight: 600,
              letterSpacing: "0.01em",
            }}
          >
            Roadmap <span className="gold-text">Hub</span>
          </span>
        </Link>

        <nav style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <Link to="/" style={{ fontSize: "0.9rem", color: "var(--text-secondary)", fontWeight: 500 }}>
            Fields
          </Link>

          {user && (
            <Link to="/dashboard" style={{ fontSize: "0.9rem", color: "var(--text-secondary)", fontWeight: 500 }}>
              Dashboard
            </Link>
          )}

          <button
            onClick={toggleTheme}
            title="Toggle theme"
            className="btn-ghost"
            style={{ padding: "8px 14px", fontSize: "0.85rem" }}
          >
            {theme === "dark" ? "☀️" : "🌙"}
          </button>

          {user ? (
            <button
              onClick={() => {
                logout();
                navigate("/");
              }}
              className="btn-ghost"
              style={{ padding: "8px 18px", fontSize: "0.85rem" }}
            >
              Logout
            </button>
          ) : (
            <>
              <Link to="/login" className="btn-ghost" style={{ padding: "8px 18px", fontSize: "0.85rem" }}>
                Log in
              </Link>
              <Link to="/register" className="btn-gold" style={{ padding: "8px 18px", fontSize: "0.85rem" }}>
                Sign up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
