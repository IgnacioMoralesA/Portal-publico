import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


APP_ASSETS = [
    "app/frontend/index.html",
    "app/frontend/app.js",
    "app/frontend/styles.css",
    "app/README.md",
]

MOCK_ASSETS = [
    "app/mocks/user.json",
    "app/mocks/ddu.json",
    "app/mocks/sessions.json",
    "app/mocks/notifications.json",
    "app/mocks/authorizations.json",
]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path):
    return json.loads(read_text(path))


def joined_assets(paths):
    return "\n".join(read_text(path) for path in paths)


def test_no_productive_service_urls_or_external_integrations_in_app_assets():
    checked = joined_assets(APP_ASSETS + MOCK_ASSETS).lower()

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
        "saml",
        "client_id",
        "client_secret",
        "access_token",
        "refresh_token",
        "private_key",
        "-----begin",
    ]

    for marker in forbidden:
        assert marker not in checked

    assert "fetch(\"../mocks/" in checked
    assert "http://" not in joined_assets(["app/frontend/index.html", "app/frontend/app.js", "app/frontend/styles.css"]).lower()
    assert "https://" not in checked


def test_demo_storage_scope_is_session_only_and_documented():
    app = read_text("app/frontend/app.js")
    readme = read_text("app/README.md").lower()

    assert "sessionStorage" in app
    assert "localStorage" not in app
    assert "estado demo/local" in readme
    assert "no usa backend real" in readme
    assert "no conecta servicios externos" in readme


def test_mocks_do_not_contain_real_ips_or_unmasked_run_values():
    checked = joined_assets(MOCK_ASSETS)

    assert not re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", checked)
    assert not re.search(r"\b\d{1,2}\.\d{3}\.\d{3}-[\dkK]\b", checked)
    assert "runEnmascarado" in checked
    assert "***" in checked
    assert "run-" not in checked.lower()


def test_mocks_use_safe_demo_identity_and_fictitious_content():
    user = read_json("app/mocks/user.json")
    ddu = read_json("app/mocks/ddu.json")
    sessions = read_json("app/mocks/sessions.json")
    notifications = read_json("app/mocks/notifications.json")
    authorizations = read_json("app/mocks/authorizations.json")
    joined = json.dumps(
        {
            "user": user,
            "ddu": ddu,
            "sessions": sessions,
            "notifications": notifications,
            "authorizations": authorizations,
        },
        ensure_ascii=False,
    ).lower()

    assert user["nombre"] == "Persona de prueba"
    assert user["correo"].endswith("example.cl")
    assert user["demoAuth"]["usuario"] == "demo.claveunica"
    assert user["demoAuth"]["clave"] == "DemoLocal2026"
    assert user["demoAuth"]["otp"] == "123456"
    assert "demo" in joined
    assert "fictici" in joined or "simulad" in joined
    assert all("ip" not in item for item in sessions)
    assert all(item["id"].startswith("AUT-DEMO-") for item in authorizations)


def test_no_real_run_personal_data_or_binary_annex_references_in_mocks():
    mocks = joined_assets(MOCK_ASSETS).lower()

    forbidden_personal_markers = [
        "calle ",
        "avenida ",
        "pasaporte",
        "licencia",
        "documento real",
        "dato sensible real",
        "notificacion real",
        "autorizacion real",
    ]

    for marker in forbidden_personal_markers:
        assert marker not in mocks

    assert "anexo" not in mocks
    assert ".pdf" not in mocks
    assert ".docx" not in mocks
