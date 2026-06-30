import { useState, useRef, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { api } from "../api.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function ChatWidget() {
  const { user } = useAuth();
  const location = useLocation();
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! Ask me anything about your career path — I can ground answers in the roadmap you're viewing." },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const scrollRef = useRef(null);

  const fieldIdMatch = location.pathname.match(/^\/field\/([^/]+)/);
  const activeFieldId = fieldIdMatch ? fieldIdMatch[1] : null;

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, open]);

  if (!user) return null;

  async function send(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text || sending) return;
    setMessages((m) => [...m, { role: "user", content: text }, { role: "assistant", content: "" }]);
    setInput("");
    setSending(true);

    try {
      const res = await api.chatStream(text, activeFieldId);
      if (!res.ok || !res.body) {
        throw new Error("Assistant is unavailable right now.");
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        // SSE frames are separated by a blank line; each starts with "data: "
        const frames = buffer.split("\n\n");
        buffer = frames.pop(); // keep the last (possibly incomplete) frame in the buffer
        for (const frame of frames) {
          const line = frame.replace(/^data:\s*/, "").trim();
          if (!line) continue;
          const payload = JSON.parse(line);
          if (payload.delta) {
            setMessages((m) => {
              const copy = [...m];
              copy[copy.length - 1] = {
                role: "assistant",
                content: copy[copy.length - 1].content + payload.delta,
              };
              return copy;
            });
          } else if (payload.error) {
            setMessages((m) => {
              const copy = [...m];
              copy[copy.length - 1] = { role: "assistant", content: `⚠️ ${payload.error}` };
              return copy;
            });
          }
        }
      }
    } catch (err) {
      setMessages((m) => {
        const copy = [...m];
        copy[copy.length - 1] = { role: "assistant", content: `⚠️ ${err.message || "Something went wrong."}` };
        return copy;
      });
    } finally {
      setSending(false);
    }
  }

  return (
    <div style={{ position: "fixed", bottom: 24, right: 24, zIndex: 100 }}>
      {open && (
        <div
          className="glass-card"
          style={{
            width: 340,
            height: 440,
            marginBottom: 14,
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
            background: "var(--surface-solid)",
          }}
        >
          <div
            style={{
              padding: "14px 18px",
              borderBottom: "1px solid var(--border-hairline)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <div>
              <strong style={{ fontSize: "0.92rem" }}>Career Assistant</strong>
              {activeFieldId && (
                <div style={{ fontSize: "0.7rem", color: "var(--gold-soft)" }}>
                  Grounded in this roadmap
                </div>
              )}
            </div>
            <button
              onClick={() => setOpen(false)}
              style={{ background: "none", border: "none", color: "var(--text-muted)", cursor: "pointer", fontSize: "1rem" }}
            >
              ✕
            </button>
          </div>

          <div ref={scrollRef} style={{ flex: 1, overflowY: "auto", padding: 14, display: "flex", flexDirection: "column", gap: 10 }}>
            {messages.map((m, i) => (
              <div
                key={i}
                style={{
                  alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                  maxWidth: "85%",
                  padding: "9px 13px",
                  borderRadius: 12,
                  fontSize: "0.84rem",
                  lineHeight: 1.45,
                  background: m.role === "user" ? "var(--gold-grad)" : "rgba(255,255,255,0.05)",
                  color: m.role === "user" ? "#1a1406" : "var(--text-primary)",
                }}
              >
                {m.content}
              </div>
            ))}
            {sending && messages[messages.length - 1]?.content === "" && (
              <div style={{ alignSelf: "flex-start", fontSize: "0.8rem", color: "var(--text-muted)" }}>
                Thinking…
              </div>
            )}
          </div>

          <form onSubmit={send} style={{ display: "flex", borderTop: "1px solid var(--border-hairline)" }}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about your roadmap…"
              style={{
                flex: 1,
                border: "none",
                background: "transparent",
                color: "var(--text-primary)",
                padding: "12px 14px",
                fontSize: "0.85rem",
                outline: "none",
              }}
            />
            <button
              type="submit"
              disabled={sending}
              style={{
                background: "none",
                border: "none",
                color: "var(--gold-soft)",
                padding: "0 16px",
                cursor: "pointer",
                fontWeight: 700,
              }}
            >
              →
            </button>
          </form>
        </div>
      )}

      <button
        onClick={() => setOpen((o) => !o)}
        className="btn-gold"
        style={{
          width: 56,
          height: 56,
          borderRadius: "50%",
          padding: 0,
          fontSize: "1.3rem",
          float: "right",
        }}
        title="Career Assistant"
      >
        {open ? "✕" : "💬"}
      </button>
    </div>
  );
}
