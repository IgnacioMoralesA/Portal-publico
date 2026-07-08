from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_notificacion_detalle_y_marcar_leida_mock():
    detail = client.get("/api/notifications/NOT-001")
    marked = client.post("/api/notifications/NOT-001/read")
    reread = client.get("/api/notifications/NOT-001")

    assert detail.status_code == 200
    assert marked.status_code == 200
    assert marked.json()["estado"] == "leida demo"
    assert reread.status_code == 200
    assert reread.json()["estado"] == "leida demo"


def test_catalogos_y_eventos_de_notificaciones_responden():
    for path in [
        "/api/notifications/categories",
        "/api/notifications/priorities",
        "/api/notifications/read-events",
        "/api/notifications/delivery-attempts",
    ]:
        response = client.get(path)
        assert response.status_code == 200, path
        assert isinstance(response.json(), list)
