"""
Tests for compliance/scorer.py — Week 2 maturity scoring.
"""

from compliance.scorer import (
    score_function,
    get_tier,
    score_all_functions,
    score_overall,
    score_governance_completion,
)
from models.schemas import MappedFinding, CheckResult, CSFMapping, CheckStatus, Severity


def _finding(check_id, function, status):
    return MappedFinding(
        result=CheckResult(
            check_id=check_id, resource_id="test", status=status,
            severity=Severity.MEDIUM, detail="test"
        ),
        mapping=CSFMapping(
            check_id=check_id, csf_function=function,
            csf_subcategory="TEST-01", justification="test"
        )
    )


def test_score_function_basic_pass_rate():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
        _finding("b", "Protect", CheckStatus.PASS),
        _finding("c", "Protect", CheckStatus.FAIL),
    ]
    assert score_function(findings, "Protect") == 66.7


def test_score_function_excludes_errors():
    findings = [
        _finding("a", "Detect", CheckStatus.ERROR),
    ]
    assert score_function(findings, "Detect") is None


def test_score_function_no_findings_returns_none():
    assert score_function([], "Govern") is None


def test_get_tier_boundaries():
    assert get_tier(0) == "Tier 1"
    assert get_tier(25) == "Tier 1"
    assert get_tier(26) == "Tier 2"
    assert get_tier(50) == "Tier 2"
    assert get_tier(51) == "Tier 3"
    assert get_tier(75) == "Tier 3"
    assert get_tier(76) == "Tier 4"
    assert get_tier(100) == "Tier 4"
    assert get_tier(None) == "No Data"


def test_score_all_functions_only_includes_present_functions():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
    ]
    result = score_all_functions(findings)
    assert "Protect" in result
    assert "Govern" not in result


def test_score_overall_ignores_functions_with_no_data():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
        _finding("b", "Protect", CheckStatus.PASS),
        _finding("c", "Detect", CheckStatus.ERROR),
    ]
    result = score_overall(findings)
    assert result["score"] == 100.0
    assert result["tier"] == "Tier 4"


def test_score_overall_no_findings():
    result = score_overall([])
    assert result["score"] is None
    assert result["tier"] == "No Data"

def test_score_function_zero_percent():
    findings = [
        _finding("a", "Protect", CheckStatus.FAIL),
        _finding("b", "Protect", CheckStatus.FAIL),
    ]
    assert score_function(findings, "Protect") == 0.0
    assert get_tier(0.0) == "Tier 1"


def test_score_function_hundred_percent():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
        _finding("b", "Protect", CheckStatus.PASS),
    ]
    assert score_function(findings, "Protect") == 100.0
    assert get_tier(100.0) == "Tier 4"
def test_score_overall_averages_function_scores():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
        _finding("b", "Protect", CheckStatus.PASS),
        _finding("c", "Detect", CheckStatus.PASS),
        _finding("d", "Detect", CheckStatus.FAIL),
    ]
    result = score_overall(findings)
    assert result["score"] == 75.0
    assert result["tier"] == "Tier 3"
def test_score_function_ignores_errors_with_pass_fail():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
        _finding("b", "Protect", CheckStatus.FAIL),
        _finding("c", "Protect", CheckStatus.ERROR),
    ]
    assert score_function(findings, "Protect") == 50.0
    assert get_tier(50.0) == "Tier 2"

def test_governance_completion_score():
    answers = {
        "risk_owner_assigned": True,
        "security_policy_reviewed": True,
        "incident_response_plan_exists": False,
        "third_party_risk_reviewed": True,
    }

    assert score_governance_completion(answers) == 75.0


def test_governance_completion_score_all_complete():
    answers = {
        "risk_owner_assigned": True,
        "security_policy_reviewed": True,
        "incident_response_plan_exists": True,
        "third_party_risk_reviewed": True,
    }

    assert score_governance_completion(answers) == 100.0


def test_governance_completion_score_none_complete():
    answers = {
        "risk_owner_assigned": False,
        "security_policy_reviewed": False,
        "incident_response_plan_exists": False,
        "third_party_risk_reviewed": False,
    }

    assert score_governance_completion(answers) == 0.0


def test_governance_score_updates_govern_function():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
        _finding("b", "Protect", CheckStatus.PASS),
    ]

    governance_score = 75.0

    result = score_all_functions(
        findings,
        governance_score=governance_score,
    )

    assert result["Govern"]["score"] == 75.0
    assert result["Govern"]["tier"] == "Tier 3"


def test_governance_score_is_included_in_overall():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
        _finding("b", "Protect", CheckStatus.PASS),
    ]

    result = score_overall(
        findings,
        governance_score=50.0,
    )

    assert result["score"] == 75.0
    assert result["tier"] == "Tier 3"