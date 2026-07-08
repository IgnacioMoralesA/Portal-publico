from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import TrustedDevice
from app.backend.schemas.core import TrustDeviceIn
from app.backend.seed import DEMO_USER_ID


router = APIRouter()


@router.get("/trusted")
def list_trusted_devices(db: Session = Depends(get_db)):
    rows = db.scalars(select(TrustedDevice).where(TrustedDevice.user_id == DEMO_USER_ID).order_by(TrustedDevice.id)).all()
    return [
        {
            "id": item.id,
            "device_label": item.device_label,
            "device_status": item.device_status,
            "trust_score": item.trust_score,
            "remember_device": item.remember_device,
        }
        for item in rows
    ]


@router.post("/{device_id}/trust")
def trust_device(device_id: str, payload: TrustDeviceIn, db: Session = Depends(get_db)):
    device = db.get(TrustedDevice, device_id)
    if not device or device.user_id != DEMO_USER_ID:
        raise HTTPException(status_code=404, detail="Dispositivo demo no encontrado.")
    device.device_status = "confiable"
    device.remember_device = payload.remember_device
    device.trust_score = max(device.trust_score, 75)
    db.commit()
    return {"success": True, "device_id": device.id, "device_status": device.device_status}


@router.delete("/{device_id}/trust")
def revoke_device_trust(device_id: str, db: Session = Depends(get_db)):
    device = db.get(TrustedDevice, device_id)
    if not device or device.user_id != DEMO_USER_ID:
        raise HTTPException(status_code=404, detail="Dispositivo demo no encontrado.")
    device.device_status = "revocado"
    device.remember_device = False
    device.trust_score = 0
    db.commit()
    return {"success": True, "device_id": device.id, "device_status": device.device_status}
