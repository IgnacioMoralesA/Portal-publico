import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_sessions_section_markers_are_present():
    app = read_text("app/frontend/app.js")
    styles = read_text("app/frontend/styles.css")
    sessions = read_text("app/mocks/sessions.json")

    assert "Sesiones" in app
    assert "Lista de sesiones activas" in app
    assert "sesion actual" in app
    assert "Cerrar sesion remota" in app
    assert "Advertencia de multisesion simulada" in app
    assert "Volver al dashboard" in app
    assert "simulacion de politica de multisesion" in app
    assert "solo estado demo/local" in app
    assert "closeRemoteSession" in app
    assert "session-card" in styles
    assert "current-session" in styles
    assert "SES-DEMO-001" in sessions


def test_sessions_mock_uses_safe_demo_data():
    sessions = json.loads(read_text("app/mocks/sessions.json"))

    assert len(sessions) >= 3
    assert any(item["actual"] is True for item in sessions)
    assert any(item["actual"] is False for item in sessions)
    assert all("dispositivo" in item for item in sessions)
    assert all("navegador" in item for item in sessions)
    assert all("ubicacion" in item for item in sessions)
    assert all("ultimoAcceso" in item for item in sessions)
    assert all("estado" in item for item in sessions)
    assert all("ip" not in item for item in sessions)

    joined = json.dumps(sessions, ensure_ascii=False).lower()
    assert not re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", joined)
    assert "@" not in joined
    assert "run" not in joined
    assert "rut" not in joined
    assert "calle" not in joined
    assert "avenida" not in joined


def test_sessions_docs_cover_local_simulation_scope():
    readme = read_text("app/README.md")
    backlog = read_text("docs/BACKLOG_TECNICO.md")

    assert "Sesiones demo" in readme
    assert "sesiones son simuladas" in readme
    assert "no hay proteccion real productiva" in readme
    assert "no usa servicios reales" in readme
    assert "Estado: implementado en prototipo local" in backlog
    assert "gestion de sesiones activa ficticia" in backlog


def test_no_real_claveunica_service_references_or_ips_in_sessions_assets():
    checked = "\n".join(
        [
            read_text("app/frontend/app.js"),
            read_text("app/frontend/index.html"),
            read_text("app/mocks/sessions.json"),
            read_text("app/README.md"),
        ]
    ).lower()

    forbidden = [
        "accounts.claveunica",
        "api.claveunica",
        "claveunica.gob.cl",
        "openid",
        "oauth/",
        "oauth2",
        "oauth/token",
        "client_secret",
        "access_token",
    ]

    for marker in forbidden:
        assert marker not in checked

    assert not re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", checked)
