from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import Notification
from app.backend.schemas.core import NotificationItem
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


@router.get("", response_model=list[NotificationItem])
def list_notifications(db: Session = Depends(get_db)):
    return list(
        db.scalars(
            select(Notification)
            .where(Notification.user_id == DEMO_USER_ID)
            .order_by(Notification.fecha_recepcion.desc())
        )
    )
