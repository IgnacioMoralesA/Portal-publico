from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import User, UserSession
from app.backend.schemas.core import UserMeOut
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


@router.get("/me", response_model=UserMeOut)
def get_me(db: Session = Depends(get_db)):
    user = db.get(User, DEMO_USER_ID)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario demo no encontrado.")

    sessions_count = db.scalar(
        select(func.count()).select_from(UserSession).where(
            UserSession.user_id == DEMO_USER_ID,
            UserSession.estado == "activa",
        )
    )
    return UserMeOut(
        id=user.id,
        username=user.username,
        nombre=user.nombre,
        run_enmascarado=user.run_enmascarado,
        correo=user.correo,
        telefono=user.telefono,
        clave_unica_estado=user.clave_unica_estado,
        segundo_factor_activo=user.segundo_factor_activo,
        sesiones_activas=int(sessions_count or 0),
    )
