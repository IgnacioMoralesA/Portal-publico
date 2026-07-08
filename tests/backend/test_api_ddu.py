from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_ddu_configurar_cancelar_y_resumen_mock():
    configured = client.post("/api/ddu/configure")
    summary = client.get("/api/ddu/activation-summary")
    cancelled = client.post("/api/ddu/cancel")
    events = client.get("/api/ddu/events")

    assert configured.status_code == 200
    assert configured.json()["estado"] == "configurado"
    assert summary.status_code == 200
    assert summary.json()["usa_servicio_real"] is False
    assert cancelled.status_code == 200
    assert cancelled.json()["estado"] == "pendiente"
    assert events.status_code == 200
    assert len(events.json()) >= 2
