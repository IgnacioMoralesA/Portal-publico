from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.backend.config import settings
from app.backend.database import get_db
from app.backend.models import SecurityQuestion, User, UserProfile, UserSession
from app.backend.schemas.core import ContactPatchIn, SecurityQuestionVerifyIn, UserMeOut
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


@router.get("/me/profile")
def get_profile(db: Session = Depends(get_db)):
    profile = db.scalar(select(UserProfile).where(UserProfile.user_id == DEMO_USER_ID))
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil demo no encontrado.")
    return {
        "display_name": profile.display_name,
        "profile_status": profile.profile_status,
        "identity_level": profile.identity_level,
        "completion_percent": profile.completion_percent,
    }


@router.patch("/me/contact")
def patch_contact(payload: ContactPatchIn, db: Session = Depends(get_db)):
    if payload.otp != settings.demo_otp:
        raise HTTPException(status_code=401, detail="Factor demo invalido.")
    user = db.get(User, DEMO_USER_ID)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario demo no encontrado.")
    if payload.correo:
        user.correo = payload.correo
    if payload.telefono:
        user.telefono = payload.telefono
    db.commit()
    return {"success": True, "correo": user.correo, "telefono": user.telefono}


@router.get("/me/security-questions")
def list_security_questions(db: Session = Depends(get_db)):
    rows = db.scalars(select(SecurityQuestion).where(SecurityQuestion.user_id == DEMO_USER_ID)).all()
    return [
        {
            "id": item.id,
            "question_text": item.question_text,
            "answer_hint": item.answer_hint,
            "question_status": item.question_status,
        }
        for item in rows
    ]


@router.post("/me/security-questions/verify")
def verify_security_question(payload: SecurityQuestionVerifyIn):
    if payload.answer.strip().lower() != "respuesta demo":
        raise HTTPException(status_code=401, detail="Respuesta demo invalida.")
    return {"success": True, "message": "Pregunta de seguridad demo validada."}
