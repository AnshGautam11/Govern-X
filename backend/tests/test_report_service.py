from datetime import datetime

from database.db import SessionLocal
from database.models import ScanResultDB
from database.persistence import (
    ensure_governance_questions,
    save_governance_responses,
)
from reports.report_service import (
    build_report_data,
    prioritize_remediation,
)


def test_prioritize_remediation_uses_severity_and_resource_count():

    findings = [
        {
            "check_id": "high_check",
            "status": "fail",
            "severity": "high",
            "resource_id": "r1",
            "csf_function": "Protect",
            "csf_subcategory": "PR.AA-05",
            "remediation": "Apply least privilege.",
        },
        {
            "check_id": "high_check",
            "status": "fail",
            "severity": "high",
            "resource_id": "r2",
            "csf_function": "Protect",
            "csf_subcategory": "PR.AA-05",
            "remediation": "Apply least privilege.",
        },
        {
            "check_id": "critical_check",
            "status": "fail",
            "severity": "critical",
            "resource_id": "r3",
            "csf_function": "Protect",
            "csf_subcategory": "PR.AA-03",
            "remediation": "Enforce MFA.",
        },
    ]

    result = prioritize_remediation(
        findings
    )

    assert result[0]["check_id"] == "high_check"
    assert result[0]["priority_score"] == 6

    assert result[1]["check_id"] == "critical_check"
    assert result[1]["priority_score"] == 4


def test_report_data_returns_no_data_without_scan():

    db = SessionLocal()

    try:
        db.query(
            ScanResultDB
        ).delete()

        db.commit()

        report = build_report_data(db)

        assert report["status"] == "no_data"

        assert (
            report["summary"]["overall_score"]
            is None
        )

        assert (
            report["summary"]["tier_name"]
            == "No Data"
        )

    finally:
        db.close()


def test_report_data_assembles_scan_and_governance():

    db = SessionLocal()

    try:
        ensure_governance_questions(db)

        save_governance_responses(
            {
                "risk_owner_assigned": True,
                "security_policy_reviewed": True,
                "incident_response_plan_exists": False,
                "third_party_risk_reviewed": True,
            },
            db=db,
        )

        timestamp = datetime.utcnow()

        db.add_all(
            [
                ScanResultDB(
                    check_id=(
                        "iam_policy_wildcard_admin"
                    ),
                    resource_id="demo-role-1",
                    status="fail",
                    severity="critical",
                    detail="Wildcard admin access.",
                    scanned_at=timestamp,
                ),
                ScanResultDB(
                    check_id="cloudtrail_enabled",
                    resource_id="demo-trail",
                    status="pass",
                    severity="high",
                    detail="CloudTrail enabled.",
                    scanned_at=timestamp,
                ),
            ]
        )

        db.commit()

        report = build_report_data(db)

        assert report["status"] == "ready"
        assert report["summary"]["total_checks"] == 2
        assert report["summary"]["failed"] == 1
        assert (
            report["governance"]["self_attested"]
            is True
        )
        assert report["remediation"]
        assert (
            report["roi"]["status"]
            == "sample_only"
        )

    finally:
        db.close()