import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { api } from "../api.js";
import { useAuth } from "../context/AuthContext.jsx";

const RESOURCE_ICON = {
  article: "📄",
  docs: "📘",
  video: "🎬",
  course: "🎓",
  practice: "🛠️",
};

export default function FieldDetail() {
  const { fieldId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [field, setField] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [completed, setCompleted] = useState(new Set());
  const [bookmarked, setBookmarked] = useState(new Set());
  const [summaries, setSummaries] = useState({});
  const [summarizing, setSummarizing] = useState(null);
  const [quizzes, setQuizzes] = useState({});
  const [quizzing, setQuizzing] = useState(null);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [resumeBullets, setResumeBullets] = useState(null);
  const [generatingBullets, setGeneratingBullets] = useState(false);
  const [moderating, setModerating] = useState(false);

  useEffect(() => {
    setLoading(true);
    api
      .getField(fieldId)
      .then(setField)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [fieldId]);

  useEffect(() => {
    if (!user) return;
    api
      .getProgress(fieldId)
      .then((res) => setCompleted(new Set(res.completed_topic_ids)))
      .catch(() => {});
    api
      .getBookmarks()
      .then((res) =>
        setBookmarked(
          new Set(
            res.bookmarks.filter((b) => b.field_id === fieldId).map((b) => b.topic.id)
          )
        )
      )
      .catch(() => {});
  }, [user, fieldId]);

  async function toggleTopic(topicId) {
    if (!user) return;
    const next = new Set(completed);
    next.has(topicId) ? next.delete(topicId) : next.add(topicId);
    setCompleted(next);
    try {
      await api.toggleTopic(fieldId, topicId);
    } catch {
      setCompleted(completed);
    }
  }

  async function toggleBookmark(topicId) {
    if (!user) return;
    const next = new Set(bookmarked);
    next.has(topicId) ? next.delete(topicId) : next.add(topicId);
    setBookmarked(next);
    try {
      await api.toggleBookmark(fieldId, topicId);
    } catch {
      setBookmarked(bookmarked);
    }
  }

  async function handleSummarize(topicId) {
    if (!user || summaries[topicId]) return;
    setSummarizing(topicId);
    try {
      const res = await api.summarizeTopic(fieldId, topicId);
      setSummaries((s) => ({ ...s, [topicId]: res.summary }));
    } catch (err) {
      setSummaries((s) => ({ ...s, [topicId]: `⚠️ ${err.message}` }));
    } finally {
      setSummarizing(null);
    }
  }

  async function handleQuiz(topicId) {
    if (!user) return;
    if (quizzes[topicId]) {
      // toggle visibility off by clearing
      setQuizzes((q) => {
        const copy = { ...q };
        delete copy[topicId];
        return copy;
      });
      return;
    }
    setQuizzing(topicId);
    try {
      const res = await api.generateQuiz(fieldId, topicId);
      setQuizzes((q) => ({ ...q, [topicId]: res.questions }));
    } catch (err) {
      setQuizzes((q) => ({ ...q, [topicId]: { error: err.message } }));
    } finally {
      setQuizzing(null);
    }
  }

  function selectQuizAnswer(topicId, questionIndex, optionIndex) {
    setQuizAnswers((a) => ({
      ...a,
      [`${topicId}-${questionIndex}`]: optionIndex,
    }));
  }

  async function handleGenerateBullets() {
    if (!user) return;
    setGeneratingBullets(true);
    try {
      const res = await api.generateResumeBullets(fieldId);
      setResumeBullets(res.bullets);
    } catch (err) {
      setResumeBullets([`⚠️ ${err.message}`]);
    } finally {
      setGeneratingBullets(false);
    }
  }

  async function handleRegenerate() {
    if (!user) return;
    setModerating(true);
    try {
      const updated = await api.regenerateRoadmap(fieldId);
      setField(updated);
      setCompleted(new Set());
      setSummaries({});
      setQuizzes({});
    } catch (err) {
      setError(err.message);
    } finally {
      setModerating(false);
    }
  }

  async function handleDeleteGenerated() {
    if (!user) return;
    if (!window.confirm("Permanently delete this AI-generated roadmap?")) return;
    setModerating(true);
    try {
      await api.deleteGeneratedRoadmap(fieldId);
      navigate("/");
    } catch (err) {
      setError(err.message);
      setModerating(false);
    }
  }

  if (loading) {
    return (
      <div className="container" style={{ padding: "80px 0" }}>
        <div className="glass-card loading-shimmer" style={{ height: 300 }} />
      </div>
    );
  }

  if (error || !field) {
    return (
      <div className="container" style={{ padding: "80px 0", textAlign: "center" }}>
        <p style={{ color: "#ff8a8a" }}>{error || "Field not found"}</p>
        <Link to="/" className="btn-ghost" style={{ marginTop: 16, display: "inline-flex" }}>
          ← Back home
        </Link>
      </div>
    );
  }

  const totalTopics = field.stages.reduce((sum, s) => sum + s.topics.length, 0);
  const percent = totalTopics ? Math.round((completed.size / totalTopics) * 100) : 0;

  return (
    <div>
      <section style={{ padding: "60px 0 30px" }}>
        <div className="container">
          <Link to="/" style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
            ← All fields
          </Link>
          <div style={{ display: "flex", alignItems: "center", gap: 18, marginTop: 18, flexWrap: "wrap" }}>
            <span style={{ fontSize: "2.6rem" }}>{field.icon}</span>
            <div style={{ flex: 1 }}>
              <h1 style={{ fontFamily: "var(--font-display)", fontSize: "2.4rem", margin: 0, fontWeight: 600 }}>
                {field.name}
              </h1>
              <p style={{ color: "var(--text-secondary)", margin: "4px 0 0" }}>{field.tagline}</p>
            </div>
            {user && (
              <a href={api.exportPdfUrl(fieldId)} className="btn-ghost" style={{ fontSize: "0.85rem" }}>
                ↓ Export PDF report
              </a>
            )}
            {user && field.ai_generated && (
              <button
                onClick={handleRegenerate}
                disabled={moderating}
                className="btn-ghost"
                style={{ fontSize: "0.85rem" }}
                title="Discard this AI-generated roadmap and regenerate it"
              >
                {moderating ? "Working…" : "↻ Regenerate (AI)"}
              </button>
            )}
            {user && field.ai_generated && (
              <button
                onClick={handleDeleteGenerated}
                disabled={moderating}
                className="btn-ghost"
                style={{ fontSize: "0.85rem", color: "#ff8a8a", borderColor: "rgba(255,138,138,0.3)" }}
                title="Permanently delete this AI-generated roadmap"
              >
                🗑 Delete
              </button>
            )}
          </div>

          {user ? (
            <div style={{ marginTop: 28, maxWidth: 420 }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  fontSize: "0.78rem",
                  color: "var(--text-muted)",
                  marginBottom: 6,
                }}
              >
                <span>Your progress</span>
                <span>{completed.size} / {totalTopics} topics</span>
              </div>
              <div style={{ height: 8, borderRadius: 999, background: "rgba(255,255,255,0.06)", overflow: "hidden" }}>
                <div
                  style={{
                    height: "100%",
                    width: `${percent}%`,
                    background: "var(--gold-grad)",
                    transition: "width 0.5s ease",
                  }}
                />
              </div>

              {completed.size > 0 && (
                <div style={{ marginTop: 18 }}>
                  <button onClick={handleGenerateBullets} disabled={generatingBullets} className="btn-ghost" style={{ fontSize: "0.78rem" }}>
                    {generatingBullets ? "Writing bullets…" : "✨ Generate resume bullets from my progress"}
                  </button>
                  {resumeBullets && (
                    <ul style={{ marginTop: 14, paddingLeft: 18, display: "grid", gap: 8 }}>
                      {resumeBullets.map((b, i) => (
                        <li key={i} style={{ fontSize: "0.86rem", color: "var(--text-secondary)", lineHeight: 1.5 }}>
                          {b}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </div>
          ) : (
            <p style={{ marginTop: 22, fontSize: "0.85rem", color: "var(--text-muted)" }}>
              <Link to="/login" style={{ color: "var(--gold-soft)", fontWeight: 600 }}>
                Log in
              </Link>{" "}
              to track your progress and bookmark topics.
            </p>
          )}
        </div>
      </section>

      <section className="container" style={{ paddingBottom: 100 }}>
        <div style={{ position: "relative", marginTop: 30 }}>
          <div
            style={{
              position: "absolute",
              left: 27,
              top: 14,
              bottom: 14,
              width: 2,
              background: "linear-gradient(to bottom, var(--gold-soft), rgba(232,199,102,0.05))",
            }}
          />
          {field.stages
            .sort((a, b) => a.order - b.order)
            .map((stage) => (
              <div key={stage.id} style={{ marginBottom: 50, position: "relative", paddingLeft: 70 }}>
                <div
                  style={{
                    position: "absolute",
                    left: 12,
                    top: 0,
                    width: 32,
                    height: 32,
                    borderRadius: "50%",
                    background: "var(--gold-grad)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontWeight: 700,
                    fontSize: "0.85rem",
                    color: "#1a1406",
                    boxShadow: "0 0 0 6px var(--bg-void)",
                  }}
                >
                  {stage.order}
                </div>

                <h2 style={{ fontFamily: "var(--font-display)", fontSize: "1.7rem", margin: "2px 0 2px" }}>
                  {stage.title}
                </h2>
                <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginBottom: 22 }}>
                  {stage.subtitle}
                </p>

                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 18 }}>
                  {stage.topics.map((topic) => {
                    const isDone = completed.has(topic.id);
                    const isBookmarked = bookmarked.has(topic.id);
                    return (
                      <div
                        key={topic.id}
                        className="glass-card"
                        style={{ padding: 22, borderColor: isDone ? "var(--gold-bright)" : undefined }}
                      >
                        <div style={{ display: "flex", justifyContent: "space-between", gap: 10 }}>
                          <h3 style={{ fontSize: "1.05rem", margin: "0 0 6px", fontWeight: 700 }}>
                            {topic.title}
                          </h3>
                          <div style={{ display: "flex", gap: 6, flexShrink: 0 }}>
                            <button
                              onClick={() => toggleBookmark(topic.id)}
                              title={isBookmarked ? "Remove bookmark" : "Bookmark"}
                              disabled={!user}
                              style={{
                                width: 26,
                                height: 26,
                                borderRadius: 8,
                                border: "1px solid var(--border-hairline-strong)",
                                background: isBookmarked ? "rgba(255,216,107,0.15)" : "transparent",
                                color: "var(--gold-soft)",
                                cursor: user ? "pointer" : "not-allowed",
                                fontSize: "0.78rem",
                              }}
                            >
                              {isBookmarked ? "★" : "☆"}
                            </button>
                            <button
                              onClick={() => toggleTopic(topic.id)}
                              title={isDone ? "Mark incomplete" : "Mark complete"}
                              disabled={!user}
                              style={{
                                width: 26,
                                height: 26,
                                borderRadius: "50%",
                                border: isDone ? "none" : "1px solid var(--border-hairline-strong)",
                                background: isDone ? "var(--gold-grad)" : "transparent",
                                color: isDone ? "#1a1406" : "var(--text-muted)",
                                cursor: user ? "pointer" : "not-allowed",
                                fontSize: "0.8rem",
                                fontWeight: 700,
                              }}
                            >
                              {isDone ? "✓" : ""}
                            </button>
                          </div>
                        </div>
                        <p style={{ color: "var(--text-secondary)", fontSize: "0.86rem", lineHeight: 1.5, margin: "0 0 12px" }}>
                          {topic.description}
                        </p>

                        {user && (
                          <div style={{ marginBottom: 12 }}>
                            {summaries[topic.id] ? (
                              <p
                                style={{
                                  fontSize: "0.8rem",
                                  color: "var(--violet, #a98cff)",
                                  background: "rgba(169,140,255,0.08)",
                                  border: "1px solid rgba(169,140,255,0.2)",
                                  borderRadius: 8,
                                  padding: "8px 10px",
                                  lineHeight: 1.4,
                                  margin: "0 0 8px",
                                }}
                              >
                                ✨ {summaries[topic.id]}
                              </p>
                            ) : (
                              <button
                                onClick={() => handleSummarize(topic.id)}
                                disabled={summarizing === topic.id}
                                style={{
                                  fontSize: "0.74rem",
                                  color: "var(--violet, #a98cff)",
                                  background: "none",
                                  border: "1px dashed rgba(169,140,255,0.4)",
                                  borderRadius: 999,
                                  padding: "4px 12px",
                                  marginRight: 6,
                                  marginBottom: 8,
                                  cursor: "pointer",
                                }}
                              >
                                {summarizing === topic.id ? "Summarizing…" : "✨ AI quick summary"}
                              </button>
                            )}

                            <button
                              onClick={() => handleQuiz(topic.id)}
                              disabled={quizzing === topic.id}
                              style={{
                                fontSize: "0.74rem",
                                color: "var(--gold-soft)",
                                background: "none",
                                border: "1px dashed var(--border-hairline-strong)",
                                borderRadius: 999,
                                padding: "4px 12px",
                                marginBottom: 8,
                                cursor: "pointer",
                              }}
                            >
                              {quizzing === topic.id
                                ? "Generating quiz…"
                                : quizzes[topic.id]
                                ? "Hide quiz"
                                : "📝 Practice quiz"}
                            </button>

                            {quizzes[topic.id] && !quizzes[topic.id].error && (
                              <div style={{ display: "grid", gap: 10, marginTop: 8 }}>
                                {quizzes[topic.id].map((q, qi) => {
                                  const answerKey = `${topic.id}-${qi}`;
                                  const selected = quizAnswers[answerKey];
                                  return (
                                    <div
                                      key={qi}
                                      style={{
                                        background: "rgba(255,255,255,0.03)",
                                        border: "1px solid var(--border-hairline)",
                                        borderRadius: 8,
                                        padding: 10,
                                      }}
                                    >
                                      <p style={{ fontSize: "0.82rem", fontWeight: 600, margin: "0 0 8px" }}>
                                        {qi + 1}. {q.question}
                                      </p>
                                      <div style={{ display: "grid", gap: 5 }}>
                                        {q.options.map((opt, oi) => {
                                          const isSelected = selected === oi;
                                          const isCorrect = oi === q.correct_index;
                                          let bg = "transparent";
                                          if (selected !== undefined) {
                                            if (isCorrect) bg = "rgba(33,217,166,0.15)";
                                            else if (isSelected) bg = "rgba(255,138,138,0.15)";
                                          }
                                          return (
                                            <button
                                              key={oi}
                                              onClick={() => selectQuizAnswer(topic.id, qi, oi)}
                                              disabled={selected !== undefined}
                                              style={{
                                                textAlign: "left",
                                                fontSize: "0.78rem",
                                                padding: "6px 10px",
                                                borderRadius: 6,
                                                border: "1px solid var(--border-hairline)",
                                                background: bg,
                                                color: "var(--text-primary)",
                                                cursor: selected === undefined ? "pointer" : "default",
                                              }}
                                            >
                                              {opt}
                                            </button>
                                          );
                                        })}
                                      </div>
                                      {selected !== undefined && (
                                        <p style={{ fontSize: "0.74rem", color: "var(--text-muted)", margin: "8px 0 0" }}>
                                          {q.explanation}
                                        </p>
                                      )}
                                    </div>
                                  );
                                })}
                              </div>
                            )}
                          </div>
                        )}


                        <div style={{ display: "flex", gap: 10, fontSize: "0.72rem", color: "var(--text-muted)", marginBottom: 14 }}>
                          <span style={{ padding: "3px 9px", borderRadius: 999, background: "rgba(255,255,255,0.05)", textTransform: "capitalize" }}>
                            {topic.level}
                          </span>
                          <span style={{ alignSelf: "center" }}>~{topic.estimated_hours}h</span>
                        </div>
                        <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
                          {topic.resources.map((r) => (
                            <a
                              key={r.url}
                              href={r.url}
                              target="_blank"
                              rel="noreferrer"
                              style={{ fontSize: "0.83rem", color: "var(--gold-soft)", display: "flex", alignItems: "center", gap: 7 }}
                            >
                              <span>{RESOURCE_ICON[r.type] || "🔗"}</span>
                              <span style={{ textDecoration: "underline", textUnderlineOffset: 3 }}>{r.title}</span>
                            </a>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
        </div>
      </section>
    </div>
  );
}
