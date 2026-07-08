from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import DeploymentTarget, ProductChecklistItem, TestEvidenceRecord


router = APIRouter()


@router.get("/api/evidence/tests")
def list_test_evidence(db: Session = Depends(get_db)):
    rows = db.scalars(select(TestEvidenceRecord).order_by(TestEvidenceRecord.id)).all()
    return [
        {
            "id": item.id,
            "evidence_type": item.evidence_type,
            "result": item.result,
            "command": item.command,
            "recorded_at": item.recorded_at,
        }
        for item in rows
    ]


@router.get("/api/product/checklist")
def list_product_checklist(db: Session = Depends(get_db)):
    rows = db.scalars(select(ProductChecklistItem).order_by(ProductChecklistItem.id)).all()
    return [
        {
            "id": item.id,
            "title": item.title,
            "item_status": item.item_status,
            "criterion_type": item.criterion_type,
            "owner_agent": item.owner_agent,
        }
        for item in rows
    ]


@router.get("/api/deployment-targets")
def list_deployment_targets(db: Session = Depends(get_db)):
    rows = db.scalars(select(DeploymentTarget).order_by(DeploymentTarget.id)).all()
    return [
        {
            "id": item.id,
            "environment": item.environment,
            "target_status": item.target_status,
            "external_network_enabled": item.external_network_enabled,
            "deployment_note": item.deployment_note,
        }
        for item in rows
    ]
