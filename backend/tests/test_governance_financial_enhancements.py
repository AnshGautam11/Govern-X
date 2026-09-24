from fastapi.testclient import TestClient

from app import app
from risk_engine.financial_risk import (
    calculate_ale,
    calculate_sle,
    calculate_risk_for_finding,
    summarize_financial_risk,
)
from risk_engine.governance import build_governance_summary, mock_governance_profile

client = TestClient(app)


def test_governance_summary_calculates_policy_and_supply_chain_metrics():
    profile = mock_governance_profile()
    summary = build_governance_summary(profile)

    assert isinstance(summary["policy_coverage"], (int, float))
    assert isinstance(summary["supply_chain_risk"], (int, float))
    assert isinstance(summary["governance_maturity"], (int, float))
    assert 0 <= summary["policy_coverage"] <= 100
    assert 0 <= summary["supply_chain_risk"] <= 100


def test_financial_model_supports_sle_and_ale_calculation():
    sle = calculate_sle(asset_value=5000000.0, exposure_factor=0.35)
    ale = calculate_ale(sle=sle, aro=2.0)

    assert sle == 1750000.0
    assert ale == 3500000.0


def test_finding_to_financial_mapping_uses_asset_value_and_risk_factor():
    estimate = calculate_risk_for_finding(
        check_id="iam_policy_wildcard_admin",
        asset_value=4000000.0,
        exposure_factor=0.4,
        annual_rate_of_occurrence=1.5,
    )

    assert estimate["asset_name"] == "Production API"
    assert estimate["estimated_loss"] > 0
    assert estimate["risk_level"] in {"low", "medium", "high", "critical"}


def test_financial_summary_endpoint_returns_summary_payload():
    response = client.get("/risk/financial-summary")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_asset_value"] >= 0
    assert payload["estimated_financial_exposure"] >= 0
    assert payload["high_risk_assets"] >= 0


def test_governance_profile_endpoint_returns_default_org_data():
    response = client.get("/governance/profile")

    assert response.status_code == 200
    payload = response.json()
    assert payload["organization_name"] == "Demo Enterprise"
    assert payload["industry"] == "Technology"


def test_risk_assets_endpoint_accepts_a_new_asset():
    response = client.post(
        "/risk/assets",
        json={
            "asset_id": "asset-bridge",
            "asset_name": "Bridge Service",
            "asset_type": "Application",
            "cloud_provider": "AWS",
            "business_function": "Payments",
            "data_sensitivity": "Highly Sensitive",
            "criticality": "critical",
            "asset_value": 2500000.0,
            "revenue_dependency": 0.8,
            "customer_dependency": 0.7,
            "recovery_cost": 300000.0,
            "regulatory_exposure": 0.6,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["asset_name"] == "Bridge Service"
    assert body["criticality"] == "critical"


def test_summarized_risk_snapshot_is_derived_from_assets_and_findings():
    snapshot = summarize_financial_risk()

    assert snapshot["total_asset_value"] >= 0
    assert snapshot["estimated_financial_exposure"] >= 0
    assert len(snapshot["assets"]) >= 1
