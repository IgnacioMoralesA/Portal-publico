from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import AuditEvent


router = APIRouter()


@router.get("/events")
def list_audit_events(db: Session = Depends(get_db)):
    rows = db.scalars(select(AuditEvent).order_by(AuditEvent.id)).all()
    return [
        {
            "id": item.id,
            "user_id": item.user_id,
            "event_type": item.event_type,
            "severity": item.severity,
            "message": item.message,
        }
        for item in rows
    ]
