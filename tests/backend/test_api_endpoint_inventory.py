from pathlib import Path

from fastapi.testclient import TestClient

from app.backend.main import app


ROOT = Path(__file__).resolve().parents[2]
client = TestClient(app)


def test_existen_al_menos_40_rutas_api_registradas():
    api_routes = {
        route.path
        for route in app.routes
        if getattr(route, "path", "").startswith("/api/")
    }

    assert len(api_routes) >= 40


def test_endpoints_nuevos_principales_responden():
    paths = [
        "/api/auth/factors",
        "/api/users/me/profile",
        "/api/sessions/current",
        "/api/devices/trusted",
        "/api/ddu/activation-summary",
        "/api/notifications/categories",
        "/api/authorizations/history",
        "/api/institutions",
        "/api/integrations/status",
        "/api/public/news",
        "/api/help/categories",
        "/api/audit/events",
        "/api/evidence/tests",
        "/api/product/checklist",
        "/api/business-rules",
        "/api/validation-rules",
        "/api/screens",
        "/api/deployment-targets",
    ]

    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, path


def test_backend_no_declara_servicios_productivos_ni_secretos_reales():
    backend_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "app" / "backend").rglob("*.py")
    ).lower()

    forbidden = [
        "accounts.claveunica",
        "api.claveunica",
        "casillaunica.gob.cl",
        "notificaciones.gob.cl",
        "client_secret",
        "private_key",
        "-----begin",
        "refresh_token",
    ]
    for marker in forbidden:
        assert marker not in backend_text


def test_backend_no_usa_datos_personales_reales():
    backend_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "app" / "backend").rglob("*.py")
    ).lower()

    assert "persona de prueba" in backend_text
    assert "example.cl" in backend_text
    assert "datos personales reales" in backend_text
