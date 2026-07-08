from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_health_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_status_ok_and_local_mock():
    response = client.get("/api/status")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert payload["environment"] == "local_mock"
    assert payload["external_services_enabled"] is False
    assert "no produccion" in payload["note"]
