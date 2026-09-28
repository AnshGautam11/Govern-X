"""
Week 4 executive report data assembly.

The report joins persisted scan results, NIST mappings,
governance self-attestation, and the existing Monte Carlo
sample model without changing the Week 1-3 engines.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from compliance.scorer import score_all_functions, score_overall
from database.models import GovernanceQuestionDB
from database.persistence import (
    ensure_governance_questions,
    get_latest_governance_responses,
    get_latest_scan_results,
)
from mappings.csf_mappings import get_mapping
from models.schemas import CheckResult, CheckStatus, MappedFinding, Severity
from risk_engine.mock_data import MOCK_ASSET_DATA
from risk_engine.monte_carlo import run_monte_carlo, summarize


FUNCTION_ORDER = [
    "Govern",
    "Identify",
    "Protect",
    "Detect",
    "Respond",
    "Recover",
]

SEVERITY_WEIGHT = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}

# Synthetic/demo remediation cost assumptions.
# These are NOT real organizational costs.
ASSUMED_REMEDIATION_COST = {
    "critical": 25000.0,
    "high": 15000.0,
    "medium": 8000.0,
    "low": 4000.0,
}

# Synthetic/demo risk-reduction assumptions.
ASSUMED_RISK_REDUCTION = {
    "critical": 0.50,
    "high": 0.35,
    "medium": 0.20,
    "low": 0.10,
}


def _canonical_check_id(check_id: str) -> str:
    if get_mapping(check_id) is not None:
        return check_id

    candidate = check_id.removeprefix("check_")

    if get_mapping(candidate) is not None:
        return candidate

    return check_id


def _tier_for_score(score: float | None) -> tuple[int | None, str]:
    if score is None:
        return None, "No Data"

    if score <= 25:
        return 1, "Partial"

    if score <= 50:
        return 2, "Risk Informed"

    if score <= 75:
        return 3, "Repeatable"

    return 4, "Adaptive"


def _finding_dict(row: Any) -> dict[str, Any] | None:
    check_id = _canonical_check_id(row.check_id)

    mapping = get_mapping(check_id)

    if mapping is None:
        return None

    return {
        "id": row.id,
        "check_id": check_id,
        "resource_id": row.resource_id,
        "status": row.status,
        "severity": row.severity or "low",
        "detail": row.detail or "No detail recorded.",
        "csf_function": mapping.csf_function,
        "csf_subcategory": mapping.csf_subcategory,
        "remediation": mapping.justification,
        "scanned_at": row.scanned_at,
    }

def build_report_data(
    db: Session,
    sector: str = "financial",
) -> dict[str, Any]:
    """Build the complete executive report payload."""

    rows = get_latest_scan_results(db=db)

    # Keep only mapped findings for the executive report.
    # Unknown/stale check IDs should not appear as fake compliance gaps.
    findings = [
        finding
        for finding in (
            _finding_dict(row)
            for row in rows
    )
    if finding is not None
]

    ensure_governance_questions(db)

    governance_rows = get_latest_governance_responses(db=db)

    governance_total = (
        db.query(GovernanceQuestionDB)
        .filter(GovernanceQuestionDB.active.is_(True))
        .count()
    )

    governance_answered = len(governance_rows)

    governance_yes = sum(
        1
        for response, _ in governance_rows
        if response.answer
    )

    governance_score = (
        round(
            governance_yes / governance_total * 100,
            1,
        )
        if governance_total
        else None
    )

    failed_findings = [
        finding
        for finding in findings
        if finding["status"] == CheckStatus.FAIL.value
    ]

    remediation = prioritize_remediation(findings)

    if not rows:
        summary = {
            "overall_score": None,
            "tier": None,
            "tier_name": "No Data",
            "total_checks": None,
            "passed": None,
            "failed": None,
            "errors": None,
        }

        function_scores = {}

    else:
        mapped_objects = []

        for finding in findings:
            mapped_objects.append(
                MappedFinding(
                    result=CheckResult(
                        check_id=finding["check_id"],
                        resource_id=finding["resource_id"],
                        status=CheckStatus(
                            finding["status"]
                        ),
                        severity=Severity(
                            finding["severity"]
                        ),
                        detail=finding["detail"],
                        timestamp=finding["scanned_at"],
                    ),
                    mapping=get_mapping(
                        finding["check_id"]
                    ),
                )
            )

        maturity = score_overall(
            mapped_objects,
            governance_score=governance_score,
        )

        overall_score = maturity["score"]

        tier, tier_name = _tier_for_score(
            overall_score
        )

        function_scores = score_all_functions(
            mapped_objects,
            governance_score=governance_score,
        )

        summary = {
            "overall_score": overall_score,
            "tier": tier,
            "tier_name": tier_name,
            "total_checks": len(rows),
            "passed": sum(
                row.status == CheckStatus.PASS.value
                for row in rows
            ),
            "failed": sum(
                row.status == CheckStatus.FAIL.value
                for row in rows
            ),
            "errors": sum(
                row.status == CheckStatus.ERROR.value
                for row in rows
            ),
        }

    pillars = []

    for function_name in FUNCTION_ORDER:
        score_data = function_scores.get(
            function_name
        )

        score = (
            score_data.get("score")
            if score_data
            else None
        )

        tier, tier_name = _tier_for_score(score)

        pillars.append(
            {
                "function": function_name,
                "score": score,
                "tier": tier,
                "tier_name": tier_name,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc),
        "status": "ready" if rows else "no_data",
        "summary": summary,
        "pillars": pillars,
        "findings": findings,
        "data_notes": {
           "financial_data": "Sample/assumed data for demonstration purposes.",
           "governance_data": "Governance responses are self-attested questionnaire responses.",
           "scan_data": "Compliance findings are based on the available scan results."
        },
        "gaps": [
            {
                **finding,
                "affected_resources": [
                    finding["resource_id"]
                ],
            }
            for finding in failed_findings
        ],
        "remediation": remediation,
        "governance": {
            "answered": governance_answered,
            "total": governance_total,
            "score": governance_score,
            "completion": (
                round(
                    governance_answered
                    / governance_total
                    * 100,
                    1,
                )
                if governance_total
                else None
            ),
            "self_attested": True,
        },
        "roi": _build_roi(
            remediation,
            sector,
        ),
        "disclaimers": [
            "Financial figures are sample/assumed data carried forward from the Week 3 Monte Carlo model.",
            "Governance answers are self-attested questionnaire responses, not independently audited evidence.",
            "Board-ready refers to clear executive formatting and does not imply audit-grade accuracy.",
            "No Data is shown when no scan has been persisted; the report does not invent a percentage or maturity tier.",
        ],
    }

def prioritize_remediation(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Rank failed controls using:

        severity weight × number of failing resources
    """

    grouped = {}

    for finding in findings:

        if finding["status"] != CheckStatus.FAIL.value:
            continue

        check_id = finding["check_id"]

        item = grouped.setdefault(
            check_id,
            {
                "check_id": check_id,
                "title": check_id.replace(
                    "_",
                    " ",
                ).title(),
                "severity": finding["severity"],
                "affected_resources": [],
                "csf_function": finding["csf_function"],
                "csf_subcategory": finding[
                    "csf_subcategory"
                ],
                "remediation": finding[
                    "remediation"
                ],
            },
        )

        item["affected_resources"].append(
            finding["resource_id"]
        )

        current_weight = SEVERITY_WEIGHT.get(
            finding["severity"],
            1,
        )

        existing_weight = SEVERITY_WEIGHT.get(
            item["severity"],
            1,
        )

        if current_weight > existing_weight:
            item["severity"] = finding[
                "severity"
            ]

    ranked = []

    for item in grouped.values():

        weight = SEVERITY_WEIGHT.get(
            item["severity"],
            1,
        )

        resource_count = len(
            item["affected_resources"]
        )

        priority_score = (
            weight * resource_count
        )

        ranked.append(
            {
                **item,
                "resource_count": resource_count,
                "priority_score": priority_score,
            }
        )

    ranked.sort(
        key=lambda item: (
            -item["priority_score"],
            -SEVERITY_WEIGHT.get(
                item["severity"],
                1,
            ),
            item["check_id"],
        )
    )

    for index, item in enumerate(
        ranked,
        start=1,
    ):
        item["rank"] = index

    return ranked

