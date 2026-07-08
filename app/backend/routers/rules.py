from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import BusinessRule, PrototypeScreen, ValidationRule


router = APIRouter()


@router.get("/api/business-rules")
def list_business_rules(db: Session = Depends(get_db)):
    rows = db.scalars(select(BusinessRule).order_by(BusinessRule.id)).all()
    return [
        {
            "id": item.id,
            "title": item.title,
            "rule_status": item.rule_status,
            "rule_domain": item.rule_domain,
            "priority": item.priority,
            "source_ref": item.source_ref,
        }
        for item in rows
    ]


@router.get("/api/validation-rules")
def list_validation_rules(db: Session = Depends(get_db)):
    rows = db.scalars(select(ValidationRule).order_by(ValidationRule.id)).all()
    return [
        {
            "id": item.id,
            "target": item.target,
            "validation_type": item.validation_type,
            "severity": item.severity,
            "automated": item.automated,
            "description": item.description,
        }
        for item in rows
    ]


@router.get("/api/screens")
def list_screens(db: Session = Depends(get_db)):
    rows = db.scalars(select(PrototypeScreen).order_by(PrototypeScreen.id)).all()
    return [
        {
            "id": item.id,
            "name": item.name,
            "screen_area": item.screen_area,
            "screen_status": item.screen_status,
            "requires_auth": item.requires_auth,
            "route_hint": item.route_hint,
        }
        for item in rows
    ]
