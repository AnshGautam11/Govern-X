from database.db import Base, engine
from database.models import (
    GovernanceEvidenceDB,
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