"""
GovernX backend entrypoint.

Run locally:
    uvicorn app:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from models.schemas import ScanHistoryEntry, ScanHistoryResponse, ScanResponse
settings = get_settings()

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
