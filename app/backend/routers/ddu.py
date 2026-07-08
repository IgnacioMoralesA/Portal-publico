from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import DduProfile
from app.backend.schemas.core import DduStatusOut
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


@router.get("/status", response_model=DduStatusOut)
def get_ddu_status(db: Session = Depends(get_db)):
    ddu = db.scalar(select(DduProfile).where(DduProfile.user_id == DEMO_USER_ID))
    if not ddu:
        raise HTTPException(status_code=404, detail="DDU demo no encontrado.")
    return ddu
