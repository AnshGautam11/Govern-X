"""
GovernX backend entrypoint.

Run locally:
    uvicorn app:app --reload --port 8000
"""

from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from compliance.scorer import get_tier, score_all_functions, score_overall
from models.schemas import (
    CheckResult,
    CheckStatus,
    DashboardMaturityResponse,
    MaturityOverview,
    PillarMaturity,
    ScanCompareResponse,
    ScanHistoryEntry,
    ScanHistoryResponse,
    ScanResponse,
    Severity,
)

settings = get_settings()

FUNCTION_ORDER = ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]
TIER_NAME_MAP = {
    "Tier 1": "Partial",
    "Tier 2": "Risk Informed",
    "Tier 3": "Repeatable",
    "Tier 4": "Adaptive",
    "No Data": "No Data",
}
STATUS_BY_TIER = {
    1: "Needs attention",
    2: "Risk informed",
    3: "Repeatable",
    4: "Adaptive",
    None: "No Data",
}


def _numeric_tier_for_score(score: float | None) -> int | None:
    if score is None:
        return None
    if score <= 25:
        return 1
    if score <= 50:
        return 2
    if score <= 75:
        return 3
    return 4


def _tier_name_for_score(score: float | None) -> str:
    return TIER_NAME_MAP.get(get_tier(score), "No Data")


def _build_findings_from_rows(rows):
    findings = []
    for row in rows:
        result = CheckResult(
            check_id=row.check_id,
            resource_id=row.resource_id,
            status=CheckStatus(row.status),
            severity=Severity.LOW,
            detail=row.detail,
            timestamp=row.scanned_at,
        )
        from mappings.csf_mappings import get_mapping

        mapping = get_mapping(result.check_id)
        if mapping is not None:
            findings.append(type("MappedFinding", (), {"result": result, "mapping": mapping})())
    return findings


def _build_maturity_payload(findings, previous_findings=None):
    scores = score_all_functions(findings)
    previous_scores = score_all_functions(previous_findings) if previous_findings else {}

    pillars = []
    for function_name in FUNCTION_ORDER:
        score_data = scores.get(function_name, {"score": None, "tier": "No Data"})
        percentage = score_data["score"]
        current_tier = _numeric_tier_for_score(percentage)
        tier_name = _tier_name_for_score(percentage)
        previous_score = previous_scores.get(function_name, {}).get("score")
        trend = 0 if previous_score is None else round(float(percentage or 0) - float(previous_score), 1)
        pillars.append(
            PillarMaturity(
                function=function_name,
                percentage=percentage,
                tier=current_tier,
                tier_name=tier_name,
                trend=trend,
                status=STATUS_BY_TIER.get(current_tier, "No Data"),
            )
        )

    overall_data = score_overall(findings)
    overall_percentage = overall_data["score"] if overall_data.get("score") is not None else 0
    overall_tier = _numeric_tier_for_score(overall_percentage)
    previous_overall = score_overall(previous_findings) if previous_findings else {"score": 0, "tier": "Tier 1"}
    overall_trend = round(float(overall_percentage) - float(previous_overall.get("score") or 0), 1)

    return DashboardMaturityResponse(
        overall=MaturityOverview(
            percentage=overall_percentage,
            tier=overall_tier,
            tier_name=_tier_name_for_score(overall_percentage),
            trend=overall_trend,
            status=STATUS_BY_TIER.get(overall_tier, "No Data"),
        ),
        pillars=pillars,
    )


