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