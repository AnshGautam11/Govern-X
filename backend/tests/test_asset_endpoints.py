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


def test_list_assets_when_inventory_is_empty():
    """A fresh inventory should return an empty list, not an error."""
    import database.db as db_module
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from database.persistence import get_all_assets

    test_engine = create_engine("sqlite:///:memory:")
    db_module.Base.metadata.create_all(bind=test_engine)
    TestSession = sessionmaker(bind=test_engine)
    db = TestSession()

    assets = get_all_assets(db=db)
    assert assets == []


def test_create_asset_missing_required_field():
    """Missing 'criticality' entirely should be a validation error, not a 500."""
    response = client.post(
        "/assets",
        json={
            "name": "Test Server",
            "value": 1000.0,
        },
    )
    assert response.status_code == 422


def test_create_asset_rejects_zero_value():
    """value must be > 0 per the schema — zero should be rejected, not silently accepted."""
    response = client.post(
        "/assets",
        json={
            "name": "Free Tier Instance",
            "value": 0,
            "criticality": "low",
        },
    )
    assert response.status_code == 422


def test_create_asset_accepts_large_value():
    """Large dollar values (e.g. a core banking system) should work fine, not overflow."""
    response = client.post(
        "/assets",
        json={
            "name": "Core Banking Platform",
            "value": 25_000_000.0,
            "criticality": "critical",
        },
    )
    assert response.status_code == 201
    assert response.json()["value"] == 25_000_000.0


def test_create_asset_rejects_extra_unexpected_fields():
    """model_config = extra='forbid' should reject payloads with unknown fields."""
    response = client.post(
        "/assets",
        json={
            "name": "Test Server",
            "value": 1000.0,
            "criticality": "low",
            "owner": "someone@example.com",
        },
    )
    assert response.status_code == 422


def test_list_assets_reflects_multiple_criticalities():
    client.post("/assets", json={"name": "Low Asset", "value": 100.0, "criticality": "low"})
    client.post("/assets", json={"name": "High Asset", "value": 5000.0, "criticality": "high"})

    response = client.get("/assets")
    data = response.json()

    criticalities = {a["criticality"] for a in data["assets"]}
    assert "low" in criticalities
    assert "high" in criticalities