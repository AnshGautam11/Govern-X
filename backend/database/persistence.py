"""
Persist scan results (from collectors/aws_collector.py) into the database
so that /scan/history (W2-Day2) can query past scans.
"""

from sqlalchemy.orm import Session

from database.db import Base, SessionLocal, engine
from database.models import MockScenarioDB, ScanResultDB
from models.schemas import CheckResult

# Ensure the scan_results table exists (safe to call repeatedly).
Base.metadata.create_all(bind=engine)


def save_scan_results(results: list[CheckResult], db: Session | None = None) -> None:
    """Write a batch of CheckResult objects to the scan_results table."""
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        for result in results:
            db.add(
                ScanResultDB(
                    check_id=result.check_id,
                    resource_id=result.resource_id,
                    status=result.status.value,
                    detail=result.detail,
                    scanned_at=result.timestamp,
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