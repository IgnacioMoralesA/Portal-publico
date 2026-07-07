import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_authorizations_section_markers_are_present():
    app = read_text("app/frontend/app.js")
    styles = read_text("app/frontend/styles.css")
    authorizations = read_text("app/mocks/authorizations.json")

    assert "Autorizaciones" in app
    assert "authorizationsView" in app
    assert "Resumen de autorizaciones por estado" in app
    assert "pendientes" in app
    assert "aprobadas/vigentes" in app
    assert "rechazadas" in app
    assert "revocadas" in app
    assert "Lista mock de autorizaciones" in app
    assert "Detalle de autorizacion" in app
    assert "Aprobar solicitud" in app
    assert "Rechazar solicitud" in app
    assert "Revocar autorizacion" in app
    assert "Factor demo obligatorio" in app
    assert "Historial local de autorizacion" in app
    assert "Volver al dashboard" in app
    assert "simulado/local" in app
    assert "claveunica_demo_authorization_state" in app
    assert "sessionStorage" in app
    assert "authorization-card" in styles
    assert "authorization-history" in styles
    assert "AUT-DEMO-001" in authorizations


def test_authorizations_mock_uses_safe_demo_data():
    authorizations = json.loads(read_text("app/mocks/authorizations.json"))
    states = {item["estado"] for item in authorizations}

    assert len(authorizations) >= 5
    assert {"pendiente", "aprobada", "rechazada", "revocada"}.issubset(states)
    assert all("id" in item for item in authorizations)
    assert all("institucion" in item for item in authorizations)
    assert all("finalidad" in item for item in authorizations)
    assert all("tipoDato" in item for item in authorizations)
    assert all("fechaSolicitud" in item for item in authorizations)
    assert all("fechaDecision" in item for item in authorizations)
    assert all("historial" in item for item in authorizations)

    joined = json.dumps(authorizations, ensure_ascii=False).lower()
    assert "demo" in joined or "ficticia" in joined or "simulada" in joined
    assert "@" not in joined
    assert "run-" not in joined
    assert "run" not in joined
    assert "rut" not in joined
    assert "calle" not in joined
    assert "avenida" not in joined
    assert not re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", joined)


def test_authorizations_docs_cover_local_simulation_scope():
    readme = read_text("app/README.md")
    backlog = read_text("docs/BACKLOG_TECNICO.md")

    assert "Autorizaciones demo" in readme
    assert "resumen por estados" in readme
    assert "aprobar o rechazar" in readme
    assert "revocarla" in readme
    assert "factor demo `123456`" in readme
    assert "No usa autorizaciones reales" in readme
    assert "no muestra datos sensibles reales" in readme
    assert "no es una funcionalidad lista para produccion" in readme
    assert "Autorizaciones de datos sensibles" in backlog
    assert "Estado: implementado en prototipo local" in backlog
    assert "historial local en `sessionStorage`" in backlog


def test_no_real_services_or_productive_urls_are_added_for_authorizations():
    checked = "\n".join(
        [
            read_text("app/frontend/app.js"),
            read_text("app/frontend/index.html"),
            read_text("app/mocks/authorizations.json"),
            read_text("app/README.md"),
        ]
    ).lower()

    forbidden = [
        "accounts.claveunica",
        "api.claveunica",
        "claveunica.gob.cl",
        "casillaunica.gob.cl",
        "api.casillaunica",
        "notificaciones.gob.cl",
        "openid",
        "oauth/",
        "oauth2",
        "oauth/token",
        "client_secret",
        "access_token",
        "https://",
        "autorizacion real cargada",
        "dato sensible real cargado",
    ]

    for marker in forbidden:
        assert marker not in checked

    assert "run-" not in read_text("app/mocks/authorizations.json").lower()
