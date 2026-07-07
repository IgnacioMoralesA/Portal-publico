import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_ddu_section_and_gateway_markers_are_present():
    app = read_text("app/frontend/app.js")
    styles = read_text("app/frontend/styles.css")
    ddu = read_text("app/mocks/ddu.json")

    assert "Domicilio Digital Unico (DDU)" in app
    assert "Estado DDU" in app
    assert "pendiente/no configurado" in app
    assert "configurado" in app
    assert "Alerta de configuracion pendiente" in app
    assert "Confirmar derivacion simulada DDU" in app
    assert "modal-dialog" in app
    assert "Pasarela simulada de configuracion DDU" in app
    assert "Cancelar configuracion" in app
    assert "Retornar al portal" in app
    assert "Volver al dashboard" in app
    assert "acceso preparado" in app
    assert "Ir a Notificaciones" in app
    assert "sessionStorage" in app
    assert "claveunica_demo_ddu_state" in app
    assert "modal-backdrop" in styles
    assert "ddu-gateway" in styles
    assert "pendiente" in ddu


def test_ddu_mock_uses_only_safe_demo_data():
    ddu = json.loads(read_text("app/mocks/ddu.json"))
    joined = json.dumps(ddu, ensure_ascii=False).lower()

    assert ddu["estado"] == "pendiente"
    assert ddu["alertaPendiente"] is True
    assert "demo" in joined
    assert "real" in joined
    assert "casillaunica" in joined
    assert "@" not in joined
    assert not re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", joined)
    assert "calle" not in joined
    assert "avenida" not in joined
    assert "rut" not in joined
    assert "run" not in joined


def test_ddu_docs_cover_local_simulation_scope():
    readme = read_text("app/README.md")
    backlog = read_text("docs/BACKLOG_TECNICO.md")

    assert "DDU demo" in readme
    assert "Estado inicial demo" in readme
    assert "cancelar desde el modal" in readme
    assert "pasarela simulada" in readme
    assert "No usa CasillaUnica real" in readme
    assert "no configura DDU real" in readme
    assert "No es una funcionalidad lista para produccion" in readme
    assert "DDU / Domicilio Digital" in backlog
    assert "Estado: implementado en prototipo local" in backlog
    assert "pasarela simulada" in backlog


def test_no_real_claveunica_or_casillaunica_service_urls_are_added_for_ddu():
    checked = "\n".join(
        [
            read_text("app/frontend/app.js"),
            read_text("app/frontend/index.html"),
            read_text("app/mocks/ddu.json"),
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
    ]

    for marker in forbidden:
        assert marker not in checked
