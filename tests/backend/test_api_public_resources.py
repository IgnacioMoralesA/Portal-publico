from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_recursos_publicos_ayuda_instituciones_e_integraciones():
    paths = [
        "/api/public/news",
        "/api/public/service-cards",
        "/api/help/categories",
        "/api/help/articles",
        "/api/institutions",
        "/api/institutions/INS-DEMO-001",
        "/api/integrations/status",
        "/api/integrations/events",
    ]

    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, path


def test_integraciones_declaran_modo_local_mock():
    response = client.get("/api/integrations/status")

    assert response.status_code == 200
    assert response.json()[0]["external_service"] is False
