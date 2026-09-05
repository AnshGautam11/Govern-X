"""
Tests for compliance/scorer.py — Week 2 maturity scoring.
"""

from compliance.scorer import score_function, get_tier, score_all_functions, score_overall
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
