"""
Mid-Project Review: Mapping Audit test.

Proves that altering a mock AWS configuration is detected by the
scanner and correctly downgrades the specific NIST CSF 2.0 category
score.
"""

from unittest.mock import MagicMock, patch
from collectors.aws_collector import check_s3_public_access_block
from mappings.csf_mappings import get_mapping
from compliance.scorer import score_function, get_tier
from models.schemas import MappedFinding


def _run_check_and_score(is_blocked: bool):
    mock_s3 = MagicMock()
    mock_s3.list_buckets.return_value = {"Buckets": [{"Name": "audit-bucket"}]}
    mock_s3.get_public_access_block.return_value = {
        "PublicAccessBlockConfiguration": {
            "BlockPublicAcls": is_blocked,
            "IgnorePublicAcls": is_blocked,
            "BlockPublicPolicy": is_blocked,
            "RestrictPublicBuckets": is_blocked,
        }
    }

    with patch("collectors.aws_collector.get_client", return_value=mock_s3):
        results = check_s3_public_access_block()

    mapping = get_mapping("s3_public_access_block")
    findings = [MappedFinding(result=r, mapping=mapping) for r in results]
    score = score_function(findings, "Protect")
    return score, get_tier(score)


def test_mapping_audit_config_change_downgrades_score():
    """Altering the mock AWS config must be detected and must downgrade the tier."""
    before_score, before_tier = _run_check_and_score(is_blocked=True)
    after_score, after_tier = _run_check_and_score(is_blocked=False)

    assert before_score == 100.0
    assert before_tier == "Tier 4"
    assert after_score == 0.0
    assert after_tier == "Tier 1"
    assert after_score < before_score
