# Roadmap Hub

A full-stack platform that turns any engineering career path — Python, MERN, Java, AWS, System Design — into a structured, link-rich roadmap with stages, topics, curated resources and per-user progress tracking.

Built as a portfolio-grade project: **FastAPI** backend, **React (Vite)** frontend with a custom "midnight & gold" luxury UI.

## ✨ Features

- 5 curated career roadmaps, each broken into ordered stages → topics → resources
- **JWT authentication** — register/login, password hashing with bcrypt
- **Real database** (SQLite via SQLAlchemy) for users, progress, and bookmarks — easy to swap for PostgreSQL by changing `DATABASE_URL`
- Per-user progress tracking and a cross-field **dashboard** with a recharts completion graph
- **Bookmarks** — star any topic, see them all in your dashboard
- **PDF export** — download a polished progress report per field (built with ReportLab)
- **AI-powered features (Claude API)**:
  - *Roadmap Generator* — type any career field not in the curated set and Claude generates a full structured roadmap (stages/topics/resources), cached in the DB and merged into the public field list
  - *Roadmap Moderation* — regenerate or permanently delete a low-quality AI-generated roadmap
  - *Topic Quick Summary* — on-demand AI summary per topic, cached so it's only ever generated once
  - *Practice Quiz Generator* — on-demand 4-question multiple-choice quiz per topic with instant feedback, cached per topic
  - *Resume Bullet Generator* — turns a user's actually-completed topics into professional, achievement-oriented resume bullet points
  - *Career Chat Assistant* — RAG-lite conversational assistant grounded in the roadmap you're viewing, with **token-by-token streaming** (Server-Sent Events) and short-term chat memory persisted per user
  - *Semantic Search* — a dependency-free TF-IDF + cosine-similarity search engine (`app/semantic_search.py`) that matches topics by meaning/word-importance rather than exact substring, alongside the original keyword search
- Light/dark **theme toggle** ("midnight gold" / "ivory gold")
- Lightweight in-process **rate limiting** and structured request **logging** middleware
- **Pytest test suite** covering roadmap, auth, and progress endpoints
- **GitHub Actions CI** — runs backend tests and a frontend production build on every push
- Polished React UI: glassmorphism cards, gold-gradient accents, animated stage timeline
- Fully typed backend models (Pydantic) and OpenAPI docs out of the box (`/docs`)
- Dockerized for one-command deployment

## 🏗️ Architecture

```
career-roadmap-hub/
├── .github/workflows/ci.yml  GitHub Actions: backend tests + frontend build
├── backend/                  FastAPI service
│   ├── app/
│   │   ├── main.py           App entrypoint, CORS, rate limit, logging, routers
│   │   ├── models.py         Pydantic schemas (roadmap + auth + bookmarks)
│   │   ├── database.py       SQLAlchemy engine/session
│   │   ├── db_models.py      ORM models: User, TopicProgress, Bookmark
│   │   ├── security.py       Password hashing + JWT creation/verification
│   │   ├── deps.py           get_current_user / get_current_admin dependencies
│   │   ├── middleware.py     In-process rate limiter
│   │   ├── ai_client.py      Anthropic (Claude) API wrapper — single-turn + chat + streaming + JSON parsing
│   │   ├── semantic_search.py TF-IDF + cosine-similarity search engine (no external ML deps)
│   │   ├── data/              Roadmap content per field (static, version-controlled)
│   │   └── routers/
│   │       ├── auth.py        /auth/register, /auth/login, /auth/me
│   │       ├── roadmap.py     /fields, /search, /stats (merges curated + AI-generated fields)
│   │       ├── progress.py    Per-user, DB-backed completion tracking
│   │       ├── bookmarks.py   Star/unstar topics
│   │       ├── export.py      PDF report generation
│   │       └── ai.py           Roadmap generation, topic summaries, career chat
│   ├── tests/                 Pytest suite (conftest + test_*.py)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                  React + Vite app
│   ├── src/
│   │   ├── api.js             Typed fetch client (auth-aware, attaches JWT)
│   │   ├── context/            AuthContext, ThemeContext
│   │   ├── components/         Navbar, Footer, FieldCard, ProtectedRoute, ChatWidget
│   │   ├── pages/               Home, FieldDetail, Login, Register, Dashboard
│   │   └── styles/global.css   Design tokens & dark/light theme
│   └── Dockerfile
└── docker-compose.yml
```

**Design note:** roadmap *content* (fields/stages/topics/resources) stays in static Python data files rather than the database — it's reference content that's version-controlled like code, not user-generated data. Only user accounts, progress, and bookmarks are persisted in the database. This keeps the data layer simple while still demonstrating real ORM/auth/relational design where it matters (user-generated state).


