from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_sesion_actual_y_eventos_responden():
    current = client.get("/api/sessions/current")
    events = client.get("/api/sessions/events")

    assert current.status_code == 200
    assert current.json()["actual"] is True
    assert events.status_code == 200
    assert isinstance(events.json(), list)


def test_cierre_remoto_de_sesion_mock():
    response = client.post("/api/sessions/SES-DEMO-002/close")
    payload = response.json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["estado"] == "cerrada demo"


def test_dispositivos_confiables_permiten_trust_y_revocacion():
    listed = client.get("/api/devices/trusted")
    trusted = client.post("/api/devices/DEV-DEMO-001/trust", json={"remember_device": True})
    revoked = client.delete("/api/devices/DEV-DEMO-001/trust")

    assert listed.status_code == 200
    assert trusted.status_code == 200
    assert trusted.json()["device_status"] == "confiable"
    assert revoked.status_code == 200
    assert revoked.json()["device_status"] == "revocado"
