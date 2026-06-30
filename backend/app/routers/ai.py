import json
import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app import db_models
from app.models import (
    GenerateRoadmapRequest,
    SummarizeTopicRequest,
    ChatRequest,
    QuizRequest,
    ResumeBulletsRequest,
)
from app.data import FIELDS_BY_ID, ALL_FIELDS
from app.ai_client import call_claude, call_claude_chat, stream_claude_chat, extract_json

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])
logger = logging.getLogger("roadmap_hub.ai")


# ---------------------------------------------------------------------------
# 1. AI Roadmap Generator
# ---------------------------------------------------------------------------

ROADMAP_SYSTEM_PROMPT = """You are a senior engineering curriculum designer. \
Given a career field name, produce a structured learning roadmap as STRICT JSON only \
(no markdown fences, no commentary before or after).

The JSON must match this exact shape:
{
  "name": "<field display name>",
  "tagline": "<one sentence, under 100 chars>",
  "icon": "<single emoji>",
  "stages": [
    {
      "title": "<stage name>",
      "subtitle": "<short description>",
      "order": <int starting at 1>,
      "topics": [
        {
          "title": "<topic name>",
          "description": "<1-2 sentence description>",
          "level": "beginner" | "intermediate" | "advanced",
          "estimated_hours": <int>,
          "resources": [
            {"title": "<resource name>", "url": "<real, working URL to official docs or a well-known site>", "type": "docs" | "article" | "course" | "video"}
          ]
        }
      ]
    }
  ]
}

Rules:
- Produce 3-5 stages, each with 2-4 topics.
- Each topic needs 1-3 resources with REAL urls (official documentation sites, MDN, freeCodeCamp, Real Python, etc. — never invent fake URLs).
- Output ONLY the JSON object, nothing else.
"""


def _slugify(name: str) -> str:
    return "-".join(name.strip().lower().split())[:60]


