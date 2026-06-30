import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api.js";
import { useAuth } from "../context/AuthContext.jsx";
import FieldCard from "../components/FieldCard.jsx";

export default function Home() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [fields, setFields] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [searching, setSearching] = useState(false);
  const [searchMode, setSearchMode] = useState("keyword"); // "keyword" | "semantic"

  const [newFieldName, setNewFieldName] = useState("");
  const [generating, setGenerating] = useState(false);
  const [generateError, setGenerateError] = useState(null);

  useEffect(() => {
    Promise.all([api.getFields(), api.getStats()])
      .then(([fieldsData, statsData]) => {
        setFields(fieldsData);
        setStats(statsData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleSearch(e) {
    e.preventDefault();
    if (query.trim().length < 2) return;
    setSearching(true);
    try {
      const res =
        searchMode === "semantic"
          ? await api.semanticSearch(query.trim())
          : await api.search(query.trim());
      setSearchResults(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setSearching(false);
    }
  }

  async function handleGenerate(e) {
    e.preventDefault();
    if (!newFieldName.trim()) return;
    setGenerateError(null);
    setGenerating(true);
    try {
      const field = await api.generateRoadmap(newFieldName.trim());
      navigate(`/field/${field.id}`);
    } catch (err) {
      setGenerateError(err.message);
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div>
      {/* HERO */}
      <section style={{ padding: "92px 0 64px" }}>
        <div className="container" style={{ textAlign: "center" }}>
          <p className="eyebrow" style={{ marginBottom: 18 }}>
            Curated • Link-rich • Production-grade
          </p>
          <h1
            style={{
              fontFamily: "var(--font-display)",
              fontWeight: 600,
              fontSize: "clamp(2.6rem, 6vw, 4.4rem)",
              lineHeight: 1.08,
              margin: "0 0 22px",
            }}
          >
            Master any engineering path,
            <br />
            <span className="gold-text">one roadmap at a time.</span>
          </h1>
          <p
            style={{
              color: "var(--text-secondary)",
              fontSize: "1.08rem",
              maxWidth: 580,
              margin: "0 auto 38px",
              lineHeight: 1.6,
            }}
          >
            Hand-picked stages, topics and authoritative articles for
            Python, MERN, Java, AWS and System Design — structured like a
            real engineering curriculum, not a random link dump.
          </p>

          <form
            onSubmit={handleSearch}
            style={{
              display: "flex",
              gap: 10,
              maxWidth: 480,
              margin: "0 auto 36px",
            }}
          >
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search topics — e.g. asyncio, JWT, sharding…"
              style={{
                flex: 1,
                padding: "13px 18px",
                borderRadius: 999,
                border: "1px solid var(--border-hairline-strong)",
                background: "rgba(255,255,255,0.03)",
                color: "var(--text-primary)",
                fontSize: "0.92rem",
                outline: "none",
              }}
            />
            <button type="submit" className="btn-gold">
              {searching ? "…" : "Search"}
            </button>
          </form>

          <div style={{ display: "flex", justifyContent: "center", gap: 8, marginTop: -22, marginBottom: 36 }}>
            {["keyword", "semantic"].map((mode) => (
              <button
                key={mode}
                type="button"
                onClick={() => setSearchMode(mode)}
                style={{
                  fontSize: "0.72rem",
                  padding: "4px 12px",
                  borderRadius: 999,
                  border: "1px solid var(--border-hairline)",
                  background: searchMode === mode ? "rgba(255,216,107,0.12)" : "transparent",
                  color: searchMode === mode ? "var(--gold-soft)" : "var(--text-muted)",
                  cursor: "pointer",
                  textTransform: "capitalize",
                }}
              >
                {mode === "semantic" ? "✨ Semantic" : "Keyword"}
              </button>
            ))}
          </div>

          {stats && (
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                gap: 44,
                flexWrap: "wrap",
              }}
            >
              {[
                ["Fields", stats.field_count],
                ["Topics", stats.topic_count],
                ["Resources", stats.resource_count],
                ["Hours mapped", stats.total_learning_hours],
              ].map(([label, value]) => (
                <div key={label} style={{ textAlign: "center" }}>
                  <div
                    className="gold-text"
                    style={{
                      fontFamily: "var(--font-display)",
                      fontSize: "2.1rem",
                      fontWeight: 700,
                    }}
                  >
                    {value}
                  </div>
                  <div
                    style={{
                      fontSize: "0.76rem",
                      color: "var(--text-muted)",
                      textTransform: "uppercase",
                      letterSpacing: "0.08em",
                    }}
                  >
                    {label}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* SEARCH RESULTS */}
      {searchResults && (
        <section className="container" style={{ marginBottom: 60 }}>
          <div className="glass-card" style={{ padding: 26 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 14 }}>
              <h3 style={{ fontFamily: "var(--font-display)", margin: 0, fontSize: "1.3rem" }}>
                {searchResults.result_count} results for "{searchResults.query}"
              </h3>
              <button
                onClick={() => {
                  setSearchResults(null);
                  setQuery("");
                }}
                className="btn-ghost"
                style={{ padding: "6px 16px", fontSize: "0.78rem" }}
              >
                Clear
              </button>
            </div>
            {searchResults.results.length === 0 && (
              <p style={{ color: "var(--text-muted)" }}>No matching topics. Try another keyword.</p>
            )}
            <div style={{ display: "grid", gap: 12 }}>
              {searchResults.results.map((r) => (
                <a
                  key={r.topic.id}
                  href={`/field/${r.field_id}`}
                  style={{
                    padding: "14px 18px",
                    borderRadius: 12,
                    background: "rgba(255,255,255,0.03)",
                    border: "1px solid var(--border-hairline)",
                  }}
                >
                  <div style={{ fontSize: "0.78rem", color: "var(--gold-soft)", marginBottom: 4, display: "flex", justifyContent: "space-between" }}>
                    <span>{r.field_name} → {r.stage_title}</span>
                    {r.relevance !== undefined && (
                      <span style={{ color: "var(--text-muted)" }}>{Math.round(r.relevance * 100)}% match</span>
                    )}
                  </div>
                  <div style={{ fontWeight: 600 }}>{r.topic.title}</div>
                  <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>
                    {r.topic.description}
                  </div>
                </a>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* AI ROADMAP GENERATOR */}
      <section className="container" style={{ marginBottom: 60 }}>
        <div
          className="glass-card"
          style={{
            padding: 30,
            background: "linear-gradient(135deg, rgba(169,140,255,0.08), rgba(255,216,107,0.05))",
          }}
        >
          <p className="eyebrow" style={{ marginBottom: 6 }}>✨ AI-Powered</p>
          <h3 style={{ fontFamily: "var(--font-display)", fontSize: "1.5rem", margin: "0 0 8px" }}>
            Don't see your field? Generate it.
          </h3>
          <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem", margin: "0 0 20px" }}>
            Type any career path — Claude will build a structured, link-rich roadmap for it on the fly.
          </p>

          {user ? (
            <form onSubmit={handleGenerate} style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <input
                value={newFieldName}
                onChange={(e) => setNewFieldName(e.target.value)}
                placeholder="e.g. Rust Developer, Data Engineer, iOS Developer…"
                style={{
                  flex: 1,
                  minWidth: 220,
                  padding: "12px 16px",
                  borderRadius: 10,
                  border: "1px solid var(--border-hairline-strong)",
                  background: "rgba(255,255,255,0.03)",
                  color: "var(--text-primary)",
                  fontSize: "0.9rem",
                  outline: "none",
                }}
              />
              <button type="submit" className="btn-gold" disabled={generating}>
                {generating ? "Generating…" : "Generate roadmap"}
              </button>
            </form>
          ) : (
            <p style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
              <a href="/login" style={{ color: "var(--gold-soft)", fontWeight: 600 }}>
                Log in
              </a>{" "}
              to generate a custom roadmap.
            </p>
          )}
          {generateError && (
            <p style={{ color: "#ff8a8a", fontSize: "0.82rem", marginTop: 12 }}>{generateError}</p>
          )}
        </div>
      </section>

      {/* FIELDS GRID */}
      <section className="container" style={{ paddingBottom: 100 }}>
        <h2
          style={{
            fontFamily: "var(--font-display)",
            fontSize: "1.9rem",
            marginBottom: 28,
            textAlign: "center",
          }}
        >
          Choose your <span className="gold-text">field</span>
        </h2>

        {error && (
          <p style={{ color: "#ff8a8a", textAlign: "center" }}>
            Couldn't reach the API ({error}). Make sure the backend is running on port 8000.
          </p>
        )}

        {loading ? (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
              gap: 22,
            }}
          >
            {[1, 2, 3].map((i) => (
              <div key={i} className="glass-card loading-shimmer" style={{ height: 230 }} />
            ))}
          </div>
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
              gap: 22,
            }}
          >
            {fields.map((field, i) => (
              <FieldCard key={field.id} field={field} index={i} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
