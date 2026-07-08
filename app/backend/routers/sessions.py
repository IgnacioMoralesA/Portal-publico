from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import UserSession
from app.backend.schemas.core import SessionItem
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


@router.get("", response_model=list[SessionItem])
def list_sessions(db: Session = Depends(get_db)):
    return list(
        db.scalars(
            select(UserSession)
            .where(UserSession.user_id == DEMO_USER_ID)
            .order_by(UserSession.id)
        )
    )
