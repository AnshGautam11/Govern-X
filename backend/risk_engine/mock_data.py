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
