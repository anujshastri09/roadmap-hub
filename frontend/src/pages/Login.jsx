import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="container" style={{ maxWidth: 420, padding: "90px 28px" }}>
      <h1 style={{ fontFamily: "var(--font-display)", fontSize: "2.2rem", marginBottom: 8 }}>
        Welcome <span className="gold-text">back</span>
      </h1>
      <p style={{ color: "var(--text-secondary)", marginBottom: 32 }}>
        Log in to track your progress and export reports.
      </p>

      <form onSubmit={handleSubmit} className="glass-card" style={{ padding: 28, display: "grid", gap: 16 }}>
        <input
          type="email"
          required
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={inputStyle}
        />
        <input
          type="password"
          required
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={inputStyle}
        />
        {error && <p style={{ color: "#ff8a8a", fontSize: "0.85rem", margin: 0 }}>{error}</p>}
        <button type="submit" className="btn-gold" disabled={submitting}>
          {submitting ? "Logging in…" : "Log in"}
        </button>
      </form>

      <p style={{ marginTop: 18, fontSize: "0.88rem", color: "var(--text-muted)" }}>
        No account?{" "}
        <Link to="/register" style={{ color: "var(--gold-soft)", fontWeight: 600 }}>
          Create one
        </Link>
      </p>
    </div>
  );
}

const inputStyle = {
  padding: "12px 16px",
  borderRadius: 10,
  border: "1px solid var(--border-hairline-strong)",
  background: "rgba(255,255,255,0.03)",
  color: "var(--text-primary)",
  fontSize: "0.92rem",
  outline: "none",
};
