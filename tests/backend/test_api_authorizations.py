from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_autorizacion_detalle_historial_y_categorias():
    detail = client.get("/api/authorizations/AUT-DEMO-001")
    history = client.get("/api/authorizations/history")
    categories = client.get("/api/authorizations/sensitive-data-categories")

    assert detail.status_code == 200
    assert detail.json()["id"] == "AUT-DEMO-001"
    assert history.status_code == 200
    assert categories.status_code == 200


def test_aprobar_rechazar_revocar_requieren_factor_demo():
    bad = client.post("/api/authorizations/AUT-DEMO-001/approve", json={"otp": "000000"})
    approved = client.post("/api/authorizations/AUT-DEMO-001/approve", json={"otp": "123456"})
    rejected = client.post("/api/authorizations/AUT-DEMO-002/reject", json={"otp": "123456"})
    revoked = client.post("/api/authorizations/AUT-DEMO-003/revoke", json={"otp": "123456"})

    assert bad.status_code == 401
    assert approved.status_code == 200
    assert approved.json()["estado"] == "aprobada"
    assert rejected.status_code == 200
    assert rejected.json()["estado"] == "rechazada"
    assert revoked.status_code == 200
    assert revoked.json()["estado"] == "revocada"
