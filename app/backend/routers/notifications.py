from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import (
    Notification,
    NotificationCategory,
    NotificationDeliveryAttempt,
    NotificationPriority,
    NotificationReadEvent,
)
from app.backend.schemas.core import NotificationItem
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


@router.get("", response_model=list[NotificationItem])
def list_notifications(db: Session = Depends(get_db)):
    return list(
        db.scalars(
            select(Notification)
            .where(Notification.user_id == DEMO_USER_ID)
            .order_by(Notification.fecha_recepcion.desc())
        )
    )


@router.get("/categories")
def list_notification_categories(db: Session = Depends(get_db)):
    rows = db.scalars(select(NotificationCategory).order_by(NotificationCategory.id)).all()
    return [
        {
            "category_code": item.category_code,
            "label": item.label,
            "enabled": item.enabled,
            "retention_days": item.retention_days,
        }
        for item in rows
    ]


@router.get("/priorities")
def list_notification_priorities(db: Session = Depends(get_db)):
    rows = db.scalars(select(NotificationPriority).order_by(NotificationPriority.sort_order)).all()
    return [
        {
            "priority_code": item.priority_code,
            "label": item.label,
            "sort_order": item.sort_order,
            "requires_banner": item.requires_banner,
        }
        for item in rows
    ]


@router.get("/read-events")
def list_read_events(db: Session = Depends(get_db)):
    rows = db.scalars(select(NotificationReadEvent).order_by(NotificationReadEvent.id)).all()
    return [
        {
            "id": item.id,
            "notification_id": item.notification_id,
            "read_channel": item.read_channel,
            "acknowledged": item.acknowledged,
            "read_at": item.read_at,
        }
        for item in rows
    ]


@router.get("/delivery-attempts")
def list_delivery_attempts(db: Session = Depends(get_db)):
    rows = db.scalars(select(NotificationDeliveryAttempt).order_by(NotificationDeliveryAttempt.id)).all()
    return [
        {
            "id": item.id,
            "notification_id": item.notification_id,
            "delivery_status": item.delivery_status,
            "channel": item.channel,
            "attempt_number": item.attempt_number,
        }
        for item in rows
    ]


@router.get("/{notification_id}", response_model=NotificationItem)
def get_notification(notification_id: str, db: Session = Depends(get_db)):
    notification = db.get(Notification, notification_id)
    if not notification or notification.user_id != DEMO_USER_ID:
        raise HTTPException(status_code=404, detail="Notificacion demo no encontrada.")
    return notification


@router.post("/{notification_id}/read")
def mark_notification_read(notification_id: str, db: Session = Depends(get_db)):
    notification = db.get(Notification, notification_id)
    if not notification or notification.user_id != DEMO_USER_ID:
        raise HTTPException(status_code=404, detail="Notificacion demo no encontrada.")
    notification.estado = "leida demo"
    db.add(
        NotificationReadEvent(
            notification_id=notification.id,
            read_channel="portal",
            acknowledged=True,
            read_duration_seconds=1,
            read_at="2026-07-08 09:30",
        )
    )
    db.commit()
    return {"success": True, "notification_id": notification.id, "estado": notification.estado}
