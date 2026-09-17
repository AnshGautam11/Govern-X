"""
W2-Day5 tests for GET /scan/compare.

Compares the two most recent scans in the scan_results table and reports
which checks newly passed, newly failed, stayed the same, or appeared /
disappeared entirely between scans.
"""

import time

from fastapi.testclient import TestClient

from app import app
from database.persistence import save_scan_results
from models.schemas import CheckResult, CheckStatus, Severity

client = TestClient(app)


def _result(check_id, resource_id, status):
    return CheckResult(
        check_id=check_id,
        resource_id=resource_id,
        status=status,
        severity=Severity.MEDIUM,
        detail=f"{check_id} is {status.value}",
    )


def test_scan_compare_detects_newly_passing_and_failing():
    save_scan_results(
        [
            _result("iam_root_mfa", "root-account", CheckStatus.FAIL),
            _result("s3_encryption_at_rest", "bucket-a", CheckStatus.PASS),
        ]
    )

    time.sleep(0.01)

    save_scan_results(
        [
            _result("iam_root_mfa", "root-account", CheckStatus.PASS),
            _result("s3_encryption_at_rest", "bucket-a", CheckStatus.FAIL),
        ]
    )

    response = client.get("/scan/compare")
    assert response.status_code == 200

    data = response.json()
    assert "iam_root_mfa" in data["newly_passing"]
    assert "s3_encryption_at_rest" in data["newly_failing"]
    assert data["current_scanned_at"] is not None
    assert data["previous_scanned_at"] is not None


def test_scan_compare_detects_unchanged_and_new_checks():
    save_scan_results([_result("iam_password_policy", "account-password-policy", CheckStatus.PASS)])

    time.sleep(0.01)

    save_scan_results(
        [
            _result("iam_password_policy", "account-password-policy", CheckStatus.PASS),
            _result("ebs_encryption", "vol-123", CheckStatus.FAIL),
        ]
    )

    response = client.get("/scan/compare")
    data = response.json()

    assert "iam_password_policy" in data["unchanged"]
    assert "ebs_encryption" in data["new_checks"]


def test_scan_compare_with_only_one_scan_present():
    """If there's only ever been one scan, there's nothing to compare against."""
    import database.db as db_module
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    test_engine = create_engine("sqlite:///:memory:")
    db_module.Base.metadata.create_all(bind=test_engine)
    TestSession = sessionmaker(bind=test_engine)
    db = TestSession()

    save_scan_results(
        [_result("iam_root_mfa", "root-account", CheckStatus.FAIL)],
        db=db,
    )

    from database.persistence import get_latest_two_scan_timestamps, get_scan_by_timestamp

    timestamps = get_latest_two_scan_timestamps(db=db)
    assert len(timestamps) == 1

    rows = get_scan_by_timestamp(timestamps[0], db=db)
    assert len(rows) == 1
    assert rows[0].check_id == "iam_root_mfa"