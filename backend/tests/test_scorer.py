"""
Tests for compliance/scorer.py — Week 2 maturity scoring.
"""
from compliance.scorer import score_function, get_tier, score_all_functions, score_overall, gap_analysis
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

def test_score_all_functions_multi_function_realistic():
    """
    Day 3 review: a realistic multi-function scan should score each
    function independently without cross-contamination.
    """
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
        _finding("b", "Protect", CheckStatus.PASS),
        _finding("c", "Protect", CheckStatus.FAIL),
        _finding("d", "Detect", CheckStatus.PASS),
        _finding("e", "Identify", CheckStatus.FAIL),
        _finding("f", "Identify", CheckStatus.FAIL),
    ]
    result = score_all_functions(findings)

    assert result["Protect"]["score"] == 66.7
    assert result["Detect"]["score"] == 100.0
    assert result["Identify"]["score"] == 0.0
    assert "Govern" not in result
    assert "Respond" not in result
    assert "Recover" not in result


def test_gap_analysis_returns_only_failing_checks_for_function():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
        _finding("b", "Protect", CheckStatus.FAIL),
        _finding("c", "Detect", CheckStatus.FAIL),
    ]
    gaps = gap_analysis(findings, "Protect")
    assert len(gaps) == 1
    assert gaps[0]["check_id"] == "b"


def test_gap_analysis_groups_by_check_id():
    findings = [
        _finding("wildcard_admin", "Protect", CheckStatus.FAIL),
    ]
    findings[0].result.resource_id = "policy-1"
    second = _finding("wildcard_admin", "Protect", CheckStatus.FAIL)
    second.result.resource_id = "policy-2"
    findings.append(second)

    gaps = gap_analysis(findings, "Protect")
    assert len(gaps) == 1
    assert gaps[0]["check_id"] == "wildcard_admin"
    assert gaps[0]["failing_resource_count"] == 2
    assert set(gaps[0]["resource_ids"]) == {"policy-1", "policy-2"}


def test_gap_analysis_sorted_worst_first():
    findings = [
        _finding("check_a", "Protect", CheckStatus.FAIL),
        _finding("check_b", "Protect", CheckStatus.FAIL),
    ]
    findings[1] = _finding("check_b", "Protect", CheckStatus.FAIL)
    extra = _finding("check_b", "Protect", CheckStatus.FAIL)
    findings.append(extra)

    gaps = gap_analysis(findings, "Protect")
    assert gaps[0]["check_id"] == "check_b"
    assert gaps[0]["failing_resource_count"] == 2


def test_gap_analysis_empty_when_no_failures():
    findings = [
        _finding("a", "Protect", CheckStatus.PASS),
    ]
    assert gap_analysis(findings, "Protect") == []
def test_gap_analysis_ignores_pass_and_error_results():
    findings = [
        _finding("passed_check", "Protect", CheckStatus.PASS),
        _finding("failed_check", "Protect", CheckStatus.FAIL),
        _finding("error_check", "Protect", CheckStatus.ERROR),
    ]

    gaps = gap_analysis(findings, "Protect")

    assert len(gaps) == 1
    assert gaps[0]["check_id"] == "failed_check"

