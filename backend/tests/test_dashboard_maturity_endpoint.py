from unittest.mock import patch

from fastapi.testclient import TestClient

from app import app
from models.schemas import CheckResult, CheckStatus, Severity


client = TestClient(app)


def test_dashboard_maturity_returns_structured_overview():
    mock_results = [
        CheckResult(
            check_id="s3_public_access_block",
            resource_id="bucket-1",
            status=CheckStatus.PASS,
            severity=Severity.HIGH,
            detail="Public access is blocked",
        ),
        CheckResult(
            check_id="iam_user_mfa",
            resource_id="user-1",
            status=CheckStatus.FAIL,
            severity=Severity.CRITICAL,
            detail="MFA is disabled",
        ),
        CheckResult(
            check_id="cloudtrail_enabled",
            resource_id="trail-1",
            status=CheckStatus.PASS,
            severity=Severity.HIGH,
            detail="CloudTrail is enabled",
        ),
    ]

    with patch("collectors.aws_collector.run_all_checks", return_value=mock_results), \
         patch("database.persistence.save_scan_results", return_value=None), \
         patch("database.persistence.get_scan_history", return_value=[]):
        response = client.get("/dashboard/maturity")

    assert response.status_code == 200
    data = response.json()

    assert "overall" in data
    assert "pillars" in data
    assert data["overall"]["percentage"] is not None
    assert data["overall"]["tier"] in {1, 2, 3, 4}
    assert data["overall"]["tier_name"]

    assert len(data["pillars"]) == 6
    pillar_functions = {pillar["function"] for pillar in data["pillars"]}
    assert {"Govern", "Identify", "Protect", "Detect", "Respond", "Recover"} == pillar_functions

    for pillar in data["pillars"]:
        assert pillar["percentage"] is not None or pillar["tier"] is None
        assert pillar["tier"] in {1, 2, 3, 4, None}


def test_dashboard_maturity_uses_history_trend_when_available():
    mock_results = [
        CheckResult(
            check_id="s3_public_access_block",
            resource_id="bucket-1",
            status=CheckStatus.PASS,
            severity=Severity.HIGH,
            detail="Public access is blocked",
        ),
        CheckResult(
            check_id="iam_user_mfa",
            resource_id="user-1",
            status=CheckStatus.FAIL,
            severity=Severity.CRITICAL,
            detail="MFA is disabled",
        ),
    ]

    with patch("collectors.aws_collector.run_all_checks", return_value=mock_results), \
         patch("database.persistence.save_scan_results", return_value=None), \
         patch("database.persistence.get_scan_history", return_value=[]):
        response = client.get("/dashboard/maturity")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["overall"]["trend"], (int, float))
