const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function getToken() {
  return localStorage.getItem("authToken");
}

async function request(path, options = {}) {
  const token = getToken();
  const headers = { ...options.headers };
  if (!(options.body instanceof URLSearchParams)) {
    headers["Content-Type"] = "application/json";
  }
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  // Roadmap content
  getFields: () => request("/api/v1/fields"),
  getField: (fieldId) => request(`/api/v1/fields/${fieldId}`),
  search: (q) => request(`/api/v1/search?q=${encodeURIComponent(q)}`),
  semanticSearch: (q) => request(`/api/v1/search/semantic?q=${encodeURIComponent(q)}`),
  getStats: () => request("/api/v1/stats"),

  // Auth
  register: (email, password, fullName) =>
    request("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, full_name: fullName }),
    }),
  login: (email, password) => {
    const form = new URLSearchParams();
    form.set("username", email);
    form.set("password", password);
    return request("/api/v1/auth/login", { method: "POST", body: form });
  },
  me: () => request("/api/v1/auth/me"),

  // Progress (requires auth)
  toggleTopic: (fieldId, topicId) =>
    request("/api/v1/progress/toggle", {
      method: "POST",
      body: JSON.stringify({ field_id: fieldId, topic_id: topicId }),
    }),
  getProgress: (fieldId) => request(`/api/v1/progress/${fieldId}`),
  getAllProgress: () => request("/api/v1/progress"),

  // Bookmarks (requires auth)
  toggleBookmark: (fieldId, topicId) =>
    request("/api/v1/bookmarks/toggle", {
      method: "POST",
      body: JSON.stringify({ field_id: fieldId, topic_id: topicId }),
    }),
  getBookmarks: () => request("/api/v1/bookmarks"),

  // PDF export
  exportPdfUrl: (fieldId) => `${BASE_URL}/api/v1/export/${fieldId}/pdf`,

  // AI features
  generateRoadmap: (fieldName) =>
    request("/api/v1/ai/generate-roadmap", {
      method: "POST",
      body: JSON.stringify({ field_name: fieldName }),
    }),
  summarizeTopic: (fieldId, topicId, forceRefresh = false) =>
    request("/api/v1/ai/summarize", {
      method: "POST",
      body: JSON.stringify({ field_id: fieldId, topic_id: topicId, force_refresh: forceRefresh }),
    }),
  chat: (message, fieldId) =>
    request("/api/v1/ai/chat", {
      method: "POST",
      body: JSON.stringify({ message, field_id: fieldId || null }),
    }),
  chatHistory: () => request("/api/v1/ai/chat/history"),

  // Streaming chat — returns a fetch Response so the caller can read the SSE body directly.
  // (Kept separate from `request()` because it doesn't parse JSON / isn't a one-shot call.)
  chatStream: (message, fieldId) => {
    const token = getToken();
    return fetch(`${BASE_URL}/api/v1/ai/chat/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ message, field_id: fieldId || null }),
    });
  },

  generateQuiz: (fieldId, topicId, forceRefresh = false) =>
    request("/api/v1/ai/quiz", {
      method: "POST",
      body: JSON.stringify({ field_id: fieldId, topic_id: topicId, force_refresh: forceRefresh }),
    }),

  generateResumeBullets: (fieldId) =>
    request("/api/v1/ai/resume-bullets", {
      method: "POST",
      body: JSON.stringify({ field_id: fieldId }),
    }),

  regenerateRoadmap: (fieldId) =>
    request(`/api/v1/ai/generated/${fieldId}/regenerate`, { method: "POST" }),
  deleteGeneratedRoadmap: (fieldId) =>
    request(`/api/v1/ai/generated/${fieldId}`, { method: "DELETE" }),
};

export { getToken, BASE_URL };
