from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import Institution, InstitutionIntegration, IntegrationStatusEvent


router = APIRouter()


@router.get("/api/institutions")
def list_institutions(db: Session = Depends(get_db)):
    rows = db.scalars(select(Institution).order_by(Institution.id)).all()
    return [
        {
            "id": item.id,
            "display_name": item.display_name,
            "institution_type": item.institution_type,
            "active": item.active,
            "support_label": item.support_label,
        }
        for item in rows
    ]


@router.get("/api/institutions/{institution_id}")
def get_institution(institution_id: str, db: Session = Depends(get_db)):
    institution = db.get(Institution, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institucion demo no encontrada.")
    return {
        "id": institution.id,
        "display_name": institution.display_name,
        "institution_type": institution.institution_type,
        "active": institution.active,
        "support_label": institution.support_label,
    }


@router.get("/api/integrations/status")
def list_integrations_status(db: Session = Depends(get_db)):
    rows = db.scalars(select(InstitutionIntegration).order_by(InstitutionIntegration.id)).all()
    return [
        {
            "id": item.id,
            "institution_id": item.institution_id,
            "integration_type": item.integration_type,
            "sync_enabled": item.sync_enabled,
            "endpoint_label": item.endpoint_label,
            "external_service": False,
        }
        for item in rows
    ]


@router.get("/api/integrations/events")
def list_integration_events(db: Session = Depends(get_db)):
    rows = db.scalars(select(IntegrationStatusEvent).order_by(IntegrationStatusEvent.id)).all()
    return [
        {
            "id": item.id,
            "integration_id": item.integration_id,
            "status": item.status,
            "severity": item.severity,
            "retry_count": item.retry_count,
            "event_at": item.event_at,
        }
        for item in rows
    ]
