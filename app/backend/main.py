from fastapi import FastAPI

from app.backend.config import settings
from app.backend.routers import (
    audit,
    auth,
    authorizations,
    ddu,
    devices,
    evidence,
    health,
    help,
    institutions,
    notifications,
    public,
    rules,
    sessions,
    users,
)
from app.backend.seed import init_db


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="API local/mock sin integraciones reales de ClaveUnica, CasillaUnica ni servicios estatales.",
    )
    app.include_router(health.router)
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(users.router, prefix="/api/users", tags=["users"])
    app.include_router(ddu.router, prefix="/api/ddu", tags=["ddu"])
    app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
    app.include_router(devices.router, prefix="/api/devices", tags=["devices"])
    app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
    app.include_router(authorizations.router, prefix="/api/authorizations", tags=["authorizations"])
    app.include_router(institutions.router, tags=["institutions"])
    app.include_router(public.router, prefix="/api/public", tags=["public"])
    app.include_router(help.router, prefix="/api/help", tags=["help"])
    app.include_router(audit.router, prefix="/api/audit", tags=["audit"])
    app.include_router(evidence.router, tags=["evidence"])
    app.include_router(rules.router, tags=["rules"])
    return app


app = create_app()


if __name__ == "__main__":
    print(f"{settings.app_name} import OK; use uvicorn app.backend.main:app --reload to serve locally.")
