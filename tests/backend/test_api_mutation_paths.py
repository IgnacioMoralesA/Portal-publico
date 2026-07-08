from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_auth_factor_recovery_logout_and_contact_paths():
    assert client.post("/api/auth/logout").status_code == 200

    factors = client.get("/api/auth/factors")
    assert factors.status_code == 200
    factor_type = factors.json()[0]["factor_type"]

    toggled = client.post("/api/auth/factors/toggle", json={"factor_type": factor_type, "enabled": False})
    assert toggled.status_code == 200
    assert toggled.json()["enabled"] is False

    missing_factor = client.post("/api/auth/factors/toggle", json={"factor_type": "missing", "enabled": True})
    assert missing_factor.status_code == 404

    attempts = client.get("/api/auth/login-attempts")
    assert attempts.status_code == 200

    missing_user = client.post("/api/auth/recovery/request", json={"username": "nadie", "channel": "email"})
    assert missing_user.status_code == 404

    requested = client.post("/api/auth/recovery/request", json={"username": "demo.claveunica", "channel": "sms"})
    assert requested.status_code == 200
    recovery_id = requested.json()["recovery_id"]

    bad_recovery = client.post("/api/auth/recovery/confirm", json={"recovery_id": recovery_id, "otp": "000000"})
    assert bad_recovery.status_code == 401

    confirmed = client.post("/api/auth/recovery/confirm", json={"recovery_id": recovery_id, "otp": "123456"})
    assert confirmed.status_code == 200

    missing_recovery = client.post("/api/auth/recovery/confirm", json={"recovery_id": "missing", "otp": "123456"})
    assert missing_recovery.status_code == 404

    bad_contact = client.patch("/api/users/me/contact", json={"correo": "demo@example.cl", "otp": "000000"})
    assert bad_contact.status_code == 401

    contact = client.patch(
        "/api/users/me/contact",
        json={"correo": "persona@example.cl", "telefono": "+56 9 1234 5678", "otp": "123456"},
    )
    assert contact.status_code == 200

    questions = client.get("/api/users/me/security-questions")
    assert questions.status_code == 200

    verified = client.post("/api/users/me/security-questions/verify", json={"answer": " respuesta demo "})
    assert verified.status_code == 200


def test_more_mutation_error_paths_and_lists():
    assert client.get("/api/ddu/status").status_code == 200
    assert client.get("/api/authorizations").status_code == 200
    assert client.get("/api/notifications").status_code == 200
    assert client.get("/api/sessions").status_code == 200

    current_close = client.post("/api/sessions/SES-DEMO-001/close")
    assert current_close.status_code == 409

    for path in (
        "/api/authorizations/missing",
        "/api/notifications/missing",
        "/api/institutions/missing",
    ):
        assert client.get(path).status_code == 404

    for path in (
        "/api/authorizations/missing/approve",
        "/api/notifications/missing/read",
        "/api/sessions/missing/close",
        "/api/devices/missing/trust",
    ):
        assert client.post(path, json={"otp": "123456", "remember_device": True}).status_code == 404

    assert client.delete("/api/devices/missing/trust").status_code == 404
