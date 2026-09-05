"""
Persist scan results (from collectors/aws_collector.py) into the database
so that /scan/history (W2-Day2) can query past scans.
"""

from sqlalchemy.orm import Session

from database.db import Base, SessionLocal, engine
from database.models import ScanResultDB
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