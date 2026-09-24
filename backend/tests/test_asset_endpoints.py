"""
W3-Day2 tests for the asset inventory API endpoints (POST/GET /assets).
"""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_create_asset_returns_201_with_stored_values():
    response = client.post(
        "/assets",
        json={
            "name": "Customer Database",
            "value": 85000.0,
            "criticality": "critical",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Customer Database"
    assert data["value"] == 85000.0
    assert data["criticality"] == "critical"
    assert "id" in data
    assert "created_at" in data


def test_create_asset_rejects_invalid_criticality():
    response = client.post(
        "/assets",
        json={
            "name": "Test Server",
            "value": 1000.0,
            "criticality": "extremely-critical",
        },
    )

    assert response.status_code == 422


def test_create_asset_rejects_negative_value():
    response = client.post(
        "/assets",
        json={
            "name": "Test Server",
            "value": -500.0,
            "criticality": "low",
        },
    )

    assert response.status_code == 422


def test_list_assets_returns_created_assets():
    client.post(
        "/assets",
        json={
            "name": "Payment Gateway",
            "value": 120000.0,
            "criticality": "critical",
        },
    )

    response = client.get("/assets")

    assert response.status_code == 200
    data = response.json()
    assert "assets" in data
    names = [asset["name"] for asset in data["assets"]]
    assert "Payment Gateway" in names