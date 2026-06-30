import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import roadmap, progress, auth, bookmarks, export, ai
from app.middleware import RateLimitMiddleware
from app.database import Base, engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("roadmap_hub")

# Create DB tables (users, progress, bookmarks) on startup.
# Roadmap content itself stays in static, version-controlled data files.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Career Roadmap Hub API",
    description=(
        "Production-ready backend serving curated, link-rich career roadmaps "
        "(Python, MERN, Java, AWS, System Design) with JWT auth, progress "
        "tracking, bookmarks, and PDF report export."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, max_requests=200, window_seconds=60)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start) * 1000, 2)
    logger.info(
        f'{request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)'
    )
    return response


app.include_router(auth.router)
app.include_router(roadmap.router)
app.include_router(progress.router)
app.include_router(bookmarks.router)
app.include_router(export.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {
        "service": "Career Roadmap Hub API",
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return JSONResponse({"status": "healthy"})
