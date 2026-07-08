from pathlib import Path

from fastapi.testclient import TestClient

from app.backend.main import app


ROOT = Path(__file__).resolve().parents[2]
client = TestClient(app)


def test_users_me_devuelve_usuario_demo():
    response = client.get("/api/users/me")
    payload = response.json()

    assert response.status_code == 200
    assert payload["id"] == "USR-001"
    assert payload["username"] == "demo.claveunica"
    assert payload["run_enmascarado"] == "12.345.***-*"
    assert payload["sesiones_activas"] >= 1


def test_endpoints_principales_responden_con_datos_demo():
    expected = {
        "/api/ddu/status": dict,
        "/api/sessions": list,
        "/api/notifications": list,
        "/api/authorizations": list,
    }

    for path, payload_type in expected.items():
        response = client.get(path)
        assert response.status_code == 200
        assert isinstance(response.json(), payload_type)


def test_no_urls_productivas_reales_en_backend():
    backend_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "app" / "backend").rglob("*.py")
    ).lower()

    forbidden = [
        "accounts.claveunica",
        "api.claveunica",
        "claveunica.gob.cl",
        "casillaunica.gob.cl",
        "api.casillaunica",
        "notificaciones.gob.cl",
        "oauth/token",
        "saml",
    ]
    for marker in forbidden:
        assert marker not in backend_text


def test_no_secretos_reales_en_backend():
    backend_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "app" / "backend").rglob("*.py")
    ).lower()

    forbidden = ["sk-", "-----begin", "private_key", "client_secret", "refresh_token"]
    for marker in forbidden:
        assert marker not in backend_text

    assert "demo-local-token" in backend_text
    assert "DemoLocal2026".lower() in backend_text
