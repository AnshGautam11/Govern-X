from fastapi.testclient import TestClient

from app import app
from risk_engine.financial_risk import (
    calculate_ale,
    calculate_risk_for_finding,
    calculate_sle,
)


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


def test_calculate_sle_uses_asset_value_and_exposure_factor():
    sle = calculate_sle(1_000_000, 0.25)

    assert sle == 250_000.0


def test_calculate_ale_uses_sle_and_annual_rate_of_occurrence():
    ale = calculate_ale(250_000, 1.5)

    assert ale == 375_000.0


def test_calculate_risk_boundary_classification():
    low = calculate_risk_for_finding(
        check_id="cloudtrail_enabled",
        asset_value=1_000_000,
        exposure_factor=0.14,
        annual_rate_of_occurrence=1.0,
    )
    medium = calculate_risk_for_finding(
        check_id="cloudtrail_enabled",
        asset_value=1_000_000,
        exposure_factor=0.15,
        annual_rate_of_occurrence=1.0,
    )
    high = calculate_risk_for_finding(
        check_id="cloudtrail_enabled",
        asset_value=1_000_000,
        exposure_factor=0.35,
        annual_rate_of_occurrence=1.0,
    )
    critical = calculate_risk_for_finding(
        check_id="cloudtrail_enabled",
        asset_value=1_000_000,
        exposure_factor=0.60,
        annual_rate_of_occurrence=1.0,
    )

    assert low["risk_level"] == "low"
    assert medium["risk_level"] == "medium"
    assert high["risk_level"] == "high"
    assert critical["risk_level"] == "critical"


def test_calculate_risk_for_finding_preserves_financial_values():
    result = calculate_risk_for_finding(
        check_id="s3_encryption_at_rest",
        asset_value=2_000_000,
        exposure_factor=0.25,
        annual_rate_of_occurrence=2.0,
    )

    assert result["asset_value"] == 2_000_000.0
    assert result["exposure_factor"] == 0.25
    assert result["likelihood"] == 2.0
    assert result["sle"] == 500_000.0
    assert result["ale"] == 1_000_000.0
    assert result["estimated_loss"] == 1_000_000.0
    assert result["currency"] == "INR"