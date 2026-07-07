from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_login_2fa_static_assets_exist():
    assert (ROOT / "app/frontend/index.html").exists()
    assert (ROOT / "app/frontend/app.js").exists()
    assert (ROOT / "app/mocks/user.json").exists()


def test_login_2fa_flow_markers_are_present():
    index = read_text("app/frontend/index.html")
    app = read_text("app/frontend/app.js")
    user = read_text("app/mocks/user.json")

    assert "Iniciar sesi" in index
    assert "login-form" in app
    assert "Verificación 2FA" in app
    assert "otp-form" in app
    assert "Dashboard privado" in app
    assert "Cerrar sesión" in app
    assert "demoAuth" in user
    assert "123456" in user
