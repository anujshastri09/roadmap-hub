from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.data import ALL_FIELDS, FIELDS_BY_ID
from app.database import get_db
from app import db_models
from app.models import Field, FieldSummary, Topic, Resource
from app.semantic_search import semantic_search

router = APIRouter(prefix="/api/v1", tags=["roadmaps"])


def _count_topics(field: dict) -> int:
    return sum(len(stage["topics"]) for stage in field["stages"])


def _count_resources(field: dict) -> int:
    return sum(
        len(topic["resources"])
        for stage in field["stages"]
        for topic in stage["topics"]
    )


@router.get("/fields")
def list_fields(db: Session = Depends(get_db)):
    """Return a lightweight summary of every available field — curated + AI-generated."""
    curated = [
        {
            "id": f["id"],
            "name": f["name"],
            "tagline": f["tagline"],
            "icon": f["icon"],
            "color": f["color"],
            "stage_count": len(f["stages"]),
            "topic_count": _count_topics(f),
            "resource_count": _count_resources(f),
            "ai_generated": False,
        }
        for f in ALL_FIELDS
    ]

    generated_rows = db.query(db_models.GeneratedRoadmap).all()
    generated = []
    for r in generated_rows:
        content = json.loads(r.content_json)
        generated.append(
            {
                "id": r.field_id,
                "name": r.name,
                "tagline": r.tagline,
                "icon": r.icon,
                "color": r.color,
                "stage_count": len(content.get("stages", [])),
                "topic_count": _count_topics(content),
                "resource_count": _count_resources(content),
                "ai_generated": True,
            }
        )

    return curated + generated


@router.get("/fields/{field_id}")
def get_field(field_id: str, db: Session = Depends(get_db)):
    """Return the full roadmap for a field — checks curated set first, then AI-generated."""
    field = FIELDS_BY_ID.get(field_id)
    if field:
        return field

    record = db.query(db_models.GeneratedRoadmap).filter_by(field_id=field_id).first()
    if record:
        return json.loads(record.content_json)

    raise HTTPException(status_code=404, detail=f"Field '{field_id}' not found")


@router.get("/fields/{field_id}/stages/{stage_id}")
def get_stage(field_id: str, stage_id: str):
    field = FIELDS_BY_ID.get(field_id)
    if not field:
        raise HTTPException(status_code=404, detail=f"Field '{field_id}' not found")
    for stage in field["stages"]:
        if stage["id"] == stage_id:
            return stage
    raise HTTPException(status_code=404, detail=f"Stage '{stage_id}' not found")


@router.get("/search")
def search_topics(q: str = Query(..., min_length=2, description="Search term")):
    """Search topics and resources across all fields by keyword."""
    q_lower = q.lower()
    matches = []
    for field in ALL_FIELDS:
        for stage in field["stages"]:
            for topic in stage["topics"]:
                haystack = " ".join(
                    [topic["title"], topic["description"]]
                    + [r["title"] for r in topic["resources"]]
                ).lower()
                if q_lower in haystack:
                    matches.append(
                        {
                            "field_id": field["id"],
                            "field_name": field["name"],
                            "stage_id": stage["id"],
                            "stage_title": stage["title"],
                            "topic": topic,
                        }
                    )
    return {"query": q, "result_count": len(matches), "results": matches}


@router.get("/search/semantic")
def semantic_search_topics(q: str = Query(..., min_length=2, description="Natural-language search query")):
    """
    Meaning-based search using TF-IDF + cosine similarity (see app/semantic_search.py).
    Unlike /search (exact substring match), this can surface relevant topics even when
    the query doesn't share an exact keyword — e.g. "handle many requests at once" can
    match an "asyncio" topic.
    """
    results = semantic_search(q, top_k=8)
    return {"query": q, "result_count": len(results), "results": results}


@router.get("/stats")
def get_platform_stats():
    """Aggregate stats used on the dashboard hero section."""
    total_topics = sum(_count_topics(f) for f in ALL_FIELDS)
    total_resources = sum(_count_resources(f) for f in ALL_FIELDS)
    total_hours = sum(
        topic["estimated_hours"]
        for f in ALL_FIELDS
        for stage in f["stages"]
        for topic in stage["topics"]
    )
    return {
        "field_count": len(ALL_FIELDS),
        "topic_count": total_topics,
        "resource_count": total_resources,
        "total_learning_hours": total_hours,
    }
