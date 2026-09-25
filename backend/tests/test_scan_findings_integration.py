from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from database.db import Base, get_db
from database import models
from models.schemas import CheckResult, CheckStatus, Severity


def test_scan_persists_findings_and_exposes_nist_gap_from_database():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    test_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    scan_result = CheckResult(
        check_id="iam_user_mfa",
        resource_id="integration-user",
        status=CheckStatus.FAIL,
        severity=Severity.CRITICAL,
        detail="MFA is not enabled",
    )

    try:
        with patch("collectors.aws_collector.run_all_checks", return_value=[scan_result]):
            scan_response = client.post("/scan/aws")

        assert scan_response.status_code == 200
        assert scan_response.json()["findings"][0]["mapping"]["csf_subcategory"] == "PR.AA-03"

        findings_response = client.get("/findings")
        assert findings_response.status_code == 200
        finding = findings_response.json()["findings"][0]
        assert finding["check_id"] == "iam_user_mfa"
        assert finding["severity"] == "critical"
        assert finding["resource_id"] == "integration-user"
        assert finding["mapping"]["csf_function"] == "Protect"

        gaps_response = client.get("/gaps")
        assert gaps_response.status_code == 200
        gap = gaps_response.json()["gaps"][0]
        assert gap["finding_id"] == finding["id"]
        assert gap["nist_function"] == "Protect"
        assert gap["nist_subcategory"] == "PR.AA-03"
        assert gap["current_state"] == "FAIL"
        assert gap["financial_impact"] is None

        overview_response = client.get("/dashboard/overview")
        assert overview_response.status_code == 200
        overview = overview_response.json()
        assert overview["open_findings"] == 1
        assert overview["critical_findings"] == 1
        assert overview["overall_maturity"] == 0.0
        assert overview["financial_risk"] is None
        assert overview["last_scan"] is not None

        risk_response = client.get("/risk/summary")
        assert risk_response.status_code == 200
        risk = risk_response.json()
        assert risk["status"] == "unavailable"
        assert risk["open_findings"] == 1
        assert risk["expected_loss"] is None
        assert risk["p95"] is None
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def test_risk_summary_reports_zero_loss_for_latest_all_pass_scan():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    test_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        from database.persistence import save_scan_results

        with test_session() as session:
            save_scan_results(
                [CheckResult(
                    check_id="s3_encryption_at_rest",
                    resource_id="bucket-pass",
                    status=CheckStatus.PASS,
                    severity=Severity.HIGH,
                    detail="Encrypted",
                )],
                db=session,
            )
        response = client.get("/risk/summary")
        assert response.status_code == 200
        assert response.json()["status"] == "calculated"
        assert response.json()["expected_loss"] == 0.0
        assert response.json()["p99"] == 0.0
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()
