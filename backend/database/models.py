"""
SQLAlchemy ORM models — mirrors database/schema.sql's scan_results table.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)

from database.db import Base


class ScanResultDB(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    check_id = Column(String, nullable=False, index=True)
    resource_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    detail = Column(Text)
    scanned_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    __table_args__ = (
        Index(
            "idx_scan_results_scanned_at_check_id",
            "scanned_at",
            "check_id",
        ),
    )

class CheckDB(Base):
    """ORM model for a GovernX security check."""

    __tablename__ = "checks"

    id = Column(String, primary_key=True)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)

class CSFMappingDB(Base):
    """ORM model linking a security check to a NIST CSF 2.0 subcategory."""

    __tablename__ = "csf_mappings"

    check_id = Column(
        String,
        ForeignKey("checks.id"),
        primary_key=True,
    )

    csf_function = Column(String, nullable=False)
    csf_subcategory = Column(String, nullable=False)
    justification = Column(Text, nullable=False)

class MockScenarioDB(Base):
    """Database-backed mock security scenario used for scoring demos/tests."""

    __tablename__ = "mock_scenarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scenario_name = Column(String, nullable=False, index=True)
    check_id = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    detail = Column(Text, nullable=False)

class GovernanceQuestionDB(Base):
    """Governance questionnaire question for NIST CSF 2.0 Govern function."""

    __tablename__ = "governance_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_key = Column(String, unique=True, nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    csf_category = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

class GovernanceResponseDB(Base):
    """Stored response to a Govern questionnaire question."""

    __tablename__ = "governance_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)

    question_id = Column(
        Integer,
        ForeignKey("governance_questions.id"),
        nullable=False,
        index=True,
    )

    answer = Column(Boolean, nullable=False)

    notes = Column(Text, nullable=True)

    answered_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )