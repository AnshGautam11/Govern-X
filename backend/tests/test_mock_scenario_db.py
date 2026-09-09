"""
W2-Day2 tests for DB-backed mock scenario lookup and scoring.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from compliance.scorer import score_all_functions, score_overall
from database.db import Base
from database.persistence import get_mock_scenario, save_mock_scenario
from mappings.csf_mappings import get_mapping
from models.schemas import (
    CheckResult,
    CheckStatus,
    MappedFinding,
    Severity,
)


def _make_test_session():
    """Create an isolated in-memory database for this test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)
    return TestSession()


def test_mock_scenario_is_saved_and_loaded_from_db():
    db = _make_test_session()

    results = [
        CheckResult(
            check_id="s3_public_access_block",
            resource_id="bucket-1",
            status=CheckStatus.PASS,
            severity=Severity.HIGH,
            detail="Public access block enabled",
        ),
        CheckResult(
            check_id="iam_user_mfa",
            resource_id="user-1",
            status=CheckStatus.FAIL,
            severity=Severity.CRITICAL,
            detail="MFA is not enabled",
        ),
    ]

    save_mock_scenario("financial", results, db=db)

    loaded = get_mock_scenario("financial", db=db)

    assert len(loaded) == 2
    assert loaded[0].check_id == "s3_public_access_block"
    assert loaded[0].status == CheckStatus.PASS
    assert loaded[1].check_id == "iam_user_mfa"
    assert loaded[1].status == CheckStatus.FAIL


def test_mock_scenario_lookup_returns_empty_for_unknown_scenario():
    db = _make_test_session()

    loaded = get_mock_scenario("does-not-exist", db=db)

    assert loaded == []


def test_mock_scenario_findings_feed_existing_scorer():
    db = _make_test_session()

    results = [
        CheckResult(
            check_id="s3_public_access_block",
            resource_id="bucket-1",
            status=CheckStatus.PASS,
            severity=Severity.HIGH,
            detail="Public access block enabled",
        ),
        CheckResult(
            check_id="iam_user_mfa",
            resource_id="user-1",
            status=CheckStatus.FAIL,
            severity=Severity.CRITICAL,
            detail="MFA is not enabled",
        ),
    ]

    save_mock_scenario("financial", results, db=db)

    loaded = get_mock_scenario("financial", db=db)

    findings = []

    for result in loaded:
        mapping = get_mapping(result.check_id)
        if mapping is not None:
            findings.append(
                MappedFinding(
                    result=result,
                    mapping=mapping,
                )
            )

    scores = score_all_functions(findings)
    overall = score_overall(findings)

    assert scores["Protect"]["score"] == 50.0
    assert scores["Protect"]["tier"] == "Tier 2"
    assert overall["score"] == 50.0
    assert overall["tier"] == "Tier 2"