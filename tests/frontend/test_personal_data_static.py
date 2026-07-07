from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_personal_data_section_markers_are_present():
    app = read_text("app/frontend/app.js")
    user = read_text("app/mocks/user.json")

    assert "Datos personales" in app
    assert "personal-data-form" in app
    assert "Correo" in app
    assert "Telefono" in app
    assert "Editar correo electronico" in app
    assert "Editar telefono" in app
    assert "Factor de seguridad simulado" in app
    assert "Factor de seguridad incorrecto" in app
    assert "Datos personales actualizados localmente" in app
    assert "Volver al dashboard" in app
    assert "runEnmascarado" in user
    assert "personalSecurity" in user
    assert "codigoDemo" in user


def test_personal_data_docs_cover_demo_security_scope():
    readme = read_text("app/README.md")
    backlog = read_text("docs/BACKLOG_TECNICO.md")

    assert "Datos personales demo" in readme
    assert "factor de seguridad demo `123456`" in readme
    assert "No se guarda en backend" in readme
    assert "servicios reales de ClaveUnica" in readme
    assert "Estado: implementado en prototipo local" in backlog
    assert "factor de seguridad demo" in backlog


def test_no_real_claveunica_service_references_are_added():
    checked = "\n".join(
        [
            read_text("app/frontend/app.js"),
            read_text("app/frontend/index.html"),
            read_text("app/mocks/user.json"),
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
