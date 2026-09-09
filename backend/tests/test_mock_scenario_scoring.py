
from compliance.scorer import score_all_functions, score_overall
from mappings.csf_mappings import get_mapping
from models.schemas import CheckResult, MappedFinding


def build_mapped_findings(findings):
    """Convert CheckResults into MappedFinding objects expected by the scorer."""
    mapped_findings = []

    for finding in findings:
        mapping = get_mapping(finding.check_id)

        if mapping:
            mapped_findings.append(
                MappedFinding(
                    result=finding,
                    mapping=mapping,
                )
            )

    return mapped_findings


def test_financial_mock_scenario_scoring():
    """Test scoring with a mixed pass/fail mock scenario."""
    findings = [
        CheckResult(
            check_id="cloudtrail_enabled",
            resource_id="mock-trail",
            status="pass",
            severity="high",
            detail="CloudTrail logging is enabled.",
        ),
        CheckResult(
            check_id="vpc_flow_logs_enabled",
            resource_id="mock-vpc",
            status="fail",
            severity="high",
            detail="VPC flow logs are disabled.",
        ),
    ]

    mapped_findings = build_mapped_findings(findings)

    function_scores = score_all_functions(mapped_findings)
    overall_score = score_overall(mapped_findings)

    assert mapped_findings
    assert function_scores
    assert overall_score is not None


def test_all_pass_mock_scenario_scores_high():
    """Test scoring when all mock checks pass."""
    findings = [
        CheckResult(
            check_id="cloudtrail_enabled",
            resource_id="mock-trail",
            status="pass",
            severity="high",
            detail="CloudTrail logging is enabled.",
        ),
        CheckResult(
            check_id="vpc_flow_logs_enabled",
            resource_id="mock-vpc",
            status="pass",
            severity="high",
            detail="VPC flow logs are enabled.",
        ),
    ]

    mapped_findings = build_mapped_findings(findings)

    function_scores = score_all_functions(mapped_findings)
    overall_score = score_overall(mapped_findings)

    assert mapped_findings
    assert function_scores
    assert overall_score is not None

    assert overall_score["score"] == 100.0
    assert overall_score["tier"] == "Tier 4"


def test_all_fail_mock_scenario_scores_low():
    """Test scoring when all mock checks fail."""
    findings = [
        CheckResult(
            check_id="cloudtrail_enabled",
            resource_id="mock-trail",
            status="fail",
            severity="high",
            detail="CloudTrail logging is disabled.",
        ),
        CheckResult(
            check_id="vpc_flow_logs_enabled",
            resource_id="mock-vpc",
            status="fail",
            severity="high",
            detail="VPC flow logs are disabled.",
        ),
    ]

    mapped_findings = build_mapped_findings(findings)

    function_scores = score_all_functions(mapped_findings)
    overall_score = score_overall(mapped_findings)

    assert mapped_findings
    assert function_scores
    assert overall_score is not None

    assert overall_score["score"] == 0.0
    assert overall_score["tier"] == "Tier 1"
