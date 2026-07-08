from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.config import settings
from app.backend.database import get_db
from app.backend.models import AuthorizationDecision, AuthorizationHistory, AuthorizationRequest, SensitiveDataCategory
from app.backend.schemas.core import AuthorizationItem, DemoFactorIn
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


def _to_item(row: AuthorizationRequest) -> AuthorizationItem:
    return AuthorizationItem(
        id=row.id,
        institucion=row.institucion,
        finalidad=row.finalidad,
        tipo_dato=row.tipo_dato,
        fecha_solicitud=row.fecha_solicitud,
        estado=row.estado,
        fecha_decision=row.fecha_decision,
        historial=[item for item in row.historial.splitlines() if item],
    )


@router.get("", response_model=list[AuthorizationItem])
def list_authorizations(db: Session = Depends(get_db)):
    rows = db.scalars(
        select(AuthorizationRequest)
        .where(AuthorizationRequest.user_id == DEMO_USER_ID)
        .order_by(AuthorizationRequest.fecha_solicitud.desc())
    )
    return [_to_item(row) for row in rows]


@router.get("/history")
def list_authorization_history(db: Session = Depends(get_db)):
    rows = db.scalars(select(AuthorizationHistory).order_by(AuthorizationHistory.id)).all()
    return [
        {
            "id": item.id,
            "authorization_id": item.authorization_id,
            "history_event": item.history_event,
            "summary": item.summary,
            "visible_to_user": item.visible_to_user,
            "event_at": item.event_at,
        }
        for item in rows
    ]


@router.get("/sensitive-data-categories")
def list_sensitive_data_categories(db: Session = Depends(get_db)):
    rows = db.scalars(select(SensitiveDataCategory).order_by(SensitiveDataCategory.id)).all()
    return [
        {
            "category_type": item.category_type,
            "label": item.label,
            "requires_explicit_consent": item.requires_explicit_consent,
            "retention_days": item.retention_days,
        }
        for item in rows
    ]


@router.get("/{authorization_id}", response_model=AuthorizationItem)
def get_authorization(authorization_id: str, db: Session = Depends(get_db)):
    authorization = db.get(AuthorizationRequest, authorization_id)
    if not authorization or authorization.user_id != DEMO_USER_ID:
        raise HTTPException(status_code=404, detail="Autorizacion demo no encontrada.")
    return _to_item(authorization)


def _decide_authorization(authorization_id: str, payload: DemoFactorIn, decision: str, target_status: str, db: Session):
    if payload.otp != settings.demo_otp:
        raise HTTPException(status_code=401, detail="Factor demo requerido.")
    authorization = db.get(AuthorizationRequest, authorization_id)
    if not authorization or authorization.user_id != DEMO_USER_ID:
        raise HTTPException(status_code=404, detail="Autorizacion demo no encontrada.")
    authorization.estado = target_status
    authorization.fecha_decision = "2026-07-08 09:40"
    authorization.historial = f"{authorization.historial}\n2026-07-08 09:40 {target_status} demo registrada".strip()
    db.add(
        AuthorizationDecision(
            authorization_id=authorization.id,
            decision=decision,
            factor_verified=True,
            decision_source="api_mock",
            decided_at="2026-07-08 09:40",
        )
    )
    db.add(
        AuthorizationHistory(
            authorization_id=authorization.id,
            history_event="revocada" if decision == "revocar" else "decidida",
            summary=f"Decision demo {decision} registrada",
            visible_to_user=True,
            event_at="2026-07-08 09:40",
        )
    )
    db.commit()
    return {"success": True, "authorization_id": authorization.id, "estado": authorization.estado}


@router.post("/{authorization_id}/approve")
def approve_authorization(authorization_id: str, payload: DemoFactorIn, db: Session = Depends(get_db)):
    return _decide_authorization(authorization_id, payload, "aprobar", "aprobada", db)


@router.post("/{authorization_id}/reject")
def reject_authorization(authorization_id: str, payload: DemoFactorIn, db: Session = Depends(get_db)):
    return _decide_authorization(authorization_id, payload, "rechazar", "rechazada", db)


@router.post("/{authorization_id}/revoke")
def revoke_authorization(authorization_id: str, payload: DemoFactorIn, db: Session = Depends(get_db)):
    return _decide_authorization(authorization_id, payload, "revocar", "revocada", db)
