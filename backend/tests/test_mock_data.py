"""
W3-Day1 tests for sample asset and governance mock data.
"""

from risk_engine.mock_data import MOCK_ASSET_DATA, MOCK_GOVERNANCE_ANSWERS


def test_mock_asset_data_contains_expected_scenarios():
    assert "financial" in MOCK_ASSET_DATA
    assert "healthcare" in MOCK_ASSET_DATA

    financial = MOCK_ASSET_DATA["financial"]

    assert financial["asset_value_range"] == (50000.0, 100000.0)
    assert financial["exposure_factor_range"] == (0.3, 0.7)
    assert financial["annual_rate_of_occurrence"] == 2.0


def test_mock_governance_answers_contain_expected_questions():
    financial = MOCK_GOVERNANCE_ANSWERS["financial"]

    assert financial["risk_owner_assigned"] is True
    assert financial["security_policy_reviewed"] is True
    assert financial["incident_response_plan_exists"] is True
    assert financial["third_party_risk_reviewed"] is False