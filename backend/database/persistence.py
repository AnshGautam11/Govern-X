"""
Persist scan results (from collectors/aws_collector.py) into the database
so that /scan/history (W2-Day2) can query past scans.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from database.db import Base, SessionLocal, engine
from database.models import (
    AssetDB,
    FinancialAssetDB,
    GovernanceProfileDB,
    GovernanceQuestionDB,
    GovernanceResponseDB,
    MockScenarioDB,
    ScanResultDB,
)
from models.schemas import CheckResult

# Ensure the scan_results table exists (safe to call repeatedly).
Base.metadata.create_all(bind=engine)

GOVERNANCE_QUESTIONS = [
    {
        "question_key": "risk_owner_assigned",
        "question_text": "Is a cybersecurity risk owner assigned at the leadership level?",
        "csf_category": "GV.RR",
    },
    {
        "question_key": "security_policy_reviewed",
        "question_text": "Has the organizational security policy been established and reviewed periodically?",
        "csf_category": "GV.PO",
    },
    {
        "question_key": "incident_response_plan_exists",
        "question_text": "Does the organization have an incident response plan?",
        "csf_category": "GV.OV",
    },
    {
        "question_key": "third_party_risk_reviewed",
        "question_text": "Is third-party and supply-chain cybersecurity risk reviewed?",
        "csf_category": "GV.SC",
    },
]

def ensure_governance_questions(db: Session | None = None) -> None:
    """Ensure the Week 3 governance questionnaire questions exist."""

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        for question_data in GOVERNANCE_QUESTIONS:
            existing = (
                db.query(GovernanceQuestionDB)
                .filter(
                    GovernanceQuestionDB.question_key
                    == question_data["question_key"]
                )
                .first()
            )

            if existing is None:
                db.add(
                    GovernanceQuestionDB(
                        question_key=question_data["question_key"],
                        question_text=question_data["question_text"],
                        csf_category=question_data["csf_category"],
                        active=True,
                    )
                )

        db.commit()

    finally:
        if owns_session:
            db.close()

def save_governance_responses(
    answers: dict[str, bool],
    db: Session | None = None,
) -> None:
    """Persist one questionnaire submission."""

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        ensure_governance_questions(db)

        questions = (
            db.query(GovernanceQuestionDB)
            .filter(
                GovernanceQuestionDB.question_key.in_(answers.keys())
            )
            .all()
        )

        question_map = {
            question.question_key: question
            for question in questions
        }

        for question_key, answer in answers.items():
            question = question_map.get(question_key)

            if question is None:
                raise ValueError(
                    f"Unknown governance question: {question_key}"
                )

            db.add(
                GovernanceResponseDB(
                    question_id=question.id,
                    answer=answer,
                )
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        if owns_session:
            db.close()

def get_latest_governance_responses(
    db: Session | None = None,
) -> list[tuple[GovernanceResponseDB, GovernanceQuestionDB]]:
    """Return the latest answer for each governance question."""

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        ensure_governance_questions(db)

        rows = (
            db.query(
                GovernanceResponseDB,
                GovernanceQuestionDB,
            )
            .join(
                GovernanceQuestionDB,
                GovernanceResponseDB.question_id
                == GovernanceQuestionDB.id,
            )
            .order_by(
                GovernanceResponseDB.answered_at.desc(),
                GovernanceResponseDB.id.desc(),
            )
            .all()
        )

        latest_by_question = {}
        
        for response, question in rows:
            if question.id not in latest_by_question:
                latest_by_question[question.id] = (
                    response,
                    question,
                )

        return list(latest_by_question.values())

    finally:
        if owns_session:
            db.close()

def save_scan_results(
    results: list[CheckResult],
    db: Session | None = None,
    scanned_at: datetime | None = None,
) -> None:
    """Write a batch of CheckResult objects to the scan_results table.

    All rows in one call share a single scanned_at timestamp (rather than
    each CheckResult's own microsecond-precision timestamp) so that one
    /scan/aws run is groupable as one "scan" — this is what W2-Day5's
    /scan/compare endpoint relies on to tell scans apart.
    """
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    batch_time = scanned_at or datetime.utcnow()

    try:

        if not results:
          return
    
        for result in results:
            db.add(
                ScanResultDB(
                    check_id=result.check_id,
                    resource_id=result.resource_id,
                    status=result.status.value,
                    detail=result.detail,
                    scanned_at=batch_time,
                )
            )
        db.commit()
    finally:
        if owns_session:
            db.close()

def get_scan_history(limit: int = 50, db: Session | None = None) -> list[ScanResultDB]:
    """Return the most recent scan_results rows, newest first."""
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        return (
            db.query(ScanResultDB)
            .order_by(ScanResultDB.scanned_at.desc())
            .limit(limit)
            .all()
        )
    finally:
        if owns_session:
            db.close()

def save_mock_scenario(
    scenario_name: str,
    results: list[CheckResult],
    db: Session | None = None,
) -> None:
    """Persist mock scenario findings for later lookup."""
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        for result in results:
            db.add(
                MockScenarioDB(
                    scenario_name=scenario_name,
                    check_id=result.check_id,
                    resource_id=result.resource_id,
                    status=result.status.value,
                    severity=result.severity.value,
                    detail=result.detail,
                )
            )
        db.commit()
    finally:
        if owns_session:
            db.close()


def get_mock_scenario(
    scenario_name: str,
    db: Session | None = None,
) -> list[CheckResult]:
    """Look up a mock scenario from the database as CheckResult objects."""
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        rows = (
            db.query(MockScenarioDB)
            .filter(MockScenarioDB.scenario_name == scenario_name)
            .order_by(MockScenarioDB.id)
            .all()
        )

        return [
            CheckResult(
                check_id=row.check_id,
                resource_id=row.resource_id,
                status=row.status,
                severity=row.severity,
                detail=row.detail,
            )
            for row in rows
        ]
    finally:
        if owns_session:
            db.close()

def get_latest_two_scan_timestamps(
    db: Session | None = None,
) -> list[datetime]:
    """Return up to the 2 most recent distinct scan timestamps."""

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        rows = (
            db.query(ScanResultDB.scanned_at)
            .distinct()
            .order_by(ScanResultDB.scanned_at.desc())
            .limit(2)
            .all()
        )

        return [row[0] for row in rows]

    finally:
        if owns_session:
            db.close()


def get_scan_by_timestamp(
    scanned_at: datetime,
    db: Session | None = None,
) -> list[ScanResultDB]:
    """Return all scan results belonging to one scan."""

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        return (
            db.query(ScanResultDB)
            .filter(
                ScanResultDB.scanned_at == scanned_at
            )
            .all()
        )

    finally:
        if owns_session:
            db.close()

def save_asset(
    name: str,
    value: float,
    criticality: str,
    db: Session | None = None,
) -> AssetDB:
    """Persist a new asset inventory entry (W3-Day2)."""
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        asset = AssetDB(name=name, value=value, criticality=criticality)
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset
    finally:
        if owns_session:
            db.close()


def get_all_assets(db: Session | None = None) -> list[AssetDB]:
    """Return every asset in the inventory, newest first (W3-Day2)."""
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        return db.query(AssetDB).order_by(AssetDB.created_at.desc()).all()
    finally:
        if owns_session:
            db.close()


def upsert_governance_profile(profile: dict, db: Session | None = None) -> GovernanceProfileDB:
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        profile_fields = {
            key: value for key, value in profile.items() if hasattr(GovernanceProfileDB, key)
        }
        if "compliance_requirements" in profile_fields:
            compliance_value = profile_fields["compliance_requirements"]
            if isinstance(compliance_value, list):
                profile_fields["compliance_requirements"] = ", ".join(compliance_value)

        existing = db.query(GovernanceProfileDB).first()
        if existing is None:
            record = GovernanceProfileDB(**profile_fields)
            db.add(record)
            db.commit()
            db.refresh(record)
            return record

        for key, value in profile_fields.items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    finally:
        if owns_session:
            db.close()


def get_governance_profile(db: Session | None = None) -> dict:
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        profile = db.query(GovernanceProfileDB).order_by(GovernanceProfileDB.id.desc()).first()
        if profile is None:
            from risk_engine.governance import mock_governance_profile
            payload = mock_governance_profile()
            upsert_governance_profile(payload, db=db)
            return payload

        compliance = profile.compliance_requirements or ""
        if isinstance(compliance, str):
            parsed = [item.strip() for item in compliance.split(",") if item.strip()]
        else:
            parsed = list(compliance or [])

        return {
            "organization_name": profile.organization_name,
            "industry": profile.industry,
            "organization_size": profile.organization_size,
            "security_policy_status": profile.security_policy_status,
            "cybersecurity_policy_review_frequency": profile.cybersecurity_policy_review_frequency,
            "risk_management_policy": profile.risk_management_policy,
            "access_control_policy": profile.access_control_policy,
            "data_protection_policy": profile.data_protection_policy,
            "incident_response_policy": profile.incident_response_policy,
            "business_continuity_policy": profile.business_continuity_policy,
            "vendor_supplier_security_policy": profile.vendor_supplier_security_policy,
            "third_party_risk_management": profile.third_party_risk_management,
            "security_awareness_training": profile.security_awareness_training,
            "asset_ownership": profile.asset_ownership,
            "risk_appetite": profile.risk_appetite,
            "compliance_requirements": parsed,
            "policy_owner": profile.policy_owner,
            "last_policy_review_date": profile.last_policy_review_date,
            "policy_coverage": 88.0,
            "supply_chain_risk": 32.5,
            "governance_control_coverage": 76.0,
            "governance_maturity": 81.0,
            "governance_gaps": [
                "Third-party contract security clauses require review",
                "Privileged access reviews are not fully quarterly",
            ],
            "critical_governance_controls": [
                "IAM least privilege",
                "Vendor security review",
                "Incident response readiness",
            ],
            "policy_review_status": "Current",
            "vendor_risk": [
                {
                    "vendor_name": "Cloud Monitoring Provider",
                    "vendor_type": "SaaS",
                    "criticality": "High",
                    "service_provided": "Telemetry ingestion",
                    "data_access": True,
                    "privileged_access": True,
                    "security_assessment_status": "Review pending",
                    "contract_security_requirements": "SOC 2 + MFA enforcement",
                    "last_assessment": "2026-08-20",
                    "risk_level": "Moderate",
                    "associated_technical_controls": ["IAM least privilege", "MFA enforcement"],
                }
            ],
            "control_mappings": [
                {
                    "policy": "Access Control Policy",
                    "governance_requirement": "Privileged access must be restricted",
                    "technical_control": "IAM least privilege",
                    "aws_finding": "Wildcard administrative policy detected",
                    "nist": "Govern / Protect",
                    "risk": "High",
                }
            ],
        }
    finally:
        if owns_session:
            db.close()


def save_financial_asset(asset: dict, db: Session | None = None) -> FinancialAssetDB:
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        record = db.query(FinancialAssetDB).filter(FinancialAssetDB.asset_id == asset["asset_id"]).first()
        if record is None:
            record = FinancialAssetDB(**asset)
            db.add(record)
        else:
            for key, value in asset.items():
                if hasattr(record, key):
                    setattr(record, key, value)
        db.commit()
        db.refresh(record)
        return record
    finally:
        if owns_session:
            db.close()


def get_financial_assets(db: Session | None = None) -> list[FinancialAssetDB]:
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        return db.query(FinancialAssetDB).order_by(FinancialAssetDB.created_at.desc()).all()
    finally:
        if owns_session:
            db.close()
