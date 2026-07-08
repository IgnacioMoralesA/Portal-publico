from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import AuthorizationRequest
from app.backend.schemas.core import AuthorizationItem
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


@router.get("", response_model=list[AuthorizationItem])
def list_authorizations(db: Session = Depends(get_db)):
    rows = db.scalars(
        select(AuthorizationRequest)
        .where(AuthorizationRequest.user_id == DEMO_USER_ID)
        .order_by(AuthorizationRequest.fecha_solicitud.desc())
    )
    return [
        AuthorizationItem(
            id=row.id,
            institucion=row.institucion,
            finalidad=row.finalidad,
            tipo_dato=row.tipo_dato,
            fecha_solicitud=row.fecha_solicitud,
            estado=row.estado,
            fecha_decision=row.fecha_decision,
            historial=[item for item in row.historial.splitlines() if item],
        )
        for row in rows
    ]
