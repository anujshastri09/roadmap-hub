from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app import db_models
from app.models import BookmarkToggleRequest
from app.data import FIELDS_BY_ID

router = APIRouter(prefix="/api/v1/bookmarks", tags=["bookmarks"])


@router.post("/toggle")
def toggle_bookmark(
    payload: BookmarkToggleRequest,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    field = FIELDS_BY_ID.get(payload.field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Unknown field_id")

    existing = (
        db.query(db_models.Bookmark)
        .filter_by(user_id=user.id, field_id=payload.field_id, topic_id=payload.topic_id)
        .first()
    )
    if existing:
        db.delete(existing)
        db.commit()
        return {"bookmarked": False}

    db.add(
        db_models.Bookmark(
            user_id=user.id, field_id=payload.field_id, topic_id=payload.topic_id
        )
    )
    db.commit()
    return {"bookmarked": True}


@router.get("")
def list_bookmarks(
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    rows = db.query(db_models.Bookmark).filter_by(user_id=user.id).all()
    results = []
    for row in rows:
        field = FIELDS_BY_ID.get(row.field_id)
        if not field:
            continue
        topic = next(
            (t for stage in field["stages"] for t in stage["topics"] if t["id"] == row.topic_id),
            None,
        )
        if topic:
            results.append(
                {"field_id": row.field_id, "field_name": field["name"], "topic": topic}
            )
    return {"bookmarks": results}
