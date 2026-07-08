from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import DduActivationEvent, DduCancellationEvent, DduProfile
from app.backend.schemas.core import DduStatusOut
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


@router.get("/status", response_model=DduStatusOut)
def get_ddu_status(db: Session = Depends(get_db)):
    ddu = db.scalar(select(DduProfile).where(DduProfile.user_id == DEMO_USER_ID))
    if not ddu:
        raise HTTPException(status_code=404, detail="DDU demo no encontrado.")
    return ddu


@router.post("/configure")
def configure_ddu(db: Session = Depends(get_db)):
    ddu = db.scalar(select(DduProfile).where(DduProfile.user_id == DEMO_USER_ID))
    if not ddu:
        raise HTTPException(status_code=404, detail="DDU demo no encontrado.")
    ddu.estado = "configurado"
    ddu.domicilio = "Casilla demo configurada localmente"
    ddu.alerta_pendiente = False
    ddu.fecha_configuracion = "2026-07-08 09:20"
    ddu.canal = "portal local"
    ddu.casilla_demo = "casilla-demo-local"
    event = db.get(DduActivationEvent, "DDU-ACT-API")
    if not event:
        db.add(
            DduActivationEvent(
                id="DDU-ACT-API",
                user_id=DEMO_USER_ID,
                activation_status="completada demo",
                origin_channel="portal",
                requires_confirmation=False,
                event_at="2026-07-08 09:20",
            )
        )
    db.commit()
    return {"success": True, "estado": ddu.estado, "casilla_demo": ddu.casilla_demo}


@router.post("/cancel")
def cancel_ddu(db: Session = Depends(get_db)):
    ddu = db.scalar(select(DduProfile).where(DduProfile.user_id == DEMO_USER_ID))
    if not ddu:
        raise HTTPException(status_code=404, detail="DDU demo no encontrado.")
    ddu.estado = "pendiente"
    ddu.alerta_pendiente = True
    ddu.fecha_configuracion = ""
    ddu.canal = ""
    ddu.casilla_demo = ""
    event = db.get(DduCancellationEvent, "DDU-CAN-API")
    if not event:
        db.add(
            DduCancellationEvent(
                id="DDU-CAN-API",
                user_id=DEMO_USER_ID,
                cancellation_status="confirmada demo",
                reason_code="usuario",
                restored_previous_state=True,
                event_at="2026-07-08 09:25",
            )
        )
    db.commit()
    return {"success": True, "estado": ddu.estado, "alerta_pendiente": ddu.alerta_pendiente}


@router.get("/events")
def list_ddu_events(db: Session = Depends(get_db)):
    activations = [
        {
            "id": item.id,
            "event_type": "activation",
            "status": item.activation_status,
            "channel": item.origin_channel,
            "event_at": item.event_at,
        }
        for item in db.scalars(select(DduActivationEvent).where(DduActivationEvent.user_id == DEMO_USER_ID))
    ]
    cancellations = [
        {
            "id": item.id,
            "event_type": "cancellation",
            "status": item.cancellation_status,
            "reason_code": item.reason_code,
            "event_at": item.event_at,
        }
        for item in db.scalars(select(DduCancellationEvent).where(DduCancellationEvent.user_id == DEMO_USER_ID))
    ]
    return activations + cancellations


@router.get("/activation-summary")
def get_activation_summary(db: Session = Depends(get_db)):
    ddu = db.scalar(select(DduProfile).where(DduProfile.user_id == DEMO_USER_ID))
    if not ddu:
        raise HTTPException(status_code=404, detail="DDU demo no encontrado.")
    return {
        "estado": ddu.estado,
        "alerta_pendiente": ddu.alerta_pendiente,
        "usa_servicio_real": False,
        "nota": "Configuracion local/mock sin CasillaUnica real.",
    }