app = FastAPI(
    title="GovernX API",
    description="Automated NIST CSF 2.0 compliance and risk quantification engine",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Basic liveness check."""
    return {"status": "ok", "service": "GovernX", "env": settings.environment}

@app.post("/scan/aws", response_model=ScanResponse)
def run_aws_scan():
    """
    Trigger the AWS collector, run all registered checks, map results to
    NIST CSF 2.0 subcategories, score maturity per function, and return
    the findings.

    Week 2: results are persisted (database/persistence.py) and scored
    (compliance/scorer.py) alongside the raw check results.
    """
    from collectors.aws_collector import run_all_checks
    from database.persistence import save_scan_results
    from mappings.csf_mappings import get_mapping
    from compliance.scorer import score_all_functions, score_overall
    from models.schemas import MappedFinding, FunctionScore

    try:
        results = run_all_checks()
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="AWS scan is currently unavailable. Check backend AWS permissions and configuration.",
        ) from exc

    save_scan_results(results)

    # Build MappedFinding objects for scoring — skip any check missing a
    # CSF mapping row rather than crashing the whole scan.
    findings = []
    for result in results:
        mapping = get_mapping(result.check_id)
        if mapping is not None:
            findings.append(MappedFinding(result=result, mapping=mapping))

    raw_scores = score_all_functions(findings)
    scores = {
        fn: FunctionScore(score=v["score"], tier=v["tier"])
        for fn, v in raw_scores.items()
    }
    raw_overall = score_overall(findings)
    overall = FunctionScore(score=raw_overall["score"], tier=raw_overall["tier"])

    from compliance.scorer import gap_analysis
    gaps = {
        fn: gap_analysis(findings, fn)
        for fn in scores.keys()
    }

    return ScanResponse(results=results, scores=scores, overall=overall, gaps=gaps)


@app.get("/scan/history", response_model=ScanHistoryResponse)
def scan_history(limit: int = 50):
    """
    Return the most recently persisted scan results, newest first.

    W2-Day2 (Sujal) — reads from the scan_results table written by
    /scan/aws (see database/persistence.py).
    """
    from database.persistence import get_scan_history

    rows = get_scan_history(limit=limit)

    entries = [
        ScanHistoryEntry(
            id=row.id,
            check_id=row.check_id,
            resource_id=row.resource_id,
            status=row.status,
            detail=row.detail,
            scanned_at=row.scanned_at,
        )
        for row in rows
    ]

    return ScanHistoryResponse(entries=entries)


@app.get("/scan/compare", response_model=ScanCompareResponse)
def scan_compare():
    """
    Compare the two most recent scans and report what changed.

    W2-Day5 (Sujal) — newly passing/failing checks between the current
    and previous scan, plus checks that appeared or disappeared entirely
    (e.g. a new S3 bucket, or a resource that was deleted).
    """
    from database.persistence import get_latest_two_scan_timestamps, get_scan_by_timestamp

    timestamps = get_latest_two_scan_timestamps()

    if len(timestamps) < 2:
        current_ts = timestamps[0] if timestamps else None
        current_rows = get_scan_by_timestamp(current_ts) if current_ts else []
        return ScanCompareResponse(
            current_scanned_at=current_ts,
            previous_scanned_at=None,
            newly_passing=[],
            newly_failing=[],
            unchanged=[row.check_id for row in current_rows],
            new_checks=[row.check_id for row in current_rows],
            removed_checks=[],
        )

    current_ts, previous_ts = timestamps[0], timestamps[1]
    current_rows = get_scan_by_timestamp(current_ts)
    previous_rows = get_scan_by_timestamp(previous_ts)

    current_status = {row.check_id: row.status for row in current_rows}
    previous_status = {row.check_id: row.status for row in previous_rows}

    current_ids = set(current_status)
    previous_ids = set(previous_status)

    newly_passing = []
    newly_failing = []
    unchanged = []

    for check_id in current_ids & previous_ids:
        was = previous_status[check_id]
        now = current_status[check_id]
        if was != "pass" and now == "pass":
            newly_passing.append(check_id)
        elif was == "pass" and now != "pass":
            newly_failing.append(check_id)
        else:
            unchanged.append(check_id)

    new_checks = sorted(current_ids - previous_ids)
    removed_checks = sorted(previous_ids - current_ids)

    return ScanCompareResponse(
        current_scanned_at=current_ts,
        previous_scanned_at=previous_ts,
        newly_passing=sorted(newly_passing),
        newly_failing=sorted(newly_failing),
        unchanged=sorted(unchanged),
        new_checks=new_checks,
        removed_checks=removed_checks,
    )


@app.get("/dashboard/maturity", response_model=DashboardMaturityResponse)
def dashboard_maturity():
    """Return a front-end-friendly maturity summary across the six NIST CSF functions."""
    from database.persistence import get_scan_history, save_scan_results

    try:
        from collectors.aws_collector import run_all_checks

        results = run_all_checks()
        save_scan_results(results)
        findings = []
        for result in results:
            from mappings.csf_mappings import get_mapping

            mapping = get_mapping(result.check_id)
            if mapping is not None:
                findings.append(type("MappedFinding", (), {"result": result, "mapping": mapping})())

        history = get_scan_history(limit=100)
        if history:
            grouped = defaultdict(list)
            for row in history:
                grouped[row.scanned_at].append(row)
            ordered_times = sorted(grouped.keys(), reverse=True)
            previous_rows = []
            if len(ordered_times) > 1:
                previous_rows = [
                    row for timestamp in [ordered_times[1]] for row in grouped[timestamp]
                ]
            current_payload = _build_maturity_payload(findings, _build_findings_from_rows(previous_rows))
            return current_payload
        return _build_maturity_payload(findings)
    except Exception as exc:
        history = get_scan_history(limit=100)
        if not history:
            raise HTTPException(
                status_code=503,
                detail="Unable to retrieve live maturity data. Check that the GovernX API is running.",
            ) from exc

        grouped = defaultdict(list)
        for row in history:
            grouped[row.scanned_at].append(row)
        ordered_times = sorted(grouped.keys(), reverse=True)
        latest_rows = [row for timestamp in [ordered_times[0]] for row in grouped[timestamp]]
        previous_rows = []
        if len(ordered_times) > 1:
            previous_rows = [
                row for timestamp in [ordered_times[1]] for row in grouped[timestamp]
            ]

        return _build_maturity_payload(_build_findings_from_rows(latest_rows), _build_findings_from_rows(previous_rows))
