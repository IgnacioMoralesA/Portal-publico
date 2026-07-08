from fastapi import APIRouter

from app.backend.config import settings
from app.backend.schemas.core import ApiStatusOut, HealthOut


router = APIRouter()


@router.get("/health", response_model=HealthOut)
def health_check():
    return HealthOut(status="ok", version=settings.version)


@router.get("/api/status", response_model=ApiStatusOut)
def api_status():
    return ApiStatusOut(
        status="ok",
        environment=settings.environment,
        app_name=settings.app_name,
        external_services_enabled=settings.external_services_enabled,
        note="Backend local/mock con datos ficticios; no produccion.",
    )
