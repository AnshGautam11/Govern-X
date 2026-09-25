"""
SQLAlchemy ORM models — mirrors database/schema.sql's scan_results table.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
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
    severity = Column(String, nullable=True)
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

class GovernanceEvidenceDB(Base):
    """Supporting evidence attached to a governance questionnaire response."""

    __tablename__ = "governance_evidence"

    id = Column(Integer, primary_key=True, autoincrement=True)

    response_id = Column(
        Integer,
        ForeignKey("governance_responses.id"),
        nullable=False,
        index=True,
    )

    evidence_type = Column(
        String,
        nullable=False,
    )

    evidence_reference = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    added_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class AssetDB(Base):
    """Asset inventory entry — used by the Week 3 financial risk
    (Monte Carlo) model to map checks/resources to a dollar value and
    criticality tier."""

    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    criticality = Column(String, nullable=False, index=True)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class FinancialAssetDB(Base):
    """Backend persistent model for financial asset calculations."""

    __tablename__ = "financial_assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(String, unique=True, nullable=False, index=True)
    asset_name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    cloud_provider = Column(String, nullable=False)
    business_function = Column(String, nullable=False)
    data_sensitivity = Column(String, nullable=False)
    criticality = Column(String, nullable=False, index=True)
    asset_value = Column(Float, nullable=False)
    revenue_dependency = Column(Float, nullable=False, default=0.0)
    customer_dependency = Column(Float, nullable=False, default=0.0)
    recovery_cost = Column(Float, nullable=False, default=0.0)
    regulatory_exposure = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class GovernanceProfileDB(Base):
    """Persisted organization governance profile for Govern function scoring."""

    __tablename__ = "governance_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_name = Column(String, nullable=False, default="Demo Enterprise")
    industry = Column(String, nullable=False, default="Technology")
    organization_size = Column(String, nullable=False, default="500-1000 employees")
    security_policy_status = Column(String, nullable=False, default="Mostly implemented")
    cybersecurity_policy_review_frequency = Column(String, nullable=False, default="Quarterly")
    risk_management_policy = Column(String, nullable=False, default="Documented")
    access_control_policy = Column(String, nullable=False, default="Implemented")
    data_protection_policy = Column(String, nullable=False, default="Implemented")
    incident_response_policy = Column(String, nullable=False, default="Implemented")
    business_continuity_policy = Column(String, nullable=False, default="Implemented")
    vendor_supplier_security_policy = Column(String, nullable=False, default="Required")
    third_party_risk_management = Column(String, nullable=False, default="Formal review")
    security_awareness_training = Column(String, nullable=False, default="Quarterly")
    asset_ownership = Column(String, nullable=False, default="Assigned by business owners")
    risk_appetite = Column(String, nullable=False, default="Low to moderate")
    compliance_requirements = Column(Text, nullable=True)
    policy_owner = Column(String, nullable=False, default="CISO")
    last_policy_review_date = Column(String, nullable=False, default="2026-09-01")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)