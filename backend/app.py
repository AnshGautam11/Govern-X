"""
GovernX backend entrypoint.

Run locally:
    uvicorn app:app --reload --port 8000
"""

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from database.db import get_db
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from compliance.scorer import get_tier, score_all_functions, score_overall
from models.schemas import (
    AssetCreateRequest,
    AssetListResponse,
    AssetResponse,
    CheckResult,
    CheckStatus,
    DashboardMaturityResponse,
    GovernanceAnswerResponse,
    GovernanceProfile,
    GovernanceResponseRequest,
    GovernanceResponsesResponse,
    MaturityOverview,
    PillarMaturity,
    ScanCompareResponse,
    ScanHistoryEntry,
    ScanHistoryResponse,
    ScanResponse,
    RiskAssessmentRequest,
    RiskAssessmentResponse,
    Severity,
    FinancialAssetCreateRequest,
    FinancialAssetResponse,
    FinancialRiskCalculationRequest,
    FinancialRiskCalculationResponse,
    FinancialSummaryResponse,
    RiskHistoryEntry,
    RiskHistoryResponse,
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


def _get_scan_results_with_fallback():
    """Try real AWS collector first; fallback to mock environment or default check results if AWS fails."""
    try:
        from collectors.aws_collector import run_all_checks
        return run_all_checks()
    except Exception as exc:
        print(f"[DEBUG] AWS collector failed ({exc}). Falling back to mock environment...")
        
        # Fallback 1: Try importing from mock_aws module
        try:
            from mock_aws.environment import run_all_checks as mock_run_all
            return mock_run_all()
        except Exception:
            pass

        try:
            from mock_aws.scanner import run_all_checks as mock_run_all
            return mock_run_all()
        except Exception:
            pass

        # Fallback 2: Direct Mock Data if mock_aws module structure varies
        return [
            CheckResult(
                check_id="check_s3_encryption_at_rest",
                resource_id="arn:aws:s3:::govern-x-mock-bucket",
                status=CheckStatus.PASS,
                severity=Severity.LOW,
                detail="S3 bucket encryption is active (Mock Data)",
                timestamp=datetime.now(timezone.utc),
            ),
            CheckResult(
                check_id="check_ebs_encryption",
                resource_id="vol-0123456789abcdef0",
                status=CheckStatus.PASS,
                severity=Severity.LOW,
                detail="EBS volume is encrypted (Mock Data)",
                timestamp=datetime.now(timezone.utc),
            ),
        ]


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


@app.get("/governance/questions")
def list_governance_questions():
    """Return the default governance questionnaire used by the frontend."""
    from risk_engine.governance import mock_governance_profile

    profile = mock_governance_profile()
    return [
        {
            "id": "GV-01",
            "category": "Govern",
            "question": "Is the organization security policy formally defined and reviewed?",
            "type": "yes_no",
            "required": True,
            "weight": 5,
            "answer": profile.get("security_policy_status") == "Mostly implemented",
        },
        {
            "id": "GV-02",
            "category": "Govern",
            "question": "Is a cybersecurity risk owner assigned at the leadership level?",
            "type": "yes_no",
            "required": True,
            "weight": 5,
            "answer": True,
        },
        {
            "id": "GV-03",
            "category": "Govern",
            "question": "Does the organization review third-party supply-chain risk?",
            "type": "yes_no",
            "required": True,
            "weight": 5,
            "answer": profile.get("third_party_risk_management") == "Formal review",
        },
        {
            "id": "GV-04",
            "category": "Govern",
            "question": "Is the incident response plan reviewed and tested?",
            "type": "yes_no",
            "required": True,
            "weight": 5,
            "answer": True,
        },
    ]


@app.get("/governance/profile", response_model=GovernanceProfile)
def get_governance_profile(db=Depends(get_db)):
    """Return the organization governance profile used for the Govern pillar."""
    from database.persistence import get_governance_profile

    profile = get_governance_profile(db=db)
    return GovernanceProfile(**profile)


@app.post(
    "/governance/responses",
    response_model=GovernanceResponsesResponse,
    status_code=201,
)
def submit_governance_responses(
    payload: GovernanceResponseRequest,
    db=Depends(get_db),
):
    """Store governance questionnaire responses."""

    from database.persistence import save_governance_responses

    answers = payload.model_dump()

    try:
        save_governance_responses(
            answers=answers,
            db=db,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except Exception as exc:
       raise HTTPException(
           status_code=500,
           detail="Unable to save governance responses.",
        ) from exc

    return get_governance_responses(db)


@app.post("/governance/assessment")
def submit_governance_assessment(payload: dict[str, Any], db=Depends(get_db)):
    """Compatibility endpoint for the frontend governance questionnaire."""
    answers = payload.get("answers") if isinstance(payload, dict) and isinstance(payload.get("answers"), dict) else payload
    if not isinstance(answers, dict):
        raise HTTPException(status_code=400, detail="Expected an 'answers' object.")

    normalized = {}
    for key, value in answers.items():
        if isinstance(value, str):
            normalized[key] = value.lower() in {"yes", "true", "complete", "implemented", "partially"}
        elif isinstance(value, bool):
            normalized[key] = value
        elif value is None:
            normalized[key] = False
        else:
            normalized[key] = bool(value)

    from database.persistence import save_governance_responses
    try:
        save_governance_responses(answers=normalized, db=db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "submitted", "answers": normalized}


@app.post(
    "/assets",
    response_model=AssetResponse,
    status_code=201,
)
def create_asset(
    payload: AssetCreateRequest,
    db=Depends(get_db),
):
    """Add a new asset to the inventory (W3-Day2, Sujal)."""

    from database.persistence import save_asset

    try:
        asset = save_asset(
            name=payload.name,
            value=payload.value,
            criticality=payload.criticality,
            db=db,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to save asset.",
        ) from exc

    return AssetResponse(
        id=asset.id,
        name=asset.name,
        value=asset.value,
        criticality=asset.criticality,
        created_at=asset.created_at,
    )


@app.get("/assets", response_model=AssetListResponse)
def list_assets(db=Depends(get_db)):
    """Return the full asset inventory, newest first (W3-Day2, Sujal)."""

    from database.persistence import get_all_assets

    rows = get_all_assets(db=db)

    assets = [
        AssetResponse(
            id=row.id,
            name=row.name,
            value=row.value,
            criticality=row.criticality,
            created_at=row.created_at,
        )
        for row in rows
    ]

    return AssetListResponse(assets=assets)


@app.post("/scan/aws", response_model=ScanResponse)

def run_aws_scan():
    """
    Trigger the AWS collector (or fallback to Mock AWS), run all registered checks,
    map results to NIST CSF 2.0 subcategories, score maturity per function, and return findings.
    """
    from database.persistence import save_scan_results
    from mappings.csf_mappings import get_mapping
    from compliance.scorer import score_all_functions, score_overall, gap_analysis
    from models.schemas import MappedFinding, FunctionScore

    results = _get_scan_results_with_fallback()
    save_scan_results(results)

    # Build MappedFinding objects for scoring
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

    gaps = {
        fn: gap_analysis(findings, fn)
        for fn in scores.keys()
    }

    overall_score = raw_overall["score"]
    numeric_tier = _numeric_tier_for_score(overall_score)
    return ScanResponse(
        results=results,
        scores=scores,
        overall=overall,
        gaps=gaps,
        scan_id=str(uuid4()),
        timestamp=datetime.now(timezone.utc),
        findings=findings,
        nist_mapping=[finding.mapping for finding in findings],
        pillar_scores=scores,
        overall_score=overall_score,
        overall_tier=numeric_tier,
        tier_name=TIER_NAME_MAP.get(raw_overall["tier"], "No Data"),
    )


@app.post("/risk/assess", response_model=RiskAssessmentResponse)
def assess_financial_risk(payload: RiskAssessmentRequest):
    """Run the documented Monte Carlo assessment for a supported scenario."""
    from risk_engine.mock_data import MOCK_ASSET_DATA
    from risk_engine.monte_carlo import (
        distribution_percentages,
        run_monte_carlo,
        summarize,
    )

    parameters = MOCK_ASSET_DATA.get(payload.sector)
    if parameters is None:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported risk assessment sector: {payload.sector}",
        )

    iterations = settings.monte_carlo_iterations
    losses = run_monte_carlo(iterations=iterations, **parameters)
    summary = summarize(losses)

    return RiskAssessmentResponse(
        sector=payload.sector,
        **summary,
        iterations=iterations,
        confidence_level=0.9,
        distribution=distribution_percentages(losses),
        generated_at=datetime.now(timezone.utc),
        data_quality="assumed_sample_data",
        disclaimer=(
            "Asset values and occurrence rates are assumed sample inputs, "
            "not real organizational figures."
        ),
    )


@app.get("/risk/assets")
def list_risk_assets(db=Depends(get_db)):
    """Return asset records used in the financial risk model."""
    from database.persistence import get_financial_assets, save_financial_asset
    from risk_engine.financial_risk import FINANCIAL_ASSET_LIBRARY

    rows = get_financial_assets(db=db)
    if not rows:
        for asset in FINANCIAL_ASSET_LIBRARY:
            save_financial_asset(asset, db=db)
        rows = get_financial_assets(db=db)

    return [
        FinancialAssetResponse(
            asset_id=row.asset_id,
            asset_name=row.asset_name,
            asset_type=row.asset_type,
            cloud_provider=row.cloud_provider,
            business_function=row.business_function,
            data_sensitivity=row.data_sensitivity,
            criticality=row.criticality,
            asset_value=row.asset_value,
            revenue_dependency=row.revenue_dependency,
            customer_dependency=row.customer_dependency,
            recovery_cost=row.recovery_cost,
            regulatory_exposure=row.regulatory_exposure,
        ).model_dump()
        for row in rows
    ]


@app.post("/risk/assets", response_model=FinancialAssetResponse, status_code=201)
def create_risk_asset(payload: FinancialAssetCreateRequest, db=Depends(get_db)):
    """Persist a financial asset used for financial exposure calculations."""
    from database.persistence import save_financial_asset

    asset_payload = payload.model_dump()
    saved = save_financial_asset(asset_payload, db=db)
    return FinancialAssetResponse(
        asset_id=saved.asset_id,
        asset_name=saved.asset_name,
        asset_type=saved.asset_type,
        cloud_provider=saved.cloud_provider,
        business_function=saved.business_function,
        data_sensitivity=saved.data_sensitivity,
        criticality=saved.criticality,
        asset_value=saved.asset_value,
        revenue_dependency=saved.revenue_dependency,
        customer_dependency=saved.customer_dependency,
        recovery_cost=saved.recovery_cost,
        regulatory_exposure=saved.regulatory_exposure,
    )


@app.get("/risk/financial-summary", response_model=FinancialSummaryResponse)
def get_financial_summary(db=Depends(get_db)):
    """Return the aggregated exposure based on the inventoried assets and findings."""
    from database.persistence import get_financial_assets
    from risk_engine.financial_risk import summarize_financial_risk

    rows = get_financial_assets(db=db)
    if not rows:
        snapshot = summarize_financial_risk()
    else:
        total = sum(float(row.asset_value) for row in rows)
        findings = [
            {
                "asset_name": row.asset_name,
                "check_id": "iam_policy_wildcard_admin",
                "estimated_loss": round(float(row.asset_value) * 0.35, 2),
                "risk_level": "high" if row.criticality in {"high", "critical"} else "medium",
            }
            for row in rows
        ]
        snapshot = {
            "total_asset_value": total,
            "estimated_financial_exposure": round(sum(item["estimated_loss"] for item in findings), 2),
            "potential_loss": round(sum(item["estimated_loss"] for item in findings) * 0.7, 2),
            "high_risk_assets": sum(1 for item in findings if item["risk_level"] in {"high", "critical"}),
            "critical_control_failures": len(findings),
            "assets": [
                {
                    "asset_id": row.asset_id,
                    "asset_name": row.asset_name,
                    "asset_type": row.asset_type,
                    "cloud_provider": row.cloud_provider,
                    "business_function": row.business_function,
                    "data_sensitivity": row.data_sensitivity,
                    "criticality": row.criticality,
                    "asset_value": row.asset_value,
                    "revenue_dependency": row.revenue_dependency,
                    "customer_dependency": row.customer_dependency,
                    "recovery_cost": row.recovery_cost,
                    "regulatory_exposure": row.regulatory_exposure,
                }
                for row in rows
            ],
            "findings": findings,
            "generated_at": datetime.now(timezone.utc),
        }

    return FinancialSummaryResponse(
        total_asset_value=snapshot["total_asset_value"],
        estimated_financial_exposure=snapshot["estimated_financial_exposure"],
        potential_loss=snapshot["potential_loss"],
        high_risk_assets=snapshot["high_risk_assets"],
        critical_control_failures=snapshot["critical_control_failures"],
        assets=snapshot.get("assets", []),
        findings=snapshot.get("findings", []),
        generated_at=snapshot.get("generated_at", datetime.now(timezone.utc)),
    )


@app.get("/risk/findings")
def list_risk_findings():
    """Return finding-to-financial-impact mappings for the current inventory."""
    from risk_engine.financial_risk import summarize_financial_risk

    summary = summarize_financial_risk()
    return summary["findings"]


@app.get("/risk/findings/{finding_id}")
def get_risk_finding(finding_id: str):
    """Return the financial impact tied to one known finding."""
    from risk_engine.financial_risk import summarize_financial_risk

    for finding in summarize_financial_risk()["findings"]:
        if finding["check_id"] == finding_id:
            return finding
    raise HTTPException(status_code=404, detail=f"Finding not found: {finding_id}")


@app.post("/risk/calculate", response_model=FinancialRiskCalculationResponse)
def calculate_risk(payload: FinancialRiskCalculationRequest):
    """Calculate SLE/ALE for a specific asset and finding using the configured risk model."""
    from risk_engine.financial_risk import calculate_risk_for_finding

    result = calculate_risk_for_finding(
        check_id=payload.check_id,
        asset_value=payload.asset_value,
        exposure_factor=payload.exposure_factor,
        annual_rate_of_occurrence=payload.annual_rate_of_occurrence,
        asset_name=payload.asset_name,
    )
    return FinancialRiskCalculationResponse(
        check_id=result["check_id"],
        asset_name=result["asset_name"],
        control=result["control"],
        asset_value=result["asset_value"],
        exposure_factor=result["exposure_factor"],
        likelihood=result["likelihood"],
        sle=result["sle"],
        aro=result["aro"],
        ale=result["ale"],
        estimated_loss=result["estimated_loss"],
        risk_level=result["risk_level"],
        nist_function=result["nist_function"],
    )


@app.get("/risk/history", response_model=RiskHistoryResponse)
def risk_history():
    """Return a compact history sleeve for financial risk trending."""
    from risk_engine.financial_risk import summarize_financial_risk

    snapshot = summarize_financial_risk()
    return RiskHistoryResponse(
        history=[
            RiskHistoryEntry(
                timestamp=snapshot["generated_at"],
                label="Current exposure",
                total_asset_value=snapshot["total_asset_value"],
                estimated_financial_exposure=snapshot["estimated_financial_exposure"],
                high_risk_assets=snapshot["high_risk_assets"],
            )
        ]
    )


@app.get(
    "/governance/responses",
    response_model=GovernanceResponsesResponse,
)
def get_governance_responses(
    db=Depends(get_db),
):
    """Return the latest governance questionnaire responses."""

    from database.persistence import get_latest_governance_responses

    rows = get_latest_governance_responses(db=db)

    responses = [
        GovernanceAnswerResponse(
            id=response.id,
            question_id=question.id,
            question_key=question.question_key,
            question_text=question.question_text,
            csf_category=question.csf_category,
            answer=response.answer,
            notes=response.notes,
            answered_at=response.answered_at,
        )
        for response, question in rows
    ]

    return GovernanceResponsesResponse(
        responses=responses,
    )


@app.get("/scan/history", response_model=ScanHistoryResponse)
def scan_history(
    limit: int = Query(
        default=50,
        gt=0,
        le=500,
        description="Max number of scan results to return (1-500).",
    )
):

    """
    Return the most recently persisted scan results, newest first.
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
        results = _get_scan_results_with_fallback()
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