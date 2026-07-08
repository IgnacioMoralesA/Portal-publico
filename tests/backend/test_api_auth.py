from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_login_correcto_requiere_otp():
    response = client.post(
        "/api/auth/login",
        json={"username": "demo.claveunica", "password": "DemoLocal2026"},
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["requires_otp"] is True
    assert payload["session_id"] == "SES-DEMO-001"


def test_login_incorrecto_rechaza_credenciales():
    response = client.post(
        "/api/auth/login",
        json={"username": "demo.claveunica", "password": "incorrecta"},
    )

    assert response.status_code == 401
    assert "invalidas" in response.json()["detail"]


def test_otp_correcto_entrega_token_demo():
    response = client.post("/api/auth/verify-otp", json={"otp": "123456"})
    payload = response.json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["token"] == "demo-local-token"


def test_otp_incorrecto_rechaza_factor():
    response = client.post("/api/auth/verify-otp", json={"otp": "000000"})

    assert response.status_code == 401
    assert "invalido" in response.json()["detail"]
