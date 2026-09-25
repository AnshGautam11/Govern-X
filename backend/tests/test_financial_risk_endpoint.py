from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_financial_risk_endpoint_returns_monte_carlo_summary():
    response = client.post("/risk/assess", json={"sector": "financial"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["sector"] == "financial"
    assert payload["p10"] <= payload["p50"] <= payload["p90"] <= payload["p95"] <= payload["p99"]
    assert payload["p10"] <= payload["expected"] <= payload["p90"]
    assert payload["iterations"] == 10_000
    assert len(payload["distribution"]) == 12
    assert payload["data_quality"] == "assumed_sample_data"
    assert "not real organizational figures" in payload["disclaimer"]


def test_financial_risk_endpoint_rejects_unknown_sector():
    response = client.post("/risk/assess", json={"sector": "unknown"})

    assert response.status_code == 422