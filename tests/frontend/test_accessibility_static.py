import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_main_semantic_shell_and_public_navigation_exist():
    index = read_text("app/frontend/index.html")

    assert '<html lang="es">' in index
    assert '<meta name="viewport"' in index
    assert '<header class="site-header">' in index
    assert '<main id="app" tabindex="-1"></main>' in index
    assert 'aria-label="Navegaci' in index
    assert 'data-action="login"' in index
    assert "<footer" in index


def test_core_views_have_accessible_headings_and_navigation():
    app = read_text("app/frontend/app.js")

    expected_markers = [
        'aria-labelledby="portal-title"',
        'id="portal-title"',
        'aria-labelledby="login-title"',
        'id="login-title"',
        'aria-labelledby="otp-title"',
        'id="otp-title"',
        'aria-labelledby="dashboard-title"',
        'id="dashboard-title"',
        'aria-labelledby="personal-data-title"',
        'aria-labelledby="sessions-title"',
        'aria-labelledby="ddu-title"',
        'aria-labelledby="notifications-title"',
        'aria-labelledby="authorizations-title"',
        'aria-current',
    ]

    for marker in expected_markers:
        assert marker in app


def test_forms_keep_programmatic_labels_and_input_hints():
    app = read_text("app/frontend/app.js")

    label_pairs = [
        ("login-user", "Usuario demo"),
        ("login-password", "Clave demo"),
        ("otp-code", "OTP demo"),
        ("personal-email", "correo"),
        ("personal-phone", "telefono"),
        ("personal-security-code", "seguridad"),
        ("ddu-demo-channel", "Canal/casilla demo"),
        ("authorization-security-code", "Factor demo"),
    ]

    for field_id, label_text in label_pairs:
        assert f'for="{field_id}"' in app
        assert label_text in app

    assert 'autocomplete="username"' in app
    assert 'autocomplete="current-password"' in app
    assert app.count('autocomplete="one-time-code"') >= 3


def test_actions_use_buttons_or_links_with_keyboard_reachable_targets():
    app = read_text("app/frontend/app.js")

    required_actions = [
        'type="button" data-action="login"',
        'type="submit">Continuar',
        'type="submit">Validar',
        'data-action="logout"',
        'data-action="close-remote-session"',
        'data-action="open-ddu-confirmation"',
        'data-action="mark-notification-read"',
        'data-action="open-authorization"',
        'data-authorization-decision="aprobar"',
        'data-authorization-decision="rechazar"',
        'data-authorization-decision="revocar"',
    ]

    for marker in required_actions:
        assert marker in app


def test_status_messages_and_modal_have_accessibility_contracts():
    app = read_text("app/frontend/app.js")

    assert 'role="alert"' in app
    assert 'aria-live="assertive"' in app
    assert 'aria-live="polite"' in app
    assert 'role="note"' in app
    assert 'role="dialog"' in app
    assert 'aria-modal="true"' in app
    assert 'aria-labelledby="ddu-modal-title"' in app


def test_focus_visible_and_responsive_rules_exist():
    styles = read_text("app/frontend/styles.css")

    assert ":focus-visible" in styles
    assert "outline:" in styles
    assert "@media (max-width: 820px)" in styles
    assert re.search(r"\.hero,\s*\n\s*\.auth-layout,\s*\n\s*\.private-layout", styles)
    assert "grid-template-columns: 1fr" in styles
