export default function Footer() {
  return (
    <footer
      style={{
        borderTop: "1px solid var(--border-hairline)",
        marginTop: 80,
        padding: "36px 0",
      }}
    >
      <div
        className="container"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <span style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
          Roadmap Hub — curated career paths, built with FastAPI &amp; React.
        </span>
        <span style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
          Crafted for engineers who ship.
        </span>
      </div>
    </footer>
  );
}
