from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend.config import settings
from app.backend.database import get_db
from app.backend.models import AuthFactor, LoginAttempt, PasswordRecoveryRequest, User
from app.backend.schemas.core import (
    RecoveryConfirmIn,
    RecoveryRequestIn,
    LoginIn,
    LoginOut,
    ToggleFactorIn,
    VerifyOtpIn,
    VerifyOtpOut,
)
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


@router.post("/login", response_model=LoginOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    valid = payload.username == settings.demo_username and payload.password == settings.demo_password
    db.add(
        LoginAttempt(
            username=payload.username,
            result="success" if valid else "failure",
            detail="login demo local" if valid else "credenciales demo invalidas",
        )
    )
    db.commit()

    if not valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales demo invalidas.")

    user = db.get(User, DEMO_USER_ID)
    return LoginOut(
        success=True,
        message="Login demo correcto; requiere OTP local.",
        requires_otp=bool(user and user.segundo_factor_activo),
        session_id="SES-DEMO-001",
    )


@router.post("/verify-otp", response_model=VerifyOtpOut)
def verify_otp(payload: VerifyOtpIn):
    if payload.otp != settings.demo_otp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP demo invalido.")

    return VerifyOtpOut(success=True, message="OTP demo correcto.", token=settings.demo_token)


@router.post("/logout")
def logout():
    return {"success": True, "message": "Sesion demo cerrada localmente."}


@router.get("/factors")
def list_factors(db: Session = Depends(get_db)):
    factors = db.query(AuthFactor).filter(AuthFactor.user_id == DEMO_USER_ID).order_by(AuthFactor.factor_type).all()
    return [{"id": item.id, "factor_type": item.factor_type, "enabled": item.enabled} for item in factors]


@router.post("/factors/toggle")
def toggle_factor(payload: ToggleFactorIn, db: Session = Depends(get_db)):
    factor = (
        db.query(AuthFactor)
        .filter(AuthFactor.user_id == DEMO_USER_ID, AuthFactor.factor_type == payload.factor_type)
        .first()
    )
    if not factor:
        raise HTTPException(status_code=404, detail="Factor demo no encontrado.")
    factor.enabled = payload.enabled
    db.commit()
    return {"success": True, "factor_type": factor.factor_type, "enabled": factor.enabled}


@router.get("/login-attempts")
def list_login_attempts(db: Session = Depends(get_db)):
    attempts = db.query(LoginAttempt).order_by(LoginAttempt.id.desc()).limit(10).all()
    return [{"id": item.id, "username": item.username, "result": item.result, "channel": item.channel} for item in attempts]


@router.post("/recovery/request")
def request_recovery(payload: RecoveryRequestIn, db: Session = Depends(get_db)):
    if payload.username != settings.demo_username:
        raise HTTPException(status_code=404, detail="Usuario demo no encontrado.")
    recovery_id = "REC-DEMO-API"
    recovery = db.get(PasswordRecoveryRequest, recovery_id)
    if not recovery:
        recovery = PasswordRecoveryRequest(
            id=recovery_id,
            user_id=DEMO_USER_ID,
            request_status="solicitada",
            delivery_channel=payload.channel,
            attempt_count=0,
            requested_at="2026-07-08 09:00",
        )
        db.add(recovery)
    recovery.request_status = "solicitada"
    recovery.delivery_channel = payload.channel
    db.commit()
    return {"success": True, "recovery_id": recovery_id, "channel": payload.channel}


@router.post("/recovery/confirm")
def confirm_recovery(payload: RecoveryConfirmIn, db: Session = Depends(get_db)):
    recovery = db.get(PasswordRecoveryRequest, payload.recovery_id)
    if not recovery:
        raise HTTPException(status_code=404, detail="Solicitud demo no encontrada.")
    if payload.otp != settings.demo_otp:
        recovery.attempt_count += 1
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Factor demo invalido.")
    recovery.request_status = "validada demo"
    db.commit()
    return {"success": True, "message": "Recuperacion demo validada."}
