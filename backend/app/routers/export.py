import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from app.database import get_db
from app.deps import get_current_user
from app import db_models
from app.data import FIELDS_BY_ID

router = APIRouter(prefix="/api/v1/export", tags=["export"])

GOLD = colors.HexColor("#B8860B")
DARK = colors.HexColor("#15131C")


@router.get("/{field_id}/pdf")
def export_field_progress_pdf(
    field_id: str,
    db: Session = Depends(get_db),
    user: db_models.User = Depends(get_current_user),
):
    """Generate a polished progress-report PDF for a field — shareable on a resume/portfolio."""
    field = FIELDS_BY_ID.get(field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Unknown field_id")

    completed_ids = {
        r.topic_id
        for r in db.query(db_models.TopicProgress).filter_by(
            user_id=user.id, field_id=field_id
        )
    }

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    y = height - margin

    c.setFillColor(DARK)
    c.rect(0, height - 35 * mm, width, 35 * mm, fill=True, stroke=False)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, height - 18 * mm, f"{field['icon']}  {field['name']} - Roadmap Report")
    c.setFillColor(colors.whitesmoke)
    c.setFont("Helvetica", 10)
    c.drawString(margin, height - 26 * mm, f"Generated for {user.full_name or user.email}")
    c.drawRightString(
        width - margin, height - 26 * mm, datetime.utcnow().strftime("%d %b %Y")
    )

    y = height - 45 * mm
    total = sum(len(s["topics"]) for s in field["stages"])
    pct = round((len(completed_ids) / total) * 100, 1) if total else 0

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, f"Overall completion: {len(completed_ids)}/{total} topics ({pct}%)")
    y -= 12 * mm

    for stage in sorted(field["stages"], key=lambda s: s["order"]):
        if y < 30 * mm:
            c.showPage()
            y = height - margin
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin, y, f"Stage {stage['order']}: {stage['title']}")
        y -= 7 * mm

        for topic in stage["topics"]:
            if y < 20 * mm:
                c.showPage()
                y = height - margin
            mark = "[x]" if topic["id"] in completed_ids else "[ ]"
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 10)
            c.drawString(margin + 6 * mm, y, f"{mark} {topic['title']}  (~{topic['estimated_hours']}h)")
            y -= 6 * mm
        y -= 4 * mm

    c.showPage()
    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{field_id}-roadmap-report.pdf"'
        },
    )
