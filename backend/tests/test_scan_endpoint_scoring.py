"""
Integration test — confirms /scan/aws returns scores alongside raw results.
"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app
from models.schemas import CheckResult, CheckStatus, Severity


def test_scan_aws_includes_scores():
    mock_results = [
        CheckResult(
            check_id="s3_public_access_block", resource_id="bucket-1",
            status=CheckStatus.PASS, severity=Severity.HIGH, detail="test"
        ),
        CheckResult(
            check_id="iam_user_mfa", resource_id="user-1",
            status=CheckStatus.FAIL, severity=Severity.CRITICAL, detail="test"
        ),
    ]

    client = TestClient(app)

    with patch("collectors.aws_collector.run_all_checks", return_value=mock_results), \
         patch("database.persistence.save_scan_results", return_value=None):
        response = client.post("/scan/aws")

    assert response.status_code == 200
    data = response.json()

    assert "scores" in data
    assert "overall" in data
    assert data["scores"]["Protect"]["score"] == 50.0
    assert data["scores"]["Protect"]["tier"] == "Tier 2"
    assert data["overall"]["score"] == 50.0


def test_scan_aws_skips_checks_without_mapping():
    """A check with no CSF mapping row should not crash scoring."""
    mock_results = [
        CheckResult(
            check_id="not_a_real_check", resource_id="x",
            status=CheckStatus.PASS, severity=Severity.LOW, detail="test"
        ),
    ]

    client = TestClient(app)

    with patch("collectors.aws_collector.run_all_checks", return_value=mock_results), \
         patch("database.persistence.save_scan_results", return_value=None):
        response = client.post("/scan/aws")

    assert response.status_code == 200
    data = response.json()
    assert data["overall"]["score"] is None
    assert data["overall"]["tier"] == "No Data"