## 🚀 Running locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env             # set VITE_API_URL if backend isn't on :8000
npm run dev
```

App available at `http://localhost:5173`.

### With Docker

```bash
docker-compose up --build
```

## 📡 Key API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register` | – | Create account, returns JWT |
| POST | `/api/v1/auth/login` | – | OAuth2 password login, returns JWT |
| GET | `/api/v1/auth/me` | ✅ | Current user profile |
| GET | `/api/v1/fields` | – | List all fields with summary stats |
| GET | `/api/v1/fields/{field_id}` | – | Full roadmap for one field |
| GET | `/api/v1/search?q=` | – | Search topics/resources by keyword |
| GET | `/api/v1/stats` | – | Platform-wide aggregate stats |
| POST | `/api/v1/progress/toggle` | ✅ | Mark a topic complete/incomplete |
| GET | `/api/v1/progress/{field_id}` | ✅ | Completion % for one field |
| GET | `/api/v1/progress` | ✅ | Completion overview across all fields |
| POST | `/api/v1/bookmarks/toggle` | ✅ | Star/unstar a topic |
| GET | `/api/v1/bookmarks` | ✅ | List all bookmarked topics |
| GET | `/api/v1/export/{field_id}/pdf` | ✅ | Download a PDF progress report |
| POST | `/api/v1/ai/generate-roadmap` | ✅ | Generate + cache a roadmap for any field name via Claude |
| GET | `/api/v1/ai/generated` | – | List all AI-generated fields |
| POST | `/api/v1/ai/generated/{field_id}/regenerate` | ✅ | Discard and regenerate a low-quality AI roadmap |
| DELETE | `/api/v1/ai/generated/{field_id}` | ✅ | Permanently delete an AI-generated roadmap |
| POST | `/api/v1/ai/summarize` | ✅ | Get (or generate + cache) an AI summary for a topic |
| POST | `/api/v1/ai/quiz` | ✅ | Get (or generate + cache) a 4-question practice quiz for a topic |
| POST | `/api/v1/ai/resume-bullets` | ✅ | Generate resume bullet points from the user's completed topics |
| POST | `/api/v1/ai/chat` | ✅ | Send a message to the roadmap-grounded career assistant (single response) |
| POST | `/api/v1/ai/chat/stream` | ✅ | Same as above, streamed token-by-token via Server-Sent Events |
| GET | `/api/v1/ai/chat/history` | ✅ | Get the user's chat history |
| GET | `/api/v1/search/semantic?q=` | – | Meaning-based search (TF-IDF + cosine similarity) |

`✅` endpoints require `Authorization: Bearer <token>`.

### ⚠️ AI features require an API key

Add your Anthropic API key to `backend/.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
```

Without it, every other feature works normally — AI endpoints simply return `503` until a key is configured. The app boots fine either way (the Anthropic client is initialized lazily).

## 🧪 Running tests

```bash
cd backend
pytest -v
```

CI runs this automatically (plus a frontend production build) on every push via `.github/workflows/ci.yml`.

## 🧠 Why this is a good resume project

- Real authentication (JWT + bcrypt) and a relational data model (SQLAlchemy ORM, foreign keys, unique constraints)
- **LLM integration done properly**: structured JSON generation with validation/caching, token-by-token streaming via Server-Sent Events, a RAG-lite assistant that grounds answers in retrieved roadmap data, moderation controls (regenerate/delete), and graceful degradation when no API key is present
- A hand-rolled TF-IDF/cosine-similarity search engine — demonstrates understanding of information retrieval fundamentals without reaching for a heavyweight dependency
- Clean separation of concerns: routers / models / db_models / security / deps / ai_client
- Automated tests (pytest) and CI (GitHub Actions) — shows you ship with confidence, not just code
- Server-side PDF generation — a genuinely uncommon, demo-able backend feature
- Rate limiting + structured logging middleware — production-mindset touches
- Frontend consumes a real authenticated API, manages global auth/theme state via Context, and renders a live chart (recharts) from backend data
- Containerized with Docker for deployment readiness

## 🔭 Possible extensions

- Swap SQLite for PostgreSQL (`DATABASE_URL=postgresql://...`) — code already supports it
- Move rate limiting to Redis-backed `slowapi` for multi-instance deployments
- Add an admin panel (the `is_admin` flag and `get_current_admin` dependency are already wired up) to edit roadmap content
- Add OAuth login (Google/GitHub) alongside email/password
- Deploy backend on Render/Railway/AWS and frontend on Vercel/Netlify, then link the live demo on your resume

## 📝 License

MIT — use freely for learning or portfolio purposes.
