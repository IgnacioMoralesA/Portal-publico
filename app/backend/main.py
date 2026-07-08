from fastapi import FastAPI

from app.backend.config import settings
from app.backend.routers import auth, authorizations, ddu, health, notifications, sessions, users
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
    app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
    app.include_router(authorizations.router, prefix="/api/authorizations", tags=["authorizations"])
    return app


app = create_app()


if __name__ == "__main__":
    print(f"{settings.app_name} import OK; use uvicorn app.backend.main:app --reload to serve locally.")
