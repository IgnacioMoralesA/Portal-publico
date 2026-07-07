import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_notifications_section_and_ddu_gate_markers_are_present():
    app = read_text("app/frontend/app.js")
    styles = read_text("app/frontend/styles.css")
    notifications = read_text("app/mocks/notifications.json")

    assert "Notificaciones" in app
    assert "notificationsView" in app
    assert "getDduState" in app
    assert "DDU pendiente requerido" in app
    assert "Ir a DDU" in app
    assert "No se muestra listado mientras el DDU esta pendiente/no configurado" in app
    assert "Listado de notificaciones pendientes" in app
    assert "Fecha de recepcion ficticia" in app
    assert "Institucion remitente ficticia" in app
    assert "Estado" in app
    assert "Prioridad/categoria" in app
    assert "Abrir detalle" in app
    assert "Detalle local seguro" in app
    assert "derivacion simulada/local a CasillaUnica" in app
    assert "Marcar como leida" in app
    assert "Volver al listado" in app
    assert "Volver al dashboard" in app
    assert "claveunica_demo_notification_reads" in app
    assert "notification-card" in styles
    assert "NOT-001" in notifications


def test_notifications_mock_uses_safe_demo_data():
    notifications = json.loads(read_text("app/mocks/notifications.json"))

    assert len(notifications) >= 2
    assert all(item["estado"] == "pendiente" for item in notifications)
    assert all("fechaRecepcion" in item for item in notifications)
    assert all("institucion" in item for item in notifications)
    assert all("titulo" in item for item in notifications)
    assert all("prioridad" in item for item in notifications)
    assert all("categoria" in item for item in notifications)
    assert all("contenido" in item for item in notifications)

    joined = json.dumps(notifications, ensure_ascii=False).lower()
    assert "demo" in joined
    assert "ficticio" in joined or "simulado" in joined
    assert "@" not in joined
    assert not re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", joined)
    assert "run" not in joined
    assert "rut" not in joined
    assert "calle" not in joined
    assert "avenida" not in joined
    assert "documentos reales" in joined


def test_notifications_docs_cover_local_simulation_scope():
    readme = read_text("app/README.md")
    backlog = read_text("docs/BACKLOG_TECNICO.md")

    assert "Notificaciones demo" in readme
    assert "DDU pendiente" in readme
    assert "listado mock de notificaciones pendientes" in readme
    assert "Abrir el detalle" in readme
    assert "Marcar la notificacion como leida" in readme
    assert "No usa CasillaUnica real" in readme
    assert "no usa notificaciones reales" in readme
    assert "no es una funcionalidad lista para produccion" in readme
    assert "Notificaciones / Casilla" in backlog
    assert "Estado: implementado en prototipo local" in backlog
    assert "derivacion simulada/local a CasillaUnica" in backlog


def test_no_real_claveunica_or_casillaunica_service_urls_are_added_for_notifications():
    checked = "\n".join(
        [
            read_text("app/frontend/app.js"),
            read_text("app/frontend/index.html"),
            read_text("app/mocks/notifications.json"),
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
        "documento real",
        "notificacion real cargada",
    ]

    for marker in forbidden:
        assert marker not in checked
