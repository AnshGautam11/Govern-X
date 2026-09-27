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

def test_combined_report_mock_scenarios_are_complete():
    from risk_engine.mock_data import MOCK_COMBINED_REPORT_SCENARIOS

    assert set(MOCK_COMBINED_REPORT_SCENARIOS) == {
        "strong_governance",
        "partial_governance",
        "weak_governance",
    }

    for scenario in MOCK_COMBINED_REPORT_SCENARIOS.values():
        assert scenario["description"]
        assert scenario["sector"] in {"financial", "healthcare"}
        assert scenario["findings"]
        assert scenario["governance_answers"]

        for finding in scenario["findings"]:
            assert finding["check_id"]
            assert finding["resource_id"]
            assert finding["status"] in {"pass", "fail"}
            assert finding["severity"]


def test_combined_report_mock_scenarios_cover_different_compliance_states():
    from risk_engine.mock_data import MOCK_COMBINED_REPORT_SCENARIOS

    scenarios = MOCK_COMBINED_REPORT_SCENARIOS.values()

    statuses = {
        finding["status"]
        for scenario in scenarios
        for finding in scenario["findings"]
    }

    assert statuses == {"pass", "fail"}