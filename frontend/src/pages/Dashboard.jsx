import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { api } from "../api.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function Dashboard() {
  const { user } = useAuth();
  const [overview, setOverview] = useState([]);
  const [bookmarks, setBookmarks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.getAllProgress(), api.getBookmarks()])
      .then(([progressRes, bookmarksRes]) => {
        setOverview(progressRes.overview);
        setBookmarks(bookmarksRes.bookmarks);
      })
      .finally(() => setLoading(false));
  }, []);

  const totalCompleted = overview.reduce((sum, f) => sum + f.completed_count, 0);
  const totalTopics = overview.reduce((sum, f) => sum + f.total_topics, 0);

  return (
    <div className="container" style={{ padding: "60px 28px 100px" }}>
      <p className="eyebrow">Your space</p>
      <h1 style={{ fontFamily: "var(--font-display)", fontSize: "2.4rem", margin: "8px 0 6px" }}>
        Welcome, <span className="gold-text">{user?.full_name || user?.email}</span>
      </h1>
      <p style={{ color: "var(--text-secondary)", marginBottom: 40 }}>
        {totalCompleted} of {totalTopics} topics completed across all fields.
      </p>

      {loading ? (
        <div className="glass-card loading-shimmer" style={{ height: 300 }} />
      ) : (
        <>
          <div className="glass-card" style={{ padding: 28, marginBottom: 32 }}>
            <h3 style={{ fontFamily: "var(--font-display)", marginTop: 0, fontSize: "1.3rem" }}>
              Completion by field
            </h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={overview} margin={{ top: 10, right: 10, left: -10, bottom: 10 }}>
                <XAxis
                  dataKey="field_name"
                  stroke="var(--text-muted)"
                  fontSize={11}
                  tickLine={false}
                  interval={0}
                  angle={-15}
                  textAnchor="end"
                  height={60}
                />
                <YAxis stroke="var(--text-muted)" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    background: "var(--surface-solid)",
                    border: "1px solid var(--border-hairline-strong)",
                    borderRadius: 10,
                    color: "var(--text-primary)",
                  }}
                />
                <Bar dataKey="percent_complete" radius={[8, 8, 0, 0]}>
                  {overview.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
              gap: 18,
              marginBottom: 40,
            }}
          >
            {overview.map((f) => (
              <Link key={f.field_id} to={`/field/${f.field_id}`} className="glass-card" style={{ padding: 20 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                  <span style={{ fontSize: "1.4rem" }}>{f.icon}</span>
                  <strong>{f.field_name}</strong>
                </div>
                <div style={{ height: 6, borderRadius: 999, background: "rgba(255,255,255,0.06)", overflow: "hidden" }}>
                  <div
                    style={{
                      height: "100%",
                      width: `${f.percent_complete}%`,
                      background: f.color,
                    }}
                  />
                </div>
                <div style={{ fontSize: "0.78rem", color: "var(--text-muted)", marginTop: 8 }}>
                  {f.completed_count}/{f.total_topics} topics · {f.percent_complete}%
                </div>
                <a
                  href={api.exportPdfUrl(f.field_id)}
                  onClick={(e) => e.stopPropagation()}
                  style={{
                    display: "inline-block",
                    marginTop: 12,
                    fontSize: "0.78rem",
                    color: "var(--gold-soft)",
                    fontWeight: 600,
                  }}
                >
                  ↓ Export PDF report
                </a>
              </Link>
            ))}
          </div>

          <h3 style={{ fontFamily: "var(--font-display)", fontSize: "1.4rem", marginBottom: 16 }}>
            Bookmarked topics
          </h3>
          {bookmarks.length === 0 ? (
            <p style={{ color: "var(--text-muted)" }}>
              No bookmarks yet — star a topic on any roadmap page to save it here.
            </p>
          ) : (
            <div style={{ display: "grid", gap: 12 }}>
              {bookmarks.map((b) => (
                <Link
                  key={b.topic.id}
                  to={`/field/${b.field_id}`}
                  className="glass-card"
                  style={{ padding: "14px 18px" }}
                >
                  <div style={{ fontSize: "0.78rem", color: "var(--gold-soft)" }}>{b.field_name}</div>
                  <div style={{ fontWeight: 600 }}>{b.topic.title}</div>
                </Link>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
