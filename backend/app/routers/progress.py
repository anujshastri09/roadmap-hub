from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app import db_models
from app.models import BookmarkToggleRequest
from app.data import FIELDS_BY_ID, ALL_FIELDS

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])


def _validate_field_and_topic(field_id: str, topic_id: str):
    field = FIELDS_BY_ID.get(field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Unknown field_id")
    valid_topic_ids = {t["id"] for stage in field["stages"] for t in stage["topics"]}
    if topic_id not in valid_topic_ids:
        raise HTTPException(status_code=404, detail="Unknown topic_id for this field")
    return field


@router.post("/toggle")
def toggle_topic(
    payload: BookmarkToggleRequest,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Mark a topic complete/incomplete for the authenticated user."""
    _validate_field_and_topic(payload.field_id, payload.topic_id)

    existing = (
        db.query(db_models.TopicProgress)
        .filter_by(user_id=user.id, field_id=payload.field_id, topic_id=payload.topic_id)
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        completed = False
    else:
        db.add(
            db_models.TopicProgress(
                user_id=user.id, field_id=payload.field_id, topic_id=payload.topic_id
            )
        )
        db.commit()
        completed = True

    count = (
        db.query(db_models.TopicProgress)
        .filter_by(user_id=user.id, field_id=payload.field_id)
        .count()
    )
    return {
        "field_id": payload.field_id,
        "topic_id": payload.topic_id,
        "completed": completed,
        "field_completed_count": count,
    }


@router.get("/{field_id}")
def get_progress(
    field_id: str,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    field = FIELDS_BY_ID.get(field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Unknown field_id")

    total_topics = sum(len(stage["topics"]) for stage in field["stages"])
    rows = (
        db.query(db_models.TopicProgress)
        .filter_by(user_id=user.id, field_id=field_id)
        .all()
    )
    completed_ids = sorted(r.topic_id for r in rows)

    return {
        "field_id": field_id,
        "completed_topic_ids": completed_ids,
        "completed_count": len(completed_ids),
        "total_topics": total_topics,
        "percent_complete": round((len(completed_ids) / total_topics) * 100, 1)
        if total_topics
        else 0,
    }


@router.get("")
def get_all_progress(
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Overview of completion across every field — powers the dashboard."""
    rows = db.query(db_models.TopicProgress).filter_by(user_id=user.id).all()
    completed_by_field = {}
    for r in rows:
        completed_by_field.setdefault(r.field_id, set()).add(r.topic_id)

    overview = []
    for field in ALL_FIELDS:
        total = sum(len(stage["topics"]) for stage in field["stages"])
        done = len(completed_by_field.get(field["id"], set()))
        overview.append(
            {
                "field_id": field["id"],
                "field_name": field["name"],
                "icon": field["icon"],
                "color": field["color"],
                "completed_count": done,
                "total_topics": total,
                "percent_complete": round((done / total) * 100, 1) if total else 0,
            }
        )
    return {"overview": overview}
