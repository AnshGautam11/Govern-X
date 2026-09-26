from database.db import Base, engine
from database.models import (
    FinancialAssetDB,
    GovernanceEvidenceDB,
    GovernanceProfileDB,
    GovernanceQuestionDB,
    GovernanceResponseDB,
)


def test_governance_question_model():
    assert GovernanceQuestionDB.__tablename__ == "governance_questions"
    assert GovernanceQuestionDB.question_key.property.columns[0].unique is True


def test_governance_response_model():
    assert GovernanceResponseDB.__tablename__ == "governance_responses"
    assert GovernanceResponseDB.question_id.property.columns[0].nullable is False
    assert GovernanceResponseDB.answer.property.columns[0].nullable is False


def test_governance_evidence_model():
    assert GovernanceEvidenceDB.__tablename__ == "governance_evidence"
    assert GovernanceEvidenceDB.response_id.property.columns[0].nullable is False


def test_governance_tables_registered():
    assert "governance_questions" in Base.metadata.tables
    assert "governance_responses" in Base.metadata.tables
    assert "governance_evidence" in Base.metadata.tables

def test_week3_financial_models_are_registered():
    assert FinancialAssetDB.__tablename__ == "financial_assets"
    assert FinancialAssetDB.asset_id.property.columns[0].unique is True
    assert FinancialAssetDB.asset_value.property.columns[0].nullable is False


def test_governance_profile_model_is_registered():
    assert GovernanceProfileDB.__tablename__ == "governance_profiles"
    assert GovernanceProfileDB.organization_name.property.columns[0].nullable is False
    assert GovernanceProfileDB.industry.property.columns[0].nullable is False