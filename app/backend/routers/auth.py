from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend.config import settings
from app.backend.database import get_db
from app.backend.models import LoginAttempt, User
from app.backend.schemas.core import LoginIn, LoginOut, VerifyOtpIn, VerifyOtpOut
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
