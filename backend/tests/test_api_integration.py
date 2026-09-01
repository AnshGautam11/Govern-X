from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_endpoint_returns_service_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "GovernX"


def test_cors_allows_vite_frontend_origin():
    response = client.get("/health", headers={"Origin": "http://localhost:5173"})

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
