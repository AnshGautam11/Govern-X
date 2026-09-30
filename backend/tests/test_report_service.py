from datetime import datetime

from database.db import SessionLocal
from database.models import ScanResultDB
from database.persistence import (
    ensure_governance_questions,
    save_governance_responses,
)
from reports.report_service import (
    SENSITIVITY_ASSUMPTIONS,
    _calculate_combined_sensitivity,
    _calculate_cost_sensitivity,
    _calculate_roi_sensitivity,
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

    result = prioritize_remediation(findings)

    assert result[0]["check_id"] == "high_check"
    assert result[0]["priority_score"] == 6

    assert result[1]["check_id"] == "critical_check"
    assert result[1]["priority_score"] == 4


def test_report_data_returns_no_data_without_scan():

    db = SessionLocal()

    try:
        db.query(ScanResultDB).delete()
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
                    check_id="iam_policy_wildcard_admin",
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


def test_report_data_filters_unknown_check_ids():

    db = SessionLocal()

    try:
        db.query(ScanResultDB).delete()
        db.commit()

        timestamp = datetime.utcnow()

        db.add_all(
            [
                ScanResultDB(
                    check_id="cloudtrail_enabled",
                    resource_id="demo-trail",
                    status="pass",
                    severity="high",
                    detail="CloudTrail enabled.",
                    scanned_at=timestamp,
                ),
                ScanResultDB(
                    check_id="unknown_test_check",
                    resource_id="unknown-resource",
                    status="fail",
                    severity="critical",
                    detail="Unknown check.",
                    scanned_at=timestamp,
                ),
            ]
        )

        db.commit()

        report = build_report_data(db)

        assert report["status"] == "ready"
        assert report["summary"]["total_checks"] == 2
        assert len(report["findings"]) == 1

        assert (
            report["findings"][0]["check_id"]
            == "cloudtrail_enabled"
        )

    finally:
        db.close()


def test_report_data_builds_pillars_for_all_csf_functions():

    db = SessionLocal()

    try:
        db.query(ScanResultDB).delete()
        db.commit()

        timestamp = datetime.utcnow()

        db.add(
            ScanResultDB(
                check_id="cloudtrail_enabled",
                resource_id="demo-trail",
                status="pass",
                severity="high",
                detail="CloudTrail enabled.",
                scanned_at=timestamp,
            )
        )

        db.commit()

        report = build_report_data(db)

        assert len(report["pillars"]) == 6

        functions = [
            pillar["function"]
            for pillar in report["pillars"]
        ]

        assert functions == [
            "Govern",
            "Identify",
            "Protect",
            "Detect",
            "Respond",
            "Recover",
        ]

    finally:
        db.close()


def test_report_data_builds_failed_gap_with_affected_resource():

    db = SessionLocal()

    try:
        db.query(ScanResultDB).delete()
        db.commit()

        timestamp = datetime.utcnow()

        db.add(
            ScanResultDB(
                check_id="iam_policy_wildcard_admin",
                resource_id="demo-role-1",
                status="fail",
                severity="critical",
                detail="Wildcard admin access.",
                scanned_at=timestamp,
            )
        )

        db.commit()

        report = build_report_data(db)

        assert report["status"] == "ready"
        assert len(report["gaps"]) == 1

        assert (
            report["gaps"][0]["check_id"]
            == "iam_policy_wildcard_admin"
        )

        assert (
            report["gaps"][0]["affected_resources"]
            == ["demo-role-1"]
        )

        assert report["remediation"]

    finally:
        db.close()


def test_roi_sensitivity_returns_expected_scenarios():

    parameters = {
        "asset_value_range": (
            1_000_000.0,
            2_000_000.0,
        ),
        "exposure_factor_range": (
            0.20,
            0.60,
        ),
        "annual_rate_of_occurrence": 0.5,
    }

    result = _calculate_roi_sensitivity(
        parameters=parameters,
        baseline_loss=500_000.0,
        remediation_cost=25_000.0,
        risk_reduction_percentages=[
            0.10,
            0.25,
            0.50,
        ],
    )

    assert len(result) == 3

    assert [
        item["risk_reduction_percent"]
        for item in result
    ] == [
        10.0,
        25.0,
        50.0,
    ]

    for item in result:
        assert (
            item["modeled_risk_reduction"]
            >= 0.0
        )

        assert item["roi_ratio"] >= 0.0


def test_roi_sensitivity_clamps_invalid_reduction_values():

    parameters = {
        "asset_value_range": (
            1_000_000.0,
            2_000_000.0,
        ),
        "exposure_factor_range": (
            0.20,
            0.60,
        ),
        "annual_rate_of_occurrence": 0.5,
    }

    result = _calculate_roi_sensitivity(
        parameters=parameters,
        baseline_loss=500_000.0,
        remediation_cost=25_000.0,
        risk_reduction_percentages=[
            -0.25,
            1.25,
        ],
    )

    assert [
        item["risk_reduction_percent"]
        for item in result
    ] == [
        0.0,
        100.0,
    ]


def test_cost_sensitivity_calculates_roi_for_alternative_costs():

    result = _calculate_cost_sensitivity(
        baseline_loss=500_000.0,
        remediated_loss=300_000.0,
        remediation_costs=[
            10_000.0,
            20_000.0,
            40_000.0,
        ],
    )

    assert len(result) == 3

    assert [
        item["assumed_remediation_cost"]
        for item in result
    ] == [
        10_000.0,
        20_000.0,
        40_000.0,
    ]

    assert [
        item["modeled_risk_reduction"]
        for item in result
    ] == [
        200_000.0,
        200_000.0,
        200_000.0,
    ]

    assert [
        item["roi_ratio"]
        for item in result
    ] == [
        20.0,
        10.0,
        5.0,
    ]


def test_cost_sensitivity_handles_zero_cost():

    result = _calculate_cost_sensitivity(
        baseline_loss=500_000.0,
        remediated_loss=300_000.0,
        remediation_costs=[
            0.0,
        ],
    )

    assert len(result) == 1

    assert (
        result[0]["assumed_remediation_cost"]
        == 0.0
    )

    assert (
        result[0]["modeled_risk_reduction"]
        == 200_000.0
    )

    assert result[0]["roi_ratio"] == 0.0


def test_combined_sensitivity_builds_what_if_scenarios():

    parameters = {
        "asset_value_range": (
            1_000_000.0,
            2_000_000.0,
        ),
        "exposure_factor_range": (
            0.20,
            0.60,
        ),
        "annual_rate_of_occurrence": 0.5,
    }

    result = _calculate_combined_sensitivity(
        parameters=parameters,
        baseline_loss=500_000.0,
        risk_reduction_percentages=[
            0.10,
            0.50,
        ],
        remediation_costs=[
            25_000.0,
            50_000.0,
        ],
    )

    assert len(result) == 4

    assert [
        item["risk_reduction_percent"]
        for item in result
    ] == [
        10.0,
        10.0,
        50.0,
        50.0,
    ]

    assert [
        item["assumed_remediation_cost"]
        for item in result
    ] == [
        25_000.0,
        50_000.0,
        25_000.0,
        50_000.0,
    ]

    for item in result:
        assert (
            item["modeled_risk_reduction"]
            >= 0.0
        )

        assert item["roi_ratio"] >= 0.0


def test_combined_sensitivity_roi_changes_with_cost():

    parameters = {
        "asset_value_range": (
            1_000_000.0,
            2_000_000.0,
        ),
        "exposure_factor_range": (
            0.20,
            0.60,
        ),
        "annual_rate_of_occurrence": 0.5,
    }

    result = _calculate_combined_sensitivity(
        parameters=parameters,
        baseline_loss=500_000.0,
        risk_reduction_percentages=[
            0.25,
        ],
        remediation_costs=[
            10_000.0,
            20_000.0,
        ],
    )

    assert len(result) == 2

    assert (
        result[0]["risk_reduction_percent"]
        == 25.0
    )

    assert (
        result[1]["risk_reduction_percent"]
        == 25.0
    )

    assert (
        result[0]["assumed_remediation_cost"]
        == 10_000.0
    )

    assert (
        result[1]["assumed_remediation_cost"]
        == 20_000.0
    )

    assert (
        result[0]["modeled_risk_reduction"]
        == result[1]["modeled_risk_reduction"]
    )

    assert (
        result[0]["roi_ratio"]
        >= result[1]["roi_ratio"]
    )


def test_sensitivity_assumptions_are_documented():

    assert (
        SENSITIVITY_ASSUMPTIONS[
            "risk_reduction_percentages"
        ]
        == [
            10.0,
            25.0,
            50.0,
        ]
    )

    assert (
        SENSITIVITY_ASSUMPTIONS[
            "remediation_costs"
        ]
        == [
            10000.0,
            25000.0,
            50000.0,
        ]
    )

    assert (
        "synthetic"
        in SENSITIVITY_ASSUMPTIONS[
            "description"
        ].lower()
    )

    assert (
        "not audited"
        in SENSITIVITY_ASSUMPTIONS[
            "description"
        ].lower()
    )
def test_roi_output_includes_interpretation():
    db = SessionLocal()

    try:
        ensure_governance_questions(db)

        save_governance_responses(
            {
                "risk_owner_assigned": True,
                "security_policy_reviewed": True,
                "incident_response_plan_exists": True,
                "third_party_risk_reviewed": True,
            },
            db=db,
        )

        timestamp = datetime.utcnow()

        db.add(
            ScanResultDB(
                check_id="iam_policy_wildcard_admin",
                resource_id="demo-role-1",
                status="fail",
                severity="critical",
                detail="Wildcard admin access.",
                scanned_at=timestamp,
            )
        )

        db.commit()

        report = build_report_data(db)

        roi_item = report["roi"]["items"][0]

        assert (
            roi_item["roi_interpretation"]
            == (
                "Modeled risk reduction per unit of "
                "assumed remediation cost."
            )
        )

        assert roi_item["roi_ratio"] is not None

    finally:
        db.close()