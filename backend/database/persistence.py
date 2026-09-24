"""
Persist scan results (from collectors/aws_collector.py) into the database
so that /scan/history (W2-Day2) can query past scans.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from database.db import Base, SessionLocal, engine
from database.models import (
    AssetDB,
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