@router.post("/generate-roadmap")
def generate_roadmap(
    payload: GenerateRoadmapRequest,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Generate a structured roadmap for a field not in the curated set, using Claude.
    Result is cached in the database so the same field is never regenerated twice."""
    slug = _slugify(payload.field_name)

    if slug in FIELDS_BY_ID:
        raise HTTPException(
            status_code=400, detail="This field already exists in the curated roadmap set."
        )

    existing = db.query(db_models.GeneratedRoadmap).filter_by(field_id=slug).first()
    if existing:
        return json.loads(existing.content_json)

    try:
        raw = call_claude(
            system=ROADMAP_SYSTEM_PROMPT,
            user_message=f"Career field: {payload.field_name}",
            max_tokens=4000,
        )
        parsed = extract_json(raw)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Roadmap generation failed: {e}")
        raise HTTPException(status_code=502, detail="AI roadmap generation failed. Try again.")

    field_doc = {
        "id": slug,
        "name": parsed.get("name", payload.field_name),
        "tagline": parsed.get("tagline", ""),
        "icon": parsed.get("icon", "✨"),
        "color": "#A98CFF",
        "stages": parsed.get("stages", []),
        "ai_generated": True,
    }

    record = db_models.GeneratedRoadmap(
        field_id=slug,
        name=field_doc["name"],
        tagline=field_doc["tagline"],
        icon=field_doc["icon"],
        color=field_doc["color"],
        content_json=json.dumps(field_doc),
        requested_by_user_id=user.id,
    )
    db.add(record)
    db.commit()

    return field_doc


@router.get("/generated")
def list_generated_roadmaps(db: Session = Depends(get_db)):
    """List all AI-generated fields so they can be shown alongside curated ones."""
    rows = db.query(db_models.GeneratedRoadmap).order_by(db_models.GeneratedRoadmap.created_at.desc()).all()
    return [
        {
            "id": r.field_id,
            "name": r.name,
            "tagline": r.tagline,
            "icon": r.icon,
            "color": r.color,
            "ai_generated": True,
        }
        for r in rows
    ]


@router.get("/generated/{field_id}")
def get_generated_roadmap(field_id: str, db: Session = Depends(get_db)):
    record = db.query(db_models.GeneratedRoadmap).filter_by(field_id=field_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Generated field not found")
    return json.loads(record.content_json)


@router.post("/generated/{field_id}/regenerate")
def regenerate_roadmap(
    field_id: str,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Moderation control: discard a previously AI-generated roadmap and regenerate it from
    scratch. Useful if the first generation was low-quality or contained a bad URL."""
    record = db.query(db_models.GeneratedRoadmap).filter_by(field_id=field_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Generated field not found")

    field_name = record.name
    db.delete(record)
    db.commit()

    try:
        raw = call_claude(
            system=ROADMAP_SYSTEM_PROMPT,
            user_message=f"Career field: {field_name}",
            max_tokens=4000,
        )
        parsed = extract_json(raw)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Roadmap regeneration failed: {e}")
        raise HTTPException(status_code=502, detail="AI roadmap regeneration failed. Try again.")

    field_doc = {
        "id": field_id,
        "name": parsed.get("name", field_name),
        "tagline": parsed.get("tagline", ""),
        "icon": parsed.get("icon", "✨"),
        "color": "#A98CFF",
        "stages": parsed.get("stages", []),
        "ai_generated": True,
    }
    new_record = db_models.GeneratedRoadmap(
        field_id=field_id,
        name=field_doc["name"],
        tagline=field_doc["tagline"],
        icon=field_doc["icon"],
        color=field_doc["color"],
        content_json=json.dumps(field_doc),
        requested_by_user_id=user.id,
    )
    db.add(new_record)
    db.commit()
    return field_doc


@router.delete("/generated/{field_id}")
def delete_generated_roadmap(
    field_id: str,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Moderation control: permanently remove a low-quality AI-generated roadmap."""
    record = db.query(db_models.GeneratedRoadmap).filter_by(field_id=field_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Generated field not found")
    db.delete(record)
    db.commit()
    return {"deleted": True, "field_id": field_id}


# ---------------------------------------------------------------------------
# 2. AI Topic Summarizer (cached)
# ---------------------------------------------------------------------------

SUMMARY_SYSTEM_PROMPT = (
    "You are a concise technical writer. Summarize the given engineering topic in exactly "
    "3 short bullet-free sentences a learner can read in under 15 seconds. No markdown."
)


def _find_topic(field_id: str, topic_id: str):
    field = FIELDS_BY_ID.get(field_id)
    if not field:
        return None, None
    for stage in field["stages"]:
        for topic in stage["topics"]:
            if topic["id"] == topic_id:
                return field, topic
    return field, None


@router.post("/summarize")
def summarize_topic(
    payload: SummarizeTopicRequest,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Returns a cached AI summary for a topic, generating + caching it on first request."""
    if not payload.force_refresh:
        cached = (
            db.query(db_models.TopicSummary)
            .filter_by(field_id=payload.field_id, topic_id=payload.topic_id)
            .first()
        )
        if cached:
            return {"summary": cached.summary_text, "cached": True}

    field, topic = _find_topic(payload.field_id, payload.topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    try:
        summary = call_claude(
            system=SUMMARY_SYSTEM_PROMPT,
            user_message=f"Topic: {topic['title']}\nContext: {topic['description']}",
            max_tokens=200,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    existing = (
        db.query(db_models.TopicSummary)
        .filter_by(field_id=payload.field_id, topic_id=payload.topic_id)
        .first()
    )
    if existing:
        existing.summary_text = summary
    else:
        db.add(
            db_models.TopicSummary(
                field_id=payload.field_id, topic_id=payload.topic_id, summary_text=summary
            )
        )
    db.commit()

    return {"summary": summary, "cached": False}


# ---------------------------------------------------------------------------
# 3. AI Career Chat Assistant (RAG-lite: grounded in roadmap data)
# ---------------------------------------------------------------------------

CHAT_SYSTEM_PROMPT = """You are a friendly, knowledgeable career mentor for software engineers, \
embedded inside "Roadmap Hub". Give concise, practical, encouraging advice (3-6 sentences unless \
asked for more detail). When relevant roadmap context is provided below, ground your answer in it \
and reference specific stages/topics by name. If no context is given, answer from general \
engineering career knowledge. Never invent roadmap content that wasn't provided to you."""


def _build_context(field_id: str | None) -> str:
    if not field_id:
        return ""
    field = FIELDS_BY_ID.get(field_id)
    if not field:
        return ""
    lines = [f"Roadmap: {field['name']} — {field['tagline']}"]
    for stage in sorted(field["stages"], key=lambda s: s["order"]):
        topic_titles = ", ".join(t["title"] for t in stage["topics"])
        lines.append(f"Stage {stage['order']} ({stage['title']}): {topic_titles}")
    return "\n".join(lines)


@router.post("/chat")
def career_chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Conversational career assistant. Grounds answers in roadmap data when a field_id is given,
    and maintains short-term memory via the user's recent chat history (last 6 messages)."""
    context = _build_context(payload.field_id)

    recent = (
        db.query(db_models.ChatMessage)
        .filter_by(user_id=user.id)
        .order_by(db_models.ChatMessage.created_at.desc())
        .limit(6)
        .all()
    )
    history = [{"role": m.role, "content": m.content} for m in reversed(recent)]

    user_turn = payload.message
    if context:
        user_turn = f"[Roadmap context]\n{context}\n\n[User question]\n{payload.message}"
    history.append({"role": "user", "content": user_turn})

    try:
        reply = call_claude_chat(system=CHAT_SYSTEM_PROMPT, history=history, max_tokens=600)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=502, detail="AI assistant is unavailable right now.")

    db.add(db_models.ChatMessage(user_id=user.id, role="user", content=payload.message))
    db.add(db_models.ChatMessage(user_id=user.id, role="assistant", content=reply))
    db.commit()

    return {"reply": reply}


@router.get("/chat/history")
def chat_history(
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    rows = (
        db.query(db_models.ChatMessage)
        .filter_by(user_id=user.id)
        .order_by(db_models.ChatMessage.created_at.asc())
        .all()
    )
    return [{"role": r.role, "content": r.content, "created_at": r.created_at} for r in rows]


@router.post("/chat/stream")
def career_chat_stream(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Same as /chat, but streams the reply token-by-token via Server-Sent Events so the
    frontend can render it progressively instead of waiting for the full response."""
    context = _build_context(payload.field_id)

    recent = (
        db.query(db_models.ChatMessage)
        .filter_by(user_id=user.id)
        .order_by(db_models.ChatMessage.created_at.desc())
        .limit(6)
        .all()
    )
    history = [{"role": m.role, "content": m.content} for m in reversed(recent)]

    user_turn = payload.message
    if context:
        user_turn = f"[Roadmap context]\n{context}\n\n[User question]\n{payload.message}"
    history.append({"role": "user", "content": user_turn})

    def event_generator():
        full_reply = []
        try:
            for chunk in stream_claude_chat(system=CHAT_SYSTEM_PROMPT, history=history, max_tokens=600):
                full_reply.append(chunk)
                # SSE format: each event is "data: <payload>\n\n"
                yield f"data: {json.dumps({'delta': chunk})}\n\n"
        except RuntimeError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            return
        except Exception as e:
            logger.error(f"Streaming chat failed: {e}")
            yield f"data: {json.dumps({'error': 'AI assistant is unavailable right now.'})}\n\n"
            return

        reply_text = "".join(full_reply)
        db.add(db_models.ChatMessage(user_id=user.id, role="user", content=payload.message))
        db.add(db_models.ChatMessage(user_id=user.id, role="assistant", content=reply_text))
        db.commit()
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# 4. AI Quiz / Interview Question Generator (cached per topic)
# ---------------------------------------------------------------------------

QUIZ_SYSTEM_PROMPT = """You are a technical interviewer. Given an engineering topic, generate \
exactly 4 multiple-choice questions a candidate might be asked about it, as STRICT JSON only \
(no markdown fences, no commentary).

Output shape:
{
  "questions": [
    {
      "question": "<question text>",
      "options": ["<option A>", "<option B>", "<option C>", "<option D>"],
      "correct_index": <0-3>,
      "explanation": "<1 sentence explaining the correct answer>"
    }
  ]
}

Rules:
- Exactly 4 questions, exactly 4 options each.
- Mix conceptual and applied/practical questions.
- Output ONLY the JSON object.
"""


@router.post("/quiz")
def generate_quiz(
    payload: QuizRequest,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Returns a cached set of practice questions for a topic, generating + caching on first request."""
    if not payload.force_refresh:
        cached = (
            db.query(db_models.QuizCache)
            .filter_by(field_id=payload.field_id, topic_id=payload.topic_id)
            .first()
        )
        if cached:
            return {"questions": json.loads(cached.questions_json), "cached": True}

    field, topic = _find_topic(payload.field_id, payload.topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    try:
        raw = call_claude(
            system=QUIZ_SYSTEM_PROMPT,
            user_message=f"Topic: {topic['title']}\nContext: {topic['description']}\nLevel: {topic['level']}",
            max_tokens=1200,
        )
        parsed = extract_json(raw)
        questions = parsed.get("questions", [])
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Quiz generation failed: {e}")
        raise HTTPException(status_code=502, detail="AI quiz generation failed. Try again.")

    existing = (
        db.query(db_models.QuizCache)
        .filter_by(field_id=payload.field_id, topic_id=payload.topic_id)
        .first()
    )
    if existing:
        existing.questions_json = json.dumps(questions)
    else:
        db.add(
            db_models.QuizCache(
                field_id=payload.field_id,
                topic_id=payload.topic_id,
                questions_json=json.dumps(questions),
            )
        )
    db.commit()

    return {"questions": questions, "cached": False}


# ---------------------------------------------------------------------------
# 5. AI Resume Bullet Generator (based on a user's completed topics)
# ---------------------------------------------------------------------------

RESUME_SYSTEM_PROMPT = """You are a resume-writing expert for software engineers. Given a list of \
completed technical topics for a field, write 3-5 resume-ready bullet points that translate this \
learning into professional, achievement-oriented language a recruiter would respect. Avoid generic \
phrasing like "learned about X" — instead phrase things like real engineering competencies \
(e.g. "Built RESTful APIs with FastAPI, implementing JWT-based authentication and SQLAlchemy ORM \
data models"). Output STRICT JSON only: {"bullets": ["<bullet 1>", "<bullet 2>", ...]}. No markdown."""


@router.post("/resume-bullets")
def generate_resume_bullets(
    payload: ResumeBulletsRequest,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Generates resume bullet points from the topics the user has actually completed for a field.
    Cached per (user, field) and regenerated only when the user completes more topics."""
    field = FIELDS_BY_ID.get(payload.field_id)
    if not field:
        record = db.query(db_models.GeneratedRoadmap).filter_by(field_id=payload.field_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Unknown field_id")
        field = json.loads(record.content_json)

    completed_ids = {
        r.topic_id
        for r in db.query(db_models.TopicProgress).filter_by(
            user_id=user.id, field_id=payload.field_id
        )
    }
    if not completed_ids:
        raise HTTPException(
            status_code=400,
            detail="Complete at least one topic before generating resume bullets.",
        )

    completed_titles = [
        topic["title"]
        for stage in field["stages"]
        for topic in stage["topics"]
        if topic["id"] in completed_ids
    ]

    try:
        raw = call_claude(
            system=RESUME_SYSTEM_PROMPT,
            user_message=f"Field: {field['name']}\nCompleted topics: {', '.join(completed_titles)}",
            max_tokens=600,
        )
        parsed = extract_json(raw)
        bullets = parsed.get("bullets", [])
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Resume bullet generation failed: {e}")
        raise HTTPException(status_code=502, detail="AI resume bullet generation failed. Try again.")

    existing = (
        db.query(db_models.ResumeBulletCache)
        .filter_by(user_id=user.id, field_id=payload.field_id)
        .first()
    )
    if existing:
        existing.bullets_json = json.dumps(bullets)
    else:
        db.add(
            db_models.ResumeBulletCache(
                user_id=user.id, field_id=payload.field_id, bullets_json=json.dumps(bullets)
            )
        )
    db.commit()

    return {"bullets": bullets, "based_on_topic_count": len(completed_titles)}
