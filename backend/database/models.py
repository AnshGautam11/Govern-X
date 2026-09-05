"""
SQLAlchemy ORM models — mirrors database/schema.sql's scan_results table.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from database.db import Base


class ScanResultDB(Base):
    """One row per check result from a scan, with a timestamp for history."""

    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    check_id = Column(String, nullable=False, index=True)
    resource_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    detail = Column(Text)
    scanned_at = Column(DateTime, default=datetime.utcnow, index=True)