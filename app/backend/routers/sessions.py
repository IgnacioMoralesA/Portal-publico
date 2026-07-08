from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import SessionEvent, UserSession
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


@router.get("/current")
def get_current_session(db: Session = Depends(get_db)):
    session = db.scalar(
        select(UserSession).where(UserSession.user_id == DEMO_USER_ID, UserSession.actual.is_(True))
    )
    if not session:
        raise HTTPException(status_code=404, detail="Sesion actual demo no encontrada.")
    return {
        "id": session.id,
        "actual": session.actual,
        "dispositivo": session.dispositivo,
        "navegador": session.navegador,
        "estado": session.estado,
    }


@router.post("/{session_id}/close")
def close_session(session_id: str, db: Session = Depends(get_db)):
    session = db.get(UserSession, session_id)
    if not session or session.user_id != DEMO_USER_ID:
        raise HTTPException(status_code=404, detail="Sesion demo no encontrada.")
    if session.actual:
        raise HTTPException(status_code=409, detail="La sesion actual no se cierra remotamente en demo.")
    session.estado = "cerrada demo"
    db.add(
        SessionEvent(
            session_id=session.id,
            event_type="cierre_remoto_demo",
            risk_level="medio",
            requires_review=False,
            occurred_at="2026-07-08 09:10",
        )
    )
    db.commit()
    return {"success": True, "session_id": session.id, "estado": session.estado}


@router.get("/events")
def list_session_events(db: Session = Depends(get_db)):
    rows = db.scalars(select(SessionEvent).order_by(SessionEvent.id)).all()
    return [
        {
            "id": item.id,
            "session_id": item.session_id,
            "event_type": item.event_type,
            "risk_level": item.risk_level,
            "requires_review": item.requires_review,
            "occurred_at": item.occurred_at,
        }
        for item in rows
    ]
