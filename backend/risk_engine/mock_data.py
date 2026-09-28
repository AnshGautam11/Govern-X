"""
Sample mock data for Week 3 risk and governance demos.

IMPORTANT: All values in this module are synthetic/demo inputs.
They are not real organizational figures.
"""

MOCK_ASSET_DATA = {
    "financial": {
        "asset_value_range": (50000.0, 100000.0),
        "exposure_factor_range": (0.3, 0.7),
        "annual_rate_of_occurrence": 2.0,
    },
    "healthcare": {
        "asset_value_range": (75000.0, 150000.0),
        "exposure_factor_range": (0.4, 0.8),
        "annual_rate_of_occurrence": 1.5,
    },
}

MOCK_GOVERNANCE_ANSWERS = {
    "financial": {
        "risk_owner_assigned": True,
        "security_policy_reviewed": True,
        "incident_response_plan_exists": True,
        "third_party_risk_reviewed": False,
    },
    "healthcare": {
        "risk_owner_assigned": True,
        "security_policy_reviewed": True,
        "incident_response_plan_exists": False,
        "third_party_risk_reviewed": True,
    },
}
MOCK_COMBINED_REPORT_SCENARIOS = {
    "strong_governance": {
        "description": "Mostly compliant organization with low governance gaps.",
        "sector": "financial",
        "findings": [
            {
                "check_id": "cloudtrail_enabled",
                "resource_id": "mock-trail",
                "status": "pass",
                "severity": "high",
                "detail": "CloudTrail logging is enabled.",
            },
            {
                "check_id": "vpc_flow_logs_enabled",
                "resource_id": "mock-vpc",
                "status": "pass",
                "severity": "high",
                "detail": "VPC flow logs are enabled.",
            },
        ],
        "governance_answers": MOCK_GOVERNANCE_ANSWERS["financial"],
    },
    "partial_governance": {
        "description": "Mixed compliance with identifiable governance and infrastructure gaps.",
        "sector": "financial",
        "findings": [
            {
                "check_id": "cloudtrail_enabled",
                "resource_id": "mock-trail",
                "status": "pass",
                "severity": "high",
                "detail": "CloudTrail logging is enabled.",
            },
            {
                "check_id": "vpc_flow_logs_enabled",
                "resource_id": "mock-vpc-1",
                "status": "fail",
                "severity": "high",
                "detail": "VPC flow logs are disabled.",
            },
            {
                "check_id": "vpc_flow_logs_enabled",
                "resource_id": "mock-vpc-2",
                "status": "fail",
                "severity": "high",
                "detail": "VPC flow logs are disabled.",
            },
        ],
        "governance_answers": MOCK_GOVERNANCE_ANSWERS["financial"],
    },
    "weak_governance": {
        "description": "Low compliance scenario with multiple failed controls.",
        "sector": "healthcare",
        "findings": [
            {
                "check_id": "cloudtrail_enabled",
                "resource_id": "mock-trail",
                "status": "fail",
                "severity": "high",
                "detail": "CloudTrail logging is disabled.",
            },
            {
                "check_id": "vpc_flow_logs_enabled",
                "resource_id": "mock-vpc",
                "status": "fail",
                "severity": "high",
                "detail": "VPC flow logs are disabled.",
            },
        ],
        "governance_answers": MOCK_GOVERNANCE_ANSWERS["healthcare"],
    },
}
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

# Week 4 demo dataset.
# All values are synthetic and intended only for local demonstrations.
DEMO_REPORT_DATASET = {
    "name": "executive_report_demo",
    "description": (
        "Synthetic multi-function report scenario "
        "for local demos."
    ),
    "findings": [
        {
            "check_id": "iam_policy_wildcard_admin",
            "resource_id": "demo-iam-role",
            "status": "fail",
            "severity": "critical",
            "detail": (
                "Wildcard administrative access "
                "is present."
            ),
        },
        {
            "check_id": "security_group_open_ingress",
            "resource_id": "demo-sg-web",
            "status": "fail",
            "severity": "high",
            "detail": (
                "A security group permits "
                "unrestricted ingress."
            ),
        },
        {
            "check_id": "cloudtrail_enabled",
            "resource_id": "demo-trail",
            "status": "pass",
            "severity": "high",
            "detail": (
                "CloudTrail logging is enabled."
            ),
        },
        {
            "check_id": "vpc_flow_logs_enabled",
            "resource_id": "demo-vpc",
            "status": "fail",
            "severity": "medium",
            "detail": (
                "VPC Flow Logs are disabled."
            ),
        },
        {
            "check_id": "s3_encryption_at_rest",
            "resource_id": "demo-bucket",
            "status": "pass",
            "severity": "high",
            "detail": (
                "S3 encryption at rest is enabled."
            ),
        },
    ],
    "governance_answers": MOCK_GOVERNANCE_ANSWERS[
        "financial"
    ],
}