def _sample_roi_for_remediation(
    remediation: dict[str, Any],
    sector: str,
) -> dict[str, Any]:

    parameters = (
        MOCK_ASSET_DATA.get(sector)
        or MOCK_ASSET_DATA["financial"]
    )

    baseline_losses = run_monte_carlo(
        iterations=5000,
        seed=42,
        **parameters,
    )

    baseline = summarize(
        baseline_losses
    )

    severity = remediation["severity"]

    reduction = ASSUMED_RISK_REDUCTION.get(
        severity,
        0.10,
    )

    low, high = parameters[
        "exposure_factor_range"
    ]

    remediated_range = (
        max(
            0.0,
            low * (1 - reduction),
        ),
        max(
            0.0,
            high * (1 - reduction),
        ),
    )

    remediated_losses = run_monte_carlo(
        iterations=5000,
        seed=42,
        asset_value_range=parameters[
            "asset_value_range"
        ],
        exposure_factor_range=remediated_range,
        annual_rate_of_occurrence=parameters[
            "annual_rate_of_occurrence"
        ],
    )

    remediated = summarize(
        remediated_losses
    )

    risk_reduced = max(
        0.0,
        baseline["expected"]
        - remediated["expected"],
    )

    cost = ASSUMED_REMEDIATION_COST.get(
        severity,
        4000.0,
    )

    return {
        "check_id": remediation["check_id"],
        "rank": remediation["rank"],
        "baseline_expected_loss": round(
            baseline["expected"],
            2,
        ),
        "remediated_expected_loss": round(
            remediated["expected"],
            2,
        ),
        "risk_reduced": round(
            risk_reduced,
            2,
        ),
        "assumed_remediation_cost": cost,
        "roi_ratio": round(
            risk_reduced / cost,
            2,
        )
        if cost
        else None,
        "assumptions": {
            "severity": severity,
            "risk_reduction_percent": round(
                reduction * 100,
                1,
            ),
            "sector": sector,
            "data_quality": "assumed_sample_data",
        },
    }


def _build_roi(
    remediations: list[dict[str, Any]],
    sector: str,
) -> dict[str, Any]:

    if not remediations:
        return {
            "status": "no_gap_data",
            "sector": sector,
            "items": [],
            "message": (
                "No failed controls are available "
                "for remediation ROI modeling."
            ),
        }

    return {
        "status": "sample_only",
        "sector": sector,
        "items": [
            _sample_roi_for_remediation(
                item,
                sector,
            )
            for item in remediations[:5]
        ],
        "formula": (
            "ROI ratio = modeled risk reduction "
            "/ assumed remediation cost."
        ),
        "message": (
            "Financial figures use assumed sample "
            "inputs from the existing Monte Carlo "
            "model and must not be interpreted as "
            "audit-grade or real organizational figures."
        ),
    }