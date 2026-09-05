"""
W2-Day1 test for scan result persistence — verifies CheckResult objects
get written to the scan_results table with a timestamp.
"""

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.db import Base
from database.models import ScanResultDB
from database.persistence import save_scan_results
from models.schemas import CheckResult, CheckStatus, Severity


def _make_test_session():
    """Isolated in-memory SQLite DB, separate from the real governx.db file."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)
    return TestSession()


def test_save_scan_results_persists_one_row():
    db = _make_test_session()

    results = [
        CheckResult(
            check_id="s3_public_access_block",
            resource_id="my-bucket",
            status=CheckStatus.PASS,
            severity=Severity.HIGH,
            detail="Public access block fully enabled",
        )
    ]

    save_scan_results(results, db=db)

    rows = db.query(ScanResultDB).all()
    assert len(rows) == 1
    assert rows[0].check_id == "s3_public_access_block"
    assert rows[0].resource_id == "my-bucket"
    assert rows[0].status == "pass"
    assert isinstance(rows[0].scanned_at, datetime)


def test_save_scan_results_persists_multiple_rows():
    db = _make_test_session()

    results = [
        CheckResult(
            check_id="iam_root_mfa",
            resource_id="root-account",
            status=CheckStatus.FAIL,
            severity=Severity.CRITICAL,
            detail="Root account MFA is NOT enabled",
        ),
        CheckResult(
            check_id="iam_password_policy",
            resource_id="account-password-policy",
            status=CheckStatus.PASS,
            severity=Severity.MEDIUM,
            detail="Password policy meets minimum requirements",
        ),
    ]

    save_scan_results(results, db=db)

    rows = db.query(ScanResultDB).order_by(ScanResultDB.id).all()
    assert len(rows) == 2
    assert rows[0].status == "fail"
    assert rows[1].status == "pass"
    assert rows[0].scanned_at is not None