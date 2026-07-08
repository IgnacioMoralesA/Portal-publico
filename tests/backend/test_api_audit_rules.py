from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_auditoria_evidencia_reglas_y_pantallas_responden():
    paths = [
        "/api/audit/events",
        "/api/evidence/tests",
        "/api/product/checklist",
        "/api/business-rules",
        "/api/validation-rules",
        "/api/screens",
        "/api/deployment-targets",
    ]

    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, path
        assert isinstance(response.json(), list)


def test_deploy_ec2_sigue_pendiente_y_sin_red_externa():
    response = client.get("/api/deployment-targets")

    assert response.status_code == 200
    payload = response.json()[0]
    assert payload["target_status"] == "pendiente"
    assert payload["external_network_enabled"] is False
