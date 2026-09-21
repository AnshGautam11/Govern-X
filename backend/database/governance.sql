-- GovernX Week 3 Day 1
-- Governance questionnaire database schema

CREATE TABLE IF NOT EXISTS governance_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_key TEXT NOT NULL UNIQUE,
    question_text TEXT NOT NULL,
    csf_category TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS governance_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer BOOLEAN NOT NULL,
    notes TEXT,
    answered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES governance_questions(id)
);

CREATE TABLE IF NOT EXISTS governance_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL,
    evidence_type TEXT NOT NULL,
    evidence_reference TEXT NOT NULL,
    description TEXT,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (response_id) REFERENCES governance_responses(id)
);

CREATE INDEX IF NOT EXISTS idx_governance_questions_key
ON governance_questions(question_key);

CREATE INDEX IF NOT EXISTS idx_governance_responses_question
ON governance_responses(question_id);

CREATE INDEX IF NOT EXISTS idx_governance_responses_answered_at
ON governance_responses(answered_at);

CREATE INDEX IF NOT EXISTS idx_governance_evidence_response
ON governance_evidence(response_id);