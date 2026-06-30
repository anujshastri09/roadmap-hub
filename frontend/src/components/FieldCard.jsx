import { Link } from "react-router-dom";

export default function FieldCard({ field, index }) {
  return (
    <Link to={`/field/${field.id}`}>
      <div
        className="glass-card"
        style={{
          padding: 28,
          height: "100%",
          position: "relative",
          overflow: "hidden",
          animation: `fadeUp 0.6s ease ${index * 0.07}s both`,
        }}
      >
        <div
          style={{
            position: "absolute",
            top: -40,
            right: -40,
            width: 140,
            height: 140,
            borderRadius: "50%",
            background: field.color,
            opacity: 0.14,
            filter: "blur(30px)",
          }}
        />
        <div
          style={{
            fontSize: "2.1rem",
            marginBottom: 18,
            width: 56,
            height: 56,
            borderRadius: 14,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "rgba(255,255,255,0.04)",
            border: "1px solid var(--border-hairline)",
            position: "relative",
          }}
        >
          {field.icon}
          {field.ai_generated && (
            <span
              style={{
                position: "absolute",
                top: -8,
                right: -8,
                fontSize: "0.6rem",
                fontWeight: 700,
                padding: "2px 7px",
                borderRadius: 999,
                background: "var(--gold-grad)",
                color: "#1a1406",
              }}
            >
              AI
            </span>
          )}
        </div>

        <h3
          style={{
            fontFamily: "var(--font-display)",
            fontSize: "1.55rem",
            fontWeight: 600,
            margin: "0 0 8px",
          }}
        >
          {field.name}
        </h3>
        <p
          style={{
            color: "var(--text-secondary)",
            fontSize: "0.92rem",
            lineHeight: 1.5,
            margin: "0 0 22px",
            minHeight: 42,
          }}
        >
          {field.tagline}
        </p>

        <div style={{ display: "flex", gap: 18, fontSize: "0.78rem", color: "var(--text-muted)" }}>
          <span>{field.stage_count} stages</span>
          <span>{field.topic_count} topics</span>
          <span>{field.resource_count} resources</span>
        </div>

        <div
          style={{
            marginTop: 20,
            fontSize: "0.85rem",
            fontWeight: 600,
            color: "var(--gold-soft)",
            display: "flex",
            alignItems: "center",
            gap: 6,
          }}
        >
          Explore roadmap <span style={{ transition: "transform 0.2s" }}>→</span>
        </div>
      </div>
    </Link>
  );
}